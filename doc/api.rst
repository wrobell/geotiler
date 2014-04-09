API
===
Map Rendering
-------------
.. autosummary::

   geotiler.Map
   geotiler.render_map
   geotiler.find_provider

.. autoclass:: geotiler.Map
   :members:
   :special-members:

.. autofunction:: geotiler.render_map
.. autofunction:: geotiler.find_provider


Tile Management
---------------
.. autosummary::

   geotiler.tilenet.TileDownloader
   geotiler.tilenet.TileThreadDownloader
   geotiler.cache.redis.RedisCache


.. autoclass:: geotiler.tilenet.TileDownloader
   :members:

.. autoclass:: geotiler.tilenet.TileThreadDownloader
   :members:

.. autoclass:: geotiler.cache.redis.RedisCache
   :members:

.. vim: sw=4:et:ai
