// Blends for the cord path. Everything here is a cutting tool, meant for the
// same negative half of the difference() that carries cord_cutter().
//
// Two edges get rounded, both with a rolling ball of radius r:
//
//   the seam   where a trough runs into the through-bore. The cord turns
//              ninety degrees over this edge on its way down the hole, so it
//              is the edge that saws.
//   the lips   where a trough breaks out through a face. With a positive
//              troughOffset these are undercut knife edges and the cord has
//              to snap past them.
//
// Both are built for the watch-face side -- face at z = t, trough axis at
// z = t - troughOffset, trough running +X. The wrist side is the same solid
// turned 180 degrees about the Y axis at z = t/2, which is exactly the
// symmetry cord_slots() lays the two troughs out with.

module cord_rounds(wid, t, holeY, dia, troughDia, troughOffset, seamR, lipR) {
    for (flip = [0, 1])
        translate([0, 0, t / 2]) rotate([0, 180 * flip, 0]) translate([0, 0, -t / 2]) {
            if (seamR > 0)
                trough_seam_round(t, holeY, dia, troughDia, troughOffset, seamR);
            if (lipR > 0)
                trough_lip_round(wid, t, holeY, troughDia, troughOffset, lipR);
        }
}

// ---------------------------------------------------------------------------
// Seam: trough cylinder into bore cylinder.
//
// The two axes meet at (0, holeY, zt) and are perpendicular, so a ball of
// radius r rolling in the corner keeps its centre where the two offset
// cylinders cross:
//
//     v      = (rt + r) * sin(psi)
//     c(psi) = [ sqrt((rb + r)^2 - v^2), holeY + v, zt + (rt + r)*cos(psi) ]
//
// In the cross-section at each psi the fillet is the curvilinear triangle
// between the bore wall, the trough wall and the ball -- which is exactly
// triangle(A, T, V) minus the ball, where A and T are the ball's tangent
// points on the two walls and V is the corner. The ball is tangent to both
// sides of that triangle, so it eats the whole triangle except the corner
// sliver, and nothing outside it. So: loft the triangles along psi, subtract
// the swept ball.
//
// V is pushed `slop` further into the void than the true corner, because the
// triangle's straight sides are chords of two curved walls and would
// otherwise fall a hair short of covering the corner. Overshoot is free --
// the extra sits inside the bore, which is already being cut away. Pushing A
// or T past their tangent points would NOT be free: the ball stops there, so
// anything beyond would be cut without being rounded.
//
// psi runs the full turn even though the top of the loop is above the face
// and has no seam to blend; that part of the tool lands outside the body.

// [A, T, V, ball centre] for one station on the seam.
function seam_frame(psi, y0, zt, rb, rt, r, slop) =
    let (v  = (rt + r) * sin(psi),
         cx = sqrt(pow(rb + r, 2) - v * v),
         cz = zt + (rt + r) * cos(psi),
         c  = [cx, y0 + v, cz],
         n1 = [cx, v, 0] / (rb + r),          // out of the bore wall
         n2 = [0, v, cz - zt] / (rt + r),     // out of the trough wall
         k  = n1 * n2,
         b  = (n1 + n2) / norm(n1 + n2),
         d  = (r + slop) / sqrt((1 + k) / 2))
    [c - r * n1, c - r * n2, c - d * b, c];

// Unit tangent of the ball-centre curve, by difference -- the closed-form
// derivative buys nothing here and this cannot go stale.
function seam_tangent(psi, y0, zt, rb, rt, r) =
    let (h = 0.01,
         d = seam_frame(psi + h, y0, zt, rb, rt, r, 0)[3]
           - seam_frame(psi - h, y0, zt, rb, rt, r, 0)[3])
    d / norm(d);

// One ring of the swept ball. The frame is taken fresh from the tangent at
// each station rather than carried along the curve, so it cannot accumulate
// twist and closes on itself at psi = 360. +X never runs parallel to the
// tangent, so the cross product is always well conditioned.
function seam_ball_ring(psi, y0, zt, rb, rt, r, m) =
    let (c = seam_frame(psi, y0, zt, rb, rt, r, 0)[3],
         tg = seam_tangent(psi, y0, zt, rb, rt, r),
         u = cross(tg, [1, 0, 0]) / norm(cross(tg, [1, 0, 0])),
         w = cross(tg, u) / norm(cross(tg, u)))
    [for (k = [0 : m - 1]) c + r * (cos(k * 360 / m) * u + sin(k * 360 / m) * w)];

module trough_seam_round(t, holeY, dia, troughDia, troughOffset, r,
                         steps = 72, facets = 24, slop = 0.2) {
    rb = dia / 2;
    rt = troughDia / 2;
    zt = t - troughOffset;
    for (s = [-1, 1])
        difference() {
            ring_loft([for (i = [0 : steps - 1])
                let (f = seam_frame(i * 360 / steps, s * holeY, zt, rb, rt, r, slop))
                [f[0], f[1], f[2]]]);
            ring_loft([for (i = [0 : steps - 1])
                seam_ball_ring(i * 360 / steps, s * holeY, zt, rb, rt, r, facets)]);
        }
}

// A closed tube of quads: `rings` is a closed loop of equal-length closed
// rings. Both loops wrap, so there are no end caps.
module ring_loft(rings) {
    n = len(rings);
    m = len(rings[0]);
    polyhedron(points = [for (ring = rings) each ring],
               faces  = [for (i = [0 : n - 1], k = [0 : m - 1]) each
                            [[loft_ix(i, k, n, m), loft_ix(i + 1, k, n, m),
                              loft_ix(i + 1, k + 1, n, m)],
                             [loft_ix(i, k, n, m), loft_ix(i + 1, k + 1, n, m),
                              loft_ix(i, k + 1, n, m)]]],
               convexity = 8);
}

function loft_ix(i, k, n, m) = (i % n) * m + (k % m);

// ---------------------------------------------------------------------------
// Lips: where the trough breaks out through the face.
//
// A lip runs dead straight along X, so its blend is one y-z profile swept
// along the trough. Erode the profile by r and dilate it back -- a
// morphological opening, which rounds convex corners by exactly r and leaves
// concave ones alone. The only convex corners in reach are the two lips, so
// whatever the opening ate is the tool.
//
// Note the trough is buried inside the bore for the first rb of its run, so
// the near end of the sweep cuts nothing.

module trough_lip_round(wid, t, holeY, troughDia, troughOffset, r) {
    rt  = troughDia / 2;
    zt  = t - troughOffset;
    win = rt + 4 * r + 1;   // must clear the blend; must not reach the slab's corners
    for (s = [-1, 1])
        translate([0, s * holeY, 0])
            // (a, b, h) -> (h, a, b): profile in y-z, swept along +X
            multmatrix([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
                linear_extrude(height = wid / 2 + 1)
                    lip_profile(t, zt, rt, r, win);
}

module lip_profile(t, zt, rt, r, win) {
    big = 4 * win;
    intersection() {
        difference() {
            lip_stock(t, zt, rt, big);
            offset(r = r) offset(r = -r) lip_stock(t, zt, rt, big);
        }
        // keep the two lips, drop the corners of the stock, which the opening
        // rounds off as well
        translate([-win, t - win]) square([2 * win, win + 1]);
    }
}

// Face-side material in the y-z plane, as a slab under the face with the
// trough taken out of it.
module lip_stock(t, zt, rt, big) {
    difference() {
        translate([-big, t - big]) square([2 * big, big]);
        translate([0, zt]) circle(r = rt);
    }
}
