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

## Verification
- (filled in after the browser check — desktop 1920px + mobile)

## Known gaps
- The A2 video banner (`hero_ftrfUy`, the A2 ad film) is KEPT further down the homepage — the new hero uses a photo, so the two A2 sections differ.
- The hero photo shows the White colourway only; the 4 colours are shown as dots.
- `sticky_details` on product pages is a separate open item (draft 190044602435).
