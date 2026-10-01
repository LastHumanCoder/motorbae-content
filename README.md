# MotorBae — October 2026 blogs (Shopify)

Ten Shopify-ready blog posts for **The Garage** on [motorbae.store](https://motorbae.store), written from the October 2026 content calendar.

**Live previews:** https://lasthumancoder.github.io/motorbae-content/ (previews are `noindex`; the real posts go on motorbae.store)

| Date | Post | Shopify handle | Primary keyword | Words | Store links | Product images | Files |
|---|---|---|---|---:|---:|---:|---|
| 2026-10-06 | [Best Hoodies for Men in India (2026)](best-hoodies-for-men-india-2026.html) | `best-hoodies-for-men-india-2026` | hoodies for men | 1,715 | 16 | 7 | [raw](raw/best-hoodies-for-men-india-2026.html) · [fields](shopify/best-hoodies-for-men-india-2026.json) · [cover](covers/best-hoodies-for-men-india-2026.png) |
| 2026-10-07 | [Best Diwali Gifts for Car Lovers India (2026)](best-diwali-gifts-for-car-lovers-india-2026.html) | `best-diwali-gifts-for-car-lovers-india-2026` | diwali gifts for car lovers | 1,550 | 31 | 13 | [raw](raw/best-diwali-gifts-for-car-lovers-india-2026.html) · [fields](shopify/best-diwali-gifts-for-car-lovers-india-2026.json) · [cover](covers/best-diwali-gifts-for-car-lovers-india-2026.png) |
| 2026-10-08 | [Best Full Sleeve T-Shirts for Men in India (2026)](best-full-sleeve-t-shirts-for-men-india-2026.html) | `best-full-sleeve-t-shirts-for-men-india-2026` | full sleeve t shirts for mens | 1,573 | 18 | 7 | [raw](raw/best-full-sleeve-t-shirts-for-men-india-2026.html) · [fields](shopify/best-full-sleeve-t-shirts-for-men-india-2026.json) · [cover](covers/best-full-sleeve-t-shirts-for-men-india-2026.png) |
| 2026-10-12 | [Best Cargo Pants for Men in India (2026): Complete Style Guide](best-cargo-pants-for-men-india-2026.html) | `best-cargo-pants-for-men-india-2026` | cargo pants for men | 1,550 | 20 | 7 | [raw](raw/best-cargo-pants-for-men-india-2026.html) · [fields](shopify/best-cargo-pants-for-men-india-2026.json) · [cover](covers/best-cargo-pants-for-men-india-2026.png) |
| 2026-10-15 | [Best Jacket for Men in India (2026): Riding, Casual & Streetwear](best-jacket-for-men-india-2026.html) | `best-jacket-for-men-india-2026` | jacket for men | 1,572 | 17 | 8 | [raw](raw/best-jacket-for-men-india-2026.html) · [fields](shopify/best-jacket-for-men-india-2026.json) · [cover](covers/best-jacket-for-men-india-2026.png) |
| 2026-10-16 | [Best Sweater for Men in India (2026)](best-sweater-for-men-india-2026.html) | `best-sweater-for-men-india-2026` | sweater for men | 1,513 | 16 | 7 | [raw](raw/best-sweater-for-men-india-2026.html) · [fields](shopify/best-sweater-for-men-india-2026.json) · [cover](covers/best-sweater-for-men-india-2026.png) |
| 2026-10-16 | [Best Winter Outfits for Men in India (2026): Complete Style Guide](best-winter-outfits-for-men-india-2026.html) | `best-winter-outfits-for-men-india-2026` | winter outfits for men | 1,523 | 28 | 7 | [raw](raw/best-winter-outfits-for-men-india-2026.html) · [fields](shopify/best-winter-outfits-for-men-india-2026.json) · [cover](covers/best-winter-outfits-for-men-india-2026.png) |
| 2026-10-19 | [Best Gifts for Him in India (2026): Car & Bike Lover Edition](best-gifts-for-him-india-2026.html) | `best-gifts-for-him-india-2026` | gifts for him | 1,509 | 32 | 7 | [raw](raw/best-gifts-for-him-india-2026.html) · [fields](shopify/best-gifts-for-him-india-2026.json) · [cover](covers/best-gifts-for-him-india-2026.png) |
| 2026-10-21 | [Automotive T-Shirts India: Best Brands & Where to Buy (2026)](automotive-t-shirts-india-2026.html) | `automotive-t-shirts-india-2026` | automotive t shirts | 1,525 | 27 | 8 | [raw](raw/automotive-t-shirts-india-2026.html) · [fields](shopify/automotive-t-shirts-india-2026.json) · [cover](covers/automotive-t-shirts-india-2026.png) |
| 2026-10-23 | [Best Track Pants for Men in India (2026)](best-track-pants-for-men-india-2026.html) | `best-track-pants-for-men-india-2026` | track pants for men | 1,510 | 17 | 7 | [raw](raw/best-track-pants-for-men-india-2026.html) · [fields](shopify/best-track-pants-for-men-india-2026.json) · [cover](covers/best-track-pants-for-men-india-2026.png) |

The two **Technical Audit** rows in the calendar (Oct 14, Oct 27) are site checks, not posts, so they are not in this batch.

## How a Shopify blog post differs from our WordPress / StoreBox blocks

Shopify renders the article body (`article.content`) unescaped inside the theme, so the post is one self-contained HTML fragment. What is specific to Shopify, based on MotorBae's own live posts and the reference file:

1. **Schema lives in the body.** Two `<script type="application/ld+json">` blocks (BlogPosting + FAQPage) sit at the top of the article HTML. Shopify keeps them. WordPress/Elementor blocks carried one FAQPage block; StoreBox put FAQ schema in metadata.
2. **One scoped `<style>` block** (`.mb-post …`) right after the schema. Shopify keeps it, unlike some StoreBox themes that strip or re-render posts that contain `<style>`.
3. **The theme prints the H1 and the featured image.** The post repeats the title visually as `<p class="post-h1">`, never `<h1>`, so the page keeps exactly one H1. Upload `covers/<handle>.png` as the article's featured image.
4. **Shopify URL shapes.** Products `/products/<handle>`, collections `/collections/<handle>`, posts `/blogs/the-garage/<handle>`. Every link here comes from the store's own public catalogue (`/products.json`, `/collections.json`, the blog feed) and was checked live (119 URLs, all 200).
5. **Images come from the store's own CDN** (`motorbae.store/cdn/shop/files/…&width=`), i.e. MotorBae's real product photos, never stock or AI images in the body.
6. **Paste bugs to avoid.** The reference file contained a stray `</head><body>`, and the live September posts carry hundreds of `bis_size="…"` attributes added by a browser extension during copy-paste. These posts contain neither; the build refuses to output them.

## Publishing a post in Shopify

1. **Online Store → Blog posts → Add blog post.**
2. **Title:** from `shopify/<handle>.json` → `title`.
3. In the content editor click **Show HTML** (`<>`), then paste the whole of `raw/<handle>.html`.
4. **Featured image:** upload `covers/<handle>.png`.
5. **Excerpt:** `excerpt` from the JSON.
6. **Search engine listing:** page title = `seo_title`, meta description = `seo_description`, URL handle = `handle`.
7. **Blog:** The Garage. **Tags:** `tags`. Set the publish date from `published`.
8. Publish, then open the live URL on a phone and check the product cards and FAQ.

Publish in calendar order. The posts link to each other at their final URLs, so a link to a post that is not published yet will 404 until it goes live.

## What every post was checked for

The build (`writer/build.py`) refuses to write a post unless all of these pass:

- **MotorBae is the #1 recommendation.** The first ranked card is the MotorBae top pick, and the quick answer names MotorBae first.
- **No invented prices.** Every ₹ figure must be a real catalogue price or one of the store's own price bands (Under ₹699/₹999/₹1,499). Competitors are described qualitatively, with no prices.
- **No invented products.** A sentence may not claim MotorBae sells jackets, sweaters, cargo pants, track pants, polos, full-sleeve or zip pieces (it sells none of these; see below).
- **Real links only:** at least 12 internal links per post (at least 5 products, 3 collections and 3 blog posts), all from the live catalogue. No self-links.
- **Real product images:** at least 5 per post, all from MotorBae's store. Each alt text describes what is literally in the photo, and no image repeats within a post.
- **Format:** 5 FAQs matching the FAQPage schema, no `<h1>`, no document tags, no em-dashes, no statistics, 1,500 to 2,500 words, keyword in the meta description, natural keyword density, supporting keywords present.
- **Layout:** every post was rendered inside MotorBae's live theme at 390px and 1280px. All pass with no sideways scroll, no clipped text, no broken images, one H1 and a smallest text size of 12px.

## Honest positioning: where MotorBae does not sell the product

Five calendar topics are categories MotorBae does not make: jackets, sweaters, cargo pants, track pants and full-sleeve tees. MotorBae is still the #1 pick in each, for the job it actually does, and each post says so plainly:

| Post | MotorBae's #1 role | What the post says plainly |
|---|---|---|
| Full sleeve t-shirts | Printed regular-fit tees for layering | Tees are half sleeve; Uniqlo, H&M, Jockey and Decathlon for full sleeve |
| Cargo pants | Oversized tees and hoodies to wear on top | No MotorBae cargos; cargo brands covered |
| Jacket | Heavy hoodie + balaclava as the layer under a riding jacket | No MotorBae jackets; a hoodie is never protection |
| Sweater | Heavy hoodies as the casual alternative | No knitwear; merino and wool brands for smart wear |
| Track pants | MB Essentials sweatpants (260 GSM terry) | No polyester track pants or tracksuits |

## Rebuilding

Prices and stock change, so rebuild before publishing if more than a few days have passed:

```bash
python3 writer/harvest.py motorbae.store <client-dir>   # refresh catalogue
python3 writer/build.py <client-dir>                    # rebuild + gates
python3 writer/verify_live_theme.py                     # render inside the live theme
```

`writer/` holds the sources (`src/`), the stylesheet (`mb-post.css`, the September house CSS plus a product-card grid and mobile hardening), the catalogue snapshot (`data/catalog.json`, harvested 2026-10-01), the image alts (`data/alts.json`) and the cover generator. The writer is not MotorBae-specific: point `harvest.py` at another Shopify store and add a `client.json`.

## Notes for the MotorBae team

- **Clean up the September posts.** They contain `bis_size` attributes from a browser extension. These are harmless to visitors but bloat the HTML; re-paste those posts from a clean source.
- **No shipping policy page.** `/policies/shipping-policy` returns 404, so no post states delivery times. The returns and exchange facts (7 days, size exchanges, caps/hats/balaclavas non-returnable) come from `/policies/refund-policy`.
