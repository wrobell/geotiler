Command Line Tools
==================

GeoTiler Lint Script
--------------------
GeoTiler provides `geotiler-lint` script, which can be used to create a map
image from commandline.

For example, to create a map image using Blue Marble map tiles provider,
map center, zoom and map image size::

    geotiler-lint -c -6.069 53.390 -z 8 -s 512 512 bluemarble map-bluemarble.png

.. figure:: map-bluemarble.png
   :align: center

The script supports all implemented map tiles providers. Map can be
specified with any of the required map parameters combination. It allows to
switch map tiles caching strategy to use Redis cache.

.. vim: sw=4:et:ai
