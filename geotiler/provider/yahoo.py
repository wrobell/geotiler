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
>>> p = RoadProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=...&t=m&x=10507&y=7445&z=2',)
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=...&t=m&x=10482&y=7434&z=2',)

>>> p = AerialProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10507&y=7445&z=2',)
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10482&y=7434&z=2',)

>>> p = HybridProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10507&y=7445&z=2', 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=...&t=h&x=10507&y=7445&z=2')
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10482&y=7434&z=2', 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=...&t=h&x=10482&y=7434&z=2')
"""

import math

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

ROAD_VERSION = '3.52'
AERIAL_VERSION = '1.7'
HYBRID_VERSION = '2.2'

class AbstractProvider(IMapProvider):
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        pi = math.pi
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def getZoomString(self, coordinate, zoom):
        return 'x=%d&y=%d&z=%d' % toYahoo(int(coordinate[0]), int(coordinate[1]), int(zoom))



class RoadProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=%s&t=m&%s' % (ROAD_VERSION, self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom)),)


class AerialProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=%s&t=a&%s' % (AERIAL_VERSION, self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom)),)


class HybridProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        under = AerialProvider().get_tile_urls(tile_coord, zoom)[0]
        over = 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=%s&t=h&%s' % (HYBRID_VERSION, self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom))
        return (under, over)



def fromYahoo(x, y, z):
    """ Return column, row, zoom for Yahoo x, y, z.
    """
    zoom = 18 - z
    row = int(math.pow(2, zoom - 1) - y - 1)
    col = x
    return col, row, zoom

def toYahoo(col, row, zoom):
    """ Return x, y, z for Yahoo tile column, row, zoom.
    """
    x = col
    y = int(math.pow(2, zoom - 1) - row - 1)
    z = 18 - zoom
    return x, y, z

def fromYahooRoad(x, y, z):
    """ Return column, row, zoom for Yahoo Road tile x, y, z.
    """
    return fromYahoo(x, y, z)

def toYahooRoad(col, row, zoom):
    """ Return x, y, z for Yahoo Road tile column, row, zoom.
    """
    return toYahoo(col, row, zoom)

def fromYahooAerial(x, y, z):
    """ Return column, row, zoom for Yahoo Aerial tile x, y, z.
    """
    return fromYahoo(x, y, z)

def toYahooAerial(col, row, zoom):
    """ Return x, y, z for Yahoo Aerial tile column, row, zoom.
    """
    return toYahoo(col, row, zoom)

# vim:et sts=4 sw=4:
