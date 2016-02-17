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
Microsoft map tiles provider unit tests.
"""

from geotiler.provider.ms import fromMicrosoftRoad, toMicrosoftRoad, \
    fromMicrosoftAerial, toMicrosoftAerial

import unittest


class MSConversionTestCase(unittest.TestCase):
    """
    Microsfot conversion functions tests.
    """
    def test_from_ms_road(self):
        """
        Test conversion from MS road
        """
        result = fromMicrosoftRoad('0')
        self.assertEqual((0, 0, 1), result)

        result = fromMicrosoftRoad('0230102122203031')
        self.assertEqual((10507, 25322, 16), result)

        result = fromMicrosoftRoad('0230102033330212')
        self.assertEqual((10482, 25333, 16), result)


    def test_to_ms_road(self):
        """
        Test conversion to MS road
        """
        result = toMicrosoftRoad(0, 0, 1)
        self.assertEqual('0', result)

        result = toMicrosoftRoad(10507, 25322, 16)
        self.assertEqual('0230102122203031', result)

        result = toMicrosoftRoad(10482, 25333, 16)
        self.assertEqual('0230102033330212', result)


    def test_from_ms_aerial(self):
        """
        Test conversion from MS aerial
        """
        result = fromMicrosoftAerial('0')
        self.assertEqual((0, 0, 1), result)

        result = fromMicrosoftAerial('0230102122203031')
        self.assertEqual((10507, 25322, 16), result)

        result = fromMicrosoftAerial('0230102033330212')
        self.assertEqual((10482, 25333, 16), result)


    def test_to_ms_aerial(self):
        """
        Test conversion to MS aerial
        """
        result = toMicrosoftAerial(0, 0, 1)
        self.assertEqual('0', result)

        result = toMicrosoftAerial(10507, 25322, 16)
        self.assertEqual('0230102122203031', result)
        result = toMicrosoftAerial(10482, 25333, 16)
        self.assertEqual('0230102033330212', result)


# vim:et sts=4 sw=4:
