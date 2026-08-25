// Mechanical down selector -- the top shell.
//
// The top half of the three-part printed slider down counter: the plate a
// referee reads, carrying the slot the button rides in and the numerals 1-4
// that say which down it is. The bottom shell nests into the cavity
// underneath and sets the four stations; the button is captive in the slot
// between them.
//
// Converted from the Onshape Part Studio `top` of document
// 3db840dfeff4095d8508aa97 (the original, do-not-modify copy), measured
// 2026-08-25. See README.md for what the conversion does and does not carry
// over.
//
// Coordinates are Onshape's, kept verbatim rather than recentred, because the
// three parts share a frame: the slot runs from y = 0 to y = 45 on x = 0, and
// those four stations are exactly where the bottom shell's index holes sit.
// +Z is out of the watch face, and z = 0 is the underside of the plate, so
// the plate is z = 0 to +3.1 and the skirt hangs to z = -4.

use <lib/profile.scad>
use <lib/shell.scad>
use <lib/slot.scad>
use <lib/numbers.scad>

/* [Case] */
shellWidth   =  2.0;   // skirt wall, and how far the cavity is inset
plateT       =  3.1;   // solid plate, z = 0 to +plateT
skirtDepth   =  4.0;   // skirt wall, z = -skirtDepth to 0
cornerRadius =  6.0;   // of the cavity; the outer corners add shellWidth
keyCut       =  5.0;   // 45-degree orientation key at the -X/+Y cavity corner
topChamfer   =  1.0;   // 45-degree break around the top face
bottomFillet =  0.5;   // round along both edges of the bottom face
draftAngle   =  3.0;   // on the cavity walls, widest at the ceiling

/* [Slot] */
stationPitch   = 15.0;  // between downs
stationCount   =  4;
holeDiameter   =  8.4;  // the opening at the top face
buttonDiameter = 13.0;  // the pocket under it, which holds the flange captive
pocketDepth    =  1.4;  // how far the pocket reaches up from the underside

/* [Numbers] */
textSize     =  6.85;         // ~6.94mm numerals, as the original measures
textBaseline =  9.4142136;    // the x the numerals stand on
textFont     = "DejaVu Sans"; // the original is Open Sans; see lib/numbers.scad
// Measured ink centres of the original, which are not on the station pitch.
textCentres  = [47.857, 32.219, 15.590, -1.095];
// The counter of the 4 has to be tied back to the plate or it drops out of
// the print -- see lib/numbers.scad, and the Fidelity section of README.md
// for why the original does not do this. The bar crosses the diagonal stroke
// at mid height, anchored in plate on its far side. Tuned for textFont at
// textSize; set tiedNumeral to 0 to cut the numerals as the original does.
tiedNumeral  =  4;
tieBar       = [-3.5, -0.2, 3.85, 4.55];   // across0, across1, up0, up1

/* [Fidelity] */
// How far in from the corner the two +X corner arcs are centred. At the
// corner radius, 8, they would be ordinary tangent fillets; the original has
// them at 7, on arcs of 5*sqrt(2) that are tangent to neither wall. That is
// almost certainly a slip, but it is a half-millimetre slip where it is
// widest, so the default reproduces it. See lib/profile.scad, and the
// Fidelity section of README.md for what it costs.
cornerSwing  =  7.0;

/* [Quality] */
$fn = 96;

/* [Hidden] */
stations = [for (i = [0 : stationCount - 1]) i * stationPitch];
cavX = [-10.0, 20.0];                              // slot centre to each wall
cavY = [-stationPitch, stationPitch * stationCount];
outX = [cavX[0] - shellWidth, cavX[1] + shellWidth];
outY = [cavY[0] - shellWidth, cavY[1] + shellWidth];
outR = cornerRadius + shellWidth;
draftInset = skirtDepth * tan(draftAngle);

assert(bottomFillet <= shellWidth / 2,
       str("bottom fillet ", bottomFillet,
           "mm cannot exceed half the ", shellWidth,
           "mm wall, or the two rounds along the bottom face meet"));
assert(topChamfer < plateT - pocketDepth,
       str("top chamfer ", topChamfer, "mm reaches past the pocket ledge at ",
           pocketDepth, "mm and would break into the slot"));
assert(pocketDepth < plateT,
       "the pocket must stop short of the top face or the slot has no ledge");
assert(buttonDiameter > holeDiameter,
       "the pocket must be wider than the opening or nothing is held captive");
assert(draftInset < shellWidth,
       str("draft takes ", draftInset, "mm off a ", shellWidth,
           "mm wall at the bottom face"));
assert(keyCut + shellWidth < min(cavX[1] - cavX[0], cavY[1] - cavY[0]),
       "the orientation key is bigger than the case");
assert(buttonDiameter / 2 < min(-cavX[0], cavX[1]),
       "the slot pocket breaks out through a cavity wall");

echo(footprint = [outX[1] - outX[0], outY[1] - outY[0], plateT + skirtDepth],
     cavity = [cavX[1] - cavX[0], cavY[1] - cavY[0]],
     draftInset = draftInset,
     ledgeWidth = (buttonDiameter - holeDiameter) / 2);

down_indicator_selector();

module down_indicator_selector() {
    difference() {
        shell_blank(outline(outX, outY, outR, keyCut + shellWidth, cornerSwing, $fn),
                    -skirtDepth, plateT, bottomFillet, topChamfer, $fn);
        cavity_cutter(outline(cavX, cavY, cornerRadius, keyCut, cornerRadius, $fn),
                      -skirtDepth, draftAngle, bottomFillet, $fn);
        slot_cutter(stations, holeDiameter, buttonDiameter, plateT, pocketDepth,
                    topChamfer);
        numbers_cutter(textBaseline, textCentres, textSize, textFont, plateT,
                       tieBar, tiedNumeral);
    }
}
