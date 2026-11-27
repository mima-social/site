"""Tests for shared partials: `<!-- include: name -->` in a Learn article (#51).

They drive the builder (`build.load_articles`, then `article_page` and
`article_md`) on a temporary tree, so they check what a reader gets.
"""

import json
import pathlib
import tempfile
import unittest
from unittest import mock

import _paths  # noqa: F401
import build

FRONT = "---\ntitle: T\nslug: {slug}\nsummary: S\ntopic: Agents\nupdated: 2026-11-27\n---\n\n"


class Includes(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        self.src = root / "learn-src"
        self.partials = root / "content" / "partials"
        (self.src / "articles").mkdir(parents=True)
        self.partials.mkdir(parents=True)
        (self.src / "topics.json").write_text(json.dumps([{"name": "Agents", "slug": "agents", "blurb": "B"}]))
        for patch in (mock.patch.object(build, "HERE", self.src),
                      mock.patch.object(build, "PARTIALS", self.partials, create=True)):
            patch.start()
            self.addCleanup(patch.stop)

    def article(self, body, slug="one"):
        (self.src / "articles" / f"{slug}.md").write_text(FRONT.format(slug=slug) + body)

    def partial(self, name, text):
        (self.partials / f"{name}.md").write_text(text)

    def load(self):
        articles = build.load_articles(build.load_topics())
        return articles, {a["slug"]: a for a in articles}

    def test_expands_in_the_html_page_and_the_markdown_copy(self):
        self.partial("steps", "1. Open **Settings**.\n2. See [home](/).\n")
        self.article("Intro.\n\n## How\n\n<!-- include: steps -->\n\n## After\n\nEnd.\n")
        articles, by_slug = self.load()
        page = build.article_page(articles[0], by_slug)
        text = build.article_md(articles[0], by_slug)
        self.assertIn('<ol><li>Open <strong>Settings</strong>.</li><li>See <a href="/">home</a>.</li></ol>', page)
        self.assertIn("1. Open **Settings**.\n2. See [home](https://www.mima.social/).", text)
        self.assertNotIn("<!-- include", page)
        self.assertNotIn("<!-- include", text)

    def test_expanded_body_equals_the_same_text_written_inline(self):
        # What keeps a page byte-identical when its text moves into a partial:
        # the partial's trailing newline must not add or remove a blank line.
        self.partial("steps", "First.\n\nLast.\n")
        self.article("## How\n\n<!-- include: steps -->\n\n## After\n\nEnd.\n", slug="one")
        self.article("## How\n\nFirst.\n\nLast.\n\n## After\n\nEnd.\n", slug="two")
        _, by_slug = self.load()
        self.assertEqual(by_slug["one"]["body_md"], by_slug["two"]["body_md"])
        self.assertEqual(by_slug["one"]["html"], by_slug["two"]["html"])

    def test_one_partial_can_be_included_by_two_articles(self):
        self.partial("steps", "Shared words.\n")
        self.article("<!-- include: steps -->\n", slug="one")
        self.article("Before.\n\n<!-- include: steps -->\n", slug="two")
        _, by_slug = self.load()
        self.assertIn("<p>Shared words.</p>", by_slug["one"]["html"])
        self.assertIn("<p>Shared words.</p>", by_slug["two"]["html"])

    def test_heading_inside_a_partial_gets_its_id_and_a_contents_entry(self):
        self.partial("steps", "### Inside the partial\n\nText.\n")
        self.article("## How\n\n<!-- include: steps -->\n")
        articles, by_slug = self.load()
        self.assertIn((3, "inside-the-partial", "Inside the partial"), articles[0]["headings"])
        page = build.article_page(articles[0], by_slug)
        self.assertIn('<h3 id="inside-the-partial">Inside the partial</h3>', page)
        self.assertIn('<a href="#inside-the-partial">', page)

    def test_faq_inside_a_partial_becomes_faq_data(self):
        self.partial("faq", "## FAQ\n\n**Is it free?** Yes.\n")
        self.article("Intro.\n\n<!-- include: faq -->\n")
        articles, by_slug = self.load()
        self.assertEqual(articles[0]["faq"], [("Is it free?", "Yes.")])
        self.assertIn('"@type": "FAQPage"', build.article_page(articles[0], by_slug))

    def test_missing_partial_fails_the_build_and_names_both_files(self):
        self.article("<!-- include: nope -->\n")
        with self.assertRaises(SystemExit) as stop:
            self.load()
        self.assertIn("one.md", str(stop.exception))
        self.assertIn("nope.md", str(stop.exception))

    def test_include_inside_a_partial_fails_the_build(self):
        self.partial("inner", "Inner.\n")
        self.partial("outer", "Outer.\n\n<!-- include: inner -->\n")
        self.article("<!-- include: outer -->\n")
        with self.assertRaises(SystemExit) as stop:
            self.load()
        self.assertIn("outer.md", str(stop.exception))

    def test_name_that_is_a_path_fails_the_build(self):
        (self.partials.parent / "secret.md").write_text("Secret.\n")
        self.article("<!-- include: ../secret -->\n")
        with self.assertRaises(SystemExit) as stop:
            self.load()
        self.assertIn("../secret", str(stop.exception))

    def test_only_a_directive_alone_on_its_line_outside_code_expands(self):
        # A guard: this passes without include support too.
        self.partial("steps", "Shared words.\n")
        self.article("Write `<!-- include: steps -->` on its own line.\n\n"
                     "```\n<!-- include: steps -->\n```\n")
        articles, _ = self.load()
        self.assertNotIn("Shared words.", articles[0]["html"])
        self.assertIn("&lt;!-- include: steps --&gt;", articles[0]["html"])


class SharedHowTo(unittest.TestCase):
    """The repo's own partial: the agent-setup steps, written once."""

    def test_mcp_article_includes_the_shared_how_to(self):
        root = _paths.ROOT
        partial = root / "content" / "partials" / "connect-agent-howto.md"
        self.assertTrue(partial.is_file(), "content/partials/connect-agent-howto.md is missing")
        article = (root / "learn-src" / "articles" / "04-mcp-server-bluesky-x-linkedin-mastodon.md").read_text()
        self.assertIn("\n<!-- include: connect-agent-howto -->\n", article)
        self.assertIn("Connect to Claude Desktop", partial.read_text())


if __name__ == "__main__":
    unittest.main()
