#!/usr/bin/env python3
"""Generate FullZapette layout mock-ups from one shared key layout.

Outputs (next to this script):
  front-layout.svg      1:1 front views of all variants (print at 100 % scale)
  mockup_<variant>.scad printable ergonomic dummy (render to STL with OpenSCAD)

All dimensions in millimetres. Origin = top-left of the front face, y grows
towards the tail. Edit the constants / build() and re-run.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent

W = 58.0                      # body width
NOSE = 10.0                   # bezel above the display (antenna + IR)
DISP = (50.0, 69.2)           # 2.8" module outline
ACTIVE = (43.2, 57.6)         # 2.8" active area
TAIL = 8.0                    # margin below the last key row
CELL = (18.6, 70.0)           # 18650, protected length
CELL_TAIL = 18.0              # cell end to tail: leaves room for the USB-C receptacle


def rect(name, cx, cy, w, h, kind="key", fill=None):
    return dict(name=name, cx=cx, cy=cy, w=w, h=h, kind=kind, fill=fill)


def row(names, cy, w, h, fills=None, margin=8.75):
    """Evenly spread keys across the width."""
    n = len(names)
    xs = [W / 2] if n == 1 else [margin + i * (W - 2 * margin) / (n - 1) for i in range(n)]
    return [rect(nm, x, cy, w, h, fill=(fills[i] if fills else None))
            for i, (nm, x) in enumerate(zip(names, xs))]


def build(numpad=True):
    keys = []
    y = NOSE + DISP[1]                      # bottom edge of the display
    # system / navigation row
    y += 7.5
    keys += row(["PWR", "BACK", "HOME", "ACT"], y, 11, 7.5)
    # D-pad ring + OK, flanked by volume and channel rockers
    y += 4 + 3 + 15
    dpad = dict(name="DPAD", cx=W / 2, cy=y, r_out=15.0, r_ok=6.0, kind="dpad")
    keys.append(dpad)
    keys.append(rect("VOL", 7.0, y, 9.5, 30, kind="rocker"))
    keys.append(rect("CH", W - 7.0, y, 9.5, 30, kind="rocker"))
    y += 15 + 3 + 4
    keys += row(["MENU", "MUTE", "LAST", "GUIDE"], y, 11, 7.5)
    y += 10
    keys += row(["REW", "PLAY", "FF", "STOP"], y, 11, 7.5)
    y += 8
    keys += row(["R", "G", "Y", "B"], y, 11, 4.5,
                fills=["#d33", "#3a3", "#dc2", "#36c"])
    if numpad:
        y += 9.5 - 9
        for names in (["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["-/--", "0", "ENT"]):
            y += 9
            keys += row(names, y, 13, 7.5, margin=12.0)
        y += 3.75 - 2.25
    length = y + 2.25 + TAIL
    return keys, length


VARIANTS = {"full": build(True)}   # add "short": build(False) to compare a numpad-less body


# ----------------------------------------------------------------- SVG ----
def svg_variant(name, keys, L, ox, oy):
    o = [f'<g transform="translate({ox},{oy})" font-family="sans-serif" text-anchor="middle">']
    o.append(f'<rect x="0" y="0" width="{W}" height="{L}" rx="8" fill="#2b2b2e" stroke="#000" stroke-width="0.3"/>')
    for i in (-1, 0, 1):                                      # IR emitters
        o.append(f'<circle cx="{W/2 + i*9}" cy="4.5" r="1.8" fill="#522"/>')
    dx = (W - DISP[0]) / 2
    o.append(f'<rect x="{dx}" y="{NOSE}" width="{DISP[0]}" height="{DISP[1]}" rx="1.5" fill="#0c0c0e"/>')
    ax = (W - ACTIVE[0]) / 2
    o.append(f'<rect x="{ax}" y="{NOSE+4}" width="{ACTIVE[0]}" height="{ACTIVE[1]}" fill="#1d3b5c"/>')
    o.append(f'<text x="{W/2}" y="{NOSE+4+ACTIVE[1]/2}" font-size="3.5" fill="#9bd">2.8" 240x320</text>')
    # 18650 behind the board (dashed)
    o.append(f'<rect x="{(W-CELL[0])/2}" y="{L-CELL_TAIL-CELL[1]}" width="{CELL[0]}" height="{CELL[1]}" rx="3" '
             f'fill="none" stroke="#fa0" stroke-width="0.3" stroke-dasharray="1.5 1"/>')
    for k in keys:
        if k["kind"] == "dpad":
            cx, cy = k["cx"], k["cy"]
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{k["r_out"]}" fill="#55565c"/>')
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{k["r_ok"]+1}" fill="#2b2b2e"/>')
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{k["r_ok"]}" fill="#6a6b72"/>')
            o.append(f'<text x="{cx}" y="{cy+1}" font-size="2.8" fill="#fff">OK</text>')
            continue
        x, y = k["cx"] - k["w"] / 2, k["cy"] - k["h"] / 2
        fill = k["fill"] or "#55565c"
        o.append(f'<rect x="{x}" y="{y}" width="{k["w"]}" height="{k["h"]}" rx="2" fill="{fill}"/>')
        if k["kind"] == "rocker":
            o.append(f'<text x="{k["cx"]}" y="{k["cy"]-9}" font-size="3.2" fill="#fff">+</text>')
            o.append(f'<text x="{k["cx"]}" y="{k["cy"]+1}" font-size="2.2" fill="#fff">{k["name"]}</text>')
            o.append(f'<text x="{k["cx"]}" y="{k["cy"]+11}" font-size="3.2" fill="#fff">-</text>')
        elif not k["fill"]:
            o.append(f'<text x="{k["cx"]}" y="{k["cy"]+1}" font-size="2.4" fill="#fff">{k["name"]}</text>')
    o.append(f'<text x="{W/2}" y="{L+6}" font-size="3.5" fill="#000">{name}: {W:.0f} x {L:.0f} mm</text>')
    o.append("</g>")
    return "\n".join(o)


def write_svg():
    gap, m = 20.0, 10.0
    total_w = m * 2 + len(VARIANTS) * W + (len(VARIANTS) - 1) * gap
    total_h = m * 2 + max(L for _, L in VARIANTS.values()) + 18
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}mm" height="{total_h}mm" '
         f'viewBox="0 0 {total_w} {total_h}">',
         f'<rect width="{total_w}" height="{total_h}" fill="#fff"/>']
    for i, (name, (keys, L)) in enumerate(VARIANTS.items()):
        o.append(svg_variant(name, keys, L, m + i * (W + gap), m))
    by = total_h - 6                                           # print-scale check bar
    o.append(f'<path d="M{m},{by} h50 M{m},{by-1.5} v3 M{m+50},{by-1.5} v3" stroke="#000" stroke-width="0.3" fill="none"/>')
    o.append(f'<text x="{m+25}" y="{by-1.5}" font-size="3" text-anchor="middle" font-family="sans-serif">'
             f'50 mm - check after printing</text>')
    o.append("</svg>")
    (OUT / "front-layout.svg").write_text("\n".join(o))


# ---------------------------------------------------------------- SCAD ----
SCAD = """// FullZapette ergonomic dummy - variant "{name}" (generated, do not edit)
// Solid block: checks size, grip and thumb reach. Print on its back with supports.
W = {W}; L = {L};
T_NOSE = 13; T_SCREEN = 16; T_BELLY = 27; T_TAIL = 23;  // thickness along the body
BACK_W = 26;      // width of the flat on the back (18650 ridge)
EDGE = 8;         // height of the vertical side edge
BUMP = 0.8;       // key height above the front face
$fn = 48;

module slice(y, t) {{
  translate([0, y, 0]) rotate([90, 0, 0]) linear_extrude(0.01)
    polygon([[-BACK_W/2, -t], [BACK_W/2, -t], [W/2, -EDGE], [W/2, -1.5], [W/2-1.5, 0],
             [-W/2+1.5, 0], [-W/2, -1.5], [-W/2, -EDGE]]);
}}
module body() {{
  intersection() {{
    hull() {{
      slice(L, T_NOSE); slice(L-75, T_SCREEN); slice(95, T_BELLY);
      slice(20, T_BELLY); slice(0.01, T_TAIL);
    }}
    translate([0, 0, -50]) linear_extrude(60)
      translate([-W/2, 0]) offset(r=8) offset(delta=-8) square([W, L]);
  }}
}}
module key(cx, cy, w, h) {{
  translate([cx - W/2, L - cy, -0.01]) linear_extrude(BUMP)
    offset(r=1.5) offset(delta=-1.5) square([w, h], center=true);
}}
module dpad(cx, cy, ro, rok) {{
  translate([cx - W/2, L - cy, -0.01]) {{
    difference() {{ cylinder(r=ro, h=BUMP); translate([0,0,-1]) cylinder(r=rok+1, h=5); }}
    cylinder(r=rok, h=BUMP + 0.4);
  }}
}}
translate([0, 0, T_BELLY]) {{
  difference() {{
    body();
    // display: active-area recess
    translate([-{aw}/2, L - {ay} - {ah}, -0.4]) cube([{aw}, {ah}, 1]);
    // IR emitter dimples
    for (i = [-1, 0, 1]) translate([i*9, L - 4.5, -0.6]) cylinder(r=1.8, h=1);
  }}
{keys}
}}
"""


def write_scad():
    for name, (keys, L) in VARIANTS.items():
        lines = []
        for k in keys:
            if k["kind"] == "dpad":
                lines.append(f'  dpad({k["cx"]}, {k["cy"]}, {k["r_out"]}, {k["r_ok"]});')
            else:
                lines.append(f'  key({k["cx"]}, {k["cy"]}, {k["w"]}, {k["h"]});  // {k["name"]}')
        (OUT / f"mockup_{name}.scad").write_text(SCAD.format(
            name=name, W=W, L=round(L, 2), aw=ACTIVE[0], ah=ACTIVE[1], ay=NOSE + 4,
            keys="\n".join(lines)))


if __name__ == "__main__":
    write_svg()
    write_scad()
    for name, (keys, L) in VARIANTS.items():
        n = sum(5 if k["kind"] == "dpad" else 2 if k["kind"] == "rocker" else 1 for k in keys)
        print(f"{name}: {W:.0f} x {L:.1f} mm, {n} keys")
