---
name: seo-monthly
description: Write the monthly SEO review for Greystone Guesthouse (analytics-data/SEO/reports/YYYY-MM-monthly.md): search + GA4 month, Book Now clicks vs NightsBridge bookings, rankings, every local competitor's visibility and rates. Use when the user runs /seo-monthly or asks for the monthly SEO review. Optional argument: a month like 2026-09.
---

# /seo-monthly

The real instructions live in the private data repo, so the GitHub Actions run (10th of each month) and runs on this PC follow the same copy:

**Read `analytics-data/.claude/skills/seo-monthly/SKILL.md` and follow it exactly**, passing on any month argument. Run its commands from inside `analytics-data/`; all its paths are relative to that folder.

The review is normally written automatically on the 10th of each month, then emailed as a GitHub issue in `shaunparsloe/greystone-analytics-data`. Run it here to redo a month, or if the cloud run failed. Its DataForSEO script costs money (it never re-buys data it already has for the month).
