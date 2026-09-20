#!/usr/bin/env python3
"""
Removes a checkerboard "transparency preview" background baked into a
flattened JPG/PNG (the classic two-tone grey checker pattern some image
tools export when you save a "transparent" PNG as a JPG, losing the real
alpha channel). Unlike remove_bg.py (single solid background color), this
keys on pixels that are both near-grayscale (R ≈ G ≈ B) and light,
which the checker squares are and real food photography usually isn't.

Usage:
    python3 scripts/remove_bg_checker.py input.jpg output.png [gray_tol] [min_light]

Requires numpy and scipy (pip install numpy scipy).
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def remove_checker_bg(path, out_path, gray_tol=14, min_light=195, feather=2.0):
    im = Image.open(path).convert("RGB")
    arr = np.array(im).astype(np.int16)
    h, w, _ = arr.shape

    spread = arr.max(axis=2) - arr.min(axis=2)
    lightness = arr.mean(axis=2)
    bg_mask = (spread < gray_tol) & (lightness > min_light)

    labeled, n = ndimage.label(bg_mask)
    border_labels = set(labeled[0, :]) | set(labeled[-1, :]) | set(labeled[:, 0]) | set(labeled[:, -1])
    border_labels.discard(0)
    connected_bg = np.isin(labeled, list(border_labels))

    alpha = np.where(connected_bg, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L")
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))

    rgba = im.convert("RGBA")
    rgba.putalpha(alpha_img)

    bbox = alpha_img.point(lambda p: 255 if p > 10 else 0).getbbox()
    if bbox:
        pad = 14
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
    gray_tol = float(sys.argv[3]) if len(sys.argv) > 3 else 14
    min_light = float(sys.argv[4]) if len(sys.argv) > 4 else 195
    remove_checker_bg(src, dst, gray_tol=gray_tol, min_light=min_light)
