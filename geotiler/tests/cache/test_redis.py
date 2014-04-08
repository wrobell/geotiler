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
Redis cache unit tests.
"""

from geotiler.cache.redis import RedisCache

import unittest
from unittest import mock

class RedisCacheTestCase(unittest.TestCase):
    """
    Redis cache unit tests.
    """
    def test_wrapper(self):
        """
        Test Redis cache wrapper
        """ 
        client = mock.MagicMock()
        downloader = mock.MagicMock()
        f = lambda host, path, query: True

        cache = RedisCache(client, downloader)
        fc = cache(f)
        self.assertEqual(f, fc.__wrapped__)


    def test_updating_cache(self):
        """
        Test Redis cache update

        Check that valid paramaters are passed to underlying function and
        that cache got updated
        """ 
        client = mock.MagicMock()

        downloader = mock.MagicMock()
        data = mock.MagicMock()
        downloader.f.return_value = data

        cache = RedisCache(client, downloader)
        fc = cache(downloader.f) # function f with cachinig capability

        client.exists.return_value = False
        value = fc('host', 'path', 'query')
        self.assertEqual(data, value)
        downloader.f.assert_called_once_with(
            downloader, 'host', 'path', 'query'
        )
        
        client.setex.assert_called_once_with(
            ('host', 'path', 'query'),
            data,
            cache.timeout
        )


    def test_cache_use(self):
        """
        Test Redis cache use

        Verify that value is fetched from Redis cache on cache hit
        """ 
        client = mock.MagicMock()
        data = mock.MagicMock() # data returned from cache

        downloader = mock.MagicMock()

        cache = RedisCache(client, downloader)
        fc = cache(downloader.f) # function f with cachinig capability

        client.exists.return_value = True # cache hit
        client.get.return_value = data    # return data from cache

        value = fc('host', 'path', 'query')
        self.assertEqual(data, value)
        self.assertFalse(downloader.f.called)
        client.get.assert_called_once_with(('host', 'path', 'query'))


# vim: sw=4:et:ai
