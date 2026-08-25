"""The shell: footprint, walls, the chamfer and fillet, and the cavity."""

import math

from pytest import approx

from conftest import inside, render, render_failure, section_area, walls

WALL = 2.0
PLATE = 3.1
SKIRT = 4.0
CHAMFER = 1.0
FILLET = 0.5
DRAFT = 3.0
BULGE = 5 * math.sqrt(2) - 7      # 0.0711mm, at the two swung corners

CAV_X = (-10.0, 20.0)
CAV_Y = (-15.0, 60.0)
OUT_X = (CAV_X[0] - WALL, CAV_X[1] + WALL)
OUT_Y = (CAV_Y[0] - WALL, CAV_Y[1] + WALL)


def test_blank_is_one_closed_solid(blank):
    assert blank.is_watertight
    assert blank.is_winding_consistent
    assert blank.body_count == 1


def test_the_case_is_thirty_four_by_seventy_nine_by_seven_one(blank):
    low, high = blank.bounds
    assert low[2] == approx(-SKIRT, abs=1e-6)
    assert high[2] == approx(PLATE, abs=1e-6)
    # The walls are on 34 x 79; only the two swung corners reach past them.
    assert (low[0], high[0]) == approx((OUT_X[0], OUT_X[1] + BULGE), abs=1e-3)
    assert (low[1], high[1]) == approx((OUT_Y[0] - BULGE, OUT_Y[1] + BULGE), abs=1e-3)


def test_the_walls_stand_where_the_original_puts_them(part):
    """On 34 x 79, whatever the corners are doing.

    This is the assertion that caught the convex hull in `banded` flattening
    each wall out to the corner bulge instead of leaving it on the wall line.
    """
    across = walls(part, 0, 22.5, -2.0, -13.0, 23.0)
    assert list(across[[0, -1]]) == approx(list(OUT_X), abs=2e-3)
    along = walls(part, 1, 5.0, -2.0, -18.0, 63.0)
    assert list(along[[0, -1]]) == approx(list(OUT_Y), abs=2e-3)


def test_the_skirt_wall_is_two_millimetres_at_the_ceiling(part):
    across = walls(part, 0, 22.5, -0.05, -13.0, 23.0)
    assert across[1] - across[0] == approx(WALL, abs=0.01)
    assert across[3] - across[2] == approx(WALL, abs=0.01)


def test_the_corner_key_cuts_the_minus_x_plus_y_corner(part):
    # The key runs y - x = 67 on the outside, so the corner past it is gone...
    assert not inside(part, [-11.0, 57.0, 1.0], [-8.0, 60.0, 1.0]).any()
    # ...and the material just inside it is there.
    assert inside(part, [-11.0, 55.0, 1.0], [-8.0, 58.0, 1.0]).all()
    # The same offset into each of the other three corners is solid.
    assert inside(part, [-9.0, -14.0, 1.0], [19.0, -14.0, 1.0], [19.0, 59.0, 1.0]).all()


def test_the_top_face_is_chamfered_one_millimetre_all_round(part):
    full = walls(part, 0, 22.5, PLATE - CHAMFER - 0.05, -13.0, 23.0)
    assert list(full[[0, -1]]) == approx(list(OUT_X), abs=2e-3)
    top = walls(part, 0, 22.5, PLATE - 0.05, -13.0, 23.0)
    # The -X wall is between two ordinary fillets and chamfers exactly; the +X
    # wall runs between the two swung corners, so it keeps the dent depth --
    # see the note on the clip in lib/shell.scad.
    assert top[0] == approx(OUT_X[0] + CHAMFER - 0.05, abs=2e-3)
    assert top[-1] == approx(OUT_X[1] - CHAMFER + 0.05 + BULGE, abs=2e-3)


def test_the_bottom_face_is_rounded_half_a_millimetre_all_round(part):
    face = part.vertices[abs(part.vertices[:, 2] + SKIRT) < 1e-6]
    assert face[:, 0].min() == approx(OUT_X[0] + FILLET, abs=1e-3)
    assert face[:, 1].max() == approx(OUT_Y[1] + BULGE - FILLET, abs=1e-3)
    # Full width again by the top of the round.
    full = walls(part, 0, 22.5, -SKIRT + FILLET + 0.05, -13.0, 23.0)
    assert list(full[[0, -1]]) == approx(list(OUT_X), abs=2e-3)


def test_the_cavity_is_thirty_by_seventy_five_at_its_ceiling(part):
    across = walls(part, 0, 22.5, -0.05, -13.0, 23.0)
    assert (across[1], across[2]) == approx(CAV_X, abs=0.01)
    along = walls(part, 1, 5.0, -0.05, -18.0, 63.0)
    assert (along[1], along[2]) == approx(CAV_Y, abs=0.01)


def test_the_cavity_is_drafted_narrower_toward_its_own_opening(part):
    """Three degrees, which grips the bottom shell rather than guiding it in."""
    ceiling = walls(part, 0, 22.5, -0.05, -13.0, 23.0)
    deep = walls(part, 0, 22.5, -3.55, -13.0, 23.0)
    for near, far in ((ceiling[1], deep[1]), (ceiling[2], deep[2])):
        assert abs(far) < abs(near), "the cavity should close up, not open out"
        assert abs(abs(near) - abs(far)) == approx(3.5 * math.tan(math.radians(DRAFT)),
                                                   abs=0.01)


def test_the_plate_is_solid_from_the_ceiling_to_the_top_face(part):
    assert inside(part, [15.0, 40.0, 0.05], [15.0, 40.0, 1.55], [15.0, 40.0, PLATE - 0.05]).all()
    assert not inside(part, [15.0, 40.0, -0.05], [15.0, 40.0, PLATE + 0.05]).any()


def test_the_plate_section_is_the_footprint_less_the_pocket(unmarked):
    """34 x 79, less what the corners and the key take off, less the pocket."""
    # One tangent fillet at 13.7345, and two swung corners at 9.6352 each.
    corners = 8.0 ** 2 * (1 - math.pi / 4) + 2 * 9.635239
    key = (7.0 ** 2) / 2
    pocket = 45.0 * 13.0 + math.pi * 6.5 ** 2
    footprint = 34.0 * 79.0 - corners - key
    assert section_area(unmarked, 0.7) == approx(footprint - pocket, abs=0.5)


def test_a_fillet_wider_than_half_the_wall_is_rejected():
    complaint = render_failure("down_indicator_selector.scad", bottomFillet=1.5)
    assert "bottom fillet" in complaint


def test_true_corner_fillets_are_a_different_shape_not_a_rounding_error(blank):
    """Which is why the default keeps the original's swung arcs.

    The swung arc comes half a millimetre closer to the corner than a tangent
    fillet does. The 0.0711mm it bulges past the walls is the small half of
    that difference, and quoting only that number is what nearly talked this
    model into squaring the corners off.
    """
    filleted = render("tests/scad/blank_only.scad", cornerSwing=8.0)
    low, high = filleted.bounds
    assert (low[0], high[0]) == approx(OUT_X, abs=1e-3)
    assert (low[1], high[1]) == approx(OUT_Y, abs=1e-3)
    # 0.48mm nearer the corner, over two corners and the full 7.1mm height.
    assert blank.volume - filleted.volume > 50.0
