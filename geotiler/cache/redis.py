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
Cache for GeoTiler based on Redis.
"""

from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RedisCache(object):
    """
    Cache for GeoTiler based on Redis.

    :var client: Redis client object.
    :var downloader: Map tile downloader instance.
    :var timeout: Expiry time for the cached data.
    """

    def __init__(self, client, downloader, timeout=3600 * 24 * 7):
        """
        Create Redis based cache.

        :param client: Redis client object.
        :param downloader: Map tile downloader instance.
        :param timeout: Expiry time for the cached data.
        """
        self.client = client
        self.downloader = downloader
        self.timeout = timeout


    def __call__(self, f):
        """
        Wrap tile downloader's function `f` to cache the function results.

        :param f: Map tile downloader function, which results shall be
            cached.
        """
        @wraps(f)
        def wrapper(host, path, query):
            key = (host, path, query)
            if self.client.exists(key):
                if __debug__:
                    logger.debug('cache hit, key {}'.format(key))
                data = self.client.get(key)
                return data
            else:
                data = f(self.downloader, host, path, query)
                self.client.setex(key, data, self.timeout)
                if __debug__:
                    logger.debug('data stored in cache, key {}'.format(key))
                return data
        return wrapper


# vim: sw=4:et:ai
