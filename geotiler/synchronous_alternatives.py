#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2020 by Artur Wroblewski <wrobell@riseup.net>
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
This file has synchronous versions of functions in .map and .tile
This will compromise the speed at which these functions run, however in the case that you require
a single threaded version of these functions this may be useful. It can help with running code
on WSGI servers.
"""

import logging
from functools import partial
from .map import fetch_tiles
from .tile.img import _error_image, _tile_image
from .tile.io import HEADERS
import requests
import PIL.Image  # type: ignore
import PIL.ImageDraw  # type: ignore

logger = logging.getLogger(__name__)


def synchronous_render_image(map, tiles):
    if __debug__:
        logger.debug("combining tiles")
    provider = map.provider

    # PIL requires image size to be a tuple
    image = PIL.Image.new("RGBA", tuple(map.size))
    error = _error_image(provider.tile_width, provider.tile_height)

    for tile in tiles:
        img = _tile_image(tile.img) if tile.img else error
        image.paste(img, tile.offset)

    return image


def synchronous_render_map(map, tiles=None, **kw):
    if not tiles:
        tiles = fetch_tiles(map, synchronous_fetch_tiles, **kw)

    return synchronous_render_image(map, tiles)


def synchronous_fetch_tiles(tiles, num_workers):
    if __debug__:
        logger.debug("fetching tiles...")

        with requests.Session() as session:
            f = partial(synchronous_fetch_tile, session)
            tasks = [f(t) for t in tiles]
            for task in tasks:
                tile = task
                yield tile

    if __debug__:
        logger.debug("fetching tiles done")


def synchronous_fetch_tile(session, tile):
    try:
        with session.get(tile.url, headers=HEADERS) as response:
            data = response.content
    except Exception as e:
        logger.error(e)
        tile = tile._replace(img=None, error="Error")
    else:
        tile = tile._replace(img=data, error=None)

    return tile
