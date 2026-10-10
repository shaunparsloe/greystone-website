# SEO Audit & Optimization Prompt

Act as a senior technical SEO engineer and full-stack web developer. Audit and optimize my website's codebase for maximum search engine visibility, indexing, and performance based on the following requirements:

## 1. Crawling & Indexing
- Remove unintended `noindex` tags across public production pages.
- Generate a clean, dynamic `sitemap.xml` and configure a valid `robots.txt` file.
- Implement correct self-referencing `canonical` tags across all URLs.
- Provide step-by-step setup instructions to verify the domain in Google Search Console.

## 2. On-Page & Semantic HTML
- Ensure each page contains strictly one `<h1>` tag, with a logical heading hierarchy (`<h2>` through `<h6>`).
- Generate optimized, keyword-relevant meta titles and meta descriptions for all main routes.
- Add descriptive `alt` attributes to every `<img>` element.
- Implement structured data via JSON-LD schema markup (e.g., Organization, WebSite, BreadcrumbList, Article/Product).
- Configure Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`) for social previews.

## 3. Architecture & Linking
- Clean and normalize all URL slugs (lowercase, hyphen-separated, free of special characters or parameters).
- Scan for and eliminate all broken links (404s).
- Implement a logical internal linking structure to distribute page authority effectively.
- Outline an actionable backlink acquisition strategy tailored to this project's niche.

## 4. Performance & Technical Delivery
- Optimize Core Web Vitals (LCP, INP, CLS) through lazy loading, font preloading, and script deferral.
- Compress and convert images to modern formats (WebP/AVIF) with explicit width and height dimensions.
- Enforce strict HTTPS redirection and configure security headers.
- Audit and resolve all mobile responsiveness issues, ensuring clean layouts across all viewport sizes.

Review the project files, list identified issues, and implement the necessary code changes and configuration updates directly.
