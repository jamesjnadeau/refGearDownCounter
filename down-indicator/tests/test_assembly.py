"""The complete part, and the guards on its parameters."""

from pytest import approx

from conftest import inside, render, render_failure

BODY_T = 6.7
CORD_R = 3.5
MID = BODY_T / 2
HOLE_Y = 10.0
FLOOR = BODY_T - CORD_R  # 3.2mm under each cord trough
BAR_Y = 24.5
CHAM = 1.0  # chamfer where the outer walls meet each face


def test_the_part_is_one_closed_printable_solid(part):
    assert part.is_watertight
    assert part.is_winding_consistent
    assert part.body_count == 1
    assert part.volume == approx(7278.693, rel=1e-4)


def test_overall_dimensions(part):
    low, high = part.bounds
    assert list(low) == approx([-15.0, -26.5, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 26.5, 6.7], abs=1e-6)


def test_the_cord_slots_survive_the_assembly(part):
    """Face channel on +X, wrist channel on -X, both holes, floor intact."""
    for sign in (-1, 1):
        y = sign * HOLE_Y
        assert not inside(part, [0.0, y, MID])[0], "hole is blocked"
        for x in (5.0, 9.0, 13.0):
            assert not inside(part, [x, y, 6.4])[0], "face channel missing"
            assert not inside(part, [-x, y, 0.3])[0], "wrist channel missing"
            assert inside(part, [x, y, FLOOR / 2])[0], "face channel broke through"


def test_the_troughs_exit_the_side_walls_and_clear_the_horns(part):
    """Troughs run in X at y = +-10; the horns start at y = 19.5. No overlap."""
    for sign in (-1, 1):
        y = sign * HOLE_Y
        assert not inside(part, [14.6, y, 6.4])[0], "face trough does not exit"
        assert not inside(part, [-14.6, y, 0.3])[0], "wrist trough does not exit"
    assert inside(part, [12.5, 22.0, MID])[0], "a trough has eaten into a horn"


def test_the_lugs_survive_the_assembly(part):
    assert not inside(part, [12.5, BAR_Y, MID])[0], "bore is blocked"
    assert inside(part, [12.5, BAR_Y, MID + 1.5])[0], "horn material is missing"


def test_a_body_too_thin_to_floor_the_trough_is_rejected():
    # 5.0mm body -> 1.5mm of floor under a 3.5mm-deep trough.
    err = render_failure("down_indicator.scad", bodyT=5.0)
    assert "floor under the cord trough" in err


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


def test_every_outer_wall_is_chamfered_at_both_faces(part):
    """Near each face the wall is cut back by 1mm; at mid-height it is not.

    Walked around the whole outer boundary -- both side walls, all four horn
    tips, and both band-gap faces -- because a chamfer cutter that misses one
    wall looks identical in the bounding box and nearly identical in volume.
    """
    near = 0.1   # just inside the chamfer
    far = 0.8    # just outside it
    for z in (0.3, BODY_T - 0.3):
        for sx in (-1, 1):  # side walls, x = +-15
            assert not inside(part, [sx * (15.0 - near), 0.0, z])[0]
            assert inside(part, [sx * (15.0 - CHAM - far), 0.0, z])[0]
        for sx in (-1, 1):  # horn tip faces, y = +-26.5
            for sy in (-1, 1):
                assert not inside(part, [sx * 12.5, sy * (26.5 - near), z])[0]
                assert inside(part, [sx * 12.5, sy * (26.5 - CHAM - far), z])[0]
        for sy in (-1, 1):  # band gap, body end faces at y = +-20
            assert not inside(part, [5.0, sy * (20.0 - near), z])[0]
            assert inside(part, [5.0, sy * (20.0 - CHAM - far), z])[0]


def test_the_horn_interiors_are_left_square(part):
    """The faces the strap bears against keep their full height.

    Bevelling these would open the band gap by 1mm at each face, so a strap
    sized to the gap would sit loose top and bottom. All four are checked --
    the cutters that used to do this were per-horn, so one could be dropped
    while three stayed.
    """
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (0.15, MID, BODY_T - 0.15):
                assert inside(part, [sx * (10.1 + 0.15), sy * 23.0, z])[0], (
                    f"horn interior bevelled at z={z}"
                )


def test_the_band_gap_is_the_same_width_at_every_height(part):
    """20.2mm face to face, not just at mid-thickness."""
    for z in (0.15, MID, BODY_T - 0.15):
        assert not inside(part, [10.0, 23.0, z])[0], "gap narrower than 20.2"
        assert inside(part, [10.3, 23.0, z])[0], "gap wider than 20.2"


def test_the_chamfer_leaves_the_walls_full_height_at_mid_thickness(part):
    """The chamfer is a 1mm bevel, not a taper down the whole wall."""
    for sx in (-1, 1):
        assert inside(part, [sx * 14.9, 0.0, MID])[0]
        for sy in (-1, 1):
            assert inside(part, [sx * 12.5, sy * 26.4, MID])[0]


def test_the_horns_survive_the_chamfer(part):
    """A half-space cutter aimed at one horn's inner face can swallow another."""
    for sx in (-1, 1):
        for sy in (-1, 1):
            assert inside(part, [sx * 12.5, sy * 23.0, MID])[0]


def test_a_chamfer_thicker_than_half_the_body_is_rejected():
    err = render_failure("down_indicator.scad", edgeCham=4.0)
    assert "under half the" in err and "body thickness" in err


def test_a_chamfer_thicker_than_half_a_horn_is_rejected():
    err = render_failure("down_indicator.scad", edgeCham=3.0)
    assert "under half the" in err and "horn thickness" in err


def test_the_chamfer_can_be_switched_off(part):
    square = render("down_indicator.scad", edgeCham=0)
    assert square.is_watertight
    assert square.body_count == 1
    assert square.volume > part.volume
    assert inside(square, [14.9, 0.0, 0.3])[0], "wall should be square at z=0.3"


def test_a_chamfer_that_would_eat_the_horns_is_rejected():
    """Past hornThk/2 the horn polygon self-intersects and the lugs vanish."""
    err = render_failure("down_indicator.scad", tipChamfer=2.5)
    assert "tip chamfer" in err


def test_a_cord_too_fat_for_the_body_is_rejected():
    # A 10mm cord in a 6.7mm body would leave 1.7mm of floor.
    err = render_failure("down_indicator.scad", cordDia=10.0)
    assert "floor under the cord trough" in err


def test_a_thinner_body_still_builds_with_a_thinner_floor():
    thin = render("down_indicator.scad", bodyT=6.0)
    assert thin.is_watertight
    assert thin.body_count == 1
    assert thin.bounds[1][2] == approx(6.0, abs=1e-6)
    # 2.5mm of floor, still above the 2.0mm minimum
    assert inside(thin, [9.0, HOLE_Y, 1.25])[0]
    assert not inside(thin, [9.0, HOLE_Y, 5.7])[0]
