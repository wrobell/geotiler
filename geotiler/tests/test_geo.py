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

from geotiler.core import Coordinate
from geotiler.geo import Transformation, MercatorProjection

import unittest

class TransformationTestCase(unittest.TestCase):
    def test_1(self):
        t = Transformation(1, 0, 0, 0, 1, 0)
        p = 1, 1

        pt = t.transform(p)
        self.assertEquals(1.0, pt[0])
        self.assertEquals(1.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEquals(1.0, ptt[0])
        self.assertEquals(1.0, ptt[1])


    def test_2(self):
        t = Transformation(0, 1, 0, 1, 0, 0)
        p = 0, 1

        pt = t.transform(p)
        self.assertEquals(1.0, pt[0])
        self.assertEquals(0.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEquals(0.0, ptt[0])
        self.assertEquals(1.0, ptt[1])


    def test_3(self):
        t = Transformation(1, 0, 1, 0, 1, 1)
        p = 0, 0

        pt = t.transform(p)
        self.assertEquals(1.0, pt[0])
        self.assertEquals(1.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEquals(0.0, ptt[0])
        self.assertEquals(0.0, ptt[1])



class MercatorProjectionTestCase(unittest.TestCase):
    def test_1(self):
        m = MercatorProjection(10)
        coord = m.locationCoordinate((0, 0))
        self.assertAlmostEquals(0.0, coord.column)
        self.assertAlmostEquals(0.0, coord.row)
        self.assertAlmostEquals(10.0, coord.zoom)

        pt = m.coordinateLocation(Coordinate(0, 0, 10))
        self.assertAlmostEquals(0.0, pt[0])
        self.assertAlmostEquals(0.0, pt[1])


    def test_2(self):
        m = MercatorProjection(10)
        coord = m.locationCoordinate((-122, 37))
        self.assertAlmostEquals(0.696, coord.row, 3)
        self.assertAlmostEquals(-2.129, coord.column, 3)
        self.assertAlmostEquals(10.0, coord.zoom)

        pt = m.coordinateLocation(Coordinate(0.696, -2.129, 10.000))
        self.assertAlmostEquals(-121.983, pt[0], 3)
        self.assertAlmostEquals(37.001, pt[1], 3)


# vim: sw=4:et:ai
