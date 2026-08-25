// The station numerals, cut clean through the top plate.
//
// A cutting tool, meant for the negative half of a difference() against the
// shell. The numerals run down the plate in -Y with their tops facing +X, so
// they read the right way up to a referee looking along their own forearm
// with the slot on the far side.
//
// Two things about the original are worth knowing before changing anything
// here. It was set in Open Sans, which is not a font OpenSCAD can count on
// having, so `font` defaults to one that ships nearly everywhere; the shapes
// differ a little. And the four numerals are NOT on the 15mm station pitch --
// they were placed by hand and drift about 3mm over the run, so `centres`
// below is the measured ink centre of each numeral in the original rather
// than a regenerated layout. Centring on the measured ink, rather than
// setting from a baseline origin, is also what keeps a substituted font from
// walking the numerals along the plate: a font's advance widths change, the
// place the ink is wanted does not.

// `baseline` is the x the numerals stand on; they grow toward +X from there.
// `tie` is described on `numeral` below, and applies only to numeral `tied`.
module numbers_cutter(baseline, centres, size, font, plate, tie, tied) {
    if (len(centres) > 0)
    for (i = [0 : len(centres) - 1])
        translate([baseline, centres[i], -1])
            rotate([0, 0, -90])
                linear_extrude(height = plate + 2)
                    numeral(i + 1, size, font, i + 1 == tied ? tie : []);
}

// One numeral, less its tie bar if it has one.
//
// A numeral with a closed counter -- the 4, and in some faces the 0, 6, 8 and
// 9 -- cannot be cut clean through a plate: the piece inside the counter ends
// up attached to nothing and drops out of the print. The original has exactly
// that defect. The fix is the one stencil faces use: leave a bar of material
// uncut across one stroke, tying the loose piece back to the plate.
//
// `tie` is [across0, across1, up0, up1] in millimetres in the numeral's own
// frame -- `across` runs the way the numerals read, measured from the
// numeral's centre, and `up` runs from its baseline. Give it as an empty
// list for no tie. One end wants to sit well outside the numeral, so the bar
// is anchored in plate; the other wants to stop inside the counter.
//
// It is a rectangle in glyph coordinates and so depends on the face in use.
// Changing `font` or `size` means checking it still lands: the test that the
// part renders as one closed solid is what catches a tie that has missed.
module numeral(n, size, font, tie) {
    difference() {
        text(str(n), size = size, font = font, halign = "center", valign = "baseline");
        if (len(tie) == 4)
            translate([tie[0], tie[2]])
                square([tie[1] - tie[0], tie[3] - tie[2]]);
    }
}
