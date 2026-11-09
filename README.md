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

Run `og_cards.py` before `build.py` when the cards change, because the pages stamp
each asset with a content hash (`?v=…`). Links and asset paths are relative, so the
same files work at the Pages preview URL and at the custom domain. Absolute URLs
(canonical, hreflang, `og:image`) use `SITE`, default `https://openab.dev`.

Two files are hand-maintained and not generated: `CNAME` (the Pages custom domain,
`openab.dev`) and `discord/index.html`, which redirects https://openab.dev/discord to
the Discord invite. The apex DNS is not proxied through Cloudflare, so that page
replaces the old Cloudflare redirect rule.
