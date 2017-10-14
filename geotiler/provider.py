#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2017 by Artur Wroblewski <wrobell@riseup.net>
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

import configparser
import glob
import itertools
import json
import logging
import os.path
import re

from math import pi
from .geo import MercatorProjection, deriveTransformation
from .errors import GeoTilerError

logger = logging.getLogger(__name__)

DEFAULT_PROVIDER = 'osm'
RE_URL_OBFUSCATE = re.compile('(?<=apikey=)[a-z0-9-]+|(?<=api-key=)[a-z0-9-]+', re.I)

# the attributes inspired by poor-maps project tile source definition
# https://github.com/otsaloma/poor-maps/tree/master/tilesources
ATTRIBUTES = 'id', 'name', 'attribution', 'url', 'subdomains', 'extension', \
    'limit', 'api-key-ref'

class MapProvider:
    def __init__(self, data, api_key=None):
        self.id = None
        self.name = None
        self.attribution = None
        self.url = None
        self.subdomains = tuple()
        self.extension = 'png'
        self.limit = 1
        self.api_key_ref = None
        self.api_key = api_key

        # change a-b-c to a_b_c to allow python attribute access
        norm = lambda n: n.replace('-', '_')
        attrs = ((norm(n), data[n]) for n in ATTRIBUTES if n in data)
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
            'api_key': self.api_key,
        }
        url = self.url.format(**params)
        if __debug__:
            logger.debug('tile url: {}'.format(obfuscate(url)))
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
    cp = read_config()
    data = read_provider_data(id)

    api_key_ref = data.get('api-key-ref')
    api_key = None
    if api_key_ref:
        # no api key for the api key reference, then raise fatal error; no
        # api key means no access
        if not cp.has_option('api-key', api_key_ref):
            raise GeoTilerError('No API key for for reference "{}"'.format(api_key_ref))

        api_key = cp.get('api-key', api_key_ref)

    if __debug__:
        logger.debug('map provider "{}" api key reference: {}'.format(
            id, api_key_ref
        ))

    provider = MapProvider(data, api_key=api_key)
    return provider

def base_dir():
    """
    Get map provider data base directory.
    """
    mod = __import__('geotiler')
    return os.path.join(mod.__path__[0], 'source')

def read_config():
    """
    Read GeoTiler configuration file.
    """
    p = os.getenv('HOME', '')
    fn = os.path.join(p, '.config/geotiler/geotiler.ini')
    cp = configparser.ConfigParser()
    if os.path.exists(fn):
        cp.read(fn)
    else:
        logger.warning('configuration file {} does not exist'.format(fn))
    return cp

def read_provider_data(id):
    """
    Read map provider data.

    :param id: Map provider identificator.
    """
    fn = os.path.join(base_dir(), id + '.json')
    if __debug__:
        logger.debug('loading map provider "{}" from {}'.format(id, fn))

    with open(fn, encoding='utf8') as f:
        data = json.load(f)

    return data

def obfuscate(url):
    """
    Replace API key in a tile URL with "<apikey>" string.

    :param url: Tile URL to obfuscate.
    """
    return RE_URL_OBFUSCATE.sub('<apikey>', url)

# vim:et sts=4 sw=4:
