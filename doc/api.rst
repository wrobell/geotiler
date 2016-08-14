API
===
Map Rendering
-------------
.. autosummary::

   geotiler.Map
   geotiler.render_map
   geotiler.render_map_async
   geotiler.providers
   geotiler.find_provider

.. autoclass:: geotiler.Map
   :members:
   :special-members:

.. autofunction:: geotiler.render_map
.. autofunction:: geotiler.render_map_async
.. autofunction:: geotiler.providers
.. autofunction:: geotiler.find_provider


Tile Downloading and Caching
----------------------------
.. autosummary::

   geotiler.cache.caching_downloader
   geotiler.cache.redis_downloader
   geotiler.tile.io.fetch_tiles

.. autofunction:: geotiler.cache.caching_downloader
.. autofunction:: geotiler.cache.redis_downloader
.. autofunction:: geotiler.tile.io.fetch_tiles

.. vim: sw=4:et:ai
