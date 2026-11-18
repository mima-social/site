"""Characterization tests for tools/submit_pages.py."""

import unittest

import _paths  # noqa: F401
import submit_pages


class Parse(unittest.TestCase):
    def test_urls_with_and_without_lastmod(self):
        xml = ('<urlset>\n  <url><loc>https://www.mima.social/</loc></url>\n'
               '  <url><loc> https://www.mima.social/learn/ </loc><lastmod>2026-04-02</lastmod></url>\n'
               '  <url><lastmod>2026-01-01</lastmod></url>\n</urlset>')
        self.assertEqual(submit_pages.parse(xml), {"https://www.mima.social/": "",
                                                   "https://www.mima.social/learn/": "2026-04-02"})

    def test_empty_or_missing_sitemap(self):
        self.assertEqual(submit_pages.parse(""), {})
        self.assertEqual(submit_pages.parse(None), {})


if __name__ == "__main__":
    unittest.main()
