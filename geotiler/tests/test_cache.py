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
Caching downloader unit tests.
"""

import asyncio
from functools import partial

from geotiler.cache import caching_downloader, redis_downloader

import unittest
from unittest import mock

class CachingDownloaderTestCase(unittest.TestCase):
    """
    Caching downloader tests.
    """
    def test_caching_all(self):
        """
        Test caching downloader for all tiles to be fetched
        """
        @asyncio.coroutine
        def images(urls):
            return 'img1', 'img2'

        cache = mock.MagicMock()
        downloader = partial(caching_downloader, cache.get, cache.set, images)

        loop = asyncio.get_event_loop()

        cache.get.side_effect = [None, None]
        task = downloader(['url1', 'url2'])
        result = loop.run_until_complete(task)
        self.assertEqual(['img1', 'img2'], list(result))

        args = [v[0][0] for v in cache.get.call_args_list]
        self.assertEqual(['url1', 'url2'], args)


    def test_caching_missing(self):
        """
        Test caching downloader for some tiles to be fetched
        """
        @asyncio.coroutine
        def images(urls):
            self.assertEqual(('url1', 'url4'), urls)
            return 'img1', 'img4'

        cache = mock.MagicMock()
        downloader = partial(caching_downloader, cache.get, cache.set, images)

        loop = asyncio.get_event_loop()

        cache.get.side_effect = [None, 'img2', 'img3', None]
        task = downloader(['url1', 'url2', 'url3', 'url4'])
        result = loop.run_until_complete(task)
        self.assertEqual(['img1', 'img2', 'img3', 'img4'], list(result))

        args = [v[0][0] for v in cache.get.call_args_list]
        self.assertEqual(['url1', 'url2', 'url3', 'url4'], args)

        args = sorted(v[0] for v in cache.set.call_args_list)
        self.assertEqual(4, len(args))
        self.assertEqual(('url1', 'img1'), args[0])
        self.assertEqual(('url2', 'img2'), args[1])
        self.assertEqual(('url3', 'img3'), args[2])
        self.assertEqual(('url4', 'img4'), args[3])



class RedisCacheTestCase(unittest.TestCase):
    """
    Redis cache unit tests.
    """
    def test_redis_downloader(self):
        """
        Test creating Redis downloader
        """
        @asyncio.coroutine
        def images(urls):
            return 'img1', 'img2', 'img3'

        client = mock.MagicMock()
        client.get.side_effect = ['img1', 'img2', 'img3']
        downloader = redis_downloader(client, downloader=images, timeout=10)
        self.assertEqual(caching_downloader, downloader.func)

        task = downloader(['url1', 'url2', 'url3'])
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(task)

        args = [v[0][0] for v in client.get.call_args_list]
        self.assertEqual(['url1', 'url2', 'url3'], args)

        args = sorted(v[0] for v in client.setex.call_args_list)
        self.assertEqual(3, len(args))
        self.assertEqual(('url1', 'img1', 10), args[0])
        self.assertEqual(('url2', 'img2', 10), args[1])
        self.assertEqual(('url3', 'img3', 10), args[2])


# vim: sw=4:et:ai
