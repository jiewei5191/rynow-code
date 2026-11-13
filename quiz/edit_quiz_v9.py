#!/usr/bin/env python3
"""v9: replace CSS answer pulse + entrances with GSAP 3.12.5 animations.

- GSAP loaded from CDN (defer) before the quiz's own script.
- Answer pulse: GSAP timeline on .quiz__fx (opacity 0 -> 0.75 -> 0), per-theme
  FXDUR (Amaran 0.9s bloom, Godox 0.6s flash). No pulse on the final answer;
  showResult runs its own clean pulse instead (avoids two tweens fighting).
- Entrances: GSAP fromTo on question label + question (y 14 -> 0) and option
  buttons with 0.06s stagger; result card scale 0.96 -> 1, y 12 -> 0.
- Every gsap call guarded by motionOK() (window.gsap present + no
  prefers-reduced-motion), checked at CALL time (GSAP loads deferred, so a
  load-time check would always be false).
- REMOVED (dead code): .quiz--fire rule, quizFx keyframes, .quiz__step--in
  rule, .quiz__result:not([hidden]) rule, quizIn keyframes, and the JS
  class-toggle / setTimeout code.
- KEPT: CSS drift, sparks, shimmer, popup gate, FX/FXDUR tokens, all data.
"""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- 1. GSAP CDN tag before the quiz's own script ----
rep(
  "<script>\n(function () {",
  '<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>\n<script>\n(function () {')

# ---- 2. Remove dead CSS: .quiz--fire rule, step/result entrance rules ----
rep(
  "  .quiz--fire .quiz__fx { animation: quizFx __FXDUR__ ease-out; }\n",
  "")
rep(
  "  .quiz__step--in { animation: quizIn .65s ease both; }\n",
  "")
rep(
  "  .quiz__result:not([hidden]) { animation: quizIn .7s ease both; }\n",
  "")
rep(
  "  @keyframes quizFx { 0% { opacity: 0; } 18% { opacity: .7; } 100% { opacity: 0; } }\n",
  "")
rep(
  "  @keyframes quizIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }\n",
  "")

# ---- 3. Helpers: fx element, numeric FXDUR, motion guard, pulse ----
rep(
  "  var backBtn = root.querySelector('[data-quiz-back]');",
  "  var backBtn = root.querySelector('[data-quiz-back]');\n"
  "  var fxEl = root.querySelector('.quiz__fx');\n"
  "  var FXDUR = parseFloat('__FXDUR__') || 0.8;\n"
  "  function motionOK() {\n"
  "    return !!window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n"
  "  }\n"
  "  function firePulse() {\n"
  "    if (!motionOK() || !fxEl) return;\n"
  "    gsap.killTweensOf(fxEl);\n"
  "    gsap.timeline()\n"
  "      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.2, ease: 'power1.in' })\n"
  "      .to(fxEl, { opacity: 0, duration: FXDUR * 0.8, ease: 'power2.out' });\n"
  "  }")

# ---- 4. Option click: GSAP pulse (not on the final answer — showResult pulses) ----
rep(
  "      b.addEventListener('click', function () {\n"
  "        answers[step] = opt[0];\n"
  "        root.classList.add('quiz--fire');\n"
  "        setTimeout(function () { root.classList.remove('quiz--fire'); }, 600);\n"
  "        step++;\n"
  "        if (step < total) { renderQuestion(); } else { showResult(); }\n"
  "      });",
  "      b.addEventListener('click', function () {\n"
  "        answers[step] = opt[0];\n"
  "        step++;\n"
  "        if (step < total) { firePulse(); renderQuestion(); } else { showResult(); }\n"
  "      });")

# ---- 5. Question entrance: GSAP stagger (replaces .quiz__step--in toggle) ----
rep(
  "    stepEl.hidden = false;\n"
  "    stepEl.classList.remove('quiz__step--in');\n"
  "    void stepEl.offsetWidth;\n"
  "    stepEl.classList.add('quiz__step--in');\n"
  "  }",
  "    stepEl.hidden = false;\n"
  "    if (motionOK()) {\n"
  "      gsap.fromTo([countEl, qEl], { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' });\n"
  "      gsap.fromTo(optsEl.querySelectorAll('.quiz__option'), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, stagger: 0.06, ease: 'power3.out', delay: 0.1 });\n"
  "    }\n"
  "  }")

# ---- 6. Result entrance + glow pulse in showResult ----
rep(
  "    resultEl.scrollIntoView({ behavior: 'auto', block: 'start' });\n  }",
  "    resultEl.scrollIntoView({ behavior: 'auto', block: 'start' });\n"
  "    if (motionOK() && fxEl) {\n"
  "      gsap.fromTo(resultEl, { scale: 0.96, y: 12, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.7, ease: 'power3.out' });\n"
  "      gsap.killTweensOf(fxEl);\n"
  "      gsap.set(fxEl, { opacity: 0 });\n"
  "      gsap.timeline({ delay: 0.15 })\n"
  "        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.25, ease: 'power1.in' })\n"
  "        .to(fxEl, { opacity: 0, duration: FXDUR * 0.75, ease: 'power2.out' });\n"
  "    }\n"
  "  }")

open(P, "w").write(s)
print("v9 edits applied to build_quiz.py")
