#!/usr/bin/env python3
"""v3: Amaran blue theme + images in quizzes, entry banners, homepage block."""
import json, re

P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

AMARAN_RAY360 = "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/amaran-ray-360c-rgb-led-monolight.jpg?v=1793890302"
GODOX_AD600_DARK = "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/ad600pro-ii-dark.jpg?v=1794415218"
AMARAN_HALO600 = "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/1b8640dc-bf5e-4d77-9a99-0f327d50585a.png?v=1785945566"
GODOX_AD200_POSTER = "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/ad200pro-ii-poster.png?v=1794457653"

# ---- 1. Amaran theme: amber -> blue ----
old_theme = '''AMARAN_THEME = {
    "BG": "#171310", "BG2": "#241d17", "BORDER": "#3d342a",
    "TEXT": "#f5f1ea", "MUTED": "#a89e92", "SOFT": "#d8d0c4",
    "ACCENT": "#e8a04c", "ACCENT_TEXT": "#1a1714",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(232,160,76,0.25), rgba(232,160,76,0) 70%)",
    "FILL": "linear-gradient(90deg, #ff9a3c, #ffd9a0, #fff6e8)",
}'''
new_theme = '''AMARAN_THEME = {
    "BG": "#0f141b", "BG2": "#18202b", "BORDER": "#2a3547",
    "TEXT": "#f2f6fb", "MUTED": "#9aa8ba", "SOFT": "#d3dce8",
    "ACCENT": "#4a9be0", "ACCENT_TEXT": "#0b1220",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(74,155,224,0.25), rgba(74,155,224,0) 70%)",
    "FILL": "linear-gradient(90deg, #2478d4, #6db3f2, #eaf4ff)",
}'''
assert old_theme in s
s = s.replace(old_theme, new_theme)

# ---- 2. Intro hero image in the quiz template ----
old_intro = '''  <div class="quiz__intro" data-quiz-intro>
    <p class="quiz__eyebrow">{{ section.settings.eyebrow }}</p>'''
assert old_intro in s
s = s.replace(old_intro, '''  <div class="quiz__intro" data-quiz-intro>
    <div class="quiz__hero"><img src="__INTRO_IMG__" alt="" loading="lazy"></div>
    <p class="quiz__eyebrow">{{ section.settings.eyebrow }}</p>''')

old_css_anchor = "  .quiz__step, .quiz__result { scroll-margin-top: 96px; }"
assert old_css_anchor in s
s = s.replace(old_css_anchor, old_css_anchor + """
  .quiz__hero { max-width: 640px; margin: 0 auto 28px; }
  .quiz__hero img { width: 100%; height: 260px; object-fit: cover; border-radius: 20px; display: block; }""")

old_media = "    .quiz__title { font-size: 27px; }"
assert old_media in s
s = s.replace(old_media, old_media + "\n    .quiz__hero img { height: 180px; }")

# ---- 3. build_section gains intro_img ----
old_sig = "def build_section(section_name, eyebrow, heading, sub, products, questions, weights, theme, bar_labels):"
assert old_sig in s
s = s.replace(old_sig, "def build_section(section_name, eyebrow, heading, sub, products, questions, weights, theme, bar_labels, intro_img):")
old_rep = '    out = out.replace("__BAR_LABELS__", bar_labels)'
assert old_rep in s
s = s.replace(old_rep, old_rep + '\n    out = out.replace("__INTRO_IMG__", intro_img)')

old_call_a = "'<div class=\"quiz__bar-labels\"><span>2800K</span><span>6500K</span></div>'"
assert old_call_a in s
s = s.replace(old_call_a, old_call_a + f",\n    \"{AMARAN_RAY360}\")")
old_call_g = "GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS, GODOX_THEME, \"\")"
assert old_call_g in s
s = s.replace(old_call_g, f"GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS, GODOX_THEME, \"\", \"{GODOX_AD600_DARK}\")")

# ---- 4. Entry banner: blue Amaran + image panels ----
new_entry = "ENTRY_SECTION = r'''" + """{% if collection.handle == 'amaran' %}
<div class="quiz-entry quiz-entry--amaran">
  <div class="quiz-entry__inner">
    <div class="quiz-entry__text">
      <p class="quiz-entry__eyebrow">AMARAN</p>
      <h3 class="quiz-entry__title">Not sure which light is right for you?</h3>
      <p class="quiz-entry__sub">Answer 3 quick questions &mdash; 30 seconds &mdash; and we will match you with the right Amaran light.</p>
      <a class="quiz-entry__btn" href="/pages/find-your-amaran-light">Find your light</a>
    </div>
    <div class="quiz-entry__media"><img src="__AMARAN_ENTRY_IMG__" alt="Amaran Halo 600x" loading="lazy"></div>
  </div>
</div>
{% elsif collection.handle == 'godox' %}
<div class="quiz-entry quiz-entry--godox">
  <div class="quiz-entry__inner">
    <div class="quiz-entry__text">
      <p class="quiz-entry__eyebrow">GODOX</p>
      <h3 class="quiz-entry__title">Which Godox gear do you actually need?</h3>
      <p class="quiz-entry__sub">Flash, video light, phone flash or trigger &mdash; answer 3 quick questions and we will point you to the right one.</p>
      <a class="quiz-entry__btn" href="/pages/find-your-godox-gear">Find your gear</a>
    </div>
    <div class="quiz-entry__media"><img src="__GODOX_ENTRY_IMG__" alt="Godox AD200Pro II" loading="lazy"></div>
  </div>
</div>
{% endif %}

{% stylesheet %}
  .quiz-entry { padding: 8px 20px 40px; }
  .quiz-entry__inner { max-width: 1200px; margin: 0 auto; border-radius: 20px; display: flex; align-items: stretch; overflow: hidden; }
  .quiz-entry--amaran .quiz-entry__inner { background: radial-gradient(560px 260px at 85% 0%, rgba(74,155,224,0.28), rgba(74,155,224,0) 70%), #0f141b; }
  .quiz-entry--godox .quiz-entry__inner { background: radial-gradient(560px 260px at 85% 0%, rgba(255,107,44,0.26), rgba(255,107,44,0) 70%), #0b0b0d; }
  .quiz-entry__text { flex: 1; padding: 36px 40px; }
  .quiz-entry__eyebrow { font-size: 12px; letter-spacing: 0.22em; font-weight: 600; margin: 0 0 10px; }
  .quiz-entry--amaran .quiz-entry__eyebrow { color: #4a9be0; }
  .quiz-entry--godox .quiz-entry__eyebrow { color: #ff6b2c; }
  .quiz-entry__title { font-size: 26px; line-height: 1.25; margin: 0 0 8px; color: #f5f5f7; letter-spacing: -0.01em; }
  .quiz-entry__sub { font-size: 15px; line-height: 1.55; color: #a8a8ad; margin: 0 0 20px; max-width: 560px; }
  .quiz-entry__btn { display: inline-block; border-radius: 999px; padding: 13px 28px; font-size: 15px; font-weight: 600; text-decoration: none; line-height: 1.2; white-space: nowrap; }
  .quiz-entry--amaran .quiz-entry__btn { background: #4a9be0; color: #0b1220; }
  .quiz-entry--godox .quiz-entry__btn { background: #ff6b2c; color: #ffffff; }
  .quiz-entry__btn:hover { opacity: 0.92; }
  .quiz-entry__media { width: 260px; flex-shrink: 0; }
  .quiz-entry__media img { width: 100%; height: 100%; object-fit: cover; display: block; }
  @media (max-width: 640px) {
    .quiz-entry__inner { flex-direction: column-reverse; }
    .quiz-entry__text { padding: 28px 24px; }
    .quiz-entry__title { font-size: 22px; }
    .quiz-entry__media { width: 100%; height: 160px; }
  }
{% endstylesheet %}

{% schema %}
{
  "name": "Quiz entry banner",
  "presets": [{ "name": "Quiz entry banner" }]
}
{% endschema %}
'''"""
s2, n = re.subn(r"ENTRY_SECTION = r'''.*?'''\n", new_entry + "\n", s, count=1, flags=re.S)
assert n == 1, "ENTRY_SECTION not found"
s = s2
s = s.replace("__AMARAN_ENTRY_IMG__", AMARAN_HALO600).replace("__GODOX_ENTRY_IMG__", GODOX_AD200_POSTER)

open(P, "w").write(s)
print("v3 edits applied to build_quiz.py")
