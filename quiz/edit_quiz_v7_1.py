#!/usr/bin/env python3
"""v7.1 + v8: strengthen the motion (longer, bolder, actually visible) and add the
Forms popup gate (hide popup while the quiz is active, reveal it at the result)."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- v7.1: per-theme flash duration + stronger Amaran bloom ----
rep(
  '    "FX": "radial-gradient(circle at 50% 42%, rgba(255,214,160,0.9), rgba(232,160,76,0.32) 42%, transparent 68%)",',
  '    "FX": "radial-gradient(circle at 50% 42%, rgba(255,205,130,0.95), rgba(255,170,60,0.5) 50%, transparent 78%)",\n    "FXDUR": "0.9s",')
rep(
  '    "FX": "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(255,107,44,0.38) 42%, transparent 68%)",',
  '    "FX": "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(255,107,44,0.38) 42%, transparent 68%)",\n    "FXDUR": "0.6s",')
rep(
  "  .quiz--fire .quiz__fx { animation: quizFx .55s ease-out; }",
  "  .quiz--fire .quiz__fx { animation: quizFx __FXDUR__ ease-out; }")
rep(
  "  @keyframes quizFx { 0% { opacity: 0; } 18% { opacity: .55; } 100% { opacity: 0; } }",
  "  @keyframes quizFx { 0% { opacity: 0; } 18% { opacity: .7; } 100% { opacity: 0; } }")

# ---- v7.1: longer entrances, stronger shimmer ----
rep(
  "  .quiz__step--in { animation: quizIn .45s ease both; }",
  "  .quiz__step--in { animation: quizIn .65s ease both; }")
rep(
  "  .quiz__result:not([hidden]) { animation: quizIn .5s ease both; }",
  "  .quiz__result:not([hidden]) { animation: quizIn .7s ease both; }")
rep(
  '  .quiz__bar-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent); transform: translateX(-100%); animation: quizShimmer 2.2s ease-in-out infinite; }',
  '  .quiz__bar-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent 25%, rgba(255,255,255,0.85) 50%, transparent 75%); transform: translateX(-100%); animation: quizShimmer 2.6s ease-in-out infinite; }')

# ---- v8: Forms popup gate ----
rep(
  "  var root = document.getElementById('quiz-{{ section.id }}');",
  "  var root = document.getElementById('quiz-{{ section.id }}');\n"
  "  function syncFormsGate(show) {\n"
  "    var g = document.getElementById('quiz-forms-gate');\n"
  "    if (show) {\n"
  "      if (!g) {\n"
  "        g = document.createElement('style');\n"
  "        g.id = 'quiz-forms-gate';\n"
  "        g.textContent = 'shopify-forms-embed{display:none!important}';\n"
  "        document.head.appendChild(g);\n"
  "      }\n"
  "    } else if (g) { g.remove(); }\n"
  "  }\n"
  "  syncFormsGate(true);")
rep(
  "  function showResult() {\n    var p = pickWinner();",
  "  function showResult() {\n    var p = pickWinner();\n    syncFormsGate(false);")
rep(
  "    resultEl.hidden = true;\n    stepEl.hidden = true;\n    intro.hidden = false;\n  });",
  "    resultEl.hidden = true;\n    stepEl.hidden = true;\n    intro.hidden = false;\n    syncFormsGate(true);\n  });")

open(P, "w").write(s)
print("v7.1 + v8 edits applied to build_quiz.py")
