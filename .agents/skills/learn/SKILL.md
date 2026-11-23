---
name: learn
description: Write and update the /learn guides when Mima ships. Use on a release message from the desktop Release Manager, on a `documentation` issue titled "Document <feature> (Mima vX.Y.Z)", or when asked for a Learn page; ends in a draft PR with app pictures.
---

# /learn: release-to-guides writer

You write the guides at `/learn/`. People read them, and AI agents crawl the
Markdown copies and `llms.txt`, so every guide is the **answer** to a question
someone would type or ask an agent. When Mima releases, you turn the release
into new and updated guides and open a **draft** PR.

Read first: `README.md` → "Learn (the knowledge base)" for front matter,
Markdown support and the build; `PRODUCT.md` for claim and voice rules;
`app-shots/README.md` for pictures. Load `/writing-for-agents` before you
compose: its levers (one meaning in one place, positive statements, no
no-op sentences) apply to the guide's Markdown copy as much as to a skill.

## 1. Take the release

The release arrives one of three ways: an `<hc from=…>` message from the
desktop Release Manager, a `documentation` issue filed by desktop's `/release`,
or the person naming a version. Whichever it is, treat its feature summary as a
lead, and the tag as the truth.

- Confirm the tag is the Latest release: `gh release view vX.Y.Z -R mima-social/desktop`.
- Read at the tag, without checking it out:
  `git -C ~/Mima/desktop show vX.Y.Z:<path>` for the announcement
  (`announcements/`), the feature's doc in `docs/`, and each component's header
  comment and `.stories.tsx`.
- List every user-visible change, and for each write down the labels the app
  uses, where it lives, what it cannot do, and what is off by default.

**Done when** every change in the summary has a line citing the file at the tag
that proves it, and every claim the tag contradicts or leaves unproven is on a
"differs from the summary" list for the PR body.

## 2. Map changes to pages

Each change gets exactly one outcome:

- **New guide** when it answers a question no guide answers yet.
- **Update** to the guide whose question it changes; bump `updated`.
- **Skip**, with the reason (a fix nobody would search for; a feature still
  hidden behind a flag, which gets its guide in the release that shows it).

Add a topic to `learn-src/topics.json` only when a new guide fits none of the
existing ones. Also bring `PRODUCT.md` ("Shipped", latest release) and the
hand-written parts of `llms.txt` in step.

**Done when** every change from step 1 has one outcome, shown as a table in the
PR body.

## 3. Write each guide as an answer

- **Title: the question**, in the reader's words, naming the things they would
  search for: "What's an MCP server for Bluesky, X, LinkedIn and Mastodon?",
  "Can I read my Bluesky and Mastodon lists in one app?".
- **`summary`: the answer in one sentence.** It is what search results and
  agents quote, so it must stand alone and name Mima.
- **Body:** TL;DR, where to find it in Mima (the app's exact labels in bold),
  how to use it, what it does not do and when another tool fits better, the
  version and date it arrived, then an FAQ of the follow-up questions. Write
  FAQ questions as bold paragraph openers.
- **Honest limits beat a clean pitch.** State the limit and the privacy cost in
  the guide's own words, checked against the tag, even when the summary you
  were handed is rosier.
- Link the new guide from `related` and from the body of the guides it touches.

**Done when** each guide's title is a question, its summary answers it alone,
and every sentence about Mima traces to your step-1 list.

## 4. Pictures and animations

Every new guide shows the feature at least once. Real screenshots show real
people, so pictures are `app-shots/` views built from the app's source at the
tag, with the fictional cast.

- **Stills:** add a view per feature state to `app-shots/build.py`, render it,
  and look at the result before using it. The first figure's caption says the
  people are made up.
- **Animations:** there is no pipeline yet. When motion explains the feature
  better than stills, ask the person for a recording and give them the shot
  list: the starting screen, each click, the end state, and the length. Put a
  still in the guide meanwhile and name the missing recording under
  "Requested" in the PR body.
- Under Herdr Core, a helper agent in an hc terminal can build the views while
  you write, as `/fix` sweep mode does; give it the views, the source paths at
  the tag, and this section.

**Done when** each figure in a guide resolves to a rendered file you have
looked at, and every recording you want is requested with its shot list.

## 5. Build, check, draft PR

Build with the three commands in the README (build, og, build again). Then
follow `/fix` steps 4 to 7 for the checks, the look at desktop and phone
widths, and the draft PR against `main`. The PR body carries, in place of
`/fix`'s repro: the step-2 table, the "differs from the summary" list, the
"Requested" list, and `Closes #<n>` for each `documentation` issue it answers.

Finish by giving the person each changed page's deploy-preview URL
(`https://deploy-preview-<pr>--mima-site.netlify.app/learn/<slug>/`) with one
line on what to check there, and reply to the Release Manager with the PR link
when the release came from it (`hc send <its id>`).

**Done when** checks pass, the PR is a draft, and the person has the preview
list. It stays a draft until they have read the pages: merging publishes them.
