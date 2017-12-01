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
import aiohttp
from contextlib import contextmanager

import geotiler.tile.io
from geotiler.map import Tile
from geotiler.tile.io import fetch_tile, fetch_tiles

import asynctest
from unittest import mock

# http://pfertyk.me/2017/06/testing-asynchronous-context-managers-in-python/
class ContextManagerMock(mock.MagicMock):
    async def __aenter__(self):
        return self.aenter

    async def __aexit__(self, *args):
        pass

@contextmanager
def mock_url_open(session, data, error_msg=None):
    """
    Mock opening of an URL.

    If error message set, then it is raised as `aiohttp.ClientError`
    exception.

    :param session: Mock of `aiohttp` client session.
    :param data: Data to be assigned to HTTP response.
    :param error_msg: Error encountered when an exception is raised.
    """
    ctx_mock = session.get.return_value.aenter

    if error_msg:
        params = {'side_effect': aiohttp.ClientError(error_msg)}
    else:
        params = {'return_value': data}

    ctx_mock.read = asynctest.CoroutineMock(**params)
    yield session

@asynctest.patch('aiohttp.ClientSession', new_callable=ContextManagerMock)
async def test_fetch_tile(session):
    """
    Test fetching a map tile.
    """
    tile = Tile('http://a.b.c', None, None, None)

    with mock_url_open(session, 'image'):
        result = await fetch_tile(session, tile)

        assert result is not tile  # copy of tile is returned
        assert tile.url == result.url
        assert 'image' == result.img
        assert result.error is None

@asynctest.patch('aiohttp.ClientSession', new_callable=ContextManagerMock)
async def test_fetch_tile_error(session):
    """
    Test fetching a map tile with an error.
    """
    # assign something to `img` and `error` to see if they are overriden
    # properly in case of an error
    tile = Tile('http://a.b.c', 'a', 'b', 'c')
    with mock_url_open(session, 'image', error_msg='some error'):
        tile = await fetch_tile(session, tile)
        assert tile.img is None

        error = 'Unable to download http://a.b.c (error: some error)'
        assert error == str(tile.error)

@asynctest.patch('aiohttp.ClientSession', new_callable=ContextManagerMock)
async def test_fetch_tiles(session):
    """
    Test fetching map tiles.
    """
    tiles = [
        Tile('http://a.b.c/1', 'o', 'image', None),
        Tile('http://a.b.c/2', 'o', 'image', None),
        Tile('http://a.b.c/3', 'o', None, 'error'),
        Tile('http://a.b.c/4', 'o', 'image', None),
    ]
    tasks = [asyncio.Future() for t in tiles]
    for task, tile in zip(tasks, tiles):
        task.set_result(tile)

    ctx_ac = mock.patch.object(asyncio, 'as_completed')
    ctx_ft = mock.patch.object(geotiler.tile.io, 'fetch_tile')
    with ctx_ac as mock_as_completed, ctx_ft:
        mock_as_completed.return_value = tasks
        tiles = [t async for t in fetch_tiles(tiles, 2)]

        img = [tile.img for tile in tiles]
        assert ['image', 'image', None, 'image'] == img, tiles

        error = [tile.error for tile in tiles]
        assert [None, None, 'error', None] == error, tiles

# vim: sw=4:et:ai
