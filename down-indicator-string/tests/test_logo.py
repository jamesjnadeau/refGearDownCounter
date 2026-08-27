"""The RefGear wordmark, debossed into the watch face and the wrist face.

The mark is REF in Archivo Black butted against GEAR in Archivo Regular over a
full-width rule, the proportions taken from refgear-logo.svg. That SVG cannot
be imported directly -- OpenSCAD's SVG reader drops <text> outright, and its
variable-font support is nil, so the 900/400 weight contrast that is the whole
identity of the mark only survives via the two static faces vendored in fonts/.

The tests below probe a grid rather than named glyph coordinates: what matters
is that ink is cut to depth, that unbroken material remains beneath it, and
that the mark reads the right way round on each face. Pinning exact letter
positions would only re-assert the font's own metrics.
"""

import numpy as np

from conftest import inside

BODY_T = 6.7
LOGO_WIDTH = 26.0
LOGO_DEPTH = 0.5
LOGO_Y = -14.25

# The mark's block is a shade over five to one, so at 26mm wide it stands about
# 5.1mm tall; a 4.0mm band centred on LOGO_Y stays well inside the ink.
BAND_H = 4.0


NX, NY = 160, 12


def _mask(logo, z):
    """Which of a grid spanning the mark's footprint at `z` is cut away.

    Rows run along Y, columns along X, and the columns are symmetric about
    x = 0, so a left-for-right flip of one face's mask is comparable with the
    other's.
    """
    xs = np.linspace(-LOGO_WIDTH / 2 * 0.98, LOGO_WIDTH / 2 * 0.98, NX)
    ys = np.linspace(LOGO_Y - BAND_H / 2, LOGO_Y + BAND_H / 2, NY)
    points = [[x, y, z] for y in ys for x in xs]
    return ~inside(logo, *points).reshape(len(ys), len(xs))


def _grid(z):
    xs = np.linspace(-LOGO_WIDTH / 2 * 0.98, LOGO_WIDTH / 2 * 0.98, NX)
    ys = np.linspace(LOGO_Y - BAND_H / 2, LOGO_Y + BAND_H / 2, NY)
    return [[x, y, z] for y in ys for x in xs]


def test_the_wordmark_is_cut_into_the_watch_face(logo):
    """Some of the band is ink and some is the space between letters."""
    cut = _mask(logo, BODY_T - LOGO_DEPTH / 2).mean()
    assert 0.15 < cut < 0.75, f"{cut:.0%} of the band was cut away"


def test_the_wordmark_is_cut_into_the_wrist_face_too(logo):
    cut = _mask(logo, LOGO_DEPTH / 2).mean()
    assert 0.15 < cut < 0.75, f"{cut:.0%} of the band was cut away"


def test_the_recess_does_not_eat_into_the_body(logo):
    """Under the deepest ink the slab is still unbroken, both ways up."""
    for z in (BODY_T - LOGO_DEPTH - 0.25, LOGO_DEPTH + 0.25):
        assert inside(logo, *_grid(z)).all(), f"material missing at z = {z}"


def test_the_mark_reads_the_right_way_round_on_each_face(logo):
    """The wrist copy is mirrored, not shown through the body reversed.

    REFGEAR has no left-right symmetry, so cutting the same unmirrored plate
    into both faces would leave the two masks equal instead of reflected.
    """
    face = _mask(logo, BODY_T - LOGO_DEPTH / 2)
    wrist = _mask(logo, LOGO_DEPTH / 2)
    assert (wrist == np.fliplr(face)).mean() > 0.98


def test_the_wordmark_survives_the_assembly(part):
    """The mark reaches the finished part, not just the bare slab."""
    for z in (BODY_T - LOGO_DEPTH / 2, LOGO_DEPTH / 2):
        cut = (~inside(part, *_grid(z))).mean()
        assert 0.15 < cut < 0.75, f"{cut:.0%} cut away at z = {z}"


def test_a_logo_that_reaches_the_cord_holes_is_rejected():
    """Either end, so the clearance is measured from the centre line."""
    from conftest import render_failure

    for y in (8.0, -8.0):
        complaint = render_failure("down_indicator_string.scad", logoY=y)
        assert "cord" in complaint.lower()


def test_a_logo_that_runs_off_either_end_is_rejected():
    from conftest import render_failure

    for y in (17.5, -17.5):
        complaint = render_failure("down_indicator_string.scad", logoY=y)
        assert "body end" in complaint.lower()


def test_a_logo_wider_than_the_face_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoWidth=29.5)
    assert "logo" in complaint.lower()


def test_a_logo_deep_enough_to_meet_its_twin_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoDepth=3.0)
    assert "logo" in complaint.lower()
