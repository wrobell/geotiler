#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
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
GeoTiler map functionality.
"""

import itertools
import math
import logging

from .provider.conf import DEFAULT_PROVIDER
from . import core
from .geo import zoom_to
from .tilenet import render_tiles

logger = logging.getLogger(__name__)

class Map(object):
    """
    Map created from tiles and to be drawn as an image.

    The extent, zoom, center and image size can be changed at any time with
    appropriate properties.

    :var provider: Map tiles provider (default OpenStreetMap).
    :var _zoom: Map zoom attribute accessed via `zoom` property.
    :var _size: Map image size accessed via `size` property.
    :var origin: Center of base tile relative to map center.
    :var offset: Position of base tile relative to map center.
    """
    def __init__(
        self, extent=None, center=None, zoom=None, size=None,
        provider=DEFAULT_PROVIDER
    ):
        """
        Create map.

        One of the following parameters combination is required

        - center, zoom and size
        - extent and size
        - extent and zoom

        If none of above parameters combination is provided, then `ValueError`
        exception is raised.

        :param extent: Map geographical extent.
        :param center: Map geographical center.
        :param zoom: Map zoom.
        :param size: Map image size.
        :param provider: Map tiles provider.
        """
        super().__init__()
        self.provider = provider
        self.origin = None
        self.offset = None

        self._zoom = zoom
        self._size = size

        if center and extent:
            raise ValueError(
                'Bad map coverage, center and extent can\'t both be set'
            )
        elif extent and size and zoom:
            raise ValueError(
                'Bad map coverage, size and zoom can\'t be set together' \
                ' with extent'
            )
        elif center and zoom and size:
            self._change_center_zoom(center, zoom)
        elif extent and size:
            self._change_extent_and_zoom(extent)
        elif extent and zoom:
            self.extent = extent
        else:
            raise ValueError(
                'Unknown combination of extent, center, zoom and size' \
                ' parameters'
            )

        assert self._zoom is not None
        assert self._size is not None
        assert self.origin is not None
        assert self.offset is not None


    @property
    def extent(self):
        """
        Calculate map geographical extent.

        It is a tuple of 2 coordinates (longitude and latitude)

        - lower-bottom corner of the map
        - right-top corner of the map

        Setting map extent changes map image size.
        """
        w, h = self._size
        p1 = self.pointLocation((0, h))
        p2 = self.pointLocation((w, 0))
        return p1[0], p1[1], p2[0], p2[1]


    @extent.setter
    def extent(self, extent):
        p1 = extent[:2]
        p2 = extent[2:]

        projection = self.provider.projection
        c1 = projection.rev_geocode(p1)
        c1 = zoom_to(c1, projection.zoom, self._zoom)

        c2 = projection.rev_geocode(p2)
        c2 = zoom_to(c2, projection.zoom, self._zoom)

        width = abs(c1[0] - c2[0]) * self.provider.tile_width
        height = abs(c1[1] - c2[1]) * self.provider.tile_height

        col = (c1[0] + c2[0]) / 2
        row = (c1[1] + c2[1]) / 2
        center_origin = core.Coordinate(row, col, self._zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, center_origin)
        self.origin = map_origin
        self.offset = map_offset
        self._size = int(width), int(height)


    @property
    def center(self):
        """
        Calculate map geographical center.

        It is a tuple of two values - longitude and latitude.

        Setting map geographical center affects map geographical extent.
        """
        w, h = self._size
        return self.pointLocation((w / 2, h / 2))


    @center.setter
    def center(self, center):
        projection = self.provider.projection
        c = projection.rev_geocode(center)
        c = zoom_to(c, projection.zoom, self._zoom)
        center_origin = core.Coordinate(c[1], c[0], self._zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, center_origin)
        self.origin = map_origin
        self.offset = map_offset


    @property
    def zoom(self):
        """
        Map zoom value.

        Setting map value does *not* affect any other map properties like
        extent, center or image size.
        """
        return self._zoom


    @zoom.setter
    def zoom(self, zoom):
        c = self.origin
        c = zoom_to((c.column, c.row), c.zoom, zoom)
        center_origin = core.Coordinate(c[1], c[0], zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, center_origin)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = zoom


    @property
    def size(self):
        """
        Size of the image containing map.

        It is a tuple - width and height of the image.

        Setting size of the image affects map geographical extent.
        """
        return self._size


    @size.setter
    def size(self, size):
        self._size = size


    def _change_center_zoom(self, center, zoom):
        """
        Recalculate map to have new geographical center and update zoom
        value.

        :param center: Map geographical center.
        :param zoom: Map zoom value.
        """
        projection = self.provider.projection
        c = projection.rev_geocode(center)
        c = zoom_to(c, projection.zoom, zoom)
        center_origin = core.Coordinate(c[1], c[0], zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, center_origin)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = zoom


    def _change_extent_and_zoom(self, extent):
        """
        Recalculate map to have new geographical extent and calculate map
        zoom.

        :param extent: Map geographical extent.
        """
        width, height = self._size

        p1 = extent[:2]
        p2 = extent[2:]

        map_origin, map_offset = calculateMapExtent(self.provider, width, height, p1, p2)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = map_origin.zoom


    def __str__(self):
        return 'Map(%(provider)s, %(_size)s, %(coordinate)s, %(offset)s)' % self.__dict__


    def locationPoint(self, location):
        """ Return an x, y point on the map image for a given geographical location.
        """
        ox, oy = self.offset
        projection = self.provider.projection
        coord = projection.rev_geocode(location)
        coord = zoom_to(coord, projection.zoom, self.origin.zoom)

        # distance from the known coordinate offset
        x = ox + self.provider.tile_width * (coord[0] - self.origin.column)
        y = oy + self.provider.tile_height * (coord[1] - self.origin.row)

        # because of the center/corner business
        w, h = self.size
        return x + w / 2, y + h / 2


    def pointLocation(self, point):
        """ Return a geographical location on the map image for a given x, y point.
        """
        coord = self.origin
        hizoomCoord = zoom_to((coord.column, coord.row), coord.zoom, core.Coordinate.MAX_ZOOM)
        hizoomCoord = core.Coordinate(hizoomCoord[1], hizoomCoord[0], core.Coordinate.MAX_ZOOM)

        w, h = self._size

        # because of the center/corner business
        x, y = point[0] - w / 2, point[1] - h / 2

        # distance in tile widths from reference tile to point
        xtiles = (x - self.offset[0]) / self.provider.tile_width
        ytiles = (y - self.offset[1]) / self.provider.tile_height

        # distance in rows & columns at maximum zoom
        xDistance = xtiles * math.pow(2, (core.Coordinate.MAX_ZOOM - self.origin.zoom))
        yDistance = ytiles * math.pow(2, (core.Coordinate.MAX_ZOOM - self.origin.zoom))

        # new point coordinate reflecting that distance
        x = round(hizoomCoord.column + xDistance)
        y = round(hizoomCoord.row + yDistance)
        coord = zoom_to((x, y), hizoomCoord.zoom, self.origin.zoom)

        projection = self.provider.projection
        location = projection.geocode(coord, self.origin.zoom)

        return location



def render_map(map, downloader=None):
    """
    Render map image.

    If `downloader` is null, then default map tiles downloader is used.

    The function returns an image (instance of PIL.Image class).

    :param map: Map instance.
    :param downloader: Map tiles downloader.
    """
    coord, corner = _find_top_left_tile(map)
    tiles = _find_tiles(map, coord, corner)
    img = render_tiles(map.provider, tiles, map.size, downloader=downloader)
    return img


def _find_tiles(map, tile_coord, corner):
    """
    Calculate all map tiles required to render a map.

    For each tile a tuple of two items is created

    - tile coordinates
    - position of a tile within map image

    :param map: Map instance.
    :param tile_coord: Top-left map tile coordinate.
    :param corner: Top-left map tile position on map image.
    """
    tiles = []

    w, h = map.size
    cols = range(corner[0], w, map.provider.tile_width)
    rows = range(corner[1], h, map.provider.tile_height)

    # go by rows
    positions = itertools.product(enumerate(rows), enumerate(cols))
    for (i, y), (j, x) in positions:
        coord = core.Coordinate(tile_coord.row + i, tile_coord.column + j, tile_coord.zoom)
        tiles.append((coord, (x, y)))

    return tiles


def _find_top_left_tile(map):
    """
    Find coordinate of top-left tile of the map.

    The function calculate the tile coordinate and its position relative to
    top-left corner of the map image.

    :param map: Map instance.
    """
    coord = map.origin
    w, h = map.size
    tw = map.provider.tile_width
    th = map.provider.tile_height

    px = map.offset[0] + w // 2
    py = map.offset[1] + h // 2

    dx = px // tw + (px % tw > 0)
    dy = py // th + (py % th > 0)

    px -= dx * tw
    py -= dy * th

    coord = core.Coordinate(coord.row - dy, coord.column - dx, coord.zoom)

    # if corner position not in ((-tw, -th), (0, 0)], then map image does
    # not contain the map properly
    assert -tw < px <= 0 and -th < py <= 0, (px, py)

    return coord, (px, py)


def calculateMapCenter(provider, centerCoord):
    """ Based on a provider and center coordinate, returns the coordinate
        of an initial tile and its point placement, relative to the map center.
    """
    # initial tile coordinate
    initTileCoord = centerCoord.container()

    # initial tile position, assuming centered tile well in grid
    initX = (initTileCoord.column - centerCoord.column) * provider.tile_width
    initY = (initTileCoord.row - centerCoord.row) * provider.tile_height
    initPoint = round(initX), round(initY)

    return initTileCoord, initPoint

def calculateMapExtent(provider, width, height, *args):
    """ Based on a provider, width & height values, and a list of locations,
        returns the coordinate of an initial tile and its point placement,
        relative to the map center.
    """
    projection = provider.projection
    coordinates = [projection.rev_geocode(p) for p in args]

    TL = core.Coordinate(min([c[1] for c in coordinates]),
                         min([c[0] for c in coordinates]),
                         projection.zoom)

    BR = core.Coordinate(max([c[1] for c in coordinates]),
                         max([c[0] for c in coordinates]),
                         projection.zoom)

    # multiplication factor between horizontal span and map width
    hFactor = (BR.column - TL.column) / (float(width) / provider.tile_width)

    # multiplication factor expressed as base-2 logarithm, for zoom difference
    hZoomDiff = math.log(hFactor) / math.log(2)

    # possible horizontal zoom to fit geographical extent in map width
    hPossibleZoom = TL.zoom - math.ceil(hZoomDiff)

    # multiplication factor between vertical span and map height
    vFactor = (BR.row - TL.row) / (float(height) / provider.tile_height)

    # multiplication factor expressed as base-2 logarithm, for zoom difference
    vZoomDiff = math.log(vFactor) / math.log(2)

    # possible vertical zoom to fit geographical extent in map height
    vPossibleZoom = TL.zoom - math.ceil(vZoomDiff)

    # initial zoom to fit extent vertically and horizontally
    initZoom = min(hPossibleZoom, vPossibleZoom)

    ## additionally, make sure it's not outside the boundaries set by provider limits
    #initZoom = min(initZoom, provider.outerLimits()[1].zoom)
    #initZoom = max(initZoom, provider.outerLimits()[0].zoom)

    # coordinate of extent center
    centerRow = (TL.row + BR.row) / 2
    centerColumn = (TL.column + BR.column) / 2
    centerZoom = (TL.zoom + BR.zoom) / 2

    coord = zoom_to((centerColumn, centerRow), centerZoom, initZoom)
    coord = core.Coordinate(coord[1], coord[0], initZoom)

    return calculateMapCenter(provider, coord)


# vim: sw=4:et:ai
