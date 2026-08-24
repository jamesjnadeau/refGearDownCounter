// The bare case body.
//
// A plain rectangular slab, square in plan. The lug horns run flush to the
// side walls, so a corner radius here would root them into the radius rather
// than into solid end material -- the failure the down counter's lug spec
// diagnosed and fixed by squaring the corners.

// `wid` across X, `len` along Y, centred on the origin in plan, sitting on z = 0.
module body_blank(len, wid, t) {
    linear_extrude(height = t) square([wid, len], center = true);
}
