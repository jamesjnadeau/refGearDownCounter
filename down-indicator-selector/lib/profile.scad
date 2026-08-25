// Plan-view outlines.
//
// Every horizontal section of the shell is one of two outlines: the outer
// footprint the walls follow, and the cavity the bottom shell nests into.
// Both are rounded rectangles with one corner cut off at 45 degrees -- an
// orientation key, so the two shells only go together one way round.
//
// The cavity is the outer footprint brought in by the wall thickness, but it
// is drawn independently rather than offset, because the original is not a
// uniform offset: the key is mitred by stepping both its endpoints in by the
// wall thickness, which leaves only wall/sqrt(2) of material at that corner.

// Points along the arc from p0 to p1 about c, taken counter-clockwise.
// Both points must be the same distance from c; that distance is the radius.
function arc(c, p0, p1, fn) =
    let (r  = norm(p0 - c),
         a0 = atan2(p0[1] - c[1], p0[0] - c[0]),
         a1 = let (a = atan2(p1[1] - c[1], p1[0] - c[0])) a < a0 ? a + 360 : a,
         n  = max(2, ceil(fn * (a1 - a0) / 360)))
    [for (i = [0 : n]) c + r * [cos(a0 + (a1 - a0) * i / n),
                                sin(a0 + (a1 - a0) * i / n)]];

// One rounded corner, walking counter-clockwise. `along` is the wall the arc
// leaves, `to` the wall it lands on, both unit vectors pointing inward. The
// arc always starts and ends `r` from the corner, so the straight walls are
// the same length whatever `swing` is.
//
// `swing` is how far in from the corner, along each wall, the arc's centre
// sits. At swing == r that centre is the tangent-fillet centre and the arc is
// an ordinary r fillet. Anything else swings the same two endpoints onto a
// larger or smaller arc, which meets the walls at a slight kink -- and that
// is what two corners of this part actually are. See `outline`.
function corner_arc(corner, along, to, r, swing, fn) =
    let (c = corner + swing * (along + to))
    arc(c, corner + r * along, corner + r * to, fn);

// One outline. `x` and `y` are the two wall planes on each axis, `r` the
// corner radius, `key` the 45-degree cut at the -X/+Y corner, and `swing` the
// centre placement for the two +X corners.
//
// `swing` is a parameter because of a slip in the original sketch. The -X/-Y
// corner is a true r fillet. The two +X corners were struck on arcs of radius
// 5*sqrt(2) through the same tangent points an r of 8 would give, which puts
// their centres 7 in from the corner rather than 8. Such an arc is tangent to
// neither wall: it bulges 0.0711mm past both, which is why the part measures
// 34.07 x 79.14 rather than 34 x 79. Seven hundredths of a millimetre is
// nothing to print, but it is what the part is, so the default reproduces it.
// Pass swing == r for the fillets that were presumably intended.
function outline(x, y, r, key, swing, fn) = concat(
    corner_arc([x[0], y[0]], [0, 1], [1, 0], r, r, fn),      // -X/-Y, a true fillet
    corner_arc([x[1], y[0]], [-1, 0], [0, 1], r, swing, fn), // +X/-Y
    corner_arc([x[1], y[1]], [0, -1], [-1, 0], r, swing, fn),// +X/+Y
    [[x[0] + key, y[1]], [x[0], y[1] - key]]                 // the key, cut across
);
