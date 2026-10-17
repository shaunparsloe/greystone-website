---
name: seo-weekly
description: Write the weekly SEO report for Greystone Guesthouse (analytics-data/SEO/reports/YYYY-Wnn.md) from cached Search Console + GA4 data, covering the last full Monday–Sunday week. Use when the user runs /seo-weekly or asks for the weekly SEO/traffic report. Optional argument: an ISO week like 2026-W40.
---

# /seo-weekly

The real instructions live in the private data repo, so the Wednesday GitHub Actions run and runs on this PC follow the same copy:

**Read `analytics-data/.claude/skills/seo-weekly/SKILL.md` and follow it exactly**, passing on any week argument. Run its commands from inside `analytics-data/`; all its paths are relative to that folder.

The report is normally written automatically every Wednesday, then emailed as a GitHub issue in `shaunparsloe/greystone-analytics-data`. Run it here to redo a week, or if the cloud run failed.
