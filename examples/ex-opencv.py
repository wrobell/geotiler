#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@pld-linux.org>
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
Create an object containing a GeoTiler object and convert the resulting
image to an OpenCV image in order to show it. Also contains functions to
plot points on the resulting map.

Zooming is possible with the mousewheel and `+` and `-` keys.

Requirements

- geotiler
- opencv
- numpy (also required by OpenCV)

Example provided by `https://github.com/matthijs876`.
"""

import geotiler
import cv2
import numpy as np


RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)


class MapObject:
    def __init__(self, center: tuple=(0.0, 51.47879),
                 zoom: int=15, size: tuple=(1900, 1000)):
        """
            MapObject constructor
            Creates a open cv compatible map image of requested size,
            zoom level and coordinates.
            After creating the object the map can be displayed using
            cv2.imShow('window name',MapObject.img) and cv2.waitKey(10)
            Keyword arguments:
                center (Optional[tuple]) -- center coordinates of the map tuple
                (lon,lat) (default 0.0,51.47879) (Greenwich)
                zoom (Optional[int]) -- zoom level of the map, int between
                3 and 19 (default 15)
                size (Optional[int]) -- resolution of the resulting image
                (default (1900,1000)) (good for full HD monitor)
        """
        self.mm = geotiler.Map(center=center, zoom=zoom, size=size)
        self.mapmarkers = []
        self.updatemap()

    def updatemap(self):
        """
            Download new maptiles and redraw everyting on the map
        """
        self.pilImage = geotiler.render_map(self.mm)
        self.drawMap()

    def drawMap(self):
        """
            Draw the map again, to redownload the maptiles use updatemap()
            If you want to draw things on the map, call your function from here
        """
        self.img = cv2.cvtColor(np.array(self.pilImage)[:, :, :3],
                                cv2.COLOR_RGB2BGR)
        self.plotPoint(self.mapmarkers)

    def zoomIn(self):
        """
            Zoom in, this functions downloads a new map
        """
        if self.mm.zoom < 19:
            self.mm.zoom += 1
        self.updatemap()

    def zoomOut(self):
        """
            Zoom out, this function dowmloads a new map
        """
        if self.mm.zoom > 3:
            self.mm.zoom -= 1
        self.updatemap()

    def plotPoint(self, markers):
        """
            Draws a circle at all the points in the list self.mapmarkers[]
        """
        for lon, lat in markers:
            x, y = self.mm.rev_geocode((lon, lat))
            cv2.circle(self.img, center=(int(x), int(y)), radius=5,
                       color=RED, thickness=-1)

    def mouse_callback(self, event, x, y, flag=0, param=None):
        """
            mouse_callback function for use with the cv2.setMouseCallback()
            Left-clicking in the windows will add a point to self.mapmarkers[]
            Richt-clicking will remove a point from self.mapmarkers[]
            Scrolling will zoom in or outat the location the mouse is pointing
        """
        if event == cv2.EVENT_MOUSEWHEEL:
            if flag > 0:  # Scroll up
                self.mm.center = self.mm.geocode((x, y))
                self.zoomIn()
            elif flag < 0:    # Scroll down
                self.mm.center = self.mm.geocode((x, y))
                self.zoomOut()
        elif event == cv2.EVENT_LBUTTONUP:
            self.mapmarkers.append(self.mm.geocode((x, y)))
            self.drawMap()
        elif event == cv2.EVENT_RBUTTONUP:
            if len(self.mapmarkers) > 0:
                del self.mapmarkers[-1]
                self.drawMap()
            else:
                print('Nothing to delete')


# Create the map object and call it "kaart"(dutch for map)
kaart = MapObject()
# Create a window called window and have it adjust in size automatically
cv2.namedWindow('window', cv2.WINDOW_AUTOSIZE)
# Create the mousecallback in the window called "window"
cv2.setMouseCallback('window', kaart.mouse_callback)


while 1:
    # Show the image in "window"
    cv2.imshow('window', kaart.img)
    # OpenCV doesn't show anything untill the waitKey function is called
    key = cv2.waitKey(20)
    # when Esc is pressed: close all opencv windows and break
    if (key == 27):
        cv2.destroyAllWindows()
        break
    elif key == 43:  # "+" key
        kaart.zoomIn()
    elif key == 45:   # "-" key
        kaart.zoomOut()
