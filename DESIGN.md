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
  page-title:
    fontFamily: "MimaDisplay, Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(2.5rem, 5vw, 4rem)"
    fontWeight: 800
    lineHeight: 1.04
    letterSpacing: "-0.02em"
  section-heading:
    fontFamily: "MimaDisplay, Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.625rem, 2.6vw, 2rem)"
    fontWeight: 800
    lineHeight: 1.12
    letterSpacing: "-0.015em"
  code:
    fontFamily: "ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.6
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
  measure: "68ch"
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
  button-download-small:
    backgroundColor: "{colors.pink-cta}"
    textColor: "{colors.card}"
    rounded: "{rounded.pill}"
    padding: "11px 20px 11px 16px"
  button-download-calm:
    backgroundColor: "{colors.a-950}"
    textColor: "{colors.card}"
    rounded: "{rounded.pill}"
    padding: "14px 34px 14px 26px"
  button-download-calm-hover:
    backgroundColor: "{colors.a-900}"
    textColor: "{colors.card}"
  button-ink-compact:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.card}"
    rounded: "{rounded.pill}"
    padding: "0 1.25rem"
    height: "3rem"
  nav-pill:
    textColor: "{colors.void-600}"
    rounded: "{rounded.pill}"
    padding: "8px 14px"
  nav-pill-current:
    backgroundColor: "{colors.a-100}"
    textColor: "{colors.a-700}"
  topic-pill:
    backgroundColor: "{colors.card}"
    textColor: "{colors.a-700}"
    rounded: "{rounded.pill}"
    padding: "9px 16px"
  topic-pill-current:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.card}"
  shelf:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "24px 26px 20px"
  fact-sheet:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "6px 22px"
  toc-link-current:
    backgroundColor: "{colors.a-100}"
    textColor: "{colors.a-700}"
    rounded: "{rounded.md}"
    padding: "7px 12px"
  callout:
    backgroundColor: "{colors.a-50}"
    textColor: "{colors.a-950}"
    rounded: "{rounded.md}"
    padding: "16px 20px"
  code-block:
    backgroundColor: "{colors.a-950}"
    textColor: "{colors.a-100}"
    typography: "{typography.code}"
    rounded: "{rounded.md}"
    padding: "18px 22px"
  code-inline:
    backgroundColor: "{colors.a-50}"
    textColor: "{colors.a-900}"
    rounded: "{rounded.sm}"
  table-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
  try-card:
    backgroundColor: "{colors.a-950}"
    textColor: "{colors.a-100}"
    rounded: "{rounded.lg}"
    padding: "clamp(24px, 3.5vw, 40px)"
  mini-try:
    backgroundColor: "{colors.a-100}"
    textColor: "{colors.a-900}"
    rounded: "{rounded.lg}"
    padding: "22px"
---

# Design System: Mima

## Overview

**Creative North Star: "The Calm Window"**

Mima's site is a lilac-white room with one big window into the product. The Ube accent scale from the Mima style guide (binding brand source) carries every tint, link, ring and dark band. Two loud brand colours are held back for marketing moments: hot pink for the one action that matters, and lime for spark strokes and dark-ground accents. Everything else stays quiet so the product can do the talking. The page shows the app working, using real-UI rasters inside a rounded window, and does not describe it with feature cards.

Density is generous. Sections breathe on a 64–120px rhythm, copy sits in measured columns (36–40rem leads), and display type is near-black extra-bold grotesque with tight tracking. Depth comes from soft, purple-tinted ambient shadows under the product window and the CTA. There are no hard edges or offset shadows. Corners are round everywhere: 16px on product frames and tiles, 24px on tabs and the video, full pills on every button.

Motion is calm and finite. The wordmark draws on once, the headline's last word cycles once and settles, and the product window cross-fades between views, zooming into the composer to type a post. The only looping motion lives inside the product window and depicts the app: a slowly scrolling timeline and a typing caret, both pausable. All of it collapses under reduced motion, and the page reads fully without it.

Learn (/learn/), the knowledge base, carries the same room into reading. It is a field guide rather than a blog river: topics stand side by side as white 24px shelves, articles read in a 68ch column with a sticky margin holding a fact sheet and an "On this page" list that follows the reader, and every article closes on a "Try it in Mima" card that shows the product. It reuses the lime closing band and onyx footer from the landing page, and adds a compact top bar, Ube Night code blocks and Ube Mist callouts.

**Key Characteristics:**
- Lilac-white ground (Ube 50 family) with grainy lime and hot-pink marketing fields at the hero edges only
- Near-black extra-bold display, calm UI sans for everything else
- One hot-pink pill per viewport; ink pills for secondary actions
- Product shown as raster screenshots in a soft-shadowed rounded window
- Network logos always in their true brand colours on rounded tiles
- Line icons from the Mima icon set (2px stroke, rounded caps), never glyphs or emoji
- AI-written text always in MimaSerif italic, labelled as AI
- Reading surfaces (Learn) use white 24px cards on lilac and Ube hairline entry rows, never thumbnail card grids

## Colors

The palette is a single purple accent scale on lilac neutrals, with hot pink and lime as rare marketing voltage.

### Primary
- **Ube Purple** (a-600): icon strokes, the headline spark, the active progress dot, feature icons. This is the brand accent at full strength.
- **Deep Ube** (a-700): link text, the focus ring colour, pause/retry text, the success check. It is the accessible text-weight purple. Links darken to **Ube Dusk** (a-800) on hover.
- **Ube Plum** (a-900): body copy on the Ube Lavender AI section, and the tint of every product shadow.
- **Ube Night** (a-950): the privacy band and the demo video ground. This is the only full-bleed dark purple surface. It is also the text colour of AI-written summaries. On Learn it also fills contained surfaces: the "Try it in Mima" card, prose code blocks, and the closing band's Download pill (darkening to Ube Plum on hover).
- **Ube Mist / Lavender / Wisteria** (a-50, a-100, a-200): hero fallback ground, AI summary panel (a-50), the AI section ground and outcome hairlines (a-100), selected feature tab (a-100 at 85%), success check fill, inactive dots, text selection (a-200), body text on the dark band (a-100/a-200). On Learn: callouts and inline code (a-50), entry and fact-sheet hairlines, the current nav pill and current "On this page" item, the shelf icon tile and the topic-page Mima note (a-100).
- **Ube Haze / Orchid** (a-300, a-400): scrollbar thumb, and the input hover/focus border.

### Secondary
- **Hot Pink CTA** (pink-cta): the Download pill (including the small Download pill in the Learn bar) and the video play disc only. It darkens to **Deep Pink** (pink-deep) on hover. The brand's display pink (#ff0054) appears only inside CTA hover glow and the painted background plate. It is never used as a text or surface colour.

### Tertiary
- **Ube Lime** (lime): spark strokes flanking the hero CTA, privacy icons on Ube Night (with a 12% lime tile), and the closing CTA band, which takes the colour full-bleed with ink type (the band itself is the softer lime-band value). Learn reuses the same band.

### Neutral
- **Lilac Ground** (bg): default page and product-window ground. **Lilac Soft** (bg-soft) separates the "how it helps" section.
- **Card White** (card): icon discs, button text, focus-ring gaps.
- **Ink** (ink): all display and body text, ink pill buttons, and the X tile. **Onyx** (onyx) is used only for the footer.
- **Void Slate** (void-600): secondary copy (subhead, ledes, descriptions, captions). **Void Muted** (void-500) is used for placeholder and the "or" divider. **Void Wash** (void-100) fills the input.
- **Field Ink and Field Stroke** (field-ink, field-stroke): the Mima style guide's input-field text and 1px border, taken verbatim. Used on form fields only; everywhere else text is Ink.
- **Network colours** (bluesky, linkedin, mastodon; X uses ink): tile fills only, in true brand colour.
- **Destructive** (destructive): form error text only.

### Named Rules
**The One Pink Rule.** Hot pink marks the download action, plus the play disc that stands in for the demo. No other element may be pink. If two pink things share a viewport, one is wrong. On Learn the bar's small Download pill is the page's pink, so further Download actions step down: the closing band's Download pill is Ube Night and the topic page's margin uses an ink pill. The one exception is the article's "Try it in Mima" card, whose full Download pill is pink because it sits at the end of the article, a scroll away from the bar.

**The Ube Scale Rule.** Every tint, ring, link and dark surface comes from the Ube a-50..a-950 scale in the Mima style guide. New purples are not invented. A theme swap redefines the scale, not the components.

**The Hairline Rule.** Stacked list items (outcomes, AI points, Learn entries, shelf links, fact-sheet rows, table rows) are separated by 1px horizontal hairlines in Ube: a-100 on light grounds, a-700 at 18% on the a-100 ground. No side stripes, no boxed rows.

**The True Colours Rule.** Third-party networks appear only in their own brand colours with white marks. They are never tinted to the palette.

## Typography

**Display Font:** MimaDisplay ExtraBold (with Avenir Next, Helvetica Neue fallback)
**Body Font:** MimaUI Regular and SemiBold (with Helvetica Neue, Helvetica, Arial)
**AI Voice Font:** MimaSerif Italic (with Georgia, Times New Roman), via `--font-ai`. Used only for AI-generated text.
**Code Font:** the system monospace stack (ui-monospace, SF Mono, Menlo, Consolas), via `--font-code`. Used only for code: inline code and code blocks in Learn articles.

**Character:** A heavy, tightly tracked grotesque shouts the promise once per section. A soft, legible UI sans does all the explaining at a calm 17px.

### Hierarchy
- **Display** (800, clamp 2.6–4.6rem, 1.02, -0.02em): the hero headline, centred, two lines; and the Learn index headline, left-aligned.
- **Page title** (800, clamp 2.5–4rem, 1.04, -0.02em): Learn article and topic page titles, below the breadcrumb.
- **Headline** (800, clamp 2–3rem, 1.08, -0.015em): one per section, balanced wrap, left-aligned except the keep-up block.
- **Section heading** (800, clamp 1.625–2rem, 1.12, -0.015em): article prose h2 and the "Try it in Mima" heading. Shelf names use the display face at 1.5rem/1.1, and topic-page entry titles at 1.375rem/1.15.
- **Title** (600, 1.25rem, 1.3): feature tab names, outcome and success titles, article h3, and Learn card headings ("Latest", "Related guides"). Privacy and AI points use 1.1875rem. Learn entry titles are 600 at 1.0625rem/1.35, shelf links 600 at 1rem.
- **Subhead** (400, clamp 1.125–1.3125rem, 1.45): the hero subhead only, max 36rem, balanced, in Void Slate.
- **Lead** (400, clamp 1.0625–1.25rem, 1.55): section ledes (max 40rem) in Void Slate, or a-200 on Ube Night.
- **Body** (400, 1.0625rem, 1.55): descriptions and footer (1rem/1.65, max 62ch).
- **Small** (400 or 600, 0.9375rem, 1.3–1.4): the Download sub-line, form error and retry text, message rows in the AI example card, and the footer byline.
- **Answer** (400, the Subhead size at 1.5): the article's "In short" lead, in Ink with a Deep Ube 600 "In short:" run-in, max 44rem.
- **AI voice** (MimaSerif Italic 400, 1.125rem, 1.5): AI-written summaries, in Ube Night on Ube Mist.
- **Label** (600, 0.875rem): network captions under tiles.
- **Button** (600, 1rem, 1): ink pills. The Download pill sets its title at 600 clamp(1.25rem, 1.8vw, 1.5rem) over a 0.9375rem sub-line.
- **Code** (system mono, 0.9375rem/1.6 in blocks; 0.875em inline): code only.

### Named Rules
**The Two Weights Rule.** UI text uses only 400 and 600, and display uses only 800. No light, medium or bold-700 in between.

**The Code Only Rule.** The monospace stack appears only on code. Labels, dates, counts and meta stay in the UI sans (with tabular numerals where figures align).

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

### Learn
Learn pages share the 1180px wrap and gutters, under a compact bar (20px block padding) and above the lime band and onyx footer.
- **Index:** a 1.15fr/1fr intro grid with the headline and lede left and the white Latest card right, then topic shelves in an auto-fill grid (columns at least 300px, 20px gaps). Shelves are capped and overflow to their topic page.
- **Article:** a two-column grid, with the reading column at the 68ch measure and a margin of at least 220px, 40–96px apart. The title block spans both (max 52rem). The margin is sticky at 24px from the top and holds the fact sheet and "On this page". The Try card and the related lists follow the prose in the reading column.
- **Topic:** the same two-column grid, with the entry list (max 52rem) left and a margin holding the topic pills and the Mima note.
- Pages open at clamp(24px, 4vw, 48px) and close at clamp(64px, 9vw, 112px). Prose flows at 1.1em between blocks, 2.2em above h2 and 1.8em above h3.
- At ≤960px Learn grids collapse to one column, the article margin moves above the prose and stops being sticky, and "On this page" is hidden. At ≤560px the bar drops its Home link and the "for Mac" words, and full Download pills go full width.

## Elevation & Depth

Depth is ambient and tinted, never structural. Surfaces are flat colour fields. Only a few kinds of object lift: the product frames (window and demo), the AI example card, the hot-pink CTA, and the network tiles. Every shadow is a long, soft, low-opacity blur. Product shadows are tinted with Ube 900 (rgba 61,41,82), and the CTA's glow is tinted with its own pink.

### Shadow Vocabulary
- **Window lift** (`box-shadow: 0 1px 0 rgba(17,17,17,.04), 0 30px 70px rgba(61,41,82,.22)`): product window, paired with a 1px rgba(17,17,17,.08) hairline. The demo frame uses the same blur at .25 without the hairline.
- **CTA glow** (`box-shadow: 0 10px 28px rgba(224,0,74,.28)`): Download pill. On hover it becomes `0 14px 32px rgba(255,0,84,.34)` with a 1px rise.
- **Card lift** (`box-shadow: 0 24px 60px rgba(61,41,82,.16)`): the white AI example card on Ube Lavender.
- **Control lift** (`box-shadow: 0 2px 10px rgba(61,41,82,.18)`): a round pause control floating over a product raster.
- **Tile lift** (`box-shadow: 0 6px 16px rgba(17,17,17,.12)`): network tiles.
- **Sheet lift** (`box-shadow: 0 24px 60px rgba(61,41,82,.12)`): Learn's white reading cards (Latest, fact sheet, topic entry list).
- **Shelf lift** (`box-shadow: 0 1px 0 rgba(17,17,17,.03), 0 18px 44px rgba(61,41,82,.08)`): topic shelves, quieter because they repeat in a grid. The table card uses the same pair at 0 12px 32px.
- **Small CTA glow** (`box-shadow: 0 8px 20px rgba(224,0,74,.22)`): the bar's small Download pill. The Ube Night band pill carries the same glow shape tinted with Ube Night (rgba 34,24,46,.22). On the Ube Night Try card the pink pill drops its glow, and the product raster lifts on `0 30px 70px rgba(17,17,17,.35)`.
- **Focus ring** (`box-shadow: 0 0 0 3px var(--ring)`): every focusable element. The Download pill uses a white 3px gap and then a 3px pink ring (on the Try card the gap is Ube Night; on the Ube Night band pill the ring is Deep Ube).

### Named Rules
**The Soft Lift Rule.** Shadows are blurred at least twice their offset and tinted to the palette. Hard or offset shadows do not exist in this world.

## Shapes

Everything is rounded, and the radius scales with size:
- 4px on link focus and inline code
- 14px on small icon tiles (privacy)
- 16px on product windows, network tiles, the email input, the AI summary panel, and on Learn the code blocks, callouts, table card, prose images and the current "On this page" highlight
- 24px on feature tabs, the video frame, the AI example card, and Learn's shelves, Latest card, fact sheet, entry list, Try card and Mima note
- The Try card's product raster is rounded 16px on its top corners only and is cropped by the card's bottom edge
- Full pills on all buttons and the active progress-dot capsule, and circles on icon discs, avatars, the pause controls and the play disc

There are no square corners and no visible borders, except the window's hairline, the input's field stroke, the retry pill's Wisteria ring and the list hairlines (including Learn's entry, table and fact-sheet rows). Brand squiggles (the looping M) are the only free-form shapes. They come from the style guide's squiggle set and are used as painted strokes crossing the hero edges.

## Components

### Buttons
- **Shape:** full pill (999px).
- **Download (primary):** hot-pink pill with a two-row grid: download icon, a 600 title, and a smaller "Free · for Apple Silicon Macs" line. It carries the CTA glow. On hover it turns deep pink, lifts 1px and the glow grows. On press it scales to 0.99. It is the only primary button, repeated once in the lime closing band.
- **Ink (secondary):** ink pill, 3.375rem tall, 600 1rem white label with an optional 20px trailing or leading icon. On hover it drops to 88% opacity, and it scales to 0.98 on press. Used for "Get updates" and "Join the Discord".
- **Retry (tertiary):** Ube Mist pill with a 1.5px Wisteria border and Deep Ube text.
- **Small Download (Learn bar):** a hot-pink pill at 600 0.9375rem with an 18px download icon and the small CTA glow; it rises 1px and deepens on hover. Below 560px it reads "Download".
- **Calm Download (Learn band):** the full two-row Download pill in Ube Night with a Ube Night glow, darkening to Ube Plum. It is used where the bar's pink pill already holds the page's pink.
- **Compact ink:** the ink pill at 3rem tall with an 18px icon, 600 0.9375rem. It is the Download in the topic page margin.

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
The landing page has no nav bar. The animated Mima wordmark sits top-left as the home link: the M strokes on over 350ms (cubic-bezier(0.45, 0, 0.55, 1)), then "ima" fades in over 150ms.

Learn has a compact bar: the wordmark (96–124px) left, then Home and Learn as nav pills (600 0.9375rem in Void Slate; hover is a 70% white wash, the current section is Deep Ube on Ube Lavender), and the small pink Download pill pushed right. Article and topic pages put a breadcrumb under the bar: 600 0.9375rem Deep Ube links separated by Ube Haze slashes.

### Learn Entries and Lists
An entry row is a title (600 1.0625rem, Ink, Deep Ube and underlined on hover), an optional one-line summary in Void Slate at 0.9375rem, and a meta line (date · topic) in Void Muted at 0.875rem with tabular numerals. Rows are separated by Ube Lavender hairlines, with no border above the first. The **Latest** list sets five such rows (no summaries) in a white 24px card with the sheet lift. On a topic page the full list sits in one white card, with titles in the display face. A "more" link (600 0.9375rem, Deep Ube, trailing arrow that slides 3px on hover) closes lists.

### Topic Shelves (signature)
White 24px cards with the shelf lift in an auto-fill grid. Each head is typographic only: the topic name (display face, 1.5rem) over a Void Muted count. No icon tile. Up to five guide links follow as hairline-separated 600 rows, and a hairline-topped "All N guides" link closes the shelf (a Void Slate "About this topic" when nothing overflows).

### Article Margin (signature)
A sticky right column. The **fact sheet** is a white 24px card of label/value rows (Topic, Updated, Reading time, Plain text): Void Slate labels left, 600 values right with tabular numerals, Ube hairlines between. Below it, **On this page** lists the article's h2s and indented h3s as 16px-radius rows in Void Slate. A scroll-spy marks the section being read (the last heading past the top third of the viewport) as Deep Ube 600 on Ube Lavender. It is hidden at ≤960px.

### Reading Column
Prose in the body style at the 68ch measure. h2 in the section heading style, h3 in the title style. List markers are Ube Purple 600. Links follow the site link style (Deep Ube, 2px underline, 3px offset).
- **Callout:** an Ube Mist block, 16px radius, Ube Night text, Deep Ube for its bold run-in ("Note:"). There is no side stripe or border.
- **Code block:** Ube Night ground, Ube Lavender code in the code font, 16px radius, 18px 22px padding, scrolls horizontally with an a-700 scrollbar.
- **Inline code:** Ube Mist chip, Ube Plum text, 4px radius.
- **Table card:** a white 16px card with the shelf-style lift that scrolls horizontally on narrow screens. Headers are 600 Void Slate on Lilac Soft; rows are separated by Ube hairlines; numbers align right with tabular numerals.
- **Rule:** a 1px Ube Lavender hairline. Images take 16px radius and the window lift.

### Try It in Mima Card
Closes every article. An Ube Night 24px card: a section-heading title in white, an a-200 paragraph (max 34rem), the full pink Download pill without its glow, then a product raster (the News Wall shot from `site-assets/app/`) set as a 16px top-rounded window cropped by the card's bottom edge. The card puts the product on show without describing features.

### Topic Margin
The topic page's margin holds "All topics" as wrapping pills (white with Deep Ube text, Ube Lavender on hover; the current topic is ink with white text), then the Mima note: an Ube Lavender 24px block with a-900 copy and the compact ink Download pill.

### Closing Band and Footer
Learn reuses the landing page's lime band (headline left, Download right, wrapping) and onyx footer unchanged. The band's Download is the Calm (Ube Night) variant on Learn.

## Do's and Don'ts

### Do:
- **Do** take every purple from the Ube a-50..a-950 scale, and use a-700 for any purple text or ring.
- **Do** keep hot pink to the single download action (and the demo play disc).
- **Do** show the product as real-UI rasters in the rounded, soft-shadowed app window, regenerated through `app-shots/` with fictional content.
- **Do** use lime as strokes, icon colour on Ube Night, or a full-bleed band with ink type, and never as text on light grounds.
- **Do** use Mima icon-set line icons (2px stroke, round caps) inline as SVG.
- **Do** set AI-generated text in MimaSerif italic (the AI voice) and label it "AI summary".
- **Do** separate stacked list items with 1px Ube hairlines.
- **Do** give reading surfaces a 68ch column, a sticky fact-sheet margin and hairline entry rows, and set code (only code) in the system mono stack.
- **Do** step secondary Download actions down to Ube Night or ink when the bar's pink pill is on the page.
- **Do** ease state changes with cubic-bezier(0.16, 1, 0.3, 1) at 0.2–0.5s, and honour reduced motion.

### Don't:
- **Don't** use hard, offset or untinted heavy shadows. Lift is soft and palette-tinted.
- **Don't** tint network logos to the palette or show them in monochrome tiles (X excepted, which is ink by its own brand).
- **Don't** add uppercase eyebrows or kickers above headings, and don't use emoji or glyph icons.
- **Don't** use square corners on buttons, tiles or frames.
- **Don't** loop decorative motion. Animations play once; repeating motion is allowed only inside the product window, depicting the app, pausable, and stopped under reduced motion.
- **Don't** separate list items or flag content with coloured side stripes. Callouts are a tinted block, not a bordered one.
- **Don't** build Learn listings as date-sorted thumbnail card grids.
