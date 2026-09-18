#!/usr/bin/env python3
"""
Generates hand-crafted, layered SVG illustrations for Shake Factory —
real fruit/nut/shake *shapes* with gradients, shading, highlights and
detail (seeds, ridges, swirls, condensation) rather than photographs.

Why SVG instead of photographs: this build environment's network policy
blocks all outbound access to image hosts (Unsplash/Pexels/Pixabay/
Wikimedia Commons, and Hugging Face's own hosted dataset images were all
checked and are unusable — either blocked or far too low-resolution,
e.g. 100x100px thumbnails). Rather than fall back to AI-generated
photorealistic renders (explicitly ruled out for this project) these are
built as clean vector illustrations: crisp at any size, small file size,
and immediately readable as the real object instead of a placeholder box.

Every shape/gradient is hand-authored below — nothing here is templated
from a stock icon set.
"""
import math
import random

OUT = "/home/user/Shake-factory/assets/images"
random.seed(11)

# ---------------------------------------------------------------- helpers

def svg_open(w, h, extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
{extra_defs}
<filter id="softShadow" x="-60%" y="-60%" width="220%" height="220%">
  <feDropShadow dx="0" dy="{h*0.028:.1f}" stdDeviation="{h*0.02:.1f}" flood-color="#2B1E16" flood-opacity="0.30"/>
</filter>
</defs>
'''

def svg_close():
    return "</svg>\n"

def lingrad(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'

def radgrad(id_, stops, cx=0.35, cy=0.3, r=0.75):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'

def highlight(cx, cy, rx, ry, opacity=0.55, rotate=0, fill="#FFFFFF"):
    t = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{opacity}"{t}/>'

def ground_shadow(cx, cy, rx, ry, opacity=0.22):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#2B1E16" opacity="{opacity}"/>'

def write(name, content):
    with open(f"{OUT}/{name}", "w") as f:
        f.write(content)
    print("wrote", name)


# ================================================================
# INGREDIENT ICONS  (240x240 viewBox)
# ================================================================

def strawberry_body(cx=120, cy=118, scale=1.0, grad_id="sbBody"):
    """Returns (defs, body). Body = berry + calyx + seeds."""
    defs = radgrad(grad_id, [(0, "#FF8FA3"), (0.55, "#E8536B"), (1, "#B8324A")], cx=0.4, cy=0.28, r=0.85)
    s = scale
    path = (f"M{cx},{cy-58*s} C{cx+34*s},{cy-58*s} {cx+52*s},{cy-24*s} {cx+50*s},{cy+8*s} "
            f"C{cx+47*s},{cy+46*s} {cx+22*s},{cy+80*s} {cx},{cy+82*s} "
            f"C{cx-22*s},{cy+80*s} {cx-47*s},{cy+46*s} {cx-50*s},{cy+8*s} "
            f"C{cx-52*s},{cy-24*s} {cx-34*s},{cy-58*s} {cx},{cy-58*s} Z")
    body = f'<path d="{path}" fill="url(#{grad_id})" filter="url(#softShadow)"/>'
    # seeds: scattered small yellow pips following the curve, with a tiny shadow crescent each
    seeds = []
    rows = [(-30, 0.6), (-8, 0.85), (14, 0.95), (36, 0.85), (56, 0.55)]
    for dy, wscale in rows:
        n = 5 if wscale > 0.7 else 3
        span = 34 * wscale * s
        for i in range(n):
            t = (i / (n - 1)) - 0.5 if n > 1 else 0
            sx = cx + t * span * 2 + random.uniform(-3, 3)
            sy = cy + dy * s + random.uniform(-2, 2)
            rot = math.degrees(math.atan2(dy, t + 0.001)) * 0.15
            seeds.append(f'<ellipse cx="{sx:.1f}" cy="{sy+1.2:.1f}" rx="{2.6*s:.1f}" ry="{1.6*s:.1f}" '
                         f'fill="#7A1F2E" opacity="0.35" transform="rotate({rot:.0f} {sx:.1f} {sy:.1f})"/>')
            seeds.append(f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{2.4*s:.1f}" ry="{3.4*s:.1f}" '
                         f'fill="#F4D35E" transform="rotate({rot:.0f} {sx:.1f} {sy:.1f})"/>')
    # calyx (leafy top)
    leaves = []
    for ang in (-70, -35, 0, 35, 70):
        rad = math.radians(ang)
        lx = cx + math.sin(rad) * 30 * s
        ly = cy - 58 * s - math.cos(rad) * 14 * s
        leaves.append(f'<path d="M{cx},{cy-52*s} Q{lx:.1f},{ly-10:.1f} {lx:.1f},{ly:.1f} '
                      f'Q{(cx+lx)/2:.1f},{ly+14:.1f} {cx},{cy-46*s} Z" fill="#6E8E42"/>')
    calyx = (f'<g filter="url(#softShadow)">' + "".join(leaves) +
             f'<ellipse cx="{cx}" cy="{cy-52*s}" rx="{9*s}" ry="{6*s}" fill="#557A34"/></g>')
    hi = highlight(cx - 20 * s, cy - 22 * s, 14 * s, 20 * s, 0.35, rotate=-20)
    return defs, calyx + body + hi + "".join(seeds)


def gen_strawberry():
    defs, body = strawberry_body()
    svg = svg_open(240, 240, defs)
    svg += ground_shadow(120, 205, 55, 10)
    svg += body
    svg += svg_close()
    write("strawberry.svg", svg)


def gen_banana():
    defs = lingrad("banBody", [(0, "#FFE28A"), (0.5, "#FFC94D"), (1, "#E8960A")], 0, 0, 1, 1)
    svg = svg_open(240, 240, defs)
    svg += ground_shadow(120, 205, 68, 10)
    path = ("M52,168 C40,120 55,78 95,52 C130,29 172,30 196,50 "
            "C182,54 150,64 128,86 C102,112 96,148 104,176 "
            "C86,186 64,186 52,168 Z")
    svg += f'<path d="{path}" fill="url(#banBody)" filter="url(#softShadow)"/>'
    # tips
    svg += '<path d="M196,50 C204,44 210,46 210,54 C210,62 200,66 192,60 Z" fill="#7A5A2E"/>'
    svg += '<path d="M52,168 C46,178 50,186 58,184 C66,182 66,172 60,166 Z" fill="#7A5A2E"/>'
    # ridge lines follow the curve
    for off in (-10, 6, 20):
        svg += (f'<path d="M{78+off*0.3},150 C{70+off},108 {95+off},72 {150+off*0.6},52" '
                f'stroke="#C97F0E" stroke-width="2.2" fill="none" opacity="0.45" stroke-linecap="round"/>')
    svg += highlight(120, 90, 34, 12, 0.4, rotate=-28)
    svg += svg_close()
    write("banana.svg", svg)


def gen_mango():
    defs = lingrad("mangoBody", [(0, "#8FAE5D"), (0.35, "#FFC94D"), (0.75, "#FF9F45"), (1, "#E8536B")], 0, 0, 0.3, 1)
    svg = svg_open(240, 240, defs)
    svg += ground_shadow(122, 205, 58, 10)
    path = ("M120,34 C156,34 182,64 184,104 C186,148 158,190 118,190 "
            "C80,190 50,154 52,110 C54,68 84,34 120,34 Z")
    svg += f'<path d="{path}" fill="url(#mangoBody)" filter="url(#softShadow)"/>'
    svg += '<path d="M112,36 C116,28 128,28 130,37 C124,40 117,40 112,36 Z" fill="#5C3A21"/>'
    svg += highlight(96, 78, 22, 30, 0.32, rotate=-18)
    svg += highlight(150, 130, 16, 22, 0.15, rotate=20, fill="#7A1F2E")
    svg += svg_close()
    write("mango.svg", svg)


def gen_blueberries():
    defs = radgrad("bbBody", [(0, "#7C87C9"), (0.55, "#4E5AA0"), (1, "#333B72")], 0.35, 0.3, 0.85)
    svg = svg_open(240, 240, defs)
    berries = [(85, 150, 34), (140, 158, 38), (105, 108, 30), (160, 112, 33), (128, 70, 26)]
    svg += ground_shadow(122, 205, 66, 10)
    for (cx, cy, r) in berries:
        svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bbBody)" filter="url(#softShadow)"/>'
        svg += highlight(cx - r * 0.32, cy - r * 0.35, r * 0.3, r * 0.22, 0.4)
        # blossom-end crown mark
        star = []
        for i in range(5):
            a = math.radians(i * 72 + 90)
            star.append(f"{cx + math.cos(a) * r * 0.13:.1f},{cy + r * 0.72 + math.sin(a) * r * 0.13:.1f}")
        svg += f'<polygon points="{" ".join(star)}" fill="#20264A" opacity="0.55"/>'
    svg += svg_close()
    write("blueberries.svg", svg)


def nut_shape(cx, cy, rx, ry, rot, grad_id, colors):
    defs = lingrad(grad_id, colors, 0, 0, 1, 1)
    body = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{grad_id})" '
            f'filter="url(#softShadow)" transform="rotate({rot} {cx} {cy})"/>')
    body += highlight(cx - rx * 0.3, cy - ry * 0.35, rx * 0.32, ry * 0.28, 0.4, rotate=rot)
    for i in range(2):
        vx = cx + (i - 0.5) * rx * 0.5
        body += (f'<path d="M{vx-rx*0.15},{cy-ry*0.5} Q{vx},{cy} {vx-rx*0.1},{cy+ry*0.55}" '
                 f'stroke="#00000022" stroke-width="1.6" fill="none" transform="rotate({rot} {cx} {cy})"/>')
    return defs, body


def gen_almonds():
    svg = svg_open(240, 240)
    svg += ground_shadow(120, 200, 66, 10)
    d1, b1 = nut_shape(95, 130, 30, 52, -18, "alm1", [(0, "#E8D2AE"), (1, "#B98A57")])
    d2, b2 = nut_shape(150, 110, 26, 46, 14, "alm2", [(0, "#DEC194"), (1, "#A9764A")])
    svg = svg.replace("<defs>", f"<defs>{d1}{d2}")
    svg += b1 + b2
    svg += svg_close()
    write("almonds.svg", svg)


def cashew_path(cx, cy, scale, rot, grad_id, colors):
    """A smooth thick 'C'-hook stroke reads far more reliably as a cashew
    than a hand-built closed outline, which tends to self-intersect."""
    defs = lingrad(grad_id, colors, 0, 0, 1, 1)
    s = scale
    r = 24 * s
    sw = 15 * s
    path = f"M{cx+r*0.66:.1f},{cy-r*0.94:.1f} A{r:.1f},{r:.1f} 0 1,1 {cx-r*0.78:.1f},{cy+r*0.5:.1f}"
    g = f'<g transform="rotate({rot} {cx} {cy})" filter="url(#softShadow)">'
    g += f'<path d="{path}" fill="none" stroke="url(#{grad_id})" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
    g += (f'<path d="{path}" fill="none" stroke="#FFFFFF" stroke-width="{sw*0.32:.1f}" '
          f'stroke-linecap="round" opacity="0.35" transform="translate(-{sw*0.16:.1f},-{sw*0.16:.1f})"/>')
    g += "</g>"
    return defs, g


def gen_cashews():
    svg = svg_open(240, 240)
    svg += ground_shadow(122, 200, 70, 10)
    d1, b1 = cashew_path(105, 120, 1.15, -12, "cw1", [(0, "#F3E3C3"), (1, "#C79A5B")])
    d2, b2 = cashew_path(155, 108, 0.95, 150, "cw2", [(0, "#EAD5A8"), (1, "#B9874E")])
    svg = svg.replace("<defs>", f"<defs>{d1}{d2}")
    svg += b1 + b2
    svg += svg_close()
    write("cashews.svg", svg)


def gen_pistachios():
    svg = svg_open(240, 240)
    defs_shell = lingrad("pisShell", [(0, "#EFE3C8"), (1, "#C9AE7C")], 0, 0, 1, 1)
    defs_nut = lingrad("pisNut", [(0, "#B7CE86"), (1, "#7E9A50")], 0, 0, 0, 1)
    svg = svg.replace("<defs>", f"<defs>{defs_shell}{defs_nut}")
    svg += ground_shadow(122, 202, 70, 10)

    def one(cx, cy, rot, scale):
        s = scale
        g = f'<g transform="rotate({rot} {cx} {cy})" filter="url(#softShadow)">'
        g += (f'<path d="M{cx-24*s},{cy} C{cx-24*s},{cy-38*s} {cx-8*s},{cy-52*s} {cx},{cy-52*s} '
              f'C{cx+8*s},{cy-52*s} {cx+24*s},{cy-38*s} {cx+24*s},{cy} '
              f'C{cx+24*s},{cy+34*s} {cx+8*s},{cy+50*s} {cx},{cy+50*s} '
              f'C{cx-8*s},{cy+50*s} {cx-24*s},{cy+34*s} {cx-24*s},{cy} Z" fill="url(#pisShell)"/>')
        g += (f'<path d="M{cx-6*s},{cy-46*s} C{cx-16*s},{cy-20*s} {cx-16*s},{cy+20*s} {cx-6*s},{cy+44*s} '
              f'L{cx+6*s},{cy+44*s} C{cx-4*s},{cy+18*s} {cx-4*s},{cy-20*s} {cx+6*s},{cy-46*s} Z" '
              f'fill="url(#pisNut)"/>')
        g += highlight(cx - 12 * s, cy - 20 * s, 6 * s, 14 * s, 0.35)
        g += "</g>"
        return g

    svg += one(100, 122, -10, 1.0)
    svg += one(150, 112, 16, 0.85)
    svg += svg_close()
    write("pistachios.svg", svg)


def gen_hazelnuts():
    svg = svg_open(240, 240)
    defs = radgrad("hzBody", [(0, "#C99B6A"), (0.6, "#A2703F"), (1, "#7A4E28")], 0.35, 0.3, 0.9)
    svg = svg.replace("<defs>", f"<defs>{defs}")
    svg += ground_shadow(122, 200, 66, 10)

    def one(cx, cy, r):
        g = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#hzBody)" filter="url(#softShadow)"/>'
        g += f'<path d="M{cx-r*0.5},{cy-r*0.75} Q{cx},{cy-r*1.15} {cx+r*0.5},{cy-r*0.75} L{cx+r*0.3},{cy-r*0.55} Q{cx},{cy-r*0.8} {cx-r*0.3},{cy-r*0.55} Z" fill="#DCC49A"/>'
        g += highlight(cx - r * 0.32, cy - r * 0.2, r * 0.28, r * 0.22, 0.35)
        return g

    svg += one(96, 132, 38)
    svg += one(152, 118, 34)
    svg += one(126, 168, 30)
    svg += svg_close()
    write("hazelnuts.svg", svg)


def gen_chocolate():
    svg = svg_open(240, 240)
    defs = lingrad("chocBody", [(0, "#6E4A2E"), (0.5, "#4A2E1A"), (1, "#2A170C")], 0, 0, 1, 1)
    svg = svg.replace("<defs>", f"<defs>{defs}")
    svg += ground_shadow(122, 202, 68, 10)

    def chunk(cx, cy, s, rot):
        pts = [(-1, -1), (0.6, -1.2), (1.1, -0.2), (0.9, 1), (-0.3, 1.1), (-1.2, 0.2)]
        p = " ".join(f"{cx+px*s:.1f},{cy+py*s:.1f}" for px, py in pts)
        g = f'<g transform="rotate({rot} {cx} {cy})" filter="url(#softShadow)">'
        g += f'<polygon points="{p}" fill="url(#chocBody)"/>'
        g += (f'<line x1="{cx-s*0.8:.1f}" y1="{cy-s*0.6:.1f}" x2="{cx+s*0.7:.1f}" y2="{cy-s*0.1:.1f}" '
              f'stroke="#FFFFFF" stroke-width="{s*0.16:.1f}" opacity="0.28" stroke-linecap="round"/>')
        g += "</g>"
        return g

    svg += chunk(100, 128, 42, -12)
    svg += chunk(158, 118, 34, 20)
    svg += chunk(128, 172, 30, 55)
    svg += svg_close()
    write("chocolate.svg", svg)


def gen_cookie():
    svg = svg_open(240, 240)
    defs = radgrad("cookieBody", [(0, "#D9B27C"), (0.65, "#C4945A"), (1, "#9C6B38")], 0.4, 0.35, 0.85)
    svg = svg.replace("<defs>", f"<defs>{defs}")
    svg += ground_shadow(120, 205, 64, 10)
    svg += f'<circle cx="120" cy="120" r="72" fill="url(#cookieBody)" filter="url(#softShadow)"/>'
    svg += highlight(90, 88, 26, 18, 0.25, rotate=-20)
    chips = [(88, 92, 8), (140, 84, 7), (160, 128, 9), (108, 142, 7.5), (150, 158, 6.5),
             (96, 158, 8), (128, 110, 6), (70, 128, 6.5)]
    for (cx, cy, r) in chips:
        svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#3B2417"/>'
        svg += f'<circle cx="{cx-r*0.3}" cy="{cy-r*0.3}" r="{r*0.3}" fill="#5C3A21" opacity="0.7"/>'
    svg += svg_close()
    write("cookie.svg", svg)


def gen_milk_splash():
    svg = svg_open(240, 240)
    defs = lingrad("milkBody", [(0, "#FFFFFF"), (1, "#DCE6ED")], 0, 0, 0, 1)
    svg = svg.replace("<defs>", f"<defs>{defs}")
    cx, cy = 120, 172
    svg += ground_shadow(cx, 210, 66, 8)

    g = '<g filter="url(#softShadow)">'
    # crown spikes first (behind the pool rim so their base tucks under it)
    heights = [26, 46, 34, 58, 30, 50, 24]
    n = len(heights)
    span = 128
    for i, h in enumerate(heights):
        sx = cx - span / 2 + span * i / (n - 1)
        sy = cy - 6
        w = 11
        g += (f'<path d="M{sx-w/2:.1f},{sy:.1f} '
              f'C{sx-w/2:.1f},{sy-h*0.55:.1f} {sx-w*0.22:.1f},{sy-h:.1f} {sx:.1f},{sy-h-5:.1f} '
              f'C{sx+w*0.22:.1f},{sy-h:.1f} {sx+w/2:.1f},{sy-h*0.55:.1f} {sx+w/2:.1f},{sy:.1f} Z" '
              f'fill="url(#milkBody)"/>')
    # pool base: a wide shallow puddle, drawn on top so spike bases sit inside it
    pool = (f"M{cx-70},{cy-4} C{cx-70},{cy-22} {cx-36},{cy-30} {cx},{cy-30} "
            f"C{cx+36},{cy-30} {cx+70},{cy-22} {cx+70},{cy-4} "
            f"C{cx+70},{cy+18} {cx+38},{cy+28} {cx},{cy+28} "
            f"C{cx-38},{cy+28} {cx-70},{cy+18} {cx-70},{cy-4} Z")
    g += f'<path d="{pool}" fill="url(#milkBody)"/>'
    g += "</g>"
    svg += g
    svg += highlight(cx - 26, cy - 12, 22, 10, 0.55)

    # a few droplets flying off, mid-air
    for (dx, dy, r) in [(-92, -18, 6.5), (86, -30, 5.5), (100, 10, 4.5), (-6, -66, 5), (38, -70, 4)]:
        svg += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="url(#milkBody)" filter="url(#softShadow)"/>'
        svg += f'<circle cx="{cx+dx-r*0.3:.1f}" cy="{cy+dy-r*0.3:.1f}" r="{r*0.3:.1f}" fill="#FFFFFF" opacity="0.8"/>'
    svg += svg_close()
    write("milk-splash.svg", svg)


def whipped_cream_swirl(cx, cy, w, h, grad_id="creamBody"):
    defs = lingrad(grad_id, [(0, "#FFFFFF"), (1, "#F1E6D2")], 0, 0, 0, 1)
    layers = []
    n = 4
    for i in range(n):
        f = 1 - i / n
        ry = h * 0.22 * f
        rx = w * 0.5 * f + w * 0.12
        y = cy + h * 0.5 - i * (h * 0.62 / n)
        layers.append(f'<ellipse cx="{cx}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{grad_id})"/>')
        layers.append(f'<ellipse cx="{cx-rx*0.25:.1f}" cy="{y-ry*0.3:.1f}" rx="{rx*0.35:.1f}" ry="{ry*0.3:.1f}" fill="#FFFFFF" opacity="0.6"/>')
    swirl_lines = ""
    for i in range(3):
        y = cy + h * 0.5 - i * (h * 0.5 / 3) - h * 0.08
        swirl_lines += (f'<path d="M{cx-w*0.32},{y:.1f} Q{cx},{y-h*0.1:.1f} {cx+w*0.32},{y:.1f}" '
                        f'stroke="#D8C7A8" stroke-width="1.4" fill="none" opacity="0.5"/>')
    body = f'<g filter="url(#softShadow)">' + "".join(layers) + swirl_lines + "</g>"
    return defs, body


def gen_whipped_cream():
    svg = svg_open(240, 240)
    d, b = whipped_cream_swirl(120, 130, 130, 130)
    svg = svg.replace("<defs>", f"<defs>{d}")
    svg += ground_shadow(120, 205, 64, 10)
    svg += b
    svg += svg_close()
    write("whipped-cream.svg", svg)


def ice_cube(cx, cy, s, rot=0):
    top = f"{cx-s},{cy-s*0.5} {cx},{cy-s} {cx+s},{cy-s*0.5} {cx},{cy}"
    front = f"{cx-s},{cy-s*0.5} {cx},{cy} {cx},{cy+s} {cx-s},{cy+s*0.5}"
    side = f"{cx},{cy} {cx+s},{cy-s*0.5} {cx+s},{cy+s*0.5} {cx},{cy+s}"
    g = f'<g transform="rotate({rot} {cx} {cy})" filter="url(#softShadow)" opacity="0.88">'
    g += f'<polygon points="{top}" fill="#E9F5FA"/>'
    g += f'<polygon points="{front}" fill="#CFE7F0"/>'
    g += f'<polygon points="{side}" fill="#AACDDD"/>'
    g += f'<line x1="{cx-s*0.4}" y1="{cy-s*0.1}" x2="{cx-s*0.1}" y2="{cy+s*0.5}" stroke="#FFFFFF" stroke-width="2" opacity="0.6"/>'
    g += "</g>"
    return g


def gen_ice_cubes():
    svg = svg_open(240, 240)
    svg += ground_shadow(120, 200, 66, 10)
    svg += ice_cube(95, 140, 34, -6)
    svg += ice_cube(150, 122, 30, 10)
    svg += svg_close()
    write("ice-cubes.svg", svg)


# ================================================================
# SHAKE GLASSES  (260x360 viewBox, portrait)
# ================================================================

GLASS_TOP_W = 96
GLASS_BOTTOM_W = 66
GLASS_TOP_Y = 70
GLASS_BOTTOM_Y = 300
GLASS_CX = 130


def glass_outline_path():
    x1, x2 = GLASS_CX - GLASS_TOP_W, GLASS_CX + GLASS_TOP_W
    x3, x4 = GLASS_CX - GLASS_BOTTOM_W, GLASS_CX + GLASS_BOTTOM_W
    return (f"M{x1},{GLASS_TOP_Y} L{x2},{GLASS_TOP_Y} "
            f"C{x2-4},{160} {x4+6},{220} {x4},{GLASS_BOTTOM_Y} "
            f"C{x4-2},{312} {x3+2},{312} {x3},{GLASS_BOTTOM_Y} "
            f"C{x3-6},{220} {x1+4},{160} {x1},{GLASS_TOP_Y} Z")


def fill_wave_path(level_y):
    x1, x2 = GLASS_CX - GLASS_TOP_W + 3, GLASS_CX + GLASS_TOP_W - 3
    x3, x4 = GLASS_CX - GLASS_BOTTOM_W + 2, GLASS_CX + GLASS_BOTTOM_W - 2
    t = (level_y - GLASS_TOP_Y) / (GLASS_BOTTOM_Y - GLASS_TOP_Y)
    lx = x1 + (x3 - x1) * t
    rx = x2 + (x4 - x2) * t
    return (f"M{lx},{level_y} Q{GLASS_CX},{level_y-10} {rx},{level_y} "
            f"C{rx-2},{312} {lx+2},{312} {lx},{level_y+ (GLASS_BOTTOM_Y-level_y)} "
            f"C{lx-6},{220} {lx if t>0.5 else x1+4},{160} {lx},{level_y} Z")


def straw(color="#FFFFFF", stripe="#E8536B"):
    g = '<g filter="url(#softShadow)">'
    g += (f'<path d="M96,20 L84,54 L112,96" stroke="{color}" stroke-width="12" '
          f'fill="none" stroke-linecap="round"/>')
    for i in range(6):
        y = 24 + i * 12
        g += f'<line x1="{92-i*0.6}" y1="{y}" x2="{100-i*0.6}" y2="{y+8}" stroke="{stripe}" stroke-width="4" opacity="0.85"/>'
    g += "</g>"
    return g


def condensation():
    dots = ""
    pts = [(90, 250, 4), (176, 230, 3.5), (100, 270, 3), (168, 265, 4.5), (120, 285, 3), (150, 200, 3)]
    for (x, y, r) in pts:
        dots += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="0.55"/>'
    return dots


def build_shake(filename, fill_stops, garnish_fn, whip=True):
    defs_glass = lingrad("glassBody", [(0, "#FFFFFF"), (0.5, "#EAF3F7"), (1, "#D8E6EC")], 0, 0, 1, 0.2)
    defs_fill = lingrad("shakeFill", fill_stops, 0, 0, 0, 1)
    svg = svg_open(260, 360, defs_glass + defs_fill)
    svg += ground_shadow(GLASS_CX, 330, 78, 12)
    # glass body (behind fill for the base, then fill, then glass front highlight/outline)
    svg += f'<path d="{glass_outline_path()}" fill="url(#glassBody)" opacity="0.55" filter="url(#softShadow)"/>'
    svg += f'<clipPath id="glassClip"><path d="{glass_outline_path()}"/></clipPath>'
    svg += f'<g clip-path="url(#glassClip)"><path d="{fill_wave_path(118)}" fill="url(#shakeFill)"/>'
    svg += f'<ellipse cx="{GLASS_CX-24}" cy="150" rx="14" ry="60" fill="#FFFFFF" opacity="0.12"/></g>'
    # glass outline stroke + rim ellipse
    svg += f'<path d="{glass_outline_path()}" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.65"/>'
    svg += f'<ellipse cx="{GLASS_CX}" cy="{GLASS_TOP_Y}" rx="{GLASS_TOP_W}" ry="10" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.5"/>'
    svg += condensation()
    if whip:
        d, b = whipped_cream_swirl(GLASS_CX, 56, 118, 66)
        svg = svg.replace("<defs>", f"<defs>{d}", 1)
        svg += b
    svg += garnish_fn(GLASS_CX)
    svg += straw()
    svg += svg_close()
    write(filename, svg)


def garnish_strawberry(cx):
    d, body = strawberry_body(cx + 20, 34, 0.55, grad_id="garnSb")
    g = f'<defs>{d}</defs>' + body
    g += f'<path d="M{cx-46},70 C{cx-20},86 {cx+10},86 {cx+30},74" stroke="#E8536B" stroke-width="4" fill="none" opacity="0.7" stroke-linecap="round"/>'
    return g


def garnish_chocolate(cx):
    g = ""
    for i, (dx, dy, rot) in enumerate([(-30, 20, -20), (10, 10, 30), (-6, 34, 70)]):
        d, b = "", ""
        gid = f"garnChoc{i}"
        d = lingrad(gid, [(0, "#6E4A2E"), (1, "#2A170C")], 0, 0, 1, 1)
        g += f"<defs>{d}</defs>"
        cxp, cyp = cx + dx, 40 + dy
        pts = [(-1, -1), (0.6, -1.2), (1.1, -0.2), (0.9, 1), (-0.3, 1.1), (-1.2, 0.2)]
        p = " ".join(f"{cxp+px*14:.1f},{cyp+py*14:.1f}" for px, py in pts)
        g += f'<polygon points="{p}" fill="url(#{gid})" transform="rotate({rot} {cxp} {cyp})" filter="url(#softShadow)"/>'
    g += f'<path d="M{cx-40},64 Q{cx},78 {cx+40},64" stroke="#4A2E1A" stroke-width="5" fill="none" opacity="0.75" stroke-linecap="round"/>'
    g += f'<path d="M{cx-30},74 Q{cx},86 {cx+30},74" stroke="#4A2E1A" stroke-width="4" fill="none" opacity="0.6" stroke-linecap="round"/>'
    return g


def garnish_mango(cx):
    gid = "garnMango"
    d = lingrad(gid, [(0, "#FFC94D"), (1, "#FF9F45")], 0, 0, 1, 1)
    g = f"<defs>{d}</defs>"
    g += (f'<path d="M{cx-20},20 A26,26 0 0 1 {cx+26},20 L{cx+26},50 A26,26 0 0 1 {cx-20},50 Z" '
          f'fill="url(#{gid})" filter="url(#softShadow)"/>')
    for i in range(4):
        g += f'<line x1="{cx-14+i*10}" y1="22" x2="{cx-14+i*10}" y2="48" stroke="#FFFFFF" stroke-width="1.4" opacity="0.5"/>'
    g += f'<path d="M{cx-38},66 Q{cx},80 {cx+38},64" stroke="#FF9F45" stroke-width="4" fill="none" opacity="0.7" stroke-linecap="round"/>'
    return g


def garnish_pistachio(cx):
    g = ""
    for i, (dx, rot) in enumerate([(-26, -15), (-4, 10), (20, -25)]):
        gid1, gid2 = f"pshell{i}", f"pnut{i}"
        g += f"<defs>{lingrad(gid1, [(0, '#EFE3C8'), (1, '#C9AE7C')], 0, 0, 1, 1)}{lingrad(gid2, [(0, '#B7CE86'), (1, '#7E9A50')], 0, 0, 0, 1)}</defs>"
        cxp, cyp, s = cx + dx, 44, 0.5
        g += (f'<g transform="rotate({rot} {cxp} {cyp})" filter="url(#softShadow)">'
              f'<path d="M{cxp-24*s},{cyp} C{cxp-24*s},{cyp-38*s} {cxp-8*s},{cyp-52*s} {cxp},{cyp-52*s} '
              f'C{cxp+8*s},{cyp-52*s} {cxp+24*s},{cyp-38*s} {cxp+24*s},{cyp} '
              f'C{cxp+24*s},{cyp+34*s} {cxp+8*s},{cyp+50*s} {cxp},{cyp+50*s} '
              f'C{cxp-8*s},{cyp+50*s} {cxp-24*s},{cyp+34*s} {cxp-24*s},{cyp} Z" fill="url(#{gid1})"/>'
              f'<path d="M{cxp-6*s},{cyp-46*s} C{cxp-16*s},{cyp-20*s} {cxp-16*s},{cyp+20*s} {cxp-6*s},{cyp+44*s} '
              f'L{cxp+6*s},{cyp+44*s} C{cxp-4*s},{cyp+18*s} {cxp-4*s},{cyp-20*s} {cxp+6*s},{cyp-46*s} Z" fill="url(#{gid2})"/>'
              f'</g>')
    # crushed sprinkle dots
    for _ in range(14):
        x = cx + random.uniform(-42, 42)
        y = 62 + random.uniform(-6, 14)
        g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.4,2.6):.1f}" fill="#7E9A50" opacity="0.8"/>'
    return g


def garnish_caramel(cx):
    g = f'<path d="M{cx-44},50 Q{cx-20},30 {cx},52 Q{cx+20},74 {cx+44},48" ' \
        f'stroke="#C97F1E" stroke-width="5" fill="none" opacity="0.85" stroke-linecap="round"/>'
    g += f'<path d="M{cx-34},64 Q{cx-10},50 {cx+10},64 Q{cx+26},76 {cx+38},62" ' \
         f'stroke="#E8960A" stroke-width="4" fill="none" opacity="0.7" stroke-linecap="round"/>'
    for i, (dx, kind) in enumerate([(-24, "alm"), (18, "cw")]):
        gid = f"garnNut{i}"
        cxp, cyp = cx + dx, 36
        if kind == "alm":
            g += f"<defs>{lingrad(gid, [(0, '#E8D2AE'), (1, '#B98A57')], 0, 0, 1, 1)}</defs>"
            g += (f'<ellipse cx="{cxp}" cy="{cyp}" rx="14" ry="22" fill="url(#{gid})" '
                  f'transform="rotate(-15 {cxp} {cyp})" filter="url(#softShadow)"/>')
        else:
            d, b = cashew_path(cxp, cyp, 0.55, 20, gid, [(0, "#F3E3C3"), (1, "#C79A5B")])
            g += f"<defs>{d}</defs>{b}"
    return g


def garnish_cookie(cx):
    gid = "garnCookie"
    g = f"<defs>{radgrad(gid, [(0, '#D9B27C'), (0.65, '#C4945A'), (1, '#9C6B38')], 0.4, 0.35, 0.85)}</defs>"
    g += f'<circle cx="{cx}" cy="36" r="26" fill="url(#{gid})" filter="url(#softShadow)" transform="rotate(-8 {cx} 36)"/>'
    for (dx, dy, r) in [(-8, -6, 3), (8, 2, 2.6), (-4, 10, 2.8), (10, -10, 2.4)]:
        g += f'<circle cx="{cx+dx}" cy="{36+dy}" r="{r}" fill="#3B2417"/>'
    g += f'<path d="M{cx-40},58 Q{cx},70 {cx+40},56" stroke="#C4945A" stroke-width="4" fill="none" opacity="0.6" stroke-linecap="round"/>'
    for (dx, dy, r) in [(-30, 44, 4), (28, 40, 3.4), (-6, 50, 3)]:
        g += f'<circle cx="{cx+dx}" cy="{dy}" r="{r}" fill="#9C6B38" opacity="0.85"/>'
    return g


def gen_shakes():
    build_shake("shake-strawberry.svg",
                [(0, "#FFC1CC"), (0.5, "#F06A83"), (1, "#C93B52")],
                garnish_strawberry)
    build_shake("shake-chocolate.svg",
                [(0, "#8A6142"), (0.5, "#5C3A21"), (1, "#3B2417")],
                garnish_chocolate)
    build_shake("shake-mango.svg",
                [(0, "#FFD98A"), (0.5, "#FFB100"), (1, "#E8960A")],
                garnish_mango)
    build_shake("shake-pistachio.svg",
                [(0, "#D3E0AE"), (0.5, "#A6C36F"), (1, "#7E9A50")],
                garnish_pistachio)
    build_shake("shake-caramel.svg",
                [(0, "#E8C48A"), (0.5, "#C4945A"), (1, "#A3702E")],
                garnish_caramel)
    build_shake("shake-cookie.svg",
                [(0, "#E7D3B0"), (0.5, "#C9A87A"), (1, "#9C7A4E")],
                garnish_cookie)


# ================================================================
# BOTTLE  — matching the classic glass milk-bottle product shot
# (240x400 viewBox, portrait)
# ================================================================

def gen_bottle():
    w, h = 240, 400
    defs = (lingrad("bottleGlass", [(0, "#FFFFFF"), (0.5, "#EEF5F8"), (1, "#DCE8EE")], 0, 0, 1, 0.15) +
            lingrad("bottleFill", [(0, "#FFC9D3"), (0.5, "#F6A0B2"), (1, "#EE87A0")], 0, 0, 0, 1) +
            lingrad("bottleCap", [(0, "#FF6F87"), (0.5, "#E8536B"), (1, "#B8324A")], 0, 0, 1, 1))
    svg = svg_open(w, h, defs)
    cx = w / 2
    svg += ground_shadow(cx, 382, 78, 12)

    neck_w, shoulder_y, body_w, body_top, body_bottom, body_r = 34, 96, 92, 118, 360, 20
    bottle_path = (
        f"M{cx-neck_w/2},48 L{cx+neck_w/2},48 "
        f"L{cx+neck_w/2},{shoulder_y-18} "
        f"C{cx+neck_w/2+8},{shoulder_y} {cx+body_w/2},{shoulder_y+10} {cx+body_w/2},{body_top} "
        f"L{cx+body_w/2},{body_bottom-body_r} "
        f"Q{cx+body_w/2},{body_bottom} {cx+body_w/2-body_r},{body_bottom} "
        f"L{cx-body_w/2+body_r},{body_bottom} "
        f"Q{cx-body_w/2},{body_bottom} {cx-body_w/2},{body_bottom-body_r} "
        f"L{cx-body_w/2},{body_top} "
        f"C{cx-body_w/2},{shoulder_y+10} {cx-neck_w/2-8},{shoulder_y} {cx-neck_w/2},{shoulder_y-18} Z"
    )
    svg += f'<path d="{bottle_path}" fill="url(#bottleGlass)" opacity="0.5" filter="url(#softShadow)"/>'
    svg += f'<clipPath id="bottleClip"><path d="{bottle_path}"/></clipPath>'
    fill_top = body_top + 26
    fill_path = (f"M{cx-body_w/2},{fill_top} L{cx+body_w/2},{fill_top} L{cx+body_w/2},{body_bottom} "
                 f"L{cx-body_w/2},{body_bottom} Z")
    svg += f'<g clip-path="url(#bottleClip)"><path d="{fill_path}" fill="url(#bottleFill)"/>'
    svg += f'<ellipse cx="{cx}" cy="{fill_top}" rx="{body_w/2}" ry="6" fill="#FFD9E0"/>'
    svg += f'<ellipse cx="{cx-body_w*0.22:.1f}" cy="{(fill_top+body_bottom)/2}" rx="9" ry="{(body_bottom-fill_top)/2*0.8}" fill="#FFFFFF" opacity="0.18"/></g>'
    svg += f'<path d="{bottle_path}" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.6"/>'

    # cap
    svg += f'<rect x="{cx-neck_w/2-2}" y="20" width="{neck_w+4}" height="30" rx="4" fill="url(#bottleCap)" filter="url(#softShadow)"/>'
    for i in range(4):
        svg += f'<line x1="{cx-neck_w/2-2}" y1="{28+i*6}" x2="{cx+neck_w/2+2}" y2="{28+i*6}" stroke="#0000001a" stroke-width="1.4"/>'
    svg += highlight(cx - neck_w * 0.22, 32, 4, 12, 0.4)

    # neck hang-tag with strawberry mark
    tag_w, tag_h, tag_x, tag_y = 30, 46, cx + neck_w / 2 - 4, 46
    svg += f'<rect x="{tag_x}" y="{tag_y}" width="{tag_w}" height="{tag_h}" rx="3" fill="url(#bottleCap)" filter="url(#softShadow)"/>'
    d_sb, body_sb = strawberry_body(tag_x + tag_w / 2, tag_y + 24, 0.26, grad_id="tagSb")
    svg += f"<defs>{d_sb}</defs>{body_sb}"
    svg += f'<text x="{tag_x+tag_w/2}" y="{tag_y+12}" font-family="Arial,sans-serif" font-weight="700" font-size="9" fill="#FFFFFF" text-anchor="middle">100%</text>'

    # label band
    label_y, label_h = 232, 92
    svg += (f'<rect x="{cx-body_w/2+2}" y="{label_y}" width="{body_w-4}" height="{label_h}" '
            f'fill="url(#bottleCap)" filter="url(#softShadow)"/>')
    svg += f'<circle cx="{cx+body_w*0.28:.1f}" cy="{label_y+label_h*0.3:.1f}" r="{body_w*0.6:.1f}" fill="#FFFFFF" opacity="0.08"/>'
    svg += (f'<text x="{cx}" y="{label_y+34}" font-family="Georgia,serif" font-weight="700" font-size="19" '
            f'fill="#FFFFFF" text-anchor="middle">STRAWBERRY</text>')
    svg += (f'<text x="{cx}" y="{label_y+58}" font-family="Georgia,serif" font-weight="700" font-size="19" '
            f'fill="#FFFFFF" text-anchor="middle">MILKSHAKE</text>')
    svg += (f'<text x="{cx}" y="{label_y+78}" font-family="Arial,sans-serif" font-weight="600" font-size="10" '
            f'letter-spacing="2" fill="#FFFFFF" opacity="0.85" text-anchor="middle">SHAKE FACTORY</text>')

    # condensation
    for (dx, dy, r) in [(-26, 30, 3.2), (22, 60, 2.6), (-16, 90, 2.4), (28, 20, 2.8), (-6, 130, 2.2)]:
        svg += f'<circle cx="{cx+dx}" cy="{fill_top+dy}" r="{r}" fill="#FFFFFF" opacity="0.55"/>'
    svg += svg_close()
    write("bottle.svg", svg)


# ================================================================
# SPLASH RING  — the two-tone (fruit / cream) pour ring transition
# (300x320 viewBox)
# ================================================================

def _ribbon_path(cx, cy, R, theta_start, theta_end, n=36, seed=0):
    outer, inner = [], []
    for i in range(n + 1):
        t = theta_start + (theta_end - theta_start) * i / n
        rad = math.radians(t)
        frac = i / n
        wob = 1 + 0.05 * math.sin(frac * 9 + seed) + 0.03 * math.sin(frac * 17 + seed * 2)
        width = 16 + 26 * math.sin(math.pi * frac) ** 0.7
        ro = R * wob + width / 2
        ri = R * wob - width / 2
        outer.append((cx + ro * math.sin(rad), cy - ro * math.cos(rad)))
        inner.append((cx + ri * math.sin(rad), cy - ri * math.cos(rad)))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", outer


def gen_splash_ring():
    w, h = 300, 320
    cx, cy, R = 150, 168, 108
    defs = (lingrad("ringRed", [(0, "#FF8FA3"), (0.5, "#E8536B"), (1, "#A32B42")], 0, 0, 1, 1) +
            lingrad("ringCream", [(0, "#FFFFFF"), (0.5, "#F7F1E6"), (1, "#E3D6BE")], 0, 0, 1, 1))
    svg = svg_open(w, h, defs)

    left_path, left_pts = _ribbon_path(cx, cy, R, -18, -182, seed=1)
    right_path, right_pts = _ribbon_path(cx, cy, R, 18, 182, seed=4)

    # Kept deliberately light on shape count: an SVG group filter
    # (feDropShadow) forces the browser to rasterize+blur everything
    # inside it, so a big group full of dozens of small shapes is
    # expensive to paint on first render, especially stacked alongside
    # the many other filtered elements in the hero. A plain CSS
    # drop-shadow on the <img> itself (see .hero__splash) gives the
    # same grounding shadow far more cheaply, so no SVG-level filter
    # is used here at all.
    g = "<g>"
    g += f'<path d="{left_path}" fill="url(#ringRed)"/>'
    g += f'<path d="{right_path}" fill="url(#ringCream)"/>'
    # a handful of foam/splatter blobs along each ribbon's outer edge
    for (pts, fill) in ((left_pts, "#F0637A"), (right_pts, "#FFFFFF")):
        for i in range(4, len(pts) - 4, 7):
            x, y = pts[i]
            r = random.uniform(3, 6)
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" opacity="0.7"/>'
    g += "</g>"
    svg += g

    # two strawberries falling into the top gap
    d1, b1 = strawberry_body(cx - 22, 26, 0.42, grad_id="ringSb1")
    d2, b2 = strawberry_body(cx + 20, 44, 0.36, grad_id="ringSb2")
    svg = svg.replace("<defs>", f"<defs>{d1}{d2}", 1)
    svg += b1 + b2
    svg += highlight(cx - R * 0.5, cy - R * 0.6, 20, 30, 0.25, rotate=-20)
    svg += svg_close()
    write("splash-ring.svg", svg)


if __name__ == "__main__":
    # gen_strawberry() is intentionally not called — strawberry.png is now
    # a real cutout photo (see assets/images/README.md). The function is
    # left in place since strawberry_body() (used by shake garnishes,
    # splash-ring.svg, and bottle.svg's hang-tag) still depends on it.
    gen_banana()
    gen_mango()
    gen_blueberries()
    gen_almonds()
    gen_cashews()
    gen_pistachios()
    gen_hazelnuts()
    gen_chocolate()
    gen_cookie()
    gen_milk_splash()
    gen_whipped_cream()
    gen_ice_cubes()
    gen_shakes()
    gen_bottle()
    gen_splash_ring()
    print("done")
