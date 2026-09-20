#!/usr/bin/env python3
"""
Removes a uniform (studio white/grey) background from a photo, keeping
only the background region that's connected to the image border (so a
bright highlight inside the subject isn't mistaken for background).

Usage:
    python3 scripts/remove_bg.py input.jpg output.png [tolerance]

tolerance (default 28) is the max color distance from the sampled corner
color still considered "background" — raise it if some background is
left over, lower it if part of the subject is getting cut away.

Requires numpy and scipy (pip install numpy scipy).
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def remove_bg(path, out_path, tol=28, feather=2.5):
    im = Image.open(path).convert("RGB")
    arr = np.array(im).astype(np.int16)
    h, w, _ = arr.shape

    # estimate bg color from the four corners (average of small patches)
    patches = [arr[0:8, 0:8], arr[0:8, w-8:w], arr[h-8:h, 0:8], arr[h-8:h, w-8:w]]
    bg_color = np.mean([p.reshape(-1, 3).mean(axis=0) for p in patches], axis=0)

    dist = np.sqrt(((arr - bg_color) ** 2).sum(axis=2))
    bg_mask = dist < tol

    # only keep background connected to the border (flood fill from edges)
    labeled, n = ndimage.label(bg_mask)
    border_labels = set(labeled[0, :]) | set(labeled[-1, :]) | set(labeled[:, 0]) | set(labeled[:, -1])
    border_labels.discard(0)
    connected_bg = np.isin(labeled, list(border_labels))

    alpha = np.where(connected_bg, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L")
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))

    rgba = im.convert("RGBA")
    rgba.putalpha(alpha_img)

    # crop to the bounding box of the non-transparent content, with a bit of padding
    bbox = alpha_img.point(lambda p: 255 if p > 10 else 0).getbbox()
    if bbox:
        pad = 12
        l, t, r, b = bbox
        l = max(0, l - pad); t = max(0, t - pad)
        r = min(w, r + pad); b = min(h, b + pad)
        rgba = rgba.crop((l, t, r, b))

    rgba.save(out_path)
    print(f"{path} -> {out_path}  {rgba.size}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 28
    remove_bg(src, dst, tol=tol)
