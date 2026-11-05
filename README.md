# openab-site

Source of the OpenAB ecosystem landing page (openab.dev), in English, Traditional
Chinese, Japanese and Korean. Static HTML/CSS served by GitHub Pages from `main` `/`.

Do not edit the HTML by hand. Every page is generated:

```sh
python3 scripts/og_cards.py   # og-{en,zh,ja,ko}.png sharing cards (1200×630, needs Pillow + macOS fonts)
python3 scripts/build.py      # index.html, zh/, ja/, ko/
```

Run `og_cards.py` before `build.py` when the cards change, because the pages stamp
each asset with a content hash (`?v=…`). Links and asset paths are relative, so the
same files work at the Pages preview URL and at the custom domain. Absolute URLs
(canonical, hreflang, `og:image`) use `SITE`, default `https://openab.dev`.
