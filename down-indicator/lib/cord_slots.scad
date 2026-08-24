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
