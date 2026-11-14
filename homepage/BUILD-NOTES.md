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
