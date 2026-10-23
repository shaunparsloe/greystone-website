"""Checks every page of the Greystone Guesthouse website.

Run from the repo root: python3 -m unittest tests.test_site -v
Stdlib only. The pages live in website/; this folder is never published.
"""
import functools
import json
import re
import subprocess
import unittest
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "website"
BASE = "https://greystoneguesthouse.co.za"
BOOK = "https://book.nightsbridge.com/20319"
WHATSAPP = "https://wa.me/27829537641"
LODGING_ID = BASE + "/#lodging"

NAV_HREFS = [
    "/", "/rooms/", "/surf-accommodation-supertubes/", "/things-to-do-jeffreys-bay/",
    "/restaurants-jeffreys-bay/", "/reviews.html", "/af/", WHATSAPP, BOOK,
]
# The Afrikaans page swaps its own "AF" link for an "EN" link to the English home page.
AF_NAV_HREFS = [("/" if h == "/af/" else h) for h in NAV_HREFS]
# Pages that have their own nav item, so carry aria-current="page" on it.
NAV_ITEM_PAGES = {
    "/rooms/", "/surf-accommodation-supertubes/", "/things-to-do-jeffreys-bay/",
    "/restaurants-jeffreys-bay/", "/reviews.html",
}
FOOTER_HREFS = [
    "/", "/rooms/", "/surf-accommodation-supertubes/", "/things-to-do-jeffreys-bay/",
    "/restaurants-jeffreys-bay/", "/business-travel/", "/reviews.html", "/#faq", "/af/", BOOK,
]
HELP_MESSAGES = {
    "surf": "Hi Monique, I'm staying at Greystone and would like help arranging surf lessons or board and wetsuit hire.",
    "shuttle": "Hi Monique, I'm staying at Greystone and would like help arranging an airport shuttle.",
    "restaurants": "Hi Monique, I'm staying at Greystone. Which restaurants would you recommend?",
}
BANNED = [
    "R638", "R723", "R1,105", "R1,275", "ZAR 638", "ZAR 723", "ZAR 1,105", "ZAR 1,275",
    "breakfast included", "Monique will book", "we arrange", "we'll organise", "Shuttle Service",
]
AF_HREFLANG = {
    "en-ZA": BASE + "/",
    "af": BASE + "/af/",
    "x-default": BASE + "/",
}

# One entry per page. Tasks add their page here.
PAGES = {
    "/": {
        "file": "index.html",
        "title": "Jeffreys Bay Accommodation | Greystone Guesthouse B&B",
        "h1": None,
        "lang": "en-ZA",
        "schema_types": {"BedAndBreakfast", "FAQPage"},
        "help_topics": [],
        "hreflang": AF_HREFLANG,
    },
    "/reviews.html": {
        "file": "reviews.html",
        "title": "Guest Reviews | Greystone Guesthouse B&B Jeffreys Bay",
        "h1": None,
        "lang": "en-ZA",
        "schema_types": {"BreadcrumbList", "BedAndBreakfast"},
        "help_topics": [],
        "hreflang": {},
    },
    "/404.html": {
        "file": "404.html",
        "title": "Page Not Found | Greystone Guesthouse Jeffreys Bay",
        "h1": None,
        "lang": "en-ZA",
        "schema_types": set(),
        "help_topics": [],
        "hreflang": {},
    },
    "/rooms/": {
        "file": "rooms/index.html",
        "title": "Rooms & Rates | Jeffreys Bay Accommodation | Greystone",
        "h1": "Rooms & rates at Greystone, Jeffreys Bay",
        "lang": "en-ZA",
        "schema_types": {"BreadcrumbList", "ItemList", "HotelRoom", "Offer", "FAQPage"},
        "help_topics": [],
        "hreflang": {},
    },
    "/things-to-do-jeffreys-bay/": {
        "file": "things-to-do-jeffreys-bay/index.html",
        "title": "Things to Do in Jeffreys Bay: A Local Guide | Greystone",
        "h1": "Things to do in Jeffreys Bay",
        "lang": "en-ZA",
        "schema_types": {"Article", "ItemList", "TouristAttraction", "BreadcrumbList"},
        "help_topics": ["surf", "restaurants", "shuttle"],
        "hreflang": {},
    },
    "/restaurants-jeffreys-bay/": {
        "file": "restaurants-jeffreys-bay/index.html",
        "title": "Restaurants in Jeffreys Bay Near Supertubes | Greystone",
        "h1": "Where to eat in Jeffreys Bay",
        "lang": "en-ZA",
        "schema_types": {"Article", "ItemList", "Restaurant", "BreadcrumbList"},
        "help_topics": ["restaurants"],
        "hreflang": {},
    },
    "/surf-accommodation-supertubes/": {
        "file": "surf-accommodation-supertubes/index.html",
        "title": "Surf Accommodation near Supertubes, Jeffreys Bay | Greystone",
        "h1": "Surf accommodation 300 m from Supertubes",
        "lang": "en-ZA",
        "schema_types": {"Article", "FAQPage", "BreadcrumbList"},
        "help_topics": ["surf", "shuttle"],
        "hreflang": {},
    },
    "/scuba-diving-jeffreys-bay/": {
        "file": "scuba-diving-jeffreys-bay/index.html",
        "title": "Scuba Diving in Jeffreys Bay: Reefs & Dive Trips | Greystone",
        "h1": "Scuba diving in Jeffreys Bay",
        "lang": "en-ZA",
        "schema_types": {"Article", "FAQPage", "BreadcrumbList", "SportsActivityLocation"},
        "help_topics": [],
        "hreflang": {},
    },
    "/business-travel/": {
        "file": "business-travel/index.html",
        "title": "Business Accommodation in Jeffreys Bay | Greystone",
        "h1": "Business stays in Jeffreys Bay",
        "lang": "en-ZA",
        "schema_types": {"WebPage", "FAQPage", "BreadcrumbList"},
        "help_topics": ["shuttle"],
        "hreflang": {},
    },
    "/af/": {
        "file": "af/index.html",
        "title": "Verblyf in Jeffreysbaai | Greystone Gastehuis B&B",
        "h1": "Greystone Gastehuis, B&B-verblyf in Jeffreysbaai",
        "lang": "af",
        "schema_types": {"WebPage", "BreadcrumbList"},
        "help_topics": [],
        "hreflang": AF_HREFLANG,
    },
}
# Pages that existed before the restructure. New pages must reference the lodging,
# never redefine it; these two keep their own schema.
OLD_PAGES = {"/", "/reviews.html", "/404.html"}

CONTAINERS = {"section", "article", "blockquote", "main", "aside"}


class Page(HTMLParser):
    """Collects what the tests need from one HTML file."""

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self.meta = {}
        self.links = []          # <link> attrs
        self.anchors = []        # <a> attrs, plus "_help_box" when inside aside.help-box
        self.h1s = []
        self.jsonld = []
        self.imgs = []           # <img> attrs, plus "_picture_webp"
        self.urls = []           # every href/src/srcset URL in the body and head
        self.nav_hrefs = []
        self.nav_current = []
        self.footer_hrefs = []
        self.text_parts = []     # visible text outside quoted guest reviews (<blockquote>)
        self._quote = 0
        self._in = {"title": 0, "h1": 0, "script": 0, "style": 0}
        self._script_type = None
        self._script_buf = []
        self._h1_buf = []
        self._nav_depth = 0
        self._nav_main = False
        self._footer_depth = 0
        self._footer_site = False
        self._containers = 0
        self._help_box = 0
        self._picture = False
        self._picture_webp = False
        self.feed(text)
        self.text = " ".join(self.text_parts)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        if tag in self._in:
            self._in[tag] += 1
        if tag == "script":
            self._script_type = a.get("type", "")
            self._script_buf = []
        if tag == "h1":
            self._h1_buf = []
        if tag in CONTAINERS:
            self._containers += 1
            if tag == "blockquote":
                self._quote += 1
            if tag == "aside" and "help-box" in a.get("class", "").split():
                self._help_box += 1
        if tag == "nav":
            if self._nav_depth == 0:
                self._nav_main = a.get("id") == "nav"
            self._nav_depth += 1
        if tag == "footer":
            if self._footer_depth == 0:
                self._footer_site = self._containers == 0
            self._footer_depth += 1
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        if tag == "link":
            self.links.append(a)
        if tag == "picture":
            self._picture, self._picture_webp = True, False
        if tag == "source" and self._picture and a.get("type") == "image/webp":
            self._picture_webp = True
        if tag == "img":
            a["_in_picture"] = self._picture
            a["_picture_webp"] = self._picture_webp
            self.imgs.append(a)
        if tag == "a":
            a["_help_box"] = self._help_box > 0
            self.anchors.append(a)
            href = a.get("href", "")
            if self._nav_depth and self._nav_main:
                self.nav_hrefs.append(href)
                if a.get("aria-current") == "page":
                    self.nav_current.append(href)
            if self._footer_depth and self._footer_site:
                self.footer_hrefs.append(href)
        for attr in ("href", "src"):
            if attr in a and tag in ("a", "link", "img", "script", "source"):
                self.urls.append(a[attr])
        if "srcset" in a:
            self.urls.extend(part.strip().split()[0] for part in a["srcset"].split(",") if part.strip())

    def handle_endtag(self, tag):
        if tag in self._in and self._in[tag]:
            self._in[tag] -= 1
        if tag == "script" and self._script_type == "application/ld+json":
            self.jsonld.append("".join(self._script_buf))
            self._script_type = None
        if tag == "h1":
            self.h1s.append(" ".join("".join(self._h1_buf).split()))
        if tag in CONTAINERS and self._containers:
            self._containers -= 1
            if tag == "blockquote" and self._quote:
                self._quote -= 1
            if tag == "aside" and self._help_box:
                self._help_box -= 1
        if tag == "nav" and self._nav_depth:
            self._nav_depth -= 1
        if tag == "footer" and self._footer_depth:
            self._footer_depth -= 1
        if tag == "picture":
            self._picture = False

    def handle_data(self, data):
        if self._in["script"]:
            self._script_buf.append(data)
            return
        if self._in["style"]:
            return
        if self._in["title"]:
            self.title += data
            return
        if self._in["h1"]:
            self._h1_buf.append(data)
        if not self._quote:
            self.text_parts.append(data)


@functools.lru_cache(maxsize=None)
def load(path):
    return (SITE / PAGES[path]["file"]).read_text(encoding="utf-8")


@functools.lru_cache(maxsize=None)
def parse(path):
    return Page(load(path))


@functools.lru_cache(maxsize=None)
def tracking_block():
    """The tracking head block from main's index.html, found by its markers."""
    src = subprocess.run(
        ["git", "show", "main:website/index.html"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    start = src.index("  <!-- Tracking opt-out")
    end = src.index("</script>", src.index('"yzbe0qilo7");')) + len("</script>")
    return src[start:end]


def schema_types(objects):
    found = set()

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                found.update([t] if isinstance(t, str) else t)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for o in objects:
        walk(o)
    return found


def defines_lodging(objects):
    hit = False

    def walk(o):
        nonlocal hit
        if isinstance(o, dict):
            if o.get("@id") == LODGING_ID and "name" in o:
                hit = True
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for o in objects:
        walk(o)
    return hit


def strip_reviews(o):
    if isinstance(o, dict):
        return {k: strip_reviews(v) for k, v in o.items() if k != "reviewBody"}
    if isinstance(o, list):
        return [strip_reviews(v) for v in o]
    return o


def site_file(url):
    """Map a root-relative URL to the file under website/ that serves it."""
    path = urllib.parse.urlsplit(url).path
    if path.endswith("/"):
        path += "index.html"
    return SITE / path.lstrip("/")


class SiteTests(unittest.TestCase):

    def pages(self, skip=()):
        return [(path, parse(path)) for path in PAGES if path not in skip]

    def test_title_and_description(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                spec = PAGES[path]
                self.assertEqual(p.title.strip(), spec["title"])
                self.assertLessEqual(len(p.title.strip()), 60)
                self.assertEqual(p.lang, spec["lang"])
                self.assertEqual(len(p.h1s), 1, p.h1s)
                if spec["h1"]:
                    self.assertEqual(p.h1s[0], spec["h1"])
                if path != "/404.html":
                    desc = p.meta.get("description", "")
                    self.assertTrue(140 <= len(desc) <= 160, f"description is {len(desc)} chars")

    def test_canonical_and_og(self):
        for path, p in self.pages(skip={"/404.html"}):
            with self.subTest(page=path):
                canonical = [l.get("href") for l in p.links if l.get("rel") == "canonical"]
                self.assertEqual(canonical, [BASE + path])
                for key in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
                    self.assertTrue(p.meta.get(key), f"missing {key}")
                self.assertEqual(p.meta["og:url"], BASE + path)
                self.assertTrue(p.meta["og:image"].startswith(BASE + "/images/"))

    def test_hreflang(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                found = {l.get("hreflang"): l.get("href") for l in p.links
                         if l.get("rel") == "alternate" and l.get("hreflang")}
                self.assertEqual(found, PAGES[path]["hreflang"])

    def test_tracking_block(self):
        block = tracking_block()
        for path, _ in self.pages(skip={"/404.html"}):
            with self.subTest(page=path):
                head = load(path).split("</head>")[0]
                self.assertIn(block, head)

    def test_jsonld(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                objects = [json.loads(b) for b in p.jsonld]
                found = schema_types(objects)
                self.assertTrue(PAGES[path]["schema_types"] <= found,
                                f"missing {PAGES[path]['schema_types'] - found}")
                if path not in ("/", "/404.html"):
                    self.assertIn("BreadcrumbList", found)
                if path not in OLD_PAGES:
                    self.assertFalse(defines_lodging(objects), "redefines the lodging; reference its @id")

    def test_nav_identical(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                self.assertEqual(p.nav_hrefs, AF_NAV_HREFS if path == "/af/" else NAV_HREFS)
                self.assertEqual(p.nav_current, [path] if path in NAV_ITEM_PAGES else [])

    def test_footer_explore(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                for href in FOOTER_HREFS:
                    self.assertIn(href, p.footer_hrefs)

    def test_links_resolve(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                for url in p.urls:
                    if url.startswith("/") and not url.startswith("//"):
                        self.assertTrue(site_file(url).is_file(), f"{url} has no file")

    def test_root_relative_assets(self):
        allowed = ("/", "#", "https://", "mailto:", "tel:")
        for path, p in self.pages():
            with self.subTest(page=path):
                for url in p.urls:
                    self.assertTrue(url.startswith(allowed), f"not root-relative: {url}")

    def test_images(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                for i, img in enumerate(p.imgs):
                    src = img.get("src")
                    self.assertTrue(img.get("alt", "").strip(), f"{src} has no alt")
                    self.assertTrue(img.get("width") and img.get("height"), f"{src} has no width/height")
                    if i > 0:
                        self.assertEqual(img.get("loading"), "lazy", f"{src} isn't lazy")
                    if img["_in_picture"]:
                        self.assertTrue(img["_picture_webp"], f"{src} has no WebP source")

    def test_booking_links(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                hrefs = [a.get("href", "") for a in p.anchors]
                self.assertIn(BOOK, hrefs)
                if path != "/404.html":
                    self.assertIn("/rooms/", hrefs)

    def test_copy_rules(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                # Guests' own words (blockquotes, reviewBody) aren't Greystone's claims.
                text = p.text + " " + " ".join(json.dumps(strip_reviews(json.loads(b))) for b in p.jsonld)
                # Asking "Is breakfast included?" (answered "room-only") is fine; claiming it isn't.
                lowered = text.lower().replace("is breakfast included", "")
                for phrase in BANNED:
                    self.assertFalse(phrase.lower() in lowered, f"found '{phrase}'")
                if "port elizabeth" in text.lower():
                    self.assertIn("gqeberha", text.lower())

    def test_help_boxes(self):
        for path, p in self.pages():
            with self.subTest(page=path):
                boxes = [a for a in p.anchors if "data-help-topic" in a]
                self.assertEqual([a["data-help-topic"] for a in boxes], PAGES[path]["help_topics"])
                for a in boxes:
                    self.assertTrue(a["_help_box"], "help link isn't inside aside.help-box")
                    self.assertIn("btn-whatsapp", a.get("class", "").split())
                    url = urllib.parse.urlsplit(a["href"])
                    self.assertEqual(f"{url.scheme}://{url.netloc}{url.path}", WHATSAPP)
                    text = urllib.parse.parse_qs(url.query)["text"][0]
                    self.assertEqual(text, HELP_MESSAGES[a["data-help-topic"]])

    def test_sitemap(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
              "image": "http://www.google.com/schemas/sitemap-image/1.1"}
        urls = {u.findtext("s:loc", namespaces=ns): u
                for u in ET.parse(SITE / "sitemap.xml").getroot().findall("s:url", ns)}
        for path in PAGES:
            if path == "/404.html":
                continue
            with self.subTest(page=path):
                self.assertIn(BASE + path, urls)
                self.assertTrue(urls[BASE + path].findtext("s:lastmod", namespaces=ns))
        if "/rooms/" in PAGES:
            rooms = urls.get(BASE + "/rooms/")
            self.assertIsNotNone(rooms)
            self.assertGreaterEqual(len(rooms.findall("image:image", ns)), 3)


    def test_css_files(self):
        chrome = (SITE / "css/chrome.css").read_text(encoding="utf-8")
        site = (SITE / "css/site.css").read_text(encoding="utf-8")
        for token in ("--ink: #080808", "--surface: #111", "--surface-2: #181818", "--gold: #C9A96E",
                      "--gold-light: #E8D5B0", "--cream: #F5F0E8", "--muted: #7A7567"):
            self.assertIn(token, chrome)
        self.assertIn("@media (max-width: 768px)", chrome)
        self.assertIn(".nav-toggle", chrome)
        self.assertIn(".help-box", site)
        self.assertIn(".btn-whatsapp", site)
        for css in (chrome, site):
            self.assertNotIn("@import", css)


    def test_sitejs_static(self):
        js = (SITE / "js/site.js").read_text(encoding="utf-8")
        for name in ("begin_booking", "contact_whatsapp", "view_reviews", "click_booking_com",
                     "click_tripadvisor", "navigate_section", "help_topic", "data-help-topic",
                     "aria-expanded", "Escape", "typeof gtag"):
            self.assertIn(name, js)


    def test_guide_length(self):
        path = "/things-to-do-jeffreys-bay/"
        main = load(path).split("<main", 1)[1].split("</main>", 1)[0]
        main = re.sub(r"<script.*?</script>|<style.*?</style>", " ", main, flags=re.S)
        words = len(re.sub(r"<[^>]+>", " ", main).split())
        self.assertTrue(1200 <= words <= 2000, f"guide has {words} words")
        hrefs = [a.get("href") for a in parse(path).anchors]
        self.assertIn("/restaurants-jeffreys-bay/", hrefs)
        self.assertIn("/surf-accommodation-supertubes/", hrefs)


    def test_restaurants_named(self):
        path = "/restaurants-jeffreys-bay/"
        main = re.sub(r"<script.*?</script>", " ", load(path).split("<main", 1)[1].split("</main>", 1)[0], flags=re.S)
        text = " ".join(re.sub(r"<[^>]+>", " ", main).split()).replace("&#x27;", "'").replace("&amp;", "&")
        walking = text.split("Within walking distance", 1)[1]
        self.assertIn("Nina's Real Food", walking)
        # Hyper Cafe (unverifiable), Quitschy's (in Walmer, Gqeberha) the 60's Diner (permanently closed) and Jolly Dolphin (a party venue, not a listed restaurant) stay off the page.
        for name in ("Hyper Cafe", "Quitschy", "60's Diner", "Jolly Dolphin"):
            self.assertNotIn(name, text)
        self.assertIsNone(re.search(r"\b\d{1,2}[:h]\d{2}\b", text), "looks like opening hours")
        self.assertIn("/things-to-do-jeffreys-bay/", [a.get("href") for a in parse(path).anchors])


    def test_no_third_party_rating_markup(self):
        # Ratings and reviews come from Booking.com, so they're shown as text, never marked up as the site's own.
        for path, p in self.pages():
            with self.subTest(page=path):
                found = schema_types([json.loads(b) for b in p.jsonld])
                self.assertFalse({"AggregateRating", "Review"} & found)

    def test_unconfirmed_claims_absent(self):
        # Not confirmed by Greystone: which floor the deluxe rooms are on, board storage,
        # and claims about what other guests enjoy. They stay off the site until Monique confirms.
        phrases = ["upstairs", "each with a balcony", "Kamers 1–4 · Bo", "where to keep your boards",
                   "where to keep and rinse them", "highlight for many guests", "guests have enjoyed"]
        for path, p in self.pages():
            with self.subTest(page=path):
                text = (p.text + " " + " ".join(p.jsonld)).lower()
                for phrase in phrases:
                    self.assertFalse(phrase.lower() in text, f"found '{phrase}'")


    def test_af_links_to_english_pages_say_so(self):
        # Only the home page has an Afrikaans version, so on /af/ the menu and footer
        # name the English pages in English (and mark them lang="en").
        html = load("/af/")
        parts = [html.split('<nav id="nav"', 1)[1].split("</nav>", 1)[0],
                 html.split('<footer class="site-footer">', 1)[1].split("</footer>", 1)[0]]
        english = {"/": {"Home", "EN"}, "/rooms/": {"Rooms", "Rooms &amp; rates"},
                   "/surf-accommodation-supertubes/": {"Surf"}, "/things-to-do-jeffreys-bay/": {"Things to do"},
                   "/restaurants-jeffreys-bay/": {"Restaurants"}, "/business-travel/": {"Business travel"},
                   "/reviews.html": {"Reviews", "Guest reviews"}, "/#faq": {"FAQ"}}
        for part in parts:
            for tag, href, label in re.findall(r'(<a href="([^"]+)"[^>]*>)([^<]*)</a>', part):
                if href in english and "nav-logo" not in tag:
                    with self.subTest(href=href, label=label):
                        self.assertIn(label.strip(), english[href])
                        self.assertIn('lang="en"', tag)


    def test_home_clips_sideways_overflow(self):
        # The home page's slide-in (.reveal-right) and Ken Burns animations start up to 44px
        # off-screen. Phone browsers widen the page to fit them unless <html> clips it, which
        # pushes the menu button off the right edge.
        css = load("/").split("<style>", 1)[1].split("</style>", 1)[0]
        self.assertRegex(css, r"html\s*\{[^}]*overflow-x:\s*clip")
    def test_footer_phone(self):
        # Guests phone (117 calls from the Google profile), so every footer's Find Us block
        # gives the number as a tap-to-call link, straight after the address.
        for path in PAGES:
            with self.subTest(page=path):
                footer = load(path).split('<footer class="site-footer">', 1)[1].split("</footer>", 1)[0]
                address = footer.split("<address>", 1)[1].split("</address>", 1)[0]
                after = address.split("South Africa<br>", 1)[1]
                self.assertRegex(after.lstrip(), r'^<a href="tel:\+27829537641"[^>]*>\+27 82 953 7641</a>')


if __name__ == "__main__":
    unittest.main()
