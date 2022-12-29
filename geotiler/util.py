#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2022 by Artur Wroblewski <wrobell@riseup.net>
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
GeoTiler utility functions.
"""

import re

RE_URL_OBFUSCATE = re.compile('(?<=apikey=)[a-z0-9-]+|(?<=api-key=)[a-z0-9-]+', re.I)

def obfuscate(url: str) -> str:
    """
    Replace API key in a tile URL with "<apikey>" string.

    :param url: Tile URL to obfuscate.
    """
    return RE_URL_OBFUSCATE.sub('<apikey>', url)

def log_tiles(print, tiles):
    tiles = (print(t) for t in tiles)
    return tiles

def div_ceil(n: int, m: int) -> int:
    """
    Calculate ceiling of `n` divided by `m`.
    """
    return (n + m - 1) // m

# vim: sw=4:et:ai
