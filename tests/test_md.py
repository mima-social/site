"""Characterization tests for learn-src/md.py, the Markdown step behind every
Learn page. They pin today's output; change them only on purpose."""

import unittest

import _paths  # noqa: F401
import md


class Slugify(unittest.TestCase):
    def test_lowercases_strips_tags_and_punctuation(self):
        self.assertEqual(md.slugify("Hello, <em>World</em> -- 2026!"), "hello-world-2026")

    def test_collapses_spaces_and_hyphens(self):
        self.assertEqual(md.slugify("  Cross-post   to  - Bluesky  "), "cross-post-to-bluesky")


class FrontMatter(unittest.TestCase):
    def test_splits_flat_keys_from_body(self):
        meta, body = md.front_matter('---\ntitle: "Hi: there"\n# note: skipped\nslug: hi\n---\n\nBody\n')
        self.assertEqual(meta, {"title": "Hi: there", "slug": "hi"})
        self.assertEqual(body, "Body\n")

    def test_no_front_matter(self):
        self.assertEqual(md.front_matter("Just text\n"), ({}, "Just text\n"))


class Inline(unittest.TestCase):
    def test_link(self):
        self.assertEqual(md.inline("See [docs](https://x.io)."), 'See <a href="https://x.io">docs</a>.')

    def test_code_is_escaped_and_not_formatted(self):
        self.assertEqual(md.inline("`a<b> **x**`"), "<code>a&lt;b&gt; **x**</code>")

    def test_emphasis(self):
        self.assertEqual(md.inline("**bold** and *it*"), "<strong>bold</strong> and <em>it</em>")

    def test_lone_asterisks_and_html_are_left_as_text(self):
        self.assertEqual(md.inline("2*3*4 & <tag>"), "2*3*4 &amp; &lt;tag&gt;")


class ToHtml(unittest.TestCase):
    def test_table_with_right_aligned_column(self):
        out, headings = md.to_html("| A | B |\n|---|--:|\n| 1 | 2 |")
        self.assertEqual(out, '<div class="table-wrap"><table><thead><tr><th scope="col">A</th>'
                              '<th scope="col" class="num">B</th></tr></thead><tbody><tr><td>1</td>'
                              '<td class="num">2</td></tr></tbody></table></div>')
        self.assertEqual(headings, [])

    def test_wide_table_scrolls(self):
        out, _ = md.to_html("| a | b | c | d | e |\n|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 |")
        self.assertTrue(out.startswith('<div class="table-wrap wide" tabindex="0" role="region"'))

    def test_nested_list(self):
        out, _ = md.to_html("- one\n- two\n  - nested")
        self.assertEqual(out, "<ul><li>one</li><li>two<ul><li>nested</li></ul></li></ul>")

    def test_ordered_list(self):
        out, _ = md.to_html("1. first\n2. second")
        self.assertEqual(out, "<ol><li>first</li><li>second</li></ol>")

    def test_heading_ids_are_unique_and_collected(self):
        out, headings = md.to_html("## Intro\n\n## Intro\n\n### Sub {#custom}")
        self.assertEqual(out, '<h2 id="intro">Intro</h2>\n<h2 id="intro-2">Intro</h2>\n<h3 id="custom">Sub</h3>')
        self.assertEqual(headings, [(2, "intro", "Intro"), (2, "intro-2", "Intro"), (3, "custom", "Sub")])


if __name__ == "__main__":
    unittest.main()
