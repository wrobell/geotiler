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
Functions and coroutines to download map tiles.
"""

import asyncio
import urllib.request
import logging
from concurrent import futures
from functools import partial, lru_cache

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'GeoTiler/0.13.0',
}

FMT_DOWNLOAD_LOG = 'Cannot download a tile due to error: {}'.format
FMT_DOWNLOAD_ERROR = 'Unable to download {} (HTTP status {})'.format

def fetch_tile(tile):
    """
    Fetch map tile.

    :param tile: Map tile.
    """
    request = urllib.request.Request(tile.url)
    for k, v in HEADERS.items():
        request.add_header(k, v)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as ex:
        error = ValueError(FMT_DOWNLOAD_ERROR(tile.url, ex.code))
        tile = tile._replace(img=None, error=error)
    else:
        tile = tile._replace(img=response.read(), error=None)

    return tile

async def fetch_tiles(tiles, num_workers):
    """
    Download map tiles.

    This is asyncio coroutine.

    A collection of tiles is returned. Each successfully downloaded tile
    has `Tile.img` attribute set. If there was an error while downloading
    a tile, then `Tile.img` is set to null and `Tile.error` to a value error.

    :param tiles: Collection of tiles.
    :param num_workers: Number of workers used to connect to a map provider
        service.
    """
    if __debug__:
        logger.debug('fetching tiles...')

    loop = asyncio.get_event_loop()

    # TODO: is it possible to call `urllib.request` in real async mode
    # without executor by creating appropriate opener? running in executor
    # sucks, but thanks to `urllib.request` we get all the goodies like
    # automatic proxy handling and various protocol support
    pool = create_pool(num_workers)
    f = partial(loop.run_in_executor, pool, fetch_tile)
    tasks = (f(t) for t in tiles)
    tiles = await asyncio.gather(*tasks, return_exceptions=True)

    if __debug__:
        logger.debug('fetching tiles done')

    # log missing tiles
    for t in tiles:
        if t.error:
            logger.warning(FMT_DOWNLOAD_LOG(t.error))

    return tiles

@lru_cache(maxsize=2)
def create_pool(num):
    """
    Create thread pool executor with a number of workers.

    :param num: Number of workers to create.
    """
    return futures.ThreadPoolExecutor(
        max_workers=num, thread_name_prefix='geotiler'
    )

# vim: sw=4:et:ai
