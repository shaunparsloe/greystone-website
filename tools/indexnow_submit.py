"""Tell Bing (and the other IndexNow search engines) which site pages have changed.

The key is the name of website/<key>.txt, which holds the same key. IndexNow keys are public by
design: the file proves the site owner sent the request.

Only pages listed in website/sitemap.xml are sent. The Pages workflow runs this after each deploy
to main with the files that changed in the push; a manual run of the workflow sends every page.

Usage:
  python3 tools/indexnow_submit.py --all                 # every page in the sitemap
  python3 tools/indexnow_submit.py website/rooms/index.html website/css/site.css
  python3 tools/indexnow_submit.py --all --dry-run       # print the request, don't send it
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "website"
HOST = "greystoneguesthouse.co.za"
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_FILE = re.compile(r"^[0-9a-f]{32}$")


def find_key(site=SITE):
    """Return the key from the single website/<32 hex>.txt file whose content matches its name."""
    keys = [p for p in site.glob("*.txt") if KEY_FILE.match(p.stem)]
    if len(keys) != 1:
        raise SystemExit(f"expected one IndexNow key file in {site}, found {len(keys)}")
    key = keys[0].stem
    if keys[0].read_text(encoding="utf-8").strip() != key:
        raise SystemExit(f"{keys[0].name} must contain exactly its own key")
    return key


def sitemap_urls(site=SITE):
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.parse(site / "sitemap.xml").getroot()
    return [u.findtext("s:loc", namespaces=ns).strip() for u in root.findall("s:url", ns)]


def file_to_url(path):
    """Map a repo path such as website/rooms/index.html to its public URL, or None for non-pages."""
    path = str(path).replace("\\", "/")
    if not path.startswith("website/") or not path.endswith(".html"):
        return None
    rel = path[len("website/"):]
    if rel == "index.html":
        rel = ""
    elif rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    return f"https://{HOST}/{rel}"


def urls_for(changed, site=SITE):
    """Sitemap URLs whose page file is among the changed paths, in sitemap order."""
    listed = sitemap_urls(site)
    wanted = {file_to_url(p) for p in changed} - {None}
    return [u for u in listed if u in wanted]


def payload(urls, key):
    return {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }


def submit(body):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="send every page in the sitemap")
    ap.add_argument("--dry-run", action="store_true", help="print the request without sending it")
    ap.add_argument("files", nargs="*", help="changed repo paths (website/...)")
    args = ap.parse_args(argv)

    urls = sitemap_urls() if args.all else urls_for(args.files)
    if not urls:
        print("IndexNow: no sitemap pages changed, nothing to send")
        return 0
    body = payload(urls, find_key())
    print("IndexNow: sending", *urls, sep="\n  ")
    if args.dry_run:
        print(json.dumps(body, indent=2))
        return 0
    status = submit(body)
    # 200 = accepted, 202 = accepted while the key is checked; anything else is a failure.
    print(f"IndexNow: HTTP {status}")
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main())
