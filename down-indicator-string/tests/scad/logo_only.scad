use <../../lib/body.scad>
use <../../lib/logo.scad>

bodyLen = 40.0;
bodyWid = 30.0;
bodyT   =  6.7;

logoWidth = 26.0;
logoDepth =  0.5;
logoY     = -14.25;
$fn = 96;

difference() {
    body_blank(bodyLen, bodyWid, bodyT);
    logo_cutter(bodyT, logoWidth, logoDepth, logoY);
}
