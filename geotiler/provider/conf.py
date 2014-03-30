#
# geoTiler - library to create maps using tiles from a map provider
#
# NOTE: The code contains BSD licensed code from Modest Maps project.
#
# Copyright (C) 2013-2014 by Artur Wroblewski <wrobell@pld-linux.org>
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

"""
List of builtin map tiles providers.
"""

from . import yahoo, ms, bluemarble, osm, cloudmade, mapquest, stamen

PROVIDERS = {
    'osm': osm.Provider,
    'osm-cycle': osm.CycleProvider,
    'bluemarble': bluemarble.Provider,
    'mapquest_road': mapquest.RoadProvider,
    'mapquest_aerial': mapquest.AerialProvider,
    'ms_road': ms.RoadProvider,
    'ms_aerial': ms.AerialProvider,
    'ms_hybrid': ms.HybridProvider,
    'yahoo_road': yahoo.RoadProvider,
    'yahoo_aerial': yahoo.AerialProvider,
    'yahoo_hybrid': yahoo.HybridProvider,
    'cloudmade_original': cloudmade.OriginalProvider,
    'cloudmade_fineline': cloudmade.FineLineProvider,
    'cloudmade_tourist': cloudmade.TouristProvider,
    'cloudmade_fresh': cloudmade.FreshProvider,
    'cloudmade_paledawn': cloudmade.PaleDawnProvider,
    'cloudmade_midnightcommander': cloudmade.MidnightCommanderProvider,
    'stamen_toner': stamen.TonerProvider,
    'stamen_terrain': stamen.TerrainProvider,
    'stamen_watercolor': stamen.WatercolorProvider,
}

DEFAULT_PROVIDER = PROVIDERS['osm']()


def find_provider(key):
    """
    Find map tiles provider.

    :param key: Map provider string id.
    """
    cls = PROVIDERS[key]
    return cls()


# vim: sw=4:et:ai
