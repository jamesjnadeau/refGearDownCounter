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
// unbounded, because the part never reaches past them. The body end faces
// inside the band gap face inward, so their half-space would run on through
// the horns; that one is bounded to the gap width.

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

    // The horns' inner faces are deliberately NOT chamfered. They are the
    // faces the strap bears against, and bevelling them would open the band
    // gap by `cham` at each face -- the strap would sit loose at the top and
    // bottom of a gap sized to hold it. They stay square for their full
    // height.
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
