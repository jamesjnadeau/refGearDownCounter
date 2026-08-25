"""How the three parts go together.

Nothing records this. The Onshape assembly is empty -- no instances, no mates
-- so the only evidence for how the counter stacks up is the geometry itself.
These tests are that reading, written down and checked, and the one that
matters most is the last: as drawn, the bottom shell does not fit the cavity
it goes into.

Each part is drawn about its own z = 0. Put in the top shell's frame:

    bottom shell   -5.10 .. 0.00    its top face on the cavity ceiling
    top shell      -4.00 .. 3.10
    button flange   0.00 .. 1.00
    button boss     1.00 .. 5.00
"""

import math

from pytest import approx

from conftest import inside, walls

DRAFT = 3.0
SKIRT = 4.0
FILLET = 0.5


def test_the_bottom_shell_is_the_shape_of_the_cavity_at_its_ceiling(part, bottom):
    for axis, at, lo, hi in ((0, 22.5, -13.0, 23.0), (1, 5.0, -18.0, 63.0)):
        cavity = walls(part, axis, at, -0.05, lo, hi)
        plate = walls(bottom, axis, at, 1.0, lo, hi)
        assert (plate[0], plate[-1]) == approx((cavity[1], cavity[2]), abs=0.02)


def test_the_bottom_shell_does_not_fit_the_cavity_it_goes_into(part, bottom):
    """0.18mm of interference per side, and this is the as-built number.

    The cavity is drafted three degrees and is widest at its ceiling, so it
    narrows toward the opening the bottom shell has to come in through. The
    bottom shell is the full ceiling size. It cannot be pushed in without
    deforming something.

    This is the original's geometry, faithfully converted. Whether it is a
    press fit on purpose or leftover moulding draft is not recorded anywhere
    -- see README.md. The test exists so that if anyone changes the draft to
    fix it, the change is deliberate and the number here moves with it.
    """
    mouth = walls(part, 0, 22.5, -SKIRT + FILLET, -13.0, 23.0)   # tightest section
    plate = walls(bottom, 0, 22.5, 1.0, -13.0, 23.0)
    interference = (plate[-1] - plate[0]) - (mouth[2] - mouth[1])
    assert interference == approx(2 * (SKIRT - FILLET) * math.tan(math.radians(DRAFT)),
                                  abs=0.01)
    assert interference == approx(0.367, abs=0.01)


def test_the_flange_is_captive_under_the_plate(part, button):
    """Wider than the opening it sits under, narrower than the pocket."""
    flange = walls(button, 0, 0.0, -0.5, -8.0, 8.0)
    pocket = walls(part, 0, 22.5, 0.7, -8.0, 8.0)
    opening = walls(part, 0, 22.5, 1.8, -8.0, 8.0)
    assert flange[-1] - flange[0] < pocket[1] - pocket[0]
    assert flange[-1] - flange[0] > opening[1] - opening[0]
    assert (pocket[1] - pocket[0]) - (flange[-1] - flange[0]) == approx(1.0, abs=0.02)


def test_the_boss_passes_through_the_opening(part, button):
    boss = walls(button, 0, 0.0, 2.0, -8.0, 8.0)
    opening = walls(part, 0, 22.5, 1.8, -8.0, 8.0)
    assert (opening[1] - opening[0]) - (boss[-1] - boss[0]) == approx(0.4, abs=0.02)


def test_the_button_stands_proud_of_the_top_face(part, button):
    """1mm of flange in a 1.4mm pocket, so the boss reaches 1.9mm clear."""
    flange_t = button.bounds[1][2] - button.bounds[0][2] - 4.0
    pocket_depth = 1.4
    plate = 3.1
    assert flange_t == approx(1.0, abs=1e-3)
    assert flange_t + 4.0 - plate == approx(1.9, abs=1e-3)
    assert pocket_depth - flange_t == approx(0.4, abs=1e-3), "how far it can lift"


def test_the_bore_lines_up_over_a_station(button, bottom):
    """Something has to run through the one into the other. It is not drawn."""
    bore = walls(button, 0, 0.0, 1.0, -5.0, 5.0)[1:3]
    station = walls(bottom, 0, 0.0, 1.5, -5.0, 5.0)
    assert list(bore) == approx(list(station), abs=0.01)


def test_the_bottom_shell_stands_proud_of_the_skirt(part, bottom):
    """5.1mm of shell into a 4mm cavity: 1.1mm of it stays outside."""
    depth = -part.bounds[0][2]
    thickness = bottom.bounds[1][2] - bottom.bounds[0][2]
    assert depth == approx(4.0, abs=1e-6)
    assert thickness == approx(5.1, abs=1e-6)
    assert thickness - depth == approx(1.1, abs=1e-6)


def test_the_stations_sit_under_the_slot(part, bottom):
    """The four holes are on the slot's centreline and within its run."""
    for y in (0.0, 15.0, 30.0, 45.0):
        assert not inside(part, [0.0, y, 2.0])[0], f"no slot over the station at {y}"
        assert not inside(bottom, [0.0, y, 1.5])[0], f"no hole at the station at {y}"
