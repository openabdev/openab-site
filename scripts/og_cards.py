#!/usr/bin/env python3
"""Sharing cards, one per language: og-<lang>.png at 1200x630, mode RGB.

Ported from connect.openab.dev's generator (layout measured from deepsrt.com): margin
x=75, icon 78px at (75, 63), headline at y=250/326, subtitle y=424, domain y=557,
text boundary x=780 (connect uses 820; narrower here for the art). Light field matching openab.dev.

Right-side art: the home cards carry the jellyfish mascot (scripts/og-mascot.webp, made by
make_icons.py). Dev-note cards already show the mascot top left, so their right side carries an
illustration of the note's topic instead, never the mascot again. A note picks its art with
`og_art` in notes.py (a key of ARTS below); the notes index uses "notes". Any text in an
illustration is generic (role names, refs), and it must stay readable at a 600x315 thumbnail.

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
    "en": (["An open-source community", "that loves freedom and openness."],
           "A secure, private, reliable runtime for coding agents"),
    "zh": (["OpenAB 是一個熱愛", "自由與開放的開源社群。"],
           "安全、注重隱私、可靠的 coding agent 運行環境"),
    "ja": (["自由とオープンさを愛する", "オープンソースコミュニティ。"],
           "安全でプライバシーを守る、信頼できるエージェントの実行環境"),
    "ko": (["자유와 개방을 사랑하는", "오픈소스 커뮤니티."],
           "안전하고 프라이버시를 지키는, 믿을 수 있는 에이전트 실행 환경"),
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


# Topic illustrations, drawn at 2x on a transparent layer the size of the card, then scaled.
SS = 2
CARD = (0xFF, 0xFF, 0xFF)
TINT = (0xEC, 0xE6, 0xF8)
LINE = (0xD9, 0xD2, 0xEA)
DEEP = (0x3D, 0x1F, 0x79)


def dashed(d, pts, fill, width, dash=14, gap=9):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        pos = 0.0
        while pos < length:
            a, b = pos / length, min(pos + dash, length) / length
            d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a),
                    (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], fill=fill, width=width)
            pos += dash + gap


def dashed_rect(d, box, fill, width):
    x1, y1, x2, y2 = box
    dashed(d, [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], fill, width)


def window(d, x1, y1, x2, y2):
    s = SS
    d.rounded_rectangle([x1 * s + 6, y1 * s + 10, x2 * s + 6, y2 * s + 10], 18 * s, fill=(0xE4, 0xDD, 0xF3))
    d.rounded_rectangle([x1 * s, y1 * s, x2 * s, y2 * s], 18 * s, fill=CARD, outline=LINE, width=2 * s)
    d.rounded_rectangle([x1 * s, y1 * s, x2 * s, (y1 + 40) * s], 18 * s, fill=TINT)
    d.rectangle([x1 * s + 2 * s, (y1 + 22) * s, x2 * s - 2 * s, (y1 + 40) * s], fill=TINT)
    for i in range(3):
        cx, cy = (x1 + 24 + i * 20) * s, (y1 + 20) * s
        d.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=(0xC9, 0xBD, 0xE8))


def art_ax_tree(layer):
    """An app window with a highlighted button, and its accessibility tree (e1/e2/e3) beside
    it, a dashed line running from the e3 node to the button's frame."""
    s = SS
    d = ImageDraw.Draw(layer)
    window(d, 820, 110, 1135, 330)
    for i, w in enumerate((200, 150)):          # two fields, label stubs on the left
        y = 175 + i * 46
        d.rounded_rectangle([848 * s, (y + 8) * s, 900 * s, (y + 18) * s], 5 * s, fill=LINE)
        d.rounded_rectangle([915 * s, y * s, (915 + w) * s, (y + 28) * s], 7 * s,
                            fill=(0xF7, 0xF4, 0xFC), outline=LINE, width=2 * s)
    d.rounded_rectangle([935 * s, 272 * s, 1010 * s, 306 * s], 9 * s, fill=(0xF7, 0xF4, 0xFC),
                        outline=LINE, width=2 * s)
    d.rounded_rectangle([1025 * s, 272 * s, 1112 * s, 306 * s], 9 * s, fill=ACCENT)
    dashed_rect(d, (1016 * s, 263 * s, 1121 * s, 315 * s), ACCENT, 3 * s)

    mono = font(MONO, 25 * s)
    rows = [(0, "e1", "AXWindow"), (1, "e2", "AXGroup"), (2, "e3", "AXButton")]
    x0, y0, step = 830, 372, 50
    for i, (lvl, ref, role) in enumerate(rows):
        y = y0 + i * step
        x = x0 + lvl * 34
        if lvl:
            d.line([((x - 20) * s, (y - 28) * s), ((x - 20) * s, (y + 15) * s), ((x - 6) * s, (y + 15) * s)],
                   fill=LINE, width=3 * s)
        if ref == "e3":
            right = x + 48 + d.textbbox((0, 0), role, font=mono)[2] / s + 14
            d.rounded_rectangle([(x - 10) * s, (y - 6) * s, right * s, (y + 36) * s], 10 * s,
                                fill=TINT, outline=ACCENT, width=2 * s)
            top = y - 6
        d.text((x * s, y * s), ref, font=mono, fill=ACCENT)
        d.text(((x + 48) * s, y * s), role, font=mono, fill=DEEP if ref == "e3" else INK)
    # e3 → its frame on screen: up from the node's box to the button's dashed frame
    dashed(d, [(1068 * s, (top - 1) * s), (1068 * s, 333 * s)], ACCENT, 3 * s)
    d.polygon([(1068 * s, 317 * s), (1060 * s, 331 * s), (1076 * s, 331 * s)], fill=ACCENT)


def art_notes(layer):
    """The notes index: a small stack of note cards, the top one with a dated title."""
    s = SS
    d = ImageDraw.Draw(layer)
    for i, (dx, dy) in enumerate(((60, 0), (30, 40), (0, 80))):
        x1, y1 = 820 + dx, 120 + dy
        x2, y2 = x1 + 270, y1 + 330
        d.rounded_rectangle([x1 * s + 6, y1 * s + 10, x2 * s + 6, y2 * s + 10], 20 * s, fill=(0xE4, 0xDD, 0xF3))
        d.rounded_rectangle([x1 * s, y1 * s, x2 * s, y2 * s], 20 * s, fill=CARD, outline=LINE, width=2 * s)
        if i < 2:
            continue
        d.rounded_rectangle([(x1 + 28) * s, (y1 + 30) * s, (x1 + 120) * s, (y1 + 46) * s], 8 * s, fill=TINT)
        d.rounded_rectangle([(x1 + 28) * s, (y1 + 66) * s, (x1 + 230) * s, (y1 + 86) * s], 10 * s, fill=ACCENT)
        d.rounded_rectangle([(x1 + 28) * s, (y1 + 96) * s, (x1 + 180) * s, (y1 + 116) * s], 10 * s, fill=ACCENT)
        for j, w in enumerate((214, 190, 205, 150, 200, 120)):
            y = y1 + 146 + j * 26
            d.rounded_rectangle([(x1 + 28) * s, y * s, (x1 + 28 + w) * s, (y + 10) * s], 5 * s, fill=LINE)


def art_ui_action(layer):
    """ui_action: a window whose button is pressed by ref e3 (rings around it, a dashed line to
    the call), and a cursor below that stays put, with "(x, y) = (x, y)" beside it."""
    s = SS
    d = ImageDraw.Draw(layer)
    window(d, 820, 100, 1135, 320)
    for i, w in enumerate((210, 160)):           # two lines of text in the window
        y = 168 + i * 34
        d.rounded_rectangle([848 * s, y * s, (848 + w) * s, (y + 12) * s], 6 * s, fill=LINE)
    d.rounded_rectangle([930 * s, 258 * s, 1010 * s, 292 * s], 9 * s, fill=(0xF7, 0xF4, 0xFC),
                        outline=LINE, width=2 * s)
    bx1, by1, bx2, by2 = 1025, 258, 1112, 292     # the pressed button
    cx, cy = (bx1 + bx2) / 2, (by1 + by2) / 2
    for r, a in ((70, 70), (56, 120)):           # press rings
        d.ellipse([(cx - r) * s, (cy - r * 0.62) * s, (cx + r) * s, (cy + r * 0.62) * s],
                  outline=ACCENT + (a,), width=3 * s)
    d.rounded_rectangle([bx1 * s, by1 * s, bx2 * s, by2 * s], 9 * s, fill=DEEP)
    d.rounded_rectangle([(bx1 + 4) * s, (by1 + 4) * s, (bx2 - 4) * s, (by2 - 4) * s], 7 * s,
                        fill=ACCENT)

    mono = font(MONO, 25 * s)
    # the call, in a pill under the window, joined to the button by a dashed line
    px, py = 846, 368
    label = "ui_action e3 press"
    tw = d.textbbox((0, 0), label, font=mono)[2] / s
    d.rounded_rectangle([(px - 14) * s, (py - 10) * s, (px + tw + 14) * s, (py + 38) * s], 12 * s,
                        fill=TINT, outline=ACCENT, width=2 * s)
    d.text((px * s, py * s), "ui_action", font=mono, fill=INK)
    d.text(((px + d.textbbox((0, 0), "ui_action ", font=mono)[2] / s) * s, py * s), "e3 press",
           font=mono, fill=ACCENT)
    dashed(d, [(cx * s, (py - 10) * s), (cx * s, (by2 + 22) * s)], ACCENT, 3 * s)
    d.polygon([(cx * s, (by2 + 8) * s), ((cx - 8) * s, (by2 + 22) * s), ((cx + 8) * s, (by2 + 22) * s)],
              fill=ACCENT)

    # the cursor, untouched, and its reading before = after
    x, y = 852, 440
    pts = [(0, 0), (0, 44), (12, 32), (21, 52), (29, 48), (20, 29), (37, 29)]
    d.polygon([((x + a) * s, (y + b) * s) for a, b in pts], fill=INK, outline=CARD)
    d.text(((x + 60) * s, (y + 8) * s), "(x, y) = (x, y)", font=mono, fill=DEEP)


ARTS = {"ax-tree": art_ax_tree, "ui-action": art_ui_action, "notes": art_notes}


def build(lang, text=None, dest=None, art=None):
    """Draw one card. Defaults are the home page card; notes pass their own text, path and art."""
    im = gradient()
    im = im.convert("RGBA")
    if art:
        layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
        ARTS[art](layer)
        im.alpha_composite(layer.resize((W, H), Image.LANCZOS))
    else:
        mascot = Image.open(ART).convert("RGBA").resize((ART_PX, ART_PX), Image.LANCZOS)
        im.alpha_composite(mascot, (ART_X, (H - ART_PX) // 2))
    im = im.convert("RGB")

    d = ImageDraw.Draw(im)
    mark = Image.open(ICON).convert("RGBA").resize((ICON_PX, ICON_PX), Image.LANCZOS)
    im.paste(mark, ICON_XY, mark)
    wf = font(LATIN, 31, bold=True)
    wy = ICON_XY[1] + ICON_PX // 2 - d.textbbox((0, 0), WORDMARK, font=wf)[3] // 2 - 3
    d.text((ICON_XY[0] + ICON_PX + 18, wy), WORDMARK, font=wf, fill=INK)

    lines, sub = text or TEXT[lang]
    hpath = HEAD_FACE.get(lang, FACE[lang])
    hf, hsize = fit(d, lines, hpath, 58 if lang == "en" else 54, 34, TEXT_R)
    if len(lines) == 2:
        d.text((MARGIN, HEAD_Y1), lines[0], font=hf, fill=INK)
        d.text((MARGIN, HEAD_Y2 if hsize > 44 else HEAD_Y1 + hsize + 22), lines[1], font=hf, fill=INK)
    else:
        # A longer headline (3-4 lines): same leading ratio as the 2-line case (73/54), the block
        # ending where the 2-line block ends, so the subtitle and domain stay where they are.
        step = round(hsize * 1.32)
        top = HEAD_Y2 - (len(lines) - 1) * step
        for i, line in enumerate(lines):
            d.text((MARGIN, top + i * step), line, font=hf, fill=INK)

    sf_size = 27 if lang == "en" else 25
    sf = font(FACE[lang], sf_size)
    while MARGIN + width(d, sub, sf) > TEXT_R and sf_size > 17:
        sf_size -= 1
        sf = font(FACE[lang], sf_size)
    d.text((MARGIN, SUB_Y), sub, font=sf, fill=MUTED)
    d.text((MARGIN, DOMAIN_Y), DOMAIN, font=font(MONO, 26), fill=ACCENT)

    dest = dest or ROOT / f"og-{lang}.png"
    im.save(dest, optimize=True)
    over = [l for l in lines if MARGIN + width(d, l, hf) > TEXT_R]
    if MARGIN + width(d, sub, sf) > TEXT_R:
        over.append(sub)
    return dest, hsize, sf_size, "/".join(hf.getname()), over


def jobs():
    """Every card: the home page, the notes index, and each note, one per language."""
    from notes import INDEX, NOTES
    for lang in ("en", "zh", "ja", "ko"):
        lang_dir = ROOT / ("" if lang == "en" else lang)
        yield lang, None, None, None
        yield lang, INDEX[lang]["og"], lang_dir / "notes" / f"og-{lang}.png", "notes"
        for n in NOTES:
            yield (lang, n["langs"][lang]["og"], lang_dir / "notes" / n["slug"] / f"og-{lang}.png",
                   n["og_art"])


if __name__ == "__main__":
    for lang, text, path, art in jobs():
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
        dest, hs, ss, name, over = build(lang, text, path, art)
        im = Image.open(dest)
        print(f"  {lang:3} {str(dest.relative_to(ROOT)):40} {im.size[0]}x{im.size[1]} {im.mode:4} "
              f"head={hs}px sub={ss}px  {name}" + ("  OVERFLOW: %s" % over if over else ""))
