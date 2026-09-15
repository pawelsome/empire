#!/usr/bin/env python3
"""Render 1200x630 share images for blog posts into assets/img/blog/<slug>.png.

Run locally after adding posts (needs Pillow):  python tools/make_og.py [--force]
"""

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path(__file__).resolve().parent.parent
OUT = SRC / "assets" / "img" / "blog"
SANS = SRC / "tools" / "fonts" / "IBMPlexSans-SemiBold.ttf"
MONO = SRC / "tools" / "fonts" / "IBMPlexMono-Medium.ttf"

PAPER, INK, MUTED, ACCENT, DOT = (243, 241, 236), (21, 23, 26), (107, 111, 117), (200, 71, 27), (214, 209, 199)
CROWN = [(349, 3), (503, 157), (223, 437), (268, 491), (206, 552), (2, 348), (179, 351), (175, 173), (352, 179)]
BRACKET = [(597, 250), (659, 313), (377, 597), (470, 690), (753, 407), (816, 470), (470, 816), (250, 597)]
SS = 2  # supersampling


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def render(meta, path):
    W, H = 1200 * SS, 630 * SS
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(40 * SS, W, 24 * SS):
        for y in range(40 * SS, H - 40 * SS, 24 * SS):
            if x > W * 0.62:
                d.ellipse([x - SS, y - SS, x + SS, y + SS], fill=DOT)

    # logo + name
    size, ox, oy = 52 * SS, 72 * SS, 62 * SS
    for poly in (CROWN, BRACKET):
        d.polygon([(ox + px * size / 818, oy + py * size / 818) for px, py in poly], fill=INK)
    d.text((ox + size + 18 * SS, oy + 8 * SS), "Empire Corporation", font=ImageFont.truetype(str(SANS), 30 * SS), fill=INK)

    # category
    mono = ImageFont.truetype(str(MONO), 22 * SS)
    d.text((72 * SS, 170 * SS), meta["category"].upper(), font=mono, fill=ACCENT)

    # title: shrink until it fits in 4 lines
    for fs in (66, 60, 54, 48, 44):
        font = ImageFont.truetype(str(SANS), fs * SS)
        lines = wrap(d, meta["title"], font, 1000 * SS)
        if len(lines) <= 4:
            break
    y = 214 * SS
    for line in lines[:4]:
        d.text((72 * SS, y), line, font=font, fill=INK)
        y += int(fs * 1.16) * SS

    d.text((72 * SS, 548 * SS), "empirecorporation.eu/blog", font=ImageFont.truetype(str(MONO), 20 * SS), fill=MUTED)
    d.rectangle([0, H - 10 * SS, W, H], fill=INK)
    d.rectangle([0, H - 10 * SS, 180 * SS, H], fill=ACCENT)

    im.resize((1200, 630), Image.LANCZOS).save(path, optimize=True)


def main():
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for f in sorted((SRC / "blog-src" / "posts").glob("*.html")):
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*META-->", f.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        meta = json.loads(m.group(1))
        target = OUT / f"{f.stem}.png"
        if target.exists() and not force:
            continue
        render(meta, target)
        made += 1
    print(f"rendered {made} image(s) into {OUT}")


if __name__ == "__main__":
    main()
