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
Cairo example.
"""

import cairocffi as cairo
import logging
import math

logging.basicConfig(level=logging.DEBUG)

import geotiler

bbox = 11.78560, 46.48083, 11.79067, 46.48283

#
# download background map using default map tiles provider - OpenStreetMap
#
mm = geotiler.Map(extent=bbox, zoom=18)
width, height = mm.size

img = geotiler.render_map(mm)

#
# create cairo surface
#
buff = bytearray(img.convert('RGBA').tobytes('raw', 'BGRA'))
surface = cairo.ImageSurface.create_for_data(
    buff, cairo.FORMAT_ARGB32, width, height
)
cr = cairo.Context(surface)

#
# plot circles around custom points
#
x0, y0 = 11.78816, 46.48114 # http://www.openstreetmap.org/search?query=46.48114%2C11.78816
x1, y1 = 11.78771, 46.48165 # http://www.openstreetmap.org/search?query=46.48165%2C11.78771
points = ((x0, y0), (x1, y1))
points = (mm.rev_geocode(p) for p in points)
for x, y in points:
    cr.set_source_rgba(0.0, 0.0, 1.0, 0.1)
    cr.arc(x, y, 30, 0, 2 * math.pi)
    cr.fill()

surface.write_to_png('ex-cairo.png')

# vim: sw=4:et:ai
