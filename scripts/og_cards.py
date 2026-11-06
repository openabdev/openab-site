#!/usr/bin/env python3
"""Sharing cards, one per language: og-<lang>.png at 1200x630, mode RGB.

Ported from connect.openab.dev's generator (layout measured from deepsrt.com): margin
x=75, icon 78px at (75, 63), headline at y=250/326, subtitle y=424, domain y=557,
text boundary x=780 (connect uses 820; narrower here for the art). Light field matching openab.dev; the art is
the jellyfish mascot with its edges faded to transparent (scripts/og-mascot.webp, made by
make_icons.py), so it blends into the field with no box edge.

    python3 scripts/og_cards.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent

W, H = 1200, 630
MARGIN = 75
TEXT_R = 780
ICON_XY, ICON_PX = (75, 63), 78
HEAD_Y1, HEAD_Y2 = 250, 326
SUB_Y, DOMAIN_Y = 424, 557

GRAD_LEFT, GRAD_RIGHT = (0xF7, 0xF4, 0xFC), (0xFC, 0xFB, 0xFE)   # site --bg family
INK = (0x22, 0x16, 0x40)
MUTED = (0x61, 0x5A, 0x78)
ACCENT = (0x7B, 0x62, 0xC9)
ART_PX, ART_X = 500, 730

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
ICON = ROOT / "assets/brand-128.png"
ART = ROOT / "scripts/og-mascot.webp"


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
    for x in range(W):
        t = x / (W - 1)
        d.line([(x, 0), (x, H)],
               fill=tuple(round(GRAD_LEFT[i] + (GRAD_RIGHT[i] - GRAD_LEFT[i]) * t) for i in range(3)))
    return im


def build(lang):
    im = gradient()
    im = im.convert("RGBA")
    art = Image.open(ART).convert("RGBA").resize((ART_PX, ART_PX), Image.LANCZOS)
    im.alpha_composite(art, (ART_X, (H - ART_PX) // 2))
    im = im.convert("RGB")

    d = ImageDraw.Draw(im)
    mark = Image.open(ICON).convert("RGBA").resize((ICON_PX, ICON_PX), Image.LANCZOS)
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
    for lang in ("en", "zh", "ja", "ko"):
        dest, hs, ss, name, over = build(lang)
        im = Image.open(dest)
        print(f"  {lang:3} {dest.name:10} {im.size[0]}x{im.size[1]} {im.mode:4} "
              f"head={hs}px sub={ss}px  {name}" + ("  OVERFLOW: %s" % over if over else ""))
