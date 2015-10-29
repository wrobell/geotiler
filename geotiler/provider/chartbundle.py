from math import pi

from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider


URL_FMT = 'http://wms.chartbundle.com/tms/v1.0/{style}/{{zoom}}/{{col}}/{{row}}.{ext}?type=google'


class BaseProvider(IMapProvider):
    def __init__(self, style, ext='png'):
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

        self.url_fmt = URL_FMT.format(style=style, ext=ext)

    def get_tile_urls(self, tile_coord, zoom):
        col, row = tile_coord
        return (self.url_fmt.format(zoom=zoom, col=col, row=row),)


class TerminalArea(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'tac', 'png')


class Sectional(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'sec', 'png')


class USWorld(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'wac', 'png')


class EnrouteLow(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'enrl', 'png')


class EnrouteHigh(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'enrh', 'png')


class EnrouteArea(BaseProvider):
    def __init__(self):
        BaseProvider.__init__(self, 'enra', 'png')
