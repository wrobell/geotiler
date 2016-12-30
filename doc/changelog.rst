Changelog
=========
0.10.0
------
- added type check for map image size, which is a sequence of two integer
  values
- read map configuration files using Unicode encoding

0.9.0
-----
- replace Python based map providers configuration with JSON file
  configuration (inspired by `poor-maps` project tile source definition
  https://github.com/otsaloma/poor-maps/tree/master/tilesources)
- `geotiler-lint` map provider argument is optional now
- `geotiler.Map` class constructor parameter for provider is changed to be
  string instead of map provider instance
- added caching example using `shelve` Python module (thanks to `matthijs876`)

0.8.0
-----
- implemented `geotiler-fetch` script to cache map tiles upfront
- implemented `geotiler-route` script to draw GPX track on a map
- OpenCV example added, thanks to `matthijs876`

0.7.0
-----
- use :py:mod:`urllib` Python standard library to fetch map tiles, which
  allows us to support proxies; :py:mod:`aiohttp` is no longer used
- implemented ChartBundle map providers

0.6.0
-----
- map rendering performance improved
- Qt application example simplified and its performance improved

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
