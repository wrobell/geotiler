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
        center = 11.788137, 46.481832
        zoom = 17
        size = 512, 512
        map = Map(center=center, zoom=zoom, size=size)
        self.assertEquals((512, 512), map.size)
        self.assertEquals(17, map.zoom)

        expected = 11.785390377044687, 46.4799402452901, 11.790883541107167, 46.48372275323265
        self.assertEquals(expected, map.extent)
        self.assertAlmostEquals(11.788137, map.center[0], 6)
        self.assertAlmostEquals(46.481832, map.center[1], 6)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


    def test_map_create_extent_size(self):
        """
        Test map instantiation with extent and size
        """
        provider = osm.Provider()
        extent = 11.785390377044687, 46.4799402452901, 11.790883541107167, 46.48372275323265
        size = 512, 512
        map = Map(extent=extent, size=size)

        self.assertEquals((512, 512), map.size)
        self.assertEquals(17, map.zoom)
        self.assertEquals(extent, map.extent)
        self.assertAlmostEquals(11.788137, map.center[0], 6)
        self.assertAlmostEquals(46.481832, map.center[1], 6)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


    def test_map_create_extent_zoom(self):
        """
        Test map instantiation with extent and zoom
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        self.assertEquals((472, 270), map.size)
        self.assertEquals(17, map.zoom)
        self.assertEquals(extent, map.extent)
        self.assertAlmostEquals(11.788137, map.center[0], 6)
        self.assertAlmostEquals(46.481832, map.center[1], 6)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


    def test_map_size_change_954_541(self):
        """
        Test changing map size (954x541)
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        map.size = 945, 541

        self.assertEquals((945, 541), map.size)
        self.assertEquals(17, map.zoom) # zoom has not changed
        expected = 11.783073, 46.4798368, 11.7932010, 46.4838261
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


    def test_map_size_change_1908x1082(self):
        """
        Test changing map size (1908x1082)
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        map.size = 1908, 1082

        self.assertEquals((1908, 1082), map.size)
        self.assertEquals(17, map.zoom) # zoom has not changed
        expected = 11.777902, 46.4778346, 11.7983723, 46.4858281
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


    def test_map_center_change(self):
        """
        Test changing map center
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size

        delta = 4 * 1e-5
        map.center = 11.788136959075942 + delta, 46.481831532133 + delta

        self.assertEquals((472, 270), map.size)
        self.assertEquals(17, map.zoom)

        expected = 11.7856478, 46.480871, 11.790712, 46.482866
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6, map.extent)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-242.0, map.offset.x)
        self.assertEquals(-189.0, map.offset.y)


    def test_map_zoom_change(self):
        """
        Test changing map zoom
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size
        assert map.zoom == 17, map.zoom

        map.zoom = 16

        self.assertEquals((472, 270), map.size)
        self.assertEquals(16, map.zoom)

        expected = 11.780519, 46.481270, 11.790648, 46.485259
        for v1, v2 in zip(expected, map.extent):
            self.assertAlmostEquals(v1, v2, 6, map.extent)

        self.assertEquals(34913, map.origin.column)
        self.assertEquals(23188, map.origin.row)
        self.assertEquals(16, map.origin.zoom)
        self.assertEquals(-128.0, map.offset.x)
        self.assertEquals(0.0, map.offset.y)


    def test_map_extent_change(self):
        """
        Test changing map extent
        """
        provider = osm.Provider()
        extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
        zoom = 17
        map = Map(extent=extent, zoom=zoom)

        assert map.size == (472, 270), map.size
        assert map.zoom == 17, map.zoom

        map.extent = 11.785590, 46.480830, 11.790680, 46.482840

        self.assertEquals((474, 272), map.size)
        self.assertEquals(17, map.zoom)

        self.assertEquals(69827, map.origin.column)
        self.assertEquals(46376, map.origin.row)
        self.assertEquals(17, map.origin.zoom)
        self.assertEquals(-238.0, map.offset.x)
        self.assertEquals(-194.0, map.offset.y)


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
        self.assertEquals(395.000, m.origin.row)
        self.assertEquals(163.000, m.origin.column)
        self.assertEquals(10, m.origin.zoom)
        self.assertEquals(-236.000, m.offset.x)
        self.assertEquals(-102.000, m.offset.y)


    def test_6(self):
        extent = -121.208153, 36.893326, -123.533554, 38.864246
        zoom = 9
        provider = ms.RoadProvider()
        m = Map(extent=extent, zoom=zoom, provider=provider)

        self.assertEquals((846.000, 909.000), m.size)
        self.assertEquals(197.000, m.origin.row)
        self.assertEquals(81.000, m.origin.column)
        self.assertEquals(9, m.origin.zoom)
        self.assertEquals(-246.000, m.offset.x)
        self.assertEquals(-179.000, m.offset.y)


# vim: sw=4:et:ai
