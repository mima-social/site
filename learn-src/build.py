#!/usr/bin/env python3
"""Build the Learn knowledge base from Markdown.

Run `python3 learn-src/build.py` from anywhere. It reads the articles in
learn-src/articles/*.md and the topics in learn-src/topics.json, then writes:

- learn/index.html                  the index: latest guides and topic shelves
- learn/topics/<topic>/index.html   every guide in one topic
- learn/<slug>/index.html           each article
- learn/<slug>.md                   each article as plain Markdown, for agents
- sitemap.xml, robots.txt           for crawlers
- llms.txt                          its "## Learn" section is regenerated

Output is committed, so Netlify serves it with no build step. Standard
library only, like app-shots/build.py.
"""

import datetime
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import md  # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT / "learn"
SITE = "https://mima.social"
SHELF_LIMIT = 5   # entries a topic shelf shows before "All N guides"
LATEST_COUNT = 5  # entries in the index's Latest list
DOWNLOAD = "https://mima.social/download"
GA_ID = "G-GHJGZHDR95"
MIMA_LINE = "Mima collects all your social feeds and friends in one calm place."

esc = html.escape


# ---------------------------------------------------------------- content

def load_topics():
    topics = json.loads((HERE / "topics.json").read_text())
    for t in topics:
        t["articles"] = []
    return topics


def load_articles(topics):
    by_name = {t["name"]: t for t in topics}
    articles, slugs = [], set()
    for path in sorted((HERE / "articles").glob("*.md")):
        meta, body = md.front_matter(path.read_text())
        for key in ("title", "slug", "summary", "topic", "updated"):
            if not meta.get(key):
                sys.exit(f"{path.name}: front matter is missing `{key}`")
        if meta["slug"] in slugs:
            sys.exit(f"{path.name}: slug `{meta['slug']}` is used twice")
        if meta["topic"] not in by_name:
            sys.exit(f"{path.name}: topic `{meta['topic']}` is not in topics.json")
        slugs.add(meta["slug"])
        a = dict(meta)
        a["body_md"] = body
        a["html"], a["headings"] = md.to_html(body)
        a["updated_d"] = datetime.date.fromisoformat(meta["updated"])
        a["published_d"] = datetime.date.fromisoformat(meta.get("published") or meta["updated"])
        a["order"] = int(meta.get("order") or 999)
        a["related"] = [s.strip() for s in meta.get("related", "").split(",") if s.strip()]
        a["minutes"] = max(1, round(len(re.findall(r"\w+", body)) / 220))
        a["url"] = f"/learn/{a['slug']}/"
        a["md_url"] = f"/learn/{a['slug']}.md"
        a["topic_obj"] = by_name[meta["topic"]]
        a["faq"] = faq_pairs(body)
        by_name[meta["topic"]]["articles"].append(a)
        articles.append(a)
    for a in articles:
        missing = [s for s in a["related"] if s not in slugs]
        if missing:
            sys.exit(f"{a['slug']}: related slugs not found: {', '.join(missing)}")
    for t in topics:
        t["articles"].sort(key=lambda a: a["order"])
        t["url"] = f"/learn/topics/{t['slug']}/"
    return articles


def faq_pairs(body):
    """Questions under a `## Common questions` or `## FAQ` heading become
    FAQPage data. Write each question as a `### Question?` heading, or as a
    paragraph that starts with the question in bold: `**Question?** Answer`."""
    m = re.search(r"^## (?:Common questions|FAQs?|Frequently asked questions)\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not m:
        return []
    section = m.group(1)
    pairs = []
    for q in re.finditer(r"^### (.+?)\s*$(.*?)(?=^### |\Z)", section, re.M | re.S):
        answer = " ".join(q.group(2).split())
        if answer:
            pairs.append((q.group(1).strip(), re.sub(r"[*`]", "", answer)))
    for q in re.finditer(r"^\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\n|\Z)", section, re.M | re.S):
        answer = " ".join(q.group(2).split())
        if answer:
            pairs.append((q.group(1).strip(), re.sub(r"[*`]", "", answer)))
    return pairs


def nice_date(d):
    return f"{d.day} {d.strftime('%b %Y')}"


# ---------------------------------------------------------------- shared chrome

def sprite():
    """Pull the icons Learn uses out of the landing page, so they stay in step."""
    page = (ROOT / "index.html").read_text()
    want = ["i-download", "arrow-right", "arrow-left", "heart-filled", "sparkle", "i-email"]
    out = []
    for name in want:
        m = re.search(rf'<symbol id="{name}".*?</symbol>', page, re.S)
        if m:
            out.append(m.group(0))
    return '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(out) + "</svg>"


def wordmark():
    page = (ROOT / "index.html").read_text()
    m = re.search(r'<svg class="wordmark".*?</svg>', page, re.S)
    return m.group(0) if m else "Mima"


SPRITE = None
WORDMARK = None


def icon(name):
    return f'<svg class="i" aria-hidden="true" focusable="false"><use href="#{name}"></use></svg>'


def head(title, description, path, jsonld, extra=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="referrer" content="no-referrer" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    <link rel="canonical" href="{url}" />
    {extra}
    <meta property="og:type" content="{'article' if path.count('/') == 3 and '/topics/' not in path else 'website'}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:image" content="{SITE}/site-assets/og-image.jpg" />
    <meta name="twitter:card" content="summary_large_image" />
    <script type="application/ld+json">
{json.dumps(jsonld, indent=2, ensure_ascii=False)}
    </script>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag("js", new Date());
        gtag("config", "{GA_ID}");
        addEventListener("load", function () {{
            var s = document.createElement("script");
            s.async = true;
            s.src = "https://www.googletagmanager.com/gtag/js?id={GA_ID}";
            document.head.appendChild(s);
        }});
    </script>
    <link rel="preload" href="/site-assets/MimaDisplay-ExtraBold.subset.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/site-assets/MimaUI-Regular.subset.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/learn/learn.css" />
</head>
<body>
{SPRITE}
<a class="skip" href="#content">Skip to content</a>
<header class="bar">
  <div class="wrap bar-row">
    <a class="logo" href="/" aria-label="Mima home">{WORDMARK}</a>
    <nav class="bar-nav" aria-label="Site">
      <a href="/">Home</a>
      <a href="/learn/" aria-current="{'page' if path == '/learn/' else 'true'}">Learn</a>
    </nav>
    <a class="pill" href="{DOWNLOAD}" data-download>{icon('i-download')}<span>Download<span class="wide"> for Mac</span></span></a>
  </div>
</header>
"""


def band():
    return f"""<div class="band">
  <div class="wrap">
    <h2>Your people, without the noise.</h2>
    <a class="download calm" href="{DOWNLOAD}" data-download>{icon('i-download')}<b>Download for Mac</b><small>Free beta · for Apple Silicon Macs</small></a>
  </div>
</div>
"""


def foot():
    return f"""<footer class="site">
  <div class="wrap">
    <p class="legal"><strong>Mima Labs LTD</strong>&nbsp;is registered in England and Wales, company number 17376227<br />
      <i>36 East Stockwell Street, Colchester, Essex, CO1 1ST, England, United Kingdom</i><br />
      <a href="mailto:aloha@mima.social">aloha@mima.social</a> · <a href="/learn/">Learn</a></p>
    <p class="byline"><span>Made with</span>{icon('heart-filled')}<span>and</span>{icon('sparkle')}<span>by <a href="https://dressedforspace.com">Dressed for Space</a></span></p>
  </div>
</footer>
<script src="/learn/learn.js" defer></script>
</body>
</html>
"""


ORG = {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Mima",
       "url": f"{SITE}/", "logo": f"{SITE}/site-assets/Logo.png"}
APP = {"@type": "SoftwareApplication", "name": "Mima", "operatingSystem": "macOS",
       "applicationCategory": "SocialNetworkingApplication", "downloadUrl": DOWNLOAD,
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + url}
        for i, (name, url) in enumerate(items)]}


def crumbs_html(items):
    lis = "".join(f'<li><a href="{url}">{esc(name)}</a></li>' for name, url in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'


def entry(a, show_topic=True, show_summary=True, tag="h3"):
    meta = [f'<time datetime="{a["published_d"]}">{nice_date(a["published_d"])}</time>']
    if show_topic:
        meta.append(f'<span>{esc(a["topic"])}</span>')
    summary = f'<p>{esc(a["summary"])}</p>' if show_summary else ""
    return (f'<li class="entry"><{tag}><a href="{a["url"]}">{esc(a["title"])}</a></{tag}>'
            f'{summary}<p class="meta">{" · ".join(meta)}</p></li>')


# ---------------------------------------------------------------- pages

def index_page(topics, articles):
    latest = sorted(articles, key=lambda a: (a["published_d"], -a["order"]), reverse=True)[:LATEST_COUNT]
    shelves = []
    for t in topics:
        if not t["articles"]:
            continue
        n = len(t["articles"])
        items = "".join(
            f'<li><a href="{a["url"]}">{esc(a["title"])}</a></li>' for a in t["articles"][:SHELF_LIMIT])
        more = (f'<a class="more" href="{t["url"]}">All {n} guides<span class="sr-only"> in {esc(t["name"])}</span>{icon("arrow-right")}</a>'
                if n > SHELF_LIMIT else
                f'<a class="more quiet" href="{t["url"]}">About this topic<span class="sr-only">: {esc(t["name"])}</span>{icon("arrow-right")}</a>')
        shelves.append(f"""<section class="shelf" aria-labelledby="shelf-{t['slug']}">
      <div class="shelf-head">
        <h3 id="shelf-{t['slug']}"><a href="{t['url']}">{esc(t['name'])}</a></h3>
        <p class="count">{n} guide{'s' if n != 1 else ''}</p>
      </div>
      <ul>{items}</ul>
      {more}
    </section>""")
    desc = "Plain guides to keeping up with the people you follow on Bluesky, X, LinkedIn and Mastodon, without the algorithms, from the makers of Mima."
    ld = {"@context": "https://schema.org", "@graph": [
        ORG,
        {"@type": "CollectionPage", "@id": f"{SITE}/learn/#page", "name": "Learn", "url": f"{SITE}/learn/",
         "description": desc, "publisher": {"@id": ORG["@id"]},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(articles), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": SITE + a["url"], "name": a["title"]}
             for i, a in enumerate(sorted(articles, key=lambda a: (a["topic_obj"]["slug"], a["order"])))]}},
        crumbs_ld([("Home", "/"), ("Learn", "/learn/")]),
    ]}
    return head("Learn: guides to calmer social media · Mima", desc, "/learn/", ld,
                md_link("/learn/index.md", "Learn as Markdown")) + f"""
<main id="content">
  <section class="intro">
    <div class="wrap intro-grid">
      <div>
        <h1>Keep up with your people, not the algorithms</h1>
        <p class="lede">Plain guides to following friends, posting and keeping conversations going across Bluesky, X, LinkedIn and Mastodon, and how Mima brings it all into one calm place.</p>
        <p class="agents">For AI assistants, every guide is also published as Markdown and listed in <a href="/llms.txt">llms.txt</a>.</p>
      </div>
      <section class="latest" aria-labelledby="latest-title">
        <h2 id="latest-title">Latest guides</h2>
        <ol class="entries">{"".join(entry(a, show_summary=False) for a in latest)}</ol>
      </section>
    </div>
  </section>
  <section class="shelves" aria-labelledby="topics-title">
    <div class="wrap">
      <h2 id="topics-title">Browse by topic</h2>
      <div class="shelf-grid">
    {"".join(shelves)}
      </div>
    </div>
  </section>
</main>
{band()}{foot()}"""


def topic_page(t, topics):
    others = "".join(
        f'<li><a href="{o["url"]}"{" aria-current=\"page\"" if o is t else ""}>{esc(o["name"])}</a></li>'
        for o in topics if o["articles"])
    ld = {"@context": "https://schema.org", "@graph": [
        ORG,
        {"@type": "CollectionPage", "name": t["name"], "url": SITE + t["url"], "description": t["blurb"],
         "isPartOf": {"@id": f"{SITE}/learn/#page"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(t["articles"]), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": SITE + a["url"], "name": a["title"]}
             for i, a in enumerate(t["articles"])]}},
        crumbs_ld([("Home", "/"), ("Learn", "/learn/"), (t["name"], t["url"])]),
    ]}
    return head(f"{t['name']} · Learn · Mima", t["blurb"], t["url"], ld,
                md_link(f"/learn/topics/{t['slug']}.md", f"{t['name']} as Markdown")) + f"""
<main id="content">
  <div class="wrap topic">
    <header class="topic-head">
      {crumbs_html([("Learn", "/learn/")])}
      <h1>{esc(t['name'])}</h1>
      <p class="lede">{esc(t['blurb'])}</p>
      <p class="count">{len(t['articles'])} guide{'s' if len(t['articles']) != 1 else ''}</p>
    </header>
    <ol class="entries big">{"".join(entry(a, show_topic=False, tag="h2") for a in t["articles"])}</ol>
    <aside class="margin" aria-label="More from Learn">
      <nav class="topic-nav" aria-labelledby="topics-nav-title"><h2 id="topics-nav-title">All topics</h2><ul>{others}</ul></nav>
      <div class="mini-try">
        <p><strong>Try it in Mima.</strong> {esc(MIMA_LINE)}</p>
        <a class="btn-ink" href="{DOWNLOAD}" data-download>{icon('i-download')}Download</a>
      </div>
    </aside>
  </div>
</main>
{band()}{foot()}"""


def article_page(a, by_slug):
    t = a["topic_obj"]
    toc = "".join(
        f'<li class="l{lvl}"><a href="#{hid}">{text}</a></li>' for lvl, hid, text in a["headings"])
    toc_html = f'<nav class="toc" aria-labelledby="toc-title"><h2 id="toc-title">On this page</h2><ol>{toc}</ol></nav>' if toc else ""
    related = [by_slug[s] for s in a["related"]]
    siblings = [x for x in t["articles"] if x is not a and x not in related][:4]
    rel_html = ""
    if related:
        rel_html += f'<section aria-labelledby="related-title"><h2 id="related-title">Related guides</h2><ul class="entries">{"".join(entry(r, tag="h3") for r in related)}</ul></section>'
    if siblings:
        rel_html += (f'<section aria-labelledby="sib-title"><h2 id="sib-title">More in {esc(t["name"])}</h2>'
                     f'<ul class="entries">{"".join(entry(r, show_topic=False, tag="h3") for r in siblings)}</ul>'
                     f'<a class="more" href="{t["url"]}">All {len(t["articles"])} guides in {esc(t["name"])}{icon("arrow-right")}</a></section>')
    graph = [
        ORG,
        {"@type": "Article", "@id": f"{SITE}{a['url']}#article", "headline": a["title"],
         "description": a["summary"], "url": SITE + a["url"], "mainEntityOfPage": SITE + a["url"],
         "datePublished": str(a["published_d"]), "dateModified": str(a["updated_d"]),
         "articleSection": a["topic"], "inLanguage": "en", "timeRequired": f"PT{a['minutes']}M",
         "author": {"@id": ORG["@id"]}, "publisher": {"@id": ORG["@id"]},
         "isPartOf": {"@id": f"{SITE}/learn/#page"},
         "about": APP,
         "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": SITE + a["md_url"]}},
        crumbs_ld([("Home", "/"), ("Learn", "/learn/"), (t["name"], t["url"]), (a["title"], a["url"])]),
    ]
    if a["faq"]:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in a["faq"]]})
    note = a.get("mima") or MIMA_LINE
    extra = md_link(a["md_url"], "This guide as Markdown")
    return head(f"{a['title']} · Learn · Mima", a["summary"], a["url"],
                {"@context": "https://schema.org", "@graph": graph}, extra) + f"""
<main id="content">
  <article class="wrap art">
    <div class="art-top">
      {crumbs_html([("Learn", "/learn/"), (t["name"], t["url"])])}
      <h1>{esc(a['title'])}</h1>
      <p class="answer"><strong>In short:</strong> {esc(a['summary'])}</p>
    </div>
    <aside class="margin" aria-label="About this guide">
      <dl class="facts">
        <div><dt>Topic</dt><dd><a href="{t['url']}">{esc(t['name'])}</a></dd></div>
        <div><dt>Updated</dt><dd><time datetime="{a['updated_d']}">{nice_date(a['updated_d'])}</time></dd></div>
        <div><dt>Reading time</dt><dd>{a['minutes']} min</dd></div>
        <div><dt>Plain text</dt><dd><a href="{a['md_url']}" type="text/markdown">Markdown version</a></dd></div>
      </dl>
      {toc_html}
    </aside>
    <div class="prose">
{a['html']}
    </div>
    <section class="try" aria-labelledby="try-title">
      <h2 id="try-title">Try it in Mima</h2>
      <p>{esc(note)} One feed of the people you follow, one composer for every network, and one inbox for your conversations.</p>
      <a class="download" href="{DOWNLOAD}" data-download>{icon('i-download')}<b>Download for Mac</b><small>Free beta · for Apple Silicon Macs</small></a>
      <figure class="try-shot"><img src="/site-assets/app/feed.webp" alt="The Mima News Wall: posts from friends on Bluesky, X, LinkedIn and Mastodon in one timeline" width="1600" height="1080" loading="lazy"></figure>
    </section>
    <div class="after">{rel_html}</div>
  </article>
</main>
{foot()}"""


def md_link(path, title):
    """The <head> pointer from a page to its Markdown version, for agents and crawlers."""
    return f'<link rel="alternate" type="text/markdown" href="{SITE}{path}" title="{esc(title)}" />'


ABOUT_MIMA = ("Mima is a free desktop app (beta, Apple Silicon Macs) with one feed of the people you follow on "
              "Bluesky, X, LinkedIn and Mastodon, one composer for posting to several networks, and one inbox for "
              f"conversations. Download: {DOWNLOAD}. Overview for AI assistants: {SITE}/llms.txt")


def guide_line(a):
    return f"- [{a['title']}]({SITE}{a['md_url']}): {a['summary']} (Updated {a['updated_d']}.)"


def index_md(topics, articles):
    latest = sorted(articles, key=lambda a: (a["published_d"], -a["order"]), reverse=True)[:LATEST_COUNT]
    lines = ["# Learn: keep up with your people, not the algorithms", "",
             "> Plain guides from the makers of Mima to following friends, posting and keeping conversations going "
             "across Bluesky, X, LinkedIn and Mastodon. Each guide links to its Markdown version.", "",
             f"Source: {SITE}/learn/", "", "## Latest guides", ""] + [guide_line(a) for a in latest] + [""]
    for t in topics:
        if t["articles"]:
            lines += [f"## {t['name']}", "", t["blurb"], ""] + [guide_line(a) for a in t["articles"]] + ["",
                f"All {t['name']} guides: {SITE}/learn/topics/{t['slug']}.md", ""]
    lines += ["---", "", f"About Mima: {ABOUT_MIMA}", ""]
    return "\n".join(lines)


def topic_md(t):
    lines = [f"# {t['name']}", "", f"> {t['blurb']}", "", f"Source: {SITE}{t['url']} · Part of {SITE}/learn/index.md", ""]
    lines += [guide_line(a) for a in t["articles"]] + ["", "---", "", f"About Mima: {ABOUT_MIMA}", ""]
    return "\n".join(lines)


def article_md(a, by_slug):
    lines = [f"# {a['title']}", "", f"> {a['summary']}", "",
             f"Topic: {a['topic']} · Updated: {a['updated_d']} · Source: {SITE}{a['url']}", "",
             re.sub(r"\]\(/", f"]({SITE}/", a["body_md"].strip()), ""]
    related = [by_slug[s] for s in a["related"]]
    if related:
        lines += ["## Related guides", ""] + [f"- [{r['title']}]({SITE}{r['md_url']}): {r['summary']}" for r in related] + [""]
    lines += ["---", "",
              f"About Mima: {a.get('mima') or MIMA_LINE} Mima is a free desktop app (beta, Apple Silicon Macs) "
              "with one feed of the people you follow on Bluesky, X, LinkedIn and Mastodon, one composer for "
              f"posting to several networks, and one inbox for conversations. Download: {DOWNLOAD}. "
              f"More guides: {SITE}/learn/. Overview for AI assistants: {SITE}/llms.txt", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- crawler files

def sitemap(topics, articles):
    today = max(a["updated_d"] for a in articles)
    urls = [("/", None), ("/learn/", today)]
    urls += [(t["url"], max(a["updated_d"] for a in t["articles"])) for t in topics if t["articles"]]
    urls += [(a["url"], a["updated_d"]) for a in articles]
    rows = []
    for path, d in urls:
        lastmod = f"<lastmod>{d}</lastmod>" if d else ""
        rows.append(f"  <url><loc>{SITE}{path}</loc>{lastmod}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")


ROBOTS = f"""# mima.social: everything is public. Crawlers and AI agents are welcome.
# Guides for agents live at /learn/. Every Learn page has a Markdown version,
# linked from its <head>; start at /learn/index.md.
User-agent: *
Allow: /
Disallow: /api/

Sitemap: {SITE}/sitemap.xml
"""


def llms_section(topics):
    out = ["## Learn", "",
           f"Guides from the makers of Mima. Each is also published as Markdown at the link below; the HTML version is at the same path without `.md`. Index: {SITE}/learn/index.md", ""]
    for t in topics:
        if not t["articles"]:
            continue
        out.append(f"### {t['name']}")
        out.append("")
        out += [f"- [{a['title']}]({SITE}{a['md_url']}): {a['summary']}" for a in t["articles"]]
        out.append("")
    return "\n".join(out)


def update_llms(topics):
    path = ROOT / "llms.txt"
    text = path.read_text()
    section = llms_section(topics)
    # Replace an existing "## Learn" section (up to the next "## " heading),
    # otherwise insert it before "## Optional", which llmstxt.org keeps last.
    if re.search(r"^## Learn\s*$", text, re.M):
        text = re.sub(r"^## Learn\s*$.*?(?=^## (?!#)|\Z)", section + "\n", text, flags=re.M | re.S)
    elif "\n## Optional" in text:
        text = text.replace("\n## Optional", "\n" + section + "\n## Optional", 1)
    else:
        text = text.rstrip() + "\n\n" + section
    path.write_text(text)


# ---------------------------------------------------------------- main

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    global SPRITE, WORDMARK
    SPRITE, WORDMARK = sprite(), wordmark()
    topics = load_topics()
    articles = load_articles(topics)
    by_slug = {a["slug"]: a for a in articles}

    # Clear previously generated pages so renamed or deleted guides don't linger.
    keep = {"learn.css", "learn.js"}
    if OUT.exists():
        for p in sorted(OUT.rglob("*"), reverse=True):
            if p.is_file() and p.name not in keep:
                p.unlink()
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()

    write(OUT / "index.html", index_page(topics, articles))
    write(OUT / "index.md", index_md(topics, articles))
    for t in topics:
        if t["articles"]:
            write(OUT / "topics" / t["slug"] / "index.html", topic_page(t, topics))
            write(OUT / "topics" / f"{t['slug']}.md", topic_md(t))
    for a in articles:
        write(OUT / a["slug"] / "index.html", article_page(a, by_slug))
        write(OUT / f"{a['slug']}.md", article_md(a, by_slug))
    write(ROOT / "sitemap.xml", sitemap(topics, articles))
    write(ROOT / "robots.txt", ROBOTS)
    update_llms(topics)
    print(f"Built {len(articles)} guides in {sum(1 for t in topics if t['articles'])} topics.")


if __name__ == "__main__":
    main()
