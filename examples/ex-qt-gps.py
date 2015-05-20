#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2015 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

"""
Read data from GPS and show map centered at the position.

1. The last 120 positions are stored in a queue and plotted on the map.
2. Use keys like '+', '-', 'n', 'p' to zoom in, zoom out and change map
   provider.

Requirements:

- geotiler
- quamash
- PyQt 5
"""

import asyncio
import functools
import json
import logging
import redis
import sys
from collections import deque

import PIL.ImageDraw
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QProgressBar, QLabel
from PyQt5.QtGui import QPixmap, QImage
from quamash import QEventLoop, QThreadExecutor

import geotiler
from geotiler.cache import redis_downloader

logging.getLogger('geotiler').setLevel(logging.DEBUG)
logging.basicConfig()

# use redis to cache map tiles
client = redis.Redis('localhost')
downloader = redis_downloader(client)
render_map = functools.partial(
    geotiler.render_map_async, downloader=downloader
)


@asyncio.coroutine
def read_gps(event, positions):
    """
    Read postion from gpsd daemon and put it to positions queue.

    The map rendering event is set when a position is put to the queue.

    :param event: Map rendering event.
    :param positions: Queue of positions.
    """
    reader, writer = yield from asyncio.open_connection(port=2947)
    writer.write('?WATCH={"enable":true,"json":true}\n'.encode())
    while True:
        line = yield from reader.readline()
        data = json.loads(line.decode())
        if 'lon' in data:
            positions.append((data['lon'], data['lat']))
            event.set()



def update_image(widget, img, positions):
    """
    Update map widget with new map image.

    The positions are rendered on the map image as well.

    :param widget: Map widget.
    :param img: New map image.
    :param positions: Collection of positions.
    """
    map = widget.map
    pos = positions[-1]
    draw = PIL.ImageDraw.Draw(img)
    msg = '{:.6f},{:.6f}'.format(*pos)
    tw, th = draw.textsize(msg)
    width, height = map.size
    draw.text(((width - tw), (height - th)), msg, 'red')

    x, y = width / 2, height / 2
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), outline='green')

    points = [map.rev_geocode(p) for p in positions]
    draw.point(points, fill='blue')

    qimg = ImageQt(img)
    pixmap = QPixmap.fromImage(qimg)
    widget.setPixmap(pixmap)


@asyncio.coroutine
def update_map(map, pos, size):
    """
    Update map center with position, change map size and download new map
    image.

    :param map: Geotiler map object.
    :param pos: New center of the map (longitude, latitude).
    :param size: New size of map image (width, height).
    """
    map.center = pos
    map.size = size
    img = yield from render_map(map)
    return img
    

@asyncio.coroutine
def show_map(event, executor, widget, positions):
    """
    This is asyncio coroutine.

    :param event: Map rendering event.
    :param executor: Executor running map update in the map widget.
    :param widget: Map widget.
    :param positions: Queue of positions obtained from GPS.
    """
    map = widget.map
    while True:
        yield from event.wait()
        event.clear()
        if not positions:
            continue

        pos = positions[-1]
        size = widget.map_size
        img = yield from update_map(map, pos, size)
        yield from loop.run_in_executor(executor, update_image, widget, img, positions)


class MapWindow(QLabel):
    """
    Qt widget based on QLabel to display map image and control application
    with keyboard.
    """
    def __init__(self, map, event, *args):
        super().__init__(*args)
        self.map = map
        self.event = event
        self.providers = deque([
            'osm', 'osm-cycle', 'stamen-terrain', 'stamen-toner-lite', 'stamen-toner',
            'stamen-watercolor', 'ms-aerial', 'ms-hybrid', 'ms-road', 'bluemarble',
        ])

    @property
    def map_size(self):
        """
        Get size of the map image window.
        """
        size = self.size()
        return size.width(), size.height()


    def keyPressEvent(self, event):
        """
        Handle key press events

        - '-' to zoom out
        - '+'/'=' to zoom in
        - 'n' to use next map provider
        - 'p' to use previous map provider
        - 'q' to quit
        
        """
        key = event.key()
        if key == QtCore.Qt.Key_Minus:
            self.map.zoom -= 1
        elif key == QtCore.Qt.Key_Plus or key == QtCore.Qt.Key_Equal:
            self.map.zoom += 1
        elif key == QtCore.Qt.Key_Q:
            loop.stop()
        elif key == QtCore.Qt.Key_N:
            self.providers.rotate(-1)
            p = self.providers[0]
            self.map.provider = geotiler.find_provider(p)
        elif key == QtCore.Qt.Key_P:
            self.providers.rotate(1)
            p = self.providers[0]
            self.map.provider = geotiler.find_provider(p)
        self.event.set()


    def resizeEvent(self, event):
        """
        On resize event redraw the map.
        """
        self.event.set()



size = 800, 800
start = 0, 0
provider = geotiler.find_provider('osm')
mm = geotiler.Map(size=size, center=start, zoom=19, provider=provider)

# bind Qt application with Python asyncio loop
app = QApplication(sys.argv)
loop = QEventLoop(app)
qt_exec = QThreadExecutor()
asyncio.set_event_loop(loop)

event = asyncio.Event() # map rendering event, set the event to redraw the map
window = MapWindow(mm, event)
window.show()

positions = deque([], maxlen=120)
t1 = show_map(event, qt_exec, window, positions)
t2 = read_gps(event, positions)
task = asyncio.gather(t1, t2)

loop.run_until_complete(task)
