---
version: 1
slug: "learn-index-html"
primary_target: "learn/index.html"
related_targets: ["learn/article-one/index.html"]
---

# Learn knowledge base (learn/index.html, learn/<slug>/index.html, learn/topics/<slug>/index.html)

Scope: mima.social/learn, the "Learn" knowledge base. Visitor mode: Read, with an edu-marketing job (user, 2026-11-09: "This is edu-marketing, telling people why Mima is the best option"). Primary readers are AI agents and crawlers; pages must still look good to people. Not a blog.

Audience and job: an agent or person with a question about keeping up across Bluesky, X, LinkedIn and Mastodon finds a direct answer, then learns why Mima is the better way and can download it.

Content: articles are Markdown in learn-src/articles/ (front matter: title, slug, summary, topic, order, updated, related), topics in learn-src/topics.json. `python3 learn-src/build.py` renders every page, the Markdown twins (learn/<slug>.md), sitemap.xml, robots.txt and the Learn section of llms.txt. 18 slots, generic lorem placeholders for now (user choice). Many topics expected over time, plus a running feed of new articles; shelves must handle more articles than fit.

Build path: code-led (Read surface; concept-seed prints code-led for Read whatever .impeccable/config.json records). No comp round; critique reference .impeccable/mocks/decision/field-guide.html.

Constraints: PRODUCT.md claims rules apply to every article. Brand guide binding. Each article states its answer in its first lines (summary) for agents.

## Direction contract

THESIS: A naturalist's field guide, not a blog river: topics stand side by side as shelves, and every article carries a margin fact sheet. Refuses the category default of a date-sorted card grid with thumbnails.

OWN-WORLD: Mima Ube world. Lilac ground, white 24px shelves with soft Ube lift, Ube hairline entries, near-black extra-bold display, Ube Night code blocks, Ube Mist callouts, lime closing band with ink Download pill.

STORY: The reader sees the newest guides in a running list, scans topic shelves for their question, opens a guide, gets the short answer at once, reads the steps with facts in the margin, learns what Mima does differently, and downloads or keeps browsing the topic.

FIRST VIEWPORT: Index: bar (wordmark left, Learn nav, small Download pill right); headline and lede left with the Latest list (5 newest, date and topic) right; then topic shelves in an auto-fill grid, each capped at 5 entries with "All N guides" linking to the topic page. Article: breadcrumb, title, short-answer lead; reading column at 68ch with a sticky right margin holding the fact sheet and On this page contents.

FORM: Field guide shelves, position 5 on the ordered list; seed:f40533d57939158c. Signature interaction: margin contents tracks the section being read (scroll-spy), and shelves overflow into topic pages.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
