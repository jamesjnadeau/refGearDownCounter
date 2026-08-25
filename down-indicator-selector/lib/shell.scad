// The shell itself: the solid the walls sweep out, and the cavity cut out of
// it. Both are built the same way, as a stack of bands between stations, so
// the chamfer at the top, the fillets along the bottom and the draft on the
// cavity walls are all just different lists of stations.

EPS = 0.001;

// Slack on the clipping prism in `shell_blank`. Without it the prism and the
// hull it clips share tangent points at the corners, and CGAL leaves a
// zero-thickness flap standing at one of them -- no volume, but the mesh is
// no longer closed, which is exactly the sort of thing a slicer trips on.
// A tenth of a micron of slack separates the two surfaces everywhere.
CLIP = 0.0001;

// A station is [z, delta]: at height z, the outline is `offset(delta)` of the
// plan profile. The band between two stations is the hull of a wafer at each,
// which makes its wall the straight line between the two offsets -- exact at
// both ends, and off by O(EPS) in between.
//
// hull() is a convex hull, so this is only exact for a convex profile, which
// the default footprint is. Swing the corners in far enough to make it
// concave -- `cornerSwing` below the corner radius, which is what the
// original drawing does -- and the hull bridges the dents, standing every
// wall between those corners off by the depth of the dent. `shell_blank`
// clips that back so the walls stay put; the chamfer and the fillet, which
// are narrower than the clip, keep the error.
module banded(pts, stations) {
    for (i = [0 : len(stations) - 2])
        hull() {
            wafer(pts, stations[i][1], stations[i][0], EPS);
            wafer(pts, stations[i + 1][1], stations[i + 1][0] - EPS, EPS);
        }
}

module wafer(pts, delta, z, h) {
    translate([0, 0, z])
        linear_extrude(height = h)
            offset(delta = delta)
                polygon(pts);
}

// How far a quarter-round of radius r has pulled the wall in, u above the
// bottom face: r at u = 0, nothing at u = r.
function fillet_inset(r, u) = r - sqrt(max(0, 2 * r * u - u * u));

// The stations a bottom fillet contributes, from the bottom face upward, on a
// wall already drafted by `slope` (rise over run, measured from z = 0).
// `sign` is -1 to pull a wall in, which rounds an outside edge, and +1 to
// push a cutter out, which rounds the inside edge it leaves behind.
function fillet_stations(z0, r, sign, slope, n) =
    [for (i = [0 : n]) let (u = r * i / n, z = z0 + u)
        [z, z * slope + sign * fillet_inset(r, u)]];

// The outer solid, before anything is cut out of it: full profile from the
// bottom fillet up to the chamfer, then 45 degrees in to the top face.
//
// Clipping the bands to a straight prism of the profile is what keeps the
// walls where they belong when the profile is concave -- see `banded`. That
// makes the whole straight-sided run exact, walls and corners both. What it
// cannot fix is the two bands that are narrower than the clip: along the
// walls between the swung corners, the chamfer and the bottom fillet come out
// up to the dent depth -- 0.0711mm -- narrow. On a convex profile the clip
// changes nothing and every face is exact.
module shell_blank(pts, bottom, top, fillet, chamfer, fn) {
    intersection() {
        translate([0, 0, bottom])
            linear_extrude(height = top - bottom)
                offset(delta = CLIP) polygon(pts);
        banded(pts, concat(
            fillet_stations(bottom, fillet, -1, 0, max(2, ceil(fn / 8))),
            [[top - chamfer, 0], [top, -chamfer]]
        ));
    }
}

// A plain plate of the same profile, chamfered along its bottom edge and
// rounded along its top one. That is the bottom shell: no cavity, no draft,
// and its two edge breaks the other way round from the top shell's.
module plate_blank(pts, bottom, top, chamfer, fillet, fn) {
    n = max(2, ceil(fn / 8));
    banded(pts, concat(
        [[bottom, -chamfer], [bottom + chamfer, 0]],
        [for (i = [n : -1 : 0]) let (u = fillet * i / n)
            [top - u, -fillet_inset(fillet, u)]]
    ));
}

// The cavity the bottom shell nests into: open at the bottom face, ceilinged
// by the underside of the top plate, and drafted so it is widest at that
// ceiling. The draft is a grip, not a lead-in -- the cavity narrows toward
// its own opening, so the two shells wedge rather than slide.
//
// The cutter runs a millimetre proud of the bottom face so its end is clear
// of the face it cuts through. Its top face at z = 0 needs no such clearance:
// the plate above is solid there, so that face lands inside material.
module cavity_cutter(pts, bottom, draft, fillet, fn) {
    slope = tan(draft);   // z is negative below the ceiling, so this insets
    banded(pts, concat(
        [[bottom - 1, bottom * slope + fillet]],
        fillet_stations(bottom, fillet, +1, slope, max(2, ceil(fn / 8))),
        [[0, 0]]
    ));
}
