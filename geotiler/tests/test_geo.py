#
# GeoTiler - library to create maps using tiles from a map provider
#
# NOTE: The code contains BSD licensed code from Modest Maps project.
#
# Copyright (C) 2013-2014 by Artur Wroblewski <wrobell@pld-linux.org>
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

from shapely.geometry import Point

from geotiler.Core import Coordinate
from geotiler.Geo import Transformation, MercatorProjection

import unittest

class TransformationTestCase(unittest.TestCase):
    def test_1(self):
        t = Transformation(1, 0, 0, 0, 1, 0)
        p = Point(1, 1)

        pt = t.transform(p)
        self.assertEquals(1.0, pt.x)
        self.assertEquals(1.0, pt.y)

        ptt = t.untransform(pt)
        self.assertEquals(1.0, ptt.x)
        self.assertEquals(1.0, ptt.y)


    def test_2(self):
        t = Transformation(0, 1, 0, 1, 0, 0)
        p = Point(0, 1)

        pt = t.transform(p)
        self.assertEquals(1.0, pt.x)
        self.assertEquals(0.0, pt.y)

        ptt = t.untransform(pt)
        self.assertEquals(0.0, ptt.x)
        self.assertEquals(1.0, ptt.y)


    def test_3(self):
        t = Transformation(1, 0, 1, 0, 1, 1)
        p = Point(0, 0)

        pt = t.transform(p)
        self.assertEquals(1.0, pt.x)
        self.assertEquals(1.0, pt.y)

        ptt = t.untransform(pt)
        self.assertEquals(0.0, ptt.x)
        self.assertEquals(0.0, ptt.y)



class MercatorProjectionTestCase(unittest.TestCase):
    def test_1(self):
        m = MercatorProjection(10)
        coord = m.locationCoordinate(Point(0, 0))
        self.assertAlmostEquals(0.0, coord.column)
        self.assertAlmostEquals(0.0, coord.row)
        self.assertAlmostEquals(10.0, coord.zoom)

        pt = m.coordinateLocation(Coordinate(0, 0, 10))
        self.assertAlmostEquals(0.0, pt.x)
        self.assertAlmostEquals(0.0, pt.y)


    def test_2(self):
        m = MercatorProjection(10)
        coord = m.locationCoordinate(Point(-122, 37))
        self.assertAlmostEquals(0.696, coord.row, 3)
        self.assertAlmostEquals(-2.129, coord.column, 3)
        self.assertAlmostEquals(10.0, coord.zoom)

        pt = m.coordinateLocation(Coordinate(0.696, -2.129, 10.000))
        self.assertAlmostEquals(-121.983, pt.x, 3)
        self.assertAlmostEquals(37.001, pt.y, 3)


# vim: sw=4:et:ai
