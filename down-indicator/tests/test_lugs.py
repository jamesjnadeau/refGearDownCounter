"""Spring-bar lugs, carried over from the down counter's as-built geometry."""

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
    # 4 horns, less a 0.5mm chamfer on each of the two tip corners per horn.
    expected = 4 * HORN_THK * PROT * BODY_T - 4 * 2 * (0.5 * 0.5**2) * BODY_T
    assert lugs.volume - BLANK_VOLUME == approx(expected, rel=1e-6)


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
