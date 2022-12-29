#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2022 by Artur Wroblewski <wrobell@riseup.net>
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
Example of downloading map tiles and then rendering them as a map.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

import asyncio
import geotiler

def log_error(tile):
    if tile.error:
        print('tile {} error: {}'.format(tile.url, tile.error))
    return tile

async def fetch(mm):
    tiles = geotiler.fetch_tiles(mm)
    # process tile in error and then render all the tiles
    tiles = (log_error(t) async for t in tiles)
    img = await geotiler.render_map_async(mm, tiles=tiles)
    return img


bbox = 11.78560, 46.48083, 11.79067, 46.48283
mm = geotiler.Map(extent=bbox, zoom=18)

loop = asyncio.get_event_loop()

img = loop.run_until_complete(fetch(mm))
img.save('ex-fetch-tiles.png', 'png')

# vim: sw=4:et:ai
