#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@pld-linux.org>
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
Yahoo map tiles provider unit tests.
"""

from geotiler.provider.yahoo import fromYahooRoad, toYahooRoad, \
    fromYahooAerial, toYahooAerial

import unittest

class YahooConvertTestCase(unittest.TestCase):
    """
    Yahoo conversion functions tests.
    """
    def test_from_yahoo_road(self):
        """
        Test column conversion from Yahoo road
        """
        result = fromYahooRoad(0, 0, 17)
        self.assertEqual((0, 0, 1), result)

        result = fromYahooRoad(10507, 7445, 2)
        self.assertEqual((10507, 25322, 16), result)

        result = fromYahooRoad(10482, 7434, 2)
        self.assertEqual((10482, 25333, 16), result)


    def test_to_yahoo_road(self):
        """
        Test column converstion to Yahoo road
        """
        result = toYahooRoad(0, 0, 1)
        self.assertEqual((0, 0, 17), result)

        result = toYahooRoad(10507, 25322, 16)
        self.assertEqual((10507, 7445, 2), result)

        result = toYahooRoad(10482, 25333, 16)
        self.assertEqual((10482, 7434, 2), result)


    def test_from_yahoo_aerial(self):
        """
        Test column converstion from Yahoo aerial
        """
        result = fromYahooAerial(0, 0, 17)
        self.assertEqual((0, 0, 1), result)

        result = fromYahooAerial(10507, 7445, 2)
        self.assertEqual((10507, 25322, 16), result)

        result = fromYahooAerial(10482, 7434, 2)
        self.assertEqual((10482, 25333, 16), result)


    def test_to_yahoo_aerial(self):
        """
        Test column converstion to Yahoo aerial
        """
        result = toYahooAerial(0, 0, 1)
        self.assertEqual((0, 0, 17), result)

        result = toYahooAerial(10507, 25322, 16)
        self.assertEqual((10507, 7445, 2), result)

        result = toYahooAerial(10482, 25333, 16)
        self.assertEqual((10482, 7434, 2), result)


# vim:et sts=4 sw=4:
