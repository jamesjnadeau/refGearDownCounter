# Wrist down counter, 2 by 2

A down counter worn on the wrist. One button moves between four positions set
in a 2 by 2 square, 14mm apart. There are two tops to choose from: one for a
watch strap on spring bars, one for a strap threaded through it.

Source document these were exported from:
https://cad.onshape.com/documents/00b1e7c9d07aec2789568fab/w/f48449999f7a6cf5db9ca973/e/4cc8a07cd495c58cc3707666?renderMode=0&uiState=6ac21225fe808cdfa36533a6

The STEP files here are the design. They are the owner's exports and are not
to be redrawn or changed.

> **State of this page.** Every size below was measured from the STEP files on
> 2026-10-04 with OpenCascade 8.0. Nothing was printed or assembled. Anything
> marked *inferred* was read off the geometry and is not the owner's word.

## The files

| File | Part | Print | Size | Solid volume |
| --- | --- | --- | --- | --- |
| `top.step` | top shell for a spring-bar strap | 1 of the two tops | 34 × 50 × 7.1mm | 4 139mm³ |
| `top-elastic-strap.step` | top shell for a threaded strap | 1 of the two tops | 34 × 50 × 7.1mm | 4 229mm³ |
| `Bottom.step` | bottom shell | 1 | 30 × 30 × 5.1mm | 4 019mm³ |
| *not in this folder* | button | 1 | see below | |

Each file holds one closed, valid solid. Meshed at 0.01mm, each comes out as
one watertight body. Slicers that read STEP (PrusaSlicer, OrcaSlicer, Bambu
Studio) open them directly; there are no STL files here.

**There is no button file in this folder.** The button from
[`down-counter-umpire/button.step`](../down-counter-umpire/) is the one to
print. The owner said on 2026-10-04 that this counter, the slider and the
Umpire Counter "all use the same button/pin and magnets". The files agree: that
button fits both tops and the bottom shell with no overlap at all four
positions, and the openings, pockets and holes are the same sizes as that
counter's.

**Both tops** share the same middle: a 3.1mm plate with a 4.0mm skirt around a
30mm square cavity. The opening is a rounded square 22.4mm across, with a 27mm
pocket 1.4mm high underneath that keeps the button's flange captive. The
button is free to move anywhere in the square; there are no tracks between the
positions. **Neither top carries numerals or any other marking.**

**`top.step`, for a spring-bar strap.** Four horns, two at each end, each 6mm
wide and 8mm long. The gap between a pair is **22.0mm**. Each horn has a 1.1mm
cross hole right through it, drawn as a teardrop so it prints without support,
4mm out from the body. *Inferred:* the holes take the tips of a watch spring
bar, so this top takes a **22mm** watch strap and two 22mm spring bars. Note
that the other counters in this repository are drawn for 20mm straps. The
holes at one end sit 0.45mm lower than at the other; recorded, not changed.

**`top-elastic-strap.step`, for a threaded strap.** No horns and no cross
holes. Each end has an opening **24.0mm** wide and 5mm long, closed at the tip
by a low rounded bar of 3mm radius. *Inferred:* the strap passes over the bar
and down through the opening at each end, so this top takes a strap up to
**24mm** wide, with no room to spare at 24mm, and needs no spring bars. The
owner's own strap is a 24mm Velcro strap; see [Field use](#field-use).

**Bottom shell.** Four round holes, 6.03mm across and 3.1mm deep, over a 2.0mm
floor, on a 14mm square.

## Parts list

| Item | Qty | What is known |
| --- | --- | --- |
| Top shell, printed | 1 | `top.step` or `top-elastic-strap.step` |
| Bottom shell, printed | 1 | `Bottom.step` |
| Button, printed | 1 | No file here. `../down-counter-umpire/button.step`, 12 × 12 × 5mm (owner, 2026-10-04) |
| Magnets | **not recorded** | 6mm × 2mm discs, the same as the slider and the Umpire Counter (owner, 2026-10-04); the holes are the same 6.03mm. The bottom shell has 4 holes that take one each, with 1.1mm to spare in depth. How many magnets, and where they sit, is not recorded. |
| Pin | **not recorded** | The same pin as the slider and the Umpire Counter (owner, 2026-10-04). It is not drawn or sized anywhere. *Inferred:* one, 6mm across. |
| Strap | 1 | With `top.step`: a 22mm watch strap. With `top-elastic-strap.step`: a strap up to 24mm wide. Type and length not recorded. |
| Spring bars | 2 with `top.step`, 0 with the other | For a 22mm strap, with tips that fit a 1.1mm hole. Length and supplier not recorded. |
| Fasteners, glue | 0 | None in the files. The shells press together. |

## How it goes together

As far as the files show. *All of this is inferred from the geometry;* the
Onshape assembly was not exported.

1. Fit the magnets and pin. Where they go is not recorded.
2. Lay the top shell face down. Drop the button into the opening, sleeve
   first, so its flange rests in the pocket.
3. Press the bottom shell into the skirt, holes towards the button. The button
   must go in first: once the shells are together its flange cannot pass the
   opening.
4. Fit the strap: on two spring bars between the horns, or threaded over the
   bar at each end.

The bottom shell seats against the underside of the plate and stands 1.1mm
proud of the skirt. The finished counter is 34 × 50mm and 8.2mm thick, 10.1mm
over the button, which stands 1.9mm above the face.

## Fit, checked on the solids

- **The shells are a press fit.** The cavity is 30.0mm square at the plate and
  tapers to about 0.18mm per side narrower than the bottom shell at its mouth,
  with a small lead-in at the very edge. This is the slider's fit, which the
  owner confirmed is intended. The bottom shell is square, so it goes in any
  of four ways round.
- **The Umpire Counter's button clears both shells** at all four positions,
  with either top.
- **A 6mm × 2mm magnet fits the holes and the button's bore** on paper, with
  0.015mm a side. *Inferred:* printed holes usually come out a little small,
  so expect a push fit.

## Field use

The owner has worn this counter in at least 10 games in the 2026 season, as
reported on 2026-10-03 and confirmed as this model on 2026-10-04: "the one
with 4 slots in a 2 by 2 configuration". It is worn on a 24mm Velcro strap,
and the owner reports that the strap slots as sized keep it from sliding.
*Inferred:* a 24mm strap through slots is `top-elastic-strap.step`; it is too
wide for the 22mm gap between the horns of `top.step`.

## Not known

- How many magnets, where they sit, and which way their poles face. What the
  pin is.
- Which position stands for which down. Nothing on the part says.
- The strap for each top: its type and length. Either top may be used; the
  builder picks one.
- Print material, layer height, and which face goes on the bed.
