#
# GeoTiler - library to create maps using tiles from a map provider
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

from . import yahoo, ms, bluemarble, osm, cloudmade, mapquest, stamen

# a handy list of possible providers, which isn't
# to say that you can't go writing your own.
builtinProviders = {
    'OPENSTREETMAP': osm.Provider,
    'BLUE_MARBLE': bluemarble.Provider,
    'MAPQUEST_ROAD': mapquest.RoadProvider,
    'MAPQUEST_AERIAL': mapquest.AerialProvider,
    'MICROSOFT_ROAD': ms.RoadProvider,
    'MICROSOFT_AERIAL': ms.AerialProvider,
    'MICROSOFT_HYBRID': ms.HybridProvider,
    'YAHOO_ROAD': yahoo.RoadProvider,
    'YAHOO_AERIAL': yahoo.AerialProvider,
    'YAHOO_HYBRID': yahoo.HybridProvider,
    'CLOUDMADE_ORIGINAL': cloudmade.OriginalProvider,
    'CLOUDMADE_FINELINE': cloudmade.FineLineProvider,
    'CLOUDMADE_TOURIST': cloudmade.TouristProvider,
    'CLOUDMADE_FRESH': cloudmade.FreshProvider,
    'CLOUDMADE_PALEDAWN': cloudmade.PaleDawnProvider,
    'CLOUDMADE_MIDNIGHTCOMMANDER': cloudmade.MidnightCommanderProvider,
    'STAMEN_TONER': stamen.TonerProvider,
    'STAMEN_TERRAIN': stamen.TerrainProvider,
    'STAMEN_WATERCOLOR': stamen.WatercolorProvider,
}


default_provider = builtinProviders['OPENSTREETMAP']()

def find_provider(id):
    cls = builtinProviders[id]
    return cls()

# vim: sw=4:et:ai
