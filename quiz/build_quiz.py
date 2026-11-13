#!/usr/bin/env python3
"""Build the Amaran + Godox product-finder quiz sections for the RYNOW draft theme.
Reads ~/workspace/quiz_products.txt (name|handle|lo|hi|img) and quiz_variants.json.
Writes sections/quiz-amaran.liquid and sections/quiz-godox.liquid + the two page templates.
Prices are the live Shopify sale prices (permanent 20% off); compare-at = round(price/0.8).
"""
import json, math, os

WS = os.path.expanduser("~/workspace")
OUT = os.path.join(WS, "quiz_build")
os.makedirs(OUT, exist_ok=True)

prod = {}
for line in open(os.path.join(WS, "quiz_products.txt")):
    name, handle, lo, hi, img = line.strip().split("|")
    prod[handle] = {"name": name, "handle": handle, "price": float(lo),
                    "from_price": float(lo) != float(hi), "img": img}
variants = json.load(open(os.path.join(WS, "quiz_variants.json")))

def P(handle, why):
    d = dict(prod[handle])
    d["variant"] = variants[handle]
    d["was"] = round(d["price"] / 0.8)
    d["why"] = why
    return d

AMARAN_PRODUCTS = [
    P("amaran-halo-60x-bi-color-led-light", "56W of Bi-Color light in a pocket-sized body. The easiest way to start lighting your videos and streams."),
    P("amaran-halo-100x-bi-color-cob-led-light", "100W Bi-Color in an ultra-compact body. Enough power for a home studio, small enough to take anywhere."),
    P("amaran-halo-200x-bi-color-cob-led-light", "200W of clean Bi-Color light for a serious home studio or small set."),
    P("amaran-halo-300x-bi-color-cob-led-light", "300W Bi-Color COB for studio work. Bright enough for key light duty with Bowens modifiers."),
    P("amaran-halo-600x-bi-color-cob-led-light", "600W of professional Bi-Color power. The studio workhorse."),
    P("amaran-ray-60c-rgb-cob-led-video-light", "65W of full RGB colour in a portable body. Creative looks, anywhere."),
    P("amaran-ray-120c-rgb-cob-led-video-light-120w-full-color-portable-photography-light-599g", "120W RGB COB, just 599g. Big colour, small bag."),
    P("amaran-ray-360c-omnicolor-cob-led-light", "360W OmniColor with IP54 weather sealing. Full-colour studio power, indoors or out."),
    P("amaran-ray-660c-omnicolor-cob-led-light", "660W of full-colour professional power. The brightest Amaran we carry."),
]
AMARAN_QUESTIONS = [
    ("What do you mainly shoot?", [("photo", "Photos & portraits"), ("video", "Video & short-form"), ("live", "Livestreaming"), ("colour", "Creative colour looks")]),
    ("Where will you use it?", [("home", "At home / small room"), ("studio", "In a studio"), ("outdoor", "Outdoors / on location")]),
    ("What is your budget?", [("under500", "Under RM500"), ("mid", "RM500 - RM900"), ("high", "RM900 - RM1,500"), ("pro", "Over RM1,500")]),
]
AMARAN_WEIGHTS = {
    "photo": {"halo60x": 2, "halo100x": 2, "halo200x": 2, "halo300x": 2, "halo600x": 2},
    "video": {"halo100x": 2, "halo200x": 2, "halo300x": 1, "ray60c": 1, "ray120c": 1},
    "live": {"halo60x": 3, "halo100x": 2, "ray60c": 2},
    "colour": {"ray60c": 3, "ray120c": 3, "ray360c": 3, "ray660c": 3},
    "home": {"halo60x": 3, "halo100x": 2, "ray60c": 2},
    "studio": {"halo200x": 2, "halo300x": 3, "halo600x": 3, "ray360c": 3, "ray660c": 3},
    "outdoor": {"halo60x": 2, "halo100x": 2, "ray60c": 3, "ray120c": 3},
    "under500": {"halo60x": 3},
    "mid": {"halo100x": 3, "halo200x": 2, "ray60c": 2, "ray120c": 2, "halo300x": 1},
    "high": {"halo300x": 3, "halo600x": 2, "ray360c": 3, "ray120c": 1},
    "pro": {"halo600x": 2, "ray660c": 3, "ray360c": 1},
}

GODOX_PRODUCTS = [
    P("godox-it30pro-ttl-mini-flash-speedlite-for-sony-canon-nikon-fujifilm-olympus-leica-hss-1-8000s-wireless-trigger", "A tiny TTL speedlite that lives on your camera. HSS, wireless, and it fits in a jacket pocket."),
    P("godox-lux-junior-ii-s-retro-flash", "Retro looks, simple manual flash. For film cameras and anyone who loves the vintage vibe."),
    P("godox-v1-mid-ttl-round-head-camera-flash", "The round-head V1 experience at a friendlier price, with 650 flashes per charge."),
    P("godox-v1-ttl-round-head-camera-flash", "The classic round-head TTL speedlite. Soft, natural light straight out of the box."),
    P("godox-ms300v-studio-strobe-flash", "A 300Ws studio strobe with a bright LED modelling lamp. The cheapest way into real studio light."),
    P("godox-sk400iii-v-studio-strobe-flash", "400Ws of studio power with Bowens mount. Built for the studio, priced for everyone."),
    P("godox-v1-pro-ttl-round-head-camera-flash", "76Ws of round-head power with a detachable sub-flash and Type-C charging. The flagship on-camera flash."),
    P("godox-v100-ttl-round-head-camera-flash", "100Ws, touchscreen, and the most powerful hot-shoe flash Godox makes."),
    P("godox-ad100pro-ii-pocket-flash", "100Ws in a pocket-sized body. The travel flash that pros actually carry."),
    P("godox-ad200pro-ii-pocket-flash", "200Ws of pocket flash power with a Bi-Color modelling light. Our best-selling flash."),
    P("godox-ad600pro-ii-outdoor-flash", "600Ws of Bowens-mount power. The location flash for serious outdoor work."),
    P("godox-ad300pro-ii-outdoor-flash", "300Ws in a compact body. The sweet spot between portable and powerful."),
    P("godox-ad400pro-ii-outdoor-flash", "400Ws with Bowens mount. Studio power that still travels."),
    P("godox-ad800pro-outdoor-flash", "800Ws. The most powerful portable flash we carry."),
    P("godox-sl100bi-100w-bi-color-led-video-light", "100W Bi-Color for home studios. Bright enough for a proper key light."),
    P("godox-sl60ii-bi-60w-bi-color-led-video-light", "60W Bi-Color with Bowens mount. Warm to cool, with all your modifiers."),
    P("godox-sl60w-60w-cob-led-video-light", "60W of clean daylight COB light. The no-fuss starter video light."),
    P("godox-ml60ii-bi-70w-bi-color-led-video-light", "70W Bi-Color in a palm-sized body. Small light, serious output."),
    P("godox-ml80bi-80w-bi-color-portable-led-video-light", "80W Bi-Color, fan-cooled and portable. A creator favourite."),
    P("godox-ml40bi-ml40r-portable-led-video-light", "A pocket LED that goes anywhere. Bi-Color or full RGB."),
    P("godox-rs100bi-rs100r-100w-portable-led-video-light", "100W of portable light with a built-in battery. No cables, no fuss."),
    P("godox-litemons-sr20r-portable-rgb-led-ring-light-for-photography-video-recording-live-streaming", "A ring light that doubles as your camera remote. Built for TikTok lives."),
    P("godox-a2-smartphone-xenon-flash-ttl-hss-1-8000s-magnetic-flash-with-bi-color-led-light", "A real xenon flash for your phone. Better light than any phone flash can give."),
    P("godox-x2t-ttl-wireless-flash-trigger", "The classic 2.4G trigger. Reliable, simple, and it just works."),
    P("godox-x3-touchscreen-ttl-wireless-flash-trigger", "A touchscreen trigger that feels like a phone. Fast to set up, easy to read."),
    P("godox-x3-pro-touchscreen-ttl-wireless-flash-trigger", "Touchscreen, Bluetooth, and full TTL control. The trigger for people who shoot a lot."),
    P("godox-xpro-ii-ttl-wireless-flash-trigger", "Five groups, a big screen, and every flash in your bag under control."),
]
GODOX_QUESTIONS = [
    ("What are you shopping for?", [("flash", "A camera flash"), ("video", "A video light"), ("phone", "A phone flash"), ("trigger", "A flash trigger")]),
    ("Where do you shoot most?", [("home", "At home / small space"), ("studio", "In a studio"), ("outdoor", "Outdoors / on location"), ("travel", "On the go / travel")]),
    ("What is your budget?", [("under300", "Under RM300"), ("mid", "RM300 - RM800"), ("high", "RM800 - RM1,500"), ("pro", "Over RM1,500")]),
]
FLASH = ["it30", "lux", "v1mid", "v1", "ms300v", "sk400", "v1pro", "v100", "ad100", "ad200", "ad600", "ad300", "ad400", "ad800"]
VIDEO = ["sl100bi", "sl60ii", "sl60w", "ml60ii", "ml80bi", "ml40", "rs100", "sr20r"]
TRIG = ["x2t", "x3", "x3pro", "xpro"]
GODOX_WEIGHTS = {
    "flash": {k: 3 for k in FLASH} | {"x2t": 1, "x3": 1, "x3pro": 1, "xpro": 1},
    "video": {k: 3 for k in VIDEO},
    "phone": {"a2": 5},
    "trigger": {k: 4 for k in TRIG} | {k: 1 for k in ["it30", "lux", "v1mid", "v1", "v1pro", "v100", "ad100", "ad200"]},
    "home": {"lux": 2, "it30": 2, "v1mid": 2, "v1": 2, "sl60w": 2, "sl60ii": 2, "ml40": 2, "sr20r": 2, "ml60ii": 1, "a2": 1},
    "studio": {"sk400": 3, "ms300v": 3, "ad600": 3, "ad400": 2, "ad800": 2, "sl100bi": 3, "sl60ii": 2, "ad300": 2, "v1pro": 1, "v100": 1},
    "outdoor": {"ad200": 3, "ad300": 3, "ad400": 2, "ad600": 3, "ad100": 2, "ml80bi": 2, "rs100": 2, "ad800": 1},
    "travel": {"ad100": 3, "ad200": 2, "lux": 2, "it30": 3, "ml40": 3, "sr20r": 3, "a2": 2, "v1mid": 1, "ml80bi": 1},
    "under300": {"lux": 3, "it30": 3, "a2": 3, "sr20r": 3, "x2t": 3, "x3": 2, "xpro": 2, "ms300v": 1, "ml40": 1},
    "mid": {"v1mid": 3, "v1": 3, "sl60w": 3, "sl60ii": 3, "ml60ii": 3, "ml40": 3, "ml80bi": 2, "sl100bi": 2, "sk400": 2, "ms300v": 3, "x3pro": 2, "x3": 1, "xpro": 1},
    "high": {"v1pro": 3, "v100": 3, "ad100": 3, "ad200": 3, "rs100": 3, "ml80bi": 2, "sl100bi": 1, "ml60ii": 1},
    "pro": {"ad300": 3, "ad400": 3, "ad600": 3, "ad800": 3},
}

# sanity: every product key used in weights must exist; every weight key must be an answer id
def check(products, questions, weights):
    keys = {p["key"] for p in products}
    answers = {a for _, opts in questions for a, _ in opts}
    assert set(weights) == answers, f"weight answers mismatch: {set(weights) ^ answers}"
    for ans, w in weights.items():
        bad = set(w) - keys
        assert not bad, f"{ans} references unknown products: {bad}"
    print("checked OK:", len(products), "products,", len(questions), "questions")

HANDLE_TO_KEY = {
    "amaran-halo-60x-bi-color-led-light": "halo60x",
    "amaran-halo-100x-bi-color-cob-led-light": "halo100x",
    "amaran-halo-200x-bi-color-cob-led-light": "halo200x",
    "amaran-halo-300x-bi-color-cob-led-light": "halo300x",
    "amaran-halo-600x-bi-color-cob-led-light": "halo600x",
    "amaran-ray-60c-rgb-cob-led-video-light": "ray60c",
    "amaran-ray-120c-rgb-cob-led-video-light-120w-full-color-portable-photography-light-599g": "ray120c",
    "amaran-ray-360c-omnicolor-cob-led-light": "ray360c",
    "amaran-ray-660c-omnicolor-cob-led-light": "ray660c",
    "godox-it30pro-ttl-mini-flash-speedlite-for-sony-canon-nikon-fujifilm-olympus-leica-hss-1-8000s-wireless-trigger": "it30",
    "godox-lux-junior-ii-s-retro-flash": "lux",
    "godox-v1-mid-ttl-round-head-camera-flash": "v1mid",
    "godox-v1-ttl-round-head-camera-flash": "v1",
    "godox-ms300v-studio-strobe-flash": "ms300v",
    "godox-sk400iii-v-studio-strobe-flash": "sk400",
    "godox-v1-pro-ttl-round-head-camera-flash": "v1pro",
    "godox-v100-ttl-round-head-camera-flash": "v100",
    "godox-ad100pro-ii-pocket-flash": "ad100",
    "godox-ad200pro-ii-pocket-flash": "ad200",
    "godox-ad600pro-ii-outdoor-flash": "ad600",
    "godox-ad300pro-ii-outdoor-flash": "ad300",
    "godox-ad400pro-ii-outdoor-flash": "ad400",
    "godox-ad800pro-outdoor-flash": "ad800",
    "godox-sl100bi-100w-bi-color-led-video-light": "sl100bi",
    "godox-sl60ii-bi-60w-bi-color-led-video-light": "sl60ii",
    "godox-sl60w-60w-cob-led-video-light": "sl60w",
    "godox-ml60ii-bi-70w-bi-color-led-video-light": "ml60ii",
    "godox-ml80bi-80w-bi-color-portable-led-video-light": "ml80bi",
    "godox-ml40bi-ml40r-portable-led-video-light": "ml40",
    "godox-rs100bi-rs100r-100w-portable-led-video-light": "rs100",
    "godox-litemons-sr20r-portable-rgb-led-ring-light-for-photography-video-recording-live-streaming": "sr20r",
    "godox-a2-smartphone-xenon-flash-ttl-hss-1-8000s-magnetic-flash-with-bi-color-led-light": "a2",
    "godox-x2t-ttl-wireless-flash-trigger": "x2t",
    "godox-x3-touchscreen-ttl-wireless-flash-trigger": "x3",
    "godox-x3-pro-touchscreen-ttl-wireless-flash-trigger": "x3pro",
    "godox-xpro-ii-ttl-wireless-flash-trigger": "xpro",
}
for p in AMARAN_PRODUCTS + GODOX_PRODUCTS:
    p["key"] = HANDLE_TO_KEY[p["handle"]]
    p["price"] = int(p["price"])
    p["was"] = int(p["was"])

check(AMARAN_PRODUCTS, AMARAN_QUESTIONS, AMARAN_WEIGHTS)
check(GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS)

SECTION_TEMPLATE = r'''
<div class="quiz" id="quiz-{{ section.id }}">
  <div class="quiz__sparks" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span></div>
  <div class="quiz__fx" aria-hidden="true"></div>
  <div class="quiz__intro" data-quiz-intro>
    <p class="quiz__eyebrow">{{ section.settings.eyebrow }}</p>
    <h2 class="quiz__title">{{ section.settings.heading }}</h2>
    <p class="quiz__sub">{{ section.settings.subheading }}</p>
    <p class="quiz__meta">3 questions &middot; 30 seconds &middot; no email needed</p>
    <button class="quiz__btn quiz__btn--primary" type="button" data-quiz-start>Start the quiz</button>
  </div>

  <div class="quiz__step" data-quiz-step hidden>
    <p class="quiz__progress"><span data-quiz-count>Question 1 of 3</span></p>
    <div class="quiz__bar"><div class="quiz__bar-fill" data-quiz-fill></div></div>
    __BAR_LABELS__
    <h3 class="quiz__q" data-quiz-question></h3>
    <div class="quiz__options" data-quiz-options></div>
    <button class="quiz__back" type="button" data-quiz-back hidden>&larr; Back</button>
  </div>

  <div class="quiz__result" data-quiz-result hidden>
    <p class="quiz__eyebrow">Your match</p>
    <div class="quiz__result-grid">
      <div class="quiz__result-media"><img data-quiz-img src="" alt="" loading="lazy"></div>
      <div class="quiz__result-info">
        <h3 class="quiz__result-name" data-quiz-name></h3>
        <p class="quiz__price"><span data-quiz-price></span> <s data-quiz-was></s> <span class="quiz__save">Save 20%</span></p>
        <p class="quiz__why" data-quiz-why></p>
        <div class="quiz__actions">
          <a class="quiz__btn quiz__btn--primary" data-quiz-view href="#">View product</a>
          <button class="quiz__btn quiz__btn--ghost" type="button" data-quiz-add>Add to cart</button>
        </div>
        <button class="quiz__retake" type="button" data-quiz-retake>Retake the quiz</button>
      </div>
    </div>
  </div>
</div>

{% stylesheet %}
  .quiz { background: __BG__; background-image: __GLOW__; background-repeat: no-repeat; background-position: center top; color: __TEXT__; padding: 64px 20px 72px; text-align: center; position: relative; overflow: hidden; }
  .quiz::before { content: ""; position: absolute; inset: 0; background-image: url("__INTRO_IMG__"); background-size: 150% auto; background-position: center; background-repeat: no-repeat; filter: blur(28px); opacity: __BGOP__; pointer-events: none; animation: quizDrift 36s ease-in-out infinite alternate; }
  .quiz__intro, .quiz__step, .quiz__result { position: relative; z-index: 1; }
  .quiz__sparks { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
  .quiz__sparks span { position: absolute; width: 5px; height: 5px; border-radius: 50%; background: __ACCENT__; box-shadow: 0 0 14px 2px __ACCENT__; opacity: .5; animation: quizFloat 7s ease-in-out infinite alternate; }
  .quiz__sparks span:nth-child(1) { left: 8%; top: 68%; }
  .quiz__sparks span:nth-child(2) { left: 16%; top: 24%; animation-duration: 9s; animation-delay: -2s; }
  .quiz__sparks span:nth-child(3) { left: 86%; top: 30%; animation-duration: 8s; animation-delay: -4s; }
  .quiz__sparks span:nth-child(4) { left: 92%; top: 72%; animation-duration: 10s; animation-delay: -1s; }
  .quiz__sparks span:nth-child(5) { left: 48%; top: 12%; width: 4px; height: 4px; animation-duration: 6s; animation-delay: -3s; }
  .quiz__sparks span:nth-child(6) { left: 68%; top: 84%; width: 4px; height: 4px; animation-duration: 11s; animation-delay: -5s; }
  .quiz__fx { position: absolute; inset: 0; background: __FX__; opacity: 0; pointer-events: none; z-index: 2; }
  .quiz__bar-fill { position: relative; }
  .quiz__bar-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent 25%, rgba(255,255,255,0.85) 50%, transparent 75%); transform: translateX(-100%); animation: quizShimmer 2.6s ease-in-out infinite; }
  @keyframes quizDrift { from { transform: translate3d(-2%, -1%, 0) scale(1); } to { transform: translate3d(2%, 1.5%, 0) scale(1.08); } }
  @keyframes quizFloat { from { transform: translateY(0); opacity: .3; } to { transform: translateY(-26px); opacity: .7; } }
  @keyframes quizShimmer { 0% { transform: translateX(-100%); } 60%, 100% { transform: translateX(100%); } }
  @media (prefers-reduced-motion: reduce) { .quiz::before, .quiz__sparks span, .quiz__bar-fill::after { animation: none; } }
  .quiz__eyebrow { font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase; color: __ACCENT__; margin: 0 0 14px; font-weight: 600; }
  .quiz__title { font-size: 34px; line-height: 1.15; margin: 0 0 12px; letter-spacing: -0.01em; color: __TEXT__; }
  .quiz__sub { font-size: 17px; line-height: 1.55; color: __MUTED__; margin: 0 auto 8px; max-width: 520px; }
  .quiz__meta { font-size: 13px; color: __MUTED__; margin: 0 0 28px; opacity: 0.8; }
  .quiz__step, .quiz__result { scroll-margin-top: 96px; }

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
  .quiz__option { width: 100%; padding: 17px 20px; border: 1px solid __BORDER__; border-radius: 14px; background: __BG2__; font-size: 16px; line-height: 1.4; cursor: pointer; text-align: left; color: __TEXT__; transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease; }
  .quiz__option:hover { border-color: __ACCENT__; box-shadow: 0 0 0 1px __ACCENT__, 0 8px 30px rgba(0,0,0,0.35); transform: translateY(-2px); }
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
    .quiz::before { background-size: 240% auto; background-position: center 12%; }
    .quiz__q { font-size: 22px; }
    .quiz__result-grid { grid-template-columns: 1fr; gap: 20px; margin-top: 24px; }
    .quiz__result-media { max-width: 320px; margin: 0 auto; }
    .quiz__result-info { text-align: center; }
    .quiz__actions { justify-content: center; }
  }
{% endstylesheet %}

<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script>
(function () {
  var root = document.getElementById('quiz-{{ section.id }}');
  function syncFormsGate(show) {
    var g = document.getElementById('quiz-forms-gate');
    if (show) {
      if (!g) {
        g = document.createElement('style');
        g.id = 'quiz-forms-gate';
        g.textContent = 'shopify-forms-embed{display:none!important}';
        document.head.appendChild(g);
      }
    } else if (g) { g.remove(); }
  }
  syncFormsGate(true);
  if (!root) return;
  var DATA = __DATA_JSON__;
  var total = DATA.questions.length;
  var step = -1;
  var answers = [];
  var intro = root.querySelector('[data-quiz-intro]');
  var stepEl = root.querySelector('[data-quiz-step]');
  var resultEl = root.querySelector('[data-quiz-result]');
  var countEl = root.querySelector('[data-quiz-count]');
  var fillEl = root.querySelector('[data-quiz-fill]');
  var qEl = root.querySelector('[data-quiz-question]');
  var optsEl = root.querySelector('[data-quiz-options]');
  var backBtn = root.querySelector('[data-quiz-back]');
  var fxEl = root.querySelector('.quiz__fx');
  var FXDUR = parseFloat('__FXDUR__') || 0.8;
  function motionOK() {
    return !!window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  function firePulse() {
    if (!motionOK() || !fxEl) return;
    gsap.killTweensOf(fxEl);
    gsap.timeline()
      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.2, ease: 'power1.in' })
      .to(fxEl, { opacity: 0.75, duration: FXDUR * 0.45, ease: 'none' })
      .to(fxEl, { opacity: 0, duration: FXDUR * 0.8, ease: 'power2.out' });
  }

  function money(n) { return 'RM' + n.toLocaleString('en-MY'); }

  function renderQuestion() {
    var q = DATA.questions[step];
    countEl.textContent = 'Question ' + (step + 1) + ' of ' + total;
    fillEl.style.width = Math.round(((step + 1) / total) * 100) + '%';
    qEl.textContent = q[0];
    optsEl.innerHTML = '';
    q[1].forEach(function (opt) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'quiz__option';
      b.textContent = opt[1];
      b.addEventListener('click', function () {
        answers[step] = opt[0];
        step++;
        if (step < total) { firePulse(); renderQuestion(); } else { showResult(); }
      });
      optsEl.appendChild(b);
    });
    backBtn.hidden = step === 0;
    intro.hidden = true;
    resultEl.hidden = true;
    stepEl.hidden = false;
    if (motionOK()) {
      gsap.fromTo([countEl, qEl], { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' });
      gsap.fromTo(optsEl.querySelectorAll('.quiz__option'), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.65, stagger: 0.09, ease: 'power3.out', delay: 0.12 });
    }
  }

  function pickWinner() {
    var best = null;
    var bestScore = -1;
    DATA.products.forEach(function (p) {
      var s = 0;
      answers.forEach(function (a) {
        var w = DATA.weights[a] || {};
        if (w[p.key]) s += w[p.key];
      });
      if (s > bestScore) { bestScore = s; best = p; }
    });
    return best;
  }

  function showResult() {
    var p = pickWinner();
    syncFormsGate(false);
    stepEl.hidden = true;
    intro.hidden = true;
    resultEl.hidden = false;
    var img = root.querySelector('[data-quiz-img]');
    img.src = p.img;
    img.alt = p.name;
    root.querySelector('[data-quiz-name]').textContent = p.name;
    root.querySelector('[data-quiz-price]').textContent = (p.from_price ? 'From ' : '') + money(p.price);
    root.querySelector('[data-quiz-was]').textContent = money(p.was);
    root.querySelector('[data-quiz-why]').textContent = p.why;
    root.querySelector('[data-quiz-view]').href = '/products/' + p.handle;
    var addBtn = root.querySelector('[data-quiz-add]');
    addBtn.dataset.variant = p.variant;
    addBtn.textContent = 'Add to cart';
    resultEl.scrollIntoView({ behavior: 'auto', block: 'start' });
    if (motionOK() && fxEl) {
      gsap.fromTo(resultEl, { scale: 0.96, y: 12, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.7, ease: 'power3.out' });
      gsap.killTweensOf(fxEl);
      gsap.set(fxEl, { opacity: 0 });
      gsap.timeline({ delay: 0.15 })
        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.25, ease: 'power1.in' })
        .to(fxEl, { opacity: 0.55, duration: FXDUR * 0.4, ease: 'none' })
        .to(fxEl, { opacity: 0, duration: FXDUR * 0.75, ease: 'power2.out' });
    }
  }

  root.querySelector('[data-quiz-start]').addEventListener('click', function () {
    step = 0;
    answers = [];
    renderQuestion();
  });
  backBtn.addEventListener('click', function () {
    if (step > 0) { step--; renderQuestion(); }
  });
  root.querySelector('[data-quiz-retake]').addEventListener('click', function () {
    step = -1;
    answers = [];
    resultEl.hidden = true;
    stepEl.hidden = true;
    intro.hidden = false;
    syncFormsGate(true);
  });
  root.querySelector('[data-quiz-add]').addEventListener('click', function () {
    var btn = root.querySelector('[data-quiz-add]');
    var variantId = btn.dataset.variant;
    btn.textContent = 'Adding...';
    fetch('/cart/add.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: variantId, quantity: 1 })
    }).then(function (r) {
      if (r.ok) { window.location.href = '/cart'; }
      else { window.location.href = root.querySelector('[data-quiz-view]').href; }
    }).catch(function () {
      window.location.href = root.querySelector('[data-quiz-view]').href;
    });
  });
})();
</script>

{% schema %}
{
  "name": "__SECTION_NAME__",
  "settings": [
    { "type": "text", "id": "eyebrow", "label": "Eyebrow", "default": "__EYEBROW_DEFAULT__" },
    { "type": "text", "id": "heading", "label": "Heading", "default": "__HEADING_DEFAULT__" },
    { "type": "textarea", "id": "subheading", "label": "Subheading", "default": "__SUB_DEFAULT__" }
  ],
  "presets": [{ "name": "__SECTION_NAME__" }]
}
{% endschema %}
'''

def build_section(section_name, eyebrow, heading, sub, products, questions, weights, theme, bar_labels, intro_img):
    data = {
        "questions": [[q, [[a, l] for a, l in opts]] for q, opts in questions],
        "products": [{k: p[k] for k in ("key", "name", "handle", "price", "was", "from_price", "img", "why", "variant")} for p in products],
        "weights": weights,
    }
    out = SECTION_TEMPLATE
    out = out.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
    out = out.replace("__SECTION_NAME__", section_name)
    out = out.replace("__EYEBROW_DEFAULT__", eyebrow)
    out = out.replace("__HEADING_DEFAULT__", heading)
    out = out.replace("__SUB_DEFAULT__", sub)
    out = out.replace("__BAR_LABELS__", bar_labels)
    out = out.replace("__INTRO_IMG__", intro_img)
    for k, v in theme.items():
        out = out.replace("__" + k + "__", v)
    return out

AMARAN_THEME = {
    "BG": "#0f141b", "BG2": "#18202b", "BORDER": "#2a3547",
    "TEXT": "#f2f6fb", "MUTED": "#9aa8ba", "SOFT": "#d3dce8",
    "ACCENT": "#4a9be0", "ACCENT_TEXT": "#0b1220",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(74,155,224,0.25), rgba(74,155,224,0) 70%)",
    "FILL": "linear-gradient(90deg, #2478d4, #6db3f2, #eaf4ff)",
    "BGOP": "0.18",
    "FX": "radial-gradient(circle at 50% 42%, rgba(255,205,130,0.95), rgba(255,170,60,0.5) 50%, transparent 78%)",
    "FXDUR": "0.9s",
}
GODOX_THEME = {
    "BG": "#0b0b0d", "BG2": "#17181d", "BORDER": "#2c2e37",
    "TEXT": "#f5f5f7", "MUTED": "#86868b", "SOFT": "#d2d2d7",
    "ACCENT": "#ff6b2c", "ACCENT_TEXT": "#ffffff",
    "GLOW": "radial-gradient(640px 320px at 50% -40px, rgba(255,107,44,0.22), rgba(255,107,44,0) 70%)",
    "FILL": "#ff6b2c",
    "BGOP": "0.26",
    "FX": "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(255,107,44,0.38) 42%, transparent 68%)",
    "FXDUR": "0.6s",
}
amaran = build_section(
    "Amaran product finder", "AMARAN", "Find your Amaran light",
    "Answer 3 quick questions and we will match you with the right light for how you shoot.",
    AMARAN_PRODUCTS, AMARAN_QUESTIONS, AMARAN_WEIGHTS, AMARAN_THEME,
    '<div class="quiz__bar-labels"><span>2800K</span><span>6500K</span></div>',
    "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/logo-amaran-clean-v2.png?v=1794584832")
godox = build_section(
    "Godox product finder", "GODOX", "Find your Godox gear",
    "Flash, video light, phone flash or trigger - answer 3 quick questions and we will point you to the right one.",
    GODOX_PRODUCTS, GODOX_QUESTIONS, GODOX_WEIGHTS, GODOX_THEME, "", "https://cdn.shopify.com/s/files/1/0693/9230/2147/collections/logo-godox.png?v=1793897642")
open(os.path.join(OUT, "quiz-amaran.liquid"), "w").write(amaran)
open(os.path.join(OUT, "quiz-godox.liquid"), "w").write(godox)
print("sections written:", len(amaran), "bytes amaran;", len(godox), "bytes godox")

# ---- page templates (main-page + quiz section) ----
MAIN_PAGE = {
    "type": "main-page",
    "blocks": {
        "heading": {
            "type": "text", "name": "Title",
            "settings": {
                "text": "<h1>{{ closest.page.title }}</h1>", "width": "100%", "max_width": "normal",
                "alignment": "left", "type_preset": "h2", "font": "var(--font-primary--family)",
                "font_size": "", "line_height": "normal", "letter_spacing": "normal",
                "case": "none", "wrap": "pretty", "background": False,
                "background_color": "#00000026", "corner_radius": 0,
                "padding-block-start": 0, "padding-block-end": 0,
                "padding-inline-start": 0, "padding-inline-end": 0
            },
            "blocks": {}
        },
        "page-content": {"type": "page-content", "settings": {}, "blocks": {}}
    },
    "block_order": ["heading", "page-content"],
    "settings": {
        "content_direction": "column", "gap": 32,
        "background_color": "{{ settings.color_palette.background }}",
        "padding-block-start": 40, "padding-block-end": 80
    }
}

def page_template(section_type):
    return json.dumps({
        "sections": {"main": MAIN_PAGE, "quiz": {"type": section_type, "settings": {}}},
        "order": ["main", "quiz"]
    }, indent=2, ensure_ascii=False)

open(os.path.join(OUT, "page.quiz-amaran.json"), "w").write(page_template("quiz-amaran"))
open(os.path.join(OUT, "page.quiz-godox.json"), "w").write(page_template("quiz-godox"))
print("page templates written")

# ---- quiz entry banner (shows only on the Amaran / Godox collection pages) ----
ENTRY_SECTION = r'''{% if collection.handle == 'amaran' %}
<div class="quiz-entry quiz-entry--amaran">
  <div class="quiz-entry__inner">
    <div class="quiz-entry__text">
      <p class="quiz-entry__eyebrow">AMARAN</p>
      <h3 class="quiz-entry__title">Not sure which light is right for you?</h3>
      <p class="quiz-entry__sub">Answer 3 quick questions &mdash; 30 seconds &mdash; and we will match you with the right Amaran light.</p>
      <a class="quiz-entry__btn" href="/pages/find-your-amaran-light">Find your light</a>
    </div>
    <div class="quiz-entry__media"><img src="https://cdn.shopify.com/s/files/1/0693/9230/2147/files/logo-amaran-clean-v2.png?v=1794584832" alt="Amaran" loading="lazy"></div>
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
    <div class="quiz-entry__media"><img src="https://cdn.shopify.com/s/files/1/0693/9230/2147/collections/logo-godox.png?v=1793897642" alt="Godox" loading="lazy"></div>
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
  .quiz-entry__media { width: 260px; flex-shrink: 0; position: relative; overflow: hidden; }
  .quiz-entry__media img { position: absolute; width: 150%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }
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
'''
open(os.path.join(OUT, "quiz-entry.liquid"), "w").write(ENTRY_SECTION)
print("entry section written:", len(ENTRY_SECTION), "bytes")

# ---- collection.json with the entry section inserted after the heading ----
coll = json.load(open("/tmp/collection.json"))
coll["sections"]["quiz-entry"] = {"type": "quiz-entry", "settings": {}}
order = coll["order"]
order.insert(order.index("section") + 1, "quiz-entry")
coll["order"] = order
open(os.path.join(OUT, "collection.json"), "w").write(json.dumps(coll, indent=2, ensure_ascii=False))
print("collection.json written, order:", coll["order"])

# ---- homepage block: two quiz cards with a title ----
HOME_SECTION = r'''<div class="quiz-home">
  <div class="quiz-home__head">
    <p class="quiz-home__eyebrow">{{ section.settings.eyebrow }}</p>
    <h2 class="quiz-home__title">{{ section.settings.heading }}</h2>
    <p class="quiz-home__sub">{{ section.settings.subheading }}</p>
  </div>
  <div class="quiz-home__grid">
    <a class="quiz-home__card quiz-home__card--amaran" href="/pages/find-your-amaran-light">
      <div class="quiz-home__media"><img src="__AMARAN_IMG__" alt="Amaran" loading="lazy"></div>
      <div class="quiz-home__body">
        <p class="quiz-home__card-eyebrow">AMARAN</p>
        <h3 class="quiz-home__card-title">Find your Amaran light</h3>
        <p class="quiz-home__card-sub">Halo or RAY, studio or portable &mdash; 3 questions to the right light.</p>
        <span class="quiz-home__btn">Take the quiz</span>
      </div>
    </a>
    <a class="quiz-home__card quiz-home__card--godox" href="/pages/find-your-godox-gear">
      <div class="quiz-home__media"><img src="__GODOX_IMG__" alt="Godox" loading="lazy"></div>
      <div class="quiz-home__body">
        <p class="quiz-home__card-eyebrow">GODOX</p>
        <h3 class="quiz-home__card-title">Find your Godox gear</h3>
        <p class="quiz-home__card-sub">Flash, video light, phone flash or trigger &mdash; 3 questions to the right gear.</p>
        <span class="quiz-home__btn">Take the quiz</span>
      </div>
    </a>
  </div>
</div>

{% stylesheet %}
  .quiz-home { max-width: 1200px; margin: 0 auto; padding: 64px 20px; text-align: center; }
  .quiz-home__eyebrow { font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase; color: #6e6e73; margin: 0 0 12px; font-weight: 600; }
  .quiz-home__title { font-size: 32px; line-height: 1.2; margin: 0 0 10px; letter-spacing: -0.01em; color: #1d1d1f; }
  .quiz-home__sub { font-size: 17px; line-height: 1.55; color: #6e6e73; margin: 0 auto 36px; max-width: 560px; }
  .quiz-home__grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; text-align: left; }
  .quiz-home__card { display: block; border-radius: 20px; overflow: hidden; text-decoration: none; transition: transform 0.25s ease, box-shadow 0.25s ease; }
  .quiz-home__card:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0,0,0,0.22); }
  .quiz-home__card--amaran { background: #0f141b; }
  .quiz-home__card--godox { background: #0b0b0d; }
  .quiz-home__media { height: 220px; position: relative; overflow: hidden; }
  .quiz-home__card--amaran .quiz-home__media { background: radial-gradient(420px 200px at 50% 0%, rgba(74,155,224,0.30), rgba(74,155,224,0) 70%), #0f141b; }
  .quiz-home__card--godox .quiz-home__media { background: radial-gradient(420px 200px at 50% 0%, rgba(255,107,44,0.28), rgba(255,107,44,0) 70%), #0b0b0d; }
  .quiz-home__media img { position: absolute; width: 130%; max-width: none; height: auto; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.12; display: block; }
  .quiz-home__body { padding: 28px 28px 32px; }
  .quiz-home__card-eyebrow { font-size: 12px; letter-spacing: 0.22em; font-weight: 600; margin: 0 0 10px; }
  .quiz-home__card--amaran .quiz-home__card-eyebrow { color: #4a9be0; }
  .quiz-home__card--godox .quiz-home__card-eyebrow { color: #ff6b2c; }
  .quiz-home__card-title { font-size: 24px; line-height: 1.3; margin: 0 0 8px; color: #f5f5f7; }
  .quiz-home__card-sub { font-size: 15px; line-height: 1.55; color: #a8a8ad; margin: 0 0 22px; }
  .quiz-home__btn { display: inline-block; border-radius: 999px; padding: 12px 26px; font-size: 15px; font-weight: 600; line-height: 1.2; }
  .quiz-home__card--amaran .quiz-home__btn { background: #4a9be0; color: #0b1220; }
  .quiz-home__card--godox .quiz-home__btn { background: #ff6b2c; color: #ffffff; }
  @media (max-width: 640px) {
    .quiz-home { padding: 48px 20px; }
    .quiz-home__title { font-size: 26px; }
    .quiz-home__grid { grid-template-columns: 1fr; }
    .quiz-home__media { height: 180px; }
    .quiz-home__media img { width: 140%; }
  }
{% endstylesheet %}

{% schema %}
{
  "name": "Product finder - homepage",
  "settings": [
    { "type": "text", "id": "eyebrow", "label": "Eyebrow", "default": "FIND YOUR GEAR" },
    { "type": "text", "id": "heading", "label": "Heading", "default": "Not sure where to start?" },
    { "type": "textarea", "id": "subheading", "label": "Subheading", "default": "Answer 3 quick questions and we will match you with the right gear. 30 seconds, no email needed." }
  ],
  "presets": [{ "name": "Product finder - homepage" }]
}
{% endschema %}
'''
HOME_SECTION = HOME_SECTION.replace("__AMARAN_IMG__", "https://cdn.shopify.com/s/files/1/0693/9230/2147/files/logo-amaran-clean-v2.png?v=1794584832")
HOME_SECTION = HOME_SECTION.replace("__GODOX_IMG__", "https://cdn.shopify.com/s/files/1/0693/9230/2147/collections/logo-godox.png?v=1793897642")
open(os.path.join(OUT, "quiz-home.liquid"), "w").write(HOME_SECTION)
print("home section written:", len(HOME_SECTION), "bytes")

# ---- index.json: insert quiz-home between guides row and brands ----
idx = json.load(open("/tmp/index.json"))
idx["sections"]["quiz-home"] = {"type": "quiz-home", "settings": {}}
order = idx["order"]
order.insert(order.index("rynow_guides_row") + 1, "quiz-home")
idx["order"] = order
open(os.path.join(OUT, "index.json"), "w").write(json.dumps(idx, indent=2, ensure_ascii=False))
print("index.json written, order:", idx["order"])
