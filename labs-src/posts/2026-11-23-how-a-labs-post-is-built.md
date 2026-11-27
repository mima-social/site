---
title: How a Labs post is put together
slug: how-a-labs-post-is-built
deck: A stand-in post that shows every part of the layout: the sleeve, the credits band, an annotated figure, margin notes and code.
category: Engineering
date: 2026-11-23
author: dave-monk
draft: true
draft-note: The credits name Dave Monk because his post will be the first. None of these words are his.
shipped: Stand-in: the Labs post layout
figure: /site-assets/app/board.webp
figure-alt: The Mima News Wall in Board view, with posts from four networks in columns above the composer
figure-caption: Stand-in figure: the News Wall from the landing page. The people and posts in it are made up.
callout-1: 46 10 from 54 0 | Network filters
callout-2: 72 10 from 86 0 | Timeline and Board views
callout-3: 10 86 from 0 72 | One composer for every network
---

This page is a draft. It stands in for the first Labs post until its author sends the real one, and it uses every part of the layout once so each part can be checked on a deploy preview.[^why]

## The sleeve

The dark block at the top is the sleeve. It holds the category, the title, a one-sentence deck and the hero figure. The lime card across its foot is the credits band: who wrote the post, their role, what shipped, the reading time and the date.

The figure can carry three to five numbered callouts, and the text refers to them by number. In the stand-in figure above, callout 1 marks the network filters, callout 2 the switch between Timeline and Board, and callout 3 the composer.[^callouts]

## What a post is made of

A post is one Markdown file in `labs-src/posts/`. Its front matter fills the sleeve and the credits band. This is the front matter of the page you are reading, shortened:

```
---
title: How a Labs post is put together
slug: how-a-labs-post-is-built
category: Engineering
date: 2026-11-23
author: dave-monk
draft: true
figure: /site-assets/app/board.webp
callout-1: 46 10 from 54 0 | Network filters
---
```

::: number 68ch | the width of the reading column, the same measure Learn uses

An author is defined once in `labs-src/authors.json` and reused by every post they write.[^authors] The build is the same script that builds Learn, and it uses only the Python standard library.

| Field | Needed | What it does |
|---|---|---|
| `title`, `deck` | Yes | The sleeve's headline and the sentence under it |
| `category` | Yes | The lime line above the title |
| `author` | Yes | A key in `authors.json` |
| `shipped` | No | The "what shipped" cell of the credits band |
| `compact` | No | The smaller sleeve for a short post |
| `draft` | No | Keeps the post out of the index, feed, sitemap and `llms.txt` |

## Notes in the margin

A note is written as a Markdown footnote. On a wide screen it sits in the margin beside the paragraph that cites it. On a narrow screen it follows that paragraph.

> **Note:** a number in a post is either real or labelled as illustrative. The big number in the margin is real: it is the column width set in the stylesheet.

Lists, tables, code and callouts look the way they do on Learn, so a reader who knows one knows the other.

- Code is the only text set in a monospace face.
- Hot pink stays on the Download button in the bar.
- A draft is marked at the top of its page and is not published.

[^why]: The real first post, its author's site link and their photo are still to come.
[^callouts]: Callouts are set in front matter, as a point on the figure, a place for the numbered disc and a short label.
[^authors]: An author with no photo gets a disc with their initials, and an author with no link gets no link.
