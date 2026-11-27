"""Build Labs, the Mima blog at /labs/, from Markdown.

`python3 learn-src/build.py` runs this with the Learn build (one command
builds the whole site). It reads labs-src/posts/*.md, labs-src/authors.json
and labs-src/categories.json, then writes:

- labs/index.html             the index: newest post as a sleeve, the rest as rows
- labs/<slug>/index.html      each published post
- labs/<slug>.md              each post as plain Markdown, for agents
- labs/feed.xml               an Atom feed of the published posts
- labs/drafts/…               the same pages for posts marked `draft: true`

Drafts are for looking at on a deploy preview. They are noindex and stay out
of labs/index.html, the feed, sitemap.xml and llms.txt. The Learn build asks
this module for the sitemap rows and the llms.txt section, so those two files
have one writer. Standard library only.
"""

import datetime
import html
import json
import math
import pathlib
import re
import struct
import sys

import build  # learn-src/build.py: shared chrome (head, foot, band, icons)
import md

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT / "labs"
SITE = build.SITE
FEED = "/labs/feed.xml"
CSS = ("/labs/labs.css",)  # loaded after learn.css
TAGLINE = "How Mima gets built, by the people building it."
# The feed's own date while nothing is published (Atom needs one, and the
# build must give the same output every run).
EPOCH = datetime.date(2026, 11, 23)
LONG_TITLE = 40  # characters; longer titles step down a size
DRAFT_NOTE = "Not published, and not in the feed, the sitemap or llms.txt."
NEEDED = "[NEEDED"  # marks a field the author still has to supply; allowed in drafts only

esc = html.escape


# ---------------------------------------------------------------- helpers

def image_size(path):
    """(width, height) of a WebP, PNG or JPEG file, read from its header."""
    data = pathlib.Path(path).read_bytes()
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        kind = data[12:16]
        if kind == b"VP8X":
            return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
        if kind == b"VP8L":
            bits = int.from_bytes(data[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h)
            i += 2 + length
    raise ValueError(f"{path}: not a WebP, PNG or JPEG image")


def parse_callout(text):
    """A hero-figure callout from front matter.

    `44 13 from 30 0 | Network filters` puts a numbered disc at 30% across
    and 0% down the figure, and draws a stroke from it to the point 44% across
    and 13% down. Returns {"to": (x, y), "from": (x, y), "text": str}."""
    m = re.fullmatch(r"\s*([\d.]+)\s+([\d.]+)\s+from\s+([\d.]+)\s+([\d.]+)\s*\|\s*(.+?)\s*", text)
    if not m:
        raise ValueError(f"callout `{text}` should look like `44 13 from 30 0 | Label`")
    nums = [float(m.group(i)) for i in range(1, 5)]
    if any(n < 0 or n > 100 for n in nums):
        raise ValueError(f"callout `{text}`: positions are percentages from 0 to 100")
    return {"to": (nums[0], nums[1]), "from": (nums[2], nums[3]), "text": m.group(5)}


def callout_path(start, end):
    """The stroke from a callout's disc to its target: one loose S-curve in
    the style of the brand squiggles. Points are in SVG user units."""
    (x1, y1), (x2, y2) = start, end
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1
    px, py = -dy / length, dx / length  # unit normal
    bend = length * 0.28
    c1 = (x1 + dx * 0.3 + px * bend, y1 + dy * 0.3 + py * bend)
    c2 = (x1 + dx * 0.7 - px * bend, y1 + dy * 0.7 - py * bend)
    return "M{:.1f} {:.1f} C {:.1f} {:.1f}, {:.1f} {:.1f}, {:.1f} {:.1f}".format(x1, y1, *c1, *c2, x2, y2)


def initials(name):
    words = name.split()
    return (words[0][0] + (words[-1][0] if len(words) > 1 else "")).upper()


def host(url):
    """The short form of an author's link: `https://www.mima.social/` is `mima.social`."""
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


def title_class(title):
    return "long" if len(title) > LONG_TITLE else ""


_CITE = re.compile(r"\[\^([\w-]+)\]")
_NOTE_DEF = re.compile(r"^\[\^([\w-]+)\]:\s+(.*)$")
_NUMBER = re.compile(r"^:::\s*number\s+(.+)$")


def split_notes(body):
    """Pull the margin material out of a post body.

    Returns (body, notes, numbers). `notes` maps a footnote id to its Markdown
    text (`[^id]: text` lines). Each `::: number 68ch | label` line becomes a
    marker block in the body, and `numbers` lists its parts in order."""
    notes, numbers, lines, fenced = {}, [], [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
        if not fenced:
            m = _NOTE_DEF.match(line)
            if m:
                notes[m.group(1)] = m.group(2).strip()
                continue
            m = _NUMBER.match(line.strip())
            if m:
                parts = [p.strip() for p in m.group(1).split("|")]
                if len(parts) < 2:
                    raise ValueError(f"`{line.strip()}` should look like `::: number 68ch | what it counts`")
                numbers.append({"figure": parts[0], "label": parts[1], "flags": parts[2:]})
                lines += ["", f"<!--number:{len(numbers) - 1}-->", ""]
                continue
        lines.append(line)
    return "\n".join(lines), notes, numbers


def number_card(n):
    lime = " lime" if "lime" in n["flags"] else ""
    tag = '<span class="tag">Illustrative</span>' if "illustrative" in n["flags"] else ""
    return (f'<p class="bignum{lime}"><b>{esc(n["figure"])}</b>'
            f'<span>{md.inline(n["label"])}</span>{tag}</p>')


def with_margin(blocks, notes, numbers):
    """Join a post's blocks, hanging its margin material beside them.

    Each `[^id]` in a block becomes a numbered marker, and the note follows
    its block in the page as an <aside>. The aside carries the grid rows it
    covers (`--r` to `--e`): from its own block down to the next aside, so
    notes line up with the paragraph that cites them and never overlap.
    Returns (html, count of notes)."""
    rows = []   # the block HTML, one per grid row
    asides = {}  # row index -> list of aside items
    order = {}  # note id -> its number
    for block in blocks:
        m = re.fullmatch(r"<!--number:(\d+)-->", block.strip())
        if m:
            if not rows:
                raise ValueError("`::: number` must follow the paragraph it sits beside")
            asides.setdefault(len(rows) - 1, []).append(number_card(numbers[int(m.group(1))]))
            continue
        if not block.startswith("<pre"):
            def cite(c, row=len(rows)):
                key = c.group(1)
                if key not in notes:
                    return c.group(0)
                if key not in order:
                    order[key] = len(order) + 1
                    asides.setdefault(row, []).append(
                        f'<p class="sidenote" id="sn-{order[key]}" role="note"><a class="num" href="#snr-{order[key]}" '
                        f'aria-label="Back to the text for note {order[key]}">{order[key]}</a>'
                        f'<span>{md.inline(notes[key])}</span></p>')
                    return (f'<sup class="snr"><a id="snr-{order[key]}" href="#sn-{order[key]}" '
                            f'aria-label="Note {order[key]}">{order[key]}</a></sup>')
                return f'<sup class="snr"><a href="#sn-{order[key]}" aria-label="Note {order[key]}">{order[key]}</a></sup>'
            # Leave `[^x]` alone inside inline code.
            parts = re.split(r"(<code>.*?</code>)", block, flags=re.S)
            block = "".join(p if p.startswith("<code>") else _CITE.sub(cite, p) for p in parts)
        rows.append(block)
    unused = sorted(set(notes) - set(order))
    if unused:
        raise ValueError(f"notes never cited: {', '.join(unused)}")
    out, marks = [], sorted(asides)
    for i, block in enumerate(rows):
        out.append(block)
        if i in asides:
            later = [m for m in marks if m > i]
            end = (later[0] if later else len(rows)) + 1
            lead = " first" if i == 0 else (" tight" if re.match(r"<h[23]", rows[i - 1]) else "")
            out.append(f'<aside class="margin-notes{lead}" style="--r:{i + 1};--e:{end}">{"".join(asides[i])}</aside>')
    return "\n".join(out), len(order)


def plain_markdown(body):
    """The post body for its Markdown twin: big-number lines become quotes."""
    def number(m):
        parts = [p.strip() for p in m.group(1).split("|")]
        note = " (illustrative)" if "illustrative" in parts[2:] else ""
        return f"> **{parts[0]}**: {parts[1]}{note}"
    out, fenced = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
        m = None if fenced else _NUMBER.match(line.strip())
        out.append(number(m) if m else line)
    return re.sub(r"\]\(/", f"]({SITE}/", "\n".join(out).strip())


# ---------------------------------------------------------------- content

def load_authors():
    authors = json.loads((HERE / "authors.json").read_text())
    for key, a in authors.items():
        a["id"] = key
        for field in ("name", "role"):
            if not a.get(field):
                sys.exit(f"authors.json: `{key}` is missing `{field}`")
        photo = ROOT / "site-assets" / "authors" / f"{key}.webp"
        a["photo"] = f"/site-assets/authors/{key}.webp" if photo.exists() else ""
        a["url"] = a.get("url") or ""
    return authors


def load_categories():
    return {c["name"]: c for c in json.loads((HERE / "categories.json").read_text())}


def load_post(source, name, authors, categories):
    """One post from its Markdown source. Raises ValueError on a bad post."""
    meta, body = md.front_matter(source)
    for key in ("title", "slug", "deck", "category", "date", "author"):
        if not meta.get(key):
            raise ValueError(f"{name}: front matter is missing `{key}`")
    draft = meta.get("draft", "").lower() == "true"
    if not draft:
        missing = [k for k, v in list(meta.items()) + list(authors.get(meta["author"], {}).items())
                   if isinstance(v, str) and NEEDED in v]
        if missing or NEEDED in body:
            raise ValueError(f"{name}: a published post cannot carry [NEEDED: …] markers ({', '.join(missing) or 'body'})")
    if meta["category"] not in categories and not (draft and meta["category"].startswith(NEEDED)):
        raise ValueError(f"{name}: category `{meta['category']}` is not in categories.json")
    if meta["author"] not in authors:
        raise ValueError(f"{name}: author `{meta['author']}` is not in authors.json")
    p = dict(meta)
    p["draft"] = draft
    p["compact"] = meta.get("compact", "").lower() == "true"
    p["author_obj"] = authors[meta["author"]]
    p["category_obj"] = categories.get(meta["category"])
    p["date_d"] = datetime.date.fromisoformat(meta["date"])
    p["updated_d"] = datetime.date.fromisoformat(meta.get("updated") or meta["date"])
    p["callouts"] = [parse_callout(meta[k]) for k in sorted(k for k in meta if re.fullmatch(r"callout-\d", k))]
    if p["callouts"] and not 3 <= len(p["callouts"]) <= 5:
        raise ValueError(f"{name}: a figure takes 3 to 5 callouts, or none")
    if meta.get("figure"):
        if not meta.get("figure-alt"):
            raise ValueError(f"{name}: `figure` needs `figure-alt`")
        p["figure_size"] = image_size(ROOT / meta["figure"].lstrip("/"))
    elif p["callouts"]:
        raise ValueError(f"{name}: callouts need a `figure`")
    base = "/labs/drafts/" if p["draft"] else "/labs/"
    p["url"] = f"{base}{p['slug']}/"
    p["md_url"] = f"{base}{p['slug']}.md"
    text, notes, numbers = split_notes(body)
    p["body_md"] = body
    blocks, _ = md.to_blocks(text)
    p["html"], p["note_count"] = with_margin(blocks, notes, numbers)
    p["minutes"] = max(1, round(len(re.findall(r"\w+", body)) / 220))
    return p


def load_posts():
    authors, categories = load_authors(), load_categories()
    posts, slugs = [], set()
    for path in sorted((HERE / "posts").glob("*.md")):
        try:
            p = load_post(path.read_text(), path.name, authors, categories)
        except ValueError as e:
            sys.exit(str(e) if str(e).startswith(path.name) else f"{path.name}: {e}")
        if p["slug"] in slugs or p["slug"] == "drafts":
            sys.exit(f"{path.name}: slug `{p['slug']}` is taken")
        slugs.add(p["slug"])
        posts.append(p)
    posts.sort(key=lambda p: (p["date_d"], p["slug"]), reverse=True)
    return posts


def published(posts):
    return [p for p in posts if not p["draft"]]


# ---------------------------------------------------------------- parts

def head_extra(md_path=None, md_title="", noindex=False):
    out = [f'<link rel="alternate" type="application/atom+xml" href="{SITE}{FEED}" title="Mima Labs" />']
    if md_path:
        out.append(build.md_link(md_path, md_title))
    if noindex:
        out.append('<meta name="robots" content="noindex" />')
    return "\n    ".join(out)


def face(author, size=64):
    if author["photo"]:
        return (f'<img class="face" src="{author["photo"]}" alt="" width="{size}" height="{size}" '
                f'style="--s:{size}px" loading="lazy" />')
    return f'<span class="face" aria-hidden="true" style="--s:{size}px">{esc(initials(author["name"]))}</span>'


def credits(p):
    """The lime credits band: who made it, what shipped, where, how long, when."""
    a = p["author_obj"]
    link = f'<a href="{esc(a["url"])}" rel="author">{esc(host(a["url"]))}</a>' if a["url"] else ""
    cells = [("Role", esc(a["role"]))]
    if p.get("shipped"):
        cells.append(("What shipped", md.inline(p["shipped"])))
    cells.append(("Read", f'{p["minutes"]} min<span class="dot"> · </span><time datetime="{p["date_d"]}">{build.nice_date(p["date_d"])}</time>'))
    return (f'<div class="credits"><div class="who">{face(a)}<p><b>{esc(a["name"])}</b>{link}</p></div>'
            f'<dl>{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in cells)}</dl></div>')


def hero_figure(p, lead=True, callouts=True):
    """The sleeve's picture in its 16px window, with optional numbered callouts."""
    if not p.get("figure"):
        return ""
    w, h = p["figure_size"]
    img = (f'<img src="{esc(p["figure"])}" alt="{esc(p["figure-alt"])}" width="{w}" height="{h}"'
           f'{" fetchpriority=\"high\"" if lead else " loading=\"lazy\""} />')
    lines = discs = key = ""
    if p["callouts"] and callouts:
        vh = round(1000 * h / w)
        paths = []
        for i, c in enumerate(p["callouts"]):
            start = (c["from"][0] * 10, c["from"][1] * vh / 100)
            end = (c["to"][0] * 10, c["to"][1] * vh / 100)
            paths.append(f'<path d="{callout_path(start, end)}" pathLength="1" style="--i:{i}" />'
                         f'<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="7" style="--i:{i}" />')
            discs += f'<span class="disc" style="left:{c["from"][0]:g}%;top:{c["from"][1]:g}%" aria-hidden="true">{i + 1}</span>'
        lines = f'<svg class="callout-lines" viewBox="0 0 1000 {vh}" aria-hidden="true" focusable="false">{"".join(paths)}</svg>'
        key = '<ol class="callout-key">' + "".join(f"<li>{md.inline(c['text'])}</li>" for c in p["callouts"]) + "</ol>"
    caption = f'<p>{md.inline(p["figure-caption"])}</p>' if p.get("figure-caption") else ""
    figcaption = f"<figcaption>{key}{caption}</figcaption>" if key or caption else ""
    return f'<figure class="hero-fig"><div class="fig-frame"><div class="fig-window">{img}</div>{lines}{discs}</div>{figcaption}</figure>'


ARC = ('<div class="sleeve-art" aria-hidden="true"><svg viewBox="0 0 262 189" fill="none" aria-hidden="true" focusable="false"><path d="M3.01758 36.5533'
       'C113.893 61.0258 139.836 162.633 108.399 174.083C67.8228 188.862 20.4979 20.4917 96.0396 14.1447C150.822 9.54191 '
       '175.95 117.698 175.95 117.698C175.95 117.698 181.943 27.9814 222.897 37.1569C263.851 46.3324 240.253 149.073 '
       '240.253 149.073" /></svg></div>')


def draft_note(p=None):
    extra = f" {md.inline(p['draft-note'])}" if p and p.get("draft-note") else ""
    return f'<p class="draft-note"><strong>Draft.</strong> {DRAFT_NOTE}{extra}</p>'


def sleeve_head(p, tag="h1", link=False):
    title = f'<a href="{p["url"]}">{esc(p["title"])}</a>' if link else esc(p["title"])
    cls = " ".join(c for c in (title_class(p["title"]),) if c)
    return f"""<div class="sleeve-head">
        <div class="sleeve-text">
          <p class="cat">{esc(p["category"])}</p>
          <{tag}{f' class="{cls}"' if cls else ""}>{title}</{tag}>
          <p class="deck">{esc(p["deck"])}</p>
        </div>
        {hero_figure(p, callouts=not link)}
      </div>"""


def row(p):
    """A post as a hairline row: title, author, category, date, read time."""
    a = p["author_obj"]
    draft = '<span class="tag">Draft</span>' if p["draft"] else ""
    return (f'<li class="release"><h3><a href="{p["url"]}">{esc(p["title"])}</a>{draft}</h3>'
            f'<p class="by">{face(a, 32)}<span>{esc(a["name"])}</span></p>'
            f'<p class="meta">{esc(p["category"])} · <time datetime="{p["date_d"]}">{build.nice_date(p["date_d"])}</time>'
            f' · {p["minutes"]} min</p></li>')


def person_ld(a):
    ld = {"@type": a.get("type") or "Person", "name": a["name"]}
    if ld["@type"] == "Person":
        ld["jobTitle"] = a["role"]
    if a["url"]:
        ld["url"] = a["url"]
    if a["photo"]:
        ld["image"] = SITE + a["photo"]
    return ld


BLOG_ID = f"{SITE}/labs/#blog"


# ---------------------------------------------------------------- pages

def post_page(p, others):
    a = p["author_obj"]
    posting = {"@type": "BlogPosting", "@id": f"{SITE}{p['url']}#post", "headline": p["title"],
               "description": p["deck"], "url": SITE + p["url"], "mainEntityOfPage": SITE + p["url"],
               "datePublished": str(p["date_d"]), "dateModified": str(p["updated_d"]),
               "articleSection": p["category"], "inLanguage": "en", "timeRequired": f"PT{p['minutes']}M",
               "author": person_ld(a), "publisher": {"@id": build.ORG["@id"]}, "isPartOf": {"@id": BLOG_ID},
               "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": SITE + p["md_url"]}}
    if p.get("figure"):
        posting["image"] = SITE + p["figure"]
    ld = {"@context": "https://schema.org", "@graph": [
        build.ORG, posting,
        build.crumbs_ld([("Home", "/"), ("Labs", "/labs/"), (p["title"], p["url"])])]}
    more = ""
    if others:
        more = (f'<h2 id="more-title">More from Labs</h2>'
                f'<ol class="releases">{"".join(row(o) for o in others[:4])}</ol>')
    index = "/labs/drafts/" if p["draft"] else "/labs/"
    return build.head(f"{p['title']} · Labs · Mima", p["deck"], p["url"], ld,
                      head_extra(p["md_url"], "This post as Markdown", noindex=p["draft"]),
                      og_type="article", body_class="labs", css=CSS) + f"""
<main id="content">
  <article class="post{' compact' if p['compact'] else ''}">
    <header class="sleeve">
      {ARC}
      <div class="wrap">
      {draft_note(p) if p["draft"] else ""}
      {sleeve_head(p)}
      {credits(p)}
      </div>
    </header>
    <div class="wrap post-body">
      <div class="prose notes">
{p['html']}
      </div>
      <nav class="post-end" aria-label="More from Labs">
        {more}
        <p class="follow"><a class="more" href="{index}">All posts{build.icon('arrow-right')}</a>
          <a class="more" href="{FEED}" type="application/atom+xml">Follow the feed{build.icon('arrow-right')}</a>
          <a class="more" href="{p['md_url']}" type="text/markdown">Read as Markdown{build.icon('arrow-right')}</a></p>
      </nav>
    </div>
  </article>
</main>
{build.band()}{build.foot()}"""


def index_page(posts, drafts=False):
    """The index: the newest post as a full sleeve, earlier posts as rows.
    `drafts=True` is the preview at /labs/drafts/, which lists every post."""
    path = "/labs/drafts/" if drafts else "/labs/"
    ld = {"@context": "https://schema.org", "@graph": [
        build.ORG,
        {"@type": "Blog", "@id": BLOG_ID, "name": "Mima Labs", "url": f"{SITE}/labs/", "description": TAGLINE,
         "publisher": {"@id": build.ORG["@id"]},
         "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE + p["url"],
                       "datePublished": str(p["date_d"]), "author": person_ld(p["author_obj"])}
                      for p in posts if not p["draft"]]},
        build.crumbs_ld([("Home", "/"), ("Labs", "/labs/")])]}
    feed = f'<a class="feed" href="{FEED}" type="application/atom+xml">Follow the feed{build.icon("arrow-right")}</a>'
    if posts:
        lead, rest = posts[0], posts[1:]
        top = f"""{sleeve_head(lead, tag="h2", link=True)}
      {credits(lead)}"""
        earlier = (f"""<div class="wrap post-body">
      <section class="earlier" aria-labelledby="earlier-title">
        <h2 id="earlier-title">Earlier posts</h2>
        <ol class="releases">{"".join(row(p) for p in rest)}</ol>
      </section>
    </div>""" if rest else '<div class="post-body"></div>')
    else:
        top = '<p class="empty">Nothing is published yet. Follow the feed and the first post will come to you.</p>'
        earlier = ""
    note = (f'<p class="draft-note"><strong>Draft preview.</strong> This is how the index looks with the drafts in it. '
            f'The real index is at <a href="/labs/">/labs/</a>. This page is not published.</p>' if drafts else "")
    # Nothing to index while Labs is empty.
    return build.head("Labs: how Mima gets built · Mima", TAGLINE, path, ld,
                      head_extra(noindex=drafts or not posts), body_class="labs", css=CSS) + f"""
<main id="content">
  <div class="post index{'' if posts else ' is-empty'}">
    <header class="sleeve">
      {ARC}
      <div class="wrap">
      {note}
      <div class="masthead">
        <h1>Labs</h1>
        <p>{TAGLINE}</p>
        {feed}
      </div>
      {top}
      </div>
    </header>
    {earlier}
  </div>
</main>
{build.band()}{build.foot()}"""


def post_md(p):
    a = p["author_obj"]
    by = f"[{a['name']}]({a['url']})" if a["url"] else a["name"]
    lines = [f"# {p['title']}", "", f"> {p['deck']}", ""]
    if p["draft"]:
        lines += [f"Draft. {DRAFT_NOTE}", ""]
    meta = [f"By {by}, {a['role']}", f"Category: {p['category']}", f"Published: {p['date_d']}",
            f"Source: {SITE}{p['url']}"]
    if p.get("shipped"):
        meta.insert(1, f"What shipped: {p['shipped']}")
    lines += [" · ".join(meta), ""]
    if p.get("figure"):
        lines += [f"![{p['figure-alt']}]({SITE}{p['figure']})", ""]
        lines += [f"{i + 1}. {c['text']}" for i, c in enumerate(p["callouts"])]
        if p["callouts"]:
            lines.append("")
    lines += [plain_markdown(p["body_md"]), "", "---", "",
              f"About Mima: {build.ABOUT_MIMA} More from Labs: {SITE}/labs/ (feed: {SITE}{FEED})", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- feed and crawler files

def stamp(d):
    return f"{d}T00:00:00Z"


def feed(posts):
    """An Atom feed of the published posts, newest first."""
    live = published(posts)
    updated = max((p["updated_d"] for p in live), default=EPOCH)
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<feed xmlns="http://www.w3.org/2005/Atom">',
           "  <title>Mima Labs</title>",
           f"  <subtitle>{esc(TAGLINE)}</subtitle>",
           f"  <id>{SITE}/labs/</id>",
           f'  <link rel="alternate" type="text/html" href="{SITE}/labs/" />',
           f'  <link rel="self" type="application/atom+xml" href="{SITE}{FEED}" />',
           f"  <updated>{stamp(updated)}</updated>",
           f"  <author><name>Mima</name><uri>{SITE}/</uri></author>"]
    for p in live:
        a = p["author_obj"]
        uri = f"<uri>{esc(a['url'])}</uri>" if a["url"] else ""
        content = re.sub(r'(src|href)="/', rf'\1="{SITE}/', p["html"])
        out += ["  <entry>",
                f"    <title>{esc(p['title'])}</title>",
                f"    <id>{SITE}{p['url']}</id>",
                f'    <link rel="alternate" type="text/html" href="{SITE}{p["url"]}" />',
                f"    <published>{stamp(p['date_d'])}</published>",
                f"    <updated>{stamp(p['updated_d'])}</updated>",
                f"    <author><name>{esc(a['name'])}</name>{uri}</author>",
                f'    <category term="{esc(p["category"])}" />',
                f"    <summary>{esc(p['deck'])}</summary>",
                f'    <content type="html">{esc(content)}</content>',
                "  </entry>"]
    out.append("</feed>")
    return "\n".join(out) + "\n"


def sitemap_rows(posts):
    """(path, date) rows for sitemap.xml: the index and each published post.
    Empty while nothing is published."""
    live = published(posts)
    if not live:
        return []
    return [("/labs/", max(p["updated_d"] for p in live))] + [(p["url"], p["updated_d"]) for p in live]


def llms_section(posts):
    """The `## Labs` section of llms.txt, or "" while nothing is published."""
    live = published(posts)
    if not live:
        return ""
    out = ["## Labs", "",
           f"The blog from the people building Mima. Each post is also published as Markdown at the link below. Feed: {SITE}{FEED}", ""]
    out += [f"- [{p['title']}]({SITE}{p['md_url']}): {p['deck']} (By {p['author_obj']['name']}, {p['date_d']}.)" for p in live]
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- main

def build_all():
    """Write every Labs file and return the posts (drafts included)."""
    posts = load_posts()
    keep = {"labs.css"}
    if OUT.exists():
        for f in sorted(OUT.rglob("*"), reverse=True):
            if f.is_file() and f.name not in keep:
                f.unlink()
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()
    live = published(posts)
    build.write(OUT / "index.html", index_page(live))
    build.write(OUT / "feed.xml", feed(posts))
    if len(live) != len(posts):
        build.write(OUT / "drafts" / "index.html", index_page(posts, drafts=True))
    for p in posts:
        pool = posts if p["draft"] else live
        build.write(OUT / p["url"][len("/labs/"):] / "index.html", post_page(p, [o for o in pool if o is not p]))
        build.write(OUT / p["md_url"][len("/labs/"):], post_md(p))
    return posts
