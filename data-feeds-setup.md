# Data Feeds Setup: Your Action List

Goal: give Claude access to **Search Console** (what people search), **Google Analytics** and **Microsoft Clarity** (what they do on the site), and **Firecrawl** and **DataForSEO** (what competitors are doing).

Last updated: 10 October 2026

## How it works (already done)

- All five connectors are registered with Claude Code for this project only.
- Your keys live in **one private file**: `~/.config/greystone-seo/secrets.env`. It's readable only by your user account and sits outside the repo, so it can't be committed.
- A launcher (`~/.config/greystone-seo/run.sh`) reads that file and starts each connector. Claude's config contains no secrets.
- Each feed works independently, so add keys one at a time in any order.

## Golden rules for keys

- Edit the keys file in a **separate terminal window**:
  ```
  nano ~/.config/greystone-seo/secrets.env
  ```
  Paste each value straight after the `=`, with no spaces or quotes. Save with **Ctrl+O**, then **Enter**, then exit with **Ctrl+X**.
- **Never** paste a key into the Claude chat, and never run a command containing a key with `!` in Claude. Both get saved in the conversation history.
- Never put keys in any file inside the `Greystone` folder. The GitHub repo is public.

To check which keys are filled in without revealing them:
```
grep -E '^[A-Z_]+=.+' ~/.config/greystone-seo/secrets.env | cut -d= -f1
```

---

## 1. Microsoft Clarity: where visitors click and scroll

Status: **done.** Tag live on all pages since 10 Oct 2026; API token in the keys file; daily pull running.

- [ ] About 2 hours after go-live, check the Clarity dashboard shows visits.

**Daily pull:** Windows Task Scheduler runs **"Greystone Clarity daily pull"** at **07:00** every day (or as soon as the PC is next on, if it was off). It runs `scripts/clarity_pull.py`, which saves to `analytics-data/clarity/`:
- `clarity_long.csv`: every metric for every day, for trends
- `raw/<date>/*.json`: the raw API responses
- `pull_log.csv` / `run.log`: one line per run, so you can check it's working

Each run uses 5 of Clarity's 10 daily API requests (totals, by page, device, channel, country), leaving 5 for questions to Claude. If the PC is off for a day or two, the next run reaches back up to 3 days. **More than 3 days off means a gap in the data.** To pause it, disable the task in Task Scheduler.

---

## 2. Google Search Console + Google Analytics: what people search, and traffic

Status: **done.** Both connected and tested 10 Oct 2026.

One Google "service account" key covers both.

### 2a. Search Console property: **done**

- [x] Domain property `sc-domain:greystoneguesthouse.co.za` is verified.
- [x] Sitemap submitted 1 Apr 2026, last read by Google 19 Apr 2026.
- [ ] **Resubmit the sitemap** so Google picks up the 10 Oct changes sooner: Search Console → **Sitemaps** → enter `sitemap.xml` → **Submit**.
- [ ] **Request indexing** for the updated pages: paste `https://greystoneguesthouse.co.za/` into the search bar at the top → **Request indexing**. Repeat for `/reviews.html`.

### 2b. Create the Google service account

- [x] Google Cloud project created: ID **`greystone-seo`** (number 228233396848). Already added to the keys file.
- [x] Google Analytics Data API enabled.
- [x] Google Analytics Admin API enabled.
- [x] **Search Console API working** (tested 10 Oct 2026). Link, in case it ever needs re-enabling: open <https://console.cloud.google.com/apis/library/searchconsole.googleapis.com?project=greystone-seo> → **Enable**.
- [x] Service account created: `claude-seo@greystone-seo.iam.gserviceaccount.com`.
- [x] JSON key created.
- [x] Key saved to `~/.config/greystone-seo/google-service-account.json` (owner-only permissions; no copy left in Downloads).

### 2c. Give the service account access

- [x] Added to Search Console as a **Restricted** user.
- [x] Added to Google Analytics as a **Viewer** (tested 10 Oct 2026).

### 2d. GA4 property ID: **done**

- [x] `GOOGLE_CLOUD_PROJECT=greystone-seo` is in the keys file. `GOOGLE_APPLICATION_CREDENTIALS` already points to the right path.
- [x] GA4 property ID: **530830177** (measurement ID `G-LHN8DCK50B`).

---

## 3. Firecrawl: scrape competitor websites

Status: **done.** Key added and tested 10 Oct 2026.

- [x] Signed up and created an API key.
- [x] `FIRECRAWL_API_KEY` is in the keys file.

Notes: free plan is **1,000 credits per month** (1,000 pages scraped *or* 500 searches), 2 requests at a time, low rate limits. A full three-competitor scan uses about 30–60 credits; a weekly check-in about 10–20.

---

## 4. DataForSEO: keyword rankings, search volumes, competitor SEO

- [ ] Sign up at <https://app.dataforseo.com>. It's **pay-as-you-go with an upfront deposit**, so decide your budget first.
- [ ] Go to the **API Access** page and copy the **API login** and **API password**. These are **not** your account email or password.
- [ ] In the keys file:
  ```
  DATAFORSEO_USERNAME=your-api-login
  DATAFORSEO_PASSWORD=your-api-password
  ```

---

## 5. Finish up

- [x] Restart Claude Code in the `Greystone` folder.
- [x] Run `/mcp`. Search Console, Analytics, Clarity and Firecrawl show **connected**, and Search Console and Analytics returned live data (10 Oct 2026). DataForSEO shows "failed" until its keys are added (step 4).
- [ ] If one shows "failed", tell Claude which one. The launcher gives a clear message for missing keys or files.

## Optional but recommended

- [ ] **Privacy notice (POPIA):** the site uses Google Analytics and Clarity with no tracking notice. Ask Claude to add a short privacy page and notice.
- [x] **Bing Webmaster Tools:** imported from Google Search Console (10 Oct 2026).
  - [ ] In a day or two, check **Sitemaps** in Bing shows `sitemap.xml` as processed, and **Site Explorer** lists both pages.
