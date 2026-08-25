# Ref Gear — Down Counter

Football down counters — the wrist-worn devices a referee uses to track which
down it is. This repository covers the **mechanical** ones, whose models live
in Onshape rather than here; what is version-controlled is the documentation.

## These are not the Watchy ref counter

The **electronic** ref counter — an ESP32-C6 board running countdown timers on
a Watchy e-paper panel — is a separate project in its own repository,
[watchy-ref-counter](https://github.com/jamesjnadeau/watchy-ref-counter). That
is a different product with different hardware and different geometry.

The two are related only in purpose — both are officiating aids for football.
**Do not carry dimensions between them.** An earlier revision of the lugs spec
did exactly that, projecting a ~43 x 53mm case from the Watchy waterproof case
spec onto a part that actually measures 34 x 79mm, and every figure derived
from it was wrong. This repository was split out of that one on 2026-08-23 so
the two cannot be confused again.

## Contents

| File | What it is |
| --- | --- |
| [2026-08-22-band-lugs-design.md](2026-08-22-band-lugs-design.md) | Design and as-built record for the spring-bar band lugs, the squared end corners, and the removal of the unprintable "4" counter. Built 2026-08-22, not yet printed. |
| [2026-08-24-finger-loop-indicator-design.md](2026-08-24-finger-loop-indicator-design.md) | Design for the finger-loop down indicator: a wrist body anchoring a bungee cord that loops over a finger. Modelled in OpenSCAD under `down-indicator-string/`, not in Onshape. |
| [down-indicator-string/](down-indicator-string/) | The OpenSCAD model for the above, with a `pytest` suite that renders it and asserts against the mesh. |
| [down-indicator-selector/](down-indicator-selector/) | All three parts of the slider down counter, converted out of Onshape into OpenSCAD on 2026-08-25, with the same kind of test suite and Onshape's own exports kept alongside as reference meshes. |
| [AGENTS.md](AGENTS.md) | Working notes for agents. Chiefly: if you cannot delete something you created in Onshape, hand back an explicit cleanup list rather than leaving orphans unmentioned. |
| [LICENSE](LICENSE) | Open Community License v1.1, verbatim. See [Licence](#licence). |

## The mechanical slider down counter

A three-part printed slider. A knob rides in a slot in the top plate and
indexes between four stations; the numbers 1–4 engraved alongside the slot
read off the current down.

### The move to OpenSCAD

All three parts have been converted to OpenSCAD and live in
[down-indicator-selector/](down-indicator-selector/), so the counter can be
built without opening Onshape. They are conversions of the **original**, so
they carry no lugs. That README records what the conversion does and does not
carry over — chiefly the typeface, the two non-tangent corner arcs, and the
floating counter of the 4, which is the one thing deliberately fixed rather
than reproduced.

Two things it turned up that were not recorded anywhere before:

- **How the three parts stack.** The assembly in Onshape is empty, so this was
  read off the geometry: the bottom shell seats against the cavity ceiling and
  stands 1.1mm proud of the skirt, the button's flange lifts 0.4mm in its
  pocket, and its boss stands 1.9mm clear of the top face. Case thickness
  8.2mm.
- **The bottom shell does not fit the cavity.** The cavity's 3° draft makes it
  widest at the ceiling and narrowest at the mouth the bottom shell enters
  through, leaving about 0.18mm of interference per side. Whether that is
  deliberate is not recorded. Confirm against a physical unit.

### Onshape models

| | |
| --- | --- |
| Original (do not modify) | `3db840dfeff4095d8508aa97`, workspace `468073bad9de0e9ca2287d8a` |
| Working copy (edit this) | `00b1e7c9d07aec2789568fab`, workspace `f48449999f7a6cf5db9ca973` |

Both documents are the work of James Nadeau, who authored the original model
and holds the rights licensed under [OCL v1.1](#licence). Nothing here is
derived from a third party's design.

The copy was made by hand — the API cannot clone a document. Working in the
copy keeps the original intact and preserves the parametric feature tree.

Elements in the working copy:

| Element | ID |
| --- | --- |
| `top` | `c8988bf041b2bcfcdef1a5a4` |
| `Bottom` | `683c1e415929ccc1972183f3` |
| `button` | `549b45f983101a2bbf977db6` |
| `Assembly 1` | `1e37806a3e2b45bacbff18d4` — **empty**, no instances or mates |
| `BOM : Assembly 1` | `e0e801cd186e08b5a415de05` |

Because the assembly carries nothing, there is no mate data describing how the
parts stack. The two shells are nonetheless modelled in a shared coordinate
space: the top's inner end face and the bottom's outer end face both sit at
y = −15, so the shells nest directly.

### Parts, as measured 2026-08-22

| Part | Size | Notes |
| --- | --- | --- |
| `top` | 79.00 x 34.00 x 7.10mm | Solid plate z = 0 to +3.10; 2.0mm skirt wall z = −4.00 to 0 around the cavity the bottom nests in. Carries the slot, the numbers, and now the lugs. |
| `Bottom` | 75.00 x 30.00 x 5.10mm | Four index holes, radius 3.02mm, at x = 0 and y = 0, 15, 30, 45. |
| `button` | 12 x 12 x 5mm | Flanged top-hat with a hollow bore: a 12mm flange, ~1mm thick, under a raised boss. |

With the lugs fitted the top plate now measures **92.00mm** end to end; the
79.00mm figure is the case body alone.

### How it works

The slot in the top plate is a racetrack running y = 0 to 45, stepped: a
13mm-diameter internal pocket, narrowing to an 8.4mm opening at the top face.
The button's 12mm flange sits captive in the pocket and cannot pass back out
through the 8.4mm opening, while its boss protrudes for a thumb. Sliding it
along the slot moves it between the four stations set by the holes in the
bottom plate, at 15mm spacing.

The exact detent interface — whether a nub on the flange drops into those
holes, or a separate pin passes through the button's bore — is not
determinable from the models alone, since the assembly is empty and no
fastener is modelled. Confirm against a physical unit before changing
anything in that area.

### Current state

Built into the working copy on 2026-08-22, as two FeatureScript features
appended to `top`:

- `Watch lugs` (`F11dhRn0iQOtIjw_2`) — 20mm spring-bar lugs, horns flush with
  the side walls, squared end corners, teardrop spring-bar bores, and deletion
  of the floating "4" counter. Parametric: `bandWidth`, `barStandoff`,
  `tipMargin`, `barHoleDia`, `teardropDown`.
- `Lug edge chamfers` (`Fg13g2ZpNtzIeQs_3`) — 0.5mm chamfer on the horn tips,
  last in the tree so it reaches geometry the original chamfer features cannot.

The original feature tree is untouched ahead of these two; rolling back past
both restores the previous case exactly. Full dimensions and reasoning are in
the [lugs spec](2026-08-22-band-lugs-design.md).

**Two Feature Studio elements are load-bearing and must not be deleted**, as
each carries the source for one of the features above:

| Feature Studio | ID — check this, not the name | Carries |
| --- | --- | --- |
| `ClaudeFS_watchLugs2` | `058db78c7f1aef7b10e6357e` | `Watch lugs` |
| `ClaudeFS_lugChamfers2` | `a9c3a085e56c94f216aaf9f3` | `Lug edge chamfers` |

**Identify these by ID, not by name.** Reissuing a feature under an existing
`fsElementName` does *not* reuse that element — it creates a new one with the
same name — so superseded Feature Studios can share a name character for
character with the live one. Open the tab in Onshape and read the `/e/<id>`
segment of the URL to tell them apart.

Also do not confuse `Draft 1` in the feature tree with a leftover draft: it is
an original taper feature on the case walls, and deleting it changes the
geometry.

**Not yet printed.** A single-end test piece with a real spring bar and strap
should come before a full case print, and the wear orientation still needs
confirming — see the spec.

## The finger-loop down indicator

A third device, and the first one whose model is version-controlled here
rather than living in Onshape. A 40 x 30 x 6.7mm body on a 20mm watch strap,
with two 7mm through-holes. Each hole has a 7mm channel on the watch face
running out to one side edge and a matching channel on the wrist side running
out to the other, so a threaded cord makes two right-angle bends inside the
body and is held by its own path rather than by a knot. The cord runs over the
back of the hand and loops over a finger; the finger is the down selector.

It reuses the down counter's spring-bar lug geometry — 20mm band, 20.2mm gap,
teardrop bores — and nothing else. Its footprint is its own.

See [the design](2026-08-24-finger-loop-indicator-design.md) and
[down-indicator-string/README.md](down-indicator-string/README.md).

## Related Onshape documents

| Document | ID | Status |
| --- | --- | --- |
| Football Umpire counter | `e2228a8db539c63d2157e3cf`, workspace `2b4b489ae8b749f04039d1b5` | **Not inspected.** Same element structure as the down counter — three Part Studios, an assembly and a BOM — but nothing here has been verified against it. |

## Working on these models

Two environment constraints, both hit during the 2026-08-22 session and both
recorded in full in the spec's session notes:

- **`create_extrude` and `create_offset_plane` return HTTP 400** on the working
  copy for every argument combination, while `create_sketch` succeeds on the
  same element. Build with `write_featurescript_feature` instead; it works.
- **The Onshape account is at the free-tier 10-document cap**, so
  `create_document` returns 409 and throwaway scratch documents are not
  available for diagnosis.

## Licence

**OCL v1.1** — the [Open Community
License](https://github.com/OpenCommunityLicence/OpenCommunityLicence)
published by Prusa Research. No add-on conditions apply. The full text is in
[LICENSE](LICENSE).

In short: as a non-commercial end user you may use, copy, modify and hack this
work freely, and if you distribute derivatives you must do so under OCL as
well. A business may use and modify it internally, including for internal
production and repair, but may not replicate it commercially without a
separate licence. The work must not be subjected to automated text or data
mining without explicit permission.

The licence covers the design work recorded here and the corresponding Onshape
geometry. Both are needed to build the part, and only the documentation is
version-controlled in this repository.
