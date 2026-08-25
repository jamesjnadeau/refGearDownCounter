// Mechanical down selector -- the button.
//
// The thumb piece. A flanged top-hat with a bore through it: the flange sits
// captive in the pocket under the top shell's plate, too wide to pass back
// out through the slot opening, while the boss stands proud through that
// opening for a thumb to push.
//
// Converted from the Onshape Part Studio `button` of document
// 3db840dfeff4095d8508aa97 (the original, do-not-modify copy), measured
// 2026-08-25. See README.md.
//
// It is a solid of revolution, so it is drawn as one: the profile below is
// the half-section in the (radius, z) plane, spun about the axis. Onshape's
// z is kept -- the flange runs z = -1 to 0 and the boss z = 0 to +4.
//
// What passes through the bore is not modelled, here or in Onshape. The bore
// and the bottom shell's holes are both 6.03mm, so something -- a pin, a
// screw -- is meant to run through the button into the hole below it and be
// the detent. The assembly in Onshape is empty and no fastener is drawn, so
// that part of the design is not recorded anywhere. Confirm against a
// physical unit before changing anything here.

use <lib/profile.scad>

/* [Button] */
boreDiameter   =  6.03;  // matches the bottom shell's holes
flangeDiameter = 12.0;   // captive in the 13mm pocket
flangeT        =  1.0;
bossDiameter   =  8.0;   // passes through the 8.4mm slot opening
bossH          =  4.0;
edgeFillet     =  0.4;   // top rim inside and out, and the flange's top edge

/* [Quality] */
$fn = 96;

/* [Hidden] */
rBore   = boreDiameter / 2;
rFlange = flangeDiameter / 2;
rBoss   = bossDiameter / 2;
f       = edgeFillet;

assert(rBore < rBoss, "the bore is wider than the boss it runs through");
assert(rBoss < rFlange, "the flange has to overhang the boss to stay captive");
assert(f < min(rBoss - rBore, rFlange - rBoss, flangeT, bossH),
       str("a ", edgeFillet, "mm fillet does not fit on this section"));

echo(height = flangeT + bossH,
     flangeOverhang = rFlange - rBoss,
     bossWall = rBoss - rBore);

down_indicator_selector_button();

module down_indicator_selector_button() {
    rotate_extrude() polygon(section());
}

// The half-section, walked anticlockwise from the bore at the bottom face.
// Three rounds: the flange's top edge, and both rims at the top of the boss.
function section() = concat(
    [[rBore, -flangeT], [rFlange, -flangeT], [rFlange, -f]],
    arc([rFlange - f, -f], [rFlange, -f], [rFlange - f, 0], $fn),
    [[rBoss, 0], [rBoss, bossH - f]],
    arc([rBoss - f, bossH - f], [rBoss, bossH - f], [rBoss - f, bossH], $fn),
    [[rBore + f, bossH]],
    arc([rBore + f, bossH - f], [rBore + f, bossH], [rBore, bossH - f], $fn)
);
