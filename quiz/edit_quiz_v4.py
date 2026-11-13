#!/usr/bin/env python3
"""v4: replace product images with brand-logo panels (homepage cards, quiz intros, entry banners)."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

AMARAN_LOGO = "https://cdn.shopify.com/s/files/1/0693/9230/2147/collections/logo-amaran.png?v=1793897639"
GODOX_LOGO = "https://cdn.shopify.com/s/files/1/0693/9230/2147/collections/logo-godox.png?v=1793897642"

# ---- 1. Swap image URLs for logo URLs (all four spots) ----
replacements = [
    ("https://cdn.shopify.com/s/files/1/0693/9230/2147/files/amaran-ray-360c-rgb-led-monolight.jpg?v=1793890302", AMARAN_LOGO),
    ("https://cdn.shopify.com/s/files/1/0693/9230/2147/files/ad600pro-ii-dark.jpg?v=1794415218", GODOX_LOGO),
    ("https://cdn.shopify.com/s/files/1/0693/9230/2147/files/1b8640dc-bf5e-4d77-9a99-0f327d50585a.png?v=1785945566", AMARAN_LOGO),
    ("https://cdn.shopify.com/s/files/1/0693/9230/2147/files/ad200pro-ii-poster.png?v=1794457653", GODOX_LOGO),
]
for old, new in replacements:
    assert old in s, "missing URL: " + old
    s = s.replace(old, new)

# ---- 2. Alt texts ----
for old, new in [
    ('alt="Amaran RAY 360c"', 'alt="Amaran"'),
    ('alt="Godox AD600Pro II"', 'alt="Godox"'),
    ('alt="Amaran Halo 600x"', 'alt="Amaran"'),
    ('alt="Godox AD200Pro II"', 'alt="Godox"'),
]:
    assert old in s, "missing alt: " + old
    s = s.replace(old, new)

# ---- 3. Quiz intro hero: product banner -> logo panel ----
old = """  .quiz__hero { max-width: 640px; margin: 0 auto 28px; }
  .quiz__hero img { width: 100%; height: 260px; object-fit: cover; border-radius: 20px; display: block; }"""
assert old in s
s = s.replace(old, """  .quiz__hero { max-width: 640px; margin: 0 auto 28px; background: __GLOW__, __BG2__; border-radius: 20px; overflow: hidden; }
  .quiz__hero img { width: 100%; height: 200px; object-fit: contain; padding: 48px 40px; box-sizing: border-box; display: block; }""")

old = "    .quiz__hero img { height: 180px; }"
assert old in s
s = s.replace(old, "    .quiz__hero img { height: 160px; padding: 32px 24px; }")

# ---- 4. Homepage cards: product image -> logo panel ----
old = "  .quiz-home__media img { width: 100%; height: 220px; object-fit: cover; display: block; }"
assert old in s
s = s.replace(old, """  .quiz-home__media { height: 220px; display: flex; align-items: center; justify-content: center; }
  .quiz-home__card--amaran .quiz-home__media { background: radial-gradient(420px 200px at 50% 0%, rgba(74,155,224,0.30), rgba(74,155,224,0) 70%), #0f141b; }
  .quiz-home__card--godox .quiz-home__media { background: radial-gradient(420px 200px at 50% 0%, rgba(255,107,44,0.28), rgba(255,107,44,0) 70%), #0b0b0d; }
  .quiz-home__media img { max-width: 280px; max-height: 110px; width: auto; height: auto; object-fit: contain; display: block; }""")

old = "    .quiz-home__media img { height: 180px; }"
assert old in s
s = s.replace(old, "    .quiz-home__media { height: 180px; }\n    .quiz-home__media img { max-width: 220px; max-height: 84px; }")

# ---- 5. Entry banners: product image panel -> logo panel ----
old = "  .quiz-entry__media { width: 260px; flex-shrink: 0; }"
assert old in s
s = s.replace(old, "  .quiz-entry__media { width: 260px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; padding: 24px; box-sizing: border-box; }")

old = "  .quiz-entry__media img { width: 100%; height: 100%; object-fit: cover; display: block; }"
assert old in s
s = s.replace(old, "  .quiz-entry__media img { max-width: 200px; max-height: 110px; width: auto; height: auto; object-fit: contain; display: block; }")

open(P, "w").write(s)
print("v4 edits applied to build_quiz.py")
