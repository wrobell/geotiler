Command Line Tools
==================

GeoTiler Lint Script
--------------------
GeoTiler provides `geotiler-lint` script, which can be used to create a map
image from command line.

For example, to create a map image using Blue Marble map tiles provider,
map center, zoom and map image size::

    geotiler-lint -c -6.069 53.390 -z 8 -s 512 512 -p bluemarble map-bluemarble.png

.. figure:: map-bluemarble.png
   :align: center

The script supports all implemented map tiles providers. Map can be
specified with any of the required map parameters combination. It allows to
switch map tiles caching strategy to use Redis cache.

Route Drawing
-------------
The `geotiler-route` script can be used to draw position information on
a map. The script uses GPX file (can be compressed with `Gzip`, `bzip2` or
`xz`) as its input.

For example::

    geotiler-route path.gpx map-path.png

.. figure:: map-path.png
   :align: center

The map extents are determined by aggregating positions stored in the input
file. The map zoom is automatically calculated from the map extent and map
image size.

Map Tiles Fetching
------------------
The `geotiler-fetch` script enables us to fetch map tiles and store them in
cache to be reused later by a map application. Optionally, map image can be
saved to a file for each zoom level.

To fetch OSM Cycle map tiles and save map images into files named
`map-01.png', `map-02.png`, ..., `map-19.png`::

    geotiler-fetch -p osm-cycle -f 'map-{:02d}.png' -6.0759 53.3830 -6.0584 53.3945

.. vim: sw=4:et:ai
