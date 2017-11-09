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
Caching downloader unit tests.
"""

import asyncio
from functools import partial

from geotiler.map import Tile
from geotiler.cache import caching_downloader, redis_downloader

from unittest import mock

def test_redis_downloader_and_cache():
    """
    Test Redis downloader and cache functions.
    """
    async def images(tiles, num_workers):
        tile = partial(Tile, error=None, offset=None)
        for t in tiles:
            yield tile(url=t.url, img='img')

    async def as_list(tiles):
        return [t async for t in tiles]

    client = mock.MagicMock()
    client.get.side_effect = ['c-img1', None, 'c-img3']
    downloader = redis_downloader(client, downloader=images, timeout=10)
    assert caching_downloader == downloader.func

    urls = ['url1', 'url2', 'url3']
    tiles = [Tile(url, None, None, None) for url in urls]

    loop = asyncio.get_event_loop()
    tiles = downloader(tiles, 2)
    result = loop.run_until_complete(as_list(tiles))

    args = [v[0][0] for v in client.get.call_args_list]
    assert ['url1', 'url2', 'url3'] == args

    args = sorted(v[0] for v in client.setex.call_args_list)
    assert 3 == len(args)
    assert ('url1', 'c-img1', 10) == args[0]
    assert ('url2', 'img', 10) == args[1]
    assert ('url3', 'c-img3', 10) == args[2]


# vim: sw=4:et:ai
