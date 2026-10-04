# Football Umpire Counter

A flat pocket counter with two tracks. One button slides over four positions
marked 1 to 4, for the down. A second button slides over seven positions, for
where on the field the ball was last spotted. It is carried in a pocket, not
worn, and set by feel: one corner is cut off so the hand can tell which way it
sits. The owner has used one for years.

Source document these were exported from:
https://cad.onshape.com/documents/e2228a8db539c63d2157e3cf/w/2b4b489ae8b749f04039d1b5/e/6bc132c3cf1c9548ce42d1b0?renderMode=0&uiState=6ac2124f4aedfc432711d4b6

The STEP files here are the design. They are the owner's exports and are not
to be redrawn or changed.

> **State of this page.** Every size below was measured from the STEP files on
> 2026-10-04 with OpenCascade 8.0. Nothing was printed or assembled. Anything
> marked *inferred* was read off the geometry and is not the owner's word.

## The files

| File | Part | Print | Size | Solid volume |
| --- | --- | --- | --- | --- |
| `top.step` | top shell | 1 | 64.07 × 79.14 × 7.1mm | 13 411mm³ |
| `Bottom.step` | bottom shell | 1 | 60 × 75 × 5.1mm | 21 652mm³ |
| `button.step` | button | **2**, one per slot | 12 × 12 × 5mm | 169mm³ each |

Each file holds one closed, valid solid. Meshed at 0.01mm, each comes out as
one watertight body. Slicers that read STEP (PrusaSlicer, OrcaSlicer, Bambu
Studio) open them directly; there are no STL files here.

**Top shell.** A 3.1mm plate with a 4.0mm skirt, walls 2mm. Two stepped slots:
8.4mm wide where the button shows through, with a 13mm wide, 1.4mm high pocket
underneath that keeps the button's flange captive. The four-position slot
travels 45mm. The seven-position slot travels 55mm and sits 30mm to the side.
The numerals 1 to 4 are cut through the plate between the slots. A V-shaped
mark is cut through beside the fourth, middle, position of the seven. The cut
corner is at the "1" end, on the four-position side, 7mm along each edge.

**Bottom shell.** Eleven round holes, 6.03mm across and 3.1mm deep, over a
2.0mm floor: four on a 15mm pitch and seven on a 9.2mm pitch. Its matching
corner is cut 5mm along each edge.

**Button.** A ring, not a cap: an 8.0mm sleeve on a 12mm flange 1.0mm thick,
with a 6.03mm bore straight through. It is the same part as the slider's
button in [`down-indicator-selector/`](../down-indicator-selector/); the two
measure the same.

## Parts list

| Item | Qty | What is known |
| --- | --- | --- |
| Top shell, printed | 1 | `top.step` |
| Bottom shell, printed | 1 | `Bottom.step` |
| Button, printed | 2 | `button.step`, printed twice |
| Magnets | **not recorded** | 6mm × 2mm discs, the same as the slider (owner, 2026-10-03). The bottom shell has 11 holes that take one each, with 1.1mm to spare in depth. Each button's bore is 5mm long. How many magnets, and where they sit, is not recorded. |
| Pin | **not recorded** | "The same magnets and pin" as the slider (owner, 2026-10-03). It is not drawn or sized anywhere. *Inferred:* one per button, 6mm across, since the bore and the holes are both 6.03mm. |
| Strap | 0 | None. It has no strap fitting. |
| Fasteners, glue | 0 | None in the files. The shells press together. |

## How it goes together

As far as the files show. *All of this is inferred from the geometry;* the
Onshape assembly was not exported.

1. Fit the magnets and pins. Where they go is not recorded.
2. Lay the top shell face down. Drop a button into each slot, sleeve first, so
   its flange rests in the pocket.
3. Press the bottom shell into the skirt, holes towards the buttons, cut corner
   to cut corner. The buttons must go in first: once the shells are together
   the flanges cannot pass the slots.

The bottom shell seats against the underside of the plate and stands 1.1mm
proud of the skirt. The finished counter is 64.07 × 79.14mm and 8.2mm thick,
10.1mm over the buttons, which stand 1.9mm above the face.

## Fit, checked on the solids

- **The shells are a press fit.** The cavity is 60.0 × 75.0mm at the plate and
  tapers to about 0.18mm per side narrower than the bottom shell at its mouth,
  with a small lead-in at the very edge. This is the slider's fit, which the
  owner confirmed is intended.
- **The buttons clear both shells** at all eleven positions: no overlap with
  the top or the bottom shell. The sleeve has 0.2mm a side in the slot, the
  flange 0.5mm a side and 0.4mm of lift in its pocket.
- **The seventh position has no spare travel.** The seven holes run from
  y = −5.0 to y = 50.2, and the slot above them from −5.0 to 50.0. At the last
  hole the button's sleeve is touching the end of the slot. It still lines up,
  with nothing left over. Recorded, not changed.
- **A 6mm × 2mm magnet fits the holes and the bore** on paper, with 0.015mm a
  side. *Inferred:* printed holes usually come out a little small, so expect a
  push fit.

## Not known

- How many magnets, where they sit, and which way their poles face.
- What the pin is: its length, its material, and whether it is a magnet stack.
- Print material, layer height, and which face goes on the bed.
- What each of the seven positions stands for. The V marks the middle one.
- Whether the numerals and the V need supports or bridging settings; they are
  cut through the full 3.1mm plate.
