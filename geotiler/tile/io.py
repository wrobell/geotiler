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

import aiohttp
import asyncio
import logging
from functools import partial

from geotiler import __version__

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'GeoTiler/{}'.format(__version__),
}

# client session params
PARAMS = {
    'headers': HEADERS,
    'trust_env': True,
    'raise_for_status': True,
}

FMT_DOWNLOAD_LOG = 'Cannot download a tile due to error: {}'.format
FMT_DOWNLOAD_ERROR = 'Unable to download {} (error: {})'.format

async def fetch_tile(session, tile):
    """
    Fetch map tile.

    :param tile: Map tile.
    """
    try:
        async with session.get(tile.url) as response:
            data = await response.read()
    except aiohttp.ClientError as ex:
        error = ValueError(FMT_DOWNLOAD_ERROR(tile.url, ex))
        tile = tile._replace(img=None, error=error)
    else:
        tile = tile._replace(img=data, error=None)

    return tile

async def fetch_tiles(tiles, num_workers):
    """
    Download map tiles.

    Asynchronous generator of map tiles is returned.

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

    # respect connection limits by defining custom connector
    connector = aiohttp.TCPConnector(limit_per_host=num_workers)

    # use `trust_env` to get proxy configuration via env variables
    async with aiohttp.ClientSession(connector=connector, **PARAMS) as session:
        f = partial(fetch_tile, session)
        tasks = [f(t) for t in tiles]
        for task in asyncio.as_completed(tasks):
            tile = await task  # no exception expected at this stage

            if tile.error:
                logger.warning(FMT_DOWNLOAD_LOG(tile.error))

            yield tile

    if __debug__:
        logger.debug('fetching tiles done')

# vim: sw=4:et:ai
