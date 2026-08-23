# Watch Band Lugs for the Down Counter Case — Design

Status: **built** 2026-08-22, not yet printed
Scope: add spring-bar lugs to the two short ends of the top case, square off the
end corners, and drop the unprintable counter of the "4"

## Which case this is, and which it is not

This spec covers the **mechanical slider down counter** — a separate project
from the electronic Watchy-based ref counter, which lives in the
[watchy-ref-counter](https://github.com/jamesjnadeau/watchy-ref-counter)
repository. The two are related in purpose, both being football down counters.
They share no hardware and no geometry.

The first revision imported dimensions from `2026-08-18-waterproof-case-design.md`
in that other repository, which describes the Watchy case — a different
product. Every figure so borrowed (~43mm wide, ~53mm long, split shell, gasket
groove, sealing land) was wrong for this part. Those imports are removed.
Nothing in the waterproof case spec constrains this design.

## Where the work happens

The model lives in Onshape, not in this repository.

| | |
| --- | --- |
| Original (do not modify) | `3db840dfeff4095d8508aa97`, workspace `468073bad9de0e9ca2287d8a`, element `8198d257a0b49b205e551477` |
| Working copy (edit this) | `00b1e7c9d07aec2789568fab`, workspace `f48449999f7a6cf5db9ca973` |
| — element `top` (the lug work) | `c8988bf041b2bcfcdef1a5a4` |
| — element `Bottom` | `683c1e415929ccc1972183f3` |
| — element `button` | `549b45f983101a2bbf977db6` |
| — element `Assembly 1` | `1e37806a3e2b45bacbff18d4` (**empty** — no instances or mates) |

## Measured geometry

Taken 2026-08-22 with `measure` on the outer wall faces, superseding the
projections the first revision relied on.

| Quantity | Measured |
| --- | --- |
| Top shell | 79.00 x 34.00 x 7.10mm |
| Bottom shell | 75.00 x 30.00 x 5.10mm |
| Wall thickness, all round | 2.0mm |
| Top shell z extent | −4.00 (skirt underside) to +3.10 (display face) |

The shell is a solid top plate from z = 0 to +3.10 across the whole footprint,
and a 2.0mm skirt wall from z = −4.00 to 0 enclosing the cavity the bottom
shell nests in. That split matters: material may be added freely in the plate,
but only as a wall band in the skirt.

No cavity breach, no gasket groove, no sealing land — this is not a sealed
design, so no seal-clearance constraint applies.

## As built

One parametric FeatureScript feature, `Watch lugs` (`FQvyVICWet8aFQF_2`),
followed by `Lug edge chamfers` (`FnRpLXh3nNIcqTZ_3`). The original tree is
untouched ahead of them; rolling back past both yields the previous case
exactly.

| Dimension | Value | Why |
| --- | --- | --- |
| Band width | 20mm | See below |
| Lug gap, inner face to inner face | 20.2mm (**verified**) | 20mm strap plus 0.2mm so it slides rather than wedges |
| Horn thickness, each | 6.9mm | Outer faces flush with the side walls at x = −12 and x = +22 |
| Total across the lugs | 34.00mm | Full case width — no shoulder |
| Spring bar bore | 1.1mm diameter, through, **teardrop** | Standard bar: 1.78mm body, ~0.9mm tips |
| Teardrop apex | Toward the part underside (−Z) | Self-supporting crown — see below |
| Bar standoff from body | 4.5mm | ~3.6mm clear gap to the bar surface, for thick bands |
| Horn protrusion | 6.5mm | Standoff plus 2.0mm of material past the bore |
| Lug-to-lug | 92.00mm (**verified**) | 79.00mm case plus 6.5mm each end |
| Tip chamfer | 0.5mm | On the horn-tip vertical edges |

Volume 9505.9mm³, one solid body.

### Decisions

**20mm band width.** The first revision chose 22mm on the strength of a
projected ~43mm-wide case leaving ~7mm of shoulder outboard of each horn. The
end measures 34.00mm, which triggered this spec's own stated fallback — *"20mm
is the fallback if the measured end is narrower than projected."*

**Horns flush with the side walls**, over a 3.5mm horn inset from the end. The
inset version left the horns rooting into the case's corner radii rather than
into solid end material, which read as thin tabs stuck on and produced eleven
sliver faces. Running the horns out to the side walls gives each one 6.9mm of
root across its full thickness and removes the shoulder entirely.

**Square end corners**, over rounded, and the chamfered "chop" at the +Y/−X
corner is gone. With flush horns the side walls now run straight from the body
through to the horn tips, so a corner radius would only reintroduce a step
where the horn meets the wall.

**Through-drilled bores**, over blind. A 1.1mm blind hole in an FDM side wall
prints badly, and a through-hole lets the bar be seated and released with a
paperclip instead of a spring-bar tool.

**Teardrop bores**, over round. The bore axis is horizontal when the case is
printed flat, so a round hole puts an unsupported crown at the top of the
circle, which sags and closes the hole up. The teardrop replaces that crown
with two flanks tangent to the bore at 45° meeting at an apex — the apex sits
r√2 from the centre, so at 1.1mm bore it extends the profile 0.23mm.

The apex points to the part's **underside** (−Z). That is only self-supporting
if the underside faces up on the bed, i.e. the case is printed display-side
down — which is also the orientation that puts the flat display face against
the bed. `teardropDown` flips it if the case is ever printed skirt-down
instead.

The 0.23mm of extra profile is in Z, while band tension pulls in ±Y, so the bar
tip still bears on the round part of the bore and the teardrop does not let it
shift under load.

**The counter of the "4" is deleted.** It was a fully disconnected solid —
the part carried two bodies, and the second was that island. It has no
support and would drop off the plate.

### Parameters

Editable on the `Watch lugs` feature; the geometry follows automatically.

| Parameter | Default |
| --- | --- |
| `bandWidth` | 20mm |
| `barStandoff` | 4.5mm |
| `tipMargin` | 2mm |
| `barHoleDia` | 1.1mm |
| `teardropDown` | true — apex toward the part underside |

Horn thickness is derived, not a parameter: the horns always run from the band
gap out to the side walls, so changing `bandWidth` rethickens them. Valid band
range is roughly 12–28mm before the horns get thinner than the walls or the
gap runs past them.

## Lug-to-lug length, for confirmation before printing

At 6.5mm of horn per end the 79.00mm case gives **92.00mm lug-to-lug**.

The first revision set a "stop if it exceeds ~58mm" threshold, derived from the
48–56mm range large *watches* occupy. That came in with the Watchy case import
and does not govern this product: a 79mm case cannot produce a 58mm span by any
arrangement of horns, and its length is not something the lugs can change. The
horns contribute 13mm of the 92mm; the rest is the device.

The open question is orientation, not horn length. The 79mm axis must run along
the forearm, since 79mm will not span a wrist — which makes lugs on the two
34mm ends the only sensible placement. **Confirm the device is worn
long-axis-along-the-arm before printing a full case.**

## Load path

Band tension pulls the horn, and through it the end wall, along the case's long
axis. That loads the wall in its own plane, where tension is not the limiting
mode. The limiting mode is the strap levering a horn up and down, which a
spring bar seated in a through-hole constrains. With flush horns the root is
6.9mm wide and 7.1mm tall, and the bore leaves 5.8mm of material across it.

## Print orientation

Printed with the case flat, layers stack in Z and strap tension pulls along the
layers rather than across them — the strong direction.

## Verification

Done: `describe_part_studio` topology checks after each feature; `measure`
confirming the 20.2mm gap and the 92.00mm lug-to-lug; a bottom render
confirming the skirt cavity is unbreached.

Outstanding: a printed single-end test piece with a real spring bar and strap
before committing to a full case print. Software confirms the geometry is
closed and printable; it cannot confirm the horns survive a wrist.

Known cosmetic note: a handful of sub-0.06mm² sliver faces remain where the new
prismatic geometry meets the original drafted and filleted walls. They are far
below FDM resolution, but check the STL export loads cleanly.

## Session notes

**Onshape authentication.** Access was confirmed working 2026-08-22 via
`list_documents`. The MCP server reads keys once at import from
`load_dotenv(os.path.join(_package_dir, ".env"))` — `onshape_mcp/server.py:19`
— where `_package_dir` is the version-pinned plugin root. A plugin update past
1.2.0 creates a new directory and the symlink must be remade; exports in
`~/.profile` avoid that. The residual failure mode is a stale server process:
the server belongs to the session that spawned it, so restarting the app
resumes the session without respawning it and credentials never load. A new
conversation fixes it.

**`create_extrude` and `create_offset_plane` are unusable on this document.**
Both return HTTP 400 from the features endpoint before Onshape evaluates
anything, for every argument combination tried — bare-number and unit-string
depths, NEW and ADD, with and without optional parameters, and with required
parameters only. `create_sketch` on the same Part Studio succeeds, so
credentials and the element id are fine; the common factor in the failures is
a quantity parameter in the payload. Everything here was therefore built with
`write_featurescript_feature`, which works. Do not spend another session
debugging the primitives — go straight to FeatureScript on this document.

**The account is at the Onshape free-tier 10-document cap**, so
`create_document` returns 409 and scratch/probe documents are not available for
diagnosis.
