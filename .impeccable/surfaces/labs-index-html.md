---
version: 1
slug: "labs-index-html"
primary_target: "labs/index.html"
related_targets: ["labs/drafts/how-a-labs-post-is-built/index.html","labs/drafts/compact-sleeve-test/index.html"]
---

# Labs, the Mima blog (labs/index.html, labs/<slug>/index.html, labs/drafts/…)

Scope: mima.social/labs, the blog called Labs (after Mima Labs). Visitor mode: Read. Direction chosen by the owner in a surface round on 2026-11-23 and recorded in mima-social/site#44; do not reopen it.

Audience and job: mainly other engineers. The people building Mima show their work and make engineers wish they were on the team. Engineering is the first category, not the whole blog; non-engineering posts come later. Posts are long technical write-ups (code, diagrams, numbers) or short show-and-tell posts led by a screenshot or recording.

Content: posts are Markdown in labs-src/posts/, authors in labs-src/authors.json, categories in labs-src/categories.json. `python3 learn-src/build.py` builds Labs with Learn (labs-src/labs.py). A post with `draft: true` builds under /labs/drafts/, is noindex, and stays out of the feed, sitemap and llms.txt. Until Dave Monk's post text, site URL and photo arrive, the only posts are a marked draft and a compact test post.

Build path: code-led (Read surface). Critique reference: .impeccable/mocks/decision/liner-notes.html (the owner's chosen sketch, composition only; none of its placeholder words, links or fake window ship).

Constraints: PRODUCT.md claims rules apply to every post; illustrative figures and numbers are labelled. Brand rule from the owner: same Mima room, more swagger. Changes to Learn are limited to the shared bar and footer links. The lime category line above the title is the owner's pinned exception to the no-eyebrow rule; it stays sentence case and names the post's category.

Borrowed pieces (owner asked for both): an annotated hero figure with 3 to 5 numbered lime callout discs joined by squiggle-style strokes that draw on once (already drawn under reduced motion); and numbered margin sidenotes with an optional big-number card, which fall inline after their paragraph at 960px and below.

Index: a discography. Newest post as a full sleeve, earlier posts as hairline rows. No thumbnail card grid. Short posts take a compact sleeve (front-matter flag).

Unresolved: Dave's post (title, deck, body), his site URL and an approved photo; the owner's photo and URL; whether index.html links to Labs once a post is published.

## Direction contract

THESIS: Every post ships like a release: the work on the sleeve, the people in the credits. Refuses the category default of a white column with a thumbnail and a grey byline.

OWN-WORLD: The Mima Ube world. An Ube Night (a-950) sleeve owns the top of each post. Lime is the credits band, with ink type. Below the sleeve: lilac ground, a 68ch reading column, Ube Night code blocks and Ube Mist callouts as on Learn. A brand squiggle (the looping M, painted in lime) crosses the sleeve's left edge; it shows from 1280px wide, where it clears the text column, and is dropped below that. Hot pink appears only on the bar's Download pill (One Pink Rule).

STORY: An engineer lands on a post, sees what was built and who built it at a glance, reads how it was done with the numbers and code beside the text, and wants to follow the team (feed, other posts) or try Mima.

FIRST VIEWPORT: Post: the Learn-style bar on the dark sleeve (wordmark, Home, Learn, Labs current, small pink Download pill). Left: category line in lime, then the title in display 800 (about 76px), then a deck in a-200. Right: the hero figure in a 16px window. Across the sleeve's foot: the lime credits band, a 24px card printed dense: author face (64px circle), name, link to their site, role, what shipped, PR or issue numbers, read time and date. Then the reading column, with the margin to its right.

FORM: Liner notes, from three dealt structures; seed:2a4af215940076c6. Signature: the credits band. Motion grammar: callout strokes draw on once.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
