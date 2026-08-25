"""The bottom shell: a plain plate with four blind stations in its top face."""

import math

from pytest import approx

from conftest import inside, render_failure, walls

LOWER = 2.0
UPPER = 3.1
CHAMFER = 1.0
FILLET = 0.5
HOLE_D = 6.03
PITCH = 15.0
STATIONS = [0.0, 15.0, 30.0, 45.0]

PLATE_X = (-10.0, 20.0)
PLATE_Y = (-15.0, 60.0)


def test_the_plate_is_one_closed_solid(bottom):
    assert bottom.is_watertight
    assert bottom.is_winding_consistent
    assert bottom.body_count == 1


def test_it_is_thirty_by_seventy_five_by_five_one(bottom):
    low, high = bottom.bounds
    assert (low[0], high[0]) == approx(PLATE_X, abs=1e-3)
    assert (low[1], high[1]) == approx(PLATE_Y, abs=1e-3)
    assert (low[2], high[2]) == approx((-LOWER, UPPER), abs=1e-6)


def test_it_is_the_shape_the_top_shells_cavity_is_cut_to(bottom, part):
    """Same outline, same call to `outline`, so the two have to agree.

    Measured at the cavity's ceiling, where it is widest -- the draft takes it
    in from there, which is the fit problem described in README.md.
    """
    cavity = walls(part, 0, 22.5, -0.05, -13.0, 23.0)
    plate = walls(bottom, 0, 22.5, 1.0, -13.0, 23.0)
    assert (plate[0], plate[-1]) == approx((cavity[1], cavity[2]), abs=0.02)


def test_the_four_stations_are_blind_from_above(bottom):
    for y in STATIONS:
        assert not inside(bottom, [0.0, y, UPPER - 0.05], [0.0, y, 0.05]).any(), \
            f"the hole at y = {y} is not open"
        assert inside(bottom, [0.0, y, -0.05], [0.0, y, -LOWER + 0.05]).all(), \
            f"the hole at y = {y} broke through the floor"


def test_the_stations_are_six_millimetres_across_on_a_fifteen_pitch(bottom):
    for y in STATIONS:
        across = walls(bottom, 0, y, 1.5, -5.0, 5.0)
        assert list(across) == approx([-HOLE_D / 2, HOLE_D / 2], abs=0.01)
    assert [b - a for a, b in zip(STATIONS, STATIONS[1:])] == [PITCH] * 3


def test_two_millimetres_of_floor_under_every_station(bottom):
    # Straight down the axis of a hole: solid from the floor at z = 0 down to
    # the bottom face, and nothing below it.
    for y in STATIONS:
        assert inside(bottom, [0.0, y, -0.05])[0]
        assert inside(bottom, [0.0, y, -LOWER + 0.05])[0]
        assert not inside(bottom, [0.0, y, -LOWER - 0.05])[0]


def test_the_bottom_face_is_chamfered_and_the_top_edge_rounded(bottom):
    face = bottom.vertices[abs(bottom.vertices[:, 2] + LOWER) < 1e-6]
    assert face[:, 0].min() == approx(PLATE_X[0] + CHAMFER, abs=1e-3)
    assert face[:, 0].max() == approx(PLATE_X[1] - CHAMFER, abs=1e-3)
    top = bottom.vertices[abs(bottom.vertices[:, 2] - UPPER) < 1e-6]
    outer = top[top[:, 0] > 10.0]        # clear of the hole rims on the axis
    assert outer[:, 0].max() == approx(PLATE_X[1] - FILLET, abs=1e-3)
    # Full width in between.
    across = walls(bottom, 0, 22.5, 1.0, -13.0, 23.0)
    assert list(across) == approx(list(PLATE_X), abs=2e-3)


def test_the_corner_key_matches_the_top_shells(bottom):
    # y - x = 65 on this outline, as on the top shell's cavity.
    assert not inside(bottom, [-9.0, 57.0, 1.0], [-6.0, 60.0, 1.0]).any()
    assert inside(bottom, [-9.0, 55.0, 1.0], [-6.0, 57.0, 1.0]).all()


def test_holes_that_would_break_out_of_a_wall_are_rejected():
    complaint = render_failure("down_indicator_selector_bottom.scad",
                               holeDiameter=25.0)
    assert "break out" in complaint


def test_the_plate_volume_is_the_prism_less_what_is_taken_off(bottom):
    profile = 30.0 * 75.0 - 3 * 6.0 ** 2 * (1 - math.pi / 4) - 5.0 ** 2 / 2
    perimeter = 199.3454
    holes = 4 * math.pi * (HOLE_D / 2) ** 2 * UPPER
    chamfer = perimeter * CHAMFER ** 2 / 2
    fillet = perimeter * FILLET ** 2 * (1 - math.pi / 4)
    assert bottom.volume == approx(
        profile * (LOWER + UPPER) - holes - chamfer - fillet, rel=0.002)
