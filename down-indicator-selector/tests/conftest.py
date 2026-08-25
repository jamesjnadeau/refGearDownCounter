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
REFERENCE = ROOT / "reference"


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
        elif isinstance(value, (list, tuple)):
            value = "[" + ",".join(str(v) for v in value) + "]"
        elif isinstance(value, str):
            value = f'"{value}"'
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
        # OpenSCAD exits 0 on a self-intersecting or non-closed mesh, having
        # said so only on stderr, so the exit code alone is not enough. A
        # missing font is a warning too, and would quietly reshape the
        # numerals, so that has to fail the suite as well.
        output = proc.stdout + proc.stderr
        complaint = next(
            (line for line in output.splitlines()
             if "ERROR:" in line or "WARNING:" in line),
            None,
        )
        if proc.returncode != 0 or not out_path.exists() or complaint:
            out_path.unlink(missing_ok=True)
            pytest.fail(
                f"OpenSCAD failed on {scad_relpath} {defines}"
                + (f"\nfirst complaint: {complaint}" if complaint else "")
                + f"\n{proc.stdout}\n{proc.stderr}"
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


def _solid_at(mesh, axis, at, z, t):
    points = np.zeros((len(t), 3))
    points[:, 2] = z
    points[:, axis] = t
    points[:, 1 - axis] = at
    return mesh.contains(points)


def walls(mesh, axis, at, z, lo, hi, samples=2001, tol=1e-5):
    """Where a line crossing the part changes between air and material.

    Walks `axis` (0 for x, 1 for y) from `lo` to `hi` with the other in-plane
    coordinate pinned to `at`, and returns the crossings in order. A cut
    through one side of the shell gives two: the outer wall and the cavity.

    The coarse walk only brackets each crossing; each bracket is then bisected
    down to `tol`, so a result can be compared against a nominal dimension
    rather than against the step the walk happened to use.
    """
    t = np.linspace(lo, hi, samples)
    solid = _solid_at(mesh, axis, at, z, t)
    edges = np.flatnonzero(np.diff(solid))
    low, high = t[edges], t[edges + 1]
    while len(low) and (high - low).max() > tol:
        mid = (low + high) / 2
        hit = _solid_at(mesh, axis, at, z, mid)
        entering = solid[edges]          # False on the way in, True on the way out
        keep_low = hit == entering
        low = np.where(keep_low, mid, low)
        high = np.where(keep_low, high, mid)
    return (low + high) / 2


def section_area(mesh, z) -> float:
    """Area of the solid's cross-section at height z.

    Sums the signed area contributed by every triangle the plane cuts,
    orienting each cut segment so material lies to its left. That needs no
    loop-finding, so it works on meshes with holes and islands in them.
    """
    tri = mesh.vertices[mesh.faces]
    normals = mesh.face_normals
    height = tri[:, :, 2] - z
    crossing = (height.min(axis=1) < 0) & (height.max(axis=1) > 0)
    total = 0.0
    for corners, normal, hs in zip(tri[crossing], normals[crossing], height[crossing]):
        cut = []
        for i in range(3):
            j = (i + 1) % 3
            if hs[i] * hs[j] < 0:
                t = hs[i] / (hs[i] - hs[j])
                cut.append(corners[i] + t * (corners[j] - corners[i]))
        if len(cut) != 2:
            continue
        a, b = cut[0][:2], cut[1][:2]
        if np.dot(b - a, np.array([-normal[1], normal[0]])) < 0:
            a, b = b, a
        total += 0.5 * (a[0] * b[1] - b[0] * a[1])
    return total


@pytest.fixture(scope="session")
def part():
    return render("down_indicator_selector.scad")


@pytest.fixture(scope="session")
def blank():
    return render("tests/scad/blank_only.scad")


@pytest.fixture(scope="session")
def unmarked():
    """The part with the numerals left off, so the typeface is out of the way."""
    return render("down_indicator_selector.scad", textCentres=[])


def _reference(name):
    path = REFERENCE / f"onshape-{name}.stl"
    if not path.exists():
        pytest.skip(f"no reference mesh at {path}")
    return trimesh.load(path, force="mesh")


@pytest.fixture(scope="session")
def onshape():
    return _reference("top")


@pytest.fixture(scope="session")
def onshape_bottom():
    return _reference("bottom")


@pytest.fixture(scope="session")
def onshape_button():
    return _reference("button")


@pytest.fixture(scope="session")
def bottom():
    return render("down_indicator_selector_bottom.scad")


@pytest.fixture(scope="session")
def button():
    return render("down_indicator_selector_button.scad")


@pytest.fixture(scope="session")
def untied():
    """The part with the 4 cut as the original cuts it, tie and all left off."""
    return render("down_indicator_selector.scad", tiedNumeral=0)
