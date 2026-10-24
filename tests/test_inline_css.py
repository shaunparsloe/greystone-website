"""Checks the publish step that writes the site's CSS files into each page (tools/inline_css.py).

Run from the repo root: python3 -m unittest tests.test_inline_css -v
"""
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "website"


class InlineCssTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from tools.inline_css import inline_site
        cls.tmp = Path(tempfile.mkdtemp())
        cls.out = cls.tmp / "_site"
        shutil.copytree(SITE, cls.out, ignore=shutil.ignore_patterns(".*"))
        cls.changed = inline_site(cls.out)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def pages(self):
        return sorted(self.out.rglob("*.html"))

    def test_no_stylesheet_links_left(self):
        for page in self.pages():
            with self.subTest(page=page.name):
                self.assertNotRegex(page.read_text(encoding="utf-8"), r'<link rel="stylesheet" href="/css/')

    def test_css_written_in_place_in_the_same_order(self):
        # Each link is replaced by its file's contents where it stood, so the cascade order is unchanged.
        for page in self.pages():
            src = (SITE / page.relative_to(self.out)).read_text(encoding="utf-8")
            out = page.read_text(encoding="utf-8")
            links = re.findall(r'<link rel="stylesheet" href="/css/([\w-]+\.css)">', src)
            with self.subTest(page=str(page.relative_to(self.out))):
                positions = []
                for name in links:
                    css = (SITE / "css" / name).read_text(encoding="utf-8").strip()
                    i = out.find(css)
                    self.assertNotEqual(i, -1, f"{name} not inlined")
                    positions.append(i)
                self.assertEqual(positions, sorted(positions))

    def test_everything_else_unchanged(self):
        # Removing the inlined CSS and the links gives back identical pages.
        for page in self.pages():
            src = (SITE / page.relative_to(self.out)).read_text(encoding="utf-8")
            out = page.read_text(encoding="utf-8")
            src_rest = re.sub(r'\s*<link rel="stylesheet" href="/css/[\w-]+\.css">', "", src)
            out_rest = re.sub(r"\s*<style data-inlined=\"[\w-]+\.css\">.*?</style>", "", out, flags=re.S)
            with self.subTest(page=str(page.relative_to(self.out))):
                self.assertEqual(out_rest, src_rest)

    def test_reports_pages_changed(self):
        linking = [p for p in SITE.rglob("*.html") if ".playwright" not in str(p)
                   and '<link rel="stylesheet" href="/css/' in p.read_text(encoding="utf-8")]
        self.assertEqual(self.changed, len(linking))


if __name__ == "__main__":
    unittest.main()
