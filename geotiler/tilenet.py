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
GeoTiler map tiles downloading functionality.

To download map tiles and render them as a single image use
:py:func:`render_tiles` function.

The :py:class:`TileThreadDownloader` implements default tiles downloading
strategy. New strategy can be implemented by deriving from
:py:class:`TileDownloader` abstract class.
"""

from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import http.client
import io
import sys
import traceback
import urllib.parse
import logging

import PIL.Image
import PIL.ImageDraw

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'GeoTiler/0.3.0',
}

MAX_ATTEMPTS = 5 # how many times to retry a failing tile


class TileRequest(object):
    """
    Tile request information.

    :var provider: Map tile provider.
    :var coord: Map tile coordinate.
    :var zoom: Map zoom level.
    :var offset: Tile position on map image.
    :var images: List of downloaded tile images.
    :var done: Downloaded if true.
    """
    def __init__(self, provider, coord, zoom, offset):
        self.provider = provider
        self.coord = coord
        self.zoom = zoom
        self.offset = offset
        self.images = []
        self.done = False



class TileDownloader(object):
    """
    Tile downloader abstract class.
    """
    def fetch_tile(self, tile):
        """
        Download tile images.

        The method returns list of images, each being instance of PIL image.

        :param tile: Tile to download.
        """
        if tile.done:
            # don't bother?
            return

        urls = tile.provider.get_tile_urls(tile.coord, tile.zoom)

        if __debug__:
            logger.debug('Requesting {}'.format(urls))

        # this is the time-consuming part
        try:
            images = []

            for (scheme, host, path, params, query, fragment) in map(urllib.parse.urlparse, urls):
                if scheme in ('file', ''):
                    data = open(path)
                else:
                    assert scheme == 'http'
                    data = self.fetch_image(host, path, query)
                    data = io.BytesIO(data)

                img = PIL.Image.open(data).convert('RGBA')
                images.append(img)
                tile.done = True

            if __debug__:
                logger.debug('received {}'.format(urls))

        except Exception as ex:
            # on error log the information and set downloaded images to
            # null; the renderer will handle this
            msg = 'failed to download tile at {}'.format(urls)
            logger.warning(msg)
            msg = ''.join(traceback.format_exception(*sys.exc_info()))
            logger.debug(msg)

            images = [None for url in urls]

        tile.images = images


    @lru_cache()
    def fetch_image(self, host, path, query):
        """
        Fetch an image using HTTP connection.

        The method returns instance of PIL image.

        :param host: HTTP server.
        :param path: HTTP path.
        :param query: HTTP query.
        """
        data = None

        conn = http.client.HTTPConnection(host)
        conn.request('GET', path + ('?' + query).rstrip('?'), headers=HEADERS)
        response = conn.getresponse()
        status = str(response.status)

        if status.startswith('2'):
            data = response.read()

        return data


    def set_cache(self, cache):
        """
        Override existing map tile downloader cache.

        The cache decorator function takes
        :py:func:`TileDownloader.fetch_image` function as an argument and
        creates a wrapper, which caches the results of the
        :py:func:`TileDownloader.fetch_image` function.

        :param cache: Cache decorator function.

        .. seealso:: :py:class:`geotiler.cache.redis.RedisCache`
        """
        self.fetch_image = cache(self.fetch_image.__wrapped__)


    def fetch(self, tiles):
        """
        Execute all tile requests.

        :param tiles: List of tile requests.
        """
        raise NotImplementedError()



class TileThreadDownloader(TileDownloader):
    """
    Tile downloader based on thead pool executor.
    """
    def fetch(self, tiles):
        """
        Execute all tile requests.

        :param tiles: List of tile requests.
        """
        pool = ThreadPoolExecutor(max_workers=32)
        pool.map(self.fetch_tile, tiles, timeout=5)
        pool.shutdown()



def render_tiles(provider, zoom, size, tiles, downloader=None):
    """
    Download map tiles and render them as an image.

    The default tiles downloader is :py:class:`TileThreadDownloader`.

    :param provider: Map tiles provider.
    :param zoom: Map zoom level.
    :param size: Map image size.
    :param tiles: List of tile coordinates and their map image positions.
    :param downloader: Map tiles downloader.
    """
    if downloader is None:
        downloader = DEFAULT_TILE_DOWNLOADER

    tile_req = [TileRequest(provider, t[0], zoom, t[1]) for t in tiles]
    requests = tile_req[:]
    for k in range(MAX_ATTEMPTS):
        downloader.fetch(requests)
        requests = [t for t in requests if not t.done]
        if not requests:
            break

    image = PIL.Image.new('RGB', size)

    for tile in tile_req:
        try:
            for img in tile.images:
                # no image, so there was error when downloading a tile
                # draw error message in such case
                if not img:
                    w, h = provider.tile_width, provider.tile_height
                    img = PIL.Image.new('RGBA', (w, h))
                    draw = PIL.ImageDraw.Draw(img)
                    msg = 'Map tile download error.'
                    tw, th = draw.textsize(msg)
                    draw.text(((w - tw) // 2, (h - th) // 2), msg, 'red')

                image.paste(img, tile.offset, img)
        except Exception as ex:
            logger.warning('tile rendering error')
            logger.exception(ex)

    return image

DEFAULT_TILE_DOWNLOADER = TileThreadDownloader()

# vim: sw=4:et:ai
