# App screenshots

The landing page shows the Mima app through images, not live HTML. They are
rendered from the dummy pages in this folder, which recreate the real app UI
filled with fake people and posts.

```sh
python3 app-shots/build.py   # regenerate feed/board/compose/conversations/thread.html
sh app-shots/render.sh       # render site-assets/app/<view>.webp (2x, 800x540 CSS px)
```

`render.sh` needs Google Chrome and `cwebp` (`brew install webp`). Preview a
page with any static server from the repo root (`python3 -m http.server`) at
`/app-shots/feed.html`.

## What's here

- `app.css`: the app's styles, copied from `mima-social/desktop` (`next`):
  `src/styles/globals.css` tokens (Ube theme, light mode) and the NewsWall,
  Conversations and Omnibox components.
- `icons.svg`: the app's icon set (`src/assets/icons/*.svg`) and the solid
  platform marks from `src/components/common/PlatformIcon.tsx`.
- `fonts/`: Gen Interface JP and Source Sans 3, as shipped in the app.
- `build.py`: the fake content and the page markup. All names, handles, posts
  and avatars are fictional; avatars are generated images in `assets/avatars/`.

## Keeping it in sync

These pages copy the app's UI by hand, so they drift whenever the app's
design changes. After a UI change in the desktop app, update `app.css` /
`build.py` to match and re-render. The longer-term fix is to render the app's
own components with fixture data in the desktop repo: mima-social/desktop#1396.
