"""Characterization tests for learn-src/build.py helpers."""

import datetime
import json
import unittest
import xml.etree.ElementTree as ET

import _paths  # noqa: F401
import build

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class FaqPairs(unittest.TestCase):
    def test_bold_question_paragraphs(self):
        body = ("Intro.\n\n## FAQ\n\n**Is it free?** Yes, *free*.\n\n"
                "**Mac only?** For now, `yes`.\n\n## Next\n\n**Not a question?** Outside the FAQ.\n")
        self.assertEqual(build.faq_pairs(body), [("Is it free?", "Yes, free."), ("Mac only?", "For now, yes.")])

    def test_h3_questions(self):
        body = "## Common questions\n\n### Is it free?\nYes.\n\n### Mac only?\nFor now.\n"
        self.assertEqual(build.faq_pairs(body), [("Is it free?", "Yes."), ("Mac only?", "For now.")])

    def test_mixed_forms_stay_separate_and_in_order(self):
        # #38: an ### answer used to swallow the **bold** question after it,
        # and the two forms were listed in separate passes, out of page order.
        body = ("## FAQ\n\n**First?** One.\n\n### Is it free?\nYes.\n\n"
                "**Mac only?** For now.\n\n### Last?\nEnd.\n")
        self.assertEqual(build.faq_pairs(body), [
            ("First?", "One."), ("Is it free?", "Yes."), ("Mac only?", "For now."), ("Last?", "End.")])

    def test_no_faq_section(self):
        self.assertEqual(build.faq_pairs("## Intro\n\n**Bold?** Not a FAQ.\n"), [])


class Sitemap(unittest.TestCase):
    def test_valid_xml_with_expected_urls(self):
        a1 = {"url": "/learn/one/", "updated_d": datetime.date(2026, 3, 1)}
        a2 = {"url": "/learn/two/", "updated_d": datetime.date(2026, 4, 2)}
        topics = [{"url": "/learn/topics/posting/", "articles": [a1, a2]},
                  {"url": "/learn/topics/empty/", "articles": []}]
        root = ET.fromstring(build.sitemap(topics, [a1, a2]))
        rows = [(u.find("s:loc", NS).text, getattr(u.find("s:lastmod", NS), "text", None))
                for u in root.findall("s:url", NS)]
        self.assertEqual(rows, [
            ("https://www.mima.social/", None),
            ("https://www.mima.social/learn/", "2026-04-02"),
            ("https://www.mima.social/learn/topics/posting/", "2026-04-02"),
            ("https://www.mima.social/learn/one/", "2026-03-01"),
            ("https://www.mima.social/learn/two/", "2026-04-02"),
        ])


class CrumbsLd(unittest.TestCase):
    def test_breadcrumb_list_is_valid_json_ld(self):
        ld = json.loads(json.dumps(build.crumbs_ld([("Learn", "/learn/"), ("Guide", "/learn/g/")])))
        self.assertEqual(ld["@type"], "BreadcrumbList")
        self.assertEqual(ld["itemListElement"], [
            {"@type": "ListItem", "position": 1, "name": "Learn", "item": "https://www.mima.social/learn/"},
            {"@type": "ListItem", "position": 2, "name": "Guide", "item": "https://www.mima.social/learn/g/"},
        ])


if __name__ == "__main__":
    unittest.main()
