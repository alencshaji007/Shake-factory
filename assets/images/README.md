# About these images

This folder is a mix of **real photographs** (supplied by the site owner)
and **hand-crafted SVG illustrations** (generated to fill in the gaps
where no photo exists yet). Every real photo listed below was uploaded
by the site owner, converted to WebP, and had its background cleaned up
where needed — nothing here is AI-generated.

## Real photographs (16 files)

| File | Shows | Source |
|---|---|---|
| `photo-chocolate-mocha.webp` | Full real Chocolate Mocha milkshake — chocolate chunks, whipped cream, chocolate shavings and drizzle, transparent bg — used on the Chocolate Mocha menu card (replaced the "Cookie Monster" SVG illustration) | user-supplied |
| `strawberry.png` | Two strawberries, transparent bg | user-supplied |
| `strawberry-alt.webp` | Single heart-shaped strawberry | user-supplied (bg removed) |
| `photo-strawberry-shake.webp` | Full real strawberry milkshake in a glass, splash crown on top, transparent bg — *currently unused* (was the hero's product shot before that was replaced by the title-only hero, see below) | user-supplied |
| `banana.webp` | Single banana, transparent bg | user-supplied |
| `mango.webp` | Six mango wedges scattered mid-air, transparent bg | user-supplied (bg removed — arrived as a flattened JPG with a checkerboard "transparency preview" baked in, not real alpha; see below) |
| `blueberries.webp` | Cluster of 4 (composited from one real blueberry photo, rotated/scaled — same photograph, arranged as a group) | user-supplied |
| `almonds.webp` | Scattered group of ~16 whole almonds, transparent bg | user-supplied |
| `coffee-beans.webp` | Scattered group of 11 roasted coffee beans, transparent bg | user-supplied |
| `cashews.webp` | Cashew group | user-supplied |
| `pistachios.webp` | Single opened pistachio | user-supplied |
| `chocolate.webp` | Chocolate syrup swirl | user-supplied |
| `ice-cubes.webp` | Ice cube cluster | user-supplied |
| `milk-splash.webp` | Milk swirl/splash | user-supplied |
| `photo-shake-jar.jpg`, `photo-shake-cookie.webp`, `photo-sundae-strawberry.webp` | Three full real milkshake/dessert photographs, used in the new "Shot, not rendered" showcase section | user-supplied |

## Still SVG illustrations (no matching photo yet)

`hazelnuts.svg`, `whipped-cream.svg`, `cookie.svg` (the plain ingredient
one — `shake-cookie.svg` is different, and is now unused: the Cookie
Monster menu card was replaced by a real Chocolate Mocha photo, see
below), and the remaining five `shake-*.svg` glass illustrations (used
on the other five menu cards + signature section now — the hero uses
the real photo above instead). See
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

`mango.webp` needed a variant of that: it arrived as a JPG with a
two-tone grey checkerboard baked into the pixels (the classic
"transparency preview" pattern some editors flatten into an export) —
not a real alpha channel. [`scripts/remove_bg_checker.py`](../../scripts/remove_bg_checker.py)
keys on pixels that are both near-grayscale and light rather than a
single background color, then does the same border-connected flood
fill and feather. Run it as
`python3 scripts/remove_bg_checker.py in.jpg out.png` if another photo
shows up with that same checker pattern.

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

- **Hero** — `strawberry.png` (tumble), plus the WebGL 3D coffee
  bean/pistachio field described above. `photo-strawberry-shake.webp`
  (previously the hero's product shot, after the bottle+glass
  illustration and then the splash-ring transition were each removed
  in turn) is currently unused — the hero now settles the tumble
  straight into the "Shake Factory" title instead of a product shot.
  The file is kept in case it's wanted again; it's still a real,
  user-supplied photo.
- **Ingredients depth scene** — all 11 ingredient photos above (including
  the new `almonds.webp` and `coffee-beans.webp`), plus `hazelnuts.svg`
  and `whipped-cream.svg`. Every image in this scene has a slow,
  continuously-looping idle drift/rotate (see "Idle motion" below) on
  top of its scroll-driven parallax, so the section keeps moving gently
  even when the page isn't being scrolled.
- **Signature** — `shake-strawberry.svg` + strawberry floaters (also
  idle-drifting).
- **Collection (menu cards)** — five `shake-*.svg` illustrations, plus
  the real `photo-chocolate-mocha.webp` photo for the Chocolate Mocha
  card (was "Cookie Monster" / `shake-cookie.svg`).
- **Showcase** (new section, between Menu and Our Craft) — the three
  full real product photographs.
- **Our Craft** — 8 tiles in a 4-column grid: strawberries, cashews,
  chocolate, banana, mango, almonds, coffee beans (real photos) and
  whipped cream (illustration). Each tile has a slow idle "breathe"
  scale pulse.

## Idle motion ("alive" page feel)

Past their one-time scroll-triggered entrance, the ingredient images
above no longer sit perfectly still — each one loops a small
(±9px drift / ±1.6° rotate, or a subtle scale pulse on the Our Craft
circles) animation indefinitely, staggered per-image with different
durations/delays so nothing moves in lockstep. It's done with the
standalone CSS `translate`/`rotate`/`scale` properties (not `transform`)
specifically so it composes cleanly with whatever GSAP is doing to the
same element's `transform` for scroll parallax, instead of fighting it.
See `@keyframes idle-drift` / `idle-breathe` in `css/style.css`. It's
automatically disabled for `prefers-reduced-motion: reduce` along with
every other animation on the site.

Note: the hero section's floating coffee beans and pistachios are a
*separate* thing — a real WebGL 3D scene (`js/hero3d.js`, Three.js),
not this folder's `coffee-beans.webp` / `almonds.webp` photos rendered
as flat CSS sprites. Those two beans/pistachios are procedurally
modelled 3D geometry, built to feel consistent with the real photos
without depending on any texture file from this folder.

## Regenerating the illustrations

```
python3 scripts/generate_svg_assets.py
```

All shapes/gradients/colors for the remaining SVGs are defined in that
one script.
