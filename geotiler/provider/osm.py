"""
>>> p = Provider()
>>> p.getTileUrls(Coordinate(10, 13, 7))
('http://tile.openstreetmap.org/7/13/10.png',)
>>> p.getTileUrls(Coordinate(13, 10, 7))
('http://tile.openstreetmap.org/7/10/13.png',)
"""

from math import pi

from ..Core import Coordinate
from ..Geo import MercatorProjection, deriveTransformation
from .base import IMapProvider
from .. import Tiles


class Base(IMapProvider):
    FMT_URL = None

    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def tileWidth(self):
        return 256

    def tileHeight(self):
        return 256

    def getTileUrls(self, coordinate):
        url = self.FMT_URL.format(
            x=coordinate.column,
            y=coordinate.row,
            z=coordinate.zoom
        )
        return (url,)



class Provider(Base):
    FMT_URL = 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'



class CycleProvider(Base):
    FMT_URL = 'http://tile.opencyclemap.org/cycle/{z}/{x}/{y}.png'



if __name__ == '__main__':
    import doctest
    doctest.testmod()
