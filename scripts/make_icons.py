#!/usr/bin/env python3
"""Site images from pahud's three mascot sources (raw originals are not committed).

    python3 scripts/make_icons.py [SRC_DIR]     # default ~/Downloads

Sources, by file name in SRC_DIR:
  STICKER  "Glossy Pastel Jellyfish Sticker.png"  1230x1278 RGBA, die-cut outline + shadow
  MASCOT   "Kawaii Pastel Jellyfish Mascot.png"   1254x1254 RGB, lavender-white field
  CARDS    "Kawaii Purple Octopus Sticker.png", "oab-{classic,pty,computer,sb,nearpush}.png"
           RGBA stickers for the octobroker, OpenAB Classic/PTY, oab-computer, oab-sb,
           oab-nearpush cards

Outputs in assets/:
  brand-{64,128}.png        sticker padded to a transparent square (header, 1x/2x)
  favicon-{16,32,64}.png    16/32 use the bell only (the tentacles turn to mush there)
  apple-touch-icon.png      180, full sticker on the page field (iOS ignores alpha)
  hero-{224,448}.webp       mascot, white field un-blended to alpha, edges faded to 0
  hero-dark-{224,448}.webp  sticker, the hero on the dark theme
  <card>-{56,112}.png       card stickers padded to a square (product cards, 1x/2x)
  openab-{connect,remote}-{56,112}.png  app icons from ~/repo/connect-site, inset to 88%
  og-mascot.webp (scripts/) 640 square faded mascot, input to og_cards.py (not served)

The source alpha has stray 1-valued pixels out to the canvas edge, so content bounds
are taken at alpha > 8; at that threshold none of the art reaches an edge.
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path.home() / "Downloads")
STICKER = SRC / "Glossy Pastel Jellyfish Sticker.png"
MASCOT = SRC / "Kawaii Pastel Jellyfish Mascot.png"
CARDS = {                        # product-card stickers, all RGBA on transparent
    "octobroker": SRC / "Kawaii Purple Octopus Sticker.png",   # 1254x1254
    "oab-classic": SRC / "oab-classic.png",                    # 1278x1230
    "oab-pty": SRC / "oab-pty.png",                            # 1254x1254
    "oab-computer": SRC / "oab-computer.png",                  # 1290x1219
    "oab-sb": SRC / "oab-sb.png",                              # 1278x1230
    "oab-nearpush": SRC / "oab-nearpush.png",                  # 1254x1254, art left of centre
}
APPS = {                         # app icons as served on connect.openab.dev (squircle, RGBA)
    "openab-connect": pathlib.Path.home() / "repo/connect-site/icon.png",
    "openab-remote": pathlib.Path.home() / "repo/connect-site/remote-icon.png",
}
APP_SCALE = 0.88                 # squircle fills its box; inset to match the stickers' weight
FIELD = (0xF7, 0xF4, 0xFC)       # --bg in style.css
A = ROOT / "assets"


def bounds(im, t=8):
    return im.split()[3].point(lambda v: 255 if v > t else 0).getbbox()


def square(im, margin, box=None):
    """Crop to the alpha bounds (or box), centre on a transparent square with margin."""
    im = im.crop(box or bounds(im))
    side = round(max(im.size) * (1 + 2 * margin))
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    return out


def save(im, name, px, **kw):
    dest = A / name
    im.resize((px, px), Image.LANCZOS).save(dest, **kw)
    return dest


def faded_mascot():
    """Square around the mascot; alpha 1 over the art, smoothstep to 0 at the edge.

    The fade follows a rounded rectangle around the art (bbox of saturation > 25,
    measured (284,113)-(1067,1015) incl. the glow), so the curls in the lower corners
    stay opaque while every edge pixel of the square is fully transparent.
    """
    im = Image.open(MASCOT).convert("RGB")
    x0, y0, side = 110, 0, 1130                  # centred on the art, inside the source
    im = im.crop((x0, y0, x0 + side, y0 + side))
    art = (284 - x0 - 20, 113 - y0 - 20, 1067 - x0 + 20, 1015 - y0 + 20)
    yy, xx = np.mgrid[0:side, 0:side].astype(np.float64)
    dx = np.maximum(np.maximum(art[0] - xx, xx - art[2]), 0)
    dy = np.maximum(np.maximum(art[1] - yy, yy - art[3]), 0)
    d = np.hypot(dx, dy)                         # 0 inside the art box
    edge = np.minimum(np.minimum(xx, side - 1 - xx), np.minimum(yy, side - 1 - yy))
    t = np.clip(d / np.maximum(d + edge, 1e-6), 0, 1)   # 0 at art box, 1 at the edge
    alpha = 1 - t * t * (3 - 2 * t)
    # Colour-to-alpha against white: the field is near-white, so take each pixel's
    # distance from white as its opacity and un-blend the colour. The white field then
    # disappears (no lighter rectangle on a lavender page); the smoothstep above still
    # zeroes the faint lavender wash before it reaches the square's edge.
    rgb = np.asarray(im, dtype=np.float64)
    # Distances below 36 are the field itself (white, plus a lavender wash up to 33 on
    # the right); they map to 0 so the field leaves no tint or box on the page.
    ca = np.clip(((255 - rgb).max(axis=2) - 36) / 80, 0, 1)
    # Pale highlights inside the bell are below that floor too, so everything enclosed by
    # the art (not reachable from the border through pale field) stays opaque.
    sil = Image.fromarray(np.where((255 - rgb).max(axis=2) > 60, 255, 0).astype(np.uint8)).copy()
    ImageDraw.floodfill(sil, (0, 0), 128)
    inside = np.asarray(sil) != 128
    inside = np.asarray(Image.fromarray(inside.astype(np.uint8) * 255)
                        .filter(ImageFilter.GaussianBlur(2)), dtype=np.float64) / 255
    ca = np.maximum(ca, inside)
    col = 255 - (255 - rgb) / np.maximum(ca, 1e-6)[..., None]
    out = np.dstack([np.clip(col, 0, 255), ca * alpha * 255])
    return Image.fromarray(out.round().astype(np.uint8))


def main():
    made = []
    st = Image.open(STICKER).convert("RGBA")
    full = square(st, 0.03)
    made += [save(full, "brand-64.png", 64, optimize=True),
             save(full, "brand-128.png", 128, optimize=True),
             save(full, "favicon-64.png", 64, optimize=True)]
    # Bell only for the tiny favicons: from the top of the outline to just under the
    # scalloped rim (y 700 in source), full width of the bell.
    x0, y0, x1, _ = bounds(st)
    bell = square(st, 0.02, (x0 + 40, y0, x1 - 40, 700))
    made += [save(bell, "favicon-32.png", 32, optimize=True),
             save(bell, "favicon-16.png", 16, optimize=True)]
    touch = Image.new("RGBA", (180, 180), FIELD + (255,))
    s = square(st, 0.0).resize((150, 150), Image.LANCZOS)
    touch.alpha_composite(s, (15, 15))
    touch.convert("RGB").save(A / "apple-touch-icon.png", optimize=True)
    made.append(A / "apple-touch-icon.png")

    fm = faded_mascot()
    made += [save(fm, "hero-224.webp", 224, quality=88, method=6),
             save(fm, "hero-448.webp", 448, quality=88, method=6),
             save(full, "hero-dark-224.webp", 224, quality=88, method=6),
             save(full, "hero-dark-448.webp", 448, quality=88, method=6)]
    fm.resize((640, 640), Image.LANCZOS).save(ROOT / "scripts/og-mascot.webp", quality=92, method=6)

    # Card stickers: every one cropped to its own alpha bounds with the same margin, so
    # they share visual weight and baseline in the 56px slot.
    for name, src in CARDS.items():
        ic = square(Image.open(src).convert("RGBA"), 0.03)
        made += [save(ic, f"{name}-56.png", 56, optimize=True),
                 save(ic, f"{name}-112.png", 112, optimize=True)]
    for name, src in APPS.items():
        ic = Image.open(src).convert("RGBA")
        side = round(ic.width / APP_SCALE)
        sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        sq.alpha_composite(ic, ((side - ic.width) // 2, (side - ic.height) // 2))
        made += [save(sq, f"{name}-56.png", 56, optimize=True),
                 save(sq, f"{name}-112.png", 112, optimize=True)]
    for p in made:
        print(f"  {p.relative_to(ROOT)}  {Image.open(p).size[0]}px  {p.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
