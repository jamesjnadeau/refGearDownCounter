// The outer solid alone: no cavity, no slot, no numerals.
use <../../lib/profile.scad>
use <../../lib/shell.scad>

shellWidth   = 2.0;
plateT       = 3.1;
skirtDepth   = 4.0;
cornerRadius = 6.0;
keyCut       = 5.0;
topChamfer   = 1.0;
bottomFillet = 0.5;
cornerSwing  = 7.0;
$fn = 96;

shell_blank(outline([-10 - shellWidth, 20 + shellWidth],
                    [-15 - shellWidth, 60 + shellWidth],
                    cornerRadius + shellWidth, keyCut + shellWidth,
                    cornerSwing, $fn),
            -skirtDepth, plateT, bottomFillet, topChamfer, $fn);
