// Spring-bar lugs, carried over from the down counter's as-built geometry
// (see 2026-08-22-band-lugs-design.md): horns flush with the side walls,
// squared roots, 0.5mm tip chamfers.
//
// Horn thickness is derived, not a parameter -- the horns always run from the
// band gap out to the side walls, so widening the band thins them.

use <util.scad>

// Four horns, one at each corner, protruding `prot` past each end face.
module lug_horns(len, wid, t, gap, prot, tipCham) {
    hornThk = (wid - gap) / 2;
    ol = 0.5;   // root overlap into the body, so the union is not face-coincident
    for (sy = [-1, 1], sx = [-1, 1])
        translate([sx * (gap / 2 + hornThk / 2),
                   sy * (len / 2 - ol / 2 + prot / 2),
                   0])
            linear_extrude(height = t)
                horn_profile(hornThk, prot + ol, tipCham, sy);
}

// Plan-view outline of one horn: a thk x prot rectangle whose two far-end
// corners are chamfered by `cham`. `sy` selects which end is the tip.
module horn_profile(thk, prot, cham, sy) {
    y0 = -sy * prot / 2;   // rooted end
    y1 =  sy * prot / 2;   // tip end
    polygon([
        [-thk / 2,        y0],
        [ thk / 2,        y0],
        [ thk / 2,        y1 - sy * cham],
        [ thk / 2 - cham, y1],
        [-thk / 2 + cham, y1],
        [-thk / 2,        y1 - sy * cham],
    ]);
}

// Spring-bar bores, one per horn, running along X at z = t/2 and
// y = +-(len/2 + standoff). Teardropped so the crown is self-supporting when
// the case prints face down; `apexDown` puts the apex toward the wrist side,
// which is the upward direction in that orientation.
module bar_bores(len, wid, t, gap, standoff, dia, apexDown) {
    hornThk = (wid - gap) / 2;
    for (sy = [-1, 1], sx = [-1, 1])
        translate([sx * (gap / 2 - 1), sy * (len / 2 + standoff), t / 2])
            rotate([0, sx * 90, 0])
                rotate([0, 0, (apexDown ? -90 : 90) * sx])
                    teardrop_bore(dia, hornThk + 2);
}
