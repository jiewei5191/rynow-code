# Product page two-column rebuild — BUILD NOTES

Date: 2026-11-14 (Sat) ~02:40–03:00 +08
Authorised by user: option C (product page first) for the visual upgrade.

## Draft theme

- **New draft: 190044602435 — "RYNOW - Product page two-column"** (role UNPUBLISHED)
- Duplicated from MAIN **189966123075** ("RYNOW - Product page two-column" branched from MAIN; the quiz draft 190037622851 was NOT touched)
- NEVER publish from this work; user publishes in Shopify admin when he decides.

## Preview links (draft only)

- AD600Pro II: https://rynow.co/products/godox-ad600pro-ii-outdoor-flash?preview_theme_id=190044602435
- Godox A2: https://rynow.co/products/godox-a2-smartphone-xenon-flash-ttl-hss-1-8000s-magnetic-flash-with-bi-color-led-light?preview_theme_id=190044602435
  (NOTE: the A2 handle is NOT `godox-a2` — verified via Shopify API. `/products/godox-a2` is a 404.)

## What changed (2 files, draft only)

### 1. `sections/product-information.liquid` — 14,139 → 13,143 bytes (−996)
- REMOVED the entire custom CSS block commented `/* RYNOW stacked product layout (desktop) */`:
  the `@media screen and (min-width: 750px)` rule that forced `.product-information__grid` to
  `grid-template-columns: 1fr`, media `width: min(1200px, 100%)` centred, details
  `width: min(900px, 100%)` centred + 40px top padding. That block was the whole cause of the
  single-column layout. It was the only `grid-template-columns` in the file (count 1 → 0).
- Everything else byte-identical, including ALL sticky-add-to-cart styles
  (`sticky-add-to-cart` occurrences: 42 before → 42 after).
- Verified by re-read after upsert: marker gone, byte length 13,143 exactly.

### 2. `templates/product.json` — 20,598 → 20,600 bytes
Three settings only (header-stripped JSON equality verified — no other diffs):
- section `main` settings `gap`: 0 → **40**
- block `product-details` settings `details_position`: flex-end → **flex-start**
- block `product-details` settings `sticky_details_desktop`: false → **true**
- Unchanged as instructed: `equal_columns` false, `desktop_media_position` left,
  media-gallery `constrain_to_viewport` true, `aspect_ratio` adapt, `media_fit` contain,
  thumbnails bottom, `enable_sticky_add_to_cart` true, product-details block `gap` 28 (different setting — left alone).

With the stacked CSS gone, Horizon's native grid takes over: media left + details right,
details `position: sticky` on desktop (via `sticky_details_desktop: true`) so the buy box
stays visible while the gallery scrolls.

## Before (live MAIN, AD600Pro II, 1919×998, verified 2026-11-14 02:39)

- Gallery 924×924px square centred; details column 898px wide centred; ~500px blank margins each side.
- First viewport = header + gallery only (88% of viewport). NO title, NO price, NO Add to cart without scrolling.

## After — VISUAL VERIFICATION STILL PENDING (browser task)

- Text fetch of the draft preview (browser.open) confirms the page renders with no errors:
  title + RM2,559/RM3,199 present, all sections render. But a text fetch CANNOT prove layout.
- Still to verify in a real browser at desktop 1920px on the AD600Pro II preview link:
  1. Two-column layout (gallery left, details right) — measure column widths.
  2. Title + price + Add to cart visible in the FIRST viewport.
  3. Details column sticks while the gallery scrolls.
  4. Sticky add-to-cart bar: does it appear after scrolling past the buy box? (See finding below.)
  5. Spot-check A2 page (handle above) + one mobile viewport (~390px) for breakage.

## Sticky add-to-cart bar — finding (static code analysis, ~10 min)

- The bar IS in the DOM (`<sticky-add-to-cart>`, bar `data-stuck="false"` initially).
- Trigger logic in `assets/sticky-add-to-cart.js` is INTACT: an IntersectionObserver watches the
  `.buy-buttons-block`; when it scrolls above the viewport the bar shows (`data-stuck="true"`);
  a second observer hides it near the footer. Nothing in that logic is broken.
- **The bar is deliberately suppressed whenever Shopify Inbox chat is active.** The component's
  `#isChatActive()` returns true when the `shopify-chat` custom element is defined AND a
  `<shopify-chat>` element exists in the DOM — both are true on this store (Inbox installed,
  live chat button visible, `chat-drawer.liquid` renders `<shopify-chat>` unconditionally).
  The show path returns early (`if (this.#isChatActive()) return;`), and a `whenDefined` handler
  hides the bar if it ever appeared before the chat bundle loaded. The code comment states the
  intent: the bar must not overlap the chat UI.
- So: **not a broken observer — intended theme behaviour, caused by the live Inbox chat.**
  The browser verification (step 4 above) is the live confirmation: if the bar never appears on
  scroll in the draft preview either, this is confirmed.
- Options if Ray wants the bar: (a) accept the trade-off (remove/relocate chat — not recommended,
  chat is a sales channel); (b) patch the JS to allow the bar above the chat button; (c) leave it —
  with sticky details the buy box already stays visible on desktop, so the bar is largely redundant
  there; it only matters on mobile, where the chat gate suppresses it too. Do NOT rewrite the bar
  without a fresh decision.

## Files in this folder

- `ORIGINAL_sections_product-information.liquid` / `ORIGINAL_templates_product.json` — copies as read from the new draft before editing
- `EDITED_sections_product-information.liquid` / `EDITED_templates_product.json` — the versions upserted into the draft
- `assets_sticky-add-to-cart.js` — copy of the theme's sticky-bar component (read for the investigation)
- `upsert.py` — themeFilesUpsert helper (variables-based, retries empty stdout ×3)
- `BUILD-NOTES.md` — this file
