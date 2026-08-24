"""The bare slab: 30mm across the wrist, 40mm along the forearm, 6.7mm thick."""

from pytest import approx


def test_blank_is_one_closed_solid(blank):
    assert blank.is_watertight
    assert blank.is_winding_consistent
    assert blank.body_count == 1


def test_blank_bounding_box(blank):
    low, high = blank.bounds
    assert list(low) == approx([-15.0, -20.0, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 20.0, 6.7], abs=1e-6)


def test_blank_volume_is_the_full_prism(blank):
    assert blank.volume == approx(30.0 * 40.0 * 6.7, rel=1e-9)


def test_blank_sits_on_the_bed_and_is_solid_through(blank):
    from conftest import inside

    assert inside(blank, [0, 0, 0.1], [0, 0, 3.35], [0, 0, 6.6]).all()
    assert not inside(blank, [0, 0, -0.1], [0, 0, 6.8]).any()
