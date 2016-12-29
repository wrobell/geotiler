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
Map tile downloading unit tests.
"""

import asyncio
import urllib.request
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
        Mock `urllib.request.urlopen` call and run `fetch_tile` function.

        The `status` parameter is HTTP error code, but can be exception as
        well. If exception, then it is raised during request.

        :param status: HTTP error code (i.e. 200) or an exception.
        :param urls: Collection of urls.
        """
        response = mock.MagicMock()
        response.read.return_value = 'image'
        response.status = status

        with mock.patch.object(urllib.request, 'Request') as _, \
                mock.patch.object(urllib.request, 'urlopen') as f:

            if isinstance(status, Exception):
                f.side_effect = status
            else:
                f.return_value = response
            result = [fetch_tile(u) for u in urls]
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
        try:
            with self.run_fetch_tile(400, 'a', 'b') as result:
                pass
        except ValueError as ex:
            self.assertTrue(str(ex).startswith('Unable to download'))


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
