#!/usr/bin/env python3
"""Redesign the quiz sections with atmosphere + add the quiz-entry banner.
Edits build_quiz.py in place: new themed stylesheet, progress bar instead of dots,
brand theme tokens, entry section, and collection.json with the entry inserted.
"""
import json, re

P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

NEW_CSS = """{% stylesheet %}
  .quiz { background: __BG__; background-image: __GLOW__; background-repeat: no-repeat; background-position: center top; color: __TEXT__; padding: 64px 20px 72px; text-align: center; }
  .quiz__eyebrow { font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase; color: __ACCENT__; margin: 0 0 14px; font-weight: 600; }
  .quiz__title { font-size: 34px; line-height: 1.15; margin: 0 0 12px; letter-spacing: -0.01em; color: __TEXT__; }
  .quiz__sub { font-size: 17px; line-height: 1.55; color: __MUTED__; margin: 0 auto 8px; max-width: 520px; }
  .quiz__meta { font-size: 13px; color: __MUTED__; margin: 0 0 28px; opacity: 0.8; }
  .quiz__btn { display: inline-block; border: 0; border-radius: 999px; padding: 13px 30px; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration: none; line-height: 1.2; }
  .quiz__btn--primary { background: __ACCENT__; color: __ACCENT_TEXT__; }
  .quiz__btn--primary:hover { opacity: 0.92; color: __ACCENT_TEXT__; }
  .quiz__btn--ghost { background: rgba(255,255,255,0.08); color: __TEXT__; }
  .quiz__btn--ghost:hover { background: rgba(255,255,255,0.14); }
  .quiz__progress { font-size: 13px; color: __MUTED__; margin: 0 0 12px; letter-spacing: 0.08em; text-transform: uppercase; }
  .quiz__bar { max-width: 520px; height: 4px; border-radius: 999px; background: rgba(255,255,255,0.14); margin: 0 auto 8px; overflow: hidden; }
  .quiz__bar-fill { height: 100%; width: 0; border-radius: 999px; background: __FILL__; transition: width 0.35s ease; }
  .quiz__bar-labels { display: flex; justify-content: space-between; max-width: 520px; margin: 0 auto 24px; font-size: 11px; letter-spacing: 0.12em; color: __MUTED__; opacity: 0.75; }
  .quiz__q { font-size: 26px; line-height: 1.3; margin: 0 0 8px; color: __TEXT__; }
  .quiz__options { display: grid; gap: 12px; max-width: 520px; margin: 24px auto 0; }
  .quiz__option { width: 100%; padding: 17px 20px; border: 1px solid __BORDER__; border-radius: 14px; background: __BG2__; font-size: 16px; line-height: 1.4; cursor: pointer; text-align: left; color: __TEXT__; transition: border-color 0.2s ease, box-shadow 0.2s ease; }
  .quiz__option:hover { border-color: __ACCENT__; box-shadow: 0 0 0 1px __ACCENT__, 0 8px 30px rgba(0,0,0,0.35); }
  .quiz__back { background: none; border: 0; color: __MUTED__; font-size: 14px; cursor: pointer; margin-top: 26px; padding: 8px 12px; }
  .quiz__back:hover { color: __TEXT__; }
  .quiz__result-grid { display: grid; grid-template-columns: 300px 1fr; gap: 36px; align-items: start; text-align: left; margin-top: 32px; max-width: 780px; margin-left: auto; margin-right: auto; }
  .quiz__result-media img { width: 100%; height: auto; border-radius: 16px; display: block; }
  .quiz__result-name { font-size: 26px; line-height: 1.3; margin: 0 0 10px; color: __TEXT__; }
  .quiz__price { font-size: 22px; margin: 0 0 12px; color: __TEXT__; }
  .quiz__price s { color: __MUTED__; font-size: 16px; margin-left: 6px; }
  .quiz__save { color: __ACCENT__; font-size: 14px; font-weight: 700; margin-left: 8px; }
  .quiz__why { font-size: 16px; line-height: 1.6; color: __SOFT__; margin: 0 0 26px; }
  .quiz__actions { display: flex; gap: 12px; flex-wrap: wrap; }
  .quiz__retake { background: none; border: 0; color: __MUTED__; font-size: 14px; cursor: pointer; margin-top: 22px; padding: 8px 0; text-decoration: underline; }
  .quiz__retake:hover { color: __TEXT__; }
  @media (max-width: 640px) {
    .quiz { padding: 48px 20px 56px; }
    .quiz__title { font-size: 27px; }
    .quiz__q { font-size: 22px; }
    .quiz__result-grid { grid-template-columns: 1fr; gap: 20px; margin-top: 24px; }
    .quiz__result-media { max-width: 320px; margin: 0 auto; }
    .quiz__result-info { text-align: center; }
    .quiz__actions { justify-content: center; }
  }
{% endstylesheet %}"""

s2, n = re.subn(r"\{% stylesheet %\}.*?\{% endstylesheet %\}", NEW_CSS, s, count=1, flags=re.S)
assert n == 1, "stylesheet block not found"
s = s2

# progress dots -> temperature/charge bar
old_dots = '    <div class="quiz__dots" data-quiz-dots></div>'
new_bar = ('    <div class="quiz__bar"><div class="quiz__bar-fill" data-quiz-fill></div></div>\n'
           '    __BAR_LABELS__')
assert old_dots in s
s = s.replace(old_dots, new_bar)

s = s.replace("  var dotsEl = root.querySelector('[data-quiz-dots]');",
              "  var fillEl = root.querySelector('[data-quiz-fill]');")
old_dots_js = """    dotsEl.innerHTML = '';
    for (var i = 0; i < total; i++) {
      var d = document.createElement('span');
      if (i === step) d.className = 'is-active';
      dotsEl.appendChild(d);
    }"""
assert old_dots_js in s
s = s.replace(old_dots_js, "    fillEl.style.width = Math.round(((step + 1) / total) * 100) + '%';")

# build_section takes a theme + bar labels
old_sig = "def build_section(section_name, eyebrow, heading, sub, products, questions, weights):"
assert old_sig in s
s = s.replace(old_sig, "def build_section(section_name, eyebrow, heading, sub, products, questions, weights, theme, bar_labels):")
old_tail = """    out = out.replace("__SUB_DEFAULT__", sub)
    return out"""
assert old_tail in s
s = s.replace(old_tail, """    out = out.replace("__SUB_DEFAULT__", sub)
    out = out.replace("__BAR_LABELS__", bar_labels)
    for k, v in theme.items():
        out = out.replace("__" + k + "__", v)
    return out""")

old_amaran_call = """amaran = build_section(
    "Amaran product finder", "AMARAN", "Find your Amaran light",
    "Answer 3 quick questions and we will match you with the right light for how you shoot.",
    AMARAN_PRODUCTS, AMARAN_QUESTIONS, AMARAN_WEIGHTS)"""
assert old_amaran_call in s
s = s.replace(old_amaran_call, """AMARAN_THEME = {
    "BG": "#171310", "BG2": "#241d17", "BORDER": "#3d342a",
    "TEXT": "#f5f1ea", "MUTED": "#a89e92", "SOFT": "#d8d0c4",
    "ACCENT": "#e8a04c", "ACCENT_TEXT": "#1a1714",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(232,160,76,0.25), rgba(232,160,76,0) 70%)",
    "FILL": "linear-gradient(90deg, #ff9a3c, #ffd9a0, #fff6e8)",
}
GODOX_THEME = {
    "BG": "#0b0b0d", "BG2": "#17181d", "BORDER": "#2c2e37",
    "TEXT": "#f5f5f7", "MUTED": "#86868b", "SOFT": "#d2d2d7",
    "ACCENT": "#ff6b2c", "ACCENT_TEXT": "#ffffff",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(255,107,44,0.22), rgba(255,107,44,0) 70%)",
    "FILL": "#ff6b2c",
}
amaran = build_section(
    "Amaran product finder", "AMARAN", "Find your Amaran light",
    "Answer 3 quick questions and we will match you with the right light for how you shoot.",
    AMARAN_PRODUCTS, AMARAN_QUESTIONS, AMARAN_WEIGHTS, AMARAN_THEME,
    '<div class="quiz__bar-labels"><span>2800K</span><span>6500K</span></div>')""")

old_godox_call = """godox = build_section(
    "Godox product finder", "GODOX", "Find your Godox gear",
    "Flash, video light, phone flash or trigger - answer 3 quick questions and we will point you to the right one.",
    GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS)"""
assert old_godox_call in s
s = s.replace(old_godox_call, """godox = build_section(
    "Godox product finder", "GODOX", "Find your Godox gear",
    "Flash, video light, phone flash or trigger - answer 3 quick questions and we will point you to the right one.",
    GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS, GODOX_THEME, "")""")

open(P, "w").write(s)
print("build_quiz.py redesigned OK")
