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
Caching strategies for GeoTiler.
"""

import asyncio
import logging
from functools import partial

from geotiler.tile.io import fetch_tiles

logger = logging.getLogger(__name__)

@asyncio.coroutine
def caching_downloader(get, set, downloader, urls, **kw):
    """
    Create caching map tiles downloader.

    This is asyncio coroutine.

    The code flow is

    - caching downloader gets tiles from cache using URLs
    - the original downloader is used to download missing tiles
    - cache is updated with all existing tiles

    The cache getter function (`get` parameter) should return `None` if
    tile data is not in cache for given URL.

    The collection of tile data is returned for each input URL (or `None`
    if tile data could not be obtained).

    :param get: Function to get a tile from cache.
    :param set: Function to put a tile in cache.
    :param downloader: Original tiles downloader (asyncio coroutine).
    :param urls: Collection of URLs of tiles.
    :param kw: Parameters passed to downloader coroutine.
    """
    data = {u: get(u) for u in urls}
    if __debug__:
        items = (u for u, v in data.items() if v is not None)
        for u in items:
            logger.debug('cache hit for {}'.format(u))

    # download missing tiles, keep the order of urls
    missing = tuple(u for u in urls if data[u] is None)
    result = yield from downloader(missing, **kw)
    data.update(zip(missing, result))

    # reset cache for new and old tiles
    existing = ((u, t) for u, t in data.items() if t)
    for u, t in existing:
        set(u, t)

    # keep the original order
    return (data[u] for u in urls)


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
