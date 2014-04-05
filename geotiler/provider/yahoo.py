﻿#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
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
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=...&t=m&x=10507&y=7445&z=2',)
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=...&t=m&x=10482&y=7434&z=2',)

>>> p = AerialProvider()
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10507&y=7445&z=2',)
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10482&y=7434&z=2',)

>>> p = HybridProvider()
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10507&y=7445&z=2', 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=...&t=h&x=10507&y=7445&z=2')
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=...&t=a&x=10482&y=7434&z=2', 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=...&t=h&x=10482&y=7434&z=2')
"""

from math import pi

from ..core import Coordinate
from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

from .. import tiles

ROAD_VERSION = '3.52'
AERIAL_VERSION = '1.7'
HYBRID_VERSION = '2.2'

class AbstractProvider(IMapProvider):
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def getZoomString(self, coordinate):
        return 'x=%d&y=%d&z=%d' % tiles.toYahoo(int(coordinate.column), int(coordinate.row), int(coordinate.zoom))

    @property
    def tile_width(self):
        return 256

    @property
    def tile_height(self):
        return 256

class RoadProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        return ('http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=%s&t=m&%s' % (ROAD_VERSION, self.getZoomString(self.sourceCoordinate(coordinate))),)

class AerialProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        return ('http://us.maps3.yimg.com/aerial.maps.yimg.com/tile?v=%s&t=a&%s' % (AERIAL_VERSION, self.getZoomString(self.sourceCoordinate(coordinate))),)

class HybridProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        under = AerialProvider().getTileUrls(coordinate)[0]
        over = 'http://us.maps3.yimg.com/aerial.maps.yimg.com/png?v=%s&t=h&%s' % (HYBRID_VERSION, self.getZoomString(self.sourceCoordinate(coordinate)))
        return (under, over)


# vim:et sts=4 sw=4: