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
under `down-indicator-string/`, version-controlled, with a `pytest` + `trimesh` suite
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

### Edge chamfers

Every outer wall that a wearer can touch is bevelled **1.0mm at 45°** where it
meets each face: both side walls, all four horn tip faces, and the two body
end faces at the base of the band gap. The part is 6.7mm of hard plastic
against a wrist, and the long side walls are the edges that press into it.

| Quantity | Value |
| --- | --- |
| Chamfer | 1.0mm at 45° |
| Walls chamfered | side walls, horn tips, band-gap base |
| Walls left square | horn interiors, holes, channels, bores |
| Volume removed | 147.69mm³ |
| Full-thickness wall remaining | 4.7mm |
| Band gap, every height | 20.2mm |

The chamfers are **exact half-spaces, not swept surfaces.** Every outer wall
here is straight and every outer solid is a straight extrusion from z = 0 to
z = 6.7, so the material to remove at a wall with outward normal n at distance
d is simply {p·n − z > d − cham}, mirrored about z = t/2 for the other face.
No stepped approximation is involved and nothing is rounded.

**The horns' inner faces are deliberately left square.** They are what the
strap bears against, and the gap is sized to the strap — 20.2mm for a 20mm
band. Bevelling them would open the gap to 22.2mm at each face while leaving
20.2mm in the middle, so the strap would sit loose top and bottom and rock in
its own slot. They keep their full 6.7mm height.

The body end faces *at the base* of the gap are chamfered, because nothing
bears on them; they only need to not be sharp. That half-space faces inward
and would run on through the horns, so it is the one cutter here that is
bounded — clipped to the gap width.

The cord holes, the cord channels and the spring-bar bores are **not**
chamfered either. They are functional surfaces, and the cord and the bar want
the full section.

`edgeCham = 0` removes the chamfers and returns the square-edged part.

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

From each hole, a trough of the **same 7.0mm diameter** runs out to a side
edge — but the two troughs of a hole run to **opposite** edges. The watch-face
trough (axis at z = 6.7) runs to +X; the wrist-side trough (axis at z = 0)
runs to −X. Both holes share the same handedness, so the two face channels are
parallel and the two wrist channels are parallel.

That opposition is the whole design. A strand entering the face channel drops
through the hole and turns into the wrist channel heading the other way, so it
makes **two right-angle bends inside the body**. The bends are the retention:
the cord is held by the shape of its own path, not by a knot and not by a
pinch fit.

| Quantity | Value |
| --- | --- |
| Trough width at its own face | 7.0mm |
| Trough depth | 3.5mm |
| Floor left under each trough | 3.2mm |
| Run, hole centre to side edge | 15.0mm |
| Volume removed, holes and troughs together | 1440.61mm³ |

**The cord is threaded, not pressed in.** Away from the hole the two channels
sit on opposite sides of the body and never meet, so there is no open slot
along either run — the only full-thickness opening is the hole itself. This is
the deliberate consequence of the opposed routing, and the test suite pins it
down directly rather than leaving it to be inferred.

**6.7mm is a free choice, not a derived one.** An earlier revision of this
spec ran both of a hole's troughs to the same end, which made them overlap at
mid-thickness into a pressed-in slot, and 6.7mm was the thickness that gave
that slot a ~2mm neck. With opposed routing there is no neck, and the binding
constraint is instead the **floor under each trough**: `bodyT − cordDia/2`,
which the model asserts stays at or above 2.0mm. At the defaults that floor is
3.2mm.

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

### Trough and lug interaction

The troughs run in X at y = ±10, spanning y ∈ [6.5, 13.5] and [−13.5, −6.5].
The horns begin at y = 19.5. The two never meet in Y, so the troughs exit the
side walls in clear material with 6mm to spare and touch neither the horns nor
the bores.

This is the payoff of routing to the sides rather than the ends: the cord
leaves the body well clear of the strap, so nothing is pinned under the spring
bar.

## Print

Printed flat, **face down** — the z = 6.7 face on the bed. This matches the
down counter's orientation, puts strap tension along the layers rather than
across them, and makes the teardrop bores self-supporting with their apex
toward −Z, i.e. upward on the bed.

One consequence is unavoidable and worth stating plainly: the part is
symmetric in Z, so of the two troughs, whichever faces the bed prints as an
unsupported 7mm arch and whichever faces up prints as a clean valley.
Flipping the part swaps which is which — there is no orientation that makes
both clean.

The arch here is milder than it looks. Because the channels are opposed, the
bed-side arch has 3.2mm of solid floor above it rather than an open slot, so
sag shows up as a rougher channel surface, not as a closed passage. The
failure mode is a cord that drags where it should slide. Check the bed-side
channel on the first print and hand-ream it if the surface is poor.

## Verification

The model is checked by rendering it to STL and asserting against the mesh:
watertight, a single body, exact bounding box, exact volume at each build
stage, and point-containment probes proving that each face carries its channel
on its own side and nothing on the other, that 3.2mm of floor survives beneath
each trough, that both troughs reach their side edge, that the cord path is
threaded rather than open, that the holes go through, that the band gap is
clear, that the bores run through all four horns with the teardrop apex on the
−Z side, and that every outer wall is bevelled at both faces while staying
full height at mid-thickness.

The suite is mutation-tested, not merely green: reversing a trough's
direction, lifting a trough off its face, stopping the troughs short of the
edge, dropping the sign that mirrors the teardrop apex, chamfering only one
side wall, chamfering only one face, cutting the bevel at 30° instead of 45°,
chamfering the band-gap base at one end only, or bevelling a horn interior —
even just one of the four — each fail it.

Software cannot confirm the 4.9mm horns survive a wrist, or that two
right-angle bends hold a real bungee under a finger's pull. Both need the
print test.

## Open questions

**Bend retention is untested against a real bungee.** Two right-angle bends
through 6.7mm of body should hold an elastic cord by friction alone, but that
is a claim about a real material, not about geometry. Print a coupon — one
hole with its two channels — and pull a bungee through it before committing to
a full body. If it slips, the cheapest fixes in order are a smaller `cordDia`
for a tighter path, then a thicker `bodyT` for longer bends.

**Threading may be fiddly.** The cord has to be fed through a 7mm hole and
turned into a channel on the far face. With a soft bungee end that may need a
threading tool or a taped tip. This is the price of the opposed routing, which
is what makes the part hold the cord without a knot.

**Whether 1mm of chamfer is enough.** The outer walls are bevelled, which
takes the bite off the edges, but the wrist side is still a flat plate. If it
still presses uncomfortably the next step is a larger `edgeCham` — the guards
allow up to 2.4mm — or a fillet rather than a chamfer, which would need a
different construction than the half-spaces used here.

**The chamfer thins the trough floor at the side walls.** Where a cord channel
exits at x = ±15 the bottom chamfer takes 1mm off the 3.2mm floor, leaving
2.2mm at the extreme edge and tapering back to full within 1mm. That is the
thinnest the floor gets anywhere and it sits right where the cord bears as it
leaves the body. Watch it on the print test.

## Licence

OCL v1.1, as with everything in this repository. See [LICENSE](LICENSE).
