# About these images

This folder is a mix of **real photographs** (supplied by the site owner)
and **hand-crafted SVG illustrations** (generated to fill in the gaps
where no photo exists yet). Every real photo listed below was uploaded
by the site owner, converted to WebP, and had its background cleaned up
where needed — nothing here is AI-generated.

## Real photographs (12 files)

| File | Shows | Source |
|---|---|---|
| `strawberry.png` | Two strawberries, transparent bg | user-supplied |
| `strawberry-alt.webp` | Single heart-shaped strawberry | user-supplied (bg removed) |
| `banana.webp` | Single banana, transparent bg | user-supplied |
| `mango.webp` | Six mango slices/wedges | user-supplied (bg removed) |
| `blueberries.webp` | Cluster of 4 (composited from one real blueberry photo, rotated/scaled — same photograph, arranged as a group) | user-supplied |
| `almonds.webp` | Scattered almond group | user-supplied |
| `cashews.webp` | Cashew group | user-supplied |
| `pistachios.webp` | Single opened pistachio | user-supplied |
| `chocolate.webp` | Chocolate syrup swirl | user-supplied |
| `ice-cubes.webp` | Ice cube cluster | user-supplied |
| `milk-splash.webp` | Milk swirl/splash | user-supplied |
| `photo-shake-jar.jpg`, `photo-shake-cookie.webp`, `photo-sundae-strawberry.webp` | Three full real milkshake/dessert photographs, used in the new "Shot, not rendered" showcase section | user-supplied |

## Still SVG illustrations (no matching photo yet)

`hazelnuts.svg`, `whipped-cream.svg`, `cookie.svg` (the plain ingredient
one — `shake-cookie.svg` is different), the six `shake-*.svg` glass
illustrations, `bottle.svg`, and `splash-ring.svg`. See
[`scripts/generate_svg_assets.py`](../../scripts/generate_svg_assets.py)
if you want to regenerate or tweak any of these — send real photos for
any of them and they'll get swapped the same way the rest were.

## How the real photos were processed

Photos that arrived already on a transparent background were used as-is
(just resized/re-encoded to WebP for file size). A few arrived on a
plain white/grey studio background as JPGs — those had their background
removed with [`scripts/remove_bg.py`](../../scripts/remove_bg.py): it
samples the corner color, flood-fills matching pixels connected to the
image border (so a bright highlight inside the subject isn't mistaken
for background), and feathers the edge — no AI background-removal tool
involved. Run it as `python3 scripts/remove_bg.py in.jpg out.png` on any
future studio-background photo.

## Swapping in more real photography

Same process as before — no code restructuring needed:

1. Save your photo (JPG/PNG/WebP, transparent or clean background for
   cutouts) into `assets/images/`.
2. In `index.html`, find the `<img src="assets/images/NAME.ext">` tag for
   that item and point `src` at your new file.
3. For the three section backgrounds (hero, signature, craft), replace
   the CSS gradient in `css/style.css` — search `.hero__bg`,
   `.signature__bg`, `.craft__bg` — with a `background-image: url(...)`.

## Where things are used

- **Hero** — `strawberry.png` (tumble/scatter) + `strawberry-alt.webp`
  (one scatter spot, for variety) + `bottle.svg` + `shake-strawberry.svg`
  + `splash-ring.svg`.
- **Ingredients depth scene** — all 9 ingredient photos above, plus
  `hazelnuts.svg` and `whipped-cream.svg`.
- **Signature** — `shake-strawberry.svg` + strawberry floaters.
- **Collection (menu cards)** — the six `shake-*.svg` illustrations.
- **Showcase** (new section, between Menu and Our Craft) — the three
  full real product photographs.
- **Our Craft** — 6 tiles: strawberries, cashews, chocolate (real
  photos), whipped cream (illustration), banana, mango (real photos).

## Regenerating the illustrations

```
python3 scripts/generate_svg_assets.py
```

All shapes/gradients/colors for the remaining SVGs are defined in that
one script.
