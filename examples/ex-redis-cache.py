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
GeoTiler example to use Redis based cache for map tiles.
"""

import redis

from geotiler.tilenet import DEFAULT_TILE_DOWNLOADER
from geotiler.cache.redis import RedisCache

import geotiler

import logging
logging.basicConfig(level=logging.DEBUG)

downloader = DEFAULT_TILE_DOWNLOADER

# create the cache connecting to local Redis server
client = redis.Redis('localhost')
cache = RedisCache(client, downloader)

# override cache of default downloader
downloader.set_cache(cache)

bbox = 11.78560, 46.48083, 11.79067, 46.48283
mm = geotiler.Map(extent=bbox, zoom=18)

# render the map for the first time...
img = geotiler.render_map(mm)

# ... and second time to demonstrate use of the cache
img = geotiler.render_map(mm)

# show some recent keys
print('recent cache keys {}'.format(client.keys()[:10]))

# vim: sw=4:et:ai
