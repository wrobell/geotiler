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
Functions and coroutines to download map tiles.
"""

import asyncio
import urllib.request
import logging

from functools import partial

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'GeoTiler/0.10.0',
}

FMT_DOWNLOAD_LOG = 'Cannot download a tile due to error: {}'.format

def fetch_tile(url):
    """
    Fetch map tile.

    If response status is not HTTP OK (`200`), then `ValueError` exception
    is raised.

    :param url: URL of map tile.
    """
    request = urllib.request.Request(url)
    for k, v in HEADERS.items():
        request.add_header(k, v)

    response = urllib.request.urlopen(request)
    if response.status != 200:
        fmt = 'Unable to download {} (HTTP status {})'.format
        raise ValueError(fmt(url, response.status))

    return response.read()


@asyncio.coroutine
def fetch_tiles(urls, loop=None):
    """
    Download map tiles for the collection of URLs.

    This is asyncio coroutine.

    Tile data for each URL is returned. If there was an error while
    downloading a tile, then None is returned for given URL.

    :param urls: Collection of URLs.
    """
    if __debug__:
        logger.debug('fetching tiles...')

    if loop is None:
        loop = asyncio.get_event_loop()

    # TODO: is it possible to call `urllib.request` in real async mode
    # without executor by creating appropriate opener? running in executor
    # sucks, but thanks to `urllib.request` we get all the goodies like
    # automatic proxy handling and various protocol support
    f = partial(loop.run_in_executor, None, fetch_tile)
    tasks = (f(u) for u in urls)
    data = yield from asyncio.gather(*tasks, loop=loop, return_exceptions=True)

    if __debug__:
        logger.debug('fetching tiles done')

    # log missing tiles
    in_error = (t for t in data if isinstance(t, Exception))
    for t in in_error:
        logger.warning(FMT_DOWNLOAD_LOG(t))

    return (None if isinstance(t, Exception) else t for t in data)


# vim: sw=4:et:ai
