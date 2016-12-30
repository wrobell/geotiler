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
Render map image using map tile data.
"""

import io
import functools
import logging

import PIL.Image
import PIL.ImageDraw

logger = logging.getLogger(__name__)


def render_image(map, tile_data, offsets):
    """
    Redner map image using map tile data.

    Each item in tile data collection is tile image data, which can be
    interpreted with `PIL` library (via `PIL.Image.open` call, i.e. PNG
    file data or JPEG file data). The item can also be `None` if tile data
    could not be downloaded, i.e. due to network error.

    The map tiles are rendered into single map image. Error tile image is
    rendered if data for a tile does not exist.

    The PIL image object is returned.

    :param map: Map object.
    :param tile_data: Collection of tile data.
    :param offsets: Tile offset within map image for each tile data item.
    """
    if __debug__:
        logger.debug('combining tiles')

    provider = map.provider

    # PIL requires image size to be a tuple
    image = PIL.Image.new('RGBA', tuple(map.size))
    error = _error_image(provider.tile_width, provider.tile_height)

    for tile, offset in zip(tile_data, offsets):
        img = _tile_image(tile) if tile else error
        image.paste(img, offset)

    return image


@functools.lru_cache(maxsize=4)
def _error_image(width, height):
    """
    Create error tile image.

    The error tile image is PIL image object showing message that a map
    tile could not be downloaded.

    :param width: Width of tile image.
    :param height: Height of tile image.
    """
    img = PIL.Image.new('RGBA', (width, height))
    draw = PIL.ImageDraw.Draw(img)
    msg = 'Error downloading map tile.'
    tw, th = draw.textsize(msg)
    draw.text(((width - tw) // 2, (height - th) // 2), msg, 'red')
    return img


def _tile_image(data):
    """
    Convert image data like PNG file data or JPEG file data into
    `PIL.Image` object.

    :param data: Tile data, i.e. PNG file data.
    """
    f = io.BytesIO(data)
    return PIL.Image.open(f).convert('RGBA')


# vim: sw=4:et:ai
