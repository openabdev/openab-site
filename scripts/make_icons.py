#!/usr/bin/env python3
"""Square icons cut from the OpenAB banner: logo-512, apple-touch-icon (180), favicon-64.

The earlier logo was a tight square crop: the dome touched the top edge, the outer
tentacle curls touched the sides and the bottom cut the inner loops mid-curl, and the
rounded-tile radius in CSS then clipped the curls further. This crop takes the whole
jellyfish with ~12% margin on every side, so a radius of up to ~25% clips only field.

The banner's capability labels (CHAT BRIDGES, ...) fall inside that square. They are
dark grey on the pale field, clear of the pastel artwork, so they are found by colour
and filled from their surroundings by normalised convolution (a blur that ignores the
masked pixels), which leaves no seam.

    python3 scripts/make_icons.py [path/to/openab/images/banner.jpg]
"""
import pathlib
import sys

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNER = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                      else pathlib.Path.home() / "repo/openab/images/banner.jpg")

# Banner coordinates (6336x2688). Jellyfish bounds measured: x 780-2380, y 290-2070.
SQUARE = (465, 65, 2695, 2295)          # 2230 px, jellyfish centred with ~12% margin
TEXT_BAND = (465, 1880, 2695, 2400)     # where the labels are; nothing above is touched


def box_blur(a, r):
    """Mean over a (2r+1)^2 window, edges clamped; a is HxW or HxWxC float."""
    for axis in (0, 1):
        pad = [(0, 0)] * a.ndim
        pad[axis] = (r + 1, r)
        c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis)
        n = a.shape[axis]
        a = (np.take(c, range(2 * r + 1, 2 * r + 1 + n), axis=axis)
             - np.take(c, range(0, n), axis=axis)) / (2 * r + 1)
    return a


def dilate(m, r):
    return box_blur(m.astype(np.float64), r) > 1e-6


def paint_out_labels(im):
    x0, y0, x1, y1 = TEXT_BAND
    a = np.asarray(im, dtype=np.float64)
    band = a[y0:y1, x0:x1]
    lum = 0.299 * band[..., 0] + 0.587 * band[..., 1] + 0.114 * band[..., 2]
    sat = band.max(axis=2) - band.min(axis=2)
    text = dilate((lum < 140) & (sat < 40), 10)   # labels lum ~30, tentacles >= 160
    keep = (~text).astype(np.float64)
    fill = band.copy()
    for _ in range(3):                    # three box passes ~ gaussian
        num = box_blur(fill * keep[..., None], 40)
        den = box_blur(keep, 40)[..., None]
        fill = np.where(text[..., None], num / np.maximum(den, 1e-6), band)
    a[y0:y1, x0:x1] = fill
    return Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8)), int(text.sum())


def main():
    im, n = paint_out_labels(Image.open(BANNER).convert("RGB"))
    print(f"  painted out {n} label pixels")
    sq = im.crop(SQUARE)
    for name, px in (("logo-512.png", 512), ("apple-touch-icon.png", 180), ("favicon-64.png", 64)):
        dest = ROOT / "assets" / name
        sq.resize((px, px), Image.LANCZOS).save(dest, optimize=True)
        print(f"  {dest.relative_to(ROOT)} {px}x{px}")


if __name__ == "__main__":
    main()
