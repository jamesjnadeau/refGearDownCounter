# Down indicator selector

The mechanical slider down counter, converted out of Onshape so the whole
thing can be worked on with nothing but OpenSCAD.

Three printed parts. The **top shell** is the plate a referee reads: 34 × 79 ×
7.1mm, with a stepped slot running its length and the numerals 1–4 cut through
beside it. The **bottom shell** nests into the cavity underneath it and sets
four stations 15mm apart. The **button** rides captive in the slot between
them, and which station it is on is the down.

| | | |
| --- | --- | --- |
| `down_indicator_selector.scad` | top shell | 34 × 79 × 7.1mm |
| `down_indicator_selector_bottom.scad` | bottom shell | 30 × 75 × 5.1mm |
| `down_indicator_selector_button.scad` | button | 12 × 12 × 5mm |

```bash
make stl
```

```bash
make test
```

## Where it came from

Onshape document `3db840dfeff4095d8508aa97`, workspace
`468073bad9de0e9ca2287d8a` — the original, do-not-modify copy. Read on
2026-08-25, at source microversion `49bf20ec9ce4d74dcad3203d`.

| Part Studio | Element |
| --- | --- |
| `top` | `8198d257a0b49b205e551477` |
| `Bottom` | `4770465acc52710e74b35fe2` |
| `button` | `82000ae215407b6dae7e9365` |

The conversion was made from the feature trees, not by tracing meshes. Every
dimension here is one of the originals' own: their variables (`holeSpaceing`
15, `holeDiameter` 8.4 on the top and 6.03 on the bottom, `cornerRadius` 6,
`buttonDiameter` 13, `shellWidth` 2, `textHeight` 7), their sketch
coordinates, and the depths, angles and radii on the extrudes, draft,
chamfers and fillets.

`reference/` holds Onshape's own exports of all three Part Studios, rescaled
from metres to millimetres and otherwise untouched. `make test` holds each
OpenSCAD model against its own reference, wall by wall.

### Coordinates are Onshape's, kept verbatim

None of the three parts is centred on the origin, and deliberately so: they
share a frame in plan. The slot runs from y = 0 to y = 45 on x = 0, and those
four stations are exactly where the bottom shell's holes sit.

In z they do not share a frame — each is drawn about its own z = 0, as it is
in Onshape. The top shell's z = 0 is the underside of its plate; the bottom
shell's is the floor of its four holes; the button's is the top of its flange.
See [How the three fit](#how-the-three-fit) for the arithmetic.

## How faithful it is

| Part | This model | Onshape | |
| --- | --- | --- | --- |
| top shell | 7819.4mm³ | 7832.5mm³ | 0.17% |
| bottom shell | 10829.4mm³ | 10828.5mm³ | 0.01% |
| button | 168.5mm³ | 168.6mm³ | 0.09% |

Every flat wall, the cavity, its draft, the slot, the pocket, the ledge, the
stations and the button's bore agree to within 0.02mm, which is the resolution
the tests measure at. On the top shell, take the numerals off both sides and
the two solids agree to about two parts in ten thousand — the numerals are the
difference, and the reason is the typeface.

Four things are worth knowing before trusting a dimension.

### The typeface

The original is set in **Open Sans**, which OpenSCAD cannot count on finding
installed. The default here is DejaVu Sans, which is a heavier face: the same
numerals cut about 20% more plate away. If Open Sans is installed, setting
`textFont = "Open Sans"` gets closer to the original.

The four numerals are *not* on the 15mm station pitch. They were placed by
hand in the original and drift about 3mm over the run. `textCentres` holds the
measured ink centre of each one rather than a regenerated layout, so a
substituted font lands each numeral where Onshape's is rather than walking it
along the plate. Putting them on the pitch is a one-line change and probably
an improvement, but it is a design change, not a conversion.

### The swung corners

Two of the three rounded corners of the footprint are not tangent fillets. The
−X/−Y corner is an ordinary 8mm fillet, but the two +X corners were struck on
arcs of 5·√2 ≈ 7.071mm through the tangent points an 8mm fillet would have
given. Such an arc is tangent to neither wall: it bulges 0.0711mm past both
and meets them at a slight kink, which is why the part measures 34.07 × 79.14
rather than 34 × 79.

This is almost certainly a slip in the original sketch, and it is tempting to
read it as a 0.07mm rounding error and square it off. It is not: at the corner
diagonal, where the difference is widest, the swung arc comes **0.48mm**
closer to the corner than a fillet would. So the default reproduces it.
`cornerSwing = cornerRadius + shellWidth` gives the fillets that were probably
intended.

Reproducing it costs one thing. A footprint with those arcs in it is slightly
concave, and the shell is built as a stack of bands whose walls are convex
hulls, so along the walls between those two corners the top chamfer and the
bottom fillet come out up to 0.0711mm narrow. The walls and corners themselves
are clipped back and are exact. See the notes in `lib/shell.scad`.

### The floating counter of the 4, which is fixed here

The numerals are cut clean through the plate, which leaves the triangle inside
the 4 attached to nothing. In the original it drops out of the print: Onshape
reports two solid bodies for `top` for exactly that reason, and the working
copy's `Watch lugs` feature ends by deleting the stray one.

**This is the one place the model deliberately departs from the original.** It
does what stencil faces do: leaves a 0.7mm bar of plate uncut across the
diagonal stroke, tying the loose piece back to the rest. The numeral still
reads as a 4. `make stl` gives a single closed solid.

The bar is a rectangle in glyph coordinates, so it depends on the face in use
— changing `textFont` or `textSize` means checking it still lands, and the
test that the part renders as one closed solid is what catches a tie that has
missed. `tiedNumeral = 0` cuts the numerals exactly as the original does,
floating counter and all.

### The bottom shell does not fit the cavity

Not a conversion artefact — it is what the originals measure, and the reason
it is under Fidelity rather than under a heading of its own is that the model
reproduces it rather than quietly correcting it.

The top shell's cavity is drafted 3° and is **widest at its ceiling**, so it
narrows toward the opening the bottom shell has to come in through: 30.000 ×
75.000 at the ceiling, 29.633 × 74.633 at its tightest section. The bottom
shell is 30.000 × 75.000. That is **0.18mm of interference per side**, and the
bottom shell's only chamfer is on the face that goes in last, so nothing leads
it in.

Whether that is a press fit on purpose or leftover moulding draft is not
recorded anywhere, and the empty assembly says nothing either way. Confirm
against a physical unit. If it wants fixing, `draftAngle` is the parameter,
and `tests/test_fit.py` pins the number so the change has to be deliberate.

## How the three fit

The Onshape assembly is empty — no instances, no mates — so nothing on either
side records how the counter stacks up. This is read off the geometry, and
`tests/test_fit.py` checks every line of it.

In the top shell's frame:

| | z | |
| --- | --- | --- |
| bottom shell | −5.10 … 0.00 | top face against the cavity ceiling, 1.10 proud of the skirt |
| top shell | −4.00 … 3.10 | |
| button flange | 0.00 … 1.00 | 1.0mm flange in a 1.4mm pocket, so 0.40 of lift |
| button boss | 1.00 … 5.00 | stands 1.90 clear of the top face |
| bottom's stations | −3.10 … 0.00 | the button's bore runs 0.00 … 5.00, straight over them |

Case thickness 8.20mm; 10.10mm over the boss. In plan the button has 0.50mm
of clearance in the pocket and 0.40mm in the opening, and its 12mm flange
cannot pass back out through the 8.4mm opening.

The detent itself is **not modelled, here or in Onshape**. The button's bore
and the bottom shell's holes are both 6.03mm, so something is meant to run
through the one into the other — a pin, a screw — but no fastener is drawn
anywhere. Confirm against a physical unit before changing anything in that
area.

## Layout

| | |
| --- | --- |
| `down_indicator_selector.scad` | the top shell: every parameter, the assertions, and the four-way difference that makes the part |
| `down_indicator_selector_bottom.scad` | the bottom shell |
| `down_indicator_selector_button.scad` | the button, as a solid of revolution |
| `lib/profile.scad` | the plan outlines, and the arc maths behind the swung corners |
| `lib/shell.scad` | banded solids: fillets, chamfers, the drafted cavity, and the plain plate |
| `lib/slot.scad` | the stepped slot and its pocket |
| `lib/numbers.scad` | the numerals, and the tie across the 4 |
| `reference/` | Onshape's exports of all three originals, in millimetres |
| `tests/` | pytest, rendering the models and asserting against the meshes |

## Still in Onshape

Nothing of this counter — all three parts are here. The lugs are a different
matter: they are a feature of the *working* copy, not of this original, and
they are still unbuilt. See
[../2026-08-22-band-lugs-design.md](../2026-08-22-band-lugs-design.md).
