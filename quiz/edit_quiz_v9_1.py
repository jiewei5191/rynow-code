#!/usr/bin/env python3
"""v9.1: make the GSAP effects sustained enough for a human eye (and a camera) to
actually see them — hold the pulse at peak, slower option cascade."""
P = "/home/hatch/workspace/quiz_build/build_quiz.py"
s = open(P).read()

def rep(old, new):
    global s
    assert old in s, "MISSING: " + old[:90]
    s = s.replace(old, new)

# ---- Pulse: hold at peak before fading (was a triangle with a ~0.2s peak) ----
rep(
  "    gsap.timeline()\n"
  "      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.2, ease: 'power1.in' })\n"
  "      .to(fxEl, { opacity: 0, duration: FXDUR * 0.8, ease: 'power2.out' });",
  "    gsap.timeline()\n"
  "      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.2, ease: 'power1.in' })\n"
  "      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.45, ease: 'none' })\n"
  "      .to(fxEl, { opacity: 0, duration: FXDUR * 0.8, ease: 'power2.out' });")

# ---- Result glow: same hold ----
rep(
  "      gsap.timeline({ delay: 0.15 })\n"
  "        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.25, ease: 'power1.in' })\n"
  "        .to(fxEl, { opacity: 0, duration: FXDUR * 0.75, ease: 'power2.out' });",
  "      gsap.timeline({ delay: 0.15 })\n"
  "        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.25, ease: 'power1.in' })\n"
  "        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.4, ease: 'none' })\n"
  "        .to(fxEl, { opacity: 0, duration: FXDUR * 0.75, ease: 'power2.out' });")

# ---- Cascade: slower stagger + longer duration so the one-by-one is visible ----
rep(
  "      gsap.fromTo(optsEl.querySelectorAll('.quiz__option'), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, stagger: 0.06, ease: 'power3.out', delay: 0.1 });",
  "      gsap.fromTo(optsEl.querySelectorAll('.quiz__option'), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.65, stagger: 0.09, ease: 'power3.out', delay: 0.12 });")

open(P, "w").write(s)
print("v9.1 edits applied to build_quiz.py")
