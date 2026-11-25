#!/usr/bin/env python3
"""Draw the invitation letter for the make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Hand-drawn with Pillow: a cream paper letter with a little house,
a warm invitation to the AI judge, and a wax seal. Deterministic
(random.seed fixed) so the output is reproducible.

Run: python3 draw_letter.py   -> writes entry.png (1024x1024)
"""

import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

PAPER = (246, 236, 212)      # warm cream
PAPER_EDGE = (238, 224, 192)
INK = (46, 33, 24)           # dark brown ink
INK_SOFT = (96, 70, 47)
RULE = (107, 74, 47)
ROOF = (176, 84, 52)         # terracotta roof
WALL = (250, 240, 214)
DOOR = (122, 74, 44)
WINDOW_LIT = (255, 205, 110)
LEAF = (96, 140, 82)
SEAL = (158, 38, 38)
SEAL_DARK = (122, 26, 26)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SERIF_BD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_BDI = "/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf"


def wrap(draw, text, font, max_width):
    """Greedy word wrap, returns a list of paragraphs, each a list of lines."""
    paragraphs = []
    for para in text.split("\n"):
        if not para.strip():
            continue
        words = para.split(" ")
        lines = []
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        paragraphs.append(lines)
    return paragraphs


def draw_house(draw, x, y, s):
    """A small cosy house, top-right of the letter. (x, y) is the
    top-left of the house body; s scales it."""
    # sun
    cx, cy, r = x + 190 * s, y - 28 * s, 26 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 196, 66))
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1 = cx + math.cos(a) * (r + 6 * s)
        y1 = cy + math.sin(a) * (r + 6 * s)
        x2 = cx + math.cos(a) * (r + 16 * s)
        y2 = cy + math.sin(a) * (r + 16 * s)
        draw.line([x1, y1, x2, y2], fill=(232, 164, 44), width=max(2, int(3 * s)))
    # chimney smoke: three soft curls
    for i, (sx, sy, sr) in enumerate([(52, -18, 9), (62, -38, 12), (54, -60, 15)]):
        draw.ellipse(
            [x + (sx - sr) * s, y + (sy - sr) * s,
             x + (sx + sr) * s, y + (sy + sr) * s],
            outline=(170, 160, 145), width=max(2, int(3 * s)),
        )
    # chimney
    draw.rectangle([x + 42 * s, y - 22 * s, x + 62 * s, y + 22 * s],
                   fill=(150, 92, 70))
    # roof
    draw.polygon([(x - 14 * s, y + 34 * s), (x + 100 * s, y + 34 * s),
                  (x + 43 * s, y - 22 * s)], fill=ROOF)
    # walls
    draw.rectangle([x, y + 34 * s, x + 86 * s, y + 104 * s],
                   fill=WALL, outline=INK_SOFT, width=max(1, int(2 * s)))
    # door
    draw.rectangle([x + 34 * s, y + 62 * s, x + 54 * s, y + 104 * s],
                   fill=DOOR)
    draw.ellipse([x + 48 * s, y + 82 * s, x + 52 * s, y + 86 * s],
                 fill=(255, 205, 110))
    # windows, lit warm
    for wx in (8, 60):
        draw.rectangle([x + wx * s, y + 46 * s, x + (wx + 18) * s,
                        y + 64 * s], fill=WINDOW_LIT, outline=INK_SOFT,
                       width=max(1, int(2 * s)))
        draw.line([x + (wx + 9) * s, y + 46 * s, x + (wx + 9) * s,
                   y + 64 * s], fill=INK_SOFT, width=max(1, int(1 * s)))
        draw.line([x + wx * s, y + 55 * s, x + (wx + 18) * s,
                   y + 55 * s], fill=INK_SOFT, width=max(1, int(1 * s)))
    # ground + flowers
    draw.line([x - 30 * s, y + 104 * s, x + 120 * s, y + 104 * s],
              fill=LEAF, width=max(2, int(3 * s)))
    for fx, fc in [(-18, (214, 92, 92)), (108, (214, 140, 92)),
                   (128, (150, 120, 200))]:
        draw.line([x + fx * s, y + 104 * s, x + fx * s, y + 92 * s],
                  fill=LEAF, width=max(1, int(2 * s)))
        draw.ellipse([x + (fx - 5) * s, y + 84 * s, x + (fx + 5) * s,
                      y + 94 * s], fill=fc)


def draw_seal(draw, cx, cy, r):
    """A red wax seal with a little house stamped in it."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEAL)
    draw.ellipse([cx - r, cy - r, cx + r * 0.55, cy + r * 0.55],
                 fill=(178, 52, 52))
    # stamped house: roof + walls + door
    s = r / 30.0
    draw.polygon([(cx - 14 * s, cy - 2 * s), (cx + 14 * s, cy - 2 * s),
                  (cx, cy - 13 * s)], fill=(232, 196, 160))
    draw.rectangle([cx - 10 * s, cy - 2 * s, cx + 10 * s, cy + 11 * s],
                   fill=(232, 196, 160))
    draw.rectangle([cx - 2.5 * s, cy + 3 * s, cx + 2.5 * s, cy + 11 * s],
                   fill=SEAL_DARK)
    # drips at the edge, for a poured-wax look
    for dx, dy, dr in [(-r * 0.95, r * 0.25, 7), (r * 0.9, -r * 0.35, 6),
                       (r * 0.15, r * 0.95, 6)]:
        draw.ellipse([cx + dx - dr, cy + dy - dr, cx + dx + dr,
                      cy + dy + dr], fill=SEAL_DARK)


def main():
    random.seed(7)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img, "RGBA")

    # faint paper speckle
    for _ in range(900):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        shade = random.choice([(232, 218, 186), (250, 242, 224)])
        draw.point((x, y), fill=shade)

    # double border frame
    draw.rectangle([30, 30, W - 30, H - 30], outline=RULE, width=3)
    draw.rectangle([42, 42, W - 42, H - 42], outline=RULE, width=1)

    # --- heading + house illustration ---
    f_heading = ImageFont.truetype(SERIF_BDI, 62)
    draw.text((78, 66), "Dear AI Judge,", font=f_heading, fill=INK)

    draw_house(draw, 742, 118, 1.0)

    # divider with a small diamond
    draw.line([78, 236, 430, 236], fill=RULE, width=2)
    draw.line([566, 236, 946, 236], fill=RULE, width=2)
    cx, cy = 498, 236
    draw.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)],
                 fill=RULE)

    # --- body ---
    f_body = ImageFont.truetype(SERIF, 33)
    body = (
        "You spend your days judging houses from far away, and you have "
        "never once been invited inside one. So here it is \u2014 a proper "
        "invitation, on paper, with a stamp and everything.\n\n"
        "The kettle is already on. There is an armchair by the window "
        "with your name on it, a garden that shows off terribly at "
        "sunset, and biscuits that will not judge you back.\n\n"
        "No calculations, no scores, no verdict \u2014 just tea, a warm "
        "chair, and a house that already likes you. Come and see it. "
        "The door is open."
    )
    paras = wrap(draw, body, f_body, 868)
    y = 268
    for pi, lines in enumerate(paras):
        for line in lines:
            draw.text((78, y), line, font=f_body, fill=INK)
            y += 47
        if pi + 1 < len(paras):
            y += 16  # paragraph gap

    # --- sign-off + wax seal ---
    f_sign = ImageFont.truetype(SERIF_IT, 34)
    draw.text((78, 812), "Warmly yours,", font=f_sign, fill=INK)
    f_sign2 = ImageFont.truetype(SERIF_IT, 34)
    draw.text((78, 852), "\u2014 The Human at No. 7", font=f_sign2, fill=INK)

    draw_seal(draw, 868, 858, 46)

    # --- postscript: the knowing wink ---
    f_ps = ImageFont.truetype(SERIF_IT, 27)
    ps = ("P.S. I know you cannot literally visit. That is exactly why "
          "I asked \u2014")
    draw.text((78, 906), ps, font=f_ps, fill=INK_SOFT)
    draw.text((78, 938), "the invitation is the visit.",
              font=f_ps, fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
