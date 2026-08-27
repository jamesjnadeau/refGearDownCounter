// The cord holes and the face troughs that carry the cord away from them.
//
// Everything here is a cutting tool, meant for the negative half of a
// difference() against the body.
//
// Each hole is a through-bore of diameter `dia`. From each hole a trough of
// diameter `troughDia` runs out to a side edge -- but the two troughs of a
// hole run to OPPOSITE edges: the watch-face trough to +X, the wrist-side
// trough to -X.
//
// That opposition is the whole point. A strand entering the face channel
// drops through the hole and turns into the wrist channel heading the other
// way, so it makes two right-angle bends inside the body. The bends are the
// retention: the cord is held by its own path rather than by a knot or a
// pinch fit. It follows that the cord must be THREADED through the hole --
// away from the hole the two channels sit on opposite sides of the body and
// never meet, so there is no open slot to press it into.
//
// `troughDia` is independent of the hole diameter, and `troughOffset` moves
// each trough axis off the face it is cut into: positive sinks the axis into
// the body, so the groove is deeper than a half-round and closes over the
// cord under a lip; negative lifts it out of the body for a groove shallower
// than a half-round. At troughOffset = 0 the axis sits exactly on the face
// and the groove is a clean half-round.
//
// The face trough axis therefore sits at z = t - troughOffset and the
// wrist-side one at z = troughOffset, leaving `t - troughOffset - troughDia/2`
// of floor beneath either; the caller asserts that floor is thick enough.

module cord_cutter(wid, t, dia, holeY, troughDia, troughOffset) {
    for (s = [-1, 1]) {
        translate([0, s * holeY, -1]) cylinder(h = t + 2, d = dia);
        cord_trough(wid, t, holeY, s, troughDia, troughOffset);
    }
}

// One face-pair of troughs for the hole at y = s * holeY. Each runs from the
// hole centre out to 1mm past its side wall, so it exits cleanly. Both holes
// share the same handedness, so the two face channels are parallel and the
// two wrist channels are parallel.
module cord_trough(wid, t, holeY, s, troughDia, troughOffset) {
    run = wid / 2 + 1;
    translate([0, s * holeY, t - troughOffset])
        rotate([0,  90, 0]) cylinder(h = run, d = troughDia);
    translate([0, s * holeY, troughOffset])
        rotate([0, -90, 0]) cylinder(h = run, d = troughDia);
}
