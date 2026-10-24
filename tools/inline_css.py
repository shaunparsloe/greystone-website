"""Write the site's own CSS files straight into each page, for the published copy only.

A linked stylesheet blocks the first paint until it has downloaded; on a slow phone that round trip
costs ~0.4 s. The source pages keep their <link rel="stylesheet" href="/css/..."> tags (one place to
edit each file); the Pages workflow runs this on _site/ just before upload.

Usage: python3 tools/inline_css.py _site
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r'<link rel="stylesheet" href="/css/([\w-]+\.css)">')


def inline_site(site_dir):
    """Replace every local stylesheet link under site_dir with a <style> block. Returns pages changed."""
    site_dir = Path(site_dir)
    cache = {}

    def css(name):
        if name not in cache:
            cache[name] = (site_dir / "css" / name).read_text(encoding="utf-8").strip()
        return cache[name]

    changed = 0
    for page in sorted(site_dir.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        new = LINK.sub(lambda m: f'<style data-inlined="{m.group(1)}">\n{css(m.group(1))}\n</style>', html)
        if new != html:
            page.write_text(new, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"inlined CSS into {inline_site(sys.argv[1])} pages")
