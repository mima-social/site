"""Unit tests for labs-src/labs.py, the Labs (blog) build, and for the hooks
it uses in learn-src/build.py and md.py."""

import datetime
import json
import re
import unittest
import xml.etree.ElementTree as ET

import _paths
import build
import labs
import md

ROOT = _paths.ROOT
ATOM = {"a": "http://www.w3.org/2005/Atom"}
AUTHORS = {
    "ada": {"id": "ada", "name": "Ada Example", "role": "Engineer", "url": "https://ada.example/", "photo": "/site-assets/authors/ada.webp"},
    "bo": {"id": "bo", "name": "Bo", "role": "Designer", "url": "", "photo": ""},
}
CATEGORIES = {"Engineering": {"name": "Engineering", "slug": "engineering"}}


def post(slug="one", extra="", body="Hello.\n", author="ada"):
    source = (f"---\ntitle: Post {slug}\nslug: {slug}\ndeck: About {slug} & more.\ncategory: Engineering\n"
              f"date: 2026-03-01\nauthor: {author}\n{extra}---\n\n{body}")
    return labs.load_post(source, f"{slug}.md", AUTHORS, CATEGORIES)


class ImageSize(unittest.TestCase):
    def test_webp_png_and_jpeg(self):
        self.assertEqual(labs.image_size(ROOT / "site-assets/app/board.webp"), (1920, 1296))
        self.assertEqual(labs.image_size(ROOT / "site-assets/Logo.png"), (834, 550))
        self.assertEqual(labs.image_size(ROOT / "site-assets/og/learn.jpg"), (2400, 1260))

    def test_other_files_are_refused(self):
        with self.assertRaises(ValueError):
            labs.image_size(ROOT / "robots.txt")


class Refs(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(labs.parse_refs("site#44, desktop#2318"), [("site", 44), ("desktop", 2318)])
        self.assertEqual(labs.parse_refs(""), [])
        self.assertEqual(labs.parse_refs(None), [])

    def test_bad_ref(self):
        with self.assertRaises(ValueError):
            labs.parse_refs("#44")

    def test_only_known_public_repos_are_linked(self):
        self.assertEqual(labs.ref_html("site", 44),
                         '<a href="https://github.com/mima-social/site/issues/44">site#44</a>')
        self.assertEqual(labs.ref_html("desktop", 7), "desktop#7")


class Callouts(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(labs.parse_callout("44 13 from 30.5 0 | Network filters"),
                         {"to": (44.0, 13.0), "from": (30.5, 0.0), "text": "Network filters"})

    def test_bad_shapes(self):
        for text in ("44 13 | No disc", "44 13 from 30 0", "144 13 from 30 0 | Off the figure"):
            with self.assertRaises(ValueError):
                labs.parse_callout(text)

    def test_path_runs_from_disc_to_target(self):
        d = labs.callout_path((0, 0), (100, 0))
        self.assertTrue(d.startswith("M0.0 0.0 C "))
        self.assertTrue(d.endswith(", 100.0 0.0"))
        # The two control points sit on opposite sides of the line: an S-curve.
        ys = [float(n) for n in re.findall(r"-?\d+\.\d", d)][3::2][:2]
        self.assertLess(ys[0] * ys[1], 0)

    def test_zero_length_path_does_not_divide_by_zero(self):
        self.assertTrue(labs.callout_path((5, 5), (5, 5)).startswith("M5.0 5.0"))


class SmallHelpers(unittest.TestCase):
    def test_initials(self):
        self.assertEqual(labs.initials("Dave Monk"), "DM")
        self.assertEqual(labs.initials("Rachel Lee Nabors"), "RN")
        self.assertEqual(labs.initials("mima"), "M")

    def test_host(self):
        self.assertEqual(labs.host("https://www.mima.social/"), "mima.social")
        self.assertEqual(labs.host("http://a.example/b/"), "a.example/b")

    def test_title_class(self):
        self.assertEqual(labs.title_class("Short title"), "")
        self.assertEqual(labs.title_class("x" * 41), "long")


class Margin(unittest.TestCase):
    def test_split_notes(self):
        body, notes, numbers = labs.split_notes(
            "Text[^a].\n\n::: number 68ch | wide | lime\n\n```\n[^a]: in code\n::: number 1 | x\n```\n\n[^a]: The *note*.\n")
        self.assertEqual(notes, {"a": "The *note*."})
        self.assertEqual(numbers, [{"figure": "68ch", "label": "wide", "flags": ["lime"]}])
        self.assertIn("<!--number:0-->", body)
        self.assertIn("[^a]: in code\n::: number 1 | x", body)  # fenced code is left alone

    def test_number_needs_a_label(self):
        with self.assertRaises(ValueError):
            labs.split_notes("::: number 68ch\n")

    def render(self, source):
        body, notes, numbers = labs.split_notes(source)
        blocks, _ = md.to_blocks(body)
        return labs.with_margin(blocks, notes, numbers)

    def test_notes_are_numbered_in_reading_order_and_follow_their_block(self):
        out, count = self.render("One[^z].\n\nTwo.\n\nThree[^a] and `[^a]`.\n\n[^a]: Later.\n[^z]: First.\n")
        self.assertEqual(count, 2)
        blocks = out.split("\n")
        self.assertIn('<a id="snr-1" href="#sn-1" aria-label="Note 1">1</a>', blocks[0])
        # The aside comes right after its paragraph and covers rows 1 to 3 (the next aside's row).
        self.assertTrue(blocks[1].startswith('<aside class="margin-notes first" style="--r:1;--e:3">'))
        self.assertIn(">First.</span>", blocks[1])
        self.assertEqual(blocks[2], "<p>Two.</p>")
        self.assertIn("<code>[^a]</code>", blocks[3])  # inline code keeps its text
        self.assertTrue(blocks[4].startswith('<aside class="margin-notes" style="--r:3;--e:4">'))

    def test_number_card_hangs_on_the_block_before_it(self):
        out, count = self.render("## Head\n\nPara.\n\n::: number 9 | things | illustrative\n")
        self.assertEqual(count, 0)
        self.assertIn('<aside class="margin-notes tight" style="--r:2;--e:3"><p class="bignum"><b>9</b>'
                      '<span>things</span><span class="tag">Illustrative</span></p></aside>', out)

    def test_uncited_and_unknown_notes(self):
        with self.assertRaises(ValueError):
            self.render("Text.\n\n[^a]: Never cited.\n")
        out, _ = self.render("A regex [^b] stays.\n")
        self.assertEqual(out, "<p>A regex [^b] stays.</p>")

    def test_code_blocks_are_not_scanned(self):
        out, count = self.render("Cite[^a].\n\n```\nre.sub('[^a]', '')\n```\n\n[^a]: Note.\n")
        self.assertEqual(count, 1)
        self.assertIn("re.sub(&#x27;[^a]&#x27;", out)

    def test_plain_markdown(self):
        text = labs.plain_markdown("See [x](/learn/).\n\n::: number 9 | things | illustrative\n\n```\n::: number 1 | x\n```\n")
        self.assertIn("See [x](https://www.mima.social/learn/).", text)
        self.assertIn("> **9**: things (illustrative)", text)
        self.assertIn("```\n::: number 1 | x\n```", text)


class ToBlocks(unittest.TestCase):
    def test_to_html_is_the_blocks_joined(self):
        source = "## A\n\nText.\n\n- one\n- two\n"
        blocks, headings = md.to_blocks(source)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(md.to_html(source), ("\n".join(blocks), headings))


class LoadPost(unittest.TestCase):
    def test_published_and_draft_paths(self):
        self.assertEqual(post()["url"], "/labs/one/")
        draft = post(extra="draft: true\ncompact: true\n")
        self.assertEqual((draft["url"], draft["md_url"]), ("/labs/drafts/one/", "/labs/drafts/one.md"))
        self.assertTrue(draft["compact"])

    def test_missing_or_unknown_fields(self):
        for source in ("---\ntitle: T\n---\n", ):
            with self.assertRaises(ValueError):
                labs.load_post(source, "x.md", AUTHORS, CATEGORIES)
        with self.assertRaises(ValueError):
            post(author="nobody")
        with self.assertRaises(ValueError):
            post(extra="figure: /site-assets/app/board.webp\n")  # no alt text
        with self.assertRaises(ValueError):
            post(extra="callout-1: 1 1 from 2 2 | Needs a figure and two more\n")

    def test_figure_and_callouts(self):
        p = post(extra="figure: /site-assets/app/board.webp\nfigure-alt: The \"wall\"\n"
                       + "".join(f"callout-{i}: {i}0 10 from {i}0 0 | Label {i}\n" for i in (1, 2, 3)))
        self.assertEqual(p["figure_size"], (1920, 1296))
        fig = labs.hero_figure(p)
        self.assertIn('alt="The &quot;wall&quot;" width="1920" height="1296"', fig)
        self.assertEqual(fig.count('<path d="M'), 3)
        self.assertIn('viewBox="0 0 1000 675"', fig)
        self.assertIn("<li>Label 3</li>", fig)
        self.assertNotIn("<path", labs.hero_figure(p, callouts=False))


class Credits(unittest.TestCase):
    def test_author_with_link_and_photo(self):
        html = labs.credits(post(extra="shipped: A thing\nrefs: site#1\n"))
        self.assertIn('<a href="https://ada.example/" rel="author">ada.example</a>', html)
        self.assertIn('<img class="face" src="/site-assets/authors/ada.webp" alt="" width="64" height="64"', html)
        self.assertIn("<dt>What shipped</dt><dd>A thing</dd>", html)
        self.assertIn('<time datetime="2026-03-01">1 Mar 2026</time>', html)

    def test_author_without_link_or_photo_gets_neither(self):
        html = labs.credits(post(author="bo"))
        self.assertNotIn("<a ", html)
        self.assertNotIn("<img", html)
        self.assertIn('<span class="face" aria-hidden="true" style="--s:64px">B</span>', html)
        self.assertNotIn("What shipped", html)

    def test_person_json_ld_leaves_out_what_is_missing(self):
        self.assertEqual(labs.person_ld(AUTHORS["bo"]), {"@type": "Person", "name": "Bo", "jobTitle": "Designer"})
        self.assertEqual(labs.person_ld(AUTHORS["ada"]), {
            "@type": "Person", "name": "Ada Example", "jobTitle": "Engineer", "url": "https://ada.example/",
            "image": "https://www.mima.social/site-assets/authors/ada.webp"})


class Outputs(unittest.TestCase):
    """The feed, sitemap rows and llms.txt section carry published posts only."""

    def setUp(self):
        self.live = post("live", body="Body <b>&</b> [link](/learn/).\n")
        self.draft = post("hidden", extra="draft: true\n")
        self.posts = [self.live, self.draft]

    def test_feed_is_valid_atom_without_drafts(self):
        root = ET.fromstring(labs.feed(self.posts))
        self.assertEqual(root.tag, "{http://www.w3.org/2005/Atom}feed")
        for required in ("a:title", "a:id", "a:updated"):
            self.assertIsNotNone(root.find(required, ATOM))
        self.assertEqual(root.find("a:updated", ATOM).text, "2026-03-01T00:00:00Z")
        entries = root.findall("a:entry", ATOM)
        self.assertEqual(len(entries), 1)
        e = entries[0]
        self.assertEqual(e.find("a:id", ATOM).text, "https://www.mima.social/labs/live/")
        self.assertEqual(e.find("a:title", ATOM).text, "Post live")
        self.assertEqual(e.find("a:summary", ATOM).text, "About live & more.")
        self.assertEqual(e.find("a:author/a:uri", ATOM).text, "https://ada.example/")
        self.assertIn('href="https://www.mima.social/learn/"', e.find("a:content", ATOM).text)
        self.assertNotIn("hidden", labs.feed(self.posts))

    def test_empty_feed_is_still_valid_and_the_same_every_run(self):
        xml = labs.feed([self.draft])
        root = ET.fromstring(xml)
        self.assertEqual(root.findall("a:entry", ATOM), [])
        self.assertEqual(root.find("a:updated", ATOM).text, "2026-11-23T00:00:00Z")
        self.assertEqual(xml, labs.feed([self.draft]))

    def test_sitemap_rows(self):
        self.assertEqual(labs.sitemap_rows(self.posts), [("/labs/", datetime.date(2026, 3, 1)),
                                                         ("/labs/live/", datetime.date(2026, 3, 1))])
        self.assertEqual(labs.sitemap_rows([self.draft]), [])

    def test_llms_section(self):
        section = labs.llms_section(self.posts)
        self.assertTrue(section.startswith("## Labs\n"))
        self.assertIn("- [Post live](https://www.mima.social/labs/live.md): About live & more.", section)
        self.assertNotIn("hidden", section)
        self.assertEqual(labs.llms_section([self.draft]), "")

    def test_markdown_twin(self):
        text = labs.post_md(self.live)
        self.assertTrue(text.startswith("# Post live\n\n> About live & more.\n"))
        self.assertIn("By [Ada Example](https://ada.example/), Engineer", text)
        self.assertNotIn("Draft.", text)
        self.assertIn("Draft. ", labs.post_md(self.draft))
        self.assertNotIn("By [Ada", labs.post_md(self.draft))


class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.SPRITE, build.WORDMARK = build.sprite(), build.wordmark()

    def ld(self, page):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
        self.assertEqual(len(blocks), 1)
        return json.loads(blocks[0])["@graph"]

    def test_post_page(self):
        p = post(extra="figure: /site-assets/app/board.webp\nfigure-alt: Wall\n")
        page = labs.post_page(p, [])
        posting = next(x for x in self.ld(page) if x["@type"] == "BlogPosting")
        self.assertEqual(posting["author"]["@type"], "Person")
        self.assertEqual(posting["headline"], "Post one")
        self.assertEqual(posting["image"], "https://www.mima.social/site-assets/app/board.webp")
        self.assertIn('<a href="/labs/" aria-current="true">Labs</a>', page)
        self.assertIn('<a href="/learn/">Learn</a>', page)
        self.assertIn('type="application/atom+xml" href="https://www.mima.social/labs/feed.xml"', page)
        self.assertIn('<meta property="og:type" content="article" />', page)
        self.assertNotIn("noindex", page)
        self.assertNotIn("draft-note", page)

    def test_draft_page_is_marked_and_noindex(self):
        page = labs.post_page(post(extra="draft: true\n"), [])
        self.assertIn('<meta name="robots" content="noindex" />', page)
        self.assertIn('<p class="draft-note"><strong>Draft.</strong>', page)
        posting = next(x for x in self.ld(page) if x["@type"] == "BlogPosting")
        self.assertEqual(posting["author"], {"@id": "https://www.mima.social/#organization"})  # stand-in words

    def test_labs_css_loads_after_learn_css(self):
        page = labs.post_page(post(), [])
        self.assertLess(page.index("/learn/learn.css"), page.index("/labs/labs.css"))

    def test_index_lists_published_posts_only_in_its_data(self):
        a, b = post("a"), post("b", extra="draft: true\n")
        page = labs.index_page([a, b], drafts=True)
        blog = next(x for x in self.ld(page) if x["@type"] == "Blog")
        self.assertEqual([x["headline"] for x in blog["blogPost"]], ["Post a"])
        self.assertIn("noindex", page)
        self.assertIn('<span class="tag">Draft</span>', page)

    def test_empty_index_is_noindex_and_says_so(self):
        page = labs.index_page([])
        self.assertIn("noindex", page)
        self.assertIn("Nothing is published yet.", page)
        self.assertIn('<a href="/labs/" aria-current="page">Labs</a>', page)


class LearnBuildHooks(unittest.TestCase):
    def test_nav_link(self):
        self.assertEqual(build.nav_link("/learn/", "Learn", "/learn/"), '<a href="/learn/" aria-current="page">Learn</a>')
        self.assertEqual(build.nav_link("/learn/", "Learn", "/learn/x/"), '<a href="/learn/" aria-current="true">Learn</a>')
        self.assertEqual(build.nav_link("/learn/", "Learn", "/labs/"), '<a href="/learn/">Learn</a>')

    def test_og_key_for_labs(self):
        self.assertEqual(build.og_key("/labs/"), "labs")
        self.assertEqual(build.og_key("/labs/a-post/"), "labs-a-post")
        self.assertEqual(build.og_key("/labs/drafts/a-post/"), "labs-drafts-a-post")
        self.assertEqual(build.og_key("/learn/a-guide/"), "a-guide")

    def test_sitemap_takes_extra_rows(self):
        a = {"url": "/learn/one/", "updated_d": datetime.date(2026, 3, 1)}
        xml = build.sitemap([{"url": "/learn/topics/t/", "articles": [a]}], [a],
                            [("/labs/", datetime.date(2026, 4, 1))])
        self.assertIn("<url><loc>https://www.mima.social/labs/</loc><lastmod>2026-04-01</lastmod></url>", xml)
        ET.fromstring(xml)

    def test_replace_section(self):
        text = "# Mima\n\n## Learn\n\nold\n\n## Optional\n\n- x\n"
        added = build.replace_section(text, "Labs", "## Labs\n\nnew\n")
        self.assertEqual(added, "# Mima\n\n## Learn\n\nold\n\n## Labs\n\nnew\n\n## Optional\n\n- x\n")
        self.assertEqual(build.replace_section(added, "Labs", "## Labs\n\nnewer\n"),
                         "# Mima\n\n## Learn\n\nold\n\n## Labs\n\nnewer\n\n## Optional\n\n- x\n")
        self.assertEqual(build.replace_section(added, "Labs", ""), text)   # nothing published: section goes
        self.assertEqual(build.replace_section(text, "Labs", ""), text)    # and is not added


if __name__ == "__main__":
    unittest.main()
