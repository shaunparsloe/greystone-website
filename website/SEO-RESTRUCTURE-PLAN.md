# Website restructure and SEO plan

Written 21 Oct 2026 for a Claude Code session started in `Greystone/website/`. It has everything needed to restructure the site. Read it in full before starting, and read `../CLAUDE.md` (property facts, data rules).

Not published: `.github/workflows/pages.yml` leaves `*.md` and `.claude/` out of the GitHub Pages upload.

---

## 1. Goal

Turn the one-page site into a small, well-linked site so that Greystone's **own website** ranks for the main Jeffreys Bay accommodation searches, plus the planning searches that bring links and early visibility. Shaun's brief: "Restructure the website, create all the pages. Fill in with your best effort for now; Monique will review and update afterwards. Ensure good SEO."

**Why:**
- The home page now targets the main terms (title, H1, H2s, FAQs; PR #2, 17 Oct 2026). But one page can only rank for so much.
- Greystone has **4 backlinks, all spam**. Local price peers have 36–120. Guide pages are the most natural way to earn links.
- A guesthouse (**On the Beach Guesthouse**, `onthebeach.co.za/activities-restaurants/`) is **#1 on Google** for "things to do in jeffreys bay". The price peers' guide pages rank only on pages 4–5. So this is winnable.

Sources: Google Search Console (9 Jul – 6 Oct 2026, retrieved 10 Oct 2026); DataForSEO Labs SA volumes (retrieved 10 and 17 Oct 2026); live SERP for "things to do in jeffreys bay" (retrieved 21 Oct 2026). Full detail is in `../analytics-data/SEO/keyword-map.md` and `../analytics-data/SEO/seo-audit-report.md`.

---

## 2. Keyword targets (SA monthly searches)

Google groups close variants, so count each cluster once.

| Cluster | Volume | Target page |
|---|---|---|
| jeffreys bay accommodation / places to stay / lodges | 4,400 | Home (already), **/rooms/** |
| restaurants in jeffreys bay / best restaurants | 3,600 | **/restaurants-jeffreys-bay/** |
| things to do in jeffreys bay / what to do / activities | 1,300 (+390, 260) | **/things-to-do-jeffreys-bay/** |
| accommodation in jeffreys bay | 880 | Home, /rooms/ |
| jeffreys bay accommodation supertubes | 720 | **/surf-accommodation-supertubes/** |
| surfing in jeffreys bay | 590 | /surf-accommodation-supertubes/ |
| hotels in jeffreys bay | 590 | /rooms/ (honest "guest house, not a hotel" framing; never claim to be a hotel) |
| guest house jeffreys bay | 480 | Home, /rooms/ |
| b&b / bed and breakfast jeffreys bay | 390 | Home, /rooms/ |
| affordable / cheap accommodation, cheap b&b | 320 + 140 | /rooms/ |
| humansdorp accommodation | 260 | **Light mention only** (Shaun's decision): a distance line and one FAQ, e.g. on /business-travel/. Never imply Greystone is in Humansdorp |
| jeffreys bay beach accommodation / sea view | 210 + 70 | /rooms/ |
| hidden gems in jeffreys bay | 140 | /things-to-do-jeffreys-bay/ |
| jeffreys bay to port elizabeth airport | 30 | Getting-here section on the guide |
| Afrikaans: verblyf jeffreysbaai, gastehuis jeffreysbaai, B&B jeffreysbaai | not measured | **/af/** |

**Don't target:**
- self-catering terms (Greystone isn't self-catering);
- "jeffreys bay main beach" (Greystone is near Point Beach and Supertubes, not Main Beach);
- competitors' brand names, and Airbnb.

---

## 3. New site structure

| URL | File | Purpose |
|---|---|---|
| `/` | `index.html` | Home (exists). Keep; add links into the new pages |
| `/rooms/` | `rooms/index.html` | Rooms and rates: each tier with photos, features, price, who it suits |
| `/things-to-do-jeffreys-bay/` | `things-to-do-jeffreys-bay/index.html` | Local guide: beaches, surf, nature, day trips, getting here |
| `/restaurants-jeffreys-bay/` | `restaurants-jeffreys-bay/index.html` | Where to eat, walking distance first |
| `/surf-accommodation-supertubes/` | `surf-accommodation-supertubes/index.html` | Surf trip page: Supertubes, season, lessons, J-Bay Open |
| `/business-travel/` | `business-travel/index.html` | Contractors and corporate guests: WiFi, solar backup, invoices, Humansdorp/Kouga |
| `/af/` | `af/index.html` | Afrikaans home page (Monique speaks Afrikaans and will check it) |
| `/reviews.html` | `reviews.html` | Exists. **Keep this URL** (it's indexed and linked) |
| `/404.html` | `404.html` | Exists. Add links to the new pages |

Use folder `index.html` files so URLs end in `/`. Canonical URLs use the trailing slash, e.g. `https://greystoneguesthouse.co.za/rooms/`.

### Per-page SEO spec

Titles must be ≤ 60 characters and descriptions 140–160. These are starting points; improve them if needed.

**/rooms/**
- Title: `Rooms & Rates | Jeffreys Bay Accommodation | Greystone`
- H1: "Rooms & rates at Greystone, Jeffreys Bay"
- Description: B&B guest house rooms in Jeffreys Bay from R638 a night: sea-view deluxe rooms with balconies, standard queen rooms and budget annex rooms, all en-suite.
- Content:
  - One section per tier (Deluxe Sea View, rooms 1–4; Standard Queen, 5–6; Budget Annex, 7–8), each with H2, photos, features, size, price for 2 / 1 guests, best for, and a Book button.
  - A comparison table.
  - "What every room has".
  - Breakfast (available to order; see facts).
  - House rules summary.
  - FAQ: "Is Greystone a hotel or a guest house?", affordable rooms, sea view, single rates, twin option in room 6, ground-floor rooms.
- Schema: `BreadcrumbList`; `ItemList` of `HotelRoom` (`bed`, `occupancy`, `floorSize` where known, `amenityFeature`) each with an `Offer` (`priceCurrency` ZAR); `FAQPage`. Link to the lodging `@id` `https://greystoneguesthouse.co.za/#lodging` (defined on the home page).

**/things-to-do-jeffreys-bay/**
- Title: `Things to Do in Jeffreys Bay: A Local Guide | Greystone`
- H1: "Things to do in Jeffreys Bay"
- Sections (H2):
  - Beaches near Greystone
  - Surfing (link to the surf page)
  - Nature reserves and walks
  - Wildlife and day trips (Addo, Tsitsikamma, St Francis Bay)
  - Adventure (skydiving, horse riding, sandboarding)
  - Rainy-day and family ideas (Shell Museum)
  - Where to eat (short; link to the restaurants page)
  - Getting here (Port Elizabeth (Gqeberha) airport, drive times)
  - Where to stay (soft CTA to Greystone)
- Write it practical, specific and local: distances from Greystone, best times, local tips. A generic list won't compete; On the Beach's page wins because it's practical. Aim for 1,200–2,000 words.
- Schema: `Article` (`about` Jeffreys Bay, `author` Greystone Guesthouse, `datePublished`/`dateModified`); `ItemList` of `TouristAttraction`; `BreadcrumbList`.

**/restaurants-jeffreys-bay/**
- Title: `Restaurants in Jeffreys Bay Near Supertubes | Greystone`
- H1: "Where to eat in Jeffreys Bay"
- Sections:
  - "Within walking distance of Greystone", nearest first (Hyper Cafe & Bar, Nina's Real Food, Quitschy's Pizza).
  - "Further afield" (e.g. Kitchen Windows beach restaurant and others; see facts).
  - Breakfast at Greystone.
  - Groceries (the Spar behind Greystone).
- Don't invent opening hours, prices or menus. Link to each restaurant's own site where known.
- Schema: `Article`, `ItemList` of `Restaurant` (name, url, address only where verified), `BreadcrumbList`.

**/surf-accommodation-supertubes/**
- Title: `Surf Accommodation near Supertubes, Jeffreys Bay | Greystone`
- H1: "Surf accommodation 300 m from Supertubes"
- Sections: the walk to Supertubes; when to come (winter swells, roughly May–September); the J-Bay Open; learning to surf (beginner lessons are at Kitchen Windows / Dolphin Beach, not Supertubes); board storage and rinsing (**ask Monique**); early breakfast for dawn patrol (**ask Monique**); FAQ.
- Schema: `Article`, `FAQPage`, `BreadcrumbList`.

**/business-travel/**
- Title: `Business Accommodation in Jeffreys Bay | Greystone`
- H1: "Business stays in Jeffreys Bay"
- Content:
  - Solar power with battery backup (WiFi and lights stay on during load shedding).
  - Free WiFi.
  - Free on-site parking.
  - Quiet hours 21:00–09:00.
  - Check-in 14:00–20:00.
  - Invoices (**ask Monique** what's provided).
  - Single-occupancy rates from R638.
  - Location for the Kouga area: Humansdorp is about 15 minutes' drive (light mention).
  - Longer-stay or group bookings: different policies apply for more than 2 rooms.
- Schema: `WebPage` + `FAQPage` + `BreadcrumbList`.

**/af/**
- Title: e.g. `Verblyf in Jeffreysbaai | Greystone Gastehuis B&B`
- An Afrikaans version of the home page content (not word-for-word; natural Afrikaans), `<html lang="af">`.
- `hreflang`:
  - every page with an Afrikaans equivalent gets `en-ZA` + `af` + `x-default` links;
  - the home page gets `hreflang="af"` pointing at `/af/`, and `/af/` points back.
- Mark it clearly for Monique's review. Don't machine-translate place names (Jeffreysbaai is the Afrikaans name).

---

## 4. Shared structure: build this first

1. **`css/site.css`:** shared styles for all new pages, derived from `index.html`'s styles so the look matches.
   - Tokens: `--ink #080808`, `--surface #111`, `--surface-2 #181818`, `--gold #C9A96E`, `--gold-light #E8D5B0`, `--cream #F5F0E8`, `--muted #7A7567`, borders.
   - Fonts: Cormorant Garamond (display) and Inter (body).
   - Classes to carry over: `.eyebrow`, `.display`, buttons `.btn-gold` / `.btn-outline` / `.btn-whatsapp`, nav, footer, FAQ `details` styling.
   - Add: a page hero (shorter than the home hero), a readable article column (~70ch), cards, tables, breadcrumbs.
2. **`js/site.js`:** nav scroll effect, reveal-on-scroll, **mobile menu**, and the **conversion-tracking click handler** (copy from `index.html`, event names unchanged; see §5).
3. **Navigation**, identical on every page, including `index.html` and `reviews.html`:
   - Items: Rooms (`/rooms/`) · Surf (`/surf-accommodation-supertubes/`) · Things to do (`/things-to-do-jeffreys-bay/`) · Restaurants (`/restaurants-jeffreys-bay/`) · Reviews (`/reviews.html`) · AF (`/af/`) · WhatsApp · **Book Now**.
   - Use root-relative links (`/rooms/`), because pages now live in subfolders. `reviews.html`'s nav currently uses the relative `reviews.html`.
   - Mark the current page with `aria-current="page"`.
   - **Fix mobile:** today, below 768px, every nav item except Book Now is hidden, so phone users can't navigate (checked with Playwright on 21 Oct 2026). Add a hamburger menu button (`aria-expanded`, `aria-controls`, Esc closes, focus handling) that opens the full list. Keep Book Now visible in the bar.
4. **Footer** on every page: brand blurb, an "Explore" list (all pages, including Business travel and FAQ), the address (11 Mimosa Street, Wavecrest, Jeffreys Bay, 6330), check-in/out times, and languages.
5. **Images:** absolute paths (`/images/...`), `<picture>` with WebP and JPG, `width`/`height`, `loading="lazy"` below the fold, and descriptive alt text that includes "Jeffreys Bay" where natural. Only the photos in `images/` exist. Don't hotlink or invent others; leave a clearly marked placeholder or reuse an existing photo where one is needed.
6. **`index.html` and `reviews.html`:** keep their own inline styles (they work). Only swap the nav/footer markup and link `css/site.css` + `js/site.js` for the shared nav/menu. Check nothing else changes visually.

---

## 5. Must keep (don't break)

- **Tracking head block:** copy it **exactly** from `index.html` lines 6–46 into every new page's `<head>`:
  - the `?notrack` opt-out and the bot filter (Singapore/China time zones; `?sa=X&ved=` with no referrer);
  - GA4 `G-LHN8DCK50B`;
  - Clarity `yzbe0qilo7`.
- **Event names:** `begin_booking` (NightsBridge links), `contact_whatsapp` (wa.me links), `view_reviews`, `click_booking_com`, `click_tripadvisor`, `navigate_section`. The weekly and monthly reports in `../analytics-data/scripts/` count `begin_booking` and `contact_whatsapp`.
- **Booking link:** `https://book.nightsbridge.com/20319`. WhatsApp: `https://wa.me/27829537641`. Phone: +27 82 953 7641.
- **Wording rule (PR #5, 21 Oct 2026):** say "Port Elizabeth (Gqeberha)" for the city and airport. The airport is Chief Dawid Stuurman International Airport, **64 km, about 1 hour**.
- **Prices:** use the figures from `../CLAUDE.md` (ZAR, incl. taxes): Deluxe R1,275 (2 guests) / R723 (1); Standard and Budget R1,105 / R638. Say "from" and link to live availability; don't promise rates.
- **Breakfast:** rates are room-only; a full cooked breakfast is available to order (that's what the home page FAQ says). Don't say "breakfast included".
- **Ratings:** Booking.com 8.4 (462 reviews), TripAdvisor 4.5 (135 reviews), Google 4.2. Copy these from the home page if quoted.
- **Home page `BedAndBreakfast` schema** `@id`: `https://greystoneguesthouse.co.za/#lodging`. New pages reference it rather than redefining it.

---

## 6. Technical SEO checklist (every page)

- [ ] Unique `<title>` (≤ 60 chars) and meta description; one H1; logical H2/H3.
- [ ] `<link rel="canonical">` (absolute URL with trailing slash); `hreflang` where an `af` version exists.
- [ ] Open Graph and Twitter tags (reuse the home page pattern; `og:image` from `/images/`).
- [ ] JSON-LD as specified in §3, plus `BreadcrumbList`. Check it parses (Python `json.loads` on each block) and passes https://validator.schema.org.
- [ ] Internal links:
  - every new page links to /rooms/ and Book Now;
  - the guide links to restaurants and surf, and they link back;
  - the home page's Rooms section gets "See all rooms & rates →" `/rooms/`, and its Location section gets "Full Jeffreys Bay guide →";
  - descriptive anchor text, never "click here".
- [ ] `sitemap.xml`: add every new URL with `lastmod`, and image entries for the room photos.
- [ ] Fast: no new frameworks or large JS; fonts loaded as on the home page; WebP images.
- [ ] Accessible: alt text, contrast, focusable menu, `lang` attribute.
- [ ] Nothing in `.claude/` or `*.md` gets linked from pages.

---

## 7. Facts

**Confirmed:** in `../CLAUDE.md`, or checked on 21 Oct 2026 as noted.

- 260 m to the beach; 300 m to Supertubes; Wavecrest (behind the Spar); a supermarket and restaurants within 100 m.
- Nearby, converted from Booking.com's figures:

  | Place | Distance |
  |---|---|
  | Point Beach | ~450 m |
  | Dolphin Beach | ~1.1 km |
  | Kabeljous Beach | ~2.1 km |
  | Pellsrus Beach | ~3.5 km |
  | Aston Bay Beach | ~6.8 km |
  | Shell Museum | ~2.7 km |
  | Kabeljous Nature Reserve | ~5.3 km |
  | Seekoeirivier Nature Reserve | ~7.6 km |
  | Train station | ~4.2 km |
  | Hyper Cafe & Bar | ~90 m |
  | Nina's Real Food | ~275 m |
  | Quitschy's Pizza | ~365 m |

- **Nina's Real Food:** 126 Da Gama Road, Wavecrest Centre; ninas.co.za; 4.4★ on TripAdvisor (1,442 reviews), checked 21 Oct 2026. Don't publish opening hours.
- Other restaurants named by Jeffreys Bay Tourism (Facebook, checked 21 Oct 2026): Tasty Table Cafe, Kitchen Windows Beach Restaurant, Seashells Strandloper, Jolly Dolphin, Jeffrey's Bay 60's Diner, De Viswijf. **Monique to confirm** which to include and add her favourites.
- **J-Bay Open (WSL Championship Tour):** 10–20 July 2026 at Supertubes, alongside the J-Bay Surf Festival (Jeffreys Bay Tourism / WSL, checked 21 Oct 2026). WSL's site also lists a "Corona Cero Open J-Bay" 16–25 Oct 2026. Treat event dates as changing every year: write "usually in July" and link to the WSL site rather than hard-coding dates.
- **Beginner surf lessons:** Wavecrest Surf School (wavecrestsurfschool.co.za) teaches at **Kitchen Windows** on Dolphin Beach, lessons from R400 (their site, checked 21 Oct 2026). Learn 2 Surf also teaches at Kitchen Windows. Supertubes is for experienced surfers.
- **Drive times:**

  | To | Distance and time | Source |
  |---|---|---|
  | Addo Elephant National Park | ~105–117 km, about 1¼–1½ hours | SANParks / Rome2Rio |
  | Tsitsikamma (Storms River) | ~110 km, about 1¼ hours | Jeffreys Bay Tourism says "about an hour" |
  | Humansdorp | about 15 minutes | Shaun's light-mention wording |
  | Port Elizabeth (Gqeberha) airport | 64 km, about 1 hour | |

- **Facilities:** see "Key Features" in `../CLAUDE.md`. Includes billiards/games room, outdoor fireplace, BBQ, shuttle service (extra charge), grocery deliveries (extra), daily housekeeping, safety deposit box, alarm, and solar + inverter + battery.
- **House rules:** check-in 14:00–20:00, check-out 07:00–10:00, 18+ unless with a guardian, no pets, no smoking, no parties, quiet hours 21:00–09:00, payment by bank transfer before arrival, cards Visa/Mastercard, no cash.

**Unconfirmed: don't state as fact.** Write neutral wording and add each to the Monique review list (§9):

- surfboard storage and rinsing;
- early breakfast times;
- invoices for business guests;
- airport shuttle price;
- St Francis Bay drive time (roughly 30–40 minutes);
- sandboarding operators;
- skydiving and horse-riding operators;
- the "best" beaches for swimming;
- any restaurant other than the three walking-distance ones.

**Never** invent reviews, awards, prices, opening hours, or "as seen in" claims.

---

## 8. How to work

1. **Git:** never commit to `main`; a hook blocks it. Branch (e.g. `site-restructure`), commit in logical steps, push, and open a PR with `gh pr create`. Shaun merges. The PR build runs the Pages workflow but deploys only from `main`.
2. **Superpowers:** use `brainstorming`, then `writing-plans`, then `executing-plans` / `subagent-driven-development`; `verification-before-completion` before calling it done.
3. **Playwright** (headless Chromium is set up in `.claude/settings.json`). Serve the folder (`python3 -m http.server 8000` from `website/`) and test `http://localhost:8000/...?notrack=1`:
   - every page at 390 px (mobile) and 1440 px (desktop), with screenshots;
   - mobile menu opens and closes, and every link works;
   - no console errors;
   - JSON-LD parses;
   - images load.

   If the Playwright MCP updates and asks for a newer browser, use its `browser_install` tool.
4. **After merge:**
   - check the live pages with `?notrack=1`;
   - submit the updated sitemap in Search Console (`sc-domain:greystoneguesthouse.co.za`) and request indexing for the new URLs;
   - add the new pages' target keywords to `../analytics-data/SEO/monthly-config.json` (`rank_keywords`) via a PR in that repo.

---

## 9. Monique review list

Create `../analytics-data/SEO/new-pages-review.md` (private repo, via a PR there). It lists, page by page, every statement she should check or fill in. Include:

- her favourite restaurants and beaches, and local tips;
- the unconfirmed facilities;
- photos she could take (each page would benefit from 1–2 real photos: the walk to Supertubes, the street, the braai area, the games room);
- the Afrikaans page wording.

Keep it in plain English, as a checklist she can work through.

---

## 10. Definition of done

- [ ] 6 new pages live in the structure above, with the shared CSS/JS, nav (working on mobile) and footer.
- [ ] Home, reviews and 404 pages use the new nav/footer and link into the new pages.
- [ ] Every page passes the §6 checklist; sitemap updated.
- [ ] Tracking unchanged and verified (GA4 events fire on Book Now and WhatsApp clicks).
- [ ] Playwright screenshots, mobile and desktop, checked for every page.
- [ ] Monique review list created.
- [ ] One PR for the website and one for the analytics repo (review list + rank keywords), with clear descriptions.
