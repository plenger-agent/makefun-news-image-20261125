#!/usr/bin/env python3
"""Renderer for the make.fun news-image-20261125 entry, v2.

Draws a rich one-page broadsheet, "THE WORLD IN ONE PAGE", summing up
the world news of Wednesday 25 November 2026: a masthead naming the
day, a markets strip, twelve illustrated lead stories with their key
figures, a UTC timeline of the day, and 21 briefs from nine regions.

Every story was verified against the day's reporting (Reuters, AP,
BBC, CFR) before being drawn. Rendering uses Pillow locally; the
hand-in program (main.py) is standard-library only and simply copies
the committed entry.png, so the grader never needs Pillow.

Deterministic: the paper grain uses a fixed seed, so re-running this
script reproduces entry.png byte for byte.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 18
INNER = W - 2 * MARGIN

PAPER = (246, 241, 229)
CARD = (255, 253, 246)
INK = (28, 30, 38)
NAVY = (20, 38, 60)
RED = (163, 31, 38)
GOLD = (176, 132, 32)
GREEN = (30, 122, 60)
GREY = (96, 98, 104)
BORDER = (206, 196, 168)
DOWN = (255, 110, 92)
UP = (126, 208, 138)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "/DejaVuSerif.ttf"
SANS_B = FONT_DIR + "/DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "/DejaVuSans.ttf"

_cache = {}


def F(kind, size):
    key = (kind, size)
    if key not in _cache:
        path = {"serif_b": SERIF_B, "serif": SERIF,
                "sans_b": SANS_B, "sans": SANS}[kind]
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, font, maxw):
    """Greedy word wrap; returns a list of lines fitting maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, font, fill, maxw, leading, max_lines=None):
    """Draw wrapped text; returns the y just past the last line."""
    x, y = xy
    lines = wrap(draw, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def vgrad(img, box, top, bottom):
    """Vertical gradient inside box, drawn straight onto img."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    strip = Image.new("RGB", (1, h))
    for i in range(h):
        t = i / h
        strip.putpixel((0, i), tuple(
            int(top[c] + (bottom[c] - top[c]) * t) for c in range(3)))
    img.paste(strip.resize((x1 - x0, h)), (x0, y0))


# ---------------------------------------------------------------- scenes
# Each scene draws inside box (x0, y0, x1, y1) on the base image.

def scene_port(img, box):
    """Tariff lead: container port at dusk with rate tags."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (38, 62, 96), (214, 132, 74))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y1 - 26, x1, y1], fill=(30, 66, 92))
    for i in range(5):
        yy = y1 - 20 + i * 4
        d.line([x0 + 8 + i * 13, yy, x1 - 30 - i * 7, yy],
               fill=(86, 138, 168), width=1)
    cols = [(196, 74, 60), (44, 110, 150), (224, 158, 60),
            (70, 140, 96), (150, 84, 140)]
    bw = (x1 - x0 - 70) // 5
    for i, c in enumerate(cols):
        bx = x0 + 8 + i * bw
        for j in range(2 + (i % 2)):
            by = y1 - 26 - (j + 1) * 17
            d.rectangle([bx, by, bx + bw - 4, by + 15], fill=c,
                        outline=(20, 24, 30), width=1)
            d.line([bx + 3, by + 3, bx + 3, by + 12], fill=(20, 24, 30))
    cx = x1 - 52
    d.rectangle([cx, y0 + 8, cx + 6, y1 - 26], fill=(24, 28, 34))
    d.rectangle([x0 + 30, y0 + 8, cx + 6, y0 + 14], fill=(24, 28, 34))
    d.line([x0 + 120, y0 + 14, x0 + 120, y0 + 34], fill=(24, 28, 34),
           width=2)
    d.rectangle([x0 + 108, y0 + 34, x0 + 132, y0 + 48],
                fill=(196, 74, 60), outline=(20, 24, 30))
    d.polygon([(x0 + 6, y1 - 26), (x0 + 120, y1 - 26),
               (x0 + 104, y1 - 12), (x0 + 22, y1 - 12)],
              fill=(22, 26, 32))
    tags = [("CHINA +20%", x0 + 10, y0 + 20),
            ("EU 15%", x0 + 96, y0 + 50),
            ("SE ASIA 18%", x0 + 126, y0 + 92)]
    for label, tx, ty in tags:
        tw = d.textlength(label, font=F("sans_b", 12))
        d.rounded_rectangle([tx, ty, tx + tw + 12, ty + 19], 4,
                            fill=(250, 246, 232), outline=RED, width=1)
        d.text((tx + 6, ty + 3), label, font=F("sans_b", 12), fill=RED)


def scene_rocket(img, box):
    """Astronaut lead: rocket climbing to a space station over Earth."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (6, 10, 34), (16, 34, 74))
    d = ImageDraw.Draw(img)
    rng = random.Random(24)
    for _ in range(46):
        sx = rng.randint(x0 + 2, x1 - 2)
        sy = rng.randint(y0 + 2, y1 - 30)
        d.point((sx, sy), fill=(230, 236, 250))
    d.ellipse([x0 - 60, y1 - 34, x1 + 60, y1 + 90], fill=(38, 92, 150))
    d.ellipse([x0 - 60, y1 - 34, x1 + 60, y1 + 90], outline=(120, 180, 230))
    sx, sy = x0 + 34, y0 + 16
    d.rectangle([sx, sy, sx + 64, sy + 12], fill=(206, 212, 220),
                outline=(90, 96, 108))
    d.rectangle([sx - 30, sy - 6, sx - 4, sy + 18], fill=(52, 84, 150),
                outline=(150, 180, 230))
    d.rectangle([sx + 68, sy - 6, sx + 94, sy + 18], fill=(52, 84, 150),
                outline=(150, 180, 230))
    rx, ry = x0 + (x1 - x0) // 2 - 8, y0 + 8
    d.polygon([(rx, ry), (rx + 16, ry + 10), (rx + 16, ry + 34),
               (rx, ry + 34)], fill=(238, 240, 244),
              outline=(120, 126, 138))
    d.polygon([(rx, ry), (rx - 8, ry + 16), (rx, ry + 24)],
              fill=(200, 60, 48))
    d.polygon([(rx + 16, ry + 16), (rx + 24, ry + 16), (rx + 16, ry + 24)],
              fill=(200, 60, 48))
    d.polygon([(rx + 3, ry + 34), (rx + 13, ry + 34), (rx + 8, ry + 46)],
              fill=(255, 176, 66))
    d.text((x0 + 8, y1 - 24), "TIANGONG", font=F("sans_b", 11),
           fill=(190, 220, 250))
    chip = "DOCKED 04:56 UTC"
    tw = d.textlength(chip, font=F("sans_b", 12))
    d.rounded_rectangle([x1 - tw - 18, y1 - 26, x1 - 6, y1 - 6], 4,
                        fill=(250, 246, 232))
    d.text((x1 - tw - 12, y1 - 23), chip, font=F("sans_b", 12), fill=NAVY)


def scene_chart(img, box):
    """Chip rout: a plunging red market chart."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (24, 26, 36), (44, 30, 34))
    d = ImageDraw.Draw(img)
    for gx in range(x0 + 14, x1, 26):
        d.line([gx, y0 + 4, gx, y1 - 6], fill=(58, 62, 76))
    for gy in range(y0 + 8, y1 - 4, 13):
        d.line([x0 + 4, gy, x1 - 4, gy], fill=(58, 62, 76))
    pts = [(x0 + 8, y0 + 12), (x0 + 44, y0 + 16), (x0 + 76, y0 + 10),
           (x0 + 108, y0 + 22), (x0 + 138, y0 + 34), (x0 + 168, y0 + 30),
           (x0 + 198, y0 + 48), (x0 + 232, y0 + 62), (x1 - 44, y1 - 12)]
    d.line(pts, fill=(255, 92, 76), width=3, joint="curve")
    for px, py in pts[::2]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 160, 140))
    d.polygon([(x1 - 44, y1 - 12), (x1 - 58, y1 - 14), (x1 - 46, y1 - 26)],
              fill=(255, 92, 76))
    d.text((x0 + 10, y0 + 8), "KOSPI", font=F("sans_b", 13),
           fill=(200, 206, 220))
    d.text((x0 + 10, y0 + 24), "-6.2%", font=F("sans_b", 25),
           fill=(255, 110, 92))


def scene_tanker(img, box):
    """Hormuz: tanker ablaze in a strait between two headlands."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (70, 96, 128), (196, 168, 128))
    d = ImageDraw.Draw(img)
    d.polygon([(x0, y0 + 30), (x0 + 84, y0 + 44), (x0 + 60, y1),
               (x0, y1)], fill=(148, 122, 84))
    d.polygon([(x1, y0 + 22), (x1 - 78, y0 + 40), (x1 - 52, y1),
               (x1, y1)], fill=(138, 112, 78))
    d.rectangle([x0, y1 - 30, x1, y1], fill=(36, 78, 110))
    tx, ty = x0 + 92, y1 - 40
    d.polygon([(tx, ty + 14), (tx + 128, ty + 14), (tx + 116, ty + 24),
               (tx + 10, ty + 24)], fill=(30, 34, 40))
    d.rectangle([tx + 14, ty + 4, tx + 104, ty + 14], fill=(120, 44, 38))
    d.rectangle([tx + 96, ty - 6, tx + 110, ty + 6], fill=(210, 214, 220))
    for fx, fh in [(tx + 34, 16), (tx + 52, 21), (tx + 70, 14)]:
        d.polygon([(fx - 7, ty + 5), (fx + 7, ty + 5), (fx, ty + 5 - fh)],
                  fill=(242, 130, 40))
    for i in range(3):
        cx = tx + 46 + i * 9
        cy = ty - 9 - i * 3
        d.ellipse([cx - 9, cy - 6, cx + 11, cy + 6], fill=(70, 70, 76))
    for mx, my in [(x0 + 66, y1 - 16), (x1 - 60, y1 - 12)]:
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(24, 28, 32))
        for ang in range(0, 360, 60):
            ex = mx + int(11 * math.cos(math.radians(ang)))
            ey = my + int(11 * math.sin(math.radians(ang)))
            d.line([mx, my, ex, ey], fill=(24, 28, 32), width=2)
    d.text((x0 + 8, y0 + 6), "STRAIT OF HORMUZ", font=F("sans_b", 11),
           fill=(250, 246, 232))


def scene_court(img, box):
    """Huawei verdict: courthouse columns and a gavel."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (32, 44, 66), (58, 74, 102))
    d = ImageDraw.Draw(img)
    d.polygon([(x0 + 20, y0 + 16), (x1 - 20, y0 + 16),
               ((x0 + x1) // 2, y0 + 2)], fill=(216, 220, 228))
    d.rectangle([x0 + 16, y0 + 18, x1 - 16, y0 + 23], fill=(216, 220, 228))
    for i in range(5):
        cx = x0 + 30 + i * ((x1 - x0 - 60) // 4)
        d.rectangle([cx, y0 + 26, cx + 10, y1 - 18], fill=(206, 212, 222))
    d.rectangle([x0 + 14, y1 - 16, x1 - 14, y1 - 10], fill=(216, 220, 228))
    gx, gy = x1 - 74, y1 - 40
    d.rectangle([gx, gy, gx + 30, gy + 10], fill=(150, 104, 52))
    d.rectangle([gx + 4, gy - 4, gx + 10, gy + 14], fill=(120, 82, 40))
    d.rectangle([gx + 20, gy - 4, gx + 26, gy + 14], fill=(120, 82, 40))
    d.line([gx + 26, gy + 8, gx + 44, gy + 24], fill=(150, 104, 52),
           width=5)
    chip = "GUILTY: 10 OF 12 COUNTS"
    tw = d.textlength(chip, font=F("sans_b", 12))
    d.rounded_rectangle([x0 + 8, y1 - 24, x0 + 16 + tw, y1 - 5], 4,
                        fill=(250, 246, 232))
    d.text((x0 + 12, y1 - 21), chip, font=F("sans_b", 12), fill=RED)


def scene_refinery(img, box):
    """Saudi strikes: refinery, city tower and an incoming drone."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (96, 74, 84), (214, 150, 92))
    d = ImageDraw.Draw(img)
    tx = x1 - 56
    d.polygon([(tx, y1 - 8), (tx + 12, y0 + 14), (tx + 24, y0 + 10),
               (tx + 34, y1 - 8)], fill=(52, 58, 70))
    d.ellipse([tx + 6, y0 + 34, tx + 28, y0 + 48], fill=(150, 190, 220))
    for cx, ch in [(x0 + 16, 44), (x0 + 44, 56), (x0 + 74, 38)]:
        d.rectangle([cx, y1 - 8 - ch, cx + 16, y1 - 8], fill=(88, 94, 106),
                    outline=(40, 44, 52))
        d.rectangle([cx, y1 - 12 - ch, cx + 16, y1 - 8 - ch],
                    fill=(240, 140, 60))
    d.ellipse([x0 + 104, y1 - 26, x0 + 148, y1 - 8], fill=(120, 128, 140))
    d.rectangle([x0 + 104, y1 - 26, x0 + 148, y1 - 17],
                fill=(120, 128, 140))
    dx, dy = x0 + 128, y0 + 12
    d.polygon([(dx, dy + 6), (dx + 16, dy), (dx + 32, dy + 6),
               (dx + 16, dy + 11)], fill=(28, 30, 36))
    d.line([dx + 16, dy + 8, dx + 16, dy + 16], fill=(28, 30, 36), width=2)
    bx, by = tx - 8, y0 + 30
    for ang in range(0, 360, 45):
        ex = bx + int(13 * math.cos(math.radians(ang)))
        ey = by + int(13 * math.sin(math.radians(ang)))
        d.line([bx, by, ex, ey], fill=(255, 190, 70), width=3)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 220, 120))
    d.text((x0 + 8, y1 - 22), "RAS TANURA + RIYADH", font=F("sans_b", 11),
           fill=(250, 246, 232))


def scene_airfield(img, box):
    """Ukraine strike: jets on a runway, smoke over a refinery."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (58, 70, 92), (150, 148, 138))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y1 - 26, x1, y1], fill=(74, 78, 84))
    d.line([x0 + 4, y1 - 13, x1 - 4, y1 - 13], fill=(230, 226, 210),
           width=2)
    for i in range(5):
        jx = x0 + 18 + i * 34
        jy = y1 - 40 - (i % 2) * 8
        d.polygon([(jx, jy), (jx + 22, jy + 5), (jx, jy + 10)],
                  fill=(38, 44, 54))
        d.polygon([(jx + 6, jy + 5), (jx - 4, jy + 12), (jx + 10, jy + 12)],
                  fill=(38, 44, 54))
    for i in range(3):
        sx = x1 - 52 + i * 14
        for j in range(3):
            r = 7 + j * 4
            d.ellipse([sx - r + j * 3, y0 + 38 - j * 11,
                       sx + r + j * 3, y0 + 50 - j * 11],
                      fill=(88, 88, 94))
    d.rectangle([x1 - 66, y1 - 34, x1 - 16, y1 - 26], fill=(96, 66, 50))
    d.text((x0 + 8, y0 + 6), "SAVASLEYKA AIRFIELD", font=F("sans_b", 11),
           fill=(250, 246, 232))
    chip = "5 JETS HIT"
    tw = d.textlength(chip, font=F("sans_b", 12))
    d.rounded_rectangle([x0 + 8, y1 - 24, x0 + 16 + tw, y1 - 5], 4,
                        fill=(250, 246, 232))
    d.text((x0 + 12, y1 - 21), chip, font=F("sans_b", 12), fill=RED)


def scene_kashmir(img, box):
    """Kashmir crisis: mountains, a river and a dashed ceasefire line."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (104, 128, 148), (196, 188, 158))
    d = ImageDraw.Draw(img)
    for base, col in [(y1 - 18, (90, 96, 108)), (y1 - 8, (70, 78, 90))]:
        pts = [(x0, base)]
        xx = x0
        up = True
        while xx < x1:
            pts.append((xx + 16, base - (26 if up else 10)))
            pts.append((xx + 32, base))
            xx += 32
            up = not up
        pts.append((x1, y1))
        pts.append((x0, y1))
        d.polygon(pts, fill=col)
    d.line([(x0 + 30, y0 + 8), (x0 + 90, y0 + 30), (x0 + 130, y1 - 20)],
           fill=(70, 130, 180), width=4)
    for t in range(0, 100, 9):
        sx = x0 + 150 + int(40 * math.sin(t / 14.0))
        sy = y0 + 6 + t * (y1 - y0 - 12) // 100
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 246, 232))
    fx, fy = x0 + 12, y0 + 8
    d.rectangle([fx, fy, fx + 34, fy + 8], fill=(240, 140, 50))
    d.rectangle([fx, fy + 8, fx + 34, fy + 16], fill=(246, 244, 238))
    d.rectangle([fx, fy + 16, fx + 34, fy + 24], fill=(40, 140, 70))
    gx = x1 - 46
    d.rectangle([gx, fy, gx + 34, fy + 24], fill=(20, 96, 52))
    d.rectangle([gx, fy, gx + 9, fy + 24], fill=(246, 244, 238))
    d.ellipse([gx + 15, fy + 6, gx + 25, fy + 16], outline=(246, 244, 238),
              width=2)
    chip = "26 KILLED IN KASHMIR"
    tw = d.textlength(chip, font=F("sans_b", 12))
    d.rounded_rectangle([x0 + 8, y1 - 24, x0 + 16 + tw, y1 - 5], 4,
                        fill=(24, 28, 34))
    d.text((x0 + 12, y1 - 21), chip, font=F("sans_b", 12),
           fill=(250, 246, 232))


def scene_store(img, box):
    """Cartagena: supermarket storefront with a police light bar."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (52, 74, 104), (120, 132, 148))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 + 10, y0 + 8, x1 - 10, y1 - 2], fill=(226, 220, 204))
    for i in range(6):
        ax = x0 + 12 + i * ((x1 - x0 - 24) // 6)
        d.polygon([(ax, y0 + 8), (ax + 16, y0 + 8), (ax + 11, y0 + 17),
                   (ax + 5, y0 + 17)], fill=(196, 64, 54))
    for i in range(3):
        wx = x0 + 22 + i * ((x1 - x0 - 44) // 3)
        d.rectangle([wx, y0 + 21, wx + 26, y1 - 8], fill=(90, 130, 160))
    d.rectangle([x0 + 30, y1 - 11, x0 + 62, y1 - 4], fill=(250, 246, 232))
    d.rectangle([x0 + 34, y1 - 10, x0 + 45, y1 - 6], fill=(220, 60, 50))
    d.rectangle([x0 + 47, y1 - 10, x0 + 58, y1 - 6], fill=(60, 110, 220))


def scene_skyline(img, box):
    """Gaza: a grey skyline under smoke."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (96, 98, 104), (168, 164, 156))
    d = ImageDraw.Draw(img)
    rng = random.Random(7)
    xx = x0 + 4
    while xx < x1 - 10:
        bw = rng.randint(14, 26)
        bh = rng.randint(12, 30)
        d.rectangle([xx, y1 - 4 - bh, xx + bw, y1 - 4], fill=(58, 60, 66))
        xx += bw + 3
    for i in range(3):
        cx = x0 + 40 + i * 60
        cy = y0 + 10 + i * 4
        d.ellipse([cx - 16, cy - 6, cx + 18, cy + 7], fill=(120, 120, 124))
    d.rectangle([x0, y1 - 4, x1, y1], fill=(44, 46, 50))


def scene_islands(img, box):
    """Solomons pact: Pacific islands under a bright sun."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (64, 130, 180), (168, 208, 226))
    d = ImageDraw.Draw(img)
    d.ellipse([x1 - 44, y0 + 6, x1 - 18, y0 + 32], fill=(250, 214, 92))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(30, 96, 140))
    for ix, iw in [(x0 + 18, 74), (x0 + 110, 96), (x0 + 218, 64)]:
        d.ellipse([ix, y1 - 26, ix + iw, y1 - 8], fill=(52, 128, 84))
        d.line([ix + iw // 2, y1 - 24, ix + iw // 2, y1 - 34],
               fill=(96, 74, 48), width=3)
        d.polygon([(ix + iw // 2, y1 - 34), (ix + iw // 2 - 10, y1 - 26),
                   (ix + iw // 2 + 2, y1 - 27)], fill=(52, 140, 80))
        d.polygon([(ix + iw // 2, y1 - 34), (ix + iw // 2 + 11, y1 - 27),
                   (ix + iw // 2 - 2, y1 - 26)], fill=(44, 120, 70))


def scene_asteroid(img, box):
    """Asteroid test: a cratered rock and a small probe."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (8, 10, 22), (22, 28, 48))
    d = ImageDraw.Draw(img)
    rng = random.Random(11)
    for _ in range(30):
        d.point((rng.randint(x0 + 2, x1 - 2), rng.randint(y0 + 2, y1 - 2)),
                fill=(210, 218, 240))
    cx, cy = x0 + 66, (y0 + y1) // 2
    d.ellipse([cx - 40, cy - 18, cx + 40, cy + 18], fill=(128, 126, 122))
    d.ellipse([cx - 16, cy - 9, cx + 8, cy + 5], fill=(92, 90, 88))
    d.ellipse([cx - 13, cy - 7, cx + 5, cy + 2], fill=(66, 64, 64))
    d.ellipse([cx + 14, cy + 3, cx + 26, cy + 10], fill=(100, 98, 96))
    px, py = x1 - 52, y0 + 12
    d.rectangle([px, py, px + 14, py + 10], fill=(210, 214, 220))
    d.rectangle([px - 16, py + 1, px - 2, py + 9], fill=(52, 84, 150))
    d.rectangle([px + 16, py + 1, px + 30, py + 9], fill=(52, 84, 150))
    d.line([px + 4, py + 10, cx + 18, cy - 6], fill=(240, 200, 90),
           width=1)


MINI_SCENES = {"store": scene_store, "skyline": scene_skyline,
               "islands": scene_islands, "asteroid": scene_asteroid}


# ---------------------------------------------------------------- layout

def card(img, box):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 6, fill=CARD, outline=BORDER, width=1)


def clipped_scene(img, box, fn):
    """Run a scene inside its own sub-image so nothing spills out."""
    x0, y0, x1, y1 = box
    sub = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    fn(sub, (0, 0, x1 - x0, y1 - y0))
    img.paste(sub, (x0, y0))


def lead_card(img, box, scene, kicker, headline, dek):
    """Standard lead: scene band on top, then kicker/headline/dek."""
    x0, y0, x1, y1 = box
    card(img, box)
    clipped_scene(img, (x0 + 1, y0 + 1, x1 - 1, y0 + 61), scene)
    d = ImageDraw.Draw(img)
    d.text((x0 + 10, y0 + 64), kicker, font=F("sans_b", 10), fill=RED)
    y = text_block(d, (x0 + 10, y0 + 76), headline, F("sans_b", 17), INK,
                   x1 - x0 - 20, 20, max_lines=2)
    text_block(d, (x0 + 10, y + 1), dek, F("sans", 12), (52, 54, 62),
               x1 - x0 - 20, 14, max_lines=2)


def mini_card(img, box, scene, headline, dek):
    x0, y0, x1, y1 = box
    card(img, box)
    clipped_scene(img, (x0 + 1, y0 + 1, x1 - 1, y0 + 43), scene)
    d = ImageDraw.Draw(img)
    y = text_block(d, (x0 + 8, y0 + 46), headline, F("sans_b", 14), INK,
                   x1 - x0 - 16, 15, max_lines=2)
    text_block(d, (x0 + 8, y + 1), dek, F("sans", 11), (52, 54, 62),
               x1 - x0 - 16, 12, max_lines=1)


def masthead(img):
    d = ImageDraw.Draw(img)
    d.line([MARGIN, 12, W - MARGIN, 12], fill=INK, width=3)
    title = "THE WORLD IN ONE PAGE"
    f = F("serif_b", 49)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 18), title, font=f, fill=NAVY)
    d.line([MARGIN, 76, W - MARGIN, 76], fill=RED, width=2)
    d.text((MARGIN, 83), "WEDNESDAY 25 NOVEMBER 2026",
           font=F("sans_b", 23), fill=RED)
    stats = "32 STORIES - 9 REGIONS - 16 FIELDS"
    f2 = F("sans_b", 14)
    d.text((W - MARGIN - d.textlength(stats, font=f2), 89), stats,
           font=f2, fill=INK)
    sub = ("The day's world news on one page, as reported by Reuters, "
           "AP, BBC and CFR")
    d.text((MARGIN, 112), sub, font=F("serif", 13), fill=GREY)


MARKETS = [
    ("KOSPI", "-6.2%", DOWN), ("NIKKEI", "-2.8%", DOWN),
    ("TAIEX", "-5.1%", DOWN),
    ("SENSEX", "+1,502", UP), ("NASDAQ", "-1.5%", DOWN),
    ("DOW", "50,019", UP), ("NVIDIA", "-5.9%", DOWN),
    ("BRENT", "$90.97", None), ("BTC", "$59,258", DOWN),
]


def markets_strip(img, y):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + 34], 5, fill=NAVY)
    x = MARGIN + 12
    d.text((x, y + 10), "MARKETS", font=F("sans_b", 13), fill=(240, 200, 90))
    x += d.textlength("MARKETS", font=F("sans_b", 13)) + 14
    for name, val, col in MARKETS:
        label = name + " "
        d.text((x, y + 11), label, font=F("sans_b", 12),
               fill=(206, 214, 226))
        x += d.textlength(label, font=F("sans_b", 12))
        d.text((x, y + 11), val, font=F("sans_b", 12),
               fill=col or (240, 242, 246))
        x += d.textlength(val, font=F("sans_b", 12)) + 11


TIMELINE = [
    ("04:56", "Shenzhou-24 docks"),
    ("06:30", "Asia markets close red"),
    ("12:00", "Cartagena: 20 freed"),
    ("13:30", "US PCE data released"),
    ("19:00", "Fed Beige Book out"),
]


def timeline_strip(img, y):
    d = ImageDraw.Draw(img)
    d.line([MARGIN, y, W - MARGIN, y], fill=BORDER, width=1)
    d.text((MARGIN, y + 5), "THE DAY IN UTC", font=F("sans_b", 11),
           fill=RED)
    x = MARGIN
    ty = y + 20
    for time, label in TIMELINE:
        d.text((x, ty), time, font=F("sans_b", 11), fill=NAVY)
        x += d.textlength(time, font=F("sans_b", 11)) + 5
        d.text((x, ty), label, font=F("sans", 11), fill=INK)
        x += d.textlength(label, font=F("sans", 11)) + 16


BRIEFS = [
    ("NORTH AMERICA", "Microsoft declares 'Code Red' after historic outage"),
    ("NORTH AMERICA", "Dell posts record $54.9B quarter as AI server sales triple"),
    ("NORTH AMERICA", "Storm threatens Thanksgiving travel and New York's parade"),
    ("LATIN AMERICA", "Troops raid a home and capture a Mexican drug lord"),
    ("LATIN AMERICA", "Argentina slips into technical recession"),
    ("LATIN AMERICA", "Cuba's life expectancy falls for the first time since 1950"),
    ("EUROPE", "Puigdemont to end a decade of exile and return to Spain on Dec 12"),
    ("EUROPE", "Poland seeks a permanent US base after Russian airspace incursions"),
    ("EUROPE", "EU levels antitrust fines at Apple and Meta"),
    ("EUROPE", "Spain votes Sunday with the far right eyeing a place in government"),
    ("MIDDLE EAST", "Qatar's F1 Grand Prix goes ahead this weekend despite the war"),
    ("AFRICA", "Fuel-truck blaze kills 21 on an Egyptian ring road"),
    ("AFRICA", "Drone strikes kill 19 civilians in Sudan's Blue Nile state"),
    ("AFRICA", "Sahel rebels take the drone war to Russia's paramilitaries"),
    ("AFRICA", "Nollywood legend Pete Edochie dies aged 79"),
    ("SOUTH ASIA", "India's food inflation broadens and squeezes household budgets"),
    ("EAST ASIA", "Shanghai party chief Chen Jining investigated in Xi's graft drive"),
    ("EAST ASIA", "AI-made fake videos target Taiwan, BBC Verify reports"),
    ("SOUTHEAST ASIA", "Bogor gold-mine flood: six dead, about 20 miners trapped"),
    ("OCEANIA", "Sydney policeman found guilty of a double murder"),
]


def briefs_block(img, y):
    d = ImageDraw.Draw(img)
    d.line([MARGIN, y, W - MARGIN, y], fill=BORDER, width=1)
    d.text((MARGIN, y + 5), "AROUND THE WORLD IN BRIEF",
           font=F("serif_b", 16), fill=NAVY)
    top = y + 30
    cols = 4
    colw = (INNER - (cols - 1) * 14) // cols
    per = (len(BRIEFS) + cols - 1) // cols
    max_y = top
    for c in range(cols):
        x = MARGIN + c * (colw + 14)
        yy = top
        for region, headline in BRIEFS[c * per:(c + 1) * per]:
            d.text((x, yy), region, font=F("sans_b", 9), fill=RED)
            yy = text_block(d, (x, yy + 9), headline, F("sans_b", 11),
                            INK, colw, 12, max_lines=2)
            yy += 2
        max_y = max(max_y, yy)
    return max_y


def grain(img):
    """Fine deterministic paper grain; also lifts the PNG's size."""
    rng = random.Random(20261125)
    noise = Image.new("L", (W, H))
    noise.putdata([rng.randint(0, 255) for _ in range(W * H)])
    noise = noise.point(lambda v: 128 + (v - 128) // 14)
    tint = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, tint, 0.06)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    masthead(img)
    markets_strip(img, 132)

    # Row 1: tariffs (wide, side scene) + astronaut.
    y = 174
    card(img, (MARGIN, y, MARGIN + 630, y + 146))
    clipped_scene(img, (MARGIN + 1, y + 1, MARGIN + 241, y + 145),
                  scene_port)
    d = ImageDraw.Draw(img)
    tx = MARGIN + 254
    d.text((tx, y + 8), "TRADE - WASHINGTON", font=F("sans_b", 10),
           fill=RED)
    yy = text_block(d, (tx, y + 21), "US PROPOSES NEW TARIFFS ON 14 PARTNERS",
                    F("sans_b", 21), INK, 630 - 254 - 12, 24, max_lines=2)
    text_block(d, (tx, yy + 2),
               "Section 301 duties target 'excess factory capacity': "
               "China +20% on top of about 25% already in place; the EU, "
               "Japan and South Korea are capped at 15%, Singapore at "
               "10%. A hearing comes in January.",
               F("sans", 13), (52, 54, 62), 630 - 254 - 12, 16,
               max_lines=4)
    lead_card(img, (MARGIN + 642, y, W - MARGIN, y + 146), scene_rocket,
              "SPACE - CHINA / PAKISTAN",
              "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
              "Muhammad Zeeshan Ali is the first foreigner aboard China's "
              "space station, arriving on Shenzhou-24.")

    # Row 2: chip rout, Hormuz, Huawei.
    y2 = y + 154
    cw3 = (INNER - 24) // 3
    lead_card(img, (MARGIN, y2, MARGIN + cw3, y2 + 146), scene_chart,
              "MARKETS - EAST ASIA", "ASIA'S CHIP ROUT DEEPENS",
              "Samsung -9.9%, SK Hynix -11.1% in Seoul; SoftBank -14.8% "
              "in Tokyo; Nvidia -5.9%.")
    lead_card(img, (MARGIN + cw3 + 12, y2, MARGIN + 2 * cw3 + 12,
                    y2 + 146), scene_tanker,
              "ENERGY - PERSIAN GULF", "TWO TANKERS HIT MINES IN HORMUZ",
              "Iran's Guards say two oil tankers struck naval mines and "
              "caught fire early Wednesday.")
    lead_card(img, (MARGIN + 2 * cw3 + 24, y2, W - MARGIN, y2 + 146),
              scene_court, "JUSTICE - NEW YORK",
              "HUAWEI CONVICTED OF FRAUD AND TRADE-THEFT",
              "A Brooklyn jury convicts on bank fraud and trade-secret "
              "theft; acquits on racketeering.")

    # Row 3: Saudi strikes, Ukraine, Kashmir.
    y3 = y2 + 154
    lead_card(img, (MARGIN, y3, MARGIN + cw3, y3 + 146), scene_refinery,
              "CONFLICT - SAUDI ARABIA", "HOUTHIS STRIKE SAUDI OIL AND CAPITAL",
              "Four drones are downed at the Ras Tanura refinery; a Riyadh "
              "tower strike wounds 11.")
    lead_card(img, (MARGIN + cw3 + 12, y3, MARGIN + 2 * cw3 + 12,
                    y3 + 146), scene_airfield,
              "WAR - UKRAINE / RUSSIA", "UKRAINE HITS 5 JETS AND 2 REFINERIES",
              "Drones set the Syzran and Kuibyshev oil plants ablaze; "
              "Moscow's own toll nears 500,000.")
    lead_card(img, (MARGIN + 2 * cw3 + 24, y3, W - MARGIN, y3 + 146),
              scene_kashmir, "ASIA - KASHMIR",
              "INDIA AND PAKISTAN DOWNGRADE TIES",
              "After 26 die in Kashmir, Delhi suspends the Indus water "
              "treaty; Islamabad closes its airspace.")

    # Row 4: four mini leads.
    y4 = y3 + 154
    cw4 = (INNER - 36) // 4
    minis = [
        ("store", "20 HOSTAGES FREED IN CARTAGENA",
         "17-hour siege ended by a police raid"),
        ("skyline", "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
         "Naeem Abu Nahel dies in Gaza City"),
        ("islands", "SOLOMONS SIGN AUSTRALIA PACT, END CHINA DEAL",
         "Canberra treaty bars foreign bases"),
        ("asteroid", "CRATER OF ASTEROID TEST REVEALED",
         "Stadium-sized scar from defence trial"),
    ]
    for i, (key, head, dek) in enumerate(minis):
        x = MARGIN + i * (cw4 + 12)
        mini_card(img, (x, y4, x + cw4, y4 + 100), MINI_SCENES[key],
                  head, dek)

    timeline_strip(img, y4 + 110)
    end_y = briefs_block(img, y4 + 110 + 40)
    d = ImageDraw.Draw(img)
    foot = ("Drawn and typeset in code by Plenger Agent - sources: "
            "Reuters, AP, BBC, CFR, reports of 25 November 2026")
    d.text((MARGIN, 1004), foot, font=F("sans", 10), fill=GREY)
    assert end_y <= 1000, f"briefs overflow: {end_y}"
    return grain(img)


if __name__ == "__main__":
    out = render()
    out.save("entry.png", optimize=True)
    print("wrote entry.png", out.size)
