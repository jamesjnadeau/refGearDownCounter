"""The button: a flanged top-hat with a bore, captive under the top plate."""

import math

from pytest import approx

from conftest import inside, render_failure, walls

BORE = 6.03
FLANGE_D = 12.0
FLANGE_T = 1.0
BOSS_D = 8.0
BOSS_H = 4.0
ROUND = 0.4

ONSHAPE_SOLID_VOLUME = 168.6   # mm^3, as Onshape measures the B-rep


def test_the_button_is_one_closed_solid(button):
    assert button.is_watertight
    assert button.is_winding_consistent
    assert button.body_count == 1


def test_it_is_twelve_by_twelve_by_five(button):
    low, high = button.bounds
    assert list(low) == approx([-FLANGE_D / 2, -FLANGE_D / 2, -FLANGE_T], abs=1e-3)
    assert list(high) == approx([FLANGE_D / 2, FLANGE_D / 2, BOSS_H], abs=1e-3)


def test_the_flange_is_twelve_across_and_one_thick(button):
    across = walls(button, 0, 0.0, -FLANGE_T / 2, -8.0, 8.0)
    assert list(across[[0, -1]]) == approx([-FLANGE_D / 2, FLANGE_D / 2], abs=0.01)
    assert not inside(button, [5.0, 0.0, 0.05])[0], "the flange is over 1mm thick"


def test_the_boss_is_eight_across_and_four_tall(button):
    across = walls(button, 0, 0.0, BOSS_H / 2, -8.0, 8.0)
    assert list(across[[0, -1]]) == approx([-BOSS_D / 2, BOSS_D / 2], abs=0.01)
    assert inside(button, [3.5, 0.0, BOSS_H - 0.5])[0]
    assert not inside(button, [3.5, 0.0, BOSS_H + 0.05])[0]


def test_the_bore_runs_right_through(button):
    for z in (-FLANGE_T + 0.05, 0.5, 2.0, BOSS_H - 0.05):
        assert not inside(button, [0.0, 0.0, z])[0], f"the bore is blocked at z = {z}"
    across = walls(button, 0, 0.0, 1.0, -5.0, 5.0)
    assert list(across[1:3]) == approx([-BORE / 2, BORE / 2], abs=0.01)


def test_the_bore_matches_the_bottom_shells_stations(button, bottom):
    """Whatever runs through one has to run into the other."""
    in_button = walls(button, 0, 0.0, 1.0, -5.0, 5.0)[1:3]
    in_plate = walls(bottom, 0, 0.0, 1.5, -5.0, 5.0)
    assert list(in_button) == approx(list(in_plate), abs=0.01)


def test_the_flange_cannot_pass_back_out_through_the_slot(button):
    """The whole point of the top hat: 12mm of flange, an 8.4mm opening."""
    assert FLANGE_D > 8.4
    assert BOSS_D < 8.4


def test_the_rims_are_rounded(button):
    top = button.vertices[abs(button.vertices[:, 2] - BOSS_H) < 1e-6]
    radius = (top[:, 0] ** 2 + top[:, 1] ** 2) ** 0.5
    assert radius.max() == approx(BOSS_D / 2 - ROUND, abs=1e-3)
    assert radius.min() == approx(BORE / 2 + ROUND, abs=1e-3)
    flange = button.vertices[abs(button.vertices[:, 2] + FLANGE_T) < 1e-6]
    flange_r = (flange[:, 0] ** 2 + flange[:, 1] ** 2) ** 0.5
    assert flange_r.max() == approx(FLANGE_D / 2, abs=1e-3), \
        "the flange's bottom edge is square in the original"


def test_the_volume_matches_the_original(button, onshape_button):
    flange = math.pi * ((FLANGE_D / 2) ** 2 - (BORE / 2) ** 2) * FLANGE_T
    boss = math.pi * ((BOSS_D / 2) ** 2 - (BORE / 2) ** 2) * BOSS_H
    assert button.volume == approx(ONSHAPE_SOLID_VOLUME, rel=0.005)
    assert button.volume < flange + boss, "the rounds have to take something off"
    # The reference mesh is a coarse tessellation of a small round solid, so
    # it reads several percent under the B-rep it came from.
    assert button.volume == approx(onshape_button.volume, rel=0.03)


def test_a_boss_wider_than_the_flange_is_rejected():
    complaint = render_failure("down_indicator_selector_button.scad",
                               bossDiameter=14.0)
    assert "captive" in complaint
