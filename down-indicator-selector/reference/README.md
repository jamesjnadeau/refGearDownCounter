# Reference meshes

Onshape's own STL exports of the three Part Studios of document
`3db840dfeff4095d8508aa97`, workspace `468073bad9de0e9ca2287d8a`, taken
2026-08-25 at source microversion `49bf20ec9ce4d74dcad3203d`.

| File | Part Studio | Element |
| --- | --- | --- |
| `onshape-top.stl` | `top` | `8198d257a0b49b205e551477` |
| `onshape-bottom.stl` | `Bottom` | `4770465acc52710e74b35fe2` |
| `onshape-button.stl` | `button` | `82000ae215407b6dae7e9365` |

Onshape exports in metres. These copies have been rescaled to millimetres, to
match every other STL in the repository, and are otherwise the bytes Onshape
produced.

They are **tessellations, not the solids**. Onshape's chord tolerance flattens
every curve, and the smaller and rounder the part the worse it reads:

| | tessellated | B-rep |
| --- | --- | --- |
| `top` | 7826.4mm³ | 7832.5mm³ |
| `Bottom` | 10827.1mm³ | 10828.5mm³ |
| `button` | 164.0mm³ | 168.6mm³ |

The top's bounding box also misses the 0.0711mm corner bulge its solid has.
`tests/test_against_onshape.py` is written around all of that: strict on flat
faces, where a tessellation is exact, and loose on curved ones — which is why
the button is compared against its B-rep volume and its walls, not against
the volume of the mesh here.

They are here so the conversion can still be checked once nobody is opening
Onshape any more. Do not regenerate them to make a test pass.
