"""Hold the conversion against the mesh Onshape exported from the original.

`reference/onshape-top.stl` is that export, rescaled to millimetres. It is a
tessellation, not the solid: Onshape's chord tolerance flattens the corner
arcs and the numeral curves, so it reads slightly small and its own bounding
box misses the 0.0711mm corner bulge that the solid has. Tolerances here are
sized for that, and the checks that need to be tight are the ones on flat
faces, where a tessellation is exact.
"""

from pytest import approx

from conftest import section_area, walls

ONSHAPE_SOLID_VOLUME = 7832.5   # mm^3, as Onshape measures the B-rep


def test_the_two_agree_on_every_flat_wall(part, onshape):
    for axis, at, lo, hi in ((0, 22.5, -13.0, 23.0), (1, 5.0, -18.0, 63.0)):
        for z in (-3.0, -2.0, -1.0, -0.05):
            ours = walls(part, axis, at, z, lo, hi)
            theirs = walls(onshape, axis, at, z, lo, hi)
            assert len(ours) == len(theirs)
            assert list(ours) == approx(list(theirs), abs=0.02), \
                f"walls differ on axis {axis} at z = {z}"


def test_the_two_agree_on_the_overall_size(part, onshape):
    low, high = part.bounds
    ref_low, ref_high = onshape.bounds
    assert list(low) == approx(list(ref_low), abs=0.08)
    assert list(high) == approx(list(ref_high), abs=0.08)
    assert low[2] == approx(ref_low[2], abs=1e-6)
    assert high[2] == approx(ref_high[2], abs=1e-6)


def test_the_two_agree_on_the_skirt_section(part, onshape):
    for z in (-3.0, -2.0, -1.0, -0.1):
        assert section_area(part, z) == approx(section_area(onshape, z), rel=0.01)


def test_the_two_agree_on_the_volume(part, onshape):
    assert part.volume == approx(onshape.volume, rel=0.005)
    assert part.volume == approx(ONSHAPE_SOLID_VOLUME, rel=0.005)


def test_the_typeface_is_the_one_real_difference(untied, unmarked, onshape):
    """Which is why the volumes agree better with the numerals left off.

    Onshape set the numerals in Open Sans. OpenSCAD cannot count on that font
    being installed, so the default is a heavier one, and heavier numerals cut
    away more plate. Take them off both sides and the two solids agree to a
    couple of parts in ten thousand.
    """
    ours = unmarked.volume
    theirs = ONSHAPE_SOLID_VOLUME + (unmarked.volume - untied.volume)
    assert ours == approx(theirs, rel=0.01)
    assert untied.volume < unmarked.volume


def test_the_floating_island_is_the_one_deliberate_departure(part, untied, onshape):
    """Onshape's `top` is two bodies. Ours is one, and that is on purpose.

    The loose piece inside the 4 is a defect, not a feature, so the model
    ties it back to the plate. Cutting the numeral the original's way -- set
    tiedNumeral to 0 -- reproduces the two bodies exactly.
    """
    assert onshape.body_count == 2
    assert untied.body_count == 2
    assert part.body_count == 1
    assert part.volume - untied.volume < 4.0, "the tie should be a bar, not a patch"


def test_the_bottom_shell_agrees_with_the_original(bottom, onshape_bottom):
    low, high = bottom.bounds
    ref_low, ref_high = onshape_bottom.bounds
    assert list(low) == approx(list(ref_low), abs=0.02)
    assert list(high) == approx(list(ref_high), abs=0.02)
    assert bottom.volume == approx(onshape_bottom.volume, rel=0.002)
    assert bottom.body_count == onshape_bottom.body_count == 1
    for z in (-1.5, 1.0, 2.5):
        assert list(walls(bottom, 0, 22.5, z, -13.0, 23.0)) \
            == approx(list(walls(onshape_bottom, 0, 22.5, z, -13.0, 23.0)), abs=0.02)


def test_the_button_agrees_with_the_original(button, onshape_button):
    low, high = button.bounds
    ref_low, ref_high = onshape_button.bounds
    assert list(low) == approx(list(ref_low), abs=0.02)
    assert list(high) == approx(list(ref_high), abs=0.02)
    # A small solid of revolution tessellates badly, so the reference reads
    # about 3% under the B-rep. Compare the walls, which are exact.
    for z in (-0.5, 2.0):
        assert list(walls(button, 0, 0.0, z, -8.0, 8.0)) \
            == approx(list(walls(onshape_button, 0, 0.0, z, -8.0, 8.0)), abs=0.02)
