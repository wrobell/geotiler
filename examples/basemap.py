# Matplotlib Basemap Toolkit example

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import ModestMaps

# background map dimensions
WIDTH = 512
HEIGHT = 512

bbox = 11.774086, 46.461487999999996, 11.817339, 46.482649
xc, yc = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)

#
# download background map using OpenStreetMap
#
dimensions = ModestMaps.Core.Point(WIDTH, HEIGHT)
loc1 = ModestMaps.Geo.Location(bbox[1], bbox[0])
loc2 = ModestMaps.Geo.Location(bbox[3], bbox[2])

cls = ModestMaps.builtinProviders['OPENSTREETMAP']
provider = cls()
map = ModestMaps.mapByExtent(provider, loc1, loc2, dimensions)
img = map.draw(True, False) # or simply save in tile cache, i.e. in
                            # <tile> file, see below for `imread` also

#
# create basemap
#
map = Basemap(
    llcrnrlon=bbox[0], llcrnrlat=bbox[1],
    urcrnrlon=bbox[2], urcrnrlat=bbox[3],
    rsphere=(6378137.00, 6356752.3142),
    resolution='h', projection='lcc', ax=ax,
    lon_0=xc, lat_0=yc
)

# or optionally, read from tile cache: im = plt.imread(<tile>)
map.imshow(img, interpolation='lanczos', origin='upper')

#
# plot 3 custom points
#
x0, y0 = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
dx = 0.0001
dy = 0.0005
x, y = map(
    (x0, x0 - dx, x0 + dx),
    (y0, y0 - dy, y0 + dy)
)
ax.scatter(x, y, c='red', edgecolor='none', s=10, alpha=0.9)

plt.savefig('test.pdf', bbox_inches='tight')
plt.close()

# vim: sw=4:et:ai
