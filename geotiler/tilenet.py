#
# GeoTiler - library to create maps using tiles from a map provider
#
# NOTE: The code contains BSD licensed code from Modest Maps project.
#
# Copyright (C) 2013-2014 by Artur Wroblewski <wrobell@pld-linux.org>
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

from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import http.client
import io
import urllib.parse
import logging

import PIL.Image

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'GeoTiler/0.1.0',
}

@lru_cache()
def fetch(host, path, query):
    img = None

    conn = http.client.HTTPConnection(host)
    conn.request('GET', path + ('?' + query).rstrip('?'), headers=HEADERS)
    response = conn.getresponse()
    status = str(response.status)

    if status.startswith('2'):
        data = io.BytesIO(response.read())
        img = PIL.Image.open(data).convert('RGBA')

    return img


class TileRequest:

    # how many times to retry a failing tile
    MAX_ATTEMPTS = 5

    def __init__(self, provider, coord, offset):
        self.done = False
        self.provider = provider
        self.coord = coord
        self.offset = offset


    def images(self):
        return self.imgs


    def load(self):
        if self.done:
            # don't bother?
            return

        urls = self.provider.getTileUrls(self.coord)

        if __debug__:
            logger.debug('Requesting {}'.format(urls))

        # this is the time-consuming part
        try:
            imgs = []

            for (scheme, host, path, params, query, fragment) in map(urllib.parse.urlparse, urls):
                if scheme in ('file', ''):
                    img = PIL.Image.open(path).convert('RGBA')
                elif scheme == 'http':
                    img = fetch(host, path, query)
                imgs.append(img)
                self.done = True

            if __debug__:
                logger.debug('Received {}'.format(urls))

        except Exception as ex:
            logger.warn('Failed {}'.format(urls))
            logger.exception(ex)

            imgs = [None for url in urls]
            raise ex # FIXME: figure out better error handling strategy
                     # before making another download attempt to avoid
                     # unnecessary server request while dealing with
                     # ModestMaps errors

        self.imgs = imgs


class TileThreadDownloader(object):
    """
    Tile downloader based on thead pool executor.
    """
    def fetch(self, tiles):
        """
        Execute all tile requests.

        :param tiles: List of tile requests.
        """
        pool = ThreadPoolExecutor(max_workers=32)
        pool.map(lambda tile: tile.load(), tiles, timeout=5)
        pool.shutdown()



def render_tiles(tiles, size, downloader=None):
    """
    Download map tiles and render them as an image.

    The default tiles downloader is :py:class:`TileThreadDownloader`.

    :param tiles: List of tiles requests.
    :param size: Map image size.
    :param downloader: Map tiles downloader.
    """
    if downloader is None:
        downloader = TileThreadDownloader()

    tp = tiles[:]
    for k in range(TileRequest.MAX_ATTEMPTS):
        downloader.fetch(tiles)
        tp = [t for t in tp if not t.done]
        if not tp:
            break

    image = PIL.Image.new('RGB', size)

    for tile in tiles:
        try:
            for img in tile.images():
                image.paste(img, (int(tile.offset.x), int(tile.offset.y)), img)
        except Exception as ex:
            logger.warn('tile rendering error')
            logger.exception(ex)

    return image


# vim: sw=4:et:ai