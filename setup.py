#!/usr/bin/env python

from distutils.core import setup

import geotiler

version = geotiler.__version__

setup(
    name='GeoTiler',
    version=version,
    description='GeoTiler',
    requires=['PIL'],
    packages=['geotiler'],
    license='GPL'
)

# vim: sw=4:et:ai
