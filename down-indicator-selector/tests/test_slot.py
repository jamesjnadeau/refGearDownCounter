"""The slot, its pocket, and the ledge between them that holds the button in."""

import math

from pytest import approx

from conftest import inside, render_failure, section_area, walls

PLATE = 3.1
POCKET = 1.4
CHAMFER = 1.0
OPENING = 8.4
FLANGE = 13.0
RUN = (0.0, 45.0)          # the four stations, 15mm apart
MID = sum(RUN) / 2


def test_the_slot_runs_the_whole_length_of_the_stations(part):
    for y in (RUN[0], 15.0, 30.0, RUN[1]):
        assert not inside(part, [0.0, y, 0.7], [0.0, y, 2.5]).any(), \
            f"the slot is blocked at the station at y = {y}"
    # And stops one opening-radius past each end.
    assert inside(part, [0.0, RUN[0] - OPENING / 2 - 0.3, 1.8])[0]
    assert inside(part, [0.0, RUN[1] + OPENING / 2 + 0.3, 1.8])[0]


def test_the_opening_is_eight_point_four_wide(part):
    across = walls(part, 0, MID, PLATE - CHAMFER - 0.05, -7.0, 7.0)
    assert list(across) == approx([-OPENING / 2, OPENING / 2], abs=0.01)


def test_the_pocket_under_it_is_thirteen_wide(part):
    across = walls(part, 0, MID, POCKET - 0.05, -7.0, 7.0)
    assert list(across) == approx([-FLANGE / 2, FLANGE / 2], abs=0.01)


def test_the_ledge_is_where_the_flange_bears(part):
    """2.3mm of overhang each side, at 1.4mm above the plate's underside."""
    assert inside(part, [5.0, MID, POCKET + 0.05], [-5.0, MID, POCKET + 0.05]).all()
    assert not inside(part, [5.0, MID, POCKET - 0.05], [-5.0, MID, POCKET - 0.05]).any()
    ledge = (45.0 * FLANGE + math.pi * (FLANGE / 2) ** 2) \
        - (45.0 * OPENING + math.pi * (OPENING / 2) ** 2)
    assert section_area(part, POCKET + 0.05) - section_area(part, POCKET - 0.05) \
        == approx(ledge, abs=1.0)


def test_the_opening_takes_the_same_chamfer_as_the_outside(part):
    """One chamfer feature in the original, propagated round every top edge."""
    top = walls(part, 0, MID, PLATE - 0.05, -7.0, 7.0)
    assert list(top) == approx([-(OPENING / 2 + CHAMFER - 0.05),
                                OPENING / 2 + CHAMFER - 0.05], abs=0.01)


def test_the_slot_is_a_racetrack_not_a_rectangle(part):
    """Square ends would let the button rock; the ends are half-round."""
    corner = OPENING / 2 / math.sqrt(2)
    assert inside(part, [corner + 0.3, RUN[1] + corner + 0.3, 1.8])[0]
    assert not inside(part, [corner - 0.3, RUN[1] + corner - 0.3, 1.8])[0]


def test_a_pocket_no_wider_than_the_opening_is_rejected():
    complaint = render_failure("down_indicator_selector.scad", buttonDiameter=8.0)
    assert "captive" in complaint
