"""The cord holes and the face troughs that carry the cord away from them.

Each hole's two troughs run to OPPOSITE side edges -- the watch-face one out
to +X, the wrist-side one out to -X -- so a strand entering one channel drops
through the hole and leaves in the other, heading the other way. The two
right-angle bends are the retention.

It follows that the cord is threaded, not pressed in: away from the hole the
two channels sit on opposite sides of the body and never meet, so there is no
open slot along the run. `test_the_cord_is_threaded_not_pressed_in` is the
test that pins that property down.
"""

import math

import numpy as np
from pytest import approx

from conftest import inside

BODY_T = 6.7
CORD_R = 3.5
MID = BODY_T / 2
HOLE_Y = 10.0
FLOOR = BODY_T - CORD_R  # 3.2mm of material left under each trough

# A 96-gon inscribed in a circle of radius r has area 48 * r^2 * sin(3.75 deg).
HOLE_AREA = 0.5 * 96 * CORD_R**2 * math.sin(math.radians(360 / 96))

HOLES = (-1, 1)  # the hole at y = -HOLE_Y and the one at y = +HOLE_Y


def test_cord_body_is_one_closed_solid(cord):
    assert cord.is_watertight
    assert cord.body_count == 1


def test_each_hole_goes_all_the_way_through(cord):
    for sign in HOLES:
        column = [[0.0, sign * HOLE_Y, z] for z in (0.2, MID, 6.5)]
        assert not inside(cord, *column).any()


def test_holes_are_seven_millimetres_across(cord):
    """Probed along Y at x = 0, where neither trough reaches at mid-height."""
    for sign in HOLES:
        y = sign * HOLE_Y
        assert not inside(cord, [0.0, y + sign * 3.4, MID])[0]
        assert inside(cord, [0.0, y + sign * 3.6, MID])[0]


def test_material_remains_between_the_holes(cord):
    for z in (0.2, MID, 6.5):
        assert inside(cord, [0.0, 0.0, z])[0]


def test_the_face_trough_runs_to_positive_x_only(cord):
    """The watch-face channel is on +X; the face on -X is unbroken."""
    for sign in HOLES:
        y = sign * HOLE_Y
        for x in (5.0, 9.0, 13.0):
            assert not inside(cord, [x, y, 6.4])[0], f"no face trough at x={x}"
            assert inside(cord, [-x, y, 6.4])[0], f"face cut on -X at x={-x}"


def test_the_wrist_trough_runs_to_negative_x_only(cord):
    """The wrist-side channel is on -X; the face on +X is unbroken."""
    for sign in HOLES:
        y = sign * HOLE_Y
        for x in (5.0, 9.0, 13.0):
            assert not inside(cord, [-x, y, 0.3])[0], f"no wrist trough at x={-x}"
            assert inside(cord, [x, y, 0.3])[0], f"wrist cut on +X at x={x}"


def test_both_troughs_reach_their_side_edge(cord):
    for sign in HOLES:
        y = sign * HOLE_Y
        assert not inside(cord, [14.6, y, 6.4])[0], "face trough stops short"
        assert not inside(cord, [-14.6, y, 0.3])[0], "wrist trough stops short"


def test_each_trough_leaves_a_floor(cord):
    """3.2mm of material under the face channel, and over the wrist one."""
    for sign in HOLES:
        y = sign * HOLE_Y
        for x in (5.0, 9.0, 13.0):
            assert inside(cord, [x, y, FLOOR / 2])[0], "face trough broke through"
            assert inside(cord, [-x, y, BODY_T - FLOOR / 2])[0], "wrist trough broke through"


def test_the_cord_is_threaded_not_pressed_in(cord):
    """No full-thickness opening anywhere along either run.

    The control is x = 0: there the hole itself goes clean through, so a
    blocked result everywhere would mean the probe, not the part, is wrong.
    """
    zs = np.linspace(0.05, BODY_T - 0.05, 60)

    def clear_through(x, y):
        column = np.column_stack([np.full_like(zs, x), np.full_like(zs, y), zs])
        return (~cord.contains(column)).all()

    for sign in HOLES:
        y = sign * HOLE_Y
        assert clear_through(0.0, y), "control failed: the hole is not open"
        for x in (5.0, 8.0, 11.0, 14.0):
            assert not clear_through(x, y), f"unexpected open slot at x={x}"
            assert not clear_through(-x, y), f"unexpected open slot at x={-x}"


def test_troughs_are_full_width_at_their_own_face(cord):
    """Seven millimetres across, measured along Y at each channel's own face."""
    for sign in HOLES:
        y = sign * HOLE_Y
        assert not inside(cord, [9.0, y + 3.3, 6.65])[0], "face trough under 7mm"
        assert inside(cord, [9.0, y + 3.7, 6.65])[0], "face trough over 7mm"
        assert not inside(cord, [-9.0, y + 3.3, 0.05])[0], "wrist trough under 7mm"
        assert inside(cord, [-9.0, y + 3.7, 0.05])[0], "wrist trough over 7mm"


def test_holes_and_troughs_together(cord):
    assert cord.volume == approx(6599.386, rel=1e-4)
    assert cord.is_watertight
    assert cord.body_count == 1
