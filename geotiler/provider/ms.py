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
('http://r....ortho.tiles.virtualearth.net/tiles/r0230102122203031.png?g=90&shading=hill',)
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://r....ortho.tiles.virtualearth.net/tiles/r0230102033330212.png?g=90&shading=hill',)

>>> p = AerialProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://a....ortho.tiles.virtualearth.net/tiles/a0230102122203031.jpeg?g=90',)
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://a....ortho.tiles.virtualearth.net/tiles/a0230102033330212.jpeg?g=90',)

>>> p = HybridProvider()
>>> p.get_tile_urls((10507, 25322), 16) #doctest: +ELLIPSIS
('http://h....ortho.tiles.virtualearth.net/tiles/h0230102122203031.jpeg?g=90',)
>>> p.get_tile_urls((10482, 25333), 16) #doctest: +ELLIPSIS
('http://h....ortho.tiles.virtualearth.net/tiles/h0230102033330212.jpeg?g=90',)
"""

from math import pi

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

import random

class AbstractProvider(IMapProvider):
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def getZoomString(self, coordinate, zoom):
        return toMicrosoft(int(coordinate[0]), int(coordinate[1]), int(zoom))



class RoadProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://r%d.ortho.tiles.virtualearth.net/tiles/r%s.png?g=90&shading=hill' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom)),)


class AerialProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://a%d.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=90' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom)),)


class HybridProvider(AbstractProvider):
    def get_tile_urls(self, tile_coord, zoom):
        return ('http://h%d.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=90' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(tile_coord, zoom), zoom)),)



microsoftFromCorners = {'0': '00', '1': '01', '2': '10', '3': '11'}
microsoftToCorners = {'00': '0', '01': '1', '10': '2', '11': '3'}

def fromMicrosoft(s):
    """ Return column, row, zoom for Microsoft tile string.
    """
    row, col = [int(''.join(v), 2) for v in zip(*[microsoftFromCorners[c] for c in s])]
    zoom = len(s)
    return col, row, zoom

def toMicrosoft(col, row, zoom):
    """ Return string for Microsoft tile column, row, zoom.
    """
    x = col
    y = row
    y, x = bin(y)[2:].rjust(zoom, '0'), bin(x)[2:].rjust(zoom, '0')
    v = ''.join([microsoftToCorners[y[c]+x[c]] for c in range(zoom)])
    return v

def fromMicrosoftRoad(s):
    """ Return column, row, zoom for Microsoft Road tile string.
    """
    return fromMicrosoft(s)

def toMicrosoftRoad(col, row, zoom):
    """ Return x, y, z for Microsoft Road tile column, row, zoom.
    """
    return toMicrosoft(col, row, zoom)

def fromMicrosoftAerial(s):
    """ Return column, row, zoom for Microsoft Aerial tile string.
    """
    return fromMicrosoft(s)

def toMicrosoftAerial(col, row, zoom):
    """ Return x, y, z for Microsoft Aerial tile column, row, zoom.
    """
    return toMicrosoft(col, row, zoom)


# vim:et sts=4 sw=4:
