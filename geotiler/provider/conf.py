#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@pld-linux.org>
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
List of builtin map tiles providers.
"""

from . import yahoo, ms, bluemarble, osm, cloudmade, mapquest, stamen, chartbundle

PROVIDERS = {
    'osm': osm.Provider,
    'osm-cycle': osm.CycleProvider,
    'bluemarble': bluemarble.Provider,
    'mapquest-road': mapquest.RoadProvider,
    'mapquest-aerial': mapquest.AerialProvider,
    'ms-road': ms.RoadProvider,
    'ms-aerial': ms.AerialProvider,
    'ms-hybrid': ms.HybridProvider,
    'yahoo-road': yahoo.RoadProvider,
    'yahoo-aerial': yahoo.AerialProvider,
    'yahoo-hybrid': yahoo.HybridProvider,
    'cloudmade-original': cloudmade.OriginalProvider,
    'cloudmade-fineline': cloudmade.FineLineProvider,
    'cloudmade-tourist': cloudmade.TouristProvider,
    'cloudmade-fresh': cloudmade.FreshProvider,
    'cloudmade-paledawn': cloudmade.PaleDawnProvider,
    'cloudmade-midnightcommander': cloudmade.MidnightCommanderProvider,
    'stamen-toner': stamen.TonerProvider,
    'stamen-toner-lite': stamen.TonerLiteProvider,
    'stamen-terrain': stamen.TerrainProvider,
    'stamen-watercolor': stamen.WatercolorProvider,
    'chartbundle-tac': chartbundle.TerminalArea,
    'chartbundle-sec': chartbundle.Sectional,
    'chartbundle-wac': chartbundle.USWorld,
    'chartbundle-enrl': chartbundle.EnrouteLow,
    'chartbundle-enrh': chartbundle.EnrouteHigh,
    'chartbundle-enra': chartbundle.EnrouteArea,
}

DEFAULT_PROVIDER = PROVIDERS['osm']()


def find_provider(key):
    """
    Find map tiles provider.

    The function returns instance of a map provider.

    :param key: Map provider string id.
    """
    cls = PROVIDERS[key]
    return cls()


# vim: sw=4:et:ai
