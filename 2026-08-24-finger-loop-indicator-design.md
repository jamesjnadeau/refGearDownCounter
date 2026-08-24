# Finger-Loop Down Indicator — Design

Status: **specified** 2026-08-24, not yet built
Scope: a wrist-worn body, modelled in OpenSCAD, that anchors a bungee cord
looping over the back of the hand and around a finger. Which finger the loop
sits on is the down.

## What this is, and what it is not

This is a **third** device in the family, and it shares geometry with neither
of the others by default:

- The **mechanical slider down counter** — Onshape, three printed parts, a
  knob indexing between four stations. See [README.md](README.md).
- The **electronic Watchy ref counter** — a separate repository,
  [watchy-ref-counter](https://github.com/jamesjnadeau/watchy-ref-counter).

The one thing carried across deliberately is the **spring-bar lug geometry**
from [the lugs spec](2026-08-22-band-lugs-design.md), because it is proven and
because a common band across the two devices is worth having. Every figure
imported is named in [Lugs](#lugs) with its source. Nothing else crosses over
— in particular the down counter's 79 x 34mm footprint does **not** apply
here, and importing it would repeat the error that spec was written to correct.

## Prior art

The commercial equivalent is a referee's down-indicator wristband: an elastic
band with a loop the wearer moves between fingers. This design replaces the
band-and-loop with a rigid body on a watch strap and a bungee loop, so the
device can share a strap with the mechanical counter.

## Where the work happens

**In this repository**, unlike the down counter. The model is OpenSCAD source
under `down-indicator/`, version-controlled, with a `pytest` + `trimesh` suite
that renders the model and asserts against the resulting mesh. No Onshape
document is involved, and none of the Onshape constraints recorded in
[AGENTS.md](AGENTS.md) apply.

## Coordinates

| Axis | Direction | Extent |
| --- | --- | --- |
| +X | across the wrist | −15 to +15 |
| +Y | along the forearm, toward the hand | −20 to +20 (body), ±26.5 with lugs |
| +Z | out of the watch face | 0 (wrist side) to 6.7 (face) |

The wrist side is z = 0 throughout. "Underside" in the lugs spec's sense means
−Z here too, so `teardropDown` keeps its original meaning.

## Geometry

### Body

A plain rectangular slab. Square in plan, no corner radius.

| Dimension | Value |
| --- | --- |
| Length, along the forearm | 40.0mm |
| Width, across the wrist | 30.0mm |
| Thickness | 6.7mm |
| Volume, blank | 8040.0mm³ |

**Square corners, not rounded.** The lug horns run flush to the side walls at
x = ±15, exactly as the down counter's do. A corner radius at the ±Y ends
would root the horns into the radius rather than into solid end material —
the failure the lugs spec diagnosed and fixed by squaring the corners. The
`cornerR` question does not arise: there is no such parameter.

### Cord holes

Two through-bores, on the Y centreline, symmetric about the origin.

| Quantity | Value |
| --- | --- |
| Diameter | 7.0mm |
| Centres | (0, +10) and (0, −10) |
| Wall, hole edge to body end | 6.5mm |
| Wall, between the two holes | 13.0mm |
| Volume removed | 515.32mm³ |

### Cord slots

From each hole, a trough of the **same 7.0mm diameter** runs outward along Y
to the body end: one cut into the watch face (axis at z = 6.7), one cut into
the wrist side (axis at z = 0). The +Y hole's pair runs to the +Y end, the −Y
hole's to the −Y end.

Because the body is **thinner than the trough diameter**, the two troughs
overlap at mid-thickness and the slot is open end to end. The cord is pressed
in from the side rather than threaded.

The narrowest point is at z = t/2, and its width follows from the geometry:

```
neck = 2 * sqrt(r² − (t/2)²)
     = 2 * sqrt(3.5² − 3.35²)
     = 2.027mm
```

| Quantity | Value |
| --- | --- |
| Slot width at either face | 7.0mm |
| Neck width at mid-thickness | 2.027mm |
| Volume removed, holes and troughs together | 1050.79mm³ |

**6.7mm is derived, not chosen.** It is the thickness that yields a ~2mm neck
at a 7mm trough. A 3mm bungee presses past a 2mm neck with a squeeze and does
not fall back out under its own weight. The relationship is one line of
arithmetic in the model and is asserted, so changing `bodyT` or `cordDia`
reports the resulting neck rather than silently producing a part that either
will not accept the cord or will not hold it.

At 7.0mm exactly the troughs would meet along a knife edge and the slot would
have zero width — the model asserts `bodyT < cordDia` to rule that out.

### Lugs

Carried over from [the lugs spec](2026-08-22-band-lugs-design.md) as built,
with two figures re-derived because the end is 30mm wide here rather than
34mm.

| Dimension | Value | Source |
| --- | --- | --- |
| Band width | 20mm | Lugs spec, as built |
| Lug gap, inner face to inner face | 20.2mm | Lugs spec, as built |
| Horn thickness, each | **4.9mm** | **Re-derived**: (30 − 20.2) / 2 |
| Horn protrusion | 6.5mm | Lugs spec: standoff 4.5 + tip margin 2.0 |
| Bar standoff | 4.5mm | Lugs spec, as built |
| Spring-bar bore | 1.1mm, through, teardrop | Lugs spec, as built |
| Teardrop apex | Toward −Z | Lugs spec, as built |
| Tip chamfer | 0.5mm | Lugs spec, as built |
| Horn height | **6.7mm** | **Re-derived**: full body thickness |
| Lug-to-lug | **53.0mm** | **Re-derived**: 40 + 2 × 6.5 |

**The horns are 4.9mm thick, against 6.9mm on the down counter.** A 30mm end
minus a 20.2mm gap leaves less material per horn than a 34mm end does. 4.9mm
is still more than twice the down counter's 2.0mm wall and the bore leaves
5.6mm of material across the horn's height, but it is the thinnest structure
in this part and the one the print test should load first. `bandWidth = 18`
restores 5.9mm horns if it proves marginal; the model asserts horn thickness
stays at or above 4.0mm, so `bandWidth = 24` is rejected outright.

**53.0mm lug-to-lug** sits inside the 48–56mm span of a large watch, which the
79mm down counter could never reach. Orientation is not in question here: the
40mm axis runs along the forearm and the lugs sit on the 30mm ends.

### Slot and lug interaction

The slot exits the end face at x ∈ [−3.5, +3.5]; the lug gap spans
x ∈ [−10.1, +10.1]. The slot therefore emerges **inside the band gap**, with
6.6mm of clearance to each horn. It does not touch the horns or the bores.

It does, however, emerge directly beneath the spring bar and the strap. See
[Open questions](#open-questions).

## Print

Printed flat, **face down** — the z = 6.7 face on the bed. This matches the
down counter's orientation, puts strap tension along the layers rather than
across them, and makes the teardrop bores self-supporting with their apex
toward −Z, i.e. upward on the bed.

One consequence is unavoidable and worth stating plainly: the part is
symmetric in Z, so of the two troughs, whichever faces the bed prints as an
unsupported 7mm arch and whichever faces up prints as a clean valley.
Flipping the part swaps which is which. The arch's apex is the neck, so sag
there narrows the neck rather than closing the slot — the failure mode is a
cord that is hard to insert, not a part that is scrap. Measure the neck on the
first print before deciding whether a self-supporting slot profile is needed.

## Verification

The model is checked by rendering it to STL and asserting against the mesh:
watertight, a single body, exact bounding box, exact volume at each build
stage, and point-containment probes proving the slot is open along its whole
run, the neck is the width the arithmetic predicts, the holes go through, the
band gap is clear, and the bores run through the horns with the teardrop apex
on the −Z side.

Software cannot confirm the 4.9mm horns survive a wrist, or that a 2.027mm
neck holds a real bungee. Both need the print test.

## Open questions

**The cord exits under the strap.** Both slots emerge in the band gap, so the
cord is pinned beneath the spring bar and the strap. That may be tidy — it
keeps the cord from flapping — or it may chafe and bind. Confirm on the first
print. If it binds, the fix is to move the holes off the Y centreline so the
slots exit a side edge instead, which is a change to `holeY` plus a slot
direction, not a redesign.

**Neck retention is untested against a real bungee.** 2.027mm is an
arithmetic target, not a measured one. Print a slot coupon before a full body.

**No comfort chamfer.** The wrist-side face is a square-edged 30 x 40mm slab.
A perimeter chamfer or fillet is deliberately deferred: it interacts with the
horn roots, and adding it before the print test would complicate the volume
assertions for a change that may want to be a fillet rather than a chamfer.

## Licence

OCL v1.1, as with everything in this repository. See [LICENSE](LICENSE).
