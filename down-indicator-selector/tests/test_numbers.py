"""The numerals 1-4, cut clean through the plate beside the slot."""

import numpy as np
from pytest import approx

from conftest import inside

PLATE = 3.1
BASELINE = 9.4142136
CENTRES = [47.857, 32.219, 15.590, -1.095]   # 1, 2, 3, 4
MID = PLATE / 2


def _ink(mesh):
    """Vertices of the numeral outlines on the top face."""
    v = mesh.vertices
    on_top = abs(v[:, 2] - PLATE) < 1e-6
    beside_the_slot = (v[:, 0] > 8.0) & (v[:, 0] < 19.0)
    # Clear of the plate's own outline, which reaches into that band of x at
    # each end of the part.
    between_the_ends = (v[:, 1] > -8.0) & (v[:, 1] < 54.0)
    return v[on_top & beside_the_slot & between_the_ends]


def test_there_are_four_numerals_and_each_is_cut_through(part):
    for numeral, y in enumerate(CENTRES, start=1):
        row = [[x, y, MID] for x in np.linspace(BASELINE + 0.2, BASELINE + 6.7, 200)]
        assert not inside(part, *row).all(), f"nothing was cut for the {numeral}"
        under = [[x, y, -0.05] for x in np.linspace(BASELINE + 0.2, BASELINE + 6.7, 200)]
        assert not inside(part, *under).any(), \
            f"the {numeral} does not reach the plate's underside"


def test_the_numerals_stand_on_the_baseline_and_grow_toward_plus_x(part):
    ink = _ink(part)
    assert ink[:, 0].min() == approx(BASELINE, abs=0.2)
    assert ink[:, 0].max() - ink[:, 0].min() == approx(7.0, abs=0.4)
    # Nothing is cut on the far side of the baseline.
    assert inside(part, *[[BASELINE - 0.3, y, MID] for y in CENTRES]).all()


def test_the_numerals_sit_between_the_slot_and_the_right_hand_wall(part):
    for y in CENTRES:
        assert inside(part, [8.0, y, MID], [18.0, y, MID]).all(), \
            f"the plate should be solid either side of the numeral at y = {y}"


def test_the_numerals_run_down_the_plate_in_order(part):
    ink = _ink(part)
    for numeral, y in enumerate(CENTRES, start=1):
        near = ink[abs(ink[:, 1] - y) < 3.5]
        assert len(near) > 8, f"found almost no outline for the {numeral}"
    assert CENTRES == sorted(CENTRES, reverse=True), \
        "1 is at the far end of the plate and 4 nearest the origin"


def test_the_part_is_one_closed_solid(part):
    """Which it only is because the 4 is tied. See the next test."""
    assert part.is_watertight
    assert part.is_winding_consistent
    assert part.body_count == 1


def test_without_the_tie_the_four_leaves_a_floating_island(untied):
    """As the original does. That is the defect the tie exists to fix.

    Cutting the numeral through the plate leaves the triangle inside it as a
    loose piece, which drops out of the print. Onshape reports two solid
    bodies for `top` for exactly this reason, and the working copy's lug
    feature ends by deleting the stray one.
    """
    assert untied.body_count == 2
    island = sorted(untied.split(only_watertight=False), key=lambda b: b.volume)[0]
    low, high = island.bounds
    assert low[2] == approx(0.0, abs=1e-6)
    assert high[2] == approx(PLATE, abs=1e-6)
    assert low[0] > BASELINE and high[0] < BASELINE + 7.0
    assert abs((low[1] + high[1]) / 2 - CENTRES[3]) < 2.0


def test_the_tie_crosses_the_diagonal_and_nothing_else(part, untied):
    """It should add one small bar of plate, not reshape the numeral."""
    added = part.volume - untied.volume
    assert 0.5 < added < 4.0, f"the tie adds {added:.2f}mm^3, which is not a tie"
    # The other three numerals are untouched: the tie is on the 4 alone.
    for y in CENTRES[:3]:
        row = [[x, y, MID] for x in np.linspace(BASELINE + 0.2, BASELINE + 6.7, 200)]
        assert list(inside(part, *row)) == list(inside(untied, *row))


def test_leaving_the_numerals_off_gives_one_solid(unmarked):
    assert unmarked.is_watertight
    assert unmarked.body_count == 1
