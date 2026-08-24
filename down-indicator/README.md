# Finger-Loop Down Indicator — OpenSCAD model

A wrist-worn body that anchors a bungee cord looping over the back of the hand
and around a finger. Which finger the loop sits on is the down.

Design and reasoning: [../2026-08-24-finger-loop-indicator-design.md](../2026-08-24-finger-loop-indicator-design.md).

## Build

    make stl      # -> build/down_indicator.stl
    make test     # render the model and assert against the mesh
    make clean

`make` creates `.venv` on first use and installs the pinned dependencies from
`requirements.txt`.

## Parameters

Every parameter is declared at the top of `down_indicator.scad` and can be
overridden without editing the file:

    openscad -o build/wide.stl -D bandWidth=18 down_indicator.scad

| Parameter | Default | Notes |
| --- | --- | --- |
| `bodyLen` | 40.0 | Along the forearm |
| `bodyWid` | 30.0 | Across the wrist |
| `bodyT` | 6.7 | Must be less than `cordDia`, or the slots never open |
| `cordDia` | 7.0 | Hole and trough diameter |
| `holeY` | 10.0 | Hole centres |
| `bandWidth` | 20.0 | 18 if the 4.9mm horns prove marginal |
| `barStandoff` | 4.5 | |
| `tipMargin` | 2.0 | |
| `barHoleDia` | 1.1 | |
| `tipChamfer` | 0.5 | |
| `teardropDown` | true | Apex toward the wrist side, for a face-down print |

Four combinations are rejected outright rather than silently producing an
unbuildable part: a body at or thicker than the cord diameter, a cord neck
outside 1.2–3.5mm, horns thinner than 4.0mm, and holes that break out of the
end.

## Print

Face down — the `z = bodyT` face on the bed. That puts strap tension along the
layers and makes the teardrop bores self-supporting.
