# Replacing the placeholder images with real photography

Every image in this folder right now is a **generated placeholder** — a
soft color card with a dashed border and a text label (e.g. "STRAWBERRY —
real cutout photo, transparent bg"). They exist only so the site has
something to render and so you can see exactly where each photo goes.
**None of them are meant to look like food** — that's intentional, so
there's no chance of mistaking a placeholder for a finished shot.

To finish the site, replace each file below with a real photograph of the
same name, same format, and roughly the same aspect ratio. Nothing else in
the code needs to change — `index.html` and `css/style.css` already
reference these exact filenames.

## Where to find real, licensable food photography

- **Unsplash** — https://unsplash.com (free license, no attribution required)
- **Pexels** — https://pexels.com (free license, no attribution required)
- **Pixabay** — https://pixabay.com (free license, check per-image terms)
- **Wikimedia Commons** — https://commons.wikimedia.org (check each image's
  specific license — many require attribution)

Search terms that work well: "strawberry isolated white background",
"banana png transparent", "milkshake glass studio photography", etc.

## Removing backgrounds

For the ingredient/product cutouts (the `.png` files), you want a real
photo with a transparent or clean background. Options:
- Download an image that's already shot on white/seamless, then remove the
  background with [remove.bg](https://remove.bg) or Photoshop.
- Search directly for "transparent PNG" versions on Pngtree, Freepik (paid)
  or Unsplash/Pexels cutout collections.
- Export as WebP or PNG with alpha — either works, just keep the filename.

## Ingredient cutouts — square-ish, transparent background

| File | Used for | Suggested min size |
|---|---|---|
| `strawberry.png` | hero opener, ingredient scene, signature floaters, craft | 900×900 |
| `banana.png` | hero opener, ingredient scene | 900×900 |
| `mango.png` | hero opener, ingredient scene | 900×900 |
| `blueberries.png` | ingredient scene (back layer) | 900×900 |
| `almonds.png` | hero opener | 900×900 |
| `cashews.png` | hero opener, ingredient scene, craft | 900×900 |
| `pistachios.png` | hero opener, ingredient scene | 900×900 |
| `hazelnuts.png` | ingredient scene (back layer) | 900×900 |
| `chocolate.png` | hero opener, ingredient scene, craft | 900×900 |
| `cookie.png` | (spare — available for future cookie-themed sections) | 900×900 |
| `milk-splash.png` | hero opener | 900×900 |
| `whipped-cream.png` | ingredient scene, signature floaters, craft | 900×900 |
| `ice-cubes.png` | hero opener | 900×900 |

## Product photographs — portrait, studio milkshake shots

Each of these should be its **own** photograph — a different glass, a
different topping, a different color of shake. Don't reuse one shake photo
recolored six times; the brief for this site is real per-flavour identity.

| File | Product | Suggested min size |
|---|---|---|
| `shake-strawberry.png` | Strawberry Cloud (also the hero + signature shot) | 1000×1400 |
| `shake-chocolate.png` | Choco Overload | 1000×1400 |
| `shake-mango.png` | Mango Blast | 1000×1400 |
| `shake-pistachio.png` | Pistachio Dream | 1000×1400 |
| `shake-caramel.png` | Nutty Caramel | 1000×1400 |
| `shake-cookie.png` | Cookie Monster | 1000×1400 |

## Scene backgrounds — landscape, full-bleed

These sit behind sections at reduced opacity, so slightly darker/moodier
photos read best.

| File | Used for | Suggested min size |
|---|---|---|
| `bg-hero.jpg` | Full-screen opening scene backdrop | 2400×1500 |
| `bg-texture-marble.jpg` | Signature product section backdrop | 2400×1500 |
| `bg-dark-choc.jpg` | Dark "Our Craft" section backdrop | 2400×1500 |

## Regenerating placeholders

If you ever want to regenerate these placeholder cards (e.g. after
changing a product name), run:

```
pip install Pillow
python3 scripts/generate_placeholders.py
```

The script lives at `scripts/generate_placeholders.py` and is the single
source of truth for filenames, labels and colors.
