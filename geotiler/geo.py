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

import math


class Transformation(object):
    def __init__(self, ax, bx, cx, ay, by, cy):
        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.ay = ay
        self.by = by
        self.cy = cy

    def transform(self, point):
        x, y = point
        return (
            self.ax * x + self.bx * y + self.cx,
            self.ay * x + self.by * y + self.cy
        )


    def untransform(self, point):
        x, y = point
        return (
            (x * self.by - y * self.bx - self.cx * self.by + self.cy * self.bx) / (self.ax * self.by - self.ay * self.bx),
            (x * self.ay - y * self.ax - self.cx * self.ay + self.cy * self.ax) / (self.bx * self.ay - self.by * self.ax)
        )


def deriveTransformation(a1x, a1y, a2x, a2y, b1x, b1y, b2x, b2y, c1x, c1y, c2x, c2y):
    """ Generates a transform based on three pairs of points, a1 -> a2, b1 -> b2, c1 -> c2.
    """
    ax, bx, cx = linearSolution(a1x, a1y, a2x, b1x, b1y, b2x, c1x, c1y, c2x)
    ay, by, cy = linearSolution(a1x, a1y, a2y, b1x, b1y, b2y, c1x, c1y, c2y)

    return Transformation(ax, bx, cx, ay, by, cy)


def linearSolution(r1, s1, t1, r2, s2, t2, r3, s3, t3):
    """ Solves a system of linear equations.

          t1 = (a * r1) + (b + s1) + c
          t2 = (a * r2) + (b + s2) + c
          t3 = (a * r3) + (b + s3) + c

        r1 - t3 are the known values.
        a, b, c are the unknowns to be solved.
        returns the a, b, c coefficients.
    """
    a = (((t2 - t3) * (s1 - s2)) - ((t1 - t2) * (s2 - s3))) \
      / (((r2 - r3) * (s1 - s2)) - ((r1 - r2) * (s2 - s3)))

    b = (((t2 - t3) * (r1 - r2)) - ((t1 - t2) * (r2 - r3))) \
      / (((s2 - s3) * (r1 - r2)) - ((s1 - s2) * (r2 - r3)))

    c = t1 - (r1 * a) - (s1 * b)

    return a, b, c

class IProjection:
    def __init__(self, zoom, transformation=Transformation(1, 0, 0, 0, 1, 0)):
        self.zoom = zoom
        self.transformation = transformation

    def rawProject(self, point):
        raise NotImplementedError("Abstract method not implemented by subclass.")

    def rawUnproject(self, point):
        raise NotImplementedError("Abstract method not implemented by subclass.")

    def project(self, point):
        point = self.rawProject(point)
        if self.transformation:
            point = self.transformation.transform(point)
        return point

    def unproject(self, point):
        if self.transformation:
            point = self.transformation.untransform(point)
        point = self.rawUnproject(point)
        return point


    def rev_geocode(self, location):
        """
        Reverse geocode location as tile coordinates at projection's zoom.

        The method returns tile coordinates (x, y) for given location and
        projection's zoom level.

        :param location: Location to reverse geocode.
        """
        x, y = location
        point = math.pi * x / 180.0, math.pi * y / 180.0
        return self.project(point)


    def geocode(self, tile_coord, zoom):
        """
        Geocode tile coordinates and zoom level information.

        The method returns (longitude, latitude) pair of the tile
        coordinates at their zoom level.

        :param tile_coord: Tile coordinates.
        :param zoom: Zoom of the tile coordinates.
        """
        pt = zoom_to(tile_coord, zoom, self.zoom)
        x, y = self.unproject(pt)
        return 180.0 * x / math.pi, 180.0 * y / math.pi



class MercatorProjection(IProjection):
    def rawProject(self, point):
        x, y = point
        return x, math.log(math.tan(0.25 * math.pi + 0.5 * y))

    def rawUnproject(self, point):
        x, y = point
        return x, 2 * math.atan(math.pow(math.e, y)) - 0.5 * math.pi



def zoom_to(tile_coord, zoom, target):
    """
    Zoom tile coordinates from current zoom to target zoom.

    :param tile_coord: Tile coordinates.
    :param zoom: Current zoom.
    :param target: Target zoom.
    """
    col, row = tile_coord
    d_zoom = target - zoom
    return col * math.pow(2, d_zoom), row * math.pow(2, d_zoom)


# vim:et sts=4 sw=4:
