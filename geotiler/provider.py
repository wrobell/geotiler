#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

"""
Load and create map providers.
"""

import glob
import itertools
import json
import logging
import os.path

from math import pi
from .geo import MercatorProjection, deriveTransformation

logger = logging.getLogger(__name__)

DEFAULT_PROVIDER = 'osm'

# the attributes inspired by poor-maps project tile source definition
# https://github.com/otsaloma/poor-maps/tree/master/tilesources
ATTRIBUTES = 'id', 'name', 'attribution', 'url', 'subdomains', 'extension', \
    'limit'

class MapProvider:
    def __init__(self, data):
        self.id = None
        self.name = None
        self.attribution = None
        self.url = None
        self.subdomains = tuple()
        self.extension = 'png'
        self.limit = 1

        attrs = ((n, data[n]) for n in ATTRIBUTES if n in data)
        self.__dict__.update(attrs)

        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)
        if self.subdomains:
            self.subdomain_cycler = itertools.cycle(self.subdomains)
        else:
            self.subdomain_cycler = itertools.cycle(('', ))

    @property
    def tile_width(self):
        return 256

    @property
    def tile_height(self):
        return 256

    def tile_url(self, tile_coord, zoom):
        params = {
            'subdomain': next(self.subdomain_cycler),
            'x': tile_coord[0],
            'y': tile_coord[1],
            'z': zoom,
            'ext': self.extension,
        }
        url = self.url.format(**params)
        if __debug__:
            logger.debug('tile url: {}'.format(url))
        return url


def providers():
    """
    Get sorted list of all map providers identificators.
    """
    path = os.path.join(base_dir(), '*.json')
    if __debug__:
        logger.debug('list map providers from {}'.format(path))
    pid = lambda fn: os.path.splitext(os.path.basename(fn))[0]
    return sorted(pid(fn) for fn in glob.iglob(path))

def find_provider(id):
    """
    Load map provider data from JSON file and create map provider.

    :param id: Map provider identificator.
    """
    fn = os.path.join(base_dir(), id + '.json')
    if __debug__:
        logger.debug('loading map provider "{}" from {}'.format(id, fn))
    with open(fn, encoding='utf8') as f:
        data = json.load(f)
        provider = MapProvider(data)
        return provider

def base_dir():
    """
    Get map provider data base directory.
    """
    mod = __import__('geotiler')
    return os.path.join(mod.__path__[0], 'source')

# vim:et sts=4 sw=4:
