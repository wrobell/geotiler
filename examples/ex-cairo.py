# cairo example

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
