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
use <lib/logo.scad>

/* [Body] */
bodyLen = 40.0;   // along the forearm
bodyWid = 30.0;   // across the wrist
bodyT   =  6.7;   // free choice; the trough floor assertion below is the constraint
edgeCham =  1.0;  // 45-degree chamfer where the outer walls meet each face

/* [Cord] */
cordDia      =  7.0;  // through-hole diameter
holeY        = 6.0;  // hole centres at (0, +holeY) and (0, -holeY)
troughDia    =  2.5;  // surface trough diameter; free of cordDia
troughOffset =  1;  // trough axis off its face: + sinks it into the body for
                      // a deeper-than-half-round groove, - lifts it out for a
                      // shallower one, 0 puts the axis on the face

/* [Lugs] */
bandWidth    = 20.0;
bandClear    =  0.2;   // added to bandWidth for the lug gap
barStandoff  =  4.5;
tipMargin    =  2.0;
barHoleDia   =  1.1;
tipChamfer   =  0.5;
teardropDown = true;   // apex toward the wrist side, for a face-down print

/* [Logo] */
logoEnable = true;
logoWidth  = 26.0;   // along the forearm; the mark stands a shade over 5:1
logoDepth  =  0.5;   // recessed into each face
logoX      = -8.75;  // centre across the wrist. Must be negative: the mark
                     // has to sit opposite the watch-face trough run, and the
                     // mirror then lands the wrist copy clear of its own
logoY      =   0.0;  // centre along the forearm

/* [Quality] */
$fn = 96;

/* [Hidden] */
lugGap      = bandWidth + bandClear;
hornThk     = (bodyWid - lugGap) / 2;
hornProt    = barStandoff + tipMargin;
lugToLug    = bodyLen + 2 * hornProt;
cordSpan    = max(cordDia, troughDia);   // widest thing cut around a hole centre
troughDepth = troughDia / 2 + troughOffset;
cordFloor   = bodyT - troughDepth;
logoH       = logo_height(logoWidth);   // across the wrist, rule included

assert(cordFloor >= 2.0,
       str("floor under the cord trough ", cordFloor,
           "mm is below the 2.0mm minimum; thicken bodyT, narrow troughDia, ",
           "or reduce troughOffset"));
assert(troughDepth > 0 && troughDepth < troughDia,
       str("troughOffset ", troughOffset, "mm must be within +/-", troughDia,
           "mm ( troughDia) or the trough stops being an open groove"));
assert(hornThk >= 4.0,
       str("horn thickness ", hornThk, "mm is too thin; reduce bandWidth"));
assert(holeY + cordSpan / 2 < bodyLen / 2,
       "cord holes or troughs break out of the body end");
assert(2 * holeY - cordSpan >= 2.0,
       str("wall between the cord holes/troughs ", 2 * holeY - cordSpan,
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

assert(!logoEnable || logoX < 0,
       str("logoX ", logoX, "mm must be negative: the watch-face troughs run ",
           "out to +X, so a mark on that side is laid across them"));
assert(!logoEnable || abs(logoX) - logoH / 2 >= cordSpan / 2,
       str("logo reaches the cord holes; its inner edge at ",
           abs(logoX) - logoH / 2, "mm is inside the ", cordSpan / 2,
           "mm they occupy"));
assert(!logoEnable || abs(logoX) + logoH / 2 <= bodyWid / 2 - edgeCham,
       str("logo runs past the side chamfer line; its outer edge at ",
           abs(logoX) + logoH / 2, "mm is past ", bodyWid / 2 - edgeCham, "mm"));
assert(!logoEnable || abs(logoY) + logoWidth / 2 <= bodyLen / 2 - edgeCham,
       str("logo runs off the body end; its far edge at ",
           abs(logoY) + logoWidth / 2, "mm is past the chamfer line at ",
           bodyLen / 2 - edgeCham, "mm"));
assert(!logoEnable || bodyT - 2 * logoDepth >= 2.0,
       str("logo recesses leave ", bodyT - 2 * logoDepth,
           "mm of web between them, below the 2.0mm minimum"));

echo(cordFloor = cordFloor, troughDepth = troughDepth,
     hornThk = hornThk, lugToLug = lugToLug, logoH = logoH);

down_indicator_string();

module down_indicator_string() {
    difference() {
        union() {
            body_blank(bodyLen, bodyWid, bodyT);
            lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
        }
        cord_cutter(bodyWid, bodyT, cordDia, holeY, troughDia, troughOffset);
        bar_bores(bodyLen, bodyWid, bodyT, lugGap,
                  barStandoff, barHoleDia, teardropDown);
        outer_edge_chamfers(bodyLen, bodyWid, bodyT, lugGap, hornProt, edgeCham);
        if (logoEnable)
            logo_cutter(bodyT, logoWidth, logoDepth, logoX, logoY);
    }
}
