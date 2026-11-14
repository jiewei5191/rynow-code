#!/usr/bin/env python3
"""Build the new RYNOW 11.11 poster for 1-17 Nov 2026.

Starts from the original baked poster (rynow-1111-hero-final-2026.png, 2043x770)
and changes only:
  1. Date line  "1 - 11 NOVEMBER 2026" -> "1 - 17 NOVEMBER 2026"
     (old text covered with a vertically-interpolated silk patch, feathered)
  2. New slogan line "11.11 ended. RYNOW hasn't." (bold, between subline and button)
  3. The black "SHOP ALL DEALS ->" pill moved down ~56px to make room
     (old pill covered with a silk patch, redrawn at the lower position)

Everything else (silk background, giant metallic 11.11 + sphere, RYNOW,
headlines, subline) is untouched.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC = "/tmp/rynow-1111-hero-final-2026.png"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "rynow-1111-poster-17nov.png")

LIB_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
LIB_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

BLACK = (0, 0, 0)
BUTTON_FILL = (21, 21, 21)
WHITE = (255, 255, 255)


def silk_patch(img, box):
    """Fill `box` (x0, y0, x1, y1) with silk sampled from its own borders.

    Coons (transfinite) interpolation: the fill blends the horizontal
    interpolation between the clean left/right border columns with the
    vertical interpolation between the clean top/bottom border rows,
    minus the bilinear corner term. It matches all four borders exactly,
    so the silk's diagonal folds pass through the patch instead of being
    flattened into a uniform strip (pure horizontal interpolation left a
    faint band behind the date line). Paste through a narrow-feathered
    mask (full strength inside, ~6px fade) so the interior is fully
    replaced and only the edge blends.
    """
    x0, y0, x1, y1 = box
    arr = np.array(img).astype(np.float32)
    w = x1 - x0
    h = y1 - y0
    left = arr[y0:y1, x0 - 1, :]     # (h, 3)
    right = arr[y0:y1, x1 + 1, :]    # (h, 3)
    top = arr[y0 - 1, x0:x1, :]      # (w, 3)
    bottom = arr[y1 + 1, x0:x1, :]   # (w, 3)
    tx = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]  # (1, w, 1)
    ty = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]  # (h, 1, 1)
    H = left[:, None, :] * (1 - tx) + right[:, None, :] * tx    # horizontal
    V = top[None, :, :] * (1 - ty) + bottom[None, :, :] * ty    # vertical
    # bilinear corner term
    c_tl = arr[y0 - 1, x0 - 1, :]
    c_tr = arr[y0 - 1, x1 + 1, :]
    c_bl = arr[y1 + 1, x0 - 1, :]
    c_br = arr[y1 + 1, x1 + 1, :]
    B = ((c_tl * (1 - tx) + c_tr * tx) * (1 - ty)
         + (c_bl * (1 - tx) + c_br * tx) * ty)
    fill = H + V - B
    patch = Image.fromarray(np.clip(fill, 0, 255).astype(np.uint8), "RGB")
    # mask: solid over the whole box, feathered only ~6px at the edges
    # (the feather zones sit above the old text/button, so nothing ghosts
    # through; a wider feather spreads the edge step so it can't read as a line)
    mask = Image.new("L", (w, h), 255)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    img.paste(patch, (x0, y0), mask)
    return img


def draw_tracked(draw, x, baseline_y, text, font, fill, tracking):
    """Draw text with manual letter-spacing; returns total drawn width."""
    cx = x
    for ch in text:
        draw.text((cx, baseline_y), ch, font=font, fill=fill, anchor="ls")
        cx += draw.textlength(ch, font=font) + tracking
    return cx - tracking - x


def tracked_width(draw, text, font, tracking):
    w = 0.0
    for ch in text:
        w += draw.textlength(ch, font=font) + tracking
    return w - tracking


def main():
    im = Image.open(SRC).convert("RGB")
    assert im.size == (2043, 770), im.size

    # --- 1. cover the old date line (measured: x 143-497, y 290-302) ---
    im = silk_patch(im, (136, 283, 505, 309))

    # --- 2. cover the old button pill (measured: x 143-495, y 556-613) ---
    im = silk_patch(im, (136, 549, 502, 620))

    d = ImageDraw.Draw(im)

    # --- 3. redraw the date line: "1 - 17 NOVEMBER 2026" ---
    # Original: x 143-497 (354 px wide), cap height ~13px, baseline ~302.
    date_text = "1 \u2013 17 NOVEMBER 2026"
    date_font = ImageFont.truetype(LIB_REG, 18)
    # tune tracking so the redrawn line is exactly 354 px wide like the original
    lo, hi = 0.0, 15.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if tracked_width(d, date_text, date_font, mid) < 354:
            lo = mid
        else:
            hi = mid
    tracking = (lo + hi) / 2
    w = draw_tracked(d, 143, 302, date_text, date_font, BLACK, tracking)
    print(f"date line: tracking={tracking:.2f} width={w:.1f} (target 354)")

    # --- 4. new slogan: "11.11 ended. RYNOW hasn't." ---
    slogan = "11.11 ended. RYNOW hasn't."
    slogan_font = ImageFont.truetype(LIB_BOLD, 40)
    sw = d.textlength(slogan, font=slogan_font)
    print(f"slogan width={sw:.1f} (x 143 -> {143 + sw:.0f})")
    d.text((143, 573), slogan, font=slogan_font, fill=BLACK, anchor="ls")

    # --- 5. redraw the button pill 56px lower: y 612-670 (was 556-613) ---
    bx0, by0, bx1, by1 = 143, 612, 495, 670
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=5, fill=BUTTON_FILL)
    btn_text = "SHOP ALL DEALS \u2192"
    btn_font = ImageFont.truetype(LIB_REG, 15)
    # original button text: cap height ~11px, letterspaced; centre it
    bw = tracked_width(d, btn_text, btn_font, 4.0)
    cx = (bx0 + bx1) / 2
    draw_tracked(d, cx - bw / 2, 646, btn_text, btn_font, WHITE, 4.0)
    print(f"button text width={bw:.1f} centred at x={cx:.0f}")

    im.save(OUT, "PNG")
    print("saved", OUT, im.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
