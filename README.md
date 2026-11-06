# openab-site

Source of the OpenAB ecosystem landing page (openab.dev), in English, Traditional
Chinese, Japanese and Korean. Static HTML/CSS served by GitHub Pages from `main` `/`.

Do not edit the HTML by hand. Every page is generated:

```sh
python3 scripts/make_icons.py [banner.jpg]  # logo-512, apple-touch-icon, favicon-64 from openab/images/banner.jpg
python3 scripts/og_cards.py   # og-{en,zh,ja,ko}.png sharing cards (1200×630, needs Pillow + macOS fonts)
python3 scripts/build.py      # index.html, zh/, ja/, ko/
```

Run `og_cards.py` before `build.py` when the cards change, because the pages stamp
each asset with a content hash (`?v=…`). Links and asset paths are relative, so the
same files work at the Pages preview URL and at the custom domain. Absolute URLs
(canonical, hreflang, `og:image`) use `SITE`, default `https://openab.dev`.

Two files are hand-maintained and not generated: `CNAME` (the Pages custom domain,
`openab.dev`) and `discord/index.html`, which redirects https://openab.dev/discord to
the Discord invite. The apex DNS is not proxied through Cloudflare, so that page
replaces the old Cloudflare redirect rule.
