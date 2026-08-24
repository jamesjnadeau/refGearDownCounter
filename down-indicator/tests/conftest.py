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


@pytest.fixture(scope="session")
def cord():
    return render("tests/scad/cord_only.scad")


@pytest.fixture(scope="session")
def lugs():
    return render("tests/scad/lugs_only.scad")


@pytest.fixture(scope="session")
def part():
    return render("down_indicator.scad")
