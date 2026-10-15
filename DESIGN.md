---
name: Mima
description: The calm, private app for all your social networking, news, and conversations.
colors:
  a-50: "#f5f0f8"
  a-100: "#ecdcf5"
  a-200: "#dabfeb"
  a-300: "#c6a3e0"
  a-400: "#b188d2"
  a-600: "#8351b4"
  a-700: "#6b4394"
  a-800: "#543773"
  a-900: "#3d2952"
  a-950: "#22182e"
  bg: "#f8f4fa"
  bg-soft: "#fcfafd"
  card: "#ffffff"
  ink: "#0f0f0f"
  onyx: "#111111"
  void-100: "#f1f1f3"
  void-500: "#67677e"
  void-600: "#5b5b70"
  field-ink: "#1b1b1b"
  field-stroke: "rgba(31, 31, 31, 0.08)"
  pink-cta: "#e0004a"
  pink-deep: "#c80042"
  lime: "#e6f81a"
  lime-band: "#e9f57e"
  destructive: "#dc2626"
  bluesky: "#1185fe"
  linkedin: "#0a66c2"
  mastodon: "#6364ff"
typography:
  display:
    fontFamily: "MimaDisplay, Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(2.6rem, 5.6vw, 4.6rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "MimaDisplay, Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(2rem, 3.6vw, 3rem)"
    fontWeight: 800
    lineHeight: 1.08
    letterSpacing: "-0.015em"
  title:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.3
  subhead:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.125rem, 1.6vw, 1.3125rem)"
    fontWeight: 400
    lineHeight: 1.45
  lead:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.0625rem, 1.4vw, 1.25rem)"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
  small:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.4
  ai-voice:
    fontFamily: "MimaSerif, Georgia, Times New Roman, serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.3
  button:
    fontFamily: "MimaUI, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1
rounded:
  sm: "4px"
  icon: "14px"
  md: "16px"
  lg: "24px"
  pill: "999px"
spacing:
  gap-sm: "8px"
  gap-md: "16px"
  gap-lg: "24px"
  gutter: "clamp(20px, 4vw, 48px)"
  band: "clamp(48px, 6vw, 80px)"
  section: "clamp(64px, 9vw, 120px)"
  wrap: "1180px"
components:
  button-download:
    backgroundColor: "{colors.pink-cta}"
    textColor: "{colors.card}"
    rounded: "{rounded.pill}"
    padding: "14px 38px 14px 30px"
  button-download-hover:
    backgroundColor: "{colors.pink-deep}"
    textColor: "{colors.card}"
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.card}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 1.5rem"
    height: "3.375rem"
  input-email:
    backgroundColor: "{colors.void-100}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.md}"
    padding: "1rem 1.125rem"
    height: "3.375rem"
  button-retry:
    backgroundColor: "{colors.a-50}"
    textColor: "{colors.a-700}"
    rounded: "{rounded.pill}"
    padding: "9px 20px"
  feature-tab:
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "18px 20px"
  feature-tab-selected:
    backgroundColor: "{colors.a-100}"
  network-tile:
    textColor: "{colors.card}"
    rounded: "{rounded.md}"
    size: "clamp(52px, 4.6vw, 62px)"
  app-window:
    backgroundColor: "{colors.bg}"
    rounded: "{rounded.md}"
  privacy-icon:
    textColor: "{colors.lime}"
    rounded: "{rounded.icon}"
    size: "44px"
  ai-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "clamp(20px, 2.5vw, 28px)"
  ai-summary:
    backgroundColor: "{colors.a-50}"
    textColor: "{colors.a-950}"
    typography: "{typography.ai-voice}"
    rounded: "{rounded.md}"
    padding: "16px 18px"
---

# Design System: Mima

## Overview

**Creative North Star: "The Calm Window"**

Mima's site is a lilac-white room with one big window into the product. The Ube accent scale from the Mima style guide (binding brand source) carries every tint, link, ring and dark band. Two loud brand colours are held back for marketing moments: hot pink for the one action that matters, and lime for spark strokes and dark-ground accents. Everything else stays quiet so the product can do the talking. The page shows the app working, using real-UI rasters inside a rounded window, and does not describe it with feature cards.

Density is generous. Sections breathe on a 64–120px rhythm, copy sits in measured columns (36–40rem leads), and display type is near-black extra-bold grotesque with tight tracking. Depth comes from soft, purple-tinted ambient shadows under the product window and the CTA. There are no hard edges or offset shadows. Corners are round everywhere: 16px on product frames and tiles, 24px on tabs and the video, full pills on every button.

Motion is calm and finite. The wordmark draws on once, the headline's last word cycles once and settles, and the product window cross-fades between views, zooming into the composer to type a post. The only looping motion lives inside the product window and depicts the app: a slowly scrolling timeline and a typing caret, both pausable. All of it collapses under reduced motion, and the page reads fully without it.

**Key Characteristics:**
- Lilac-white ground (Ube 50 family) with grainy lime and hot-pink marketing fields at the hero edges only
- Near-black extra-bold display, calm UI sans for everything else
- One hot-pink pill per viewport; ink pills for secondary actions
- Product shown as raster screenshots in a soft-shadowed rounded window
- Network logos always in their true brand colours on rounded tiles
- Line icons from the Mima icon set (2px stroke, rounded caps), never glyphs or emoji
- AI-written text always in MimaSerif italic, labelled as AI

## Colors

The palette is a single purple accent scale on lilac neutrals, with hot pink and lime as rare marketing voltage.

### Primary
- **Ube Purple** (a-600): icon strokes, the headline spark, the active progress dot, feature icons. This is the brand accent at full strength.
- **Deep Ube** (a-700): link text, the focus ring colour, pause/retry text, the success check. It is the accessible text-weight purple. Links darken to **Ube Dusk** (a-800) on hover.
- **Ube Plum** (a-900): body copy on the Ube Lavender AI section, and the tint of every product shadow.
- **Ube Night** (a-950): the privacy band and the demo video ground. This is the only full-bleed dark purple surface. It is also the text colour of AI-written summaries.
- **Ube Mist / Lavender / Wisteria** (a-50, a-100, a-200): hero fallback ground, AI summary panel (a-50), the AI section ground and outcome hairlines (a-100), selected feature tab (a-100 at 85%), success check fill, inactive dots, text selection (a-200), body text on the dark band (a-100/a-200).
- **Ube Haze / Orchid** (a-300, a-400): scrollbar thumb, and the input hover/focus border.

### Secondary
- **Hot Pink CTA** (pink-cta): the Download pill and the video play disc only. It darkens to **Deep Pink** (pink-deep) on hover. The brand's display pink (#ff0054) appears only inside CTA hover glow and the painted background plate. It is never used as a text or surface colour.

### Tertiary
- **Ube Lime** (lime): spark strokes flanking the hero CTA, privacy icons on Ube Night (with a 12% lime tile), and the closing CTA band, which takes the colour full-bleed with ink type.

### Neutral
- **Lilac Ground** (bg): default page and product-window ground. **Lilac Soft** (bg-soft) separates the "how it helps" section.
- **Card White** (card): icon discs, button text, focus-ring gaps.
- **Ink** (ink): all display and body text, ink pill buttons, and the X tile. **Onyx** (onyx) is used only for the footer.
- **Void Slate** (void-600): secondary copy (subhead, ledes, descriptions, captions). **Void Muted** (void-500) is used for placeholder and the "or" divider. **Void Wash** (void-100) fills the input.
- **Field Ink and Field Stroke** (field-ink, field-stroke): the Mima style guide's input-field text and 1px border, taken verbatim. Used on form fields only; everywhere else text is Ink.
- **Network colours** (bluesky, linkedin, mastodon; X uses ink): tile fills only, in true brand colour.
- **Destructive** (destructive): form error text only.

### Named Rules
**The One Pink Rule.** Hot pink marks the download action, plus the play disc that stands in for the demo. No other element may be pink. If two pink things share a viewport, one is wrong.

**The Ube Scale Rule.** Every tint, ring, link and dark surface comes from the Ube a-50..a-950 scale in the Mima style guide. New purples are not invented. A theme swap redefines the scale, not the components.

**The Hairline Rule.** Stacked list items (outcomes, AI points) are separated by 1px horizontal hairlines in Ube: a-100 on light grounds, a-700 at 18% on the a-100 ground. No side stripes, no boxed rows.

**The True Colours Rule.** Third-party networks appear only in their own brand colours with white marks. They are never tinted to the palette.

## Typography

**Display Font:** MimaDisplay ExtraBold (with Avenir Next, Helvetica Neue fallback)
**Body Font:** MimaUI Regular and SemiBold (with Helvetica Neue, Helvetica, Arial)
**AI Voice Font:** MimaSerif Italic (with Georgia, Times New Roman), via `--font-ai`. Used only for AI-generated text.

**Character:** A heavy, tightly tracked grotesque shouts the promise once per section. A soft, legible UI sans does all the explaining at a calm 17px.

### Hierarchy
- **Display** (800, clamp 2.6–4.6rem, 1.02, -0.02em): the hero headline only, centred, two lines.
- **Headline** (800, clamp 2–3rem, 1.08, -0.015em): one per section, balanced wrap, left-aligned except the keep-up block.
- **Title** (600, 1.25rem, 1.3): feature tab names, outcome and success titles. Privacy and AI points use 1.1875rem.
- **Subhead** (400, clamp 1.125–1.3125rem, 1.45): the hero subhead only, max 36rem, balanced, in Void Slate.
- **Lead** (400, clamp 1.0625–1.25rem, 1.55): section ledes (max 40rem) in Void Slate, or a-200 on Ube Night.
- **Body** (400, 1.0625rem, 1.55): descriptions and footer (1rem/1.65, max 62ch).
- **Small** (400 or 600, 0.9375rem, 1.3–1.4): the Download sub-line, form error and retry text, message rows in the AI example card, and the footer byline.
- **AI voice** (MimaSerif Italic 400, 1.125rem, 1.5): AI-written summaries, in Ube Night on Ube Mist.
- **Label** (600, 0.875rem): network captions under tiles.
- **Button** (600, 1rem, 1): ink pills. The Download pill sets its title at 600 clamp(1.25rem, 1.8vw, 1.5rem) over a 0.9375rem sub-line.

### Named Rules
**The Two Weights Rule.** UI text uses only 400 and 600, and display uses only 800. No light, medium or bold-700 in between.

**The AI Voice Rule.** Text written by a model is set in MimaSerif italic and labelled as AI ("AI summary"). Nothing a person wrote uses the serif, and AI text never appears in the UI sans.

**The Sentence Case Rule.** Every heading, button and label is sentence case. No uppercase tracking labels, no eyebrows above headings.

## Layout

The page is a centred column with a max width of 1180px (wrap) and fluid gutters of 20–48px. Sections stack full-bleed with alternating grounds: lilac hero with a painted plate, then lilac-soft (how it helps), lilac (demo), Ube Night (privacy), Ube Lavender (AI), a lime band, lilac (keep up), and onyx footer. Vertical rhythm is section padding of clamp(64px, 9vw, 120px). The closing band is tighter, at clamp(48px, 6vw, 80px).

The hero is centred and symmetrical: logo top-left, headline, subhead, CTA flanked by sparks, then the network row. Below it, the showcase breaks out of the wrap by up to 80px per side as a two-column grid, with the tab list at 0.8fr and the window at 1.45fr. "How it helps" mirrors this with the window first at 1.25fr and outcomes at 1fr. Privacy points sit in two columns. The AI section is a 1.1fr/1fr grid with copy and hairline points left, the example card right.

Responsive behaviour:
- At ≤900px all grids become a single column, and the product window moves above the tabs.
- At ≤600px the window switches to a portrait 780×1040 phone render (max 420px), and the compose zoom, typing and scrolling timeline are dropped.
- At ≤560px sparks hide and the Download and ink pills go full width.

Internal gaps step through 8, 14–16 and 22–24px.

## Elevation & Depth

Depth is ambient and tinted, never structural. Surfaces are flat colour fields. Only a few kinds of object lift: the product frames (window and demo), the AI example card, the hot-pink CTA, and the network tiles. Every shadow is a long, soft, low-opacity blur. Product shadows are tinted with Ube 900 (rgba 61,41,82), and the CTA's glow is tinted with its own pink.

### Shadow Vocabulary
- **Window lift** (`box-shadow: 0 1px 0 rgba(17,17,17,.04), 0 30px 70px rgba(61,41,82,.22)`): product window, paired with a 1px rgba(17,17,17,.08) hairline. The demo frame uses the same blur at .25 without the hairline.
- **CTA glow** (`box-shadow: 0 10px 28px rgba(224,0,74,.28)`): Download pill. On hover it becomes `0 14px 32px rgba(255,0,84,.34)` with a 1px rise.
- **Card lift** (`box-shadow: 0 24px 60px rgba(61,41,82,.16)`): the white AI example card on Ube Lavender.
- **Control lift** (`box-shadow: 0 2px 10px rgba(61,41,82,.18)`): a round pause control floating over a product raster.
- **Tile lift** (`box-shadow: 0 6px 16px rgba(17,17,17,.12)`): network tiles.
- **Focus ring** (`box-shadow: 0 0 0 3px var(--ring)`): every focusable element. The Download pill uses a white 3px gap and then a 3px pink ring.

### Named Rules
**The Soft Lift Rule.** Shadows are blurred at least twice their offset and tinted to the palette. Hard or offset shadows do not exist in this world.

## Shapes

Everything is rounded, and the radius scales with size:
- 4px on link focus
- 14px on small icon tiles (privacy)
- 16px on product windows, network tiles, the email input and the AI summary panel
- 24px on feature tabs, the video frame and the AI example card
- Full pills on all buttons and the active progress-dot capsule, and circles on icon discs, avatars, the pause controls and the play disc

There are no square corners and no visible borders, except the window's hairline, the input's field stroke, the retry pill's Wisteria ring and the list hairlines. Brand squiggles (the looping M) are the only free-form shapes. They come from the style guide's squiggle set and are used as painted strokes crossing the hero edges.

## Components

### Buttons
- **Shape:** full pill (999px).
- **Download (primary):** hot-pink pill with a two-row grid: download icon, a 600 title, and a smaller "Free · for Apple Silicon Macs" line. It carries the CTA glow. On hover it turns deep pink, lifts 1px and the glow grows. On press it scales to 0.99. It is the only primary button, repeated once in the lime closing band.
- **Ink (secondary):** ink pill, 3.375rem tall, 600 1rem white label with an optional 20px trailing or leading icon. On hover it drops to 88% opacity, and it scales to 0.98 on press. Used for "Get updates" and "Join the Discord".
- **Retry (tertiary):** Ube Mist pill with a 1.5px Wisteria border and Deep Ube text.

### Inputs / Fields
- **Style:** the Mima style guide's input field: Void Wash fill, 1px Field Stroke border, Field Ink text at 600 1.0625rem, 16px radius, 3.375rem tall, Void Muted placeholder.
- **Focus:** the border shifts to Ube Orchid plus a 3px Deep Ube ring. Hover shifts the border only.
- **Error:** 600 0.9375rem destructive text below the field, announced live. Disabled submit sits at 50% opacity.

### Feature Tabs (signature)
A vertical tablist next to the product window. Each tab has a 52px white icon disc with an Ube Purple line icon, a Title-weight name and a Void Slate description, inside a 24px-radius row. Hover uses a 55% white wash. The selected tab uses an 85% Ube Lavender wash. Below the list sit a white round pause toggle and progress dots (10px Wisteria circles; the active dot stretches to a 26px Ube Purple capsule). The window auto-advances every 6s, pauses on hover or focus, and follows arrow keys.

### App Window (signature)
A 16px-radius frame on lilac ground with the window-lift shadow and hairline, at an 800/540 aspect ratio. It shows product rasters that cross-fade over 0.5s. Views can act out the feature they show:
- **Feed:** the News Wall board raster.
- **Compose:** the raster zooms 1.65× from its bottom-left corner over 0.9s, the upper part fades to the app ground, and a post types itself over the composer (55ms per character) behind an Ube Purple caret.
- **Catch up:** in "How it helps", a timeline strip scrolls behind the window chrome on a 160s linear loop. It pauses on hover, focus or its round pause control (which carries the control lift), and stays still under reduced motion.

Values inside the window (the typing overlay's Source Sans 3, the #f8f8f8 app ground) belong to the depicted app, not to the site system. The rasters come from `app-shots/`: hand-recreated Mima app pages (real Ube app styles from the desktop repo, fictional people and posts) built by `build.py` and rendered by `render.sh` to `site-assets/app/*.webp`, at 2x 800×540 plus a 780×1040 phone variant, each with a provenance `.json`. Those dummy pages document the app's look. They are not part of this site's system.

### Network Tiles
52–62px squares with a 16px radius, filled in the network's true colour, with a white mark at 64% and the tile-lift shadow. The name sits beneath as a Label caption in Void Slate.

### Privacy Points
On Ube Night: a 44px, 14px-radius tile at 12% lime holding a lime line icon, a white Title and an a-200 description.

### AI Example Card
A white 24px-radius card with the card-lift shadow, set on the Ube Lavender AI section. It shows a short thread (40px round avatars, Small names at 600 and messages in Void Slate, a "+ N more replies" line in Void Muted), then the AI summary panel: Ube Mist ground, 16px radius, a Deep Ube 600 0.75rem sentence-case label ("AI summary · on this Mac") over the summary in the AI voice. A Void Muted caption marks it as illustrative.

### Navigation
There is no nav bar. The animated Mima wordmark sits top-left as the home link: the M strokes on over 350ms (cubic-bezier(0.45, 0, 0.55, 1)), then "ima" fades in over 150ms.

## Do's and Don'ts

### Do:
- **Do** take every purple from the Ube a-50..a-950 scale, and use a-700 for any purple text or ring.
- **Do** keep hot pink to the single download action (and the demo play disc).
- **Do** show the product as real-UI rasters in the rounded, soft-shadowed app window, regenerated through `app-shots/` with fictional content.
- **Do** use lime as strokes, icon colour on Ube Night, or a full-bleed band with ink type, and never as text on light grounds.
- **Do** use Mima icon-set line icons (2px stroke, round caps) inline as SVG.
- **Do** set AI-generated text in MimaSerif italic (the AI voice) and label it "AI summary".
- **Do** separate stacked list items with 1px Ube hairlines.
- **Do** ease state changes with cubic-bezier(0.16, 1, 0.3, 1) at 0.2–0.5s, and honour reduced motion.

### Don't:
- **Don't** use hard, offset or untinted heavy shadows. Lift is soft and palette-tinted.
- **Don't** tint network logos to the palette or show them in monochrome tiles (X excepted, which is ink by its own brand).
- **Don't** add uppercase eyebrows or kickers above headings, and don't use emoji or glyph icons.
- **Don't** use square corners on buttons, tiles or frames.
- **Don't** loop decorative motion. Animations play once; repeating motion is allowed only inside the product window, depicting the app, pausable, and stopped under reduced motion.
- **Don't** separate list items or flag content with coloured side stripes.
