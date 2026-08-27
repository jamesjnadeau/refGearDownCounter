"""The RefGear wordmark, debossed into the watch face and the wrist face.

The mark is REF in Archivo Black butted against GEAR in Archivo Regular over a
full-width rule, the proportions taken from refgear-logo.svg. That SVG cannot
be imported directly -- OpenSCAD's SVG reader drops <text> outright, and its
variable-font support is nil, so the 900/400 weight contrast that is the whole
identity of the mark only survives via the two static faces vendored in fonts/.

Turned a quarter-turn clockwise, the mark reads down the forearm and so has to
run alongside the cord holes rather than past them. That forces it off centre:
the watch-face troughs run out to +X, leaving the -X side clear, and mirroring
the wrist copy lands it on +X, which is the side its own troughs leave free.
One offset therefore clears both faces, and `test_the_mark_keeps_off_the_cord
_troughs` is what pins that down.

The tests probe a grid rather than named glyph coordinates: what matters is
that ink is cut to depth, that unbroken material remains beneath it, and that
the mark reads the right way round on each face. Pinning exact letter
positions would only re-assert the font's own metrics.
"""

import numpy as np

from conftest import inside

BODY_T = 6.7
LOGO_LEN = 26.0     # along the forearm, once turned
LOGO_DEPTH = 0.5
LOGO_X = -8.75      # centre across the wrist, on the watch face
LOGO_Y = 0.0

# The turned mark stands about 4.9mm across X, so a 3.0mm band centred on it
# stays inside the ink at both ends.
BAND = 3.0
NX, NY = 12, 160


def _mask(logo, z, face=1):
    """Which of a grid over the mark's footprint at `z` is cut away.

    Rows run across the mark (X), columns along it (Y). `face` is +1 for the
    watch-face copy and -1 for the mirrored wrist one, so the two grids are
    reflections of each other and their masks are directly comparable.
    """
    cx = LOGO_X * face
    xs = np.linspace(cx - BAND / 2, cx + BAND / 2, NX)
    ys = np.linspace(LOGO_Y - LOGO_LEN / 2 * 0.98, LOGO_Y + LOGO_LEN / 2 * 0.98, NY)
    points = [[x, y, z] for x in xs for y in ys]
    return ~inside(logo, *points).reshape(len(xs), len(ys))


def _grid(z, face=1):
    cx = LOGO_X * face
    xs = np.linspace(cx - BAND / 2, cx + BAND / 2, NX)
    ys = np.linspace(LOGO_Y - LOGO_LEN / 2 * 0.98, LOGO_Y + LOGO_LEN / 2 * 0.98, NY)
    return [[x, y, z] for x in xs for y in ys]


def test_the_wordmark_is_cut_into_the_watch_face(logo):
    """Some of the band is ink and some is the space between letters."""
    cut = _mask(logo, BODY_T - LOGO_DEPTH / 2).mean()
    assert 0.15 < cut < 0.75, f"{cut:.0%} of the band was cut away"


def test_the_wordmark_is_cut_into_the_wrist_face_too(logo):
    cut = _mask(logo, LOGO_DEPTH / 2, face=-1).mean()
    assert 0.15 < cut < 0.75, f"{cut:.0%} of the band was cut away"


def test_the_recess_does_not_eat_into_the_body(logo):
    """Under the deepest ink the slab is still unbroken, both ways up."""
    for z, face in ((BODY_T - LOGO_DEPTH - 0.25, 1), (LOGO_DEPTH + 0.25, -1)):
        assert inside(logo, *_grid(z, face)).all(), f"material missing at z={z}"


def test_the_mark_reads_the_right_way_round_on_each_face(logo):
    """The wrist copy is mirrored, not shown through the body reversed.

    REFGEAR has no symmetry across the axis it is mirrored in, so cutting the
    same unmirrored plate into both faces would leave the two masks equal
    instead of reflected.
    """
    face = _mask(logo, BODY_T - LOGO_DEPTH / 2)
    wrist = _mask(logo, LOGO_DEPTH / 2, face=-1)
    assert (wrist == np.flip(face, axis=0)).mean() > 0.98


def test_the_mark_keeps_off_the_cord_troughs(part):
    """Each face's mark sits on the side its own trough run leaves free.

    The watch-face troughs leave 0..+16mm in X; the wrist ones leave 0..-16mm.
    Probing along each trough's axis, just under its face, finds the channel
    open where the trough runs and solid where the mark is.
    """
    for sign, z in ((1, BODY_T - 0.2), (-1, 0.2)):
        # a point out along the trough, and the mark's own centre line
        assert not inside(part, [sign * 8.0, 6.0, z])[0]
        assert inside(part, [sign * 8.0, 16.0, z])[0]


def test_the_wordmark_survives_the_assembly(part):
    """The mark reaches the finished part, not just the bare slab."""
    for z, face in ((BODY_T - LOGO_DEPTH / 2, 1), (LOGO_DEPTH / 2, -1)):
        cut = (~inside(part, *_grid(z, face))).mean()
        assert 0.15 < cut < 0.75, f"{cut:.0%} cut away at z = {z}"


def test_a_mark_reaching_the_cord_holes_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoX=-2.0)
    assert "cord" in complaint.lower()


def test_a_mark_on_the_trough_side_is_rejected():
    """Positive logoX would lay the watch-face mark across its own troughs."""
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoX=8.75)
    assert "trough" in complaint.lower()


def test_a_mark_that_overruns_the_side_wall_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoX=-13.0)
    assert "chamfer" in complaint.lower()


def test_a_mark_too_long_for_the_body_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoWidth=40.0)
    assert "body end" in complaint.lower()


def test_a_mark_deep_enough_to_meet_its_twin_is_rejected():
    from conftest import render_failure

    complaint = render_failure("down_indicator_string.scad", logoDepth=3.0)
    assert "web" in complaint.lower()
