// Chamfers on the part's outer edges, where the exterior walls meet the two
// faces.
//
// Everything here is a cutting tool, meant for the negative half of a
// difference() against the assembled solid.
//
// The outer boundary of this part is entirely straight walls, and the body
// and horns are straight extrusions from z = 0 to z = t. That makes each
// chamfer an exact half-space rather than a swept surface: for a wall with
// outward normal n at distance d, the material below the z = 0 chamfer is
// {p.n - z > d - cham}, and the z = t chamfer is its mirror about z = t/2.
//
// Convex walls -- the side walls and the horn tips -- take that half-space
// unbounded, because the part never reaches past them. The band-gap walls
// face inward, so their half-spaces would run on through the whole body;
// those are bounded to the gap.

// Every outer edge of `part`, chamfered by `cham`.
module outer_edge_chamfers(len, wid, t, gap, prot, cham) {
    if (cham > 0) chamfer_cutters(len, wid, t, gap, prot, cham);
}

module chamfer_cutters(len, wid, t, gap, prot, cham) {
    big = (len + wid) * 4;

    // Side walls, x = +-wid/2. Convex: the horns are flush with them, so each
    // runs unbroken from one horn tip to the other.
    for (a = [-90, 90]) both_faces(a, wid / 2, t, cham, big);

    // Horn tip faces, y = +-(len/2 + prot). Convex.
    for (a = [0, 180]) both_faces(a, len / 2 + prot, t, cham, big);

    // Band gap: the body end faces, bounded to the gap so the cutter stops
    // before it reaches the horn roots.
    for (a = [0, 180])
        intersection() {
            both_faces(a, len / 2, t, cham, big);
            cube([gap, big, big], center = true);
        }

    // Band gap: the horns' inner faces. Each of these half-spaces opens away
    // from its own horn and would swallow the opposite one, so each is bounded
    // to its own quadrant -- past the body end in Y, and its own side in X.
    for (sx = [-1, 1])
        for (sy = [-1, 1])
            intersection() {
                both_faces(sx * 90, -gap / 2, t, cham, big);
                translate([sx * big / 2, sy * (len / 2 + big / 2), 0])
                    cube([big, big, big], center = true);
            }
}

// The chamfer at both faces for one wall, whose outward normal lies at `ang`
// degrees from +Y and whose plane is at p.n = d.
module both_faces(ang, d, t, cham, big) {
    low_face(ang, d, cham, big);
    translate([0, 0, t]) mirror([0, 0, 1]) low_face(ang, d, cham, big);
}

// The z = 0 chamfer alone: the half-space {p.n - z > d - cham}, built as a
// large cube with one face lying in that plane.
module low_face(ang, d, cham, big) {
    rotate([0, 0, ang])
        translate([0, d - cham, 0])
            rotate([-45, 0, 0])
                translate([-big / 2, 0, -big / 2])
                    cube([big, big, big]);
}
