// The cord holes and the face troughs that open them to the ends.
//
// Everything here is a cutting tool, meant for the negative half of a
// difference() against the body.

// Two through-bores of diameter `dia`, on the Y centreline at +-holeY.
module cord_cutter(len, t, dia, holeY) {
    for (s = [-1, 1])
        translate([0, s * holeY, -1]) cylinder(h = t + 2, d = dia);
}
