"""Checks on the repair guide site in docs/.

Standard library only. From the repository root:

    python3 -m unittest tests.test_docs_site -v
"""

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/jamesjnadeau/refGearDownCounter"

GUIDES = {
    "slider.html": "down-indicator-selector",
    "finger-loop.html": "down-indicator-string",
    "wrist-2x2.html": "down-indicator-watch",
    "umpire-counter.html": "down-counter-umpire",
}

# Every guide answers the same questions, under the same anchors.
SECTIONS = ["parts", "tools", "open", "replace", "close", "damage", "unconfirmed"]

# Linked files that are not on main yet. Each arrives with the pull request
# named beside it.
PENDING = {
    "down-indicator-selector/PARTS.md": 8,
    "down-indicator-selector/ASSEMBLY.md": 8,
    "down-indicator-string/PARTS.md": 8,
    "down-indicator-string/ASSEMBLY.md": 8,
}

VOID = {"meta", "link", "br", "hr", "img", "input"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.ids = []
        self.hrefs = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag in ("a", "link") and "href" in attrs:
            self.hrefs.append(attrs["href"])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"</{tag}> at {self.getpos()} closes {self.stack[-1:]}")
        else:
            self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)


def parse(name):
    page = Page()
    page.feed((DOCS / name).read_text(encoding="utf-8"))
    page.close()
    return page


class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {p.name: parse(p.name) for p in sorted(DOCS.glob("*.html"))}

    def test_the_site_is_served_as_plain_files(self):
        self.assertTrue((DOCS / ".nojekyll").exists())
        self.assertTrue((DOCS / "index.html").exists())
        self.assertTrue((DOCS / "style.css").exists())

    def test_every_counter_has_a_guide(self):
        for name in GUIDES:
            self.assertIn(name, self.pages)

    def test_every_page_is_well_formed(self):
        for name, page in self.pages.items():
            self.assertEqual(page.errors, [], name)
            self.assertEqual(page.stack, [], name)
            self.assertEqual(len(page.ids), len(set(page.ids)), f"{name}: repeated id")

    def test_every_guide_has_every_section(self):
        for name in GUIDES:
            for section in SECTIONS:
                self.assertIn(section, self.pages[name].ids, f"{name} lacks #{section}")

    def test_every_guide_says_what_is_unchecked_and_what_is_unknown(self):
        for name in GUIDES:
            text = " ".join(self.pages[name].text)
            self.assertIn("Not checked on a printed unit", text, name)
            self.assertIn("Not recorded", text, name)

    def test_the_front_page_lists_every_guide_its_files_and_the_licence(self):
        hrefs = self.pages["index.html"].hrefs
        for name, folder in GUIDES.items():
            self.assertIn(name, hrefs)
            self.assertIn(f"{REPO_URL}/tree/main/{folder}", hrefs)
        self.assertIn(f"{REPO_URL}/blob/main/LICENSE", hrefs)

    def test_every_guide_links_to_its_own_files(self):
        for name, folder in GUIDES.items():
            self.assertTrue(
                any(folder in h for h in self.pages[name].hrefs), f"{name}: no link to {folder}"
            )

    def test_links_within_the_site_resolve(self):
        for name, page in self.pages.items():
            for href in page.hrefs:
                if href.startswith("http"):
                    continue
                target, _, anchor = href.partition("#")
                target = target or name
                self.assertTrue((DOCS / target).exists(), f"{name}: {href}")
                if anchor:
                    self.assertIn(anchor, self.pages[target].ids, f"{name}: {href}")

    def test_links_into_the_repository_point_at_real_files(self):
        pattern = re.compile(re.escape(REPO_URL) + r"/(?:blob|tree)/main/(.+)")
        for name, page in self.pages.items():
            for href in page.hrefs:
                match = pattern.fullmatch(href)
                if not match:
                    continue
                path = match.group(1)
                if path in PENDING:
                    continue
                self.assertTrue((ROOT / path).exists(), f"{name}: {href}")


if __name__ == "__main__":
    unittest.main()
