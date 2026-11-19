// FullZapette ergonomic dummy - variant "full" (generated, do not edit)
// Solid block: checks size, grip and thumb reach. Print on its back with supports.
W = 58.0; L = 196.95;
T_NOSE = 13; T_SCREEN = 16; T_BELLY = 27; T_TAIL = 23;  // thickness along the body
BACK_W = 26;      // width of the flat on the back (18650 ridge)
EDGE = 8;         // height of the vertical side edge
BUMP = 0.8;       // key height above the front face
$fn = 48;

module slice(y, t) {
  translate([0, y, 0]) rotate([90, 0, 0]) linear_extrude(0.01)
    polygon([[-BACK_W/2, -t], [BACK_W/2, -t], [W/2, -EDGE], [W/2, -1.5], [W/2-1.5, 0],
             [-W/2+1.5, 0], [-W/2, -1.5], [-W/2, -EDGE]]);
}
module body() {
  intersection() {
    hull() {
      slice(L, T_NOSE); slice(L-75, T_SCREEN); slice(95, T_BELLY);
      slice(20, T_BELLY); slice(0.01, T_TAIL);
    }
    translate([0, 0, -50]) linear_extrude(60)
      translate([-W/2, 0]) offset(r=8) offset(delta=-8) square([W, L]);
  }
}
module key(cx, cy, w, h) {
  translate([cx - W/2, L - cy, -0.01]) linear_extrude(BUMP)
    offset(r=1.5) offset(delta=-1.5) square([w, h], center=true);
}
module dpad(cx, cy, ro, rok) {
  translate([cx - W/2, L - cy, -0.01]) {
    difference() { cylinder(r=ro, h=BUMP); translate([0,0,-1]) cylinder(r=rok+1, h=5); }
    cylinder(r=rok, h=BUMP + 0.4);
  }
}
translate([0, 0, T_BELLY]) {
  difference() {
    body();
    // display: active-area recess
    translate([-43.2/2, L - 14.0 - 57.6, -0.4]) cube([43.2, 57.6, 1]);
    // IR emitter dimples
    for (i = [-1, 0, 1]) translate([i*9, L - 4.5, -0.6]) cylinder(r=1.8, h=1);
  }
  key(8.75, 86.7, 11, 7.5);  // PWR
  key(22.25, 86.7, 11, 7.5);  // BACK
  key(35.75, 86.7, 11, 7.5);  // HOME
  key(49.25, 86.7, 11, 7.5);  // ACT
  dpad(29.0, 108.7, 15.0, 6.0);
  key(7.0, 108.7, 9.5, 30);  // VOL
  key(51.0, 108.7, 9.5, 30);  // CH
  key(8.75, 130.7, 11, 7.5);  // MENU
  key(22.25, 130.7, 11, 7.5);  // MUTE
  key(35.75, 130.7, 11, 7.5);  // LAST
  key(49.25, 130.7, 11, 7.5);  // GUIDE
  key(8.75, 140.7, 11, 7.5);  // REW
  key(22.25, 140.7, 11, 7.5);  // PLAY
  key(35.75, 140.7, 11, 7.5);  // FF
  key(49.25, 140.7, 11, 7.5);  // STOP
  key(8.75, 148.7, 11, 4.5);  // R
  key(22.25, 148.7, 11, 4.5);  // G
  key(35.75, 148.7, 11, 4.5);  // Y
  key(49.25, 148.7, 11, 4.5);  // B
  key(12.0, 158.2, 13, 7.5);  // 1
  key(29.0, 158.2, 13, 7.5);  // 2
  key(46.0, 158.2, 13, 7.5);  // 3
  key(12.0, 167.2, 13, 7.5);  // 4
  key(29.0, 167.2, 13, 7.5);  // 5
  key(46.0, 167.2, 13, 7.5);  // 6
  key(12.0, 176.2, 13, 7.5);  // 7
  key(29.0, 176.2, 13, 7.5);  // 8
  key(46.0, 176.2, 13, 7.5);  // 9
  key(12.0, 185.2, 13, 7.5);  // -/--
  key(29.0, 185.2, 13, 7.5);  // 0
  key(46.0, 185.2, 13, 7.5);  // ENT
}
