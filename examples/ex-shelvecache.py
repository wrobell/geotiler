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

import geotiler
from functools import partial
from geotiler.cache import caching_downloader
from geotiler.tile.io import fetch_tiles
import shelve
import time


#
# Make it default GeoTiler cache? We need to
#
# - create shelve file per map provider in ~/.geotiler/ directory
# - figure out key timestamp issue
# - unit tests
#
class Cache:
    """
    Cache based on Python's `shelve` module to keep map tiles.

    WARNING: There is nothing that prevents cache from growing very large
    and also nothing which determines if the data is recent (however the
    time at the moment something is placed in the database is saved).
    """
    def __init__(self, filename):
        """
        Opens an existing shelve and create new one if it does not exist.

        :param filename: Filename for the shelve.
        """
        self.cache = shelve.open(filename, writeback=True)


    def get(self, key):
        """
        Get map tile from cache.

        Null is returned if key does not exist.

        :param key: Key used to retrieve data from the cache.
        """
        try:
            data = self.cache[key][0]
        except:
            data = None
        return data


    def set(self, key, data):
        """
        Stores map tile in cache.

        The data is stored as (tile data, time) tuple.

        :param key: Key used to identify the data.
        :param data: Map tile data.
        """
        if key not in self.cache:
            self.cache[key] = (data, time.time())
        return


    def close(self):
        """
        Close the shelve used to cache the data.
        """
        self.cache.close()


# Create a cache instance
cache = Cache("test")

# Create a new downloader using the shelve cache
downloader = partial(caching_downloader, cache.get, cache.set, fetch_tiles)

# Set render_map to use new downloader function
render_map = partial(geotiler.render_map, downloader=downloader)

mm = geotiler.Map(center=(0.0, 51.47879), zoom=18, size=(1900, 1000))

# Render map for first time and save current time
t1 = time.time()
img = render_map(mm)
t2 = time.time()

# Render map for the second time to demonstrate the speed of the cache
img = render_map(mm)
t3 = time.time()

# Close the cache
cache.close()

print('time for first render: {:6.5f} seconds'.format(t2 - t1))
print('time for second render: {:6.5f} seconds'.format(t3 - t2))

# vim: sw=4:et:ai
