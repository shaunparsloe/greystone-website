"""Fail if anything other than site files is tracked under website/.

website/ is public twice over (this repo is public, and GitHub Pages publishes it), so notes,
plans, data and screenshots must never land there. The local pre-commit hook blocks them on
this machine; this check catches anything that got past it (another machine, a github.com
edit, --no-verify). Keep the allowed types in step with the rsync list in pages.yml and the hook.

Run from the repo root: python3 -I tools/check_public_files.py [paths...]
With no paths it checks every tracked file under website/.
"""
import re
import subprocess
import sys

ALLOWED = re.compile(
    r"^website/(?:"
    r"\.claude/settings\.json|\.gitignore|CNAME"
    r"|(?:[^./][^/]*/)*[^/]+\.(?:html|css|js|xml|txt|jpg|jpeg|png|webp|avif|gif|svg|ico|woff2)"
    r")$")


def main(argv):
    paths = argv or subprocess.run(
        ["git", "ls-files", "website/"], capture_output=True, text=True, check=True).stdout.splitlines()
    bad = [p for p in paths if p.startswith("website/") and not ALLOWED.match(p)]
    for p in bad:
        print(f"{p}: not a site file; website/ is public. Put notes in analytics-data/SEO/.")
    if bad:
        return 1
    print(f"All {len(paths)} files under website/ are site files.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
