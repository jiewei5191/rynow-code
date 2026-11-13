#!/usr/bin/env python3
"""v5: brand logo as a faint background watermark, not a crisp centred logo."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- 1. Quiz intro hero: giant faint watermark ----
rep(
  "  .quiz__hero { max-width: 640px; margin: 0 auto 28px; background: __GLOW__, __BG2__; border-radius: 20px; overflow: hidden; }",
  "  .quiz__hero { max-width: 640px; height: 180px; margin: 0 auto 28px; background: __GLOW__, __BG2__; border-radius: 20px; overflow: hidden; position: relative; }")
rep(
  "  .quiz__hero img { width: 100%; max-width: 400px; margin: 0 auto; height: 180px; object-fit: contain; padding: 48px 40px; box-sizing: border-box; display: block; }",
  "  .quiz__hero img { position: absolute; width: 130%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }")
rep(
  "    .quiz__hero img { height: 160px; padding: 32px 24px; }",
  "    .quiz__hero { height: 150px; }")

# ---- 2. Homepage cards: giant faint watermark ----
rep(
  "  .quiz-home__media { height: 220px; display: flex; align-items: center; justify-content: center; }",
  "  .quiz-home__media { height: 220px; position: relative; overflow: hidden; }")
rep(
  "  .quiz-home__media img { max-width: 280px; max-height: 110px; width: auto; height: auto; object-fit: contain; display: block; }",
  "  .quiz-home__media img { position: absolute; width: 130%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }")
rep(
  "    .quiz-home__media img { max-width: 220px; max-height: 84px; }",
  "    .quiz-home__media img { width: 140%; }")

# ---- 3. Entry banners: giant faint watermark ----
rep(
  "  .quiz-entry__media { width: 260px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; padding: 24px; box-sizing: border-box; }",
  "  .quiz-entry__media { width: 260px; flex-shrink: 0; position: relative; overflow: hidden; }")
rep(
  "  .quiz-entry__media img { max-width: 200px; max-height: 110px; width: auto; height: auto; object-fit: contain; display: block; }",
  "  .quiz-entry__media img { position: absolute; width: 150%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }")

open(P, "w").write(s)
print("v5 edits applied to build_quiz.py")
