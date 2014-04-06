#
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
>>> p = BaseProvider('toner')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/toner/16/10507/25322.png',)

>>> p = TonerProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/toner/16/10507/25322.png',)

>>> p = TerrainProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/terrain/16/10507/25322.png',)

>>> p = WatercolorProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/watercolor/16/10507/25322.png',)
"""

from math import pi

from ..core import Coordinate
from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider


class BaseProvider(IMapProvider):
    def __init__(self, style):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

        self.style = style


    def get_tile_urls(self, tile_coord, zoom):
        column, row = tile_coord
        return ('http://tile.stamen.com/%s/%d/%d/%d.png' % (self.style, zoom, column, row),)



class TonerProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner')



class TerrainProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'terrain')



class WatercolorProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'watercolor')


# vim:et sts=4 sw=4:
