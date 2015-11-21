Introduction
============

Features
--------
GeoTiler features are

#. Very easy map API, which can be used in interactive and non-interactive
   way with other libraries, i.e. matplotlib, Cairo, Qt, etc.
#. Supported multiple map tiles providers, i.e. OpenStreetMap, Stamen and
   Blue Marble.
#. Asynchronous and synchronous map tiles downloader.
#. Map tiles caching with Redis and support for custom caching strategies.
#. The library design supports extensibility. Implement custom map tiles
   providers, tiles downloading or caching strategies within minutes.

Installation
------------
To install GeoTiler use `pip <http://www.pip-installer.org/>`_::

    pip install --user geotiler

Requirements

- `Pillow <https://pypi.python.org/pypi/Pillow/>`_ library
- Python 3.4 or later

Project Status
--------------
The source code of GeoTiler is based on Python port of
`Modest Maps <https://github.com/stamen/modestmaps-py/>`_ project.

The GeoTiler project initial focus has been on

* library API improvements
* simplifying library design
* user documentation
* ensuring OpenStreetMap, Stamen and Blue Marble map providers work
* reimplementing default map tiles caching to use LRU cache (and now we
  switched to no cache by default)
* implementing Redis based map tiles cache
* moving docstrings tests to unit test modules
* Python 3 support
* making code PEP-8 compliant

You can help by

* testing map providers and reporting bugs
* providing more examples, i.e. how to integrate GeoTiler with various GUI
  toolkits
* implementing new caching strategies, i.e.
  `memcached <http://www.tummy.com/software/python-memcached/>`_
  or `PyLRU <https://github.com/jlhutch/pylru>`_
* working on unit tests
* making code even more PEP-8 compliant

.. vim: sw=4:et:ai
