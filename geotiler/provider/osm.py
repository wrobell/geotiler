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
>>> p = Provider()
>>> p.get_tile_urls((13, 10), 7)
('http://tile.openstreetmap.org/7/13/10.png',)
>>> p.get_tile_urls((10, 13), 7)
('http://tile.openstreetmap.org/7/10/13.png',)
"""

from math import pi

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider


class Base(IMapProvider):
    FMT_URL = None

    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)


    def get_tile_urls(self, tile_coord, zoom):
        url = self.FMT_URL.format(x=tile_coord[0], y=tile_coord[1], z=zoom)
        return (url,)



class Provider(Base):
    FMT_URL = 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'



class CycleProvider(Base):
    FMT_URL = 'http://tile.opencyclemap.org/cycle/{z}/{x}/{y}.png'


# vim:et sts=4 sw=4:
