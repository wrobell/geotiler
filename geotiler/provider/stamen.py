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
>>> p = BaseProvider('toner', 'png')
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/toner/16/10507/25322.png',)

>>> p = TonerProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/toner/16/10507/25322.png',)

>>> p = TerrainProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/terrain/16/10507/25322.jpg',)

>>> p = WatercolorProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://tile.stamen.com/watercolor/16/10507/25322.jpg',)
"""

from math import pi

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

URL_FMT = 'http://tile.stamen.com/{style}/{{zoom}}/{{col}}/{{row}}.{ext}'

class BaseProvider(IMapProvider):
    def __init__(self, style, ext):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

        self.url_fmt = URL_FMT.format(style=style, ext=ext)


    def get_tile_urls(self, tile_coord, zoom):
        column, row = tile_coord
        return (self.url_fmt.format(zoom=zoom, col=column, row=row),)



class TonerProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner', 'png')


class TonerLiteProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'toner-lite', 'png')


class TerrainProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'terrain', 'jpg')



class WatercolorProvider(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'watercolor', 'jpg')


# vim:et sts=4 sw=4:
