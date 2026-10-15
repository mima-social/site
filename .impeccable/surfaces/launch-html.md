---
version: 1
slug: "launch-html"
primary_target: "launch.html"
related_targets: ["index.html"]
---

# Launch landing page (launch.html, replaces index.html at launch)

Scope: mima.social home page. Visitor mode: Persuade. Tracking issue mima-social/desktop#1348.

Audience and job: people overwhelmed keeping up across Bluesky, X, LinkedIn and Mastodon. They must understand what Mima does and how it helps within seconds, download it, and optionally get updates / join Discord.

Proof and content: user-approved copy (session 2026-10-14). Logo + tagline "All your socials, none of the algorithms." with the last word cycling (algorithms / drama / ads / missed conversations); subhead "The calm, private app for all your social networking, news, and conversations."; CTA "Download for Mac" + "Free · for Apple Silicon Macs"; "Connect your accounts, no new signup required." with Bluesky, X, LinkedIn, Mastodon logos in brand colours, names as captions; features "One feed for your people / Everyone you follow, ordered how you want.", "Compose once, share everywhere / Compose your message once, share across multiple networks.", "Every conversation in one universal inbox / Mentions and DMs from every network, with pins and reminders so nobody gets left on read."; outcomes list (stop app-switching, never miss a friend, never leave a conversation hanging, compose once, consolidate your screentime); demo video in its own large block lower on the page; "Private by design" section with six earnest points; keep-up block (Get updates email form + Join the Discord).

Constraints: app views are raster screenshots rendered from dummy pages (app-shots/) that recreate the real Mima UI (founder screenshots of News Wall timeline/board, Conversations, cross-post) with synthetic people and posts; no real names, faces or posts. Never show features Mima lacks (no Drafts, Scheduled, Favorites folders). Download URL and demo video are placeholders. Brand guide binding; animated M wordmark draw-on (350ms) then "ima" fade (150ms).

Build path: code-led for this build (user, 2026-10-14, answering "How should I get past the mockup's invented app window?": "Switch to code-first (Recommended)"). The comp-led run in .impeccable/build/state.json was abandoned at the plates phase by that choice. Critique reference (not an approved comp): .impeccable/mocks/decision/dealt-tabs.png. Its app window is superseded by the user ("the mockup's app window no longer applies, build it from my screenshots"); app views are rasters rendered from app-shots/. Project default buildPath stays "comp" (the switch binds this build only).

Unresolved: public download URL; demo video. Resolved 2026-10-14: privacy copy uses "We never store your passwords" (verified against next) and "No Mima servers"; X/LinkedIn shown without Beta caveats by user decision.

## Direction contract

THESIS: Show the product working instead of describing it. The category default is a headline over three icon-and-sentence feature cards; this page keeps the three feature titles readable as a list while a large, live Mima window beside them demonstrates each one.

OWN-WORLD: Mima Ube world. Lilac-white ground washed with the brand's grainy lime and hot-pink marketing fields; near-black extra-bold grotesque display; purple primary, hot-pink CTA pill, lime squiggle accents; white rounded app window with soft Ube shadow; network logos in true brand colours on rounded tiles.

STORY: The visitor reads the tagline and knows Mima gathers their networks without algorithms; sees Download immediately; sees their networks; watches the app cycle through feed, compose and inbox; then reads how it helps, watches the demo, learns why it is private, and downloads or stays in touch.

FIRST VIEWPORT: Top-left Mima logo. Centred two-line extra-bold headline, subhead below, then a hot-pink pill "Download for Mac / Free · for Apple Silicon Macs" flanked by lime spark strokes, then a row of four brand-coloured network tiles with "Connect your accounts, no new signup required." Lower half: feature list (three items, icon tiles, active item highlighted, progress dots) left of a large Mima app window showing the matching view. A purple Mima-loop squiggle crosses the right edge, a pink one the left.

FORM: Show, don't tell (feature tabs with rotating product view), position 3 on the ordered list; seed: none (unavailable). The roll printed no SEED REFERENCE line. Signature interaction: the app window auto-advances through the three features, synced to the list, pausable, keyboard-selectable.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
