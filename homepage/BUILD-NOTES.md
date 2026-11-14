# RYNOW - A2 hero — build notes

## Draft
- **190045716547 — "RYNOW - A2 hero"** (duplicated from MAIN 189966123075, UNPUBLISHED, never published)
- Preview: https://rynow.co/?preview_theme_id=190045716547

## Hero image (chosen from the A2 product media)
- **White A2, clean product shot on light grey** — MediaImage 46304291291203, 1024×1024
- https://cdn.shopify.com/s/files/1/0693/9230/2147/files/my-11134207-820l7-mu56rmx4o8aw23.jpg?v=1791651519
- Why: the only clean, real product photo in the A2 media — no baked text, no spec panels.
- Rejected: the official 4-colour poster (fa4c910c…png) — baked spec text AND says "Only 60g" (verified weight is 93g); the four Shopee images (mu56jylz6jno9b / mu56jylx5i4qe8 / mu56k5xdzmyre5 / mu56o78c5gqw60) are all dense infographics with baked headlines, model photos and spec panels.
- The photo is square, so the hero is a split editorial layout (text left, image right), in the style of the AD600Pro II spotlight. The 4 colour dots (White / Black / Burgundy / Sky Blue) carry the colour story — the photo itself shows White only.

## What changed (draft only)
1. **New section `sections/rynow-hero-a2.liquid`** — custom A2 hero, real text (not baked):
   - Eyebrow "Godox A2", headline "Stop Blaming Your iPhone.", subline "A real xenon flash for your phone. Not a LED."
   - Price RM271 (was RM339), 4 colour dots with labels, CTA "Shop A2" → A2 product page.
   - Light motion only: slow Ken Burns zoom on the image (26s alternate) + staggered fade/slide-in text on load; scoped to `.rynow-hero-a2`; disabled under `prefers-reduced-motion`.
   - Schema has an `image_picker` setting (no default — image value lives in `templates/index.json`); all other settings have defaults. If the image setting is blank, the section falls back to the hardcoded CDN URL above.
2. **`templates/index.json`** — `hero_fTpYRU` (expired 11.11 baked image, link to 11.11 collection) REPLACED by `rynow_hero_a2` in the first position; order otherwise unchanged.
3. **11.11 teardown (same draft):**
   - Grid `rynow_grid`: heading "11.11 Creator Deals — In Stock" → "Creator Deals — In Stock"; eyebrow "11.11 · 1–13 NOV" → "Storewide 20% off". Collection handle `11-11-creator-deals-in-stock` UNCHANGED.
   - Storewide banner `ai_gen_block_c6f988c_qE4bTk`: `date_text` "01–13 NOV 2026" → "STOREWIDE 20% OFF". Headline "Create more. Spend less.", benefit copy and brand discounts (20/20/20) unchanged.
   - Main menu: "11.11" item (MenuItem 662911582275) removed via API — see below.

## Menu outcome
- **DONE via API 2026-11-14:** "11.11" item (MenuItem 662911582275) REMOVED from the Main menu (gid 226615459907). Menu now has 7 items: What's New, Brands, Categories, Policies, Our Story, Contact Us, RYNOW Lab. Menus are live store data, so this is live (not draft-only). First attempt used the wrong mutation shape (`MenuUpdateInput` doesn't exist); the API error revealed the flat signature `menuUpdate(id, title, items)` and the corrected call succeeded.

## Image setting note (deviation from plan)
- The section has an `image_picker` setting, but the template JSON does NOT set it: `themeFilesUpsert` rejects a full CDN URL ("does not point to an applicable resource") AND `shopify://files/...` ("must be a valid shopify url") for `image_picker` values — only `shopify://shop_images/...` references pass, and the A2 photo lives in the Files library, not the theme image library. The section therefore renders the hardcoded CDN fallback URL (same pattern as the AD600Pro section, which hardcodes its image). The picker stays available in the theme editor — the owner can swap the image there (the editor's own pick flow stores a valid `shopify://shop_images` value).

## Verification (browser check, 2026-11-14 03:19, desktop 1919x998)
- First viewport PASS: hero fills it; eyebrow, headline "Stop Blaming Your iPhone.", subline, RM271/RM339, 4 colour dots, blue "Shop A2" pill all readable; image is the clean white A2 photo.
- "Shop A2" PASS: links to the correct A2 product page.
- "11.11" CLEAN: full-page text search returned zero matches (hero, nav, Creator Deals grid, storewide banner).
- A2 video banner PASS: renders and plays (86.4% of sampled pixels changed over 2s).
- Motion PARTIAL: slow zoom CONFIRMED by pixel measurement (9.2%/10.2%/10.9% change per 1.5s interval over ~6s). Text fade/slide-in not caught on camera — already complete before the first post-load frame (same screenshot-timing limit as the quiz motion); owner's eyes are the decisive check.
- Mobile ~390px UNVERIFIED: cloud browser cannot resize; owner to check on phone.

## Known gaps
- The A2 video banner (`hero_ftrfUy`, the A2 ad film) is KEPT further down the homepage — the new hero uses a photo, so the two A2 sections differ.
- The hero photo shows the White colourway only; the 4 colours are shown as dots.
- `sticky_details` on product pages is a separate open item (draft 190044602435).

## Lenis smooth scroll (added 2026-11-14, draft only)
- **Lenis v1.3.27** (MIT, darkroom.engineering) via jsDelivr CDN: `https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.min.js` (pinned; 200 OK verified 2026-11-14).
- Files added in draft 190045716547 (same draft as the A2 hero — no new draft created):
  - `assets/lenis.css` (513 bytes, exact lenis.css fetched from jsDelivr).
  - `snippets/lenis.liquid` (1,058 chars / 1,060 bytes) — script tag (`defer`) + init on window load: `autoRaf: true, duration: 1.15, smoothWheel: true`. Disabled when the visitor prefers reduced motion; no-ops if the CDN fails to load. Anchor links (`href="#..."`) smooth-scroll via `lenis.scrollTo` instead of jumping. Exposes `window.__rynowLenis` for verification.
  - `layout/theme.liquid` — `{{ 'lenis.css' | asset_url | stylesheet_tag }}` added in `<head>` right after the `stylesheets` render; `{% render 'lenis' %}` added just before `</body>`. Nothing else changed (7,102 → 7,178 chars / 7,186 bytes).
- `assets/base.css` NOT touched (A2-hero CSS stays as-is). MAIN theme 189966123075 NOT touched.
- Verification: all three files upserted + re-read from the draft, exact-match PASS (2026-11-14). Scroll feel NOT yet verified in a browser — parent to check on the preview link; mobile check by owner.

## GSAP ScrollTrigger homepage reveals (added 2026-11-14, draft only)
- **GSAP 3.12.5 core + ScrollTrigger 3.12.5** (free) via jsDelivr CDN, pinned, `defer`: `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js` and `.../dist/ScrollTrigger.min.js`.
- Files added in draft 190045716547 (same draft as A2 hero + Lenis — no new draft created):
  - `snippets/gsap-reveal.liquid` (2,062 chars / 2,064 bytes) — script tags + init on window load.
  - `layout/theme.liquid` — `{% if template.name == 'index' %}{% render 'gsap-reveal' %}{% endif %}` added just before `</body>`, after `{% render 'lenis' %}`. Nothing else changed (7,178 → 7,253 chars / 7,261 bytes).
- Behaviour: every homepage section EXCEPT the first (A2 hero, which already animates) fades + rises (y:24 → 0, opacity 0 → 1, 0.7s, power3.out), trigger `top 88%`, once only. Card grids inside a section (`.grid` / `.card-grid` / `.collection-grid` with ≥3 children, else `.card-wrapper` ≥3) stagger 0.08. Section order in `templates/index.json`: A2 hero (skipped) → AD600Pro II spotlight → categories → Creator Deals grid → deals block → New In → A2 video banner → Lux → trust → guides → brands.
- Safety: no content is ever hidden unless GSAP + ScrollTrigger actually loaded; CDN failure or `prefers-reduced-motion` leaves the page fully visible (no CSS hiding — initial state set via `gsap.from` only when GSAP is present). Deliberately NOT wired to Lenis (no ticker sync); ScrollTrigger reads native scroll positions while Lenis runs its own autoRaf loop.
- `assets/lenis.css` / `snippets/lenis.liquid` NOT touched. MAIN theme 189966123075 NOT touched.
- Verification: both files upserted + re-read from the draft, exact-match PASS (2026-11-14). Animation look/feel NOT yet verified in a browser — parent to check on the preview link; mobile check by owner.

## Scroll-reveal replaced: GSAP ScrollTrigger \u2192 IntersectionObserver + CSS (2026-11-14, draft only)
- **What failed:** browser verification 2026-11-14 15:45 \u2014 every homepage section below the hero stayed INVISIBLE (in the DOM, opacity 0); scrolling top-to-bottom (scrollbar drag + PageDown, 2s waits) showed blank white everywhere below the hero and the footer never appeared. The hero \u2014 the only section without a from-tween \u2014 rendered normally. The GSAP version hid sections with `gsap.from` (opacity 0) and its ScrollTriggers never fired, so content got stuck hidden. Patching the trigger mechanism was not worth another cycle.
- **Replacement:** `snippets/scroll-reveal.liquid` (3,551 chars / 3,553 bytes) \u2014 vanilla JS + CSS, no external library. IntersectionObserver triggers the reveal; CSS transitions animate (same look: fade + rise 24px, 0.7s, grid stagger 0.08s). `layout/theme.liquid` now renders `scroll-reveal` instead of `gsap-reveal` on the homepage (`{% if template.name == 'index' %}` guard kept; 7,253 \u2192 7,255 chars / 7,263 bytes).
- **Why it cannot get stuck hidden:** the hiding CSS only applies under an `html.js-reveal` class added by the JS itself; no-JS, `prefers-reduced-motion`, or an unsupported IntersectionObserver all leave the page fully visible. A 3s safety net reveals anything already in (or above) the viewport.
- `theme/snippets/gsap-reveal.liquid` is SUPERSEDED \u2014 left orphaned and unused in the theme (not deleted); do not re-render it.
- `assets/lenis.css` / `snippets/lenis.liquid` NOT touched. MAIN theme 189966123075 NOT touched.
- Verification: both files upserted + re-read from the draft, exact-match PASS (2026-11-14). Animation look/feel NOT yet verified in a browser \u2014 parent to check on the preview link; mobile check by owner.

## A2 before/after comparison slider (added 2026-11-14, draft only)
- **img-comparison-slider v8.0.7** (MIT, sneas) via jsDelivr CDN, pinned, `defer`: `https://cdn.jsdelivr.net/npm/img-comparison-slider@8.0.7/dist/index.js` (+ `.../dist/styles.css`, both 200 OK verified 2026-11-14). Dependency-free web component (`<img-comparison-slider value="50">`, `slot="first"` / `slot="second"`).
- Photos: cropped matched pairs from the official Godox A2 ad film (the same video already on the homepage), 3-panel "Without Flash / Smartphone Flash / A2 Flash" layouts. Framing is close but not pixel-perfect (different video moments) — used as-is.
  - Beach pair (used in the section): before https://cdn.shopify.com/s/files/1/0693/9230/2147/files/a2-compare-beach-before.jpg?v=1794653158 (MediaImage 46775174922307) / after https://cdn.shopify.com/s/files/1/0693/9230/2147/files/a2-compare-beach-after.jpg?v=1794653165 (MediaImage 46775175970883). 490x650.
  - Bar pair (uploaded, alternate): before https://cdn.shopify.com/s/files/1/0693/9230/2147/files/a2-compare-bar-before.jpg?v=1794653171 (MediaImage 46775177150531) / after https://cdn.shopify.com/s/files/1/0693/9230/2147/files/a2-compare-bar-after.jpg?v=1794653177 (MediaImage 46775177379907). 490x644.
- Files in draft 190045716547 (same draft as A2 hero + Lenis + scroll-reveal — no new draft created):
  - `sections/rynow-compare-a2.liquid` (new, 4,894 bytes) — eyebrow "Godox A2", headline "See the difference.", subline "Same scene. Left: phone only. Right: with the A2 xenon flash. Drag the handle." Labels "Without flash" / "A2 flash" as small dark pills. Divider/handle styled subtly via the component's CSS variables (white 2px divider, 46px white handle, soft shadow). No price, no sale badge, no urgency copy. Image pickers exposed for before/after (no defaults — picker values cannot be set via upsert); hardcoded CDN fallbacks (beach pair) render when blank. Gated on the A2 product handle so it renders nothing on other products.
  - `templates/product.json` — `rynow_compare_a2` added immediately after `main` in the order list. NOTHING else changed. NOTE: this product.json was edited in the A2-hero draft only — do NOT push it to the repo (`product-page/templates/product.json` already holds the two-column version from the product-page draft; overwriting it would lose that work).
- MAIN theme 189966123075 NOT touched. Product-page draft 190044602435 NOT touched. Lenis / scroll-reveal files NOT touched.
- Verification: both files upserted + re-read from the draft, exact-match / JSON-equality PASS (2026-11-14). Slider look/feel NOT yet verified in a browser — parent to check on the preview link; mobile check by owner.

## A2 hero removed from homepage (2026-11-14, draft only)
- Owner asked to remove the A2 hero from the homepage but keep the comparison slider. `templates/index.json` in draft 190045716547: `rynow_hero_a2` removed from the `order` array AND its whole settings block removed from `sections`. New homepage order: AD600Pro II spotlight (`rynow_ad600pro`) → categories → deals blocks → New In → A2 video banner (`hero_ftrfUy`) → Lux → trust → guides → brands. The expired 11.11 hero was already gone (the A2 hero had replaced it), so nothing else was added or moved.
- `sections/rynow-hero-a2.liquid` is RETAINED in the theme, untouched (orphaned/unused — restorable later, not deleted).
- 11.11 teardown settings untouched (Creator Deals heading, "Storewide 20% off" eyebrow, "STOREWIDE 20% OFF" banner all verified unchanged after the edit).
- Comparison slider KEPT: `sections/rynow-compare-a2.liquid` and `templates/product.json` NOT touched. (Note: the slider's browser verification has since PASSED — parent verified 2026-11-14 18:50: renders, drag works both ways, labels visible, images align across the divider, no distortion.)
- Verification: index.json upserted + re-read from the draft, JSON-equality PASS (2026-11-14). Homepage look after removal NOT yet verified in a browser — parent to check on the preview link; mobile check by owner.

## 11.11 teardown reverted (2026-11-14, draft + live nav)
- Owner corrected us: "我的双11 还没完啊" — Godox 11.11 runs to 1 Dec 11:59 (Shopee promotion ID 524163660202368 + Lazada Godox Flash Sale slots). The teardown was premature; the post-11.11 admin flips (tier-discount stacking off, membership email templates, 11.11 collection takedown) are ON HOLD until after 1 Dec.
- LIVE: "11.11" nav item restored to the Main menu (position 2, after "What's New"), linking to /collections/11-11-creator-deals-in-stock (new MenuItem gid ...664356257859). All other menu items unchanged, original IDs kept.
- Draft 190045716547 `templates/index.json` restored to MAIN theme 189966123075's values (exactly 3 strings changed): grid heading "11.11 Creator Deals — In Stock", grid eyebrow "11.11 · 1–13 NOV", deals-block `date_text` "01–13 NOV 2026".
- A2 hero STAYS removed (homepage order still starts with `rynow_ad600pro`; section file still orphaned in the theme). Comparison slider, Lenis, scroll-reveal, `templates/product.json` NOT touched.
- NOTE: the restored banner date "01–13 NOV 2026" is MAIN's value and already past — the owner needs to decide what it should say (or whether to change it). Do NOT invent a new date.
- Verification: index.json upserted + re-read from the draft, JSON-equality PASS (2026-11-14); remote == local file; diff vs pre-revert file is exactly the 3 restored strings. Live nav verified by independent menu re-read.

## 11.11 dates extended to 17 Nov (2026-11-14, draft only)
- Owner: change the 11.11 end date to 17 Nov, all products. `templates/index.json` in draft 190045716547: exactly 2 strings changed — grid eyebrow "11.11 · 1–13 NOV" → "11.11 · 1–17 NOV" and deals-block `date_text` "01–13 NOV 2026" → "01–17 NOV 2026". Nothing else changed.
- A2 hero stays removed; comparison slider, Lenis, scroll-reveal, `templates/product.json` NOT touched. MAIN theme 189966123075 NOT touched. Draft only — ships when the owner publishes the draft.
- Verification: index.json upserted + re-read from the draft, JSON-equality PASS (2026-11-14); remote == local file (14,612 bytes); both new strings present, both old "13 NOV" strings absent, `rynow_hero_a2` still absent, order unchanged.

## 11.11 poster hero restored to homepage top (2026-11-14, draft only)
- Owner asked where the 11.11 poster went: it is still on the LIVE site (MAIN theme) but missing from the draft — the A2 hero had replaced it, and then the A2 hero was removed without putting it back.
- `templates/index.json` in draft 190045716547: MAIN theme 189966123075's `hero_fTpYRU` section (type "hero", image `shopify://shop_images/rynow-1111-hero-final-2026.png`) copied verbatim into `sections` and inserted as the FIRST item in `order`. New homepage top: 11.11 poster hero → AD600Pro II spotlight → categories → deals blocks → New In → A2 video banner → Lux → trust → guides → brands.
- NOTE: the poster image has "1–11 Nov" baked into the artwork and cannot be text-edited — the sale now runs to 17 Nov, so the baked dates on the poster are stale. (The grid eyebrow and banner date_text in the same file say 1–17 NOV / 01–17 NOV 2026.)
- A2 hero STAYS removed (`rynow_hero_a2` absent); 17 Nov strings intact ("11.11 · 1–17 NOV", "01–17 NOV 2026"); comparison slider, Lenis, scroll-reveal, `templates/product.json` NOT touched. MAIN theme NOT touched. Draft only — ships when the owner publishes the draft.
- Verification: index.json upserted + re-read from the draft, JSON-equality PASS (2026-11-14); remote == local file; hero settings identical to MAIN's; diff vs pre-edit file is exactly the hero_fTpYRU addition. Homepage look after the restore NOT yet verified in a browser — parent to check on the preview link; mobile check by owner.
