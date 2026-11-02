"""Checks for tools/indexnow_submit.py and the IndexNow key file."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import indexnow_submit as ix  # noqa: E402


class IndexNowTest(unittest.TestCase):
    def test_key_file(self):
        key = ix.find_key()
        self.assertEqual((ix.SITE / f"{key}.txt").read_text(encoding="utf-8").strip(), key)

    def test_file_to_url(self):
        self.assertEqual(ix.file_to_url("website/index.html"), "https://greystoneguesthouse.co.za/")
        self.assertEqual(ix.file_to_url("website/rooms/index.html"), "https://greystoneguesthouse.co.za/rooms/")
        self.assertEqual(ix.file_to_url("website/reviews.html"), "https://greystoneguesthouse.co.za/reviews.html")
        self.assertIsNone(ix.file_to_url("website/css/site.css"))
        self.assertIsNone(ix.file_to_url("tools/inline_css.py"))

    def test_every_sitemap_page_maps_from_a_file(self):
        files = [str(p.relative_to(ix.ROOT)).replace("\\", "/") for p in ix.SITE.rglob("*.html")]
        self.assertEqual(ix.urls_for(files), ix.sitemap_urls())

    def test_only_sitemap_pages_sent(self):
        self.assertEqual(ix.urls_for(["website/404.html", "website/css/site.css"]), [])
        self.assertEqual(ix.urls_for(["website/rooms/index.html"]), ["https://greystoneguesthouse.co.za/rooms/"])


if __name__ == "__main__":
    unittest.main()
