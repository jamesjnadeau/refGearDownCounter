"""The cord holes and the face troughs that open them to the ends."""

import math

import numpy as np
from pytest import approx

from conftest import inside

BODY_T = 6.7
CORD_R = 3.5
MID = BODY_T / 2


def test_cord_body_is_one_closed_solid(cord):
    assert cord.is_watertight
    assert cord.body_count == 1


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


# Where the two face troughs overlap, at mid-thickness:
#   neck = 2 * sqrt(r^2 - (t/2)^2) = 2.0273mm
NECK = 2 * math.sqrt(CORD_R**2 - (BODY_T / 2) ** 2)


def test_the_arithmetic_the_thickness_was_chosen_for():
    assert NECK == approx(2.027, abs=0.001)


def test_the_slot_is_open_from_the_hole_to_the_end(cord):
    """No solid anywhere on the slot centreline at mid-thickness."""
    for sign in (-1, 1):
        ys = np.linspace(sign * 10.0, sign * 20.0, 41)
        points = [[0.0, y, MID] for y in ys]
        assert not inside(cord, *points).any()


def test_the_neck_is_the_width_the_geometry_predicts(cord):
    y = 16.0  # midway between the hole edge and the body end
    assert not inside(cord, [NECK / 2 - 0.1, y, MID])[0], "neck is narrower than predicted"
    assert inside(cord, [NECK / 2 + 0.1, y, MID])[0], "neck is wider than predicted"


def test_the_trough_is_full_width_at_both_faces(cord):
    y = 16.0
    for z in (0.05, BODY_T - 0.05):
        assert not inside(cord, [3.3, y, z])[0], "trough is not 7mm wide at the face"
        assert inside(cord, [3.7, y, z])[0], "trough is wider than 7mm at the face"


def test_the_troughs_run_outward_not_inward(cord):
    """Between the two holes the body is untouched at every height."""
    for z in (0.05, MID, BODY_T - 0.05):
        assert inside(cord, [0.0, 0.0, z])[0]


def test_holes_and_troughs_together(cord):
    assert cord.volume == approx(6989.209, rel=1e-4)
    assert cord.is_watertight
    assert cord.body_count == 1
