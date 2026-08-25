// Shared profiles.

// A circle of radius r with a self-supporting apex: two flanks tangent to the
// bore at 45 degrees, meeting r * sqrt(2) from the centre. Printed with the
// apex upward, it replaces the unsupported crown of a horizontal round hole.
// Apex toward +Y.
module teardrop_2d(r) {
    union() {
        circle(r = r);
        rotate([0, 0, 45]) square([r, r]);
    }
}

// That profile as a bore of diameter d and length h, extruded along +Z.
module teardrop_bore(d, h) {
    linear_extrude(height = h) teardrop_2d(d / 2);
}
