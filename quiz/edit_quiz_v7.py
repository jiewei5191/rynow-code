#!/usr/bin/env python3
"""v7: make it cooler — drifting blurred background, floating sparks, answer
flash/glow pulse, step entrance, progress shimmer, option lift."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- 1. FX gradient token per theme ----
rep(
  '    "FILL": "linear-gradient(90deg, #2478d4, #6db3f2, #eaf4ff)",\n    "BGOP": "0.18",',
  '    "FILL": "linear-gradient(90deg, #2478d4, #6db3f2, #eaf4ff)",\n    "BGOP": "0.18",\n    "FX": "radial-gradient(circle at 50% 42%, rgba(255,214,160,0.9), rgba(232,160,76,0.32) 42%, transparent 68%)",')
rep(
  '    "FILL": "#ff6b2c",\n    "BGOP": "0.26",',
  '    "FILL": "#ff6b2c",\n    "BGOP": "0.26",\n    "FX": "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(255,107,44,0.38) 42%, transparent 68%)",')

# ---- 2. Sparks + FX overlay markup ----
rep(
  '<div class="quiz" id="quiz-{{ section.id }}">\n',
  '<div class="quiz" id="quiz-{{ section.id }}">\n'
  '  <div class="quiz__sparks" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span></div>\n'
  '  <div class="quiz__fx" aria-hidden="true"></div>\n')

# ---- 3. Drift on the blurred background ----
rep(
  "filter: blur(28px); opacity: __BGOP__; pointer-events: none; }",
  "filter: blur(28px); opacity: __BGOP__; pointer-events: none; animation: quizDrift 36s ease-in-out infinite alternate; }")

# ---- 4. Motion CSS block (after the z-index rule) ----
rep(
  "  .quiz__intro, .quiz__step, .quiz__result { position: relative; z-index: 1; }",
  "  .quiz__intro, .quiz__step, .quiz__result { position: relative; z-index: 1; }\n"
  "  .quiz__sparks { position: absolute; inset: 0; pointer-events: none; z-index: 0; }\n"
  "  .quiz__sparks span { position: absolute; width: 5px; height: 5px; border-radius: 50%; background: __ACCENT__; box-shadow: 0 0 14px 2px __ACCENT__; opacity: .5; animation: quizFloat 7s ease-in-out infinite alternate; }\n"
  "  .quiz__sparks span:nth-child(1) { left: 8%; top: 68%; }\n"
  "  .quiz__sparks span:nth-child(2) { left: 16%; top: 24%; animation-duration: 9s; animation-delay: -2s; }\n"
  "  .quiz__sparks span:nth-child(3) { left: 86%; top: 30%; animation-duration: 8s; animation-delay: -4s; }\n"
  "  .quiz__sparks span:nth-child(4) { left: 92%; top: 72%; animation-duration: 10s; animation-delay: -1s; }\n"
  "  .quiz__sparks span:nth-child(5) { left: 48%; top: 12%; width: 4px; height: 4px; animation-duration: 6s; animation-delay: -3s; }\n"
  "  .quiz__sparks span:nth-child(6) { left: 68%; top: 84%; width: 4px; height: 4px; animation-duration: 11s; animation-delay: -5s; }\n"
  "  .quiz__fx { position: absolute; inset: 0; background: __FX__; opacity: 0; pointer-events: none; z-index: 2; }\n"
  "  .quiz--fire .quiz__fx { animation: quizFx .55s ease-out; }\n"
  "  .quiz__step--in { animation: quizIn .45s ease both; }\n"
  "  .quiz__result:not([hidden]) { animation: quizIn .5s ease both; }\n"
  "  .quiz__bar-fill { position: relative; }\n"
  "  .quiz__bar-fill::after { content: \"\"; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent); transform: translateX(-100%); animation: quizShimmer 2.2s ease-in-out infinite; }\n"
  "  @keyframes quizDrift { from { transform: translate3d(-2%, -1%, 0) scale(1); } to { transform: translate3d(2%, 1.5%, 0) scale(1.08); } }\n"
  "  @keyframes quizFloat { from { transform: translateY(0); opacity: .3; } to { transform: translateY(-26px); opacity: .7; } }\n"
  "  @keyframes quizFx { 0% { opacity: 0; } 18% { opacity: .55; } 100% { opacity: 0; } }\n"
  "  @keyframes quizIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }\n"
  "  @keyframes quizShimmer { 0% { transform: translateX(-100%); } 60%, 100% { transform: translateX(100%); } }\n"
  "  @media (prefers-reduced-motion: reduce) { .quiz::before, .quiz__sparks span, .quiz__bar-fill::after { animation: none; } }")

# ---- 5. Option hover lift ----
rep(
  "  .quiz__option { width: 100%; padding: 17px 20px; border: 1px solid __BORDER__; border-radius: 14px; background: __BG2__; font-size: 16px; line-height: 1.4; cursor: pointer; text-align: left; color: __TEXT__; transition: border-color 0.2s ease, box-shadow 0.2s ease; }",
  "  .quiz__option { width: 100%; padding: 17px 20px; border: 1px solid __BORDER__; border-radius: 14px; background: __BG2__; font-size: 16px; line-height: 1.4; cursor: pointer; text-align: left; color: __TEXT__; transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease; }")
rep(
  "  .quiz__option:hover { border-color: __ACCENT__; box-shadow: 0 0 0 1px __ACCENT__, 0 8px 30px rgba(0,0,0,0.35); }",
  "  .quiz__option:hover { border-color: __ACCENT__; box-shadow: 0 0 0 1px __ACCENT__, 0 8px 30px rgba(0,0,0,0.35); transform: translateY(-2px); }")

# ---- 6. Fire the pulse + replay step entrance on every answer ----
rep(
  "        answers[step] = opt[0];\n        step++;",
  "        answers[step] = opt[0];\n"
  "        root.classList.add('quiz--fire');\n"
  "        setTimeout(function () { root.classList.remove('quiz--fire'); }, 600);\n"
  "        step++;")
rep(
  "    intro.hidden = true;\n    resultEl.hidden = true;\n    stepEl.hidden = false;\n  }",
  "    intro.hidden = true;\n    resultEl.hidden = true;\n    stepEl.hidden = false;\n"
  "    stepEl.classList.remove('quiz__step--in');\n"
  "    void stepEl.offsetWidth;\n"
  "    stepEl.classList.add('quiz__step--in');\n  }")

open(P, "w").write(s)
print("v7 edits applied to build_quiz.py")
