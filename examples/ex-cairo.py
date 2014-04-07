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
Cairo example.
"""

import cairo
import logging
import numpy

logging.basicConfig(level=logging.DEBUG)

import geotiler

bbox = 11.78560, 46.48083, 11.79067, 46.48283

#
# download background map using OpenStreetMap
#
mm = geotiler.Map(extent=bbox, zoom=18)
width, height = mm.size

img = geotiler.render_map(mm)
buff = bytearray(img.tobytes())

# raises "not implemented error", implemented in pycairo git...
surface = cairo.ImageSurface.create_for_data(
    buff, cairo.FORMAT_ARGB32, width, height
)

# ... so that's all folks at the moment

# vim: sw=4:et:ai
