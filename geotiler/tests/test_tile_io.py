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
Map tile downloading unit tests.
"""

import aiohttp
import asyncio
from contextlib import contextmanager
from functools import wraps

from geotiler.tile.io import fetch_tile, fetch_tiles

import unittest
from unittest import mock


class MapTileDownloadingTestCase(unittest.TestCase):
    """
    Map tile downloading unit tests.
    """
    @contextmanager
    def run_fetch_tile(self, status, *urls):
        """
        Mock aiohttp request and response for `fetch_tile` coroutine and
        run the coroutine.

        The `status` parameter is HTTP error code, but can be exception as
        well. If exception, then it is raised during request.

        :param status: HTTP error code (i.e. 200) or an exception.
        :param urls: Collection of urls.
        """
        @asyncio.coroutine
        def mock_read_and_close(*args, **kwargs):
            return 'image'

        @asyncio.coroutine
        def mock_request(*args, **kwargs):
            if isinstance(status, Exception):
                raise status

            response = mock.MagicMock()
            response.status = status
            response.read_and_close = mock_read_and_close
            return response

        with mock.patch.object(aiohttp, 'request', mock_request) as request:
            coros = (fetch_tile(u) for u in urls)
            task = asyncio.gather(*coros, return_exceptions=True)
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(task)
            yield result


    @contextmanager
    def run_fetch_tiles(self, *tile_url):
        """
        Mock `asyncio.gather` call for `fetch_tiles` coroutine and run the
        coroutine.

        The `tile_url` is pair of URL and tile data (tile data can be
        replaced with an exception). Tile data is to be returned by the
        'asyncio.gather` mock.

        :param tile_url: Pair of URL and tile data.
        """
        @asyncio.coroutine
        def mock_gather(*args, **kwargs):
            return [code for url, code in tile_url]

        with mock.patch.object(asyncio, 'gather', mock_gather) as f:
            urls = [url for url, code in tile_url]
            task = fetch_tiles(urls)
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(task)
            yield list(result)


    def test_fetch_tile(self):
        """
        Test fetching of tiles
        """
        with self.run_fetch_tile(200, 'a', 'b') as result:
            self.assertEqual(['image'] * 2, result)


    def test_fetch_tile_error(self):
        """
        Test error when fetching tile

        If HTTP error code is different than 200 for a tile, then we expect
        ValueError to be raised.
        """
        with self.run_fetch_tile(400, 'a', 'b') as result:
            self.assertEqual(2, len(result))
            expected = all(isinstance(v, ValueError) for v in result)
            self.assertTrue(expected, result)


    def test_fetch_tile_original_error(self):
        """
        Test original error when fetching tile

        We expect original error to be preserved by `fetch_tile` coroutine.
        For example if there was OSError, then OSError is returned.
        """
        with self.run_fetch_tile(OSError(), 'a', 'b') as result:
            self.assertEqual(2, len(result))
            expected = all(isinstance(v, OSError) for v in result)
            self.assertTrue(expected, result)


    def test_fetching_tiles_error(self):
        """
        Test fetching tiles error

        Check if None is returned for each non-downloaded tile.
        """
        params = (
            ('a', 'image1'), ('b', OSError()), ('c', ValueError()),
            ('d', 'image2')
        )
        with self.run_fetch_tiles(*params) as result:
            self.assertEqual(4, len(result))
            expected = ['image1', None, None, 'image2']
            self.assertEqual(expected, result)


# vim: sw=4:et:ai
