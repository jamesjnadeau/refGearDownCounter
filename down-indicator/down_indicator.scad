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
use <lib/lugs.scad>

/* [Body] */
bodyLen = 40.0;   // along the forearm
bodyWid = 30.0;   // across the wrist
bodyT   =  6.7;   // derived from cordDia -- see the neck assertion below

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
cordNeck = 2 * sqrt(pow(cordDia / 2, 2) - pow(bodyT / 2, 2));

assert(bodyT < cordDia,
       "bodyT must be less than cordDia or the face troughs never meet");
assert(cordNeck >= 1.2 && cordNeck <= 3.5,
       str("cord neck ", cordNeck, "mm is outside the 1.2-3.5mm usable range"));
assert(hornThk >= 4.0,
       str("horn thickness ", hornThk, "mm is too thin; reduce bandWidth"));
assert(holeY + cordDia / 2 < bodyLen / 2,
       "cord holes break out of the body end");

echo(cordNeck = cordNeck, hornThk = hornThk, lugToLug = lugToLug);

down_indicator();

module down_indicator() {
    difference() {
        union() {
            body_blank(bodyLen, bodyWid, bodyT);
            lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
        }
        cord_cutter(bodyLen, bodyT, cordDia, holeY);
        bar_bores(bodyLen, bodyWid, bodyT, lugGap,
                  barStandoff, barHoleDia, teardropDown);
    }
}
