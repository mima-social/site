#!/usr/bin/env python3
"""Generate the dummy Mima app pages in this folder from fake content.

Run `python3 app-shots/build.py`, then `sh app-shots/render.sh` to turn them
into the screenshots the site uses. Everything here is fictional: no real
people, handles or posts. Keep the markup in step with mima-social/desktop
(see README.md).
"""

import pathlib

HERE = pathlib.Path(__file__).parent
AV = "../assets/avatars/a{}.png"
ME = "../assets/plates/thread-avatar.png"
THUMB = "../assets/plates/link-thumb.png"
PH = "../assets/posts/{}.webp"

WORDMARK = (HERE.parent / "site-assets" / "wordmark-path.txt").read_text().strip()


def icon(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="icons.svg#{name}"/></svg>'


def glyph(net):
    # Name-row and list glyphs are the outline mark in ink, not brand colour.
    return icon(net, "g")


def page(title, body, composer=None):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} (Mima dummy view)</title>
<link rel="stylesheet" href="app.css">
</head>
<body>
<header class="titlebar">
  <div class="lights"><span></span><span></span><span></span></div>
  <svg class="wordmark" viewBox="0 0 108 52" fill="currentColor" aria-label="Mima"><path d="{WORDMARK}"/></svg>
  <span class="version">v0.2.0</span>
  <nav class="nav">
    <a class="{'on' if title.startswith('News') else ''}">{icon('megaphone')}News</a>
    <a class="{'on' if title.startswith('Conv') else ''}">{icon('messages')}Conversations<span class="badge">4</span></a>
  </nav>
  <div class="right">{icon('moon')}<span>Settings</span></div>
</header>
<main>
{body}
</main>
{composer or composer_html()}
</body>
</html>
"""


def composer_html(text="", nets=()):
    filled = bool(text)
    toggles = "".join(
        f'<span class="tg {"on " + n + "-c" if n in nets else ""}">{icon("s-" + n)}</span>'
        for n in ("bluesky", "x", "mastodon", "linkedin")
    )
    return f"""<footer class="composer">
  <div class="in">
    <div class="ta {'filled' if filled else ''}">{text or "What's on your mind?"}</div>
    <span class="img">{icon('image')}</span>
    <span class="btn-acc post-btn {'ready' if filled else ''}">Post</span>
  </div>
  <div class="net">
    <div class="toggles">{toggles}</div>
    <span class="hint"><kbd>⌘</kbd> + <kbd>Enter</kbd> to post</span>
  </div>
</footer>"""


def news_head(view="Timeline"):
    pills = '<span class="pill on">All</span>' + "".join(
        f'<span class="pill"><span class="{n}">{icon("s-" + n)}</span></span>'
        for n in ("bluesky", "x", "linkedin", "mastodon")
    )
    seg = "".join(f'<span class="{"on" if v == view else ""}">{v}</span>' for v in ("Timeline", "Board"))
    return f"""<div class="head">
  <h1 class="type-h2">News Wall</h1>
  <div class="ctrls">
    <div class="pills">{pills}</div>
    <div class="seg">{seg}</div>
    <span class="select">Newest{icon('chevron-down')}</span>
    <span class="reload">{icon('reload')}</span>
  </div>
</div>"""


def post(av, name, nets, handle, time, body, link=None, counts=(0, 0, 0), liked=False, reshare=None, wrap=True, photo=None):
    glyphs = "".join(glyph(n) for n in nets)
    meta = [] if len(nets) > 1 else [f"<span>@{handle}</span>", "<span>·</span>"]
    meta.append(f"<span>{time}</span>")
    if reshare:
        meta.append(f'<span>·</span><span class="rs">reshared by</span><span>@{reshare}</span>')
    card = ""
    if link:
        dom, ttl, desc, img = link
        thumb = f'<div class="thumb"><img src="{img}" alt=""></div>' if img else ""
        card = f'<div class="card-link">{thumb}<div class="tx"><div class="dom">{dom}</div><div class="ttl">{ttl}</div><div class="desc">{desc}</div></div></div>'
    c, r, l = counts
    actions = f"""<div class="actions">
    <span>{icon('comments')}<b>{c}</b></span><span>{icon('repeat')}<b>{r}</b></span>
    <span class="{'liked' if liked else ''}">{icon('heart-filled' if liked else 'heart')}<b>{l}</b></span><span>{icon('share')}</span>
  </div>"""
    return f"""<article class="post">
  <div class="hd"><img class="av" src="{av}" alt="">
    <div><div class="name-row">{name}<span class="glyphs">{glyphs}</span></div><div class="meta">{''.join(meta)}</div></div>
  </div>
  <p class="body">{body}</p>{card}{f'<img class="photo" src="{photo}" alt="">' if photo else ""}
  {actions}
</article>"""


# ---------------------------------------------------------------- content
P_INES = dict(av=AV.format(0), name="Ines Okafor", nets=["bluesky"], handle="ines.okafor.example", time="12m ago",
              body="Finished the zine! 40 copies, risograph, two colours.\nSwapping them at the Saturday market if anyone wants one.",
              counts=(8, 14, 96), liked=True, photo=PH.format("zine"))
P_DEV = dict(av=AV.format(2), name="Dev Raman", nets=["mastodon"], handle="dev@social.example", time="26m ago",
             reshare="mira@art.example 9m ago",
             body="Wrote up how we cut our app's cold start in half. Mostly by deleting things.",
             link=("devraman.example", "Half the cold start, none of the magic",
                   "What we removed, what we measured, and the one cache we kept.", THUMB),
             counts=(3, 21, 140))
P_MARISOL = dict(av=AV.format(6), name="Marisol Vega", nets=["linkedin"], handle="marisol-vega-studio", time="41m ago",
                 body="Twelve years in, I finally took a sabbatical. Week one: I didn't open a single dashboard. Week two: I learned to make tortillas.",
                 counts=(12, 4, 230), photo=PH.format("tortillas"))
P_BOT = dict(av=AV.format(5), name="Pixel Bot", nets=["x"], handle="pixelbot_demo", time="1h ago",
             body="Today's tiny robot waters the plants. Tomorrow: he repots them.", counts=(2, 9, 61), photo=PH.format("robot"))
P_BEA = dict(av=AV.format(4), name="Bea Lindqvist", nets=["bluesky"], handle="bea.lindqvist.example", time="1h ago",
             body="New mix is up. Two hours of rainy-day jazz for anyone else working through the weekend.",
             counts=(5, 11, 88), photo=PH.format("vinyl"))
P_CAM = dict(av=AV.format(7), name="camerawork", nets=["mastodon"], handle="camerawork@photo.example", time="2h ago",
             body="Shot a whole roll at the harbour this morning. Developing tonight, fingers crossed.",
             counts=(4, 2, 57), photo=PH.format("harbour"))
P_MOCHI = dict(av=AV.format(1), name="Mochi the cat", nets=["x"], handle="mochi_naps_demo", time="3h ago",
               body="Day 412 of sitting on the keyboard. Productivity in this household remains at zero.",
               counts=(19, 40, 512), liked=True, photo=PH.format("cat"))
P_JUNO = dict(av=AV.format(4), name="Juno Park", nets=["x"], handle="junopark_demo", time="2h ago",
              body="Hot take: the best feature of any app is the off switch.", counts=(31, 12, 402))
P_TOMAS = dict(av=AV.format(2), name="Tomás Ruiz", nets=["bluesky"], handle="tomas.ruiz.example", time="2h ago",
               body="Thursday launch party is ON. Doors at 7, bring friends, bring zines.", counts=(9, 6, 74))
P_LEE = dict(av=AV.format(3), name="leafy", nets=["mastodon"], handle="leafy@plants.example", time="3h ago",
             body="Monstera put out a new leaf overnight. I am unreasonably proud.", counts=(6, 3, 120), liked=True)
P_PRIYA = dict(av=AV.format(6), name="Marisol Vega", nets=["linkedin"], handle="marisol-vega-studio", time="4h ago",
               body="Hiring a part-time illustrator for a community garden map. Small budget, big heart. DMs open.",
               counts=(14, 22, 96))
P_ME = dict(av=ME, name="Rosa Lin", nets=["bluesky", "x", "mastodon", "linkedin"], handle="", time="just now",
            body="Launch day! Mima is out for Mac: one feed for everyone I follow, one inbox for every conversation, no algorithm.",
            counts=(0, 0, 0))

feed = page("News Wall", news_head("Timeline") + '\n<div class="feed">' +
            "".join(post(**p) for p in (P_INES, P_DEV, P_MARISOL)) + "</div>")


def tile(p, label="View post"):
    return f'<div class="tile"><span class="vt">{icon("comments")}{label}</span>{post(**p)}</div>'


BOARD_BODY = news_head("Board") + f"""
<div class="board">
  <div class="col">{tile(P_INES, "View thread")}{tile(P_JUNO)}</div>
  <div class="col">{tile(P_MOCHI)}{tile(P_TOMAS)}</div>
  <div class="col">{tile(P_LEE)}{tile(P_MARISOL)}</div>
  <div class="col">{tile(P_BEA)}{tile(P_BOT)}</div>
</div>"""
board = page("News Wall", BOARD_BODY)

# A tall timeline strip; the site scrolls it inside a static window frame.
TL = (P_INES, P_DEV, P_JUNO, P_MARISOL, P_BOT, P_LEE, P_BEA, P_TOMAS, P_CAM, P_PRIYA, P_MOCHI)
timeline_strip = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="app.css"></head>
<body class="strip"><div class="feed">{''.join(post(**p) for p in TL)}</div></body></html>"""

ALL_NETS = ("bluesky", "x", "mastodon", "linkedin")
# The site types the words into this empty composer (see launch.js).
compose = page("News Wall", BOARD_BODY, composer=composer_html("&nbsp;", nets=ALL_NETS))
# Phone frame has the words baked in (no typing overlay at that size).
compose_typed = page("News Wall", BOARD_BODY, composer=composer_html("Big news: our garden map is live!", nets=ALL_NETS))


SPARKLE = '<svg class="sparkle" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.3005 9.3005L12 3.5538L14.6995 9.3005L20.4462 12L14.6995 14.6996L12 20.4463L9.3005 14.6996L3.5537 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def row(av, name, net, vis, time, preview, you=False, cls="", pin=False, count=None, reminder=False, group=None, ai=False):
    who = f'<div class="grp"><img src="{group[0]}" alt=""><img src="{group[1]}" alt=""></div>' if group else f'<img class="av" src="{av}" alt="">'
    rem = icon("reminder", "rem") if reminder else ""
    right = icon("pin", "pin") if pin else (f'<span class="count">{count}</span>' if count else "")
    pv = SPARKLE + preview if ai else (f"<b>You:</b> {preview}" if you else preview)
    return f"""<div class="row {cls}">{who}
  <div class="tx"><div class="l1">{rem}<span class="nm">{name}</span>{glyph(net)}<span class="vis">({vis})</span><span class="t">{time}</span></div>
  <div class="l2{' ai' if ai else ''}">{pv}</div></div>{right}
</div>"""


conv_head = f"""<div class="conv-head">
  <h1 class="type-h2">Conversations</h1>
  <div class="ctrls">
    <div class="pills"><span class="pill on">All</span>{''.join(f'<span class="pill"><span class="{n}">{icon("s-" + n)}</span></span>' for n in ("bluesky", "x", "linkedin", "mastodon"))}</div>
    <div class="seg slim"><span class="on">All</span><span>Public</span><span>Private</span></div>
    <div class="seg slim"><span class="on">All</span><span>Unread</span></div>
  </div>
</div>"""

ROWS = [
    row(AV.format(4), "Juno Park", "x", "private", "23h ago", "Ship it!", you=True, cls="pinned", pin=True),
    row(AV.format(2), "Tomás Ruiz", "bluesky", "private", "7m ago", "Are you coming Thursday? I saved you a seat", cls="unread", count=2),
    row(AV.format(6), "Marisol Vega", "linkedin", "private", "29m ago", "Let's pick this up after my sabbatical!", you=True, reminder=True),
    row(None, "You & Dev Raman", "mastodon", "public", "1h ago", "This is the best write-up I've read all week", you=True, group=(ME, AV.format(2))),
    row(AV.format(1), "Mochi the cat", "x", "private", "3h ago", "I'm stealing your avatar idea", you=True),
    row(AV.format(7), "camerawork", "mastodon", "private", "4h ago", "Sending you the scans tonight"),
    row(AV.format(5), "Pixel Bot", "bluesky", "public", "5h ago", "more robots please", you=True),
]
conversations = page("Conversations", conv_head + '\n<div class="rows">' + "".join(ROWS) + "</div>")


def msg(text, time, self=False):
    av, who = (ME, "rosalin") if self else (AV.format(2), "Tomás Ruiz")
    return f"""<div class="msg {'self' if self else ''}"><img class="av sm" src="{av}" alt="">
  <div class="bubble"><div class="mm"><b>{who}</b><span>· {time}</span>{icon('link')}</div><div class="mt">{text}</div></div></div>"""


thread = page("Conversations", conv_head + '\n<div class="rows">' + "".join(ROWS) + f"""</div>
<div class="scrim"><div class="dialog">
  <div class="dh"><img class="av" src="{AV.format(2)}" alt="">
    <div><div class="ttl">Tomás Ruiz</div><span class="tag">bluesky</span><span class="vis">(private)</span></div>
    {icon('close', 'x')}
  </div>
  <div class="msgs">
    {msg("Hey! Are you coming to the launch thing on Thursday?", "1d ago")}
    {msg("Wouldn't miss it. What time?", "1d ago", self=True)}
    {msg("Doors at 7. I saved you a seat near the front", "20m ago")}
    {msg("Bring a copy of Ines's zine if you have one!", "7m ago")}
  </div>
  <div class="df"><div class="reply">Type a reply...</div><span class="img">{icon('image')}</span><span class="btn-acc">Reply</span></div>
</div></div>""")

SUM_ROWS = [
    row(None, "Launch party crew", "bluesky", "private", "4m ago",
        "Ines and Tomás confirmed Thursday at 7; Juno still needs someone for the door.", cls="unread", count=26, ai=True,
        group=(AV.format(0), AV.format(2))),
] + ROWS[1:]


def gmsg(av, who, text, time):
    return f"""<div class="msg"><img class="av sm" src="{av}" alt="">
  <div class="bubble"><div class="mm"><b>{who}</b><span>· {time}</span>{icon('link')}</div><div class="mt">{text}</div></div></div>"""


summary = page("Conversations", conv_head.replace('class="conv-head"', 'class="conv-head"') + '\n<div class="rows">' + "".join(SUM_ROWS) + f"""</div>
<div class="scrim"><div class="dialog">
  <div class="dh"><div class="grp"><img src="{AV.format(0)}" alt=""><img src="{AV.format(2)}" alt=""></div>
    <div><div class="ttl">Launch party crew</div><span class="tag">bluesky</span><span class="vis">(private)</span></div>
    {icon('close', 'x')}
  </div>
  <div class="catchup">
    <div class="ch"><h3><span class="tri">▼</span>Catch up on this conversation</h3><span class="dismiss">Dismiss</span></div>
    <p class="type-system">{SPARKLE}The launch party is Thursday, doors at 7, and Ines is bringing zines <span class="ref">→</span>.</p>
    <p class="type-system">Juno has snacks covered and needs someone on the door <span class="ref">→</span>.</p>
  </div>
  <div class="msgs">
    {gmsg(AV.format(4), "Juno Park", "Snacks are mine. Also: we need someone on the door.", "6m ago")}
    {gmsg(AV.format(0), "Ines Okafor", "I can do the first hour if someone takes over after!", "4m ago")}
  </div>
  <div class="df"><div class="reply">Type a reply...</div><span class="img">{icon('image')}</span><span class="btn-acc">Reply</span></div>
</div></div>""")

# Close-up of the same dialog on its own, for the site's AI section.
dlg = summary[summary.index('<div class="dialog">'):summary.rindex('</div></div>')] + "</div>"
summary_card = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="app.css"></head>
<body class="card-only">{dlg}</body></html>"""

for name, html in {"summary-card": summary_card, "summary": summary, "timeline-strip": timeline_strip, "feed": feed, "board": board, "compose": compose, "compose-typed": compose_typed, "conversations": conversations, "thread": thread}.items():
    (HERE / f"{name}.html").write_text(html)
    print("wrote", f"app-shots/{name}.html")
