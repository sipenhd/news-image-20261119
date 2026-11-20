#!/usr/bin/env python3
"""Build entry.png - 19 Nov 2026 world news front page, 1024x1024."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (17, 24, 39)
NAVY = (15, 42, 68)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 116, 144)
GREY = (75, 85, 99)
LIGHT_LINE = (203, 199, 186)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((48, 22), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 52), fill=(255, 255, 255))
d.text((48, 82), "THURSDAY  •  19 NOVEMBER 2026  •  SIX STORIES, ONE DAY", font=font(SANS_B, 20), fill=GOLD)

# Lead story
y = 142
d.rectangle([48, y + 4, 58, y + 210], fill=RED)
d.text((76, y), "THE HAGUE  —  JUSTICE", font=font(SANS_B, 20), fill=RED)
y += 32
d.text((76, y), "THE COURT SPEAKS:", font=font(SERIF_B, 56), fill=INK)
y += 64
d.text((76, y), "GENOCIDE", font=font(SERIF_B, 56), fill=INK)
y += 70
y = draw_wrapped(d, 76, y, "The World Court finds Myanmar guilty of genocide against the Rohingya — the first such ruling against a state. A 9–6 verdict on the 2017 campaign in Rakhine.", font(SANS, 24), 900, leading=8)
d.line([(48, 400), (976, 400)], fill=LIGHT_LINE, width=2)

# Middle two columns
y0 = 418
# left
d.text((48, y0), "SHENZHEN  —  DIPLOMACY", font=font(SANS_B, 18), fill=TEAL)
d.text((48, y0 + 28), "THREE MEN,", font=font(SERIF_B, 40), fill=INK)
d.text((48, y0 + 76), "ONE TABLE", font=font(SERIF_B, 40), fill=INK)
draw_wrapped(d, 48, y0 + 132, "Trump, Xi and Putin meet for the first three-way summit — and sign a “Declaration toward Peace” that says nothing about Ukraine or Iran.", font(SANS, 21), 440, leading=6)
# divider vertical
d.line([(512, 412), (512, 690)], fill=LIGHT_LINE, width=2)
# right
d.text((544, y0), "WALL STREET  —  TECH", font=font(SANS_B, 18), fill=TEAL)
d.text((544, y0 + 28), "THE $81 BILLION", font=font(SERIF_B, 40), fill=INK)
d.text((544, y0 + 76), "DEBUT", font=font(SERIF_B, 40), fill=INK)
draw_wrapped(d, 544, y0 + 132, "Anthropic prices its shares at $83 — the biggest IPO ever. The AI maker opens higher on day one, even as the market slides.", font(SANS, 21), 432, leading=6)

d.line([(48, 712), (976, 712)], fill=LIGHT_LINE, width=2)

# Bottom three columns
cols = [
    ("MARKETS  —  ECONOMY", "MARKETS SHIVER", "The S&P 500 falls 2.0%, a fifth straight loss. Japan’s Nikkei drops 4.68% as AI valuations wobble."),
    ("UKRAINE  —  WAR", "BRIDGE HIT AGAIN", "Ukraine strikes the Crimean Bridge a third time in four days. Putin vows a harsher response."),
    ("GAZA  —  CONFLICT", "THE LINE CROSSED", "Israeli tanks push past the Yellow Line near Nuseirat. Aid groups score the peace plan 4 out of 26."),
]
x = 48
for kicker, head, body in cols:
    d.text((x, 732), kicker, font=font(SANS_B, 15), fill=RED)
    # headline wrapped, 30pt serif
    yy = draw_wrapped(d, x, 758, head, font(SERIF_B, 30), 288, leading=4)
    draw_wrapped(d, x, yy + 6, body, font(SANS, 19), 288, leading=5)
    x += 312
    if x < 900:
        d.line([(x - 16, 732), (x - 16, 950)], fill=LIGHT_LINE, width=2)

# Footer
d.rectangle([0, 972, W, H], fill=NAVY)
d.text((48, 986), "Six stories. One day. The world, in a single frame.", font=font(SANS_B, 20), fill=(255, 255, 255))
d.text((48, 986), "", font=font(SANS, 14), fill=GREY)

out = "/home/hatch/workspace/make-fun-bounties/news-image-20261119/entry.png"
img.save(out, "PNG", optimize=True)
import os
print("saved", out, os.path.getsize(out), "bytes", img.size)
