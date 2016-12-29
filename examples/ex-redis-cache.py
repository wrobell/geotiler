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
GeoTiler example to use Redis based cache for map tiles.
"""

import functools
import redis

import geotiler
from geotiler.cache import redis_downloader

import logging
logging.basicConfig(level=logging.DEBUG)

# create tile downloader with Redis client as cache
client = redis.Redis('localhost')
downloader = redis_downloader(client)

# use map renderer with new downloader
render_map = functools.partial(geotiler.render_map, downloader=downloader)

bbox = 11.78560, 46.48083, 11.79067, 46.48283
mm = geotiler.Map(extent=bbox, zoom=18)

# render the map for the first time...
img = render_map(mm)

# ... and second time to demonstrate use of the cache
img = render_map(mm)

# show some recent keys
print('recent cache keys {}'.format(client.keys()[:10]))

# vim: sw=4:et:ai
