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

Having map object, the map tiles can be downloaded and rendered as an image
with :py:func:`geotiler.render_map` function::

    >>> image = geotiler.render_map(map) # doctest: +SKIP

.. figure:: map-osm.png
   :align: center

The rendered image is an instance of :py:class:`PIL.Image` class. Map image
can be used with other library like matplotlib or Cairo to render
additional map information, i.e. points of interests, GPS positions, text,
etc. See :ref:`integrate` section for examples.

Alternatively, the map image can be simply saved as a file::

    >>> image.save('map.png') # doctest: +SKIP

Asynchronous Map Rendering
--------------------------
The `asyncio` Python framework enables programmers to write asynchronous,
concurrent programs using coroutines.

GeoTiler allows to asynchronously download map tiles and render map image
with :py:func:`geotiler.render_map_async` `asyncio` coroutine.

Very simple example to download a map using `asyncio` framework::

    >>> coro = geotiler.render_map_async(map)  # doctest: +SKIP
    >>> loop = asyncio.get_event_loop()        # doctest: +SKIP
    >>> image = loop.run_until_complete(coro)  # doctest: +SKIP

We include more complex example below. It reads location data from `gpsd
<http://www.catb.org/gpsd/>`_ daemon, renders the map at the centre of
current position and saves map to a file. There are two concurrent tasks
running concurrently

- location reading
- map tiles downloading and rendering

The tasks communication is done via a queue holding current position.

.. literalinclude:: ../examples/ex-async-gps.py
   :lines: 51-89

Map Providers
-------------
GeoTiler supports multiple map providers.

The list of supported map providers is presented in the table below.

    ========================= ===================== ==================
         Provider                Provider Id           License
    ========================= ===================== ==================
     OpenStreetMap             osm                   `Open Data Commons Open Database License <http://www.openstreetmap.org/copyright>`_
     OpenStreetMap Cycle       osm-cycle             as above
     Stamen Toner              stamen-toner          `Creative Commons Attribution (CC BY 3.0) license <http://maps.stamen.com/>`_
     Stamen Toner Lite         stamen-toner-lite     as above
     Stamen Terrain            stamen-terrain        as above
     Stamen Water Color        stamen-watercolor     as above
     Modest Maps Blue Marble   bluemarble            see `NASA guideline <http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html>`_
    ========================= ===================== ==================

The default map provider is OpenStreetMap.

Identificators of GeoTiler map providers can be listed with
:py:func:`geotiler.providers` function. Map provider identificator can be
used with :py:func:`geotiler.find_provider` function to create instance of
map provider or it can be passed to :py:class:`geotiler.Map` class
constructor::

    >>> map = geotiler.Map(center=(-6.069, 53.390), zoom=16, size=(512, 512), provider='stamen-toner')
    >>> image = geotiler.render_map(map) # doctest: +SKIP

    # or

    >>> map = geotiler.Map(center=(-6.069, 53.390), zoom=16, size=(512, 512))
    >>> map.provider = geotiler.find_provider('stamen-toner')
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
presented in the subsections below.

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
GeoTiler allows to cache map tiles. The
:py:func:`geotiler.cache.caching_downloader` function enables us to adapt
any caching strategy.

Beside generic caching downloader adapter, GeoTiler provides `Redis store
<http://redis.io/>`_ adapter.  While it requires Redis server and Python
`Redis module <https://pypi.python.org/pypi/redis/>`_ installed, such
solution gives map tiles persistence and advanced cache management.

The Redis cache example illustrates how Redis can be user for map tiles
caching.

.. literalinclude:: ../examples/ex-redis-cache.py
   :lines: 32-58

.. vim: sw=4:et:ai
