// Mechanical down selector -- the bottom shell.
//
// The half that nests up inside the top shell and sets where the button
// stops. It is a plain 30 x 75 x 5.1mm plate with four blind holes in its
// upper face, one per down, on the same 15mm pitch as the slot above them.
//
// Converted from the Onshape Part Studio `Bottom` of document
// 3db840dfeff4095d8508aa97 (the original, do-not-modify copy), measured
// 2026-08-25. See README.md.
//
// Coordinates are Onshape's. The plan outline is the same one the top shell's
// cavity is cut to -- literally the same call to `outline` -- so x and y here
// mean what they mean there. z does not: this part is drawn about its own
// z = 0, which is the floor of the four holes. Its top face at z = +3.1 is
// the one that meets the top shell's cavity ceiling, so in the top shell's
// frame this part sits 3.1mm lower than it is drawn here. See README.md,
// which also has the arithmetic on how the two actually fit.

use <lib/profile.scad>
use <lib/shell.scad>

/* [Plate] */
lowerT       =  2.0;   // below the hole floors, z = -lowerT to 0
upperT       =  3.1;   // above them, z = 0 to +upperT -- the holes are this deep
cornerRadius =  6.0;
keyCut       =  5.0;   // 45-degree orientation key at the -X/+Y corner
bottomChamfer =  1.0;  // 45-degree break around the bottom face
topFillet     =  0.5;  // round along the top edge

/* [Holes] */
stationPitch =  15.0;
stationCount =  4;
holeDiameter =  6.03;  // the button's bore is the same size

/* [Quality] */
$fn = 96;

/* [Hidden] */
stations = [for (i = [0 : stationCount - 1]) i * stationPitch];
plateX = [-10.0, 20.0];                            // hole centres to each wall
plateY = [-stationPitch, stationPitch * stationCount];

assert(bottomChamfer + topFillet < lowerT + upperT,
       "the two edge breaks meet in the middle of the plate");
assert(holeDiameter / 2 < min(-plateX[0], plateX[1]),
       "the holes break out through a wall");
assert(holeDiameter / 2 + cornerRadius < stationPitch,
       "the end holes run into the corner radii");

echo(footprint = [plateX[1] - plateX[0], plateY[1] - plateY[0], lowerT + upperT],
     holeDepth = upperT,
     floorUnderHoles = lowerT);

down_indicator_selector_bottom();

module down_indicator_selector_bottom() {
    difference() {
        plate_blank(outline(plateX, plateY, cornerRadius, keyCut, cornerRadius, $fn),
                    -lowerT, upperT, bottomChamfer, topFillet, $fn);
        // Blind from above: floor at z = 0, open at the top face. Extended
        // past that face so the cut breaks out of it cleanly.
        for (y = stations)
            translate([0, y, 0])
                cylinder(h = upperT + 1, d = holeDiameter);
    }
}
