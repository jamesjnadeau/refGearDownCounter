"""The cord holes and the face troughs that open them to the ends."""

import math

import numpy as np
from pytest import approx

from conftest import inside

BODY_T = 6.7
CORD_R = 3.5
MID = BODY_T / 2
BLANK_VOLUME = 30.0 * 40.0 * 6.7

# A 96-gon inscribed in a circle of radius r has area 48 * r^2 * sin(3.75 deg).
HOLE_AREA = 0.5 * 96 * CORD_R**2 * math.sin(math.radians(360 / 96))


def test_cord_body_is_one_closed_solid(cord):
    assert cord.is_watertight
    assert cord.body_count == 1


def test_holes_remove_exactly_two_cylinders(cord):
    assert BLANK_VOLUME - cord.volume == approx(2 * HOLE_AREA * BODY_T, rel=1e-6)


def test_each_hole_goes_all_the_way_through(cord):
    for sign in (-1, 1):
        column = [[0.0, sign * 10.0, z] for z in (0.2, MID, 6.5)]
        assert not inside(cord, *column).any()


def test_holes_are_seven_millimetres_across(cord):
    # Probe across the +Y hole at mid-height, 0.1mm inside and outside the wall.
    assert not inside(cord, [3.4, 10.0, MID])[0]
    assert inside(cord, [3.6, 10.0, MID])[0]


def test_material_remains_between_the_holes(cord):
    assert inside(cord, [0.0, 0.0, MID])[0]
