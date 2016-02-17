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
>>> p = OriginalProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/1/256/16/10507/25322.png',)

>>> p = FineLineProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/2/256/16/10507/25322.png',)

>>> p = TouristProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/7/256/16/10507/25322.png',)

>>> p = FreshProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/997/256/16/10507/25322.png',)

>>> p = PaleDawnProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/998/256/16/10507/25322.png',)

>>> p = MidnightCommanderProvider('example')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/999/256/16/10507/25322.png',)

>>> p = BaseProvider('example', 510)
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.cloudmade.com/example/510/256/16/10507/25322.png',)
"""

from math import pi

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

class BaseProvider(IMapProvider):
    def __init__(self, apikey, style=None):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

        self.key = apikey

        if style:
            self.style = style


    def get_tile_urls(self, tile_coord, zoom):
        column, row = tile_coord
        return ('http://tile.cloudmade.com/%s/%d/256/%d/%d/%d.png' % (self.key, self.style, zoom, column, row),)


class OriginalProvider(BaseProvider):
    style = 1

class FineLineProvider(BaseProvider):
    style = 2

class TouristProvider(BaseProvider):
    style = 7

class FreshProvider(BaseProvider):
    style = 997

class PaleDawnProvider(BaseProvider):
    style = 998

class MidnightCommanderProvider(BaseProvider):
    style = 999


# vim:et sts=4 sw=4:
