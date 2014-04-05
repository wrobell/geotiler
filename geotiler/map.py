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

import math
import logging

from shapely.geometry import Point
import PIL.Image as Image

from .provider.conf import DEFAULT_PROVIDER
from . import core
from .tilenet import TileRequest, render_tiles

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
        p1 = self.pointLocation(Point(0, h))
        p2 = self.pointLocation(Point(w, 0))
        return p1.x, p1.y, p2.x, p2.y


    @extent.setter
    def extent(self, extent):
        p1 = Point(*extent[:2])
        p2 = Point(*extent[2:])

        c1 = self.provider.locationCoordinate(p1).zoomTo(self._zoom)
        c2 = self.provider.locationCoordinate(p2).zoomTo(self._zoom)

        width = abs(c1.column - c2.column) * self.provider.tile_width
        height = abs(c1.row - c2.row) * self.provider.tile_height

        row = (c1.row + c2.row) / 2
        col = (c1.column + c2.column) / 2
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
        pt = self.pointLocation(Point(w / 2, h / 2))
        return pt.x, pt.y


    @center.setter
    def center(self, center):
        p = Point(*center)
        center_origin = self.provider.locationCoordinate(p).zoomTo(self._zoom)
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
        center_origin = self.origin.zoomTo(zoom)
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
        p = Point(*center)
        center_origin = self.provider.locationCoordinate(p).zoomTo(zoom)
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

        p1 = Point(*extent[:2])
        p2 = Point(*extent[2:])

        map_origin, map_offset = calculateMapExtent(self.provider, width, height, p1, p2)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = map_origin.zoom


    def __str__(self):
        return 'Map(%(provider)s, %(_size)s, %(coordinate)s, %(offset)s)' % self.__dict__


    def locationPoint(self, location):
        """ Return an x, y point on the map image for a given geographical location.
        """
        point = Point(self.offset.x, self.offset.y)
        coord = self.provider.locationCoordinate(location).zoomTo(self.origin.zoom)

        # distance from the known coordinate offset
        point = Point(
            point.x + self.provider.tile_width * (coord.column - self.origin.column),
            point.y + self.provider.tile_height * (coord.row - self.origin.row)
        )

        # because of the center/corner business
        w, h = self._size
        point = Point(point.x + w / 2, point.y + h / 2)

        return point


    def pointLocation(self, point):
        """ Return a geographical location on the map image for a given x, y point.
        """
        hizoomCoord = self.origin.zoomTo(core.Coordinate.MAX_ZOOM)

        w, h = self._size

        # because of the center/corner business
        point = Point(point.x - w / 2, point.y - h / 2)

        # distance in tile widths from reference tile to point
        xtiles = (point.x - self.offset.x) / self.provider.tile_width
        ytiles = (point.y - self.offset.y) / self.provider.tile_height

        # distance in rows & columns at maximum zoom
        xDistance = xtiles * math.pow(2, (core.Coordinate.MAX_ZOOM - self.origin.zoom))
        yDistance = ytiles * math.pow(2, (core.Coordinate.MAX_ZOOM - self.origin.zoom))

        # new point coordinate reflecting that distance
        coord = core.Coordinate(round(hizoomCoord.row + yDistance),
                                round(hizoomCoord.column + xDistance),
                                hizoomCoord.zoom)

        coord = coord.zoomTo(self.origin.zoom)

        location = self.provider.coordinateLocation(coord)

        return location



def render_map(map, downloader=None):
    """
    Render map image.

    If `downloader` is null, then default map tiles downloader is used.

    The function returns an image (instance of PIL.Image class).

    :param map: Map instance.
    :param downloader: Map tiles downloader.
    """
    coord = map.origin.copy()
    w, h = map._size
    corner = Point(int(map.offset.x + w / 2), int(map.offset.y + h / 2))

    while corner.x > 0:
        corner = Point(corner.x - map.provider.tile_width, corner.y)
        coord = coord.left()

    while corner.y > 0:
        corner = Point(corner.x, corner.y - map.provider.tile_height)
        coord = coord.up()

    tiles = []

    rowCoord = coord.copy()
    for y in range(int(corner.y), h, map.provider.tile_height):
        tileCoord = rowCoord.copy()
        for x in range(int(corner.x), w, map.provider.tile_width):
            tiles.append(TileRequest(map.provider, tileCoord, Point(x, y)))
            tileCoord = tileCoord.right()
        rowCoord = rowCoord.down()

    return render_tiles(tiles, map._size, downloader=downloader)


def calculateMapCenter(provider, centerCoord):
    """ Based on a provider and center coordinate, returns the coordinate
        of an initial tile and its point placement, relative to the map center.
    """
    # initial tile coordinate
    initTileCoord = centerCoord.container()

    # initial tile position, assuming centered tile well in grid
    initX = (initTileCoord.column - centerCoord.column) * provider.tile_width
    initY = (initTileCoord.row - centerCoord.row) * provider.tile_height
    initPoint = Point(round(initX), round(initY))

    return initTileCoord, initPoint

def calculateMapExtent(provider, width, height, *args):
    """ Based on a provider, width & height values, and a list of locations,
        returns the coordinate of an initial tile and its point placement,
        relative to the map center.
    """
    coordinates = list(map(provider.locationCoordinate, args))

    TL = core.Coordinate(min([c.row for c in coordinates]),
                         min([c.column for c in coordinates]),
                         min([c.zoom for c in coordinates]))

    BR = core.Coordinate(max([c.row for c in coordinates]),
                         max([c.column for c in coordinates]),
                         max([c.zoom for c in coordinates]))

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
    centerCoord = core.Coordinate(centerRow, centerColumn, centerZoom).zoomTo(initZoom)

    return calculateMapCenter(provider, centerCoord)


# vim: sw=4:et:ai
