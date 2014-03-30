"""
>>> m = Map(Microsoft.RoadProvider(), Point(600, 600), Core.Coordinate(3165, 1313, 13), Point(-144, -94))
>>> p = m.locationPoint(Point(37.804274, -122.262940))
>>> p
(370.724, 342.549)
>>> m.pointLocation(p)
(37.804, -122.263)

>>> c = Point(37.804274, -122.262940)
>>> z = 12
>>> d = Point(800, 600)
>>> m = mapByCenterZoom(Microsoft.RoadProvider(), c, z, d)
>>> m.dimensions
(800.000, 600.000)
>>> m.coordinate
(1582.000, 656.000 @12.000)
>>> m.offset
(-235.000, -196.000)

>>> sw = Point(36.893326, -123.533554)
>>> ne = Point(38.864246, -121.208153)
>>> d = Point(800, 600)
>>> m = mapByExtent(Microsoft.RoadProvider(), sw, ne, d)
>>> m.dimensions
(800.000, 600.000)
>>> m.coordinate
(98.000, 40.000 @8.000)
>>> m.offset
(-251.000, -218.000)

>>> se = Point(36.893326, -121.208153)
>>> nw = Point(38.864246, -123.533554)
>>> d = Point(1600, 1200)
>>> m = mapByExtent(Microsoft.RoadProvider(), se, nw, d)
>>> m.dimensions
(1600.000, 1200.000)
>>> m.coordinate
(197.000, 81.000 @9.000)
>>> m.offset
(-246.000, -179.000)

>>> sw = Point(36.893326, -123.533554)
>>> ne = Point(38.864246, -121.208153)
>>> z = 10
>>> m = mapByExtentZoom(Microsoft.RoadProvider(), sw, ne, z)
>>> m.dimensions
(1693.000, 1818.000)
>>> m.coordinate
(395.000, 163.000 @10.000)
>>> m.offset
(-236.000, -102.000)

>>> se = Point(36.893326, -121.208153)
>>> nw = Point(38.864246, -123.533554)
>>> z = 9
>>> m = mapByExtentZoom(Microsoft.RoadProvider(), se, nw, z)
>>> m.dimensions
(846.000, 909.000)
>>> m.coordinate
(197.000, 81.000 @9.000)
>>> m.offset
(-246.000, -179.000)
"""

__version__ = 'N.N.N'

from .map import Map
from .conf import find_provider

# vim: sw=4:et:ai
