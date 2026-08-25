// Finger-loop down indicator.
//
// A wrist-worn body carrying a bungee cord that loops over the back of the
// hand and around a finger; which finger the loop sits on is the down.
// See ../2026-08-24-finger-loop-indicator-design.md.
//
// Coordinates: +X across the wrist, +Y along the forearm toward the hand,
// +Z out of the watch face. The body sits on z = 0 (wrist side).

use <lib/body.scad>
use <lib/cord_slots.scad>
use <lib/chamfer.scad>
use <lib/lugs.scad>

/* [Body] */
bodyLen = 40.0;   // along the forearm
bodyWid = 30.0;   // across the wrist
bodyT   =  6.7;   // free choice; the trough floor assertion below is the constraint
edgeCham =  1.0;  // 45-degree chamfer where the outer walls meet each face

/* [Cord] */
cordDia =  7.0;   // hole diameter, and trough diameter
holeY   = 10.0;   // hole centres at (0, +holeY) and (0, -holeY)

/* [Lugs] */
bandWidth    = 20.0;
bandClear    =  0.2;   // added to bandWidth for the lug gap
barStandoff  =  4.5;
tipMargin    =  2.0;
barHoleDia   =  1.1;
tipChamfer   =  0.5;
teardropDown = true;   // apex toward the wrist side, for a face-down print

/* [Quality] */
$fn = 96;

/* [Hidden] */
lugGap   = bandWidth + bandClear;
hornThk  = (bodyWid - lugGap) / 2;
hornProt = barStandoff + tipMargin;
lugToLug = bodyLen + 2 * hornProt;
cordFloor = bodyT - cordDia / 2;

assert(cordFloor >= 2.0,
       str("floor under the cord trough ", cordFloor,
           "mm is below the 2.0mm minimum; thicken bodyT or narrow cordDia"));
assert(hornThk >= 4.0,
       str("horn thickness ", hornThk, "mm is too thin; reduce bandWidth"));
assert(holeY + cordDia / 2 < bodyLen / 2,
       "cord holes break out of the body end");
assert(2 * holeY - cordDia >= 2.0,
       str("wall between the cord holes ", 2 * holeY - cordDia,
           "mm is below the 2.0mm minimum"));
assert(edgeCham < bodyT / 2,
       str("edge chamfer ", edgeCham, "mm must be under half the ", bodyT,
           "mm body thickness or the two face chamfers meet"));
assert(edgeCham < hornThk / 2,
       str("edge chamfer ", edgeCham, "mm must be under half the ", hornThk,
           "mm horn thickness or the horns are chamfered away"));
assert(tipChamfer < hornThk / 2,
       str("tip chamfer ", tipChamfer, "mm must be under half the ",
           hornThk, "mm horn thickness or the horns self-intersect"));

echo(cordFloor = cordFloor, hornThk = hornThk, lugToLug = lugToLug);

down_indicator_string();

module down_indicator_string() {
    difference() {
        union() {
            body_blank(bodyLen, bodyWid, bodyT);
            lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
        }
        cord_cutter(bodyWid, bodyT, cordDia, holeY);
        bar_bores(bodyLen, bodyWid, bodyT, lugGap,
                  barStandoff, barHoleDia, teardropDown);
        outer_edge_chamfers(bodyLen, bodyWid, bodyT, lugGap, hornProt, edgeCham);
    }
}
