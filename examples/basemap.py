# Matplotlib Basemap Toolkit example

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point

import logging
logging.basicConfig(level=logging.DEBUG)

import geotiler

# background map dimensions
WIDTH = 512
HEIGHT = 512

bbox = 11.78560, 46.48083, 11.79067, 46.48283

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)

#
# download background map using OpenStreetMap
#
extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
zoom = 17
size = 472, 270
center = 11.788137, 46.481832
#mm = geotiler.Map(center=center, zoom=zoom, size=size)
#mm = geotiler.Map(extent=extent, size=size)
mm = geotiler.Map(extent=extent, zoom=zoom)
#mm.extent = 11.785604953765853, 46.48083418203029, 11.790668964386, 46.4828288639531
#mm.extent = 11.785610, 46.480830, 11.790680, 46.482840
#mm.zoom = 20
#mm.size = WIDTH, HEIGHT

img = geotiler.render_map(mm)
bbox = mm.extent  # recalculate bbox, which can change due to requested
                  # image size

#
# create basemap
#
map = Basemap(
    llcrnrlon=bbox[0], llcrnrlat=bbox[1],
    urcrnrlon=bbox[2], urcrnrlat=bbox[3],
    projection='merc', ax=ax
)

# or optionally, read from tile cache: im = plt.imread(<tile>)
map.imshow(img, interpolation='lanczos', origin='upper')

#
# plot 3 custom points
#
x0, y0 = 11.78816, 46.48114 # http://www.openstreetmap.org/search?query=46.48114%2C11.78816
x1, y1 = 11.78771, 46.48165 # http://www.openstreetmap.org/search?query=46.48165%2C11.78771
x, y = map((x0, x1), (y0, y1))
ax.scatter(x, y, c='red', edgecolor='none', s=10, alpha=0.9)

plt.savefig('test.pdf', bbox_inches='tight')
plt.close()

# vim: sw=4:et:ai
