# Greystone website (`website/`)

This folder is the live site, published to https://greystoneguesthouse.co.za by GitHub Pages from `main`. The workflow leaves `*.md` and `.claude/` out of the upload.

- **Current project: the website restructure.** Read [`SEO-RESTRUCTURE-PLAN.md`](SEO-RESTRUCTURE-PLAN.md) in full before starting. It has the goals, keyword targets, page specs, facts, and what mustn't break.
- Property facts, data feeds and SEO data rules: `../CLAUDE.md`. Keyword and competitor data: `../analytics-data/SEO/` (private repo; never copy business data into this public repo).
- Plugins enabled for this folder only: **superpowers** and **playwright** (headless Chromium, set in `.claude/settings.json`).
- Git: never commit to `main`; branch, push and open a PR. Shaun merges.
- Keep the tracking head block and the GA4 event names (`begin_booking`, `contact_whatsapp`) exactly as they are. The analytics reports depend on them.
