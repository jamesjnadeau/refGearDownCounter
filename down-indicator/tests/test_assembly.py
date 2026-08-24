"""The complete part, and the guards on its parameters."""

import math

from pytest import approx

from conftest import inside, render, render_failure

BODY_T = 6.7
MID = BODY_T / 2
NECK = 2 * math.sqrt(3.5**2 - (BODY_T / 2) ** 2)
BAR_Y = 24.5


def test_the_part_is_one_closed_printable_solid(part):
    assert part.is_watertight
    assert part.is_winding_consistent
    assert part.body_count == 1
    assert part.volume == approx(7816.2, rel=1e-4)


def test_overall_dimensions(part):
    low, high = part.bounds
    assert list(low) == approx([-15.0, -26.5, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 26.5, 6.7], abs=1e-6)


def test_the_cord_slots_survive_the_assembly(part):
    for sign in (-1, 1):
        run = [[0.0, sign * y, MID] for y in (10.0, 13.0, 16.0, 19.0, 20.0)]
        assert not inside(part, *run).any()
    assert not inside(part, [NECK / 2 - 0.1, 16.0, MID])[0]
    assert inside(part, [NECK / 2 + 0.1, 16.0, MID])[0]


def test_the_slot_exits_inside_the_band_gap_and_clears_the_horns(part):
    """Slot spans x +-3.5; the gap spans x +-10.1. Nothing between them is cut."""
    assert not inside(part, [0.0, 20.5, MID])[0], "slot does not exit the end"
    assert inside(part, [12.5, 22.0, MID])[0], "the slot has eaten into a horn"


def test_the_lugs_survive_the_assembly(part):
    assert not inside(part, [12.5, BAR_Y, MID])[0], "bore is blocked"
    assert inside(part, [12.5, BAR_Y, MID + 1.5])[0], "horn material is missing"


def test_a_body_as_thick_as_the_cord_is_rejected():
    err = render_failure("down_indicator.scad", bodyT=8.0)
    assert "bodyT must be less than cordDia" in err


def test_a_band_too_wide_for_the_end_is_rejected():
    err = render_failure("down_indicator.scad", bandWidth=24)
    assert "horn thickness" in err


def test_holes_that_break_out_of_the_end_are_rejected():
    err = render_failure("down_indicator.scad", holeY=17)
    assert "cord holes break out" in err


def test_holes_that_merge_through_the_middle_are_rejected():
    """At 2*holeY <= cordDia the troughs join into a channel that severs the slab."""
    err = render_failure("down_indicator.scad", holeY=3.0)
    assert "wall between the cord holes" in err


def test_an_inter_hole_wall_under_two_millimetres_is_rejected():
    # 2*4.4 - 7 = 1.8mm of wall: still two distinct holes, but too thin.
    err = render_failure("down_indicator.scad", holeY=4.4)
    assert "wall between the cord holes" in err


def test_a_chamfer_that_would_eat_the_horns_is_rejected():
    """Past hornThk/2 the horn polygon self-intersects and the lugs vanish."""
    err = render_failure("down_indicator.scad", tipChamfer=2.5)
    assert "tip chamfer" in err


def test_a_body_too_thin_for_the_cord_neck_is_rejected():
    # 6.0mm body -> a 3.606mm neck, wide enough for the cord to escape.
    err = render_failure("down_indicator.scad", bodyT=6.0)
    assert "cord neck" in err


def test_a_body_too_thick_for_the_cord_neck_is_rejected():
    # 6.9mm body -> a 1.179mm neck, too tight to thread the cord through.
    err = render_failure("down_indicator.scad", bodyT=6.9)
    assert "cord neck" in err


def test_a_thinner_body_still_builds_and_widens_the_neck():
    thin = render("down_indicator.scad", bodyT=6.4)
    wider = 2 * math.sqrt(3.5**2 - (6.4 / 2) ** 2)
    assert wider > NECK
    assert thin.is_watertight
    assert not inside(thin, [wider / 2 - 0.1, 16.0, 6.4 / 2])[0]
