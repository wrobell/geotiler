Changelog
=========
0.5.0
-----
- format of rendered map image is changed from RGB to RGBA
- implemented example Qt application to show map centered at current
  position read from GPS; it uses asyncio and `quamash` library

0.4.0
-----
- caching API has changed
- use asyncio to download map tiles
- implemented :py:func:`geotiler.render_map_async` function to download map
  asynchronously
- default LRU caching is gone

0.3.0
-----
- implemented stamen-toner-lite map provider
- fixed stamen terrain and watercolor providers, which were broken since
  stamen started to use tiles in jpeg format

0.2.0
-----
- improved error handling of map tiles downloading
- fixed geotiler-lint script installation issue
- documentation for geotiler-lint script added
- documented map tiles licensing information

0.1.0
-----
- initial release

.. vim: sw=4:et:ai
