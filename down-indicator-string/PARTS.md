# Finger-loop down indicator — parts list

**Draft, started 2026-10-03. Not complete.** Every figure below comes from the
model in this directory or from the owner, and says which. Where neither says,
the entry reads **unknown**. Nothing here is guessed.

## Printed parts

Build it with `make stl`.

| Part | Qty | Size | File |
| --- | --- | --- | --- |
| Body | 1 | 40 × 30 × 6.7mm; 53mm over the lugs | `down_indicator_string.scad` |

## Bought parts

| Part | Qty | What is known | Source |
| --- | --- | --- | --- |
| Cord | 1 | 1/8" (3.2mm) bungee cord. Length **unknown**. How the ends are finished or joined into a loop is **unknown**. | Owner, 2026-10-03 |
| Strap | 1 | A 20mm band, from the lugs as modelled. "Any suitable strap that fits would do". Type and length **unknown**. See the note below. | Model; owner, 2026-10-03 |
| Spring bars | **unknown** | The model has two pairs of lugs with 1.1mm bores, sized for a standard bar with a 1.78mm body and about 0.9mm tips, across a 20.2mm gap. Whether the strap is fitted with spring bars is **unknown**. Bar length is **unknown**. | Model, and the lugs spec |
| Fasteners | 0 | None mentioned. | — |

**Strap width.** The lugs as modelled take a 20mm band (a 20.2mm gap). The
24mm-wide Velcro strap the owner described on 2026-10-03, and the tight fit
that keeps it from sliding, belong to a different counter: the 2 by 2 wrist
counter in [`down-indicator-watch/`](../down-indicator-watch/), as the owner
said on 2026-10-04. [README.md](README.md) still records that strap against
this model and needs the same correction.

Facts from the model that bear on the cord:

- Two through-holes, 7.0mm in diameter, 12mm apart centre to centre.
- From each hole, a groove 2.5mm wide runs to one side edge on the watch face
  and to the other side edge on the wrist side. Each groove's axis is sunk
  1mm into its face.

## Print settings

| Setting | Body |
| --- | --- |
| Which face goes on the bed | Face down: the `z = bodyT` face, which is the watch face. From [README.md](README.md#print). |
| Material | **unknown** |
| Layer height | **unknown** |
| Nozzle | **unknown** |
| Walls and infill | **unknown** |
| Supports | **unknown**. The README says the teardrop bores are self-supporting in this orientation. Nothing is said about the grooves on the bed side. |

## What is still needed to finish this list

1. Cord length, and how the loop is closed.
2. Which strap is used, and whether it is fitted with spring bars.
3. Print settings.
