use <../../lib/body.scad>
use <../../lib/lugs.scad>

bodyLen    = 40.0;
bodyWid    = 30.0;
bodyT      =  6.7;
lugGap     = 20.2;
hornProt   =  6.5;
tipChamfer =  0.5;
$fn = 96;

union() {
    body_blank(bodyLen, bodyWid, bodyT);
    lug_horns(bodyLen, bodyWid, bodyT, lugGap, hornProt, tipChamfer);
}
