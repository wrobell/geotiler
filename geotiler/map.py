#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2016 by Artur Wroblewski <wrobell@riseup.net>
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

import asyncio
import itertools
import math
import numbers
import logging

from .provider import DEFAULT_PROVIDER, find_provider
from .geo import zoom_to
from .tile.io import fetch_tiles
from .tile.img import render_image

logger = logging.getLogger(__name__)

MAX_ZOOM = 25

class Map:
    """
    Map created from tiles and to be drawn as an image.

    The extent, zoom, center and image size can be changed at any time with
    appropriate properties.

    :var provider: Map tiles provider identificator (default `osm`).
    :var _zoom: Map zoom attribute accessed via `zoom` property.
    :var _size: Map image size accessed via `size` property.
    :var origin: Tile coordinates at map zoom level of base tile.
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

        self._check_size(size)

        self.provider = find_provider(provider)
        self.origin = None
        self.offset = None

        self._zoom = zoom
        self._size = size

        if center is not None and extent is not None:
            raise ValueError(
                'Bad map coverage, center and extent can\'t both be set'
            )
        elif extent is not None and size is not None and zoom is not None:
            raise ValueError(
                'Bad map coverage, size and zoom can\'t be set together' \
                ' with extent'
            )
        elif center is not None and zoom is not None and size is not None:
            self._change_center_zoom(center, zoom)
        elif extent is not None and size is not None:
            self._change_extent_and_zoom(extent)
        elif extent is not None and zoom is not None:
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

        if __debug__:
            logger.debug(
                'extent={map.extent}, center={map.center}, zoom={map.zoom},'
                ' size={map.size}, origin={map.origin}, offset={map.offset}'
                .format(map=self)
            )


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
        p1 = self.geocode((0, h))
        p2 = self.geocode((w, 0))
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

        map_origin, map_offset = calculateMapCenter(self.provider, (col, row))
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
        return self.geocode((w / 2, h / 2))


    @center.setter
    def center(self, center):
        projection = self.provider.projection
        c = projection.rev_geocode(center)
        c = zoom_to(c, projection.zoom, self._zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, c)
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
        c = zoom_to(self.origin, self._zoom, zoom)

        map_origin, map_offset = calculateMapCenter(self.provider, c)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = zoom


    @property
    def size(self):
        """
        Size of the image containing map.

        It is a sequence of two integer values - width and height of the
        image.

        Setting size of the image affects map geographical extent.
        """
        return self._size


    @size.setter
    def size(self, size):
        self._check_size(size)
        self._size = size

    def _check_size(self, size):
        """
        Check if `size` parameter has correct type.
        """
        valid = size is None \
            or len(size) == 2 \
            and all(isinstance(v, numbers.Integral) for v in tuple(size))
        if not valid:
            raise TypeError('Size should be sequence of two integer values')

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

        map_origin, map_offset = calculateMapCenter(self.provider, c)
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

        map_origin, map_offset, zoom = calculateMapExtent(self.provider, width, height, p1, p2)
        self.origin = map_origin
        self.offset = map_offset
        self._zoom = zoom


    def __str__(self):
        return 'Map({provider}, {_size}, {origin}, {offset})'.format(**self.__dict__)


    def rev_geocode(self, location):
        """
        Reverse geocode geographical location.

        The method calculates location position (x, y) on map image.

        :param location: Geographical location (longitude, latitude).
        """
        ox, oy = self.offset
        projection = self.provider.projection
        coord = projection.rev_geocode(location)
        coord = zoom_to(coord, projection.zoom, self._zoom)

        # distance from the known coordinate offset
        x = ox + self.provider.tile_width * (coord[0] - self.origin[0])
        y = oy + self.provider.tile_height * (coord[1] - self.origin[1])

        # because of the center/corner business
        w, h = self.size
        return x + w / 2, y + h / 2


    def geocode(self, point):
        """
        Geocode map image point.

        The method calculates geographical location (longitude, latitude)
        of image point.

        :param point: Image map point (x, y).
        """
        max_zoom = MAX_ZOOM
        max_coord = zoom_to(self.origin, self._zoom, max_zoom)

        w, h = self._size

        # because of the center/corner business
        x, y = point[0] - w / 2, point[1] - h / 2

        # distance in tile widths from reference tile to point
        xtiles = (x - self.offset[0]) / self.provider.tile_width
        ytiles = (y - self.offset[1]) / self.provider.tile_height

        # distance in rows & columns at maximum zoom
        xDistance = xtiles * math.pow(2, (MAX_ZOOM - self._zoom))
        yDistance = ytiles * math.pow(2, (MAX_ZOOM - self._zoom))

        # new point coordinate reflecting that distance
        x = round(max_coord[0] + xDistance)
        y = round(max_coord[1] + yDistance)
        coord = zoom_to((x, y), max_zoom, self._zoom)

        projection = self.provider.projection
        location = projection.geocode(coord, self._zoom)

        return location


def render_map(map, downloader=None, loop=None, **kw):
    """
    Download map tiles and render map image.

    If `downloader` is null, then default map tiles downloader is used
    (:py:func:`geotiler.tile.io.fetch_tiles`).

    The function returns an image (instance of `PIL.Image` class).

    :param map: Map instance.
    :param downloader: Map tiles downloader.
    :param loop: Asyncio loop (used default one if `None`).
    :param kw: Parameters passed to default downloader.
    """
    task = render_map_async(map, downloader=downloader, loop=loop, **kw)
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_until_complete(task)


@asyncio.coroutine
def render_map_async(map, downloader=None, loop=None, **kw):
    """
    Asyncio coroutine to download map tiles asynchronously and render map
    image.

    If `downloader` is null, then default map tiles downloader is used
    (:py:func:`geotiler.tile.io.fetch_tiles`).

    The function returns an image (instance of `PIL.Image` class).

    :param map: Map instance.
    :param downloader: Map tiles downloader.
    :param loop: Asyncio loop (used default one if `None`).
    :param kw: Parameters passed to default downloader.
    """
    if downloader is None:
        downloader = fetch_tiles

    tile_url = map.provider.tile_url

    # NOTE: consider having origin tile at top-left tile instead of the
    # center, then we could skip this step
    coord, offset = _find_top_left_tile(map)

    coords = _tile_coords(map, coord, offset)
    urls = tuple(tile_url(c, map.zoom) for c in coords)
    tile_data = yield from downloader(urls, **kw)

    offsets = _tile_offsets(map, offset)
    return render_image(map, tile_data, offsets)


def _tile_coords(map, coord, offset):
    """
    Create grid of coordinates of map tiles.

    :param map: Geotiler map instance.
    :param coord: Coordinate of top-left tile.
    :param offset: Map image offset of top-left tile.
    """
    w, h = map.size

    n = (w - offset[0]) // map.provider.tile_width + 1
    m = (h - offset[1]) // map.provider.tile_height + 1
    cols = range(coord[0], coord[0] + n)
    rows = range(coord[1], coord[1] + m)
    return itertools.product(cols, rows)


def _tile_offsets(map, offset):
    """
    Create grid of offsets of map tiles.

    :param map: Geotiler map instance.
    :param offset: Map image offset of top-left tile.
    """
    w, h = map.size
    cols = range(offset[0], w, map.provider.tile_width)
    rows = range(offset[1], h, map.provider.tile_height)
    return itertools.product(cols, rows)


def _find_top_left_tile(map):
    """
    Calculate the tile coordinate and its position relative to top-left
    offset of the map image.

    :param map: Map instance.
    """
    origin = map.origin
    w, h = map.size
    tw = map.provider.tile_width
    th = map.provider.tile_height

    px = map.offset[0] + w // 2
    py = map.offset[1] + h // 2

    dx = px // tw + (px % tw > 0)
    dy = py // th + (py % th > 0)

    px -= dx * tw
    py -= dy * th
    offset = px, py

    coord = origin[0] - dx, origin[1] - dy

    # if offset position not in ((-tw, -th), (0, 0)], then map image does
    # not contain the map properly
    assert -tw < offset[0] <= 0 and -th < offset[1] <= 0, offset

    return coord, offset


def calculateMapCenter(provider, tile_coord):
    """ Based on a provider and center coordinate, returns the coordinate
        of an initial tile and its point placement, relative to the map center.
    """
    # initial tile coordinate
    initTileCoord = math.floor(tile_coord[0]), math.floor(tile_coord[1])

    # initial tile position, assuming centered tile well in grid
    initX = (initTileCoord[0] - tile_coord[0]) * provider.tile_width
    initY = (initTileCoord[1] - tile_coord[1]) * provider.tile_height
    initPoint = round(initX), round(initY)

    return initTileCoord, initPoint

def calculateMapExtent(provider, width, height, *args):
    """ Based on a provider, width & height values, and a list of locations,
        returns the coordinate of an initial tile and its point placement,
        relative to the map center.
    """
    projection = provider.projection
    coordinates = [projection.rev_geocode(p) for p in args]

    TL = min(c[0] for c in coordinates), min(c[1] for c in coordinates)
    BR = max(c[0] for c in coordinates), max(c[1] for c in coordinates)

    # multiplication factor between horizontal span and map width
    hFactor = round((BR[0] - TL[0]) / (width / provider.tile_width), 16)

    # multiplication factor expressed as base-2 logarithm, for zoom difference
    hZoomDiff = math.log(hFactor) / math.log(2)

    # possible horizontal zoom to fit geographical extent in map width
    hPossibleZoom = projection.zoom - math.ceil(hZoomDiff)

    # multiplication factor between vertical span and map height
    vFactor = round((BR[1] - TL[1]) / (height / provider.tile_height), 16)

    # multiplication factor expressed as base-2 logarithm, for zoom difference
    vZoomDiff = math.log(vFactor) / math.log(2)

    # possible vertical zoom to fit geographical extent in map height
    vPossibleZoom = projection.zoom - math.ceil(vZoomDiff)

    # initial zoom to fit extent vertically and horizontally
    initZoom = min(hPossibleZoom, vPossibleZoom)

    ## additionally, make sure it's not outside the boundaries set by provider limits
    #initZoom = min(initZoom, provider.outerLimits()[1].zoom)
    #initZoom = max(initZoom, provider.outerLimits()[0].zoom)

    # coordinate of extent center
    centerColumn = (TL[0] + BR[0]) / 2
    centerRow = (TL[1] + BR[1]) / 2
    centerZoom = projection.zoom

    coord = zoom_to((centerColumn, centerRow), centerZoom, initZoom)

    origin, offset = calculateMapCenter(provider, coord)
    return origin, offset, initZoom


# vim: sw=4:et:ai
