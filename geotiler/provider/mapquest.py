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
>>> p.get_tile_urls((13, 10), 7) #doctest: +ELLIPSIS
('http://otile....mqcdn.com/tiles/1.0.0/7/13/10.png',)
>>> p.get_tile_urls((10, 13), 7) #doctest: +ELLIPSIS
('http://otile....mqcdn.com/tiles/1.0.0/7/10/13.png',)

>>> p = AerialProvider()
>>> p.get_tile_urls((13, 10), 7) #doctest: +ELLIPSIS
('http://oatile....mqcdn.com/naip/7/13/10.png',)
>>> p.get_tile_urls((10, 13), 7) #doctest: +ELLIPSIS
('http://oatile....mqcdn.com/naip/7/10/13.png',)
"""

from math import pi
import random

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider


class AbstractProvider(IMapProvider):
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)



class RoadProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://otile%d.mqcdn.com/tiles/1.0.0/%d/%d/%d.png' % (random.randint(1, 4), zoom, tile_coord[0], tile_coord[1]),)


class AerialProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://oatile%d.mqcdn.com/naip/%d/%d/%d.png' % (random.randint(1, 4), zoom, tile_coord[0], tile_coord[1]),)


# vim:et sts=4 sw=4:
