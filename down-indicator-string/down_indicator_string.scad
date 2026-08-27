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
use <lib/cord_rounds.scad>
use <lib/chamfer.scad>
use <lib/lugs.scad>

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
seamRound    =  0.5;  // rolling-ball radius where a trough meets the bore
lipRound     =  0.5;  // ... and on the lips where a trough breaks a face.
                      // Rounding a lip cuts its tip off, so it widens the
                      // slot: see lipNeck below before trusting a snap fit

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
lugGap      = bandWidth + bandClear;
hornThk     = (bodyWid - lugGap) / 2;
hornProt    = barStandoff + tipMargin;
lugToLug    = bodyLen + 2 * hornProt;
cordSpan    = max(cordDia, troughDia);   // widest thing cut around a hole centre
troughDepth = troughDia / 2 + troughOffset;
cordFloor   = bodyT - troughDepth;
// The lip blend is tangent to the face at +/-lipOpen and to the trough wall
// at +/-lipNeck/2, and the neck is the narrowest the face slot ever gets.
lipOpen     = sqrt(pow(troughDia / 2 + lipRound, 2) - pow(troughOffset - lipRound, 2));
lipNeck     = troughDia * lipOpen / (troughDia / 2 + lipRound);

assert(cordFloor >= 2.0,
       str("floor under the cord trough ", cordFloor,
           "mm is below the 2.0mm minimum; thicken bodyT, narrow troughDia, ",
           "or reduce troughOffset"));
assert(troughDepth > 0 && troughDepth < troughDia,
       str("troughOffset ", troughOffset, "mm must be within +/-", troughDia,
           "mm ( troughDia) or the trough stops being an open groove"));
assert(seamRound <= 0 || troughDia < cordDia,
       str("troughDia ", troughDia, "mm must be under cordDia ", cordDia,
           "mm for there to be a seam to round; set seamRound = 0"));
assert(seamRound < troughDia / 2,
       str("seamRound ", seamRound, "mm must be under half the ", troughDia,
           "mm trough diameter"));
assert(lipRound < troughDia / 2,
       str("lipRound ", lipRound, "mm must be under half the ", troughDia,
           "mm trough diameter"));
assert(lipNeck <= troughDia,
       str("lipRound ", lipRound, "mm opens the face slot past the ", troughDia,
           "mm trough width, so there is no lip left to round"));
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

echo(cordFloor = cordFloor, troughDepth = troughDepth,
     faceSlot = 2 * lipOpen, lipNeck = lipNeck,
     hornThk = hornThk, lugToLug = lugToLug);

down_indicator_string();

module down_indicator_string() {
    difference() {
        union() {
            body_blank(bodyLen, bodyWid, bodyT);
            lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
        }
        cord_cutter(bodyWid, bodyT, cordDia, holeY, troughDia, troughOffset);
        cord_rounds(bodyWid, bodyT, holeY, cordDia, troughDia, troughOffset,
                    seamRound, lipRound);
        bar_bores(bodyLen, bodyWid, bodyT, lugGap,
                  barStandoff, barHoleDia, teardropDown);
        outer_edge_chamfers(bodyLen, bodyWid, bodyT, lugGap, hornProt, edgeCham);
    }
}
