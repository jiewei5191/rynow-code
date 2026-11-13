#!/usr/bin/env python3
"""v6: whole quiz background = blurred faint brand mark; hero panel removed."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- 1. Remove the hero panel div from the intro ----
rep(
  '    <div class="quiz__hero"><img src="__INTRO_IMG__" alt="" loading="lazy"></div>\n',
  '')

# ---- 2. Remove hero CSS ----
rep(
  "  .quiz__hero { max-width: 640px; height: 180px; margin: 0 auto 28px; background: __GLOW__, __BG2__; border-radius: 20px; overflow: hidden; position: relative; }\n"
  "  .quiz__hero img { position: absolute; width: 130%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }",
  "")
rep(
  "    .quiz__hero { height: 150px; }",
  "    .quiz::before { background-size: 240% auto; background-position: center 12%; }")

# ---- 3. .quiz becomes the blurred-brand canvas ----
rep(
  "  .quiz { background: __BG__; background-image: __GLOW__; background-repeat: no-repeat; background-position: center top; color: __TEXT__; padding: 64px 20px 72px; text-align: center; }",
  "  .quiz { background: __BG__; background-image: __GLOW__; background-repeat: no-repeat; background-position: center top; color: __TEXT__; padding: 64px 20px 72px; text-align: center; position: relative; overflow: hidden; }\n"
  "  .quiz::before { content: \"\"; position: absolute; inset: 0; background-image: url(\"__INTRO_IMG__\"); background-size: 150% auto; background-position: center 22%; background-repeat: no-repeat; filter: blur(28px); opacity: 0.18; pointer-events: none; }\n"
  "  .quiz__intro, .quiz__step, .quiz__result { position: relative; z-index: 1; }")

open(P, "w").write(s)
print("v6 edits applied to build_quiz.py")
