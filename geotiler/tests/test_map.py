#
# geoTiler - library to create maps using tiles from a map provider
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

from geotiler.map import Map
from geotiler.provider import ms, osm
from geotiler.core import Coordinate

import unittest


class MapTestCase(unittest.TestCase):
    """
    Map unit tests.
    """
    def test_map_create_error_center_extent(self):
        """
        Test map instantiation error with center and extent
        """
        extent = (0, 0, 0, 0)
        center = (0, 0)
        map = self.assertRaises(ValueError, Map, extent=extent, center=center)


    def test_map_create_error_extent_size_zoom(self):
        """
        Test map instantiation error with extent, size and zoom
        """
        extent = (0, 0, 0, 0)
        size = (0, 0)
        zoom = 1
        map = self.assertRaises(
            ValueError, Map, extent=extent, size=size, zoom=zoom
        )


    def test_map_create_center_zoom_size(self):
        """
        Test map instantiation with center, zoom and size
        """
        provider = osm.Provider()
        center = 11.788135, 46.48183
        zoom = 18
        size = 512, 512
        map = Map(center=center, zoom=zoom, size=size)
        self.assertEquals((512, 512), map.size)
        self.assertEquals(18, map.zoom)
        expected = (
            11.7867636, 46.4808858,
            11.7895102, 46.4827771,
        )
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6)
        #self.assertEquals((11.788135, 46.48183), map.center)


    def test_map_create_extent_size(self):
        """
        Test map instantiation with extent and size
        """
        provider = osm.Provider()
        extent = 11.78560, 46.48083, 11.79067, 46.48283
        size = 512, 512
        map = Map(extent=extent, size=size)

        self.assertEquals((512, 512), map.size)
        self.assertEquals(17, map.zoom)
        self.assertEquals((11.78560, 46.48083, 11.79067, 46.48283), map.extent)
        #self.assertEquals((11.788135, 46.48183), map.center)


    def test_map_create_extent_zoom(self):
        """
        Test map instantiation with extent and zoom
        """
        provider = osm.Provider()
        extent = 11.78560, 46.48083, 11.79067, 46.48283
        zoom = 18
        map = Map(extent=extent, zoom=zoom)

        self.assertEquals((945, 541), map.size)
        self.assertEquals(18, map.zoom)
        self.assertEquals((11.78560, 46.48083, 11.79067, 46.48283), map.extent)
        #self.assertEquals((11.788135, 46.48183), map.center)


    def test_map_size_change_512(self):
        """
        Test changing map size (512x512)
        """
        provider = osm.Provider()
        extent = 11.78560, 46.48083, 11.79067, 46.48283
        zoom = 18
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (945, 541), map.size

        map.size = 512, 512

        self.assertEquals((512, 512), map.size)
        self.assertEquals(18, map.zoom) # zoom has not changed
        expected = (
            11.7867636, 46.4808858,
            11.7895102, 46.4827771,
        )
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6)

        self.assertEquals(139655, map.coordinate.column)
        self.assertEquals(92753, map.coordinate.row)
        self.assertEquals(18, map.coordinate.zoom)
        self.assertEquals(-220.0, map.offset.x)
        self.assertEquals(-132.0, map.offset.y)


    def test_map_size_change_1024(self):
        """
        Test changing map size (1024x1024)
        """
        provider = osm.Provider()
        extent = 11.78560, 46.48083, 11.79067, 46.48283
        zoom = 18
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (945, 541), map.size

        map.size = 1024, 1024

        self.assertEquals((1024, 1024), map.size)
        self.assertEquals(18, map.zoom) # zoom has not changed
        expected = (
            11.785390, 46.479940,
            11.790884, 46.483723,
        )
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6)

        # the same as in test_map_size_change_512
        self.assertEquals(139655, map.coordinate.column)
        self.assertEquals(92753, map.coordinate.row)
        self.assertEquals(18, map.coordinate.zoom)
        # what about offset?
        self.assertEquals(-220.0, map.offset.x)
        self.assertEquals(-132.0, map.offset.y)


    def test_map_center_change(self):
        """
        Test changing map center
        """
        provider = osm.Provider()
        extent = 11.78560, 46.48083, 11.79067, 46.48283
        zoom = 18
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (945, 541), map.size

        delta = 4 * 1e-6
        map.center = 11.788135 + delta, 46.48183 + delta

        self.assertEquals((945, 541), map.size)
        self.assertEquals(18, map.zoom)

        expected = tuple(v + delta for v in extent)
        for k, (v1, v2) in enumerate(zip(expected, map.extent)):
            self.assertAlmostEquals(v1, v2, 6, k)


    # TODO: test_map_zoom_change
    # TODO: test_map_extent_change


    def test_1(self):
        provider = ms.RoadProvider()
        m = Map(extent=(0, 0, 0, 0), zoom=13, provider=provider)
        m.coordinate = Coordinate(3165, 1313, 13)
        m.offset = Point(-144, -94)
        m.size = 600, 600

        p = m.locationPoint(Point(-122.262940, 37.804274))
        self.assertAlmostEquals(p.x, 370.724, 3)
        self.assertAlmostEquals(p.y, 342.549, 3)

        p = m.pointLocation(p)
        self.assertAlmostEquals(p.x, -122.263, 3)
        self.assertAlmostEquals(p.y, 37.804, 3)


    def test_5(self):
        extent = -123.533554, 36.893326, -121.208153, 38.864246
        zoom = 10
        provider = ms.RoadProvider()

        m = Map(extent=extent, zoom=zoom, provider=provider)

        self.assertEquals((1693.000, 1818.000), m.size)
        self.assertEquals(395.000, m.coordinate.row)
        self.assertEquals(163.000, m.coordinate.column)
        self.assertEquals(10, m.coordinate.zoom)
        self.assertEquals(-236.000, m.offset.x)
        self.assertEquals(-102.000, m.offset.y)


    def test_6(self):
        extent = -121.208153, 36.893326, -123.533554, 38.864246
        zoom = 9
        provider = ms.RoadProvider()
        m = Map(extent=extent, zoom=zoom, provider=provider)

        self.assertEquals((846.000, 909.000), m.size)
        self.assertEquals(197.000, m.coordinate.row)
        self.assertEquals(81.000, m.coordinate.column)
        self.assertEquals(9, m.coordinate.zoom)
        self.assertEquals(-246.000, m.offset.x)
        self.assertEquals(-179.000, m.offset.y)


# vim: sw=4:et:ai
