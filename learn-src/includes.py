"""Shared partials: text written once and included in several pages.

A line that holds only `<!-- include: name -->` is replaced by the text of
`<folder>/name.md` (plain Markdown, no front matter). Expand a page's body
before anything else reads it, so the HTML page, the Markdown copy, heading
ids and FAQ data all see the real text.

Rules: a missing partial is an error that names the file, never a blank. A
partial cannot include another. A name is lowercase letters, digits and
hyphens. A directive inside a code fence is left as written.
"""

import re

_DIRECTIVE = re.compile(r"^<!--\s*include:\s*(.*?)\s*-->$")
_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class IncludeError(ValueError):
    """An include directive that cannot be expanded."""


def _directives(text):
    """Yield (line index, name) for each include directive outside code fences."""
    fenced = False
    for i, line in enumerate(text.split("\n")):
        stripped = line.strip()
        if stripped.startswith("```"):
            fenced = not fenced
        elif not fenced:
            m = _DIRECTIVE.match(stripped)
            if m:
                yield i, m.group(1)


def expand(body, folder):
    """Return `body` with each include directive replaced by its partial."""
    lines = body.split("\n")
    for i, name in _directives(body):
        if not _NAME.match(name):
            raise IncludeError(f"include name `{name}` must be lowercase letters, digits and hyphens")
        path = folder / f"{name}.md"
        where = f"{folder.name}/{path.name}"
        if not path.is_file():
            raise IncludeError(f"included partial `{where}` not found (looked in {folder})")
        text = path.read_text()
        if any(_directives(text)):
            raise IncludeError(f"partial `{where}` has an include of its own; partials cannot nest")
        lines[i] = text.strip("\n")
    return "\n".join(lines)
