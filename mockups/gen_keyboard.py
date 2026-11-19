#!/usr/bin/env python3
"""Draw the key area of the main board: switch + LED placement and scan matrix.

This is a placement / matrix concept generated from the same layout as the
mock-ups (gen_mockup.py). It is NOT a routed, manufacturable PCB.

Output: docs/keyboard-pcb.svg, and the matrix table on stdout (markdown).
"""
from pathlib import Path
from gen_mockup import build, W, NOSE, DISP, CELL, CELL_TAIL

OUT = Path(__file__).resolve().parent.parent / "docs" / "keyboard-pcb.svg"

SW = 5.1            # tact switch body (SKQG class, 5.2 x 5.2 mm)
LED = (0.8, 1.6)    # 0603 white LED
EDGE = 3.0          # board inset from the shell
VCOL = ["#e6194b", "#f58231", "#ffe119", "#42d4f4", "#f032e6"]   # V0..V4

keys, L = build(True)
by_name = {k["name"]: k for k in keys}
dp, vol, ch = by_name["DPAD"], by_name["VOL"], by_name["CH"]
DR, RK = 10.5, 9.0  # d-pad switch radius, rocker switch offset


def k(name):
    return by_name[name]["cx"], by_name[name]["cy"]


# H line -> list of (label, x, y, V line)
four, three = [0, 1, 3, 4], [0, 2, 4]
H = [
    [(n, *k(n), v) for n, v in zip(["PWR", "BACK", "HOME", "ACT"], four)],
    [("VOL+", vol["cx"], vol["cy"] - RK, 0), ("LEFT", dp["cx"] - DR, dp["cy"], 1),
     ("UP", dp["cx"], dp["cy"] - DR, 2), ("RIGHT", dp["cx"] + DR, dp["cy"], 3),
     ("CH+", ch["cx"], ch["cy"] - RK, 4)],
    [("VOL-", vol["cx"], vol["cy"] + RK, 0), ("OK", dp["cx"], dp["cy"], 2),
     ("DOWN", dp["cx"], dp["cy"] + DR, 1), ("CH-", ch["cx"], ch["cy"] + RK, 4)],
    [(n, *k(n), v) for n, v in zip(["MENU", "MUTE", "LAST", "GUIDE"], four)],
    [(n, *k(n), v) for n, v in zip(["REW", "PLAY", "FF", "STOP"], four)],
    [(n, *k(n), v) for n, v in zip(["R", "G", "Y", "B"], four)],
    [(n, *k(n), v) for n, v in zip(["1", "2", "3"], three)],
    [(n, *k(n), v) for n, v in zip(["4", "5", "6"], three)],
    [(n, *k(n), v) for n, v in zip(["7", "8", "9"], three)],
    [(n, *k(n), v) for n, v in zip(["-/--", "0", "ENT"], three)],
]

# backlight LEDs: beside each plain key; diagonals of the d-pad; inside OK; two per rocker
leds = []
for h in H:
    for name, x, y, _ in h:
        if name in by_name:
            leds.append((x + 3.9, y, 0))
d = 7.8
leds += [(dp["cx"] + sx * d, dp["cy"] + sy * d, 45) for sx in (-1, 1) for sy in (-1, 1)]
leds.append((dp["cx"] + 4.1, dp["cy"] + 4.1, 45))
for r in (vol, ch):
    leds += [(r["cx"], r["cy"] - 3.6, 90), (r["cx"], r["cy"] + 3.6, 90)]

S = 5  # px per mm
PADL, PADR, PADT, PADB = 16, 50, 6, 6
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{(W+PADL+PADR)*S}" height="{(L+PADT+PADB)*S}" '
     f'viewBox="{-PADL} {-PADT} {W+PADL+PADR} {L+PADT+PADB}" font-family="sans-serif">',
     f'<rect x="{-PADL}" y="{-PADT}" width="{W+PADL+PADR}" height="{L+PADT+PADB}" fill="#fff"/>',
     # shell outline (reference) and board
     f'<rect x="0" y="0" width="{W}" height="{L}" rx="8" fill="none" stroke="#999" stroke-width="0.25" stroke-dasharray="1 1"/>',
     f'<rect x="{EDGE}" y="6" width="{W-2*EDGE}" height="{L-12}" rx="5" fill="#14532d" stroke="#0a2f19" stroke-width="0.3"/>']
# display zone (module sits above the board) and back-side parts (dashed)
dx = (W - DISP[0]) / 2
o.append(f'<rect x="{dx}" y="{NOSE}" width="{DISP[0]}" height="{DISP[1]}" rx="1" fill="#0b3a20" stroke="#7fbf95" stroke-width="0.2"/>')
o.append(f'<text x="{W/2}" y="{NOSE+40}" font-size="3" fill="#9fd3b0" text-anchor="middle">2.8" display module</text>')
o.append(f'<text x="{W/2}" y="{NOSE+44.5}" font-size="2.2" fill="#9fd3b0" text-anchor="middle">(sits above the board)</text>')
o.append(f'<rect x="{W/2-8}" y="{NOSE+DISP[1]-5.5}" width="16" height="3" fill="#d4d4d4"/>')
o.append(f'<text x="{W/2}" y="{NOSE+DISP[1]-7}" font-size="2" fill="#d4d4d4" text-anchor="middle">display FPC connector</text>')


def back(x, y, w, h, label, lx=None, ly=None):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0.6" fill="none" stroke="#fbbf24" '
             f'stroke-width="0.25" stroke-dasharray="1.2 0.8"/>')
    o.append(f'<text x="{lx if lx is not None else x+w/2}" y="{ly if ly is not None else y+h/2+0.8}" '
             f'font-size="2" fill="#fbbf24" text-anchor="middle">{label}</text>')


back(W / 2 - 9, 6, 18, 25.5, "ESP32-S3 module")
CY = L - CELL_TAIL - CELL[1]
back((W - CELL[0]) / 2, CY, CELL[0], CELL[1], "", )
o.append(f'<text x="{W/2}" y="{dp["cy"]+DR+7.6}" font-size="1.8" fill="#fbbf24" text-anchor="middle">18650 cell</text>')
back(40, 118.5, 4, 4, "", )
o.append(f'<text x="42" y="125" font-size="1.8" fill="#fbbf24" text-anchor="middle">TCA8418</text>')
back(W / 2 - 4.5, L - 6 - 7.3, 9, 7.3, "USB-C (back)", ly=L - 2.8)
for x, y in ((6.5, 8.5), (W - 6.5, 8.5), (5.5, 152.7), (W - 5.5, 152.7)):
    o.append(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#fff" stroke="#c9a227" stroke-width="0.4"/>')
for i in (-1, 0, 1):
    o.append(f'<rect x="{W/2+i*9-1.5}" y="4.2" width="3" height="3" rx="1.5" fill="#7f1d1d" stroke="#fca5a5" stroke-width="0.2"/>')

# H nets
for i, h in enumerate(H):
    pts = " ".join(f"{x},{y}" for n, x, y, _ in h if n != "OK")
    if i == 2:
        o.append(f'<line x1="{dp["cx"]}" y1="{dp["cy"]}" x2="{dp["cx"]}" y2="{dp["cy"]+DR}" stroke="#86efac" stroke-width="0.35"/>')
    x0, y0 = h[0][1], h[0][2]
    o.append(f'<polyline points="{EDGE+0.8},{y0} {pts}" fill="none" stroke="#86efac" stroke-width="0.35"/>')
    o.append(f'<text x="{-1.5}" y="{y0+0.9}" font-size="2.6" fill="#166534" text-anchor="end">H{i}</text>')
    o.append(f'<line x1="-1" y1="{y0}" x2="{EDGE+0.8}" y2="{y0}" stroke="#166534" stroke-width="0.2"/>')
# LEDs
for x, y, rot in leds:
    o.append(f'<rect x="{x-LED[0]/2}" y="{y-LED[1]/2}" width="{LED[0]}" height="{LED[1]}" fill="#fef9c3" '
             f'stroke="#facc15" stroke-width="0.15" transform="rotate({rot} {x} {y})"/>')
# switches
for h in H:
    for name, x, y, v in h:
        o.append(f'<rect x="{x-SW/2}" y="{y-SW/2}" width="{SW}" height="{SW}" rx="0.4" fill="#d4d4d8" stroke="#52525b" stroke-width="0.2"/>')
        o.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#27272a"/>')
        o.append(f'<circle cx="{x-SW/2}" cy="{y-SW/2}" r="0.9" fill="{VCOL[v]}" stroke="#000" stroke-width="0.12"/>')
        o.append(f'<text x="{x}" y="{y+SW/2+2}" font-size="1.7" fill="#fff" text-anchor="middle">{name}</text>')
# legend
lx, ly = W + 5, 12
o.append(f'<text x="{lx}" y="{ly}" font-size="3" font-weight="bold">Key board, front side</text>')
o.append(f'<text x="{lx}" y="{ly+4}" font-size="2.2">{W-2*EDGE:.0f} x {L-12:.0f} mm, 37 switches, {len(leds)} LEDs</text>')
items = [("#d4d4d8", "tact switch 5.2 x 5.2 mm"), ("#fef9c3", "white backlight LED (0603)"),
         ("#86efac", "H line = one key row (H0-H9)")]
for i, (c, t) in enumerate(items):
    o.append(f'<rect x="{lx}" y="{ly+9+i*5}" width="3" height="3" fill="{c}" stroke="#555" stroke-width="0.15"/>')
    o.append(f'<text x="{lx+4.5}" y="{ly+11.4+i*5}" font-size="2.2">{t}</text>')
o.append(f'<text x="{lx}" y="{ly+28}" font-size="2.2">Dot on each switch = its V line:</text>')
for i, c in enumerate(VCOL):
    o.append(f'<circle cx="{lx+1.5+i*8}" cy="{ly+32}" r="1.3" fill="{c}" stroke="#000" stroke-width="0.12"/>')
    o.append(f'<text x="{lx+3.5+i*8}" y="{ly+32.8}" font-size="2.2">V{i}</text>')
o.append(f'<rect x="{lx}" y="{ly+37}" width="3" height="3" fill="none" stroke="#d97706" stroke-width="0.25" stroke-dasharray="1.2 0.8"/>')
o.append(f'<text x="{lx+4.5}" y="{ly+39.4}" font-size="2.2">part on the back side</text>')
o.append(f'<circle cx="{lx+1.5}" cy="{ly+44.5}" r="1.1" fill="#fff" stroke="#c9a227" stroke-width="0.4"/>')
o.append(f'<text x="{lx+4.5}" y="{ly+45.3}" font-size="2.2">M2 mounting hole (tentative)</text>')
o.append(f'<text x="{lx}" y="{ly+53}" font-size="2" fill="#555">Placement concept, not a routed PCB.</text>')
o.append("</svg>")
OUT.write_text("\n".join(o))

print("| Line | TCA8418 pin | " + " | ".join(f"V{i} (ROW{i})" for i in range(5)) + " |")
print("|---|---|" + "---|" * 5)
for i, h in enumerate(H):
    cells = {v: n for n, _, _, v in h}
    print(f"| H{i} | COL{i} | " + " | ".join(cells.get(v, "—") for v in range(5)) + " |")
print(f"\n{sum(len(h) for h in H)} switches, {len(leds)} LEDs, board {W-2*EDGE:.0f} x {L-12:.0f} mm")
