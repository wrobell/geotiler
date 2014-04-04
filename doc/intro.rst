Introduction
============
GeoTiler is a library to create maps using tiles from a map provider.

The main goal of the library is to enable a programmer to create maps
using tiles downloaded from a map provider like OpenStreetMap or Stamen.

The maps can be used by interactive applications or to create data analysis
graphs.

Features
--------
GeoTiler features are

# Non-complex map API, which can be easily integrated with other libraries,
  i.e. matplotlib, Cairo, etc.
# Implemented many map tiles providers support, i.e. OpenStreetMap and
  Stamen.
# Threaded map tiles downloader.
# Map tiles caching with LRU cache or Redis based cache.
# The library design supports extensibility. Implement custom map tiles
  providers, tiles downloading or caching strategies within minutes.

.. vim: sw=4:et:ai
