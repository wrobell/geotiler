Using GeoTiler Library
======================

Rendering Map
-------------
Rendering a map with GeoTiler library consists of two steps

- create map object
- render map as an image

Map object is created using :py:class:`geotiler.Map` class. Its constructor
requires any of the following combinations of map parameters

- center, zoom and size
- extent and zoom
- extent and size

For example, to create map using first combination of the parameters above::

    >>> import geotiler
    >>> map = geotiler.Map(center=(-6.069, 53.390), zoom=16, size=(512, 512))
    >>> map.extent
    (-6.074495315551752, 53.38671986409586, -6.063508987426756, 53.39327172612266)

After creating a map object, map can be controlled with `extent`, `center`,
`zoom` and `size` attributes. Each attribute can influence other, i.e.
changing `extent` will change map size. Refer to the :py:class:`geotiler.Map`
class documentation for details.

Having map object, it can be rendered as an image with
:py:func:`geotiler.render_map` function::

    >>> image = geotiler.render_map(map) # doctest: +SKIP

.. figure:: map-osm.png
   :align: center

The rendered image is an instance of :py:class:`PIL.Image` class. Map image
can be used with other library like matplotlib or Cairo to render
additional map information, i.e. points of interests, GPS positions, text,
etc. See :ref:`integrate` section for examples.

Alternatively, the map image can be simply saved as a file::

    >>> image.save('map.png') # doctest: +SKIP

Map Providers
-------------
GeoTiler supports multiple map providers.

The list of available map providers is presented in the table below.

    ========================= =================== ==================
         Provider                Provider Id           License
    ========================= =================== ==================
     OpenStreetMap             osm                 `Open Data Commons Open Database License <http://www.openstreetmap.org/copyright>`_
     OpenStreetMap Cycle       osm-cycle           as above
     Stamen Toner              stamen-toner        `Creative Commons Attribution (CC BY 3.0) license <http://maps.stamen.com/>`_
     Stamen Terrain            stamen-terrain      as above
     Stamen Water Color        stamen-watercolor   as above
     Modest Maps Blue Marble   bluemarble          see `NASA guideline <http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html>`_
    ========================= =================== ==================

The default map provider is OpenStreetMap.

A map provider instance can be created with :py:func:`geotiler.find_provider`
function and the instance can be passed to :py:class:`geotiler.Map` class
constructor::

    >>> toner = geotiler.find_provider('stamen-toner')
    >>> map = geotiler.Map(center=(-6.069, 53.390), zoom=16, size=(512, 512), provider=toner)
    >>> image = geotiler.render_map(map) # doctest: +SKIP

.. figure:: map-stamen-toner.png
   :align: center

.. _integrate:

3rd Party Libraries
-------------------
Map image rendered by GeoTiler can be used with other library like
matplotlib or Cairo to draw additional map information or use the map in
data analysis graphs.

GeoTiler implements various examples of such integration. The examples are
presented in the sub sections below.

Cairo Example
~~~~~~~~~~~~~
.. literalinclude:: ../examples/ex-cairo.py
   :lines: 32-71

matplotlib Example
~~~~~~~~~~~~~~~~~~
.. literalinclude:: ../examples/ex-matplotlib.py
   :lines: 32-62

Matplotlib Basemap Toolkit Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ../examples/ex-basemap.py
   :lines: 32-72

Caching
-------
GeoTiler caches map tiles with simple LRU cache, which advantage is that it
requires no setup or additional software. Multiple calls to
:py:func:`geotiler.render_map` function will reuse already downloaded map
tiles, but the cache is not persistent - once a program or script exits,
the map tiles are discarded.

The default cache can be replaced with cache based on
`Redis <http://redis.io/>`_ store. While it requires Redis server and
Python `Redis module <https://pypi.python.org/pypi/redis/>`_ installed, it
provides map tiles persistence and advanced cache management.

The Redis cache example illustrates how default cache can be replaced with
Redis based one.

.. literalinclude:: ../examples/ex-redis-cache.py
   :lines: 32-61

GeoTiler Lint Script
--------------------
GeoTiler provides `geotiler-lint` script, which can be used to create a map
image from commandline.

For example, to create a map image using Blue Marble map tiles provider,
map center, zoom and map image size::

    # geotiler-lint -c -6.069 53.390 -z 8 -s 512 512 bluemarble map-bluemarble.png

.. figure:: map-bluemarble.png
   :align: center

The script supports all implemented map tiles providers. Map can be
specified with any of the required map parameters combination. It allows to
switch map tiles caching strategy to use Redis cache.

.. vim: sw=4:et:ai
