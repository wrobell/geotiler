#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@riseup.net>
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

from geotiler.geo import Transformation, MercatorProjection, zoom_to

import unittest

class TransformationTestCase(unittest.TestCase):
    def test_1(self):
        t = Transformation(1, 0, 0, 0, 1, 0)
        p = 1, 1

        pt = t.transform(p)
        self.assertEqual(1.0, pt[0])
        self.assertEqual(1.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEqual(1.0, ptt[0])
        self.assertEqual(1.0, ptt[1])


    def test_2(self):
        t = Transformation(0, 1, 0, 1, 0, 0)
        p = 0, 1

        pt = t.transform(p)
        self.assertEqual(1.0, pt[0])
        self.assertEqual(0.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEqual(0.0, ptt[0])
        self.assertEqual(1.0, ptt[1])


    def test_3(self):
        t = Transformation(1, 0, 1, 0, 1, 1)
        p = 0, 0

        pt = t.transform(p)
        self.assertEqual(1.0, pt[0])
        self.assertEqual(1.0, pt[1])

        ptt = t.untransform(pt)
        self.assertEqual(0.0, ptt[0])
        self.assertEqual(0.0, ptt[1])



class MercatorProjectionTestCase(unittest.TestCase):
    def test_1(self):
        m = MercatorProjection(10)
        coord = m.rev_geocode((0, 0))
        self.assertAlmostEqual(0.0, coord[0])
        self.assertAlmostEqual(0.0, coord[1])

        pt = m.geocode((0, 0), 10)
        self.assertAlmostEqual(0.0, pt[0])
        self.assertAlmostEqual(0.0, pt[1])


    def test_2(self):
        m = MercatorProjection(10)
        coord = m.rev_geocode((-122, 37))
        self.assertAlmostEqual(-2.129, coord[0], 3)
        self.assertAlmostEqual(0.696, coord[1], 3)

        pt = m.geocode((-2.129, 0.696), 10.000)
        self.assertAlmostEqual(-121.983, pt[0], 3)
        self.assertAlmostEqual(37.001, pt[1], 3)



class ZoomTestCase(unittest.TestCase):
    """
    Test tile coordinates zoom functions.
    """
    def test_zoom(self):
        """
        Test zooming tile coordinates
        """
        coord = zoom_to((1, 0), 2, 3)
        self.assertEqual((2, 0), coord)

        coord = zoom_to((1, 0), 2, 1)
        self.assertEqual((0.5, 0), coord)


# vim: sw=4:et:ai
