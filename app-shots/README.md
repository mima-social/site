# App screenshots

The landing page shows the Mima app through **images**, not live HTML. Real
screenshots can't be used: they contain real people's names, faces and posts.
So this folder holds **dummy pages** that recreate the real app UI, filled with
fictional people and posts, and a script that renders them to WebP images in
`site-assets/app/`.

## Quick start

```sh
python3 app-shots/build.py   # write the dummy pages (app-shots/*.html)
sh app-shots/render.sh       # render them to site-assets/app/*.webp
```

`render.sh` needs Google Chrome (headless) and `cwebp` (`brew install webp`).
It starts a temporary static server on port 8799 (override with `PORT=`), so
run it from anywhere; it works from the repo root.

To look at a dummy page in a browser, serve the repo root
(`python3 -m http.server`) and open, for example, `/app-shots/board.html`.

## How it works

1. **Styles copied from the app.** `app.css` reproduces the Mima desktop app's
   UI from `mima-social/desktop` on the `next` branch:
   - tokens from `src/styles/globals.css` (Ube theme, light mode: colours,
     type scale, radii, shadows);
   - the News Wall (`NewsWall.tsx`, `PostCard.tsx`, `BentoGrid.tsx`),
     Conversations (`ConversationListItem.tsx`, `ConversationModal.tsx`),
     composer (`Omnibox/Composer.tsx`, `PlatformSelector.tsx`) and AI summary
     (`ConversationSummaryOverlay.tsx`, `SummaryWithReferences.tsx`,
     `ui/AiSparkle.tsx`) components, matched value by value.

   Copied as-is from the app repo:
   - `fonts/`: Gen Interface JP (UI), Source Sans 3 (what people wrote) and
     Source Serif 4 italic (AI text).
   - `icons.svg`: the app's icon set (`src/assets/icons/*.svg`) plus the solid
     platform marks from `src/components/common/PlatformIcon.tsx`.

2. **Fake content in one place.** `build.py` holds every person, post and
   conversation, and writes the pages:

   | Page | Shows | Used for |
   |---|---|---|
   | `board.html` | News Wall, Board view, 4 columns | Hero tour: "One feed for your people" |
   | `compose.html` | The same board, empty composer, all four networks selected | Hero tour: "Compose once" (the site types into it) |
   | `compose-typed.html` | The same, with the message typed in | Phone version of the compose tab |
   | `conversations.html` | Conversations list: pinned, unread, reminder, group | Hero tour: "Every conversation" |
   | `feed.html` | News Wall, Timeline view | Frame for the "Catch up" scroller |
   | `timeline-strip.html` | A tall strip of timeline posts, no chrome | Scrolls inside the "Catch up" frame |
   | `summary.html` | A conversation with the catch-up AI summary | Phone/backup view |
   | `summary-card.html` | Just that conversation dialog, close up | AI section |
   | `thread.html` | An open DM thread | Spare view |
   | `phone.html` | Loads any page in a 390px frame | Phone renders (see below) |

   People and media are fictional:
   - handles use reserved `.example` domains or `_demo` suffixes so none can
     belong to a real account;
   - avatars (`assets/avatars/a0–a7.png`) and post photos
     (`assets/posts/*.webp`) are AI-generated, each with its generation prompt
     embedded or in a `.json` sidecar.

3. **Rendering.** `render.sh` loads each page in headless Chrome at 2× pixel
   density and converts it to WebP:

   | Output | Window (CSS px) | Notes |
   |---|---|---|
   | `board`, `compose`, `conversations`, `feed` | 960 × 648 | Shared size, so the app chrome matches across shots |
   | `thread` | 800 × 540 | |
   | `summary` | 800 × 660 | |
   | `summary-card` | 720 × 542 | Close-up for the AI section |
   | `timeline-strip` | 960 × 3400 | Tall, so it can scroll |
   | `<view>-m` (phones) | 390 × 520, via `phone.html` | The narrow layout in `app.css` (`max-width: 520px`) reflows the UI, then the result is cropped to 780 × 1040 |

   Headless Chrome won't make a window narrower than ~500px, which is why the
   phone frames go through `phone.html` (a 390px iframe).

## How the site uses the images

- **Hero tour** (`index.html` `#shot`, `launch.js`): the three tabs crossfade
  between `board`, `compose` and `conversations`.
  - The compose tab zooms 2× into the composer of `compose.webp`. The typed
    message is real HTML over the image (`.typing`), positioned in container
    units so it lines up at any size.
  - Change the composer's position or the render size and you must re-aim
    `.typing` (`left`, `bottom`, `font-size`) in `launch.css`.
- **Catch up** (`.scroller`): `feed.webp` is the static frame. `timeline-strip`
  scrolls behind a window cut over the feed area: `top` and `height` in
  `launch.css`, with the loop distance set by `@keyframes timeline`, which
  equals the strip's height ÷ width × 100cqw.
- **AI section**: `summary-card.webp`.
- **Phones** (≤ 600px): every `<picture>` swaps to the `-m` image; the zoom,
  typing and scroller are off.

## Social share image

`og.html` is the source for `site-assets/og-image.jpg` (the link-preview card,
2400 × 1260). It reuses the board screenshot, so re-render it after the app
shots change:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --force-device-scale-factor=2 --virtual-time-budget=4000 --window-size=1200,630 \
  --screenshot=site-assets/og.png http://localhost:8765/app-shots/og.html
sips -s format jpeg -s formatOptions 88 site-assets/og.png --out site-assets/og-image.jpg && rm site-assets/og.png
```

## Changing things

- **Different fake content:** edit `build.py`, then run both commands.
- **The app's UI changed:** update `app.css` (and the markup helpers in
  `build.py`) to match `mima-social/desktop@next`, then re-render. Check the
  hero tour, the "Catch up" scroller and the AI section afterwards; overlay
  positions depend on the layout.
- **New fake photo or avatar:** generate it, save it under `assets/`, and keep
  its prompt with it (embedded, or as a `.json` sidecar), so every image's
  origin is on record.

These pages copy the app by hand, so they drift when the app's design changes.
The longer-term fix, rendering the app's own components with fixture data in
the desktop repo, is mima-social/desktop#1396.
