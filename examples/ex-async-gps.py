#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@riseup.net>
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
GPS example.

Requires running `gpsd` daemon.
"""

import asyncio
import functools
import logging
import json
import redis

logging.basicConfig(level=logging.DEBUG)

import geotiler
from geotiler.cache import redis_downloader

client = redis.Redis('localhost')
downloader = redis_downloader(client)
render_map_async = functools.partial(
    geotiler.render_map_async, downloader=downloader
)

@asyncio.coroutine
def read_gps(queue):
    """
    Read location data from `gpsd` daemon.
    """
    reader, writer = yield from asyncio.open_connection(port=2947)
    writer.write(b'?WATCH={"enable":true,"json":true}\n')
    while True:
        line = yield from reader.readline()
        data = json.loads(line.decode())
        if 'lon' in data:
            yield from queue.put((data['lon'], data['lat']))
        

@asyncio.coroutine
def show_map(queue, map):
    """
    Save map centered at location to a file.
    """
    while True:
        pos = yield from queue.get()

        map.center = pos
        img = yield from render_map_async(map)
        img.save('ex-async-gps.png', 'png')


size = 800, 800
start = 0, 0
mm = geotiler.Map(size=size, center=start, zoom=16)

queue = asyncio.Queue(1)        # queue holding current position from gpsd

# run location and map rendering tasks concurrently
t1 = show_map(queue, mm)
t2 = read_gps(queue)
task = asyncio.gather(t1, t2)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)

# vim: sw=4:et:ai
