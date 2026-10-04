# Finger-Loop Down Indicator — OpenSCAD model

A wrist-worn body that anchors a bungee cord looping over the back of the hand
and around a finger. Which finger the loop sits on is the down.

Design and reasoning: [../2026-08-24-finger-loop-indicator-design.md](../2026-08-24-finger-loop-indicator-design.md).

## Build

    make stl      # -> build/down_indicator_string.stl
    make test     # render the model and assert against the mesh
    make clean

`make` creates `.venv` on first use and installs the pinned dependencies from
`requirements.txt`.

Tools: OpenSCAD 2021.01, GNU Make, and for `make test` Python 3.12 or newer
with `venv`. The fonts are vendored. The full list is in
[the repository README](../README.md#what-you-need-to-build).

## Parameters

Every parameter is declared at the top of `down_indicator_string.scad` and can be
overridden without editing the file:

    openscad -o build/wide.stl -D bandWidth=18 down_indicator_string.scad

| Parameter | Default | Notes |
| --- | --- | --- |
| `bodyLen` | 40.0 | Along the forearm |
| `bodyWid` | 30.0 | Across the wrist |
| `bodyT` | 6.7 | Sets the trough floor: `bodyT - (troughDia/2 + troughOffset)`, 4.45mm at defaults, min 2.0mm |
| `edgeCham` | 1.0 | 45° bevel where each outer wall meets a face; 0 disables |
| `cordDia` | 7.0 | Through-hole diameter. The troughs are sized separately |
| `holeY` | 6.0 | Hole centres at `(0, +holeY)` and `(0, -holeY)` |
| `troughDia` | 2.5 | Surface trough diameter; independent of `cordDia` |
| `troughOffset` | 1 | Trough axis off its face: positive sinks it into the body for a groove deeper than a half-round, negative lifts it out for a shallower one, 0 puts the axis on the face |
| `bandWidth` | 20.0 | 18 if the 4.9mm horns prove marginal |
| `bandClear` | 0.2 | Added to `bandWidth` for the lug gap |
| `barStandoff` | 4.5 | |
| `tipMargin` | 2.0 | |
| `barHoleDia` | 1.1 | |
| `tipChamfer` | 0.5 | Must stay under half the horn thickness (2.45mm at defaults) |
| `teardropDown` | true | Apex toward the wrist side, for a face-down print |
| `logoEnable` | true | Cuts the RefGear wordmark into both faces |
| `logoWidth` | 26.0 | Along the forearm; the mark stands a shade over 5:1 |
| `logoDepth` | 0.5 | Recessed into each face |
| `logoX` | -8.75 | Centre across the wrist; must be negative (see below) |
| `logoY` | 0.0 | Centre along the forearm |

Eight combinations are rejected outright rather than silently producing an
unbuildable part: less than 2.0mm of floor under a cord trough, a trough
offset that stops the trough being an open groove, horns thinner than 4.0mm,
holes or troughs that break out of the end, less than 2.0mm of wall between
the two cord holes, an edge chamfer at or past half the body thickness, an
edge chamfer at or past half the horn thickness, and a tip chamfer at or past
half the horn thickness. Two of these would otherwise render without an
error: merged holes sever the slab into two pieces, and an oversized tip
chamfer self-intersects the horn polygon and deletes all four lugs.

Five more guard the logo: a mark on the wrong side of the centre line, one
that reaches the cord holes, one past the side chamfer, one that runs off the
body end, and a pair of recesses leaving under 2.0mm of web between them.

The mark reads along the forearm, so it runs *alongside* the cord holes rather
than past them and cannot be centred across the wrist. Which side is not a
free choice: the watch-face troughs run out to +X and the wrist-side ones to
-X, so the mark belongs on -X, and mirroring the wrist copy -- which it needs
anyway to read the right way round on that face -- lands it on +X, clear of
its own troughs. One offset serves both faces, and `logoX` is asserted
negative because the positive mirror image of that arrangement lays each mark
straight across its own trough run.

## Fonts

The wordmark is built from `text()` against the two static Archivo faces
vendored in `fonts/`, under the SIL Open Font License (`fonts/OFL.txt`).
Neither the checkout nor the build needs Archivo installed system-wide, but
`FONTCONFIG_FILE` must point at `fonts/fonts.conf` -- the Makefile and the
test suite both set it, so `make stl`, `make test` and a bare `pytest` all
work unassisted. Invoking `openscad` by hand needs it set:

    FONTCONFIG_FILE=fonts/fonts.conf openscad -o build/x.stl down_indicator_string.scad

Three things make that indirection load-bearing rather than tidy. OpenSCAD
resolves faces only through fontconfig and ignores its own library font
directory; a face it cannot resolve is quietly substituted rather than
refused, so a missing font is a silent visual defect and not an error; and its
SVG reader drops `<text>` elements outright, so `refgear-logo.svg` cannot be
imported and imports as the bare underline alone. A *variable* Archivo is no
help either -- OpenSCAD honours no weight axis, rendering Black and Regular
identically and flattening the 900/400 contrast the mark is built on. Hence
two static files.

The tests render with the `openscad` CLI and assert against the resulting
mesh. The exact-volume assertions were verified against **OpenSCAD 2021.01**;
a different release may triangulate curved surfaces differently and shift
those figures within their stated tolerances.

## Hardware

As the owner uses it, confirmed 2026-10-03:

| | |
| --- | --- |
| Cord | 1/8" (3.2mm) bungee cord |
| Strap | 24mm-wide Velcro strap, though any suitable strap that fits would do |

The lugs as modelled take a 20mm band (`bandWidth` 20.0, a 20.2mm gap), which
is narrower than that strap. The model has not been changed to match:
`bandWidth = 24` leaves 2.9mm horns on the 30mm body, and the 4.0mm horn guard
rejects it. How the 24mm strap is fitted is not recorded.

## Print

Face down — the `z = bodyT` face on the bed. That puts strap tension along the
layers and makes the teardrop bores self-supporting.
