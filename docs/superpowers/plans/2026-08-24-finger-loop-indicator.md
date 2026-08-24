# Finger-Loop Down Indicator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a parametric OpenSCAD model of a wrist-worn body that anchors a bungee cord in two side-loading 7mm slots and mounts on a 20mm spring-bar watch strap.

**Architecture:** One top-level `.scad` file holds every tunable parameter and the assembly; `lib/` holds pure modules that take their dimensions as arguments and read no globals, so each can be rendered standalone by a test harness. Correctness is asserted against the rendered mesh — `openscad` exports STL, `trimesh` loads it, and tests check watertightness, bounding box, exact volume and point-containment probes. Parameter combinations that would produce an unbuildable part are rejected by `assert()` inside the model rather than by a test.

**Tech Stack:** OpenSCAD 2021.01 (already installed at `/usr/bin/openscad`), Python 3.13, `trimesh` 5.0.0, `numpy`, `scipy`, `rtree`, `pytest` 9.1.1, GNU make.

**Spec:** [2026-08-24-finger-loop-indicator-design.md](../../../2026-08-24-finger-loop-indicator-design.md)

## Global Constraints

- All work lives in a new `down-indicator/` directory at the repository root. Nothing outside it changes except `README.md` (Task 6) and a new root `.gitignore` (Task 1).
- Coordinates: **+X across the wrist, +Y along the forearm toward the hand, +Z out of the watch face.** The body spans z = 0 (wrist side) to z = `bodyT` (face). Every module and test uses this frame.
- Every `lib/*.scad` module takes its dimensions as **explicit arguments**. No module reads a global. This is what lets the test harnesses render one module in isolation.
- All parameters are declared at the top level of `down_indicator.scad` so `openscad -D name=value` can override them. `use <>` does not import variables, so this is the only file where parameters live.
- `$fn = 96` everywhere, including in the test harness `.scad` files. Volume assertions are exact to the facet count and will fail if it differs.
- **OpenSCAD infers output format from the file extension.** `-o /dev/null` fails with exit code 1 regardless of the model. Always render to a real `.stl` path, including when you only care about whether the render succeeded.
- Dimensions, verbatim from the spec: `bodyLen = 40.0`, `bodyWid = 30.0`, `bodyT = 6.7`, `cordDia = 7.0`, `holeY = 10.0`, `bandWidth = 20.0`, `bandClear = 0.2`, `barStandoff = 4.5`, `tipMargin = 2.0`, `barHoleDia = 1.1`, `tipChamfer = 0.5`, `teardropDown = true`.
- Commit at the end of every task. Do not amend or squash earlier tasks' commits.

## File Structure

| File | Responsibility |
| --- | --- |
| `down-indicator/down_indicator.scad` | Every parameter, the derived values, the `assert()` guards, and the assembly. The only file with globals. |
| `down-indicator/lib/util.scad` | `teardrop_2d`, `teardrop_bore`. Shared by nothing else today; kept separate because the teardrop is the one non-obvious profile in the model. |
| `down-indicator/lib/body.scad` | `body_blank` — the bare slab. |
| `down-indicator/lib/cord_slots.scad` | `cord_cutter`, `cord_trough` — the subtractive tool for the holes and the face troughs. |
| `down-indicator/lib/lugs.scad` | `lug_horns` (additive), `horn_profile`, `bar_bores` (subtractive). |
| `down-indicator/tests/conftest.py` | `render()` and `render_failure()` — run OpenSCAD, cache by source-content hash, return a `trimesh` mesh. Plus the `inside()` probe helper and the shared fixtures. |
| `down-indicator/tests/scad/*.scad` | One tiny harness per lib module, so a module can be rendered without the rest of the assembly. |
| `down-indicator/tests/test_body.py` | Task 1 |
| `down-indicator/tests/test_cord_slots.py` | Tasks 2 and 3 |
| `down-indicator/tests/test_lugs.py` | Tasks 4 and 5 |
| `down-indicator/tests/test_assembly.py` | Task 6 — the whole part and the parameter guards |
| `down-indicator/Makefile` | `make test`, `make stl`, `make clean` |
| `down-indicator/requirements.txt` | Pinned Python dependencies |
| `down-indicator/README.md` | Task 6 |

---

### Task 1: Scaffold, render harness, and the body blank

Sets up the venv, the OpenSCAD-to-trimesh bridge every later task depends on, and the simplest possible piece of geometry to prove the bridge works end to end.

**Files:**
- Create: `down-indicator/lib/body.scad`
- Create: `down-indicator/tests/conftest.py`
- Create: `down-indicator/tests/scad/body_only.scad`
- Create: `down-indicator/tests/test_body.py`
- Create: `down-indicator/Makefile`
- Create: `down-indicator/requirements.txt`
- Create: `.gitignore` (repository root)

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `body_blank(len, wid, t)` — a solid slab `wid` in X by `len` in Y by `t` in Z, centred on the origin in X and Y, sitting on z = 0.
  - `render(scad_relpath, **overrides) -> trimesh.Trimesh` — renders a `.scad` file under `down-indicator/` and returns the mesh. Keyword overrides become `-D name=value`; Python `bool` is emitted as OpenSCAD `true`/`false`.
  - `render_failure(scad_relpath, **overrides) -> str` — asserts the render fails and returns combined stdout+stderr.
  - `inside(mesh, *points) -> numpy.ndarray[bool]` — point containment, one bool per point.

- [ ] **Step 1: Create the directory and pin the dependencies**

```bash
mkdir -p down-indicator/lib down-indicator/tests/scad
```

`down-indicator/requirements.txt`:

```
trimesh==5.0.0
numpy==2.5.2
scipy==1.18.1
rtree==1.4.1
pytest==9.1.1
```

`scipy` and `rtree` are not optional: `trimesh` degrades silently without them and then raises `ModuleNotFoundError` from inside `body_count` and `contains`, which are the two checks this suite leans on hardest.

Root `.gitignore`:

```
build/
.venv/
__pycache__/
.pytest_cache/
*.pyc
```

- [ ] **Step 2: Write the Makefile**

`down-indicator/Makefile`:

```make
OPENSCAD ?= openscad
VENV     := .venv

.PHONY: test stl clean

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r requirements.txt
	touch $(VENV)

test: $(VENV)
	$(VENV)/bin/pytest -q

stl: build/down_indicator.stl

build/down_indicator.stl: down_indicator.scad $(wildcard lib/*.scad)
	@mkdir -p build
	$(OPENSCAD) -o $@ $<

clean:
	rm -rf build
```

- [ ] **Step 3: Write the render harness**

`down-indicator/tests/conftest.py`:

```python
"""Render OpenSCAD models to meshes so tests can assert against real geometry.

Renders are cached on a hash of every .scad file in the project, so a suite
that renders the same model from several tests pays the CGAL cost once, and
editing any model file invalidates the cache.
"""

import hashlib
import os
import subprocess
from pathlib import Path

import numpy as np
import pytest
import trimesh

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "test"
OPENSCAD = os.environ.get("OPENSCAD", "openscad")


def _sources_key() -> str:
    digest = hashlib.sha1()
    for path in sorted(ROOT.rglob("*.scad")):
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def _defines(overrides: dict) -> list:
    out = []
    for key in sorted(overrides):
        value = overrides[key]
        if isinstance(value, bool):
            value = "true" if value else "false"
        out += ["-D", f"{key}={value}"]
    return out


def _run(scad_relpath: str, out_path: Path, overrides: dict):
    return subprocess.run(
        [OPENSCAD, "-o", str(out_path), *_defines(overrides), str(ROOT / scad_relpath)],
        capture_output=True,
        text=True,
    )


def render(scad_relpath: str, **overrides) -> trimesh.Trimesh:
    """Render a model and return it as a mesh. Fails the test if OpenSCAD does."""
    defines = _defines(overrides)
    key = hashlib.sha1(
        f"{scad_relpath}|{defines}|{_sources_key()}".encode()
    ).hexdigest()[:16]
    BUILD.mkdir(parents=True, exist_ok=True)
    out_path = BUILD / f"{key}.stl"
    if not out_path.exists():
        proc = _run(scad_relpath, out_path, overrides)
        if proc.returncode != 0 or not out_path.exists():
            pytest.fail(
                f"OpenSCAD failed on {scad_relpath} {defines}\n"
                f"{proc.stdout}\n{proc.stderr}"
            )
    return trimesh.load(out_path, force="mesh")


def render_failure(scad_relpath: str, **overrides) -> str:
    """Assert the render is rejected, and return what OpenSCAD said about it."""
    BUILD.mkdir(parents=True, exist_ok=True)
    out_path = BUILD / "rejected.stl"
    out_path.unlink(missing_ok=True)
    proc = _run(scad_relpath, out_path, overrides)
    assert proc.returncode != 0, (
        f"expected {scad_relpath} {overrides} to be rejected, but it rendered"
    )
    return proc.stdout + proc.stderr


def inside(mesh, *points) -> np.ndarray:
    """True for each point that lies inside the solid."""
    return mesh.contains(np.array(points, dtype=float))


@pytest.fixture(scope="session")
def blank():
    return render("tests/scad/body_only.scad")
```

- [ ] **Step 4: Write the failing test**

`down-indicator/tests/test_body.py`:

```python
"""The bare slab: 30mm across the wrist, 40mm along the forearm, 6.7mm thick."""

from pytest import approx


def test_blank_is_one_closed_solid(blank):
    assert blank.is_watertight
    assert blank.is_winding_consistent
    assert blank.body_count == 1


def test_blank_bounding_box(blank):
    low, high = blank.bounds
    assert list(low) == approx([-15.0, -20.0, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 20.0, 6.7], abs=1e-6)


def test_blank_volume_is_the_full_prism(blank):
    assert blank.volume == approx(30.0 * 40.0 * 6.7, rel=1e-9)


def test_blank_sits_on_the_bed_and_is_solid_through(blank):
    from conftest import inside

    assert inside(blank, [0, 0, 0.1], [0, 0, 3.35], [0, 0, 6.6]).all()
    assert not inside(blank, [0, 0, -0.1], [0, 0, 6.8]).any()
```

- [ ] **Step 5: Run the test to verify it fails**

```bash
cd down-indicator && make test
```

Expected: FAIL. `body_only.scad` and `body.scad` do not exist yet, so `render` calls `pytest.fail` with OpenSCAD's "Can't open input file" error.

- [ ] **Step 6: Write the model**

`down-indicator/lib/body.scad`:

```openscad
// The bare case body.
//
// A plain rectangular slab, square in plan. The lug horns run flush to the
// side walls, so a corner radius here would root them into the radius rather
// than into solid end material -- the failure the down counter's lug spec
// diagnosed and fixed by squaring the corners.

// `wid` across X, `len` along Y, centred on the origin in plan, sitting on z = 0.
module body_blank(len, wid, t) {
    linear_extrude(height = t) square([wid, len], center = true);
}
```

`down-indicator/tests/scad/body_only.scad`:

```openscad
use <../../lib/body.scad>

bodyLen = 40.0;
bodyWid = 30.0;
bodyT   =  6.7;
$fn = 96;

body_blank(bodyLen, bodyWid, bodyT);
```

- [ ] **Step 7: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 4 tests. The first run also builds `.venv`, which takes about a minute.

- [ ] **Step 8: Commit**

```bash
git add .gitignore down-indicator/
git commit -m "feat(down-indicator): scaffold OpenSCAD project and body blank"
```

---

### Task 2: Cord holes

Two 7mm through-bores on the Y centreline. Split from the troughs because the holes alone are a clean, exactly-computable volume, and getting that number right proves the subtractive path before the harder geometry lands on top of it.

**Files:**
- Create: `down-indicator/lib/cord_slots.scad`
- Create: `down-indicator/tests/scad/cord_only.scad`
- Create: `down-indicator/tests/test_cord_slots.py`
- Modify: `down-indicator/tests/conftest.py` (add the `cord` fixture)

**Interfaces:**
- Consumes: `body_blank(len, wid, t)` from Task 1.
- Produces: `cord_cutter(len, t, dia, holeY)` — the full subtractive tool for holes and troughs, positioned in the body's own frame and intended to be passed to `difference()`. This task implements the holes only; Task 3 adds the troughs to the same module without changing its signature.

- [ ] **Step 1: Add the fixture**

Append to `down-indicator/tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def cord():
    return render("tests/scad/cord_only.scad")
```

- [ ] **Step 2: Write the failing test**

`down-indicator/tests/test_cord_slots.py`:

```python
"""The cord holes and the face troughs that open them to the ends."""

import math

import numpy as np
from pytest import approx

from conftest import inside

BODY_T = 6.7
CORD_R = 3.5
MID = BODY_T / 2
BLANK_VOLUME = 30.0 * 40.0 * 6.7

# A 96-gon inscribed in a circle of radius r has area 48 * r^2 * sin(3.75 deg).
HOLE_AREA = 0.5 * 96 * CORD_R**2 * math.sin(math.radians(360 / 96))


def test_cord_body_is_one_closed_solid(cord):
    assert cord.is_watertight
    assert cord.body_count == 1


def test_holes_remove_exactly_two_cylinders(cord):
    assert BLANK_VOLUME - cord.volume == approx(2 * HOLE_AREA * BODY_T, rel=1e-6)


def test_each_hole_goes_all_the_way_through(cord):
    for sign in (-1, 1):
        column = [[0.0, sign * 10.0, z] for z in (0.2, MID, 6.5)]
        assert not inside(cord, *column).any()


def test_holes_are_seven_millimetres_across(cord):
    # Probe across the +Y hole at mid-height, 0.1mm inside and outside the wall.
    assert not inside(cord, [3.4, 10.0, MID])[0]
    assert inside(cord, [3.6, 10.0, MID])[0]


def test_material_remains_between_the_holes(cord):
    assert inside(cord, [0.0, 0.0, MID])[0]
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
cd down-indicator && .venv/bin/pytest tests/test_cord_slots.py -q
```

Expected: FAIL — `cord_only.scad` does not exist, so every test fails in the fixture with OpenSCAD's "Can't open input file".

- [ ] **Step 4: Write the model**

`down-indicator/lib/cord_slots.scad`:

```openscad
// The cord holes and the face troughs that open them to the ends.
//
// Everything here is a cutting tool, meant for the negative half of a
// difference() against the body.

// Two through-bores of diameter `dia`, on the Y centreline at +-holeY.
module cord_cutter(len, t, dia, holeY) {
    for (s = [-1, 1])
        translate([0, s * holeY, -1]) cylinder(h = t + 2, d = dia);
}
```

`down-indicator/tests/scad/cord_only.scad`:

```openscad
use <../../lib/body.scad>
use <../../lib/cord_slots.scad>

bodyLen = 40.0;
bodyWid = 30.0;
bodyT   =  6.7;
cordDia =  7.0;
holeY   = 10.0;
$fn = 96;

difference() {
    body_blank(bodyLen, bodyWid, bodyT);
    cord_cutter(bodyLen, bodyT, cordDia, holeY);
}
```

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 9 tests. `cord.volume` is 7524.6756mm³; the removed 515.3244mm³ matches the closed form to six significant figures.

- [ ] **Step 6: Commit**

```bash
git add down-indicator/
git commit -m "feat(down-indicator): add the two 7mm cord holes"
```

---

### Task 3: Cord slot troughs

The heart of the part. A trough of the same 7mm diameter is cut into the watch face and into the wrist side, running from each hole out to the body end. Because the body is thinner than the trough diameter the two overlap at mid-thickness, leaving a slot the cord presses into from the side.

**Files:**
- Modify: `down-indicator/lib/cord_slots.scad`
- Modify: `down-indicator/tests/test_cord_slots.py`

**Interfaces:**
- Consumes: `cord_cutter(len, t, dia, holeY)` from Task 2.
- Produces: `cord_trough(len, t, dia, holeY, s)` — one face-pair of troughs for the hole on side `s` (`+1` for the +Y hole, `-1` for the −Y hole), running from that hole's centre out past the end face. Called by `cord_cutter`, which keeps its Task 2 signature.

- [ ] **Step 1: Retire the superseded hole-volume test**

Delete `test_holes_remove_exactly_two_cylinders` from `down-indicator/tests/test_cord_slots.py`, and delete the now-unused `HOLE_AREA` constant and the `import math`-dependent comment above it. Keep `import math` — the neck arithmetic below needs it.

That test asserts `BLANK_VOLUME - cord.volume == 515.3244`. This task adds troughs to the same `cord_cutter`, so the figure becomes 1050.79 and the two assertions contradict each other. After this task the holes are no longer a separable feature of `cord_cutter`, so the hole-only volume cannot be observed from the `cord_only` harness without duplicating cylinder geometry into a second harness. `test_holes_and_troughs_together` below carries the combined closed-form check forward; `test_holes_are_seven_millimetres_across` and `test_each_hole_goes_all_the_way_through` keep pinning hole geometry directly and both still pass once the troughs exist.

- [ ] **Step 2: Write the failing test**

Append to `down-indicator/tests/test_cord_slots.py`:

```python
# Where the two face troughs overlap, at mid-thickness:
#   neck = 2 * sqrt(r^2 - (t/2)^2) = 2.0273mm
NECK = 2 * math.sqrt(CORD_R**2 - (BODY_T / 2) ** 2)


def test_the_arithmetic_the_thickness_was_chosen_for():
    assert NECK == approx(2.027, abs=0.001)


def test_the_slot_is_open_from_the_hole_to_the_end(cord):
    """No solid anywhere on the slot centreline at mid-thickness."""
    for sign in (-1, 1):
        ys = np.linspace(sign * 10.0, sign * 20.0, 41)
        points = [[0.0, y, MID] for y in ys]
        assert not inside(cord, *points).any()


def test_the_neck_is_the_width_the_geometry_predicts(cord):
    y = 16.0  # midway between the hole edge and the body end
    assert not inside(cord, [NECK / 2 - 0.1, y, MID])[0], "neck is narrower than predicted"
    assert inside(cord, [NECK / 2 + 0.1, y, MID])[0], "neck is wider than predicted"


def test_the_trough_is_full_width_at_both_faces(cord):
    y = 16.0
    for z in (0.05, BODY_T - 0.05):
        assert not inside(cord, [3.3, y, z])[0], "trough is not 7mm wide at the face"
        assert inside(cord, [3.7, y, z])[0], "trough is wider than 7mm at the face"


def test_the_troughs_run_outward_not_inward(cord):
    """Between the two holes the body is untouched at every height."""
    for z in (0.05, MID, BODY_T - 0.05):
        assert inside(cord, [0.0, 0.0, z])[0]


def test_holes_and_troughs_together(cord):
    assert cord.volume == approx(6989.209, rel=1e-4)
    assert cord.is_watertight
    assert cord.body_count == 1
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
cd down-indicator && .venv/bin/pytest tests/test_cord_slots.py -q
```

Expected: FAIL. `test_the_arithmetic_the_thickness_was_chosen_for` passes (it is pure arithmetic), and the five geometry tests fail — the slot centreline is solid, so `test_the_slot_is_open_from_the_hole_to_the_end` fails first.

- [ ] **Step 4: Write the model**

Replace the contents of `down-indicator/lib/cord_slots.scad`:

```openscad
// The cord holes and the face troughs that open them to the ends.
//
// Everything here is a cutting tool, meant for the negative half of a
// difference() against the body.
//
// Each hole is a through-bore of diameter `dia`. From each hole a trough of
// the same diameter runs outward along Y, cut into the watch face (axis at
// z = t) and into the wrist side (axis at z = 0). Because t < dia the two
// troughs overlap at mid-thickness, so the slot is open end to end and the
// cord presses in from the side rather than being threaded.
//
// The neck left at mid-thickness is 2 * sqrt((dia/2)^2 - (t/2)^2); at
// dia = 7.0 and t = 6.7 that is 2.027mm. The caller is responsible for
// asserting t < dia -- at t == dia the troughs meet along a knife edge and
// the slot has zero width.

module cord_cutter(len, t, dia, holeY) {
    for (s = [-1, 1]) {
        translate([0, s * holeY, -1]) cylinder(h = t + 2, d = dia);
        cord_trough(len, t, dia, holeY, s);
    }
}

// One face-pair of troughs, for the hole on side `s`. Runs from the hole
// centre out to 1mm past the end face, so the slot exits cleanly.
module cord_trough(len, t, dia, holeY, s) {
    run = len / 2 + 1 - holeY;
    for (z = [0, t])
        translate([0, s * holeY, z])
            rotate([-90 * s, 0, 0])
                cylinder(h = run, d = dia);
}
```

`rotate([-90 * s, 0, 0])` turns the cylinder's +Z axis into +Y for `s = 1` and into −Y for `s = -1`, so each hole's troughs run toward its own end of the body.

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 14 tests (the retired hole-volume test brings the file to 10).

- [ ] **Step 6: Commit**

```bash
git add down-indicator/
git commit -m "feat(down-indicator): open the cord holes to the ends with face troughs"
```

---

### Task 4: Spring-bar lug horns

The additive half of the band mount: four horns, flush with the side walls, protruding 6.5mm past each end. Geometry carried over from the down counter's lug spec, with horn thickness re-derived for a 30mm end.

**Files:**
- Create: `down-indicator/lib/lugs.scad`
- Create: `down-indicator/tests/scad/lugs_only.scad`
- Create: `down-indicator/tests/test_lugs.py`
- Modify: `down-indicator/tests/conftest.py` (add the `lugs` fixture)

Probe solid horn material at `HORN_Y = 22.0`, never at `BAR_Y = 24.5`. Task 5 drills a bore straight along X at `BAR_Y` and `z = t/2`, so any "this should be solid" probe placed there passes now and starts failing the moment the bores land.

**Interfaces:**
- Consumes: `body_blank(len, wid, t)` from Task 1.
- Produces: `lug_horns(len, wid, t, gap, prot, tipCham)` — four additive horns; `horn_profile(thk, prot, cham, sy)` — the plan-view outline of one horn, with its far-end corners chamfered, pointing in the `sy` direction.

- [ ] **Step 1: Add the fixture**

Append to `down-indicator/tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def lugs():
    return render("tests/scad/lugs_only.scad")
```

- [ ] **Step 2: Write the failing test**

`down-indicator/tests/test_lugs.py`:

```python
"""Spring-bar lugs, carried over from the down counter's as-built geometry."""

from pytest import approx

from conftest import inside

BODY_T = 6.7
MID = BODY_T / 2
GAP = 20.2          # 20mm band + 0.2mm clearance
HORN_THK = 4.9      # (30 - 20.2) / 2
PROT = 6.5          # 4.5mm bar standoff + 2.0mm tip margin
BAR_Y = 24.5        # 20 + 4.5, where Task 5 drills the bore
HORN_Y = 22.0       # solid horn, clear of the bore -- probe material here
BLANK_VOLUME = 30.0 * 40.0 * 6.7


def test_lug_body_is_one_closed_solid(lugs):
    assert lugs.is_watertight
    assert lugs.body_count == 1


def test_lug_to_lug_is_fifty_three_millimetres(lugs):
    low, high = lugs.bounds
    assert high[1] - low[1] == approx(53.0, abs=1e-6)
    assert list(low) == approx([-15.0, -26.5, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 26.5, 6.7], abs=1e-6)


def test_horns_add_four_chamfered_prisms(lugs):
    # 4 horns, less a 0.5mm chamfer on each of the two tip corners per horn.
    expected = 4 * HORN_THK * PROT * BODY_T - 4 * 2 * (0.5 * 0.5**2) * BODY_T
    assert lugs.volume - BLANK_VOLUME == approx(expected, rel=1e-6)


def test_the_band_gap_takes_a_twenty_millimetre_strap(lugs):
    # Open across the full gap...
    assert not inside(lugs, [0.0, HORN_Y, MID], [10.0, HORN_Y, MID], [-10.0, HORN_Y, MID]).any()
    # ...and solid immediately outboard of it.
    assert inside(lugs, [10.3, HORN_Y, MID], [-10.3, HORN_Y, MID]).all()


def test_horns_run_flush_to_the_side_walls(lugs):
    assert inside(lugs, [14.8, HORN_Y, MID])[0]
    assert not inside(lugs, [15.2, HORN_Y, MID])[0]


def test_horns_are_full_body_height(lugs):
    assert inside(lugs, [12.5, HORN_Y, 0.1], [12.5, HORN_Y, BODY_T - 0.1]).all()
    assert not inside(lugs, [12.5, HORN_Y, -0.1], [12.5, HORN_Y, BODY_T + 0.1]).any()


def test_tip_corners_are_chamfered(lugs):
    # The outboard tip corner at (15, 26.5) is cut back by 0.5mm.
    assert not inside(lugs, [14.9, 26.4, MID])[0]
    assert inside(lugs, [14.3, 26.4, MID])[0]
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
cd down-indicator && .venv/bin/pytest tests/test_lugs.py -q
```

Expected: FAIL, 7 tests — `lugs_only.scad` does not exist.

- [ ] **Step 4: Write the model**

`down-indicator/lib/lugs.scad`:

```openscad
// Spring-bar lugs, carried over from the down counter's as-built geometry
// (see 2026-08-22-band-lugs-design.md): horns flush with the side walls,
// squared roots, 0.5mm tip chamfers.
//
// Horn thickness is derived, not a parameter -- the horns always run from the
// band gap out to the side walls, so widening the band thins them.

// Four horns, one at each corner, protruding `prot` past each end face.
module lug_horns(len, wid, t, gap, prot, tipCham) {
    hornThk = (wid - gap) / 2;
    ol = 0.5;   // root overlap into the body, so the union is not face-coincident
    for (sy = [-1, 1], sx = [-1, 1])
        translate([sx * (gap / 2 + hornThk / 2),
                   sy * (len / 2 - ol / 2 + prot / 2),
                   0])
            linear_extrude(height = t)
                horn_profile(hornThk, prot + ol, tipCham, sy);
}

// Plan-view outline of one horn: a thk x prot rectangle whose two far-end
// corners are chamfered by `cham`. `sy` selects which end is the tip.
module horn_profile(thk, prot, cham, sy) {
    y0 = -sy * prot / 2;   // rooted end
    y1 =  sy * prot / 2;   // tip end
    polygon([
        [-thk / 2,        y0],
        [ thk / 2,        y0],
        [ thk / 2,        y1 - sy * cham],
        [ thk / 2 - cham, y1],
        [-thk / 2 + cham, y1],
        [-thk / 2,        y1 - sy * cham],
    ]);
}
```

The 0.5mm root overlap matters: butting the horn's root face exactly against the body's end face gives CGAL two coincident planes to union, which is a well-known source of non-manifold output. Overlapping is free — the extra material is inside the body.

`down-indicator/tests/scad/lugs_only.scad`:

```openscad
use <../../lib/body.scad>
use <../../lib/lugs.scad>

bodyLen    = 40.0;
bodyWid    = 30.0;
bodyT      =  6.7;
lugGap     = 20.2;
hornProt   =  6.5;
tipChamfer =  0.5;
$fn = 96;

union() {
    body_blank(bodyLen, bodyWid, bodyT);
    lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
}
```

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 22 tests. `lugs.volume` is 8886.88mm³, exactly 846.88mm³ over the blank.

- [ ] **Step 6: Commit**

```bash
git add down-indicator/
git commit -m "feat(down-indicator): add 20mm spring-bar lug horns"
```

---

### Task 5: Teardrop spring-bar bores

The subtractive half of the band mount. The bore axis is horizontal when the case prints flat, so a round hole would put an unsupported crown at the top of the circle. The teardrop replaces it with two flanks tangent at 45 degrees, apex toward −Z.

**Files:**
- Create: `down-indicator/lib/util.scad`
- Modify: `down-indicator/lib/lugs.scad`
- Modify: `down-indicator/tests/scad/lugs_only.scad`
- Modify: `down-indicator/tests/test_lugs.py`

**Interfaces:**
- Consumes: `lug_horns(...)` from Task 4.
- Produces:
  - `teardrop_2d(r)` — a 2D circle of radius `r` with a self-supporting apex at `(0, r * sqrt(2))`.
  - `teardrop_bore(d, h)` — that profile extruded `h` along +Z, apex toward +Y in the local frame.
  - `bar_bores(len, wid, t, gap, standoff, dia, apexDown)` — four bores, one per horn, run along X at `y = ±(len/2 + standoff)` and `z = t/2`. Subtractive.

- [ ] **Step 1: Write the failing test**

Append to `down-indicator/tests/test_lugs.py`:

```python
BAR_R = 0.55        # 1.1mm bore
HORNS_VOLUME = 8886.88


def test_the_bore_runs_right_through_the_horn(lugs):
    row = [[x, BAR_Y, MID] for x in (10.5, 12.5, 14.5)]
    assert not inside(lugs, *row).any()


def test_the_bore_sits_at_mid_height_with_material_above_and_below(lugs):
    assert inside(lugs, [12.5, BAR_Y, MID + 1.5], [12.5, BAR_Y, MID - 1.5]).all()


def test_the_bore_is_offset_from_the_tip_by_the_margin(lugs):
    # 2mm of material past the bore centre, so the tip at y = 26.5 is solid.
    assert inside(lugs, [12.5, 26.2, MID])[0]


def test_the_teardrop_apex_points_toward_the_wrist_side(lugs):
    """Apex at r*sqrt(2) below centre; the matching point above is solid."""
    reach = BAR_R * 1.35   # inside r*sqrt(2) = 0.778, outside r = 0.55
    assert not inside(lugs, [12.5, BAR_Y, MID - reach])[0], "no apex on the -Z side"
    assert inside(lugs, [12.5, BAR_Y, MID + reach])[0], "apex is on the wrong side"


def test_bores_remove_four_small_teardrops(lugs):
    # Teardrop area is r^2 * (3*pi/4 + 1); four bores through 4.9mm of horn.
    expected = 4 * (BAR_R**2 * (3 * math.pi / 4 + 1)) * HORN_THK
    assert HORNS_VOLUME - lugs.volume == approx(expected, rel=0.02)


def test_lug_body_is_still_one_closed_solid(lugs):
    assert lugs.is_watertight
    assert lugs.body_count == 1
```

Add `import math` to the top of the file alongside the existing imports.

`test_horns_add_four_chamfered_prisms` from Task 4 now measures a body that has bores in it and must be updated to subtract them. Replace it with:

```python
def test_horns_add_four_chamfered_prisms(lugs):
    # 4 horns, less a 0.5mm chamfer on each of the two tip corners per horn,
    # less the four bar bores.
    horns = 4 * HORN_THK * PROT * BODY_T - 4 * 2 * (0.5 * 0.5**2) * BODY_T
    bores = 4 * (BAR_R**2 * (3 * math.pi / 4 + 1)) * HORN_THK
    assert lugs.volume - BLANK_VOLUME == approx(horns - bores, rel=0.001)
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd down-indicator && .venv/bin/pytest tests/test_lugs.py -q
```

Expected: FAIL, 6 of the new tests plus the rewritten volume test — the horns are still solid, so `test_the_bore_runs_right_through_the_horn` reports every probe inside the solid.

- [ ] **Step 3: Write the teardrop helper**

`down-indicator/lib/util.scad`:

```openscad
// Shared profiles.

// A circle of radius r with a self-supporting apex: two flanks tangent to the
// bore at 45 degrees, meeting r * sqrt(2) from the centre. Printed with the
// apex upward, it replaces the unsupported crown of a horizontal round hole.
// Apex toward +Y.
module teardrop_2d(r) {
    union() {
        circle(r = r);
        rotate([0, 0, 45]) square([r, r]);
    }
}

// That profile as a bore of diameter d and length h, extruded along +Z.
module teardrop_bore(d, h) {
    linear_extrude(height = h) teardrop_2d(d / 2);
}
```

The rotated square's two near corners land at `(±r/sqrt(2), r/sqrt(2))`, which lie exactly on the circle — that is what makes the flanks tangent rather than secant.

- [ ] **Step 4: Write the bores**

Add to the top of `down-indicator/lib/lugs.scad`:

```openscad
use <util.scad>
```

Append to `down-indicator/lib/lugs.scad`:

```openscad
// Spring-bar bores, one per horn, running along X at z = t/2 and
// y = +-(len/2 + standoff). Teardropped so the crown is self-supporting when
// the case prints face down; `apexDown` puts the apex toward the wrist side,
// which is the upward direction in that orientation.
module bar_bores(len, wid, t, gap, standoff, dia, apexDown) {
    hornThk = (wid - gap) / 2;
    for (sy = [-1, 1], sx = [-1, 1])
        translate([sx * (gap / 2 - 1), sy * (len / 2 + standoff), t / 2])
            rotate([0, sx * 90, 0])
                rotate([0, 0, (apexDown ? -90 : 90) * sx])
                    teardrop_bore(dia, hornThk + 2);
}
```

The two nested rotations do different jobs and the order matters. The inner one spins the teardrop within its own profile plane so the apex ends up along the local X axis; the outer one lays the bore axis down onto world X. Both are signed by `sx`, because mirroring the horn to the other side of the part also mirrors which way "apex down" turns out to be.

Update `down-indicator/tests/scad/lugs_only.scad` to subtract them:

```openscad
use <../../lib/body.scad>
use <../../lib/lugs.scad>

bodyLen      = 40.0;
bodyWid      = 30.0;
bodyT        =  6.7;
lugGap       = 20.2;
hornProt     =  6.5;
tipChamfer   =  0.5;
barStandoff  =  4.5;
barHoleDia   =  1.1;
teardropDown = true;
$fn = 96;

difference() {
    union() {
        body_blank(bodyLen, bodyWid, bodyT);
        lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
    }
    bar_bores(bodyLen, bodyWid, bodyT, lugGap, barStandoff, barHoleDia, teardropDown);
}
```

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 27 tests. `lugs.volume` drops from 8886.88 to 8866.992mm³.

- [ ] **Step 6: Check the apex flips with the parameter**

Add to `down-indicator/tests/test_lugs.py`:

```python
def test_teardrop_can_be_flipped_for_the_other_print_orientation():
    from conftest import render

    flipped = render("tests/scad/lugs_only.scad", teardropDown=False)
    reach = BAR_R * 1.35
    assert not inside(flipped, [12.5, BAR_Y, MID + reach])[0]
    assert inside(flipped, [12.5, BAR_Y, MID - reach])[0]
```

Run it:

```bash
cd down-indicator && .venv/bin/pytest tests/test_lugs.py -q
```

Expected: PASS, 28 tests. This is also the first exercise of the `-D` override path, which Task 6 depends on entirely.

- [ ] **Step 7: Commit**

```bash
git add down-indicator/
git commit -m "feat(down-indicator): add teardrop spring-bar bores"
```

---

### Task 6: Assembly, parameter guards, and documentation

Brings the three subsystems together into the shipping model, adds the `assert()` guards that reject unbuildable parameter combinations, and documents the result.

**Files:**
- Create: `down-indicator/down_indicator.scad`
- Create: `down-indicator/tests/test_assembly.py`
- Create: `down-indicator/README.md`
- Modify: `down-indicator/tests/conftest.py` (add the `part` fixture)
- Modify: `README.md` (repository root)

**Interfaces:**
- Consumes: `body_blank`, `cord_cutter`, `lug_horns`, `bar_bores` — all as defined in Tasks 1–5, unchanged.
- Produces: `down_indicator()` — the complete part, and the top-level parameter block that `-D` overrides target.

- [ ] **Step 1: Add the fixture**

Append to `down-indicator/tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def part():
    return render("down_indicator.scad")
```

- [ ] **Step 2: Write the failing test**

`down-indicator/tests/test_assembly.py`:

```python
"""The complete part, and the guards on its parameters."""

import math

from pytest import approx

from conftest import inside, render, render_failure

BODY_T = 6.7
MID = BODY_T / 2
NECK = 2 * math.sqrt(3.5**2 - (BODY_T / 2) ** 2)
BAR_Y = 24.5


def test_the_part_is_one_closed_printable_solid(part):
    assert part.is_watertight
    assert part.is_winding_consistent
    assert part.body_count == 1
    assert part.volume == approx(7816.2, rel=1e-4)


def test_overall_dimensions(part):
    low, high = part.bounds
    assert list(low) == approx([-15.0, -26.5, 0.0], abs=1e-6)
    assert list(high) == approx([15.0, 26.5, 6.7], abs=1e-6)


def test_the_cord_slots_survive_the_assembly(part):
    for sign in (-1, 1):
        run = [[0.0, sign * y, MID] for y in (10.0, 13.0, 16.0, 19.0, 20.0)]
        assert not inside(part, *run).any()
    assert not inside(part, [NECK / 2 - 0.1, 16.0, MID])[0]
    assert inside(part, [NECK / 2 + 0.1, 16.0, MID])[0]


def test_the_slot_exits_inside_the_band_gap_and_clears_the_horns(part):
    """Slot spans x +-3.5; the gap spans x +-10.1. Nothing between them is cut."""
    assert not inside(part, [0.0, 20.5, MID])[0], "slot does not exit the end"
    assert inside(part, [12.5, 22.0, MID])[0], "the slot has eaten into a horn"


def test_the_lugs_survive_the_assembly(part):
    assert not inside(part, [12.5, BAR_Y, MID])[0], "bore is blocked"
    assert inside(part, [12.5, BAR_Y, MID + 1.5])[0], "horn material is missing"


def test_a_body_as_thick_as_the_cord_is_rejected():
    err = render_failure("down_indicator.scad", bodyT=8.0)
    assert "bodyT must be less than cordDia" in err


def test_a_band_too_wide_for_the_end_is_rejected():
    err = render_failure("down_indicator.scad", bandWidth=24)
    assert "horn thickness" in err


def test_holes_that_break_out_of_the_end_are_rejected():
    err = render_failure("down_indicator.scad", holeY=17)
    assert "cord holes break out" in err


def test_a_thinner_body_still_builds_and_widens_the_neck():
    thin = render("down_indicator.scad", bodyT=6.4)
    wider = 2 * math.sqrt(3.5**2 - (6.4 / 2) ** 2)
    assert wider > NECK
    assert thin.is_watertight
    assert not inside(thin, [wider / 2 - 0.1, 16.0, 6.4 / 2])[0]
```

- [ ] **Step 3: Run the test to verify it fails**

```bash
cd down-indicator && .venv/bin/pytest tests/test_assembly.py -q
```

Expected: FAIL — `down_indicator.scad` does not exist.

- [ ] **Step 4: Write the assembly**

`down-indicator/down_indicator.scad`:

```openscad
// Finger-loop down indicator.
//
// A wrist-worn body carrying a bungee cord that loops over the back of the
// hand and around a finger; which finger the loop sits on is the down.
// See ../2026-08-24-finger-loop-indicator-design.md.
//
// Coordinates: +X across the wrist, +Y along the forearm toward the hand,
// +Z out of the watch face. The body sits on z = 0 (wrist side).

use <lib/body.scad>
use <lib/cord_slots.scad>
use <lib/lugs.scad>

/* [Body] */
bodyLen = 40.0;   // along the forearm
bodyWid = 30.0;   // across the wrist
bodyT   =  6.7;   // derived from cordDia -- see the neck assertion below

/* [Cord] */
cordDia =  7.0;   // hole diameter, and trough diameter
holeY   = 10.0;   // hole centres at (0, +holeY) and (0, -holeY)

/* [Lugs] */
bandWidth    = 20.0;
bandClear    =  0.2;   // added to bandWidth for the lug gap
barStandoff  =  4.5;
tipMargin    =  2.0;
barHoleDia   =  1.1;
tipChamfer   =  0.5;
teardropDown = true;   // apex toward the wrist side, for a face-down print

/* [Quality] */
$fn = 96;

/* [Hidden] */
lugGap   = bandWidth + bandClear;
hornThk  = (bodyWid - lugGap) / 2;
hornProt = barStandoff + tipMargin;
lugToLug = bodyLen + 2 * hornProt;
cordNeck = 2 * sqrt(pow(cordDia / 2, 2) - pow(bodyT / 2, 2));

assert(bodyT < cordDia,
       "bodyT must be less than cordDia or the face troughs never meet");
assert(cordNeck >= 1.2 && cordNeck <= 3.5,
       str("cord neck ", cordNeck, "mm is outside the 1.2-3.5mm usable range"));
assert(hornThk >= 4.0,
       str("horn thickness ", hornThk, "mm is too thin; reduce bandWidth"));
assert(holeY + cordDia / 2 < bodyLen / 2,
       "cord holes break out of the body end");

echo(cordNeck = cordNeck, hornThk = hornThk, lugToLug = lugToLug);

down_indicator();

module down_indicator() {
    difference() {
        union() {
            body_blank(bodyLen, bodyWid, bodyT);
            lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
        }
        cord_cutter(bodyLen, bodyT, cordDia, holeY);
        bar_bores(bodyLen, bodyWid, bodyT, lugGap,
                  barStandoff, barHoleDia, teardropDown);
    }
}
```

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd down-indicator && make test
```

Expected: PASS, 37 tests. The echo line reads `cordNeck = 2.02731, hornThk = 4.9, lugToLug = 53`.

- [ ] **Step 6: Export the STL and confirm the build target works**

```bash
cd down-indicator && make stl && ls -l build/down_indicator.stl
```

Expected: `build/down_indicator.stl` exists, roughly 380KB.

- [ ] **Step 7: Write the project README**

`down-indicator/README.md`:

```markdown
# Finger-Loop Down Indicator — OpenSCAD model

A wrist-worn body that anchors a bungee cord looping over the back of the hand
and around a finger. Which finger the loop sits on is the down.

Design and reasoning: [../2026-08-24-finger-loop-indicator-design.md](../2026-08-24-finger-loop-indicator-design.md).

## Build

    make stl      # -> build/down_indicator.stl
    make test     # render the model and assert against the mesh
    make clean

`make` creates `.venv` on first use and installs the pinned dependencies from
`requirements.txt`.

## Parameters

Every parameter is declared at the top of `down_indicator.scad` and can be
overridden without editing the file:

    openscad -o build/wide.stl -D bandWidth=18 down_indicator.scad

| Parameter | Default | Notes |
| --- | --- | --- |
| `bodyLen` | 40.0 | Along the forearm |
| `bodyWid` | 30.0 | Across the wrist |
| `bodyT` | 6.7 | Must be less than `cordDia`, or the slots never open |
| `cordDia` | 7.0 | Hole and trough diameter |
| `holeY` | 10.0 | Hole centres |
| `bandWidth` | 20.0 | 18 if the 4.9mm horns prove marginal |
| `barStandoff` | 4.5 | |
| `tipMargin` | 2.0 | |
| `barHoleDia` | 1.1 | |
| `tipChamfer` | 0.5 | |
| `teardropDown` | true | Apex toward the wrist side, for a face-down print |

Four combinations are rejected outright rather than silently producing an
unbuildable part: a body at or thicker than the cord diameter, a cord neck
outside 1.2–3.5mm, horns thinner than 4.0mm, and holes that break out of the
end.

## Print

Face down — the `z = bodyT` face on the bed. That puts strap tension along the
layers and makes the teardrop bores self-supporting.
```

- [ ] **Step 8: Add it to the repository README**

In the root `README.md`, add a row to the Contents table:

```markdown
| [2026-08-24-finger-loop-indicator-design.md](2026-08-24-finger-loop-indicator-design.md) | Design for the finger-loop down indicator: a wrist body anchoring a bungee cord that loops over a finger. Modelled in OpenSCAD under `down-indicator/`, not in Onshape. |
| [down-indicator/](down-indicator/) | The OpenSCAD model for the above, with a `pytest` suite that renders it and asserts against the mesh. |
```

And add a section after "The mechanical slider down counter":

```markdown
## The finger-loop down indicator

A third device, and the first one whose model is version-controlled here
rather than living in Onshape. A 40 x 30 x 6.7mm body on a 20mm watch strap,
with two 7mm holes opening through side-loading slots to each end; a bungee
cord presses into the slots, runs over the back of the hand and loops over a
finger. The finger is the down selector.

It reuses the down counter's spring-bar lug geometry — 20mm band, 20.2mm gap,
teardrop bores — and nothing else. Its footprint is its own.

See [the design](2026-08-24-finger-loop-indicator-design.md) and
[down-indicator/README.md](down-indicator/README.md).
```

- [ ] **Step 9: Run the whole suite once more**

```bash
cd down-indicator && make test
```

Expected: PASS, 37 tests.

- [ ] **Step 10: Commit**

```bash
git add down-indicator/ README.md
git commit -m "feat(down-indicator): assemble the part, guard its parameters, document it"
```

---

## After the plan

The spec lists three things software cannot settle, all of which need a print:

1. Whether a 2.027mm neck holds a real bungee. Print a slot coupon first.
2. Whether 4.9mm horns survive a wrist. Print a single-end test piece with a real spring bar, as the down counter's lug spec also still owes.
3. Whether the cord binds where it exits under the strap. If it does, the fix is moving the holes off the Y centreline so the slots exit a side edge instead — a parameter change plus a slot direction, not a redesign.
