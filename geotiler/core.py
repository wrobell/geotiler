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
>>> c = Coordinate(0, 1, 2)
>>> c
(0.000, 1.000 @2.000)
>>> c.row
0
>>> c.column
1
>>> c.zoom
2
"""

import math

class Coordinate:
    MAX_ZOOM = 25

    def __init__(self, row, column, zoom):
        self.row = row
        self.column = column
        self.zoom = zoom

    def __repr__(self):
        return '(%(row).3f, %(column).3f @%(zoom).3f)' % self.__dict__

    def __eq__(self, other):
        return self.zoom == other.zoom and self.row == other.row and self.column == other.column

    def __cmp__(self, other):
        return cmp((self.zoom, self.row, self.column), (other.zoom, other.row, other.column))

    def __hash__(self):
        return hash(('Coordinate', self.row, self.column, self.zoom))

    def container(self):
        return self.__class__(math.floor(self.row), math.floor(self.column), self.zoom)


# vim:et sts=4 sw=4:
