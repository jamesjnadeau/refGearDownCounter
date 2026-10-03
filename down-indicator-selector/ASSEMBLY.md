# Slider down counter — assembly steps

**Draft, started 2026-10-03. Not complete.** These steps have not been
followed by anyone but the owner, and the steps for the magnets and the strap
are missing. Where a step is not known it reads **unknown**. Nothing here is
guessed. Parts are in [PARTS.md](PARTS.md).

## What the model tells us

These come from the geometry and are checked by `tests/test_fit.py`. See
[README.md](README.md#how-the-three-fit).

- The button's 12mm flange sits in the 13mm pocket under the top shell's
  plate. Its 8mm boss passes up through the 8.4mm slot opening. The flange
  cannot pass through that opening, so **the button goes in from underneath,
  before the bottom shell**.
- The bottom shell goes into the cavity under the top shell, with its four
  holes facing the button. The two shells have a 45° key at one corner, so
  they go together only one way round.
- The shells are a press fit, about 0.18mm of interference per side. The owner
  confirmed on 2026-10-03 that they are meant to press together.
- Once pressed home, the bottom shell stands 1.1mm proud of the top shell's
  skirt. The case is 8.2mm thick, and 10.1mm over the button.

## Steps

| # | Step | Status |
| --- | --- | --- |
| 1 | Print the three parts. | Print settings **unknown**. See PARTS.md. |
| 2 | Fit the magnets and the pin. | **Unknown.** How many magnets, where they sit, which way round they face, and whether they are pressed or glued in are not recorded. |
| 3 | Place the button in the pocket on the underside of the top shell, boss through the slot. | From the model. |
| 4 | Line up the keyed corners and press the bottom shell into the top shell until it seats. | From the model, and the owner's word that it is a press fit. How much force it takes, and whether a tool is needed, is **unknown**. |
| 5 | Fit the strap. | **Unknown.** This model has no strap slots or lugs. |
| 6 | Check: the button slides the length of the slot and holds at each of the four numbers. | The check follows from how the counter works. How firmly it should hold is **unknown**. |

## Taking it apart

**Unknown.** The repository does not record whether the press fit can be
opened again without damage. This matters for replacing parts.

## What is still needed to finish this page

1. Step 2, from the owner: the magnets and the pin.
2. Step 5, from the owner: the strap fitting.
3. One person other than the owner following these steps from a fresh print.
