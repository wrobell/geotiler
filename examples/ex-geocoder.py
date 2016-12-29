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
Python Geocoder example.
"""

import geocoder

import logging
logging.basicConfig(level=logging.DEBUG)

import geotiler

#
# find coordinates of Moscone Center
#
gc = geocoder.google('Moscone Center')
y, x = gc.latlng

#
# download map using OpenStreetMap
#
mm = geotiler.Map(center=(x, y), zoom=18, size=(512, 512))
img = geotiler.render_map(mm)

#
# save map image as PNG file
#
img.save('ex-geocoder.png')

# vim: sw=4:et:ai
