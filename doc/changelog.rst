Changelog
=========
0.14.7
------
- do not use `a, b, c` subdomains for osm map provider as osm does not
  support them anymore

0.14.6
------
- add missing `pkg_resources` dependency to the build system metadata

0.14.5
------
- allow to pass map provider id or map provider data to a map constructor
- add tile width and height to the map provider data
- Python 3.8 is required

0.14.4
------
- raise error if a map provider requires API key and configuration file
  does not exist

0.14.3
------
- show provider map name when requesting its string representation; this
  also makes nicer string representation of map object

0.14.2
------
- python 3.7 is required since now
- keep center and extent of map unchanged when reseting zoom value to the
  same value
- remove some of the rounding of calculations to minimize calculation error

0.14.1
------
- fixed calculation of number of required tiles to render a map; this also
  improves performance of map rendering as less tiles is required

0.14.0
------
- corrected use of Redis API in Redis cache

0.13.0
------
- implemented function `geotiler.fetch_tiles` to allow processing of tiles
  before map rendering
- use map provider download limit to honour map provider service connection
  limits
- the :py:mod:`aiohttp` module is used again (with support for proxies)
- Python 3.6 is required

0.12.0
------
- there is no OSM cycle map anymore, just OpenCycleMap by Thunderforest;
  therefore the osm-cycle map provider is replaced with thunderforest-cycle
  one
- added support for map provider api keys

0.11.0
------
- added support for stamen-terrain-background and stamen-terrain-lines map
  providers

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
