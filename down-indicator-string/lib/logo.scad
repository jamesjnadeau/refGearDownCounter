// The RefGear wordmark, debossed.
//
// A cutting tool, meant for the negative half of a difference() against the
// body, in the manner of cord_slots.scad.
//
// REF in Archivo Black butted against GEAR in Archivo Regular over a rule the
// full width of the mark -- the layout of refgear-logo.svg, rebuilt out of
// text() calls rather than imported. OpenSCAD's SVG reader drops <text>
// elements outright, so import()ing that file yields the bare underline and
// nothing else.
//
// The two static faces under fonts/ are load-bearing, not a convenience.
// OpenSCAD reads a variable font without honouring its weight axis, so a
// variable Archivo renders Black and Regular as the same glyphs and the
// 900/400 contrast that carries the mark is silently lost; and a face it
// cannot resolve is substituted rather than refused, so that failure is
// visual only and no error announces it. fonts/fonts.conf is what puts the
// vendored faces on fontconfig's path, which is the only path text() reads.

// Metrics of the vendored faces, as multiples of the size handed to text().
// OpenSCAD scales text by ascent rather than by em, so these are measured off
// a render rather than read out of the font. The suite hashes fonts/*.ttf, so
// swapping a face invalidates every render that leans on these numbers.
function logo_cap()     = 0.9555;    // cap height
function logo_ref_x0()  = 0.10277;   // left bearing of REF in Black
function logo_gear_dx() = 2.97878;   // pen offset butting GEAR onto REF
function logo_ink_w()   = 6.74330;   // ink width of the two together

// Proportions of refgear-logo.svg: a 491 x 102 viewBox with the baseline at
// y = 78 and the rule spanning y = 98..102. Against a cap height of 73 that
// makes the rule 4 thick, clearing the baseline by 20.
function logo_rule_thick() = 4 / 73;
function logo_rule_drop()  = 20 / 73;

// How tall the mark stands for a given width, rule included -- so a caller can
// place it and check its clearances without restating the metrics above.
function logo_height(width) =
    width * logo_cap() * (1 + logo_rule_drop() + logo_rule_thick()) / logo_ink_w();

// The flat mark, ink centred on the origin and spanning `width` across X.
module logo_plate(width) {
    size  = 100;   // a working size only; the resize() below sets the real one
    cap   = logo_cap() * size;
    thick = logo_rule_thick() * cap;
    drop  = logo_rule_drop() * cap;

    resize([width, 0], auto = true)
    translate([-(logo_ref_x0() + logo_ink_w() / 2) * size,
               -(cap - drop - thick) / 2])
    union() {
        text("REF", font = "Archivo:style=Black", size = size);
        translate([logo_gear_dx() * size, 0])
            text("GEAR", font = "Archivo:style=Regular", size = size);
        translate([logo_ref_x0() * size, -drop - thick])
            square([logo_ink_w() * size, thick]);
    }
}

// Both face recesses, `depth` deep, the mark centred on y.
//
// The wrist-side copy is mirrored across X so that it reads the right way
// round when that face is looked at, rather than showing through reversed.
module logo_cutter(t, width, depth, y) {
    over = 1;   // run each cut past its face so the difference closes cleanly

    translate([0, y, t - depth])
        linear_extrude(height = depth + over) logo_plate(width);

    translate([0, y, -over])
        linear_extrude(height = depth + over) mirror([1, 0, 0]) logo_plate(width);
}
