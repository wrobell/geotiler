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
Caching strategies for GeoTiler.
"""

import logging
from functools import partial
from cytoolz.itertoolz import groupby, partition_all

from .util import log_tiles
from geotiler.tile.io import fetch_tiles

logger = logging.getLogger(__name__)

def log_tile_cache_hit(tile):
    if tile.img:
        logger.debug('cache hit for: {}'.format(tile.url))
    return tile

def fetch_from_cache(get, tiles):
    tiles = (t._replace(img=get(t.url)) for t in tiles)
    if __debug__:
        tiles = log_tiles(log_tile_cache_hit, tiles)
    return tiles

async def caching_downloader(get, set, downloader, tiles, num_workers, **kw):
    """
    Download tiles from cache and missing tiles with the downloader.

    Asynchronous generator of map tiles is returned.

    The code flow is

    - caching downloader gets tile data from cache using URLs
    - the original downloader is used to download missing tile data
    - cache is updated with all existing tile data

    The cache getter function (`get` parameter) should return `None` if
    tile data is not in cache for given URL.

    A collection of tiles is returned.

    :param get: Function to get a tile data from cache.
    :param set: Function to put a tile data in cache.
    :param downloader: Original tiles downloader (asyncio coroutine).
    :param tiles: Collection tiles to fetch.
    :param num_workers: Number of workers used to connect to a map provider
        service.
    :param kw: Parameters passed to downloader coroutine.
    """
    tiles = fetch_from_cache(get, tiles)
    groups = partition_all(10, tiles)
    for tg in groups:
        missing = groupby(lambda t: t.img is None, tg)
        for t in missing.get(False, []):
            # reset cache for new and old tiles
            set(t.url, t.img)
            yield t

        result = downloader(missing.get(True, []), num_workers, **kw)
        async for t in result:
            # reset cache for new and old tiles
            set(t.url, t.img)
            yield t

def redis_downloader(client, downloader=None, timeout=3600 * 24 * 7):
    """
    Create downloader using Redis as cache for map tiles.

    :param client: Redis client object.
    :param downloader: Map tiles downloader, use `None` for default downloader.
    :param timeout: Map tile data expiry timeout, default 1 week.
    """
    if downloader is None:
        downloader = fetch_tiles
    set = lambda key, value: client.setex(key, value, timeout)
    return partial(caching_downloader, client.get, set, downloader)


# vim: sw=4:et:ai
