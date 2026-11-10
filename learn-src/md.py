"""A small Markdown-to-HTML converter, standard library only.

It covers what the Learn articles use: front matter, headings (with ids),
paragraphs, ordered and unordered lists (one level of nesting), blockquotes,
fenced code, tables, horizontal rules, figures (an image alone on its line,
with an optional "caption" title), and the inline forms **bold**,
*italic*, `code`, [links](url) and ![images](src). Raw HTML lines pass
through unchanged. Anything fancier belongs in raw HTML in the article.
"""

import html
import re

_SLUG_STRIP = re.compile(r"[^a-z0-9\s-]")


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = _SLUG_STRIP.sub("", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def front_matter(source):
    """Split `---` front matter (flat `key: value` lines) from the body."""
    meta = {}
    if source.startswith("---\n"):
        head, _, source = source[4:].partition("\n---\n")
        for line in head.splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                key, _, value = line.partition(":")
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                meta[key.strip()] = value
    return meta, source.lstrip("\n")


def inline(text):
    """Escape text, then apply inline Markdown."""
    codes = []

    def keep_code(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def _table(rows):
    def cells(row):
        return [c.strip() for c in row.strip().strip("|").split("|")]

    head = cells(rows[0])
    aligns = []
    for spec in cells(rows[1]):
        aligns.append("right" if spec.endswith(":") and not spec.startswith(":") else "")
    wide = " wide" if len(head) > 4 else ""  # many columns: scroll sideways, first column pinned
    out = [f'<div class="table-wrap{wide}" tabindex="0" role="region" aria-label="Table, scrolls sideways"><table>' if wide else '<div class="table-wrap"><table>', "<thead><tr>"]
    for i, c in enumerate(head):
        style = f' class="num"' if i < len(aligns) and aligns[i] == "right" else ""
        out.append(f'<th scope="col"{style}>{inline(c)}</th>')
    out.append("</tr></thead><tbody>")
    for row in rows[2:]:
        out.append("<tr>")
        for i, c in enumerate(cells(row)):
            style = f' class="num"' if i < len(aligns) and aligns[i] == "right" else ""
            out.append(f"<td{style}>{inline(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


_LIST = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)")


def _list(lines):
    """Render a run of list lines, nesting items indented by 2+ spaces."""
    out, stack = [], []  # stack of (indent, tag)
    for line in lines:
        m = _LIST.match(line)
        if not m:  # continuation line
            out[-1] = out[-1] + " " + inline(line.strip())
            continue
        indent, marker, text = len(m.group(1)), m.group(2), m.group(3)
        tag = "ol" if marker[0].isdigit() else "ul"
        if not stack or indent > stack[-1][0]:
            out.append(f"<{tag}>")
            stack.append((indent, tag))
        else:
            while stack and indent < stack[-1][0]:
                out.append(f"</li></{stack.pop()[1]}>")
            out.append("</li>")
        out.append(f"<li>{inline(text)}")
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def to_html(body):
    """Convert Markdown to HTML. Returns (html, headings) where headings is
    a list of (level, id, text) for h2 and h3, for a table of contents."""
    lines = body.splitlines()
    out, headings, used = [], [], set()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*(?:\{#([\w-]+)\})?$", stripped)
        if m:
            level, text = len(m.group(1)), m.group(2)
            hid = m.group(3) or slugify(text)
            base, n = hid, 2
            while hid in used:
                hid, n = f"{base}-{n}", n + 1
            used.add(hid)
            if level in (2, 3):
                headings.append((level, hid, inline(text)))
            out.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            out.append("<hr>")
            i += 1
            continue
        fig = re.match(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)$', stripped)
        if fig:
            alt, src, cap = fig.group(1), fig.group(2), fig.group(3)
            caption = f"<figcaption>{inline(cap)}</figcaption>" if cap else ""
            out.append(f'<figure><img src="{src}" alt="{html.escape(alt)}" loading="lazy">{caption}</figure>')
            i += 1
            continue
        if stripped.startswith("<"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue
        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].lstrip())
                i += 1
            inner, _ = to_html("\n".join(quote))
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_table(rows))
            continue
        if _LIST.match(line):
            items = []
            while i < len(lines) and lines[i].strip() and (_LIST.match(lines[i]) or lines[i].startswith("  ")):
                items.append(lines[i])
                i += 1
            out.append(_list(items))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|>|\||<)", lines[i].strip()) and not _LIST.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out), headings
