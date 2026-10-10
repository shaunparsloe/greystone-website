# SEO Audit — greystoneguesthouse.co.za

Audit date: 10 October 2026 · Scope: `website/` (static site on GitHub Pages) · Brief: [`seo-audit-prompt.md`](seo-audit-prompt.md)

## Summary

The site was already in good shape: one `<h1>` per page, canonicals, Open Graph, FAQ/Lodging schema, alt text on every image, valid robots.txt and sitemap, and HTTPS enforced. The main problems were **wrong map coordinates in the structured data**, a **broken image reference in the schema**, **no booking button in the mobile header**, **room "Book this room" links invisible on touch screens**, and **render-blocking fonts / no modern image formats**.

The biggest remaining SEO opportunity is not technical: the site has only two indexable pages. More pages targeting real searches (see [Internal linking & content](#3-architecture--linking)) will do more than any further code tweaks.

---

## 1. Crawling & Indexing

| Check | Finding | Action |
|---|---|---|
| `noindex` tags | None on public pages | Added explicit `index, follow, max-image-preview:large` to both pages. The new `404.html` is `noindex`. |
| robots.txt | Valid, allows everything, points to sitemap | No change needed |
| sitemap.xml | Valid but stale `lastmod`; `changefreq`/`priority` are ignored by Google | Refreshed dates, removed ignored tags, added image entries for the homepage photos |
| Canonicals | Correct and self-referencing on both pages | No change. Internal links on reviews page now point to `/` instead of `index.html`, so the duplicate `/index.html` URL is no longer linked. |
| 404 page | GitHub Pages default 404 (no way back to the site) | Added branded `404.html` with links to Home, Rooms, Reviews, Book Now |

**Sitemap "dynamic" note:** with a static site there's nothing to generate dynamically. Update `lastmod` when you change a page, and add a `<url>` entry for every new page.

### Google Search Console setup

1. Go to <https://search.google.com/search-console> and sign in with the Google account that owns the Google Business Profile.
2. Click **Add property** → choose **Domain** → enter `greystoneguesthouse.co.za`.
3. Google shows a **TXT record** (`google-site-verification=...`). Copy it.
4. Log in to the domain registrar / DNS host for `greystoneguesthouse.co.za` and add a **TXT** record on the root (`@`) with that value. Keep the existing GitHub Pages A/CNAME records untouched.
5. Back in Search Console, click **Verify**. DNS can take from a few minutes to a few hours.
6. Once verified: **Sitemaps** → submit `https://greystoneguesthouse.co.za/sitemap.xml`.
7. **URL Inspection** → paste the homepage URL → **Request indexing**. Repeat for `/reviews.html`.
8. Check **Enhancements** after a few days for FAQ / Breadcrumb / Review snippet reports, and **Page experience → Core Web Vitals** after a few weeks of traffic.
9. Optional: in **Bing Webmaster Tools** choose "Import from Google Search Console" — two clicks, covers Bing/DuckDuckGo/ChatGPT search.

*Alternative if DNS access is a hassle:* choose **URL prefix** instead, pick **HTML tag**, and I can add the `<meta name="google-site-verification">` tag to `index.html`.

---

## 2. On-Page & Semantic HTML

| Check | Finding | Action |
|---|---|---|
| One `<h1>` per page | ✅ Both pages | — |
| Heading hierarchy | Homepage host section used a `<p>` as its heading (`aria-labelledby` pointed at it) | Changed to `<h2>` with the same styling |
| Meta titles | Good, keyword-led, ~70 chars | No change |
| Meta descriptions | Homepage was ~240 chars (Google truncates at ~155) | Rewritten to ~150 chars on both pages, keeping "Jeffreys Bay", "Supertubes", price and "Book direct" |
| `meta keywords` | Ignored by Google; only shows competitors your keyword list | Removed |
| Alt text | ✅ Every `<img>` has descriptive alt | — |
| **Structured data — coordinates** | **Homepage had `-34.0488, 25.5304` (≈55 km east, near Gqeberha); reviews page had `-33.9308, 24.9355` (≈11 km north).** Both pages also disagreed with each other. | Set both to `-34.0331, 24.9295`, the Google Maps pin for 11 Mimosa St, Wavecrest. |
| Structured data — broken image | Schema listed `images/541777001.jpg`, which doesn't exist | Removed |
| Structured data — entity linking | Two separate LodgingBusiness blocks with no shared ID | Added `@id: …/#lodging` to both so Google treats them as one business; added Facebook to `sameAs` |
| WebSite schema | Missing (helps Google show "Greystone Guesthouse" as the site name in results) | Added |
| Homepage BreadcrumbList | Single-item breadcrumb — no value | Replaced by WebSite schema. Reviews page breadcrumb (2 items) kept. |
| Open Graph | Present, but declared image size 1200×630 when the file is 1024×461 | Corrected dimensions, added `og:image:alt` / `twitter:image:alt`, added size tags to reviews page |
| Favicon | None (browsers request `/favicon.ico` → 404 on every visit) | Added `favicon.svg` (gold "G" on black) |

---

## 3. Architecture & Linking

| Check | Finding | Action |
|---|---|---|
| URL slugs | `/` and `/reviews.html` — lowercase, clean, no parameters | Kept. Renaming `reviews.html` → `/reviews/` would need a 301 redirect, which GitHub Pages can't do; the gain isn't worth losing existing indexing. Use folder-style URLs (`/rooms/`) for new pages. |
| Broken links | All internal links, anchors and assets resolve. External Nightsbridge, Booking.com, WhatsApp and Facebook links return 200/redirect correctly. | — |
| Logo links | `href="#"` on homepage | Changed to `/` |
| Internal links | Reviews page nav had no "Reviews" item; FAQ not linked from footer | Added Reviews to reviews-page nav (`aria-current`), FAQ link to both footers |
| Analytics label | CTA labelled "Book … on Booking.com" but links to Nightsbridge (pollutes GA4 event labels) | Relabelled "Book Greystone Guesthouse direct" |

### Recommended new pages (highest SEO impact)

Each should link back to the homepage and booking, and be linked from the nav/footer and sitemap:

1. **`/rooms/`** (or one page per tier) — full descriptions, more photos, prices, amenities. Targets "sea view rooms Jeffreys Bay", "budget accommodation Jeffreys Bay".
2. **`/surf/`** — "Accommodation near Supertubes": walking route, best season, surf schools, board hire, the J-Bay Open. Surfers are a core segment and this is a high-intent search.
3. **`/jeffreys-bay-guide/`** — things to do, restaurants, Addo day trips, getting there from Gqeberha airport. Earns links from other sites and captures planning-stage searches.
4. **`/business-travel/`** — WiFi, solar backup, quiet hours, invoices. Targets Eastern Cape contractors and corporate guests.
5. **Afrikaans version** (`/af/`) of the homepage with `hreflang` tags — a meaningful share of domestic travellers search in Afrikaans and there's little competition.

### Backlink strategy (J-Bay guesthouse niche)

Ordered by effort-to-value. Avoid paid link schemes — they risk a Google penalty.

1. **Own every free listing, with the website link filled in:** Google Business Profile (add the URL and booking link), Facebook page "Website" field, TripAdvisor (management centre → website), Booking.com/SafariNow property profiles where allowed, TGCSA grading listing.
2. **SA travel directories:** LekkeSlaap, TravelGround, SafariNow, AA Travel, Afristay, Jeffreys Bay Tourism / Kouga tourism listings. Consistent name, address and phone (NAP) everywhere matters as much as the link.
3. **Local partner swaps:** surf schools, board-hire shops, skydive and horse-riding operators, Addo tour operators, restaurants within walking distance (Nina's, Quitschy's). Offer a "recommended stay" mention for a "local partners" mention, or a guest discount code — real referral value, not just a link.
4. **Event pages:** the J-Bay Open (WSL) and local festivals/marathons usually publish accommodation lists for competitors, media and spectators. Get on them ahead of each season.
5. **Content that earns links:** the J-Bay guide and surf pages above. Pitch them to surf forums, travel bloggers and Garden Route / Eastern Cape itinerary writers.
6. **Local press:** the solar/no-loadshedding angle, Monique's 30 years in hospitality, or a community story suits local papers and *Getaway* magazine's accommodation round-ups.
7. **Reviews → visibility:** keep asking happy guests for Google reviews (current 4.2★ / 185 is the weakest score). A QR card in the rooms linking to the Google review form helps local pack rankings directly.

---

## 4. Performance & Technical Delivery

| Check | Finding | Action |
|---|---|---|
| LCP (hero image) | Hero is a CSS background, so the browser only discovers it after parsing CSS | Added `<link rel="preload" … fetchpriority="high">` for the hero |
| Render-blocking fonts | Google Fonts stylesheet blocked first paint | Switched to non-blocking `preload` + `onload` swap with `<noscript>` fallback (`display=swap` already set) |
| Image formats | JPG only | Generated WebP for all 11 images (**~25–45% smaller**, e.g. hero 44 KB → 25 KB). `<img>` tags now use `<picture>` with WebP + JPG fallback; CSS backgrounds use `image-set()` with JPG fallback. AVIF skipped — the extra gain on files this small doesn't justify doubling assets. |
| Image dimensions (CLS) | Declared `width`/`height` didn't match the files (e.g. room photos declared 700×1050, actually 1024×461) | Set to real dimensions; added `decoding="async"` |
| Lazy loading | ✅ Already on all below-the-fold images | — |
| Script deferral | GA is `async`; inline scripts are at the end of `<body>` | No change needed |
| HTTPS | ✅ `http://` and `www.` both 301 → `https://greystoneguesthouse.co.za/` | Confirm **Settings → Pages → Enforce HTTPS** stays ticked |
| Security headers | GitHub Pages sends none and doesn't allow custom headers | Added `<meta name="referrer">`. For real headers see below. |
| **Mobile header** | **All nav links (including Book Now) hidden below 768px — mobile visitors had no booking button in the header** | Book Now now stays visible on mobile, other links collapse (both pages) |
| **Room cards on touch** | **"Book this room →" only appeared on hover, so it was invisible on phones/tablets** | Always visible on touch devices (`hover: none`), and on keyboard focus |
| Reviews page tablet nav | Nav items could crowd between 600–768px | Collapses at 768px, matching the homepage |

### Security headers (optional, requires a DNS change)

To get HSTS, `X-Content-Type-Options`, `Permissions-Policy`, etc., put the domain behind **Cloudflare's free plan**: move the nameservers to Cloudflare, keep the GitHub Pages records, and add a *Transform Rule → Modify response header* for:

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
X-Frame-Options: SAMEORIGIN
```

This affects SEO only marginally. Do it for security hygiene, not rankings, and don't enable HSTS `preload` unless you're sure HTTPS will never be dropped.

---

## Open items for you

1. **Higher-resolution photos.** Every image is ≤1024px wide, so the full-screen hero and CTA banner look soft on laptops and large phones. Originals at ≥1920px (hero) and a 1200×630 crop for social sharing would help both quality and click-through.
2. ~~**Check the rating figures**~~ **Done (10 Oct 2026):** checked live listings. TripAdvisor is **4.5/5, 135 reviews, #14 of 50** (site was right on 4.5; notes were out of date). Booking.com is **8.4, 462 reviews** (both 499 and 487 were stale — Booking.com drops reviews older than ~36 months). Updated `index.html`, `reviews.html` and `CLAUDE.md`.
3. **Review stars in Google:** the `aggregateRating` markup is valid, but Google doesn't show review stars for a business rating itself on its own site. It's harmless to keep; just don't expect stars in results from it.
4. **Visual check on a phone:** I couldn't render the pages in a browser here. Please load the preview on a phone and confirm the header Book Now button and room cards look right.

## Files changed

- `website/index.html` — meta, schema, fonts, preload, `<picture>`/WebP, mobile nav, touch CTAs, heading, links
- `website/reviews.html` — meta, schema, fonts, links, mobile nav
- `website/sitemap.xml` — refreshed with image entries
- `website/404.html` — new
- `website/favicon.svg` — new
- `website/images/*.webp` — 11 new WebP files
