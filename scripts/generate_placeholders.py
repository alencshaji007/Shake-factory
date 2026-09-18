"""
Generates clearly-labeled PLACEHOLDER art for Shake Factory.

These are NOT fake food renders — they are neutral, honestly-labeled
photo slots (a color swatch + dashed frame + filename) so the site can
be previewed and so it is obvious, at a glance, exactly which file to
swap for a real photograph. See assets/images/README.md for the full
replacement guide.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/user/Shake-factory/assets/images"

PALETTE = {
    "cream": (250, 243, 234),
    "warm_white": (255, 248, 240),
    "chocolate": (59, 36, 23),
    "chocolate_soft": (92, 58, 33),
    "strawberry": (232, 83, 107),
    "strawberry_soft": (255, 143, 163),
    "mango": (255, 177, 0),
    "mango_soft": (255, 201, 77),
    "pistachio": (143, 174, 93),
    "pistachio_soft": (166, 195, 111),
    "ink": (43, 30, 22),
}

def font(size, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def radial_gradient(size, c1, c2):
    w, h = size
    img = Image.new("RGB", size, c1)
    px = img.load()
    cx, cy = w / 2, h / 2
    maxd = math.hypot(cx, cy)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / maxd
            col = lerp(c1, c2, min(1, d))
            px[x, y] = col
            if x + 1 < w:
                px[x + 1, y] = col
            if y + 1 < h:
                px[x, y + 1] = col
            if x + 1 < w and y + 1 < h:
                px[x + 1, y + 1] = col
    return img

def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask

def add_noise(img, amount=6):
    px = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.04)):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        n = random.randint(-amount, amount)
        r, g, b = px[x, y][:3]
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img

def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=f) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def placeholder_cutout(name, label, sub, size=(900, 900), c1=None, c2=None):
    """A soft rounded, dashed-frame photo slot on a TRANSPARENT background —
    meant to sit inside the composited scene exactly where a real cutout
    photograph (strawberry.png etc.) would go."""
    c1 = c1 or PALETTE["cream"]
    c2 = c2 or PALETTE["warm_white"]
    w, h = size
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))

    pad = int(w * 0.06)
    card_size = (w - pad * 2, h - pad * 2)
    card = radial_gradient(card_size, c1, c2).convert("RGBA")
    mask = rounded_mask(card_size, int(min(card_size) * 0.12))
    card.putalpha(mask)

    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [pad, pad + int(h * 0.035), w - pad, h - pad + int(h * 0.035)],
        radius=int(min(card_size) * 0.12), fill=(20, 12, 8, 90)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(w * 0.03)))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(card, (pad, pad), card)

    draw = ImageDraw.Draw(canvas)
    dash_col = (*PALETTE["ink"], 130)
    step, gap = 16, 10
    x0, y0, x1, y1 = pad, pad, w - pad, h - pad
    x = x0
    while x < x1:
        draw.line([(x, y0), (min(x + step, x1), y0)], fill=dash_col, width=3)
        draw.line([(x, y1), (min(x + step, x1), y1)], fill=dash_col, width=3)
        x += step + gap
    y = y0
    while y < y1:
        draw.line([(x0, y), (x0, min(y + step, y1))], fill=dash_col, width=3)
        draw.line([(x1, y), (x1, min(y + step, y1))], fill=dash_col, width=3)
        y += step + gap

    f_label = font(int(w * 0.075))
    f_sub = font(int(w * 0.028), bold=False)
    f_tag = font(int(w * 0.024))

    cy = h * 0.46
    lines = wrap_text(draw, label, f_label, card_size[0] * 0.8)
    total_h = len(lines) * int(w * 0.09)
    ty = cy - total_h / 2
    for line in lines:
        tw = draw.textlength(line, font=f_label)
        draw.text((w / 2 - tw / 2, ty), line, font=f_label, fill=(*PALETTE["ink"], 235))
        ty += int(w * 0.09)

    sub_lines = wrap_text(draw, sub, f_sub, card_size[0] * 0.72)
    sy = ty + int(w * 0.02)
    for line in sub_lines:
        tw = draw.textlength(line, font=f_sub)
        draw.text((w / 2 - tw / 2, sy), line, font=f_sub, fill=(*PALETTE["ink"], 170))
        sy += int(w * 0.04)

    tag = f"assets/images/{name}"
    tw = draw.textlength(tag, font=f_tag)
    draw.text((w / 2 - tw / 2, h - pad - int(h * 0.06)), tag, font=f_tag, fill=(*PALETTE["ink"], 200))

    canvas.save(f"{OUT}/{name}")
    print("wrote", name)

def placeholder_scene_bg(name, label, sub, size=(2400, 1500), c1=None, c2=None):
    """A quiet full-bleed gradient with a small corner watermark only —
    kept deliberately unobtrusive since real page copy sits on top of it."""
    c1 = c1 or PALETTE["chocolate"]
    c2 = c2 or PALETTE["chocolate_soft"]
    w, h = size
    img = radial_gradient(size, c1, c2)
    img = add_noise(img, 4)
    img = img.filter(ImageFilter.GaussianBlur(1))
    draw = ImageDraw.Draw(img)

    f_label = font(int(w * 0.016))
    f_sub = font(int(w * 0.011), bold=False)
    pad = int(w * 0.025)

    draw.text((pad, h - pad - int(w * 0.05)), label, font=f_label, fill=(255, 248, 240, 130))
    sub_lines = wrap_text(draw, sub, f_sub, w * 0.34)
    sy = h - pad - int(w * 0.05) + int(w * 0.024)
    for line in sub_lines:
        draw.text((pad, sy), line, font=f_sub, fill=(255, 248, 240, 95))
        sy += int(w * 0.016)

    tag = f"assets/images/{name}"
    draw.text((pad, sy + int(w * 0.01)), tag, font=f_sub, fill=(255, 248, 240, 110))

    img.convert("RGB").save(f"{OUT}/{name}", quality=90)
    print("wrote", name)


INGREDIENTS = [
    ("strawberry.png", "STRAWBERRY", "real cutout photo, transparent bg", PALETTE["strawberry_soft"], PALETTE["strawberry"]),
    ("banana.png", "BANANA", "real cutout photo, transparent bg", PALETTE["mango_soft"], (235, 196, 84)),
    ("mango.png", "MANGO", "real cutout photo, transparent bg", PALETTE["mango"], PALETTE["mango_soft"]),
    ("blueberries.png", "BLUEBERRIES", "real cutout photo, transparent bg", (110, 120, 200), (70, 80, 150)),
    ("almonds.png", "ALMONDS", "real cutout photo, transparent bg", (210, 178, 130), (170, 138, 95)),
    ("cashews.png", "CASHEWS", "real cutout photo, transparent bg", (222, 196, 150), (188, 158, 108)),
    ("pistachios.png", "PISTACHIOS", "real cutout photo, transparent bg", PALETTE["pistachio_soft"], PALETTE["pistachio"]),
    ("hazelnuts.png", "HAZELNUTS", "real cutout photo, transparent bg", (168, 118, 74), (120, 80, 48)),
    ("chocolate.png", "CHOCOLATE PIECES", "real cutout photo, transparent bg", PALETTE["chocolate_soft"], PALETTE["chocolate"]),
    ("cookie.png", "COOKIE PIECES", "real cutout photo, transparent bg", (196, 148, 96), (150, 104, 60)),
    ("milk-splash.png", "MILK SPLASH", "real cutout photo, transparent bg", (255, 253, 248), (232, 224, 210)),
    ("whipped-cream.png", "WHIPPED CREAM", "real cutout photo, transparent bg", (255, 251, 244), (240, 230, 212)),
    ("ice-cubes.png", "ICE CUBES", "real cutout photo, transparent bg", (225, 240, 245), (190, 215, 225)),
]

SHAKES = [
    ("shake-strawberry.png", "STRAWBERRY CLOUD", "real product photograph", PALETTE["strawberry_soft"], PALETTE["strawberry"]),
    ("shake-chocolate.png", "CHOCO OVERLOAD", "real product photograph", PALETTE["chocolate_soft"], PALETTE["chocolate"]),
    ("shake-mango.png", "MANGO BLAST", "real product photograph", PALETTE["mango_soft"], PALETTE["mango"]),
    ("shake-pistachio.png", "PISTACHIO DREAM", "real product photograph", PALETTE["pistachio_soft"], PALETTE["pistachio"]),
    ("shake-caramel.png", "NUTTY CARAMEL", "real product photograph", (214, 165, 96), (163, 112, 56)),
    ("shake-cookie.png", "COOKIE MONSTER", "real product photograph", (198, 176, 150), (120, 90, 62)),
]

BACKGROUNDS = [
    ("bg-hero.jpg", "SHAKE FACTORY", "cinematic opening backdrop — replace with a real studio / kitchen photograph", PALETTE["chocolate"], PALETTE["chocolate_soft"]),
    ("bg-texture-marble.jpg", "PRODUCT SECTION BACKDROP", "replace with real marble / warm studio surface photo", PALETTE["cream"], PALETTE["warm_white"]),
    ("bg-dark-choc.jpg", "DARK SECTION BACKDROP", "replace with real dark chocolate / walnut surface photo", (36, 22, 15), PALETTE["chocolate"]),
]

if __name__ == "__main__":
    random.seed(7)
    for fname, label, sub, c1, c2 in INGREDIENTS:
        placeholder_cutout(fname, label, sub, size=(900, 900), c1=c1, c2=c2)
    for fname, label, sub, c1, c2 in SHAKES:
        placeholder_cutout(fname, label, sub, size=(1000, 1400), c1=c1, c2=c2)
    for fname, label, sub, c1, c2 in BACKGROUNDS:
        placeholder_scene_bg(fname, label, sub, c1=c1, c2=c2)
    print("done")
