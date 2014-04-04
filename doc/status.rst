Project Status
==============
The source code of GeoTiler is based on Python port of
`Modest Maps <https://github.com/stamen/modestmaps-py/>`_ project.

The GeoTiler project initial focus has been on

* library API improvements
* simplifying library design
* ensuring OpenStreetMap and Stamen map providers work
* reimplementing default map tiles caching to use LRU cache
* implementing Redis based map tiles cache
* moving docstrings tests to unit test modules
* Python 3 support
* making code PEP-8 compliant

You can help by

* testing map providers and reporting bugs
* providing more examples, i.e. how to integrate GeoTiler with various GUI
  toolkits
* implementing new caching strategies, i.e. memcached
* working on unit tests
* making code even more PEP-8 compliant

.. vim: sw=4:et:ai
