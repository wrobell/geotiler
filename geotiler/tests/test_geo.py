#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2022 by Artur Wroblewski <wrobell@riseup.net>
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

from geotiler.geo import Transformation, WebMercator, zoom_to
from functools import partial

import pytest

approx = partial(pytest.approx, abs=1e-3)

@pytest.fixture
def web_mercator():
    wm = WebMercator(10)
    wm.transformation = Transformation(1, 0, 0, 0, 1, 0)
    return wm


def test_transformation_identity() -> None:
    """
    Test identity transformation.
    """
    t = Transformation(1, 0, 0, 0, 1, 0)
    p = 1, 1

    pt = t.transform(p)
    assert 1.0 == pt[0]
    assert 1.0 == pt[1]

    ptt = t.untransform(pt)
    assert 1.0 == pt[0]
    assert 1.0 == pt[1]

def test_transformation_0_1_0() -> None:
    """
    Test transformation for (0, 1, 0, ...).
    """
    t = Transformation(0, 1, 0, 1, 0, 0)
    p = 0, 1

    pt = t.transform(p)
    assert 1.0 == pt[0]
    assert 0.0 == pt[1]

    ptt = t.untransform(pt)
    assert 0.0 == ptt[0]
    assert 1.0 == ptt[1]

def test_transformation_1_0_1() -> None:
    """
    Test transformation for (1, 0, 1, ...).
    """
    t = Transformation(1, 0, 1, 0, 1, 1)
    p = 0, 0

    pt = t.transform(p)
    assert 1.0 == pt[0]
    assert 1.0 == pt[1]

    ptt = t.untransform(pt)
    assert 0.0 == ptt[0]
    assert 0.0 == ptt[1]

def test_web_mercator_rev_geocode_at_zero(web_mercator) -> None:
    """
    Test Web Mercator projection reverse geocode at (0, 0) position.
    """
    coord = web_mercator.rev_geocode((0, 0))
    assert 0.0 == approx(coord[0])
    assert 0.0 == approx(coord[1])

def test_web_mercator_geocode_at_zero(web_mercator) -> None:
    """
    Test Web Mercator projection geocode at (0, 0) position.
    """
    pt = web_mercator.geocode((0, 0), 10)
    assert 0.0 == approx(pt[0])
    assert 0.0 == approx(pt[1])

def test_web_mercator_rev_geocode(web_mercator) -> None:
    """
    Test Web Mercator projection reverse geocode at a position.
    """
    coord = web_mercator.rev_geocode((-122, 37))
    assert -2.129 == approx(coord[0])
    assert 0.696 == approx(coord[1])

def test_web_mercator_geocode(web_mercator) -> None:
    """
    Test Web Mercator projection geocode at a position.
    """
    pt = web_mercator.geocode((-2.129, 0.696), 10.000)
    assert -121.983 == approx(pt[0])
    assert 37.001 == approx(pt[1])

def test_zoom() -> None:
    """
    Test zooming tile coordinates.
    """
    coord = zoom_to((1, 0), 2, 3)
    assert (2, 0) == coord

    coord = zoom_to((1, 0), 2, 1)
    assert (0.5, 0) == coord

# vim: sw=4:et:ai
