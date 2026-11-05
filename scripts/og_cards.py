#!/usr/bin/env python3
"""Sharing cards, one per language: og-<lang>.png at 1200x630, mode RGB.

Ported from connect.openab.dev's generator (layout measured from deepsrt.com): margin
x=75, icon 78px at (75, 63), headline at y=250/326, subtitle y=424, domain y=557,
text boundary x=820 with the watermark past it. Hue is the OpenAB banner's violet.

    python3 scripts/og_cards.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent

W, H = 1200, 630
MARGIN = 75
TEXT_R = 820
ICON_XY, ICON_PX = (75, 63), 78
HEAD_Y1, HEAD_Y2 = 250, 326
SUB_Y, DOMAIN_Y = 424, 557

GRAD_TOP, GRAD_BOTTOM = (0x35, 0x22, 0x66), (0x10, 0x0A, 0x22)
INK = (0xFF, 0xFF, 0xFF)
MUTED = (0xC9, 0xC0, 0xE0)
ACCENT = (0xC6, 0xB1, 0xF0)

LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/SFNSMono.ttf"
GB = "/System/Library/Fonts/Hiragino Sans GB.ttc"
KO = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FACE = {"en": LATIN, "zh": GB, "ja": "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", "ko": KO}
BOLD = {LATIN: 1, GB: 2, KO: 6}
HEAD_FACE = {"ja": GB}   # no bold Hiragino Sans cut installed; GB W6 agrees on kana

TEXT = {
    "en": (["Coding agents,", "on infrastructure you own."],
           "Chat broker, sandboxed terminal, Mac and iPhone apps, GitHub broker"),
    "zh": (["你的 Coding Agent，", "跑在你自己的基礎架構。"],
           "聊天室 broker、沙箱終端機、Mac 與 iPhone App、GitHub 憑證代管"),
    "ja": (["コーディングエージェントを、", "自分のインフラで。"],
           "チャットブローカー、サンドボックス端末、Mac と iPhone のアプリ"),
    "ko": (["코딩 에이전트를,", "내 인프라에서."],
           "채팅 브로커, 샌드박스 터미널, Mac·iPhone 앱, GitHub 브로커"),
}
DOMAIN = "openab.dev"
WORDMARK = "OpenAB"
ICON = ROOT / "assets/logo-512.png"
WATERMARK = ROOT / "assets/watermark.png"


def derive_watermark():
    """Jellyfish cut out of the logo by saturation, edges feathered with a linear ramp.

    The logo's field is a near-neutral lavender and the jellyfish is pastel but
    saturated, so max-min > 34 separates them; a distance-from-edge ramp is zero at
    the border by construction, so there is no seam at the paste column.
    """
    im = Image.open(ICON).convert("RGBA")
    px = im.load()
    w0, h0 = im.size
    xs, ys = [], []
    for x in range(0, w0, 2):
        for y in range(0, h0, 2):
            r, g, b, a = px[x, y]
            if a > 200 and max(r, g, b) - min(r, g, b) > 34:
                xs.append(x)
                ys.append(y)
    pad = 20
    crop = im.crop((max(0, min(xs) - pad), max(0, min(ys) - pad),
                    min(w0, max(xs) + pad), min(h0, max(ys) + pad)))
    w, h = crop.size
    # Alpha by saturation as well, so the pale field inside the crop drops out.
    cp = crop.load()
    alpha = Image.new("L", (w, h))
    ap = alpha.load()
    feather = int(min(w, h) * 0.22)
    for x in range(w):
        dx = min(x, w - 1 - x)
        for y in range(h):
            r, g, b, a = cp[x, y]
            sat = max(r, g, b) - min(r, g, b)
            base = 0 if sat < 20 else min(255, (sat - 20) * 255 // 30)
            d = min(dx, y, h - 1 - y)
            ap[x, y] = base * min(255, d * 255 // feather) // 255
    crop.putalpha(alpha)
    crop.save(WATERMARK)
    print(f"  derived {WATERMARK.relative_to(ROOT)} {crop.size}, feather {feather}px")


def font(path, size, bold=False):
    idx = BOLD.get(path, 0) if bold else 0
    try:
        return ImageFont.truetype(path, size, index=idx)
    except OSError:
        return ImageFont.truetype(path, size)


def width(draw, text, f):
    return draw.textbbox((0, 0), text, font=f)[2]


def fit(draw, lines, path, start, floor, limit):
    for size in range(start, floor - 1, -1):
        f = font(path, size, bold=True)
        if all(MARGIN + width(draw, l, f) <= limit for l in lines):
            return f, size
    return font(path, floor, bold=True), floor


def gradient():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(round(GRAD_TOP[i] + (GRAD_BOTTOM[i] - GRAD_TOP[i]) * t) for i in range(3)))
    return im


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius, fill=255)
    im.putalpha(mask)
    return im


def build(lang):
    im = gradient()
    wm = Image.open(WATERMARK).convert("RGBA")
    wm_h = 520
    wm = wm.resize((round(wm.width * wm_h / wm.height), wm_h), Image.LANCZOS)
    wm.putalpha(wm.split()[3].point(lambda a: int(a * 0.22)))
    im.paste(wm, (W - wm.width + 150, (H - wm_h) // 2), wm)

    d = ImageDraw.Draw(im)
    mark = rounded(Image.open(ICON).convert("RGBA").resize((ICON_PX, ICON_PX), Image.LANCZOS), 18)
    im.paste(mark, ICON_XY, mark)
    wf = font(LATIN, 31, bold=True)
    wy = ICON_XY[1] + ICON_PX // 2 - d.textbbox((0, 0), WORDMARK, font=wf)[3] // 2 - 3
    d.text((ICON_XY[0] + ICON_PX + 18, wy), WORDMARK, font=wf, fill=INK)

    lines, sub = TEXT[lang]
    hpath = HEAD_FACE.get(lang, FACE[lang])
    hf, hsize = fit(d, lines, hpath, 58 if lang == "en" else 54, 34, TEXT_R)
    d.text((MARGIN, HEAD_Y1), lines[0], font=hf, fill=INK)
    d.text((MARGIN, HEAD_Y2 if hsize > 44 else HEAD_Y1 + hsize + 22), lines[1], font=hf, fill=INK)

    sf_size = 27 if lang == "en" else 25
    sf = font(FACE[lang], sf_size)
    while MARGIN + width(d, sub, sf) > TEXT_R and sf_size > 17:
        sf_size -= 1
        sf = font(FACE[lang], sf_size)
    d.text((MARGIN, SUB_Y), sub, font=sf, fill=MUTED)
    d.text((MARGIN, DOMAIN_Y), DOMAIN, font=font(MONO, 26), fill=ACCENT)

    dest = ROOT / f"og-{lang}.png"
    im.save(dest, optimize=True)
    over = [l for l in lines if MARGIN + width(d, l, hf) > TEXT_R]
    if MARGIN + width(d, sub, sf) > TEXT_R:
        over.append(sub)
    return dest, hsize, sf_size, "/".join(hf.getname()), over


if __name__ == "__main__":
    derive_watermark()
    for lang in ("en", "zh", "ja", "ko"):
        dest, hs, ss, name, over = build(lang)
        im = Image.open(dest)
        print(f"  {lang:3} {dest.name:10} {im.size[0]}x{im.size[1]} {im.mode:4} "
              f"head={hs}px sub={ss}px  {name}" + ("  OVERFLOW: %s" % over if over else ""))
