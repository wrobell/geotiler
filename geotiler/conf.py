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

from . import Yahoo, Microsoft, BlueMarble, OpenStreetMap, CloudMade, \
    MapQuest, Stamen

# a handy list of possible providers, which isn't
# to say that you can't go writing your own.
builtinProviders = {
    'OPENSTREETMAP': OpenStreetMap.Provider,
    'OPEN_STREET_MAP': OpenStreetMap.Provider,
    'BLUE_MARBLE': BlueMarble.Provider,
    'MAPQUEST_ROAD': MapQuest.RoadProvider,
    'MAPQUEST_AERIAL': MapQuest.AerialProvider,
    'MICROSOFT_ROAD': Microsoft.RoadProvider,
    'MICROSOFT_AERIAL': Microsoft.AerialProvider,
    'MICROSOFT_HYBRID': Microsoft.HybridProvider,
    'YAHOO_ROAD': Yahoo.RoadProvider,
    'YAHOO_AERIAL': Yahoo.AerialProvider,
    'YAHOO_HYBRID': Yahoo.HybridProvider,
    'CLOUDMADE_ORIGINAL': CloudMade.OriginalProvider,
    'CLOUDMADE_FINELINE': CloudMade.FineLineProvider,
    'CLOUDMADE_TOURIST': CloudMade.TouristProvider,
    'CLOUDMADE_FRESH': CloudMade.FreshProvider,
    'CLOUDMADE_PALEDAWN': CloudMade.PaleDawnProvider,
    'CLOUDMADE_MIDNIGHTCOMMANDER': CloudMade.MidnightCommanderProvider,
    'STAMEN_TONER': Stamen.TonerProvider,
    'STAMEN_TERRAIN': Stamen.TerrainProvider,
    'STAMEN_WATERCOLOR': Stamen.WatercolorProvider,
}


default_provider = builtinProviders['OPENSTREETMAP']()

def find_provider(id):
    cls = builtinProviders[id]
    return cls()

# vim: sw=4:et:ai
