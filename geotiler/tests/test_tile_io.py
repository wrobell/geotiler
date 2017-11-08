#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2017 by Artur Wroblewski <wrobell@riseup.net>
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

from geotiler.map import Tile
from geotiler.tile.io import fetch_tile, fetch_tiles

from unittest import mock

@contextmanager
def mock_urlopen(data, status=200):
    """
    Mock `urlopen` function call.

    If status different than 200, then cause mock to raise `HTTPError`
    exception.

    :param data: Data to be assigned to HTTP response.
    :param status: HTTP status.
    """
    response = mock.MagicMock()
    response.read.return_value = data
    response.status = status

    with mock.patch.object(urllib.request, 'urlopen') as f:
        if status == 200:
            f.return_value = response
        else:
            error = urllib.error.HTTPError(
                'http://test', status, 'error message', {}, None
            )
            f.side_effect = error
        yield f

def test_fetch_tile():
    """
    Test fetching a map tile.
    """
    tile = Tile('http://a.b.c', None, None, None)
    with mock_urlopen('image') as f:
        tile = fetch_tile(tile)
        assert 'image' == tile.img
        assert tile.error is None

def test_fetch_tile_error():
    """
    Test fetching a map tile with an error.
    """
    # assign something to `img` and `error` to see if they are overriden
    # properly in case of an error
    tile = Tile('http://a.b.c', 'a', 'b', 'c')
    with mock_urlopen('image', status=400) as f:
        tile = fetch_tile(tile)
        assert tile.img is None

        error = 'Unable to download http://a.b.c (HTTP status 400)'
        assert error == str(tile.error)

def test_fetch_tiles():
    """
    Test fetching map tiles.
    """
    tiles = [
        Tile('http://a.b.c/1', 'a', 'b', 'c'),
        Tile('http://a.b.c/2', 'a', 'b', 'c'),
        Tile('http://a.b.c/3', 'a', 'b', 'c'),
        Tile('http://a.b.c/4', 'a', 'b', 'c'),
    ]
    with mock_urlopen('image') as f:
        loop = asyncio.get_event_loop()
        task = fetch_tiles(tiles, 2)
        tiles = loop.run_until_complete(task)

        img = [tile.img for tile in tiles]
        assert ['image'] * 4 == img, tiles

        error = [tile.error for tile in tiles]
        assert [None] * 4 == error, tiles

# vim: sw=4:et:ai
