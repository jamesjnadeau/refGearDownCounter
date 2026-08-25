"""Spring-bar lugs, carried over from the down counter's as-built geometry."""

import math

from pytest import approx

from conftest import inside

BODY_T = 6.7
MID = BODY_T / 2
GAP = 20.2          # 20mm band + 0.2mm clearance
HORN_THK = 4.9      # (30 - 20.2) / 2
PROT = 6.5          # 4.5mm bar standoff + 2.0mm tip margin
BAR_Y = 24.5        # 20 + 4.5, where Task 5 drills the bore
HORN_Y = 22.0       # solid horn, clear of the bore -- probe material here
BLANK_VOLUME = 30.0 * 40.0 * 6.7


def test_lug_body_is_one_closed_solid(lugs):
    assert lugs.is_watertight
    assert lugs.body_count == 1


def test_lug_to_lug_is_fifty_three_millimetres(lugs):
    low, high = lugs.bounds
    assert high[1] - low[1] == approx(53.0, abs=1e-6)
    assert list(low) == approx([-15.0, -26.5, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 26.5, 6.7], abs=1e-6)


def test_horns_add_four_chamfered_prisms(lugs):
    # 4 horns, less a 0.5mm chamfer on each of the two tip corners per horn,
    # less the four bar bores.
    horns = 4 * HORN_THK * PROT * BODY_T - 4 * 2 * (0.5 * 0.5**2) * BODY_T
    bores = 4 * (BAR_R**2 * (3 * math.pi / 4 + 1)) * HORN_THK
    assert lugs.volume - BLANK_VOLUME == approx(horns - bores, rel=0.001)


def test_the_band_gap_takes_a_twenty_millimetre_strap(lugs):
    # Open across the full gap...
    assert not inside(lugs, [0.0, HORN_Y, MID], [10.0, HORN_Y, MID], [-10.0, HORN_Y, MID]).any()
    # ...and solid immediately outboard of it.
    assert inside(lugs, [10.3, HORN_Y, MID], [-10.3, HORN_Y, MID]).all()


def test_horns_run_flush_to_the_side_walls(lugs):
    assert inside(lugs, [14.8, HORN_Y, MID])[0]
    assert not inside(lugs, [15.2, HORN_Y, MID])[0]


def test_horns_are_full_body_height(lugs):
    assert inside(lugs, [12.5, HORN_Y, 0.1], [12.5, HORN_Y, BODY_T - 0.1]).all()
    assert not inside(lugs, [12.5, HORN_Y, -0.1], [12.5, HORN_Y, BODY_T + 0.1]).any()


def test_tip_corners_are_chamfered(lugs):
    # The outboard tip corner at (15, 26.5) is cut back by 0.5mm.
    assert not inside(lugs, [14.9, 26.4, MID])[0]
    assert inside(lugs, [14.3, 26.4, MID])[0]


BAR_R = 0.55        # 1.1mm bore
HORNS_VOLUME = 8886.88


def test_the_bore_runs_right_through_the_horn(lugs):
    row = [[x, BAR_Y, MID] for x in (10.5, 12.5, 14.5)]
    assert not inside(lugs, *row).any()


def test_the_bore_sits_at_mid_height_with_material_above_and_below(lugs):
    assert inside(lugs, [12.5, BAR_Y, MID + 1.5], [12.5, BAR_Y, MID - 1.5]).all()


def test_the_bore_is_offset_from_the_tip_by_the_margin(lugs):
    # 2mm of material past the bore centre, so the tip at y = 26.5 is solid.
    assert inside(lugs, [12.5, 26.2, MID])[0]


# All four bores: (x = +-12.5) x (y = +-BAR_Y). Every one of them has to point
# the same way, or half the part prints with an unsupported crown.
HORNS = [(sx * 12.5, sy * BAR_Y) for sx in (-1, 1) for sy in (-1, 1)]
REACH = BAR_R * 1.35   # inside the apex at r*sqrt(2) = 0.778, outside r = 0.55


def test_the_teardrop_apex_points_toward_the_wrist_side(lugs):
    """Apex at r*sqrt(2) below centre; the matching point above is solid."""
    for x, y in HORNS:
        assert not inside(lugs, [x, y, MID - REACH])[0], \
            f"no apex on the -Z side of the horn at ({x}, {y})"
        assert inside(lugs, [x, y, MID + REACH])[0], \
            f"apex is on the wrong side of the horn at ({x}, {y})"


def test_bores_remove_four_small_teardrops(lugs):
    # Teardrop area is r^2 * (3*pi/4 + 1); four bores through 4.9mm of horn.
    expected = 4 * (BAR_R**2 * (3 * math.pi / 4 + 1)) * HORN_THK
    assert HORNS_VOLUME - lugs.volume == approx(expected, rel=0.02)


def test_lug_body_is_still_one_closed_solid(lugs):
    assert lugs.is_watertight
    assert lugs.body_count == 1


def test_teardrop_can_be_flipped_for_the_other_print_orientation():
    from conftest import render

    flipped = render("tests/scad/lugs_only.scad", teardropDown=False)
    for x, y in HORNS:
        assert not inside(flipped, [x, y, MID + REACH])[0], \
            f"no apex on the +Z side of the horn at ({x}, {y})"
        assert inside(flipped, [x, y, MID - REACH])[0], \
            f"apex is on the wrong side of the horn at ({x}, {y})"
