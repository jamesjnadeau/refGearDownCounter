// The slot the button rides in, and the pocket that holds it captive.
//
// A cutting tool, meant for the negative half of a difference() against the
// shell. It is a racetrack running the length of the stations, stepped: a
// wide pocket against the underside of the plate, narrowing to the opening at
// the top face. The button's flange sits in the pocket and cannot pass back
// out through the narrower opening, while its boss stands proud for a thumb.
//
// The opening takes the same chamfer as the outside of the plate. In the
// original that is not a separate feature -- one chamfer was applied to the
// top face and propagated around every edge it has, the slot's included.

SLOT_EPS = 0.001;

// `stations` are the y values the button indexes between; the slot spans them
// end to end. `pocket` is how far the wide part reaches up from the underside.
module slot_cutter(stations, opening, pocket_width, plate, pocket, chamfer) {
    y = [min(stations), max(stations)];
    r = opening / 2;

    // Down into the open cavity, so the pocket breaks out cleanly underneath.
    translate([0, 0, -1])
        linear_extrude(height = pocket + 1)
            racetrack(y, pocket_width / 2);

    translate([0, 0, pocket])
        linear_extrude(height = plate - chamfer - pocket)
            racetrack(y, r);

    hull() {
        translate([0, 0, plate - chamfer])
            linear_extrude(height = SLOT_EPS) racetrack(y, r);
        translate([0, 0, plate - SLOT_EPS])
            linear_extrude(height = SLOT_EPS) racetrack(y, r + chamfer);
    }

    // Out through the top face at the chamfer's full width.
    translate([0, 0, plate])
        linear_extrude(height = 1)
            racetrack(y, r + chamfer);
}

module racetrack(y, r) {
    hull() {
        translate([0, y[0]]) circle(r = r);
        translate([0, y[1]]) circle(r = r);
    }
}
