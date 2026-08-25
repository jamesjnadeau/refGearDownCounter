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

## Parameters

Every parameter is declared at the top of `down_indicator_string.scad` and can be
overridden without editing the file:

    openscad -o build/wide.stl -D bandWidth=18 down_indicator_string.scad

| Parameter | Default | Notes |
| --- | --- | --- |
| `bodyLen` | 40.0 | Along the forearm |
| `bodyWid` | 30.0 | Across the wrist |
| `bodyT` | 6.7 | Sets the trough floor: `bodyT - cordDia/2`, min 2.0mm |
| `edgeCham` | 1.0 | 45° bevel where each outer wall meets a face; 0 disables |
| `cordDia` | 7.0 | Hole and trough diameter; deeper troughs thin the floor |
| `holeY` | 10.0 | Hole centres |
| `bandWidth` | 20.0 | 18 if the 4.9mm horns prove marginal |
| `bandClear` | 0.2 | Added to `bandWidth` for the lug gap |
| `barStandoff` | 4.5 | |
| `tipMargin` | 2.0 | |
| `barHoleDia` | 1.1 | |
| `tipChamfer` | 0.5 | Must stay under half the horn thickness (2.45mm at defaults) |
| `teardropDown` | true | Apex toward the wrist side, for a face-down print |

Seven combinations are rejected outright rather than silently producing an
unbuildable part: a body at or thicker than the cord diameter, a cord neck
outside 1.2–3.5mm, horns thinner than 4.0mm, holes that break out of the
end, less than 2.0mm of wall between the two cord holes, and a tip chamfer at
or past half the horn thickness. The last two would otherwise render without
an error: merged holes sever the slab into two pieces, and an oversized
chamfer self-intersects the horn polygon and deletes all four lugs.

The tests render with the `openscad` CLI and assert against the resulting
mesh. The exact-volume assertions were verified against **OpenSCAD 2021.01**;
a different release may triangulate curved surfaces differently and shift
those figures within their stated tolerances.

## Print

Face down — the `z = bodyT` face on the bed. That puts strap tension along the
layers and makes the teardrop bores self-supporting.
