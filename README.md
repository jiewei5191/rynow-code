# rynow-code

Private backup of RYNOW store code. Live store: https://rynow.co (Shopify).

## What's here

### `quiz/` — product finder quizzes

Two 3-question product finder quizzes for the RYNOW Shopify store:

- **Amaran** — `/pages/find-your-amaran-light` (9 lights: Halo 60x–600x, RAY 60c–660c)
- **Godox** — `/pages/find-your-godox-gear` (27 products: flashes, video lights, A2, triggers)

Each quiz scores answers against weighted product data and shows a result card
with the real product image, live 20%-off price, was-price, Save 20%, View
product and Add to cart. Entry points: a homepage block (`quiz-home`) and
collection-page banners (`quiz-entry`, Amaran + Godox collections only).

**Current state (2026-11-14, v9.1):** lives in the UNPUBLISHED draft theme
`190037622851` ("RYNOW - Product finder quizzes"). Pages are published but
show only title + intro on the live theme until the draft is published.

Design: Amaran blue / Godox flash-orange, whole-section background is a giant
blurred faint brand wordmark, GSAP 3.12.5 motion (staggered option cascade,
answer glow/flash pulse, result scale-in). The Shopify Forms welcome popup is
gated by quiz JS (`quiz-forms-gate`) so it only appears after the result.

### Files

| File | What it is |
|---|---|
| `quiz/build_quiz.py` | Single source of truth: product data + templates, builds all section/template files |
| `quiz/quiz_products.txt`, `quiz/quiz_variants.json` | Product data (36 products, prices/variants from Shopify) |
| `quiz/edit_quiz_v*.py` | Versioned edit scripts (v3–v9.1 design/motion iterations) |
| `quiz/quiz-amaran.liquid`, `quiz-godox.liquid` | Built quiz sections (generated) |
| `quiz/quiz-entry.liquid`, `quiz-home.liquid` | Built entry banner + homepage block (generated) |
| `quiz/*.json` | Built page/collection/home templates (generated) |
| `quiz/upsert_quiz*.py`, `quiz/redesign.py` | Older upsert/design helper scripts |

## Deploy (quiz)

```bash
cd quiz
python3 build_quiz.py        # rebuilds the .liquid/.json files
# then upsert sections/quiz-amaran.liquid + sections/quiz-godox.liquid
# into draft theme 190037622851 via the Shopify CLI themeFilesUpsert
# mutation (variables, one file per call, verify by byte length).
```

Live-theme writes are blocked on the assistant's Shopify connection, so
changes go into an unpublished draft and Ray publishes it in the Shopify
admin. Batch changes into one draft per round.

## Notes

- Prices in the quiz data are the permanent storewide 20%-off prices
  (e.g. A2 RM271 vs RM339, SR20R RM295 vs RM369, AD200Pro II RM1,119).
- Brand logos: Amaran `logo-amaran-clean-v2.png`, Godox `logo-godox.png`
  (Shopify CDN, see `build_quiz.py`).
