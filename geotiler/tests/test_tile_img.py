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

"""
Tests for rendering map image using map tile data.
"""

import io
import PIL.Image

import geotiler.tile.img as tile_img

import unittest
from unittest import mock


class MapImageRenderTestCase(unittest.TestCase):
    """
    Map image rendering tests.
    """
    def test_render_error_tile(self):
        """
        Test rendering of error tile
        """
        tile_img._error_image.cache_clear()
        img = tile_img._error_image(10, 10)
        self.assertEqual((10, 10), img.size)


    def test_tile_image_png(self):
        """
        Test converting PNG data into PIL image object
        """
        tile = PIL.Image.new('RGBA', (10, 11))
        f = io.BytesIO()
        tile.save(f, format='png')

        img = tile_img._tile_image(f.getbuffer())
        self.assertEquals((10, 11), img.size)


    def test_tile_image_jpg(self):
        """
        Test converting JPEG data into PIL image object
        """
        tile = PIL.Image.new('RGBA', (12, 10))
        f = io.BytesIO()
        tile.save(f, format='jpeg')

        img = tile_img._tile_image(f.getbuffer())
        self.assertEquals((12, 10), img.size)


def test_render_image():
    """
    Test rendering map image
    """
    tile = PIL.Image.new('RGBA', (10, 10))
    map = mock.MagicMock()
    map.size = [30, 20]
    map.provider.tile_width = 10
    map.provider.tile_height = 10

    with mock.patch('geotiler.tile.img._tile_image') as tf, \
            mock.patch.object(PIL.Image, 'new') as img_new:

        tf.return_value = tile
        data = (tile, tile, tile, tile)
        offsets = ((0, 0), (10, 0), (20, 0), (0, 10))

        image = tile_img.render_image(map, data, offsets)

        img_new.assert_called_once_with('RGBA', (30, 20))
        assert 4 == tf.call_count
        tf.assert_called_with(tile)

def test_render_image_error():
    """
    Test rendering map image with error tile
    """
    tile = PIL.Image.new('RGBA', (10, 10))
    map = mock.MagicMock()
    map.size = 30, 20
    map.provider.tile_width = 10
    map.provider.tile_height = 10

    with mock.patch('geotiler.tile.img._tile_image') as tf:
        tf.return_value = tile
        data = (tile, tile, None, tile, None, tile)
        offsets = ((0, 0), (10, 0), (20, 0), (0, 10), (10, 10), (20, 10))
        image = tile_img.render_image(map, data, offsets)
        assert 4 == tf.call_count
        tf.assert_called_with(tile)

# vim: sw=4:et:ai
