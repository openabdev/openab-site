# openab-site

Source of the OpenAB community landing page (openab.dev), in English, Traditional
Chinese, Japanese and Korean. Static HTML/CSS served by GitHub Pages from `main` `/`.

Do not edit the HTML by hand. Every page is generated:

```sh
python3 scripts/make_icons.py [SRC_DIR]   # icons, hero, card stickers from the mascot sources (not committed)
python3 scripts/og_cards.py   # og-{en,zh,ja,ko}.png and the notes cards (1200×630, needs Pillow + macOS fonts)
python3 scripts/build.py      # index.html, zh/, ja/, ko/ and the notes/ pages
```

Dev notes live in `scripts/notes.py` (copy for all four languages, newest first). Each
language gets its own index (`notes/`, `zh/notes/`, `ja/notes/`, `ko/notes/`) and its own
page per note (`notes/<slug>/`, `zh/notes/<slug>/`, …), each with its own sharing card
next to it (`og-<lang>.png`).

Sharing-card rule for dev notes: the mascot is already in the top-left corner, so the right
side of a note card carries an illustration of the note's topic, never the mascot again. Set
`og_art` on the note in `notes.py` to one of the drawings in `og_cards.ARTS` (add a new one for
a new topic). Text inside an illustration stays generic (role names, refs, no real names), and
the card must stay readable at a 600×315 thumbnail.

Notes can embed animated diagrams from `scripts/figures.py` (`{fig_…}` in a body; every
visible word is localized there). `scripts/figs.js` is inlined into those pages; without JS or
the diagrams autoplay when they scroll into view and loop (pausing off-screen), with a small
Pause/Play toggle; with `prefers-reduced-motion` they show their complete static state and do not
autoplay. `?fig-step=N` freezes every diagram at step N for screenshots.

Run `og_cards.py` before `build.py` when the cards change, because the pages stamp
each asset with a content hash (`?v=…`). Links and asset paths are relative, so the
same files work at the Pages preview URL and at the custom domain. Absolute URLs
(canonical, hreflang, `og:image`) use `SITE`, default `https://openab.dev`.

Two files are hand-maintained and not generated: `CNAME` (the Pages custom domain,
`openab.dev`) and `discord/index.html`, which redirects https://openab.dev/discord to
the Discord invite. The apex DNS is not proxied through Cloudflare, so that page
replaces the old Cloudflare redirect rule.
