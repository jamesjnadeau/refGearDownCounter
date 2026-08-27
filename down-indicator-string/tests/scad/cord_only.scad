use <../../lib/body.scad>
use <../../lib/cord_slots.scad>

bodyLen = 40.0;
bodyWid = 30.0;
bodyT   =  6.7;
cordDia =  7.0;
holeY   = 10.0;
// the geometry these tests were written against: trough the width of the
// hole, axis on the face
troughDia    = 7.0;
troughOffset = 0.0;
$fn = 96;

difference() {
    body_blank(bodyLen, bodyWid, bodyT);
    cord_cutter(bodyWid, bodyT, cordDia, holeY, troughDia, troughOffset);
}
