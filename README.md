# mima.social

The website for [Mima](https://mima.social), the calm, private app for all your
social networking, news, and conversations. It's a static site with no build
step.

| File | What it is |
|---|---|
| `index.html` | The landing page |
| `launch.css`, `launch.js` | Its styles and motion: wordmark draw-on, rotating headline, feature tour, timeline scroller, background squiggles |
| `app.js` | Newsletter signup (posts to Loops). The form is also a [WebMCP](https://webmachinelearning.github.io/webmcp/) tool, `subscribe_to_mima_updates` (declarative, with an imperative fallback), and replies to agents with the real result. |
| `llms.txt` | Plain-language summary of Mima for AI assistants and crawlers ([llmstxt.org](https://llmstxt.org)). Keep it in step with the page copy. |
| `netlify/functions/email-download.mjs` | `/api/email-download`: on phones and tablets, Download opens a sheet that emails the Mac link through Loops (see below) |
| `_redirects` | Netlify redirects: `/download` → the latest .dmg |
| `oauth/bluesky/client-metadata.json` | Bluesky OAuth client metadata for the desktop app. Must stay at this path on `www.mima.social`. |
| `site-assets/`, `assets/` | Fonts, logo, hero art, app screenshots, fake avatars and photos |
| `app-shots/` | Dummy app pages and the script that renders the app screenshots |
| `PRODUCT.md`, `DESIGN.md` | Product facts and copy rules; the page's design system |

Preview locally from the repo root:

```sh
python3 -m http.server 8765   # then open http://localhost:8765/
```

Add `#tour-compose` or `#tour-conversations` to the URL to open the feature tour
on that tab.

## App screenshots

Every picture of the Mima app on the page is an image rendered from **dummy
pages** that recreate the real app UI with fictional content. Real screenshots
would show real people. To regenerate them:

```sh
python3 app-shots/build.py   # write the dummy pages from the fake content
sh app-shots/render.sh       # render them with headless Chrome to site-assets/app/*.webp
```

You need Google Chrome and `cwebp` (`brew install webp`).

How it works:
- **Styles:** copied from `mima-social/desktop`.
- **Fake content:** names, `.example` handles, and generated avatars and photos.
- **Window sizes:** each view is rendered at a set size; there's a table in
  the app-shots README.
- **Phones:** separate narrow renders for phone screens.
- **On the page:** the composer zoom types real text over its screenshot, and
  the "Catch up" timeline scrolls behind its screenshot.

Full details are in [`app-shots/README.md`](app-shots/README.md). Keeping the
screenshots in sync with the app is tracked in mima-social/desktop#1396.

## Before launch

- The Download buttons (two links, marked `data-download`) point to
  `https://mima.social/download`, which `_redirects` sends (302) to the stable
  `Mima-latest-arm64.dmg` alias in R2. The desktop release pipeline keeps that
  alias current (mima-social/desktop#1406), so `_redirects` never changes per
  release. The alias 404s until that PR ships its first release.
- When the demo video exists, remove `hidden` from `section.demo-sec` in
  `index.html` and swap in the `<video>` markup from the comment there.

## Emailing the download link (phones and tablets)

On touch devices, Download opens a sheet instead of starting a .dmg download that
can't be used there. The Netlify function at `netlify/functions/email-download.mjs`
sends a Loops transactional email with the link. If the person ticks "Also send me
occasional Mima updates" (unticked by default), it also adds them to the mailing
list and records `optInSource` and `optInAt` on their contact as proof of consent.

It needs these Netlify environment variables:

| Variable | Where it comes from |
|---|---|
| `LOOPS_API_KEY` | Loops → Settings → API |
| `LOOPS_DOWNLOAD_EMAIL_ID` | The transactional email's id. It must use a `downloadUrl` data variable for the link. |
| `LOOPS_MAILING_LIST_ID` | Loops → Audience → Lists |
