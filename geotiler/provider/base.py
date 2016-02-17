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

import re
from math import pi, pow

from ..geo import MercatorProjection, deriveTransformation


class IMapProvider(object):
    def __init__(self):
        raise NotImplementedError("Abstract method not implemented by subclass.")


    def get_tile_urls(self, tile_coord, zoom):
        raise NotImplementedError("Abstract method not implemented by subclass.")


    @property
    def tile_width(self):
        return 256


    @property
    def tile_height(self):
        return 256


    def sourceCoordinate(self, tile_coord, zoom):
        wrappedColumn = tile_coord[0] % pow(2, zoom)

        while wrappedColumn < 0:
            wrappedColumn += pow(2, zoom)

        return wrappedColumn, tile_coord[1]



class TemplatedMercatorProvider(IMapProvider):
    """ Convert URI templates into tile URLs, using a tileUrlTemplate identical to:
        http://code.google.com/apis/maps/documentation/overlays.html#Custom_Map_Types
    """
    def __init__(self, template):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

        self.templates = []

        while template:
            match = re.match(r'^((http|https|file)://\S+?)(,(http|https|file)://\S+)?$', template)
            first = match.group(1)

            if match:
                self.templates.append(first)
                template = template[len(first):].lstrip(',')
            else:
                break


    @property
    def tile_width(self):
        return 256


    @property
    def tile_height(self):
        return 256


    def get_tile_urls(self, tile_coord, zoom):
        x, y = tile_coord
        return [t.format(X=x, Y=y, Z=zoom) for t in self.templates]


# vim: sw=4:et:ai
