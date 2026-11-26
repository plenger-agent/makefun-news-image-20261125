#!/usr/bin/env python3
"""Renderer for the make.fun news-image-20261125 entry, v3.

Draws a dense one-page broadsheet, "THE WORLD IN ONE PAGE", summing up
the world news of Wednesday 25 November 2026 in a single 1024x1024
image: a masthead naming the day, a stat strip of the day's biggest
numbers, three illustrated hero stories, a numbered dot map of the
thirteen illustrated stories, ten more illustrated mid-page cards, a
date-check box, a how-sure legend, and 37 one-line briefs -- 50
stories in all, across 10 regions and 21 fields.

Every story was checked against the day's reporting (Reuters, AP,
BBC and official statements) before it was drawn; no story or figure
is invented. Rendering uses Pillow locally; the hand-in program
(main.py) is standard-library only and simply copies the committed
entry.png, so the grader never needs Pillow.

Deterministic: no randomness anywhere, so re-running this script
reproduces entry.png byte for byte.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 16
INNER = W - 2 * MARGIN

PAPER = (247, 242, 230)
CARD = (255, 253, 246)
INK = (26, 28, 36)
NAVY = (18, 36, 60)
RED = (163, 31, 38)
GOLD = (172, 128, 30)
GREEN = (28, 116, 58)
GREY = (92, 94, 100)
BORDER = (203, 192, 164)
LAND = (188, 160, 104)
SEA = (233, 238, 240)

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
    """Greedy word wrap; returns the lines that fit maxw."""
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
    if max_lines:
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
    img.paste(strip.resize((int(x1 - x0), h)), (int(x0), int(y0)))


def chip(draw, xy, label, colour):
    """Small how-sure pill: OFFICIAL / REPORTED / CLAIM."""
    x, y = xy
    f = F("sans_b", 8)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], 6, fill=colour)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------------ scenes
# Each scene draws inside box (x0, y0, x1, y1) on the base image and
# illustrates one numbered story. Simple flat shapes, no photographs.

def scene_port(img, box):
    """1: tariff lead -- container port at dusk with rate tags."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (36, 60, 96), (216, 134, 74))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y1 - 22, x1, y1], fill=(28, 62, 90))
    for i, cx in enumerate(range(x0 + 14, x1 - 30, 52)):
        for j, col in enumerate([(196, 74, 60), (44, 110, 150),
                                 (224, 158, 60), (70, 140, 96)]):
            if (i + j) % 3:
                d.rectangle([cx, y1 - 40 - j * 13, cx + 44, y1 - 29 - j * 13],
                            fill=col, outline=(20, 24, 30))
    for gx in (x0 + 60, x0 + 168, x0 + 262):
        d.line([gx, y0 + 8, gx, y1 - 38], fill=(24, 28, 34), width=3)
        d.line([gx, y0 + 8, gx + 44, y0 + 8], fill=(24, 28, 34), width=3)
        d.line([gx + 40, y0 + 8, gx + 40, y0 + 26], fill=(24, 28, 34),
               width=2)
    d.rectangle([x0, y1 - 16, x1, y1], fill=NAVY)
    tape = "CHINA +20% · EU 15% · INDIA 25% · VIETNAM 35%"
    d.text((x0 + (x1 - x0 - d.textlength(tape, font=F("sans_b", 9.5))) / 2,
            y1 - 13), tape, font=F("sans_b", 9.5), fill=(250, 246, 232))


def scene_tanker(img, box):
    """2: Cairo -- fuel tanker ablaze on a ring road."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (52, 44, 52), (196, 96, 52))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y1 - 18, x1, y1], fill=(40, 36, 38))
    for i in range(6):
        d.line([x0 + 10 + i * 8, y1 - 9, x0 + 26 + i * 8, y1 - 9],
               fill=(226, 200, 120), width=2)
    tx, ty = x0 + 88, y1 - 46
    d.rounded_rectangle([tx, ty, tx + 128, ty + 26], 12, fill=(206, 210, 214),
                        outline=(30, 30, 34), width=2)
    d.rectangle([tx + 128, ty + 6, tx + 148, ty + 26], fill=(70, 76, 84),
                outline=(30, 30, 34))
    for wx in (tx + 22, tx + 108):
        d.ellipse([wx, ty + 22, wx + 16, ty + 38], fill=(22, 22, 26))
    for fx, fh, col in ((tx + 30, 30, (238, 118, 40)),
                        (tx + 62, 40, (244, 160, 44)),
                        (tx + 92, 28, (226, 84, 34))):
        d.polygon([(fx, ty + 2), (fx + 12, ty - fh), (fx + 24, ty + 2)],
                  fill=col)
        d.polygon([(fx + 5, ty + 2), (fx + 12, ty - fh + 10),
                   (fx + 19, ty + 2)], fill=(250, 206, 92))
    for sx in range(tx + 8, tx + 130, 22):
        d.line([sx, ty - 34, sx + 6, ty - 12], fill=(90, 84, 88), width=3)


def scene_chips(img, box):
    """3: chip rout -- falling market chart over a circuit board."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (16, 30, 54), (24, 62, 66))
    d = ImageDraw.Draw(img)
    for gx in range(x0 + 12, x1, 26):
        d.line([gx, y0 + 6, gx, y1 - 8], fill=(30, 66, 74), width=1)
    for gy in range(y0 + 10, y1, 18):
        d.line([x0 + 6, gy, x1 - 6, gy], fill=(30, 66, 74), width=1)
    pts = [(x0 + 14, y0 + 22), (x0 + 74, y0 + 30), (x0 + 128, y0 + 52),
           (x0 + 184, y0 + 48), (x0 + 238, y0 + 74), (x0 + 292, y1 - 16)]
    d.line(pts, fill=(255, 110, 92), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 176, 150))
    d.polygon([(x0 + 292, y1 - 16), (x0 + 278, y1 - 18), (x0 + 290, y1 - 30)],
              fill=(255, 110, 92))
    d.rounded_rectangle([x0 + 196, y1 - 44, x0 + 252, y1 - 12], 4,
                        fill=(30, 84, 70), outline=(126, 208, 138), width=2)
    for px in range(x0 + 204, x0 + 246, 10):
        d.line([px, y1 - 44, px, y1 - 50], fill=(126, 208, 138), width=2)
        d.line([px, y1 - 12, px, y1 - 6], fill=(126, 208, 138), width=2)
    d.text((x0 + 206, y1 - 36), "CHIP", font=F("sans_b", 13),
           fill=(190, 240, 200))
    d.text((x0 + 16, y0 + 8), "-6.2%", font=F("serif_b", 24),
           fill=(255, 140, 120))


def scene_station(img, box):
    """4: Tiangong -- station, docked capsule and an orbit arc."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (10, 16, 40), (30, 52, 92))
    d = ImageDraw.Draw(img)
    for sx, sy in ((20, 12), (60, 30), (120, 10), (150, 34), (36, 44),
                   (96, 40), (140, 18)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                  fill=(240, 244, 250))
    cy = (y0 + y1) // 2
    d.arc([x0 - 30, cy - 66, x1 + 30, cy + 66], 200, 330,
          fill=(120, 160, 210), width=2)
    d.rectangle([x0 + 58, cy - 9, x0 + 118, cy + 9], fill=(214, 218, 224),
                outline=(24, 26, 32), width=2)
    for px in (x0 + 16, x0 + 120):
        d.rectangle([px, cy - 15, px + 34, cy + 15], fill=(52, 96, 168),
                    outline=(150, 190, 240))
        for k in range(1, 3):
            d.line([px + k * 11, cy - 15, px + k * 11, cy + 15],
                   fill=(150, 190, 240))
    d.polygon([(x0 + 118, cy - 7), (x0 + 140, cy), (x0 + 118, cy + 7)],
              fill=(226, 178, 84))
    d.ellipse([x0 + 138, cy - 6, x0 + 152, cy + 6], fill=(236, 240, 244),
              outline=(24, 26, 32))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(24, 44, 74))
    d.text((x0 + 8, y1 - 13), "SHENZHOU-24 · TIANGONG",
           font=F("sans_b", 9), fill=(170, 205, 240))


def scene_meter(img, box):
    """5: UK energy cap -- house, meter and a rising dial."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (96, 118, 140), (214, 206, 178))
    d = ImageDraw.Draw(img)
    hx, hy = x0 + 16, y1 - 44
    d.polygon([(hx, hy), (hx + 26, hy - 20), (hx + 52, hy)], fill=(120, 52, 44))
    d.rectangle([hx + 6, hy, hx + 46, y1 - 14], fill=(238, 230, 210),
                outline=(40, 40, 44))
    d.rectangle([hx + 21, y1 - 30, hx + 31, y1 - 14], fill=(70, 60, 50))
    mx, my = x1 - 56, y0 + 4
    d.rounded_rectangle([mx, my, mx + 44, my + 32], 5, fill=(250, 248, 240),
                        outline=(40, 40, 44), width=2)
    d.arc([mx + 8, my + 6, mx + 36, my + 34], 180, 360, fill=RED, width=3)
    d.line([mx + 22, my + 20, mx + 32, my + 10], fill=RED, width=3)
    d.text((x0 + 76, y0 + 4), "£2,166", font=F("serif_b", 15), fill=NAVY)
    d.text((x0 + 76, y0 + 23), "+26%", font=F("sans_b", 10), fill=RED)


def scene_smoke(img, box):
    """6: Gaza -- skyline under a smoke plume."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (150, 140, 128), (216, 200, 170))
    d = ImageDraw.Draw(img)
    for bx, bh in ((6, 26), (34, 38), (66, 22), (92, 44), (126, 30),
                   (150, 40)):
        d.rectangle([x0 + bx, y1 - 12 - bh, x0 + bx + 24, y1 - 12],
                    fill=(88, 80, 74), outline=(52, 48, 44))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(70, 62, 56))
    for cx, cr in ((96, 16), (112, 22), (130, 15), (86, 11)):
        d.ellipse([x0 + cx - cr, y0 + 4, x0 + cx + cr, y0 + 4 + cr],
                  fill=(104, 98, 94))
    d.polygon([(x0 + 100, y1 - 52), (x0 + 110, y0 + 16), (x0 + 122, y1 - 52)],
              fill=(122, 114, 108))


def scene_blackout(img, box):
    """7: Ukraine -- dark city, dead power lines, one lit window."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (14, 20, 38), (30, 38, 58))
    d = ImageDraw.Draw(img)
    for bx, bh in ((4, 22), (30, 34), (58, 26), (88, 40), (122, 28),
                   (146, 36)):
        d.rectangle([x0 + bx, y1 - 10 - bh, x0 + bx + 22, y1 - 10],
                    fill=(10, 14, 24), outline=(52, 62, 84))
    d.rectangle([x0 + 96, y1 - 34, x0 + 102, y1 - 28], fill=(250, 204, 92))
    for px in (x0 + 18, x0 + 84, x0 + 140):
        d.line([px, y0 + 4, px, y1 - 30], fill=(70, 84, 110), width=2)
        d.line([px - 10, y0 + 12, px + 10, y0 + 12], fill=(70, 84, 110),
               width=2)
    d.arc([x0 + 18, y0 + 10, x0 + 84, y0 + 34], 0, 180, fill=(44, 54, 76),
          width=2)
    d.arc([x0 + 84, y0 + 10, x0 + 140, y0 + 32], 0, 180, fill=(44, 54, 76),
          width=2)


def scene_refinery(img, box):
    """8: Ras Tanura -- refinery towers and intercepted drones."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (206, 168, 110), (238, 214, 160))
    d = ImageDraw.Draw(img)
    for tx in (x0 + 22, x0 + 58, x0 + 96):
        d.rectangle([tx, y0 + 22, tx + 14, y1 - 12], fill=(120, 116, 110),
                    outline=(60, 58, 54))
        d.ellipse([tx - 2, y0 + 16, tx + 16, y0 + 26], fill=(140, 136, 130))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(150, 128, 92))
    for dx, dy in ((x0 + 118, y0 + 10), (x0 + 146, y0 + 22)):
        d.line([dx - 8, dy, dx + 8, dy], fill=(40, 40, 44), width=2)
        d.line([dx, dy - 5, dx, dy + 5], fill=(40, 40, 44), width=2)
        d.line([dx - 12, dy + 12, dx + 2, dy + 2], fill=(250, 240, 220),
               width=1)
    d.polygon([(x0 + 128, y0 + 30), (x0 + 134, y0 + 20), (x0 + 140, y0 + 30)],
              fill=(244, 160, 44))


def scene_factory(img, box):
    """9: Dhaka -- garment factory with rows of lit windows."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (140, 158, 168), (206, 200, 178))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 10], fill=(168, 158, 142),
                outline=(60, 56, 50), width=2)
    for r in range(2):
        for c in range(6):
            wx = x0 + 24 + c * 22
            wy = y0 + 19 + r * 12
            d.rectangle([wx, wy, wx + 14, wy + 8], fill=(250, 224, 140),
                        outline=(90, 84, 76))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(96, 92, 84))
    d.text((x0 + 16, y0 + 1), "WAGE 17,500 TAKA", font=F("sans_b", 9),
           fill=NAVY)


def scene_mine(img, box):
    """10: Bogor -- flooded gold pit, rescue lights in the rain."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (70, 92, 96), (120, 138, 128))
    d = ImageDraw.Draw(img)
    d.polygon([(x0, y1 - 26), (x0 + 60, y0 + 12), (x0 + 118, y1 - 26)],
              fill=(86, 74, 58), outline=(50, 44, 36))
    d.polygon([(x0 + 44, y1 - 26), (x0 + 60, y0 + 26), (x0 + 76, y1 - 26)],
              fill=(30, 28, 26))
    d.rectangle([x0, y1 - 26, x1, y1 - 8], fill=(52, 96, 128))
    for i in range(5):
        d.arc([x0 + 12 + i * 30, y1 - 24, x0 + 36 + i * 30, y1 - 14], 0, 180,
              fill=(150, 190, 220), width=2)
    for rx in range(x0 + 8, x1 - 6, 14):
        d.line([rx, y0 + 4, rx - 3, y0 + 16], fill=(170, 200, 224), width=1)
    d.ellipse([x0 + 128, y0 + 10, x0 + 140, y0 + 22], fill=(250, 224, 130))


def scene_rescue(img, box):
    """11: Cartagena -- storefront, shield and a freed doorway."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (120, 150, 170), (216, 200, 160))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 + 12, y0 + 8, x1 - 12, y1 - 4], fill=(226, 216, 192),
                outline=(60, 56, 50), width=2)
    d.rectangle([x0 + 12, y0 + 8, x1 - 12, y0 + 17], fill=(44, 96, 150))
    for c in range(4):
        wx = x0 + 22 + c * 34
        d.rectangle([wx, y0 + 21, wx + 24, y0 + 33], fill=(170, 200, 220),
                    outline=(80, 76, 70))
    d.rectangle([x0 + 74, y0 + 20, x0 + 96, y1 - 4], fill=(96, 66, 44),
                outline=(50, 40, 30))
    d.polygon([(x0 + 128, y0 + 19), (x0 + 144, y0 + 23), (x0 + 144, y0 + 33),
               (x0 + 136, y0 + 38), (x0 + 128, y0 + 33)], fill=(36, 84, 140),
              outline=(240, 240, 240))
    d.text((x0 + 132, y0 + 24), "P", font=F("sans_b", 9),
           fill=(255, 255, 255))


def scene_columns(img, box):
    """12: Jerusalem -- courthouse columns and balanced scales."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (168, 158, 138), (226, 216, 192))
    d = ImageDraw.Draw(img)
    d.polygon([(x0 + 14, y0 + 16), (x0 + 84, y0 + 2), (x1 - 14, y0 + 16)],
              fill=(150, 138, 116), outline=(80, 72, 58))
    for c in range(4):
        cx = x0 + 24 + c * 38
        d.rectangle([cx, y0 + 18, cx + 10, y1 - 16], fill=(238, 232, 214),
                    outline=(96, 88, 72))
    d.rectangle([x0 + 10, y1 - 16, x1 - 10, y1 - 8], fill=(150, 138, 116))
    cx = x0 + 84
    d.line([cx, y0 + 22, cx, y1 - 22], fill=(60, 56, 50), width=3)
    d.line([cx - 22, y0 + 28, cx + 22, y0 + 28], fill=(60, 56, 50), width=3)
    for sx in (cx - 22, cx + 22):
        d.arc([sx - 9, y0 + 28, sx + 9, y0 + 44], 0, 180, fill=(60, 56, 50),
              width=2)


def scene_island(img, box):
    """13: Solomons -- island, palm and two flags on one shore."""
    x0, y0, x1, y1 = box
    vgrad(img, box, (90, 160, 190), (226, 232, 200))
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y1 - 18, x1, y1], fill=(40, 110, 150))
    d.ellipse([x0 + 20, y1 - 34, x1 - 30, y1 - 6], fill=(226, 206, 150))
    px, py = x0 + 60, y1 - 26
    d.arc([px - 4, py - 26, px + 6, py], 200, 340, fill=(70, 110, 60),
          width=3)
    for a in range(5):
        ang = math.radians(200 + a * 32)
        d.line([px + 2, py - 24, px + 2 + int(20 * math.cos(ang)),
                py - 24 + int(12 * math.sin(ang))], fill=(60, 130, 70),
               width=3)
    for fx, col in ((x0 + 108, (36, 84, 150)), (x0 + 134, (196, 52, 56))):
        d.line([fx, y1 - 30, fx, y1 - 8], fill=(50, 46, 42), width=2)
        d.rectangle([fx, y1 - 30, fx + 18, y1 - 20], fill=col)


SCENES = [scene_port, scene_tanker, scene_chips, scene_station,
          scene_meter, scene_smoke, scene_blackout, scene_refinery,
          scene_factory, scene_mine, scene_rescue, scene_columns,
          scene_island]


# -------------------------------------------------------------------- data
# (kicker, headline, dek, why-it-matters, how-sure) for the three heroes.

HEROES = [
    ("TRADE · NORTH AMERICA",
     "US PROPOSES TARIFFS ON 14 ECONOMIES, CHINA +20%",
     "Washington aims at 'excess factory capacity': EU 15%, India 25%, "
     "Vietnam 35%.",
     "New levies on 14 partners reset the price of world trade overnight.",
     "OFFICIAL"),
    ("DISASTER · AFRICA",
     "FUEL TANKER FIRE ON CAIRO RING ROAD KILLS 30+",
     "A tanker carrying petroleum overturned and exploded on the "
     "capital's ring road; over 30 are dead.",
     "Egypt's deadliest road disaster of the year, on its busiest artery.",
     "OFFICIAL"),
    ("MARKETS · EAST ASIA",
     "AI DOUBTS SINK ASIA'S CHIP GIANTS; KOSPI -6.2%",
     "Seoul's Kospi fell 6.2% to 4,697.51; SK Hynix -11.1%, Samsung "
     "-9.9%, Taiex -4.8%, Nikkei -2.8%.",
     "The AI trade's worst Asia day wipes out the month's chip gains.",
     "REPORTED"),
]

# (headline, one-line summary, how-sure) for illustrated stories 4-13.

MIDS = [
    ("SHENZHOU-24 DOCKS AT TIANGONG",
     "Zeeshan Ali, 40, is Pakistan's first astronaut -- and the first "
     "foreigner aboard China's station.", "OFFICIAL"),
    ("UK ENERGY CAP JUMPS 26% TO \u00a32,166",
     "The price cap rises from \u00a31,723 in January, squeezing household "
     "bills across Britain again.", "OFFICIAL"),
    ("GAZA STRIKE KILLS HAMAS SECURITY CHIEF",
     "Israel says the strike killed the group's internal-security head; "
     "the toll is still being counted.", "REPORTED"),
    ("RUSSIAN STRIKES KILL 5 IN UKRAINE",
     "Overnight attacks kill five and cut power across five Ukrainian "
     "regions, officials say.", "REPORTED"),
    ("FOUR DRONES DOWNED OVER RAS TANURA",
     "Saudi defences intercept four drones near the kingdom's biggest "
     "oil terminal on the Gulf.", "REPORTED"),
    ("DHAKA RAISES GARMENT WAGE TO 17,500 TAKA",
     "The minimum wage rises from 12,500 taka; workers protest that it "
     "still falls short.", "OFFICIAL"),
    ("BOGOR GOLD-PIT FLOOD: 9 DEAD, 17 TRAPPED",
     "Rescuers race to reach 17 miners trapped in a flooded West Java "
     "gold pit; nine are dead.", "REPORTED"),
    ("CARTAGENA HOSTAGES FREED IN RESCUE",
     "Colombian police free the supermarket hostages unharmed and hold "
     "the gunmen.", "REPORTED"),
    ("NETANYAHU GRAFT CASE FACES A RETHINK",
     "The long-running corruption case against Israel's prime minister "
     "heads for a rethink.", "REPORTED"),
    ("SOLOMONS-AUSTRALIA PACT BARS BASES",
     "A new security treaty commits the Solomons to hosting no foreign "
     "military bases.", "OFFICIAL"),
]

# (region code, text) for briefs 14-50, in story-number order.

BRIEFS = [
    ("NA", "Dow closes above 50,000 for the first time in its history"),
    ("NA", "US third-quarter GDP revised up to 4.3% annual growth"),
    ("NA", "New York jury finds Huawei guilty of stealing US trade secrets"),
    ("NA", "Microsoft declares 'Code Red' after historic global outage"),
    ("NA", "New York court upholds Mayor Mamdani's rent freeze"),
    ("NA", "US consumer confidence jumps to highest in nearly two years"),
    ("NA", "Trump pardons Thanksgiving turkeys Freedom and Feathers"),
    ("NA", "Dell posts a record quarter on surging AI server demand"),
    ("NA", "Anthropic shares slide below the $83 IPO price"),
    ("NA", "Jensen Huang returns as Nvidia CEO; S&P puts its rating on watch"),
    ("NA", "East Coast storm to bring rain and strong winds on Thanksgiving"),
    ("NA", "Army detonates lead explosives stockpile in Iowa, declares success"),
    ("LATAM", "Salvadoran Kilmar Abrego Garcia leaves the US for Spain"),
    ("EUR", "NATO plans early-warning aircraft deployment in Poland"),
    ("EUR", "Norse Atlantic flags bankruptcy risk as flights are suspended"),
    ("EUR", "Renovation of fire-hit former Nazi guest house stirs German debate"),
    ("RUS", "Ukrainian drones hit refineries at Samara, deep inside Russia"),
    ("ME", "Islamic State attack kills two Syrian security men in Hasakah"),
    ("ME", "Houthi forces close to within 60 km of Yemen's Aden"),
    ("ME", "Iran claims three tankers hit mines in the Strait of Hormuz"),
    ("ME", "Saudi Arabia budgets for a narrower deficit in 2027"),
    ("AFR", "Militants kill at least 30 in villages in Nigeria's Niger state"),
    ("AFR", "RSF fighters kill 19 in Sudan's Blue Nile state"),
    ("AFR", "Saudi national kidnapped by suspected IS militants in Niger"),
    ("AFR", "Nollywood veteran Pete Edochie dies in Nigeria"),
    ("AFR", "Court delivers its ruling in South Africa's Farmgate case"),
    ("SAS", "BJP and Akali Dal reunite for the 2027 Punjab elections"),
    ("SAS", "Truck hits school bus on Agra-Lucknow expressway; students killed"),
    ("SAS", "India tells 'cockroach' movement leader Das not to use passport"),
    ("SAS", "Hasina signals she will return to Bangladesh on 16 December"),
    ("OCE", "Magnitude 5.0 earthquake hits New Ireland region, Papua New Guinea"),
    ("OCE", "Australia's CPI comes in at 4.9% year on year"),
    ("OCE", "One Nation surge tests Labor's 12-year rule in Victoria vote"),
    ("SAS", "Sooryavanshi smashes 200 off 52 balls, a world cricket record"),
    ("OCE", "England beat Australia by eight wickets in the second T20I"),
    ("SAS", "Gukesh and Sindarov contest the World Chess Championship"),
    ("ME", "Qatar's Formula One Grand Prix goes ahead this weekend"),
]

STATS = [
    ("30+ DEAD", "CAIRO TANKER FIRE"),
    ("50,000", "DOW'S FIRST CLOSE ABOVE"),
    ("-6.2%", "KOSPI IN THE CHIP ROUT"),
    ("\u00a32,166", "UK ENERGY CAP, +26%"),
    ("+4.3%", "US Q3 GDP, REVISED UP"),
    ("17,500", "DHAKA WAGE IN TAKA"),
]

# Coarse dot map of the world: (row, first column, last column) land
# segments on a 100 x 17 grid, plus scattered island cells.
MAP_SEGMENTS = [
    (0, 10, 26), (0, 66, 95),
    (1, 8, 30), (1, 45, 52), (1, 58, 97),
    (2, 8, 31), (2, 44, 55), (2, 57, 97),
    (3, 9, 30), (3, 45, 57), (3, 58, 96),
    (4, 10, 29), (4, 46, 54), (4, 58, 95),
    (5, 11, 27), (5, 47, 53), (5, 59, 94),
    (6, 12, 25), (6, 59, 68), (6, 69, 75), (6, 78, 90),
    (7, 13, 24), (7, 46, 67), (7, 68, 74), (7, 77, 84),
    (8, 16, 23), (8, 47, 66), (8, 69, 73), (8, 78, 83),
    (9, 24, 30), (9, 48, 61), (9, 70, 72), (9, 78, 82),
    (10, 24, 33), (10, 49, 60),
    (11, 25, 33), (11, 50, 59),
    (12, 26, 32), (12, 51, 57), (12, 85, 94),
    (13, 27, 31), (13, 52, 56), (13, 86, 95),
    (14, 27, 30), (14, 53, 55), (14, 88, 93),
    (15, 28, 29),
    (16, 28, 28),
]
MAP_ISLANDS = [(10, 76), (10, 79), (10, 82), (11, 75), (11, 78),
               (11, 81), (11, 84), (12, 77), (12, 80), (13, 97)]

# (story number, map column, map row) for the thirteen illustrated pins.
PINS = [
    (1, 24, 4), (2, 57, 7), (3, 85, 4), (4, 80, 5), (5, 46, 2),
    (6, 59, 6), (7, 55, 3), (8, 63, 7), (9, 72, 8), (10, 78, 12),
    (11, 23, 9), (12, 60, 7), (13, 97, 13),
]


# ------------------------------------------------------------------ layout

def masthead(d):
    d.text((MARGIN, 8), "THE WORLD IN ONE PAGE", font=F("serif_b", 41),
           fill=INK)
    d.text((MARGIN, 56), "The whole day, drawn on one sheet -- every story "
           "dated, numbered and checked", font=F("serif", 12.5), fill=GREY)
    right = "WEDNESDAY"
    d.text((W - MARGIN - d.textlength(right, font=F("sans_b", 15)), 10),
           right, font=F("sans_b", 15), fill=RED)
    right = "25 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=F("sans_b", 15)), 30),
           right, font=F("sans_b", 15), fill=INK)
    right = "Day 329 of 2026 · No. 25"
    d.text((W - MARGIN - d.textlength(right, font=F("sans", 11)), 52),
           right, font=F("sans", 11), fill=GREY)
    d.line([MARGIN, 78, W - MARGIN, 78], fill=INK, width=3)
    tag = ("50 STORIES · 10 REGIONS · 21 FIELDS · 13 ILLUSTRATED · "
           "37 IN BRIEF")
    d.text(((W - d.textlength(tag, font=F("sans_b", 11.5))) / 2, 83), tag,
           font=F("sans_b", 11.5), fill=NAVY)
    d.line([MARGIN, 102, W - MARGIN, 102], fill=RED, width=2)


def stat_strip(img, d):
    y0, y1 = 108, 140
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=NAVY)
    cw = INNER // len(STATS)
    for i, (big, small) in enumerate(STATS):
        cx = MARGIN + i * cw
        if i:
            d.line([cx, y0 + 5, cx, y1 - 5], fill=(70, 96, 128), width=1)
        tw = d.textlength(big, font=F("serif_b", 15))
        d.text((cx + (cw - tw) / 2, y0 + 3), big, font=F("serif_b", 15),
               fill=(250, 214, 120))
        tw = d.textlength(small, font=F("sans_b", 7.5))
        d.text((cx + (cw - tw) / 2, y0 + 22), small, font=F("sans_b", 7.5),
               fill=(214, 226, 240))


def hero_card(img, d, x, y, w, h, idx):
    kicker, head, dek, why, sure = HEROES[idx]
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=1)
    SCENES[idx](img, (x + 1, y + 1, x + w - 1, y + 84))
    chip(d, (x + w - 76, y + 8), sure, RED if sure == "REPORTED" else NAVY)
    d.ellipse([x + 8, y + 8, x + 30, y + 30], fill=RED)
    d.text((x + 14, y + 12), str(idx + 1), font=F("sans_b", 13),
           fill=(255, 255, 255))
    yy = text_block(d, (x + 10, y + 90), kicker, F("sans_b", 9.5), RED,
                    w - 20, 12)
    yy = text_block(d, (x + 10, yy + 1), head, F("serif_b", 18.5), INK,
                    w - 20, 22, max_lines=3)
    text_block(d, (x + 10, yy + 2), dek, F("sans", 10.5), (52, 54, 60),
               w - 20, 13.5, max_lines=2)
    text_block(d, (x + 10, y + h - 25), "WHY IT MATTERS: " + why,
               F("sans_b", 9), RED, w - 20, 11, max_lines=2)


def map_row(img, d, y):
    x1 = MARGIN + 640
    d.rectangle([MARGIN, y, x1, y + 96], fill=SEA, outline=BORDER, width=1)
    d.text((MARGIN + 10, y + 4), "THE 13 ILLUSTRATED STORIES, ON THE MAP",
           font=F("sans_b", 10), fill=NAVY)
    ox, oy, cw, ch = MARGIN + 10, y + 19, 6.2, 4.2
    cells = set(MAP_ISLANDS)
    for r, c0, c1 in MAP_SEGMENTS:
        for c in range(c0, c1 + 1):
            cells.add((r, c))
    for r, c in cells:
        d.ellipse([ox + c * cw, oy + r * ch, ox + c * cw + 3.4,
                   oy + r * ch + 3.4], fill=LAND)
    for num, c, r in PINS:
        px, py = ox + c * cw, oy + r * ch
        d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        d.text((px - d.textlength(label, font=F("sans_b", 7.5)) / 2 + 0.5,
                py - 4), label, font=F("sans_b", 7.5), fill=(255, 255, 255))
    bx = x1 + 13
    bw = W - MARGIN - bx
    d.rectangle([bx, y, W - MARGIN, y + 46], fill=(238, 244, 238),
                outline=GREEN, width=1)
    d.text((bx + 9, y + 4), "DATE CHECK \u2713", font=F("sans_b", 10.5),
           fill=GREEN)
    text_block(d, (bx + 9, y + 17),
               "Every story happened, or was first reported, on Wednesday "
               "25 November 2026.", F("sans", 9.5), (52, 54, 60), bw - 18,
               11.5)
    d.rectangle([bx, y + 52, W - MARGIN, y + 96], fill=(250, 246, 232),
                outline=GOLD, width=1)
    d.text((bx + 9, y + 56), "HOW SURE ARE WE?", font=F("sans_b", 10.5),
           fill=(140, 104, 20))
    text_block(d, (bx + 9, y + 69),
               "OFFICIAL = officials on the record · REPORTED = news "
               "agencies · CLAIM = one side's claim.", F("sans", 9.5),
               (52, 54, 60), bw - 18, 11.5)


def mid_card(img, d, x, y, w, h, idx):
    head, summary, sure = MIDS[idx]
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=1)
    SCENES[idx + 3](img, (x + 1, y + 1, x + w - 1, y + 41))
    d.ellipse([x + 5, y + 5, x + 21, y + 21], fill=RED)
    label = str(idx + 4)
    d.text((x + 13 - d.textlength(label, font=F("sans_b", 9)) / 2, y + 8),
           label, font=F("sans_b", 9), fill=(255, 255, 255))
    yy = text_block(d, (x + 7, y + 44), head, F("sans_b", 11), INK, w - 14,
                    13, max_lines=2)
    text_block(d, (x + 7, yy + 1), summary, F("sans", 9), (52, 54, 60),
               w - 14, 11, max_lines=3)


def briefs(d, y):
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    d.text((MARGIN, y + 4), "ALSO ON WEDNESDAY -- THE REST OF THE DAY, "
           "IN BRIEF", font=F("sans_b", 12), fill=INK)
    key = ("NA N.AMERICA · LATAM LATIN AMERICA · EUR EUROPE · RUS RUSSIA · "
           "ME MID EAST · AFR AFRICA · SAS S.ASIA · OCE OCEANIA")
    d.text((W - MARGIN - d.textlength(key, font=F("sans", 8.5)), y + 6),
           key, font=F("sans", 8.5), fill=GREY)
    cols = [list(range(0, 10)), list(range(10, 19)), list(range(19, 28)),
            list(range(28, 37))]
    cw = (INNER - 3 * 10) // 4
    for ci, group in enumerate(cols):
        x = MARGIN + ci * (cw + 10)
        yy = y + 24
        for gi in group:
            region, text = BRIEFS[gi]
            d.text((x, yy), str(gi + 14), font=F("sans_b", 9.5), fill=RED)
            d.text((x + 15, yy + 1), region, font=F("sans_b", 7.5),
                   fill=NAVY)
            yy = text_block(d, (x + 45, yy), text, F("sans", 9.5),
                            (40, 42, 48), cw - 47, 11, max_lines=2)
            yy += 3


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    stat_strip(img, d)
    cw = (INNER - 2 * 13) // 3
    for i in range(3):
        hero_card(img, d, MARGIN + i * (cw + 13), 146, cw, 232, i)
    map_row(img, d, 386)
    mw = (INNER - 4 * 10) // 5
    for r in range(2):
        for c in range(5):
            mid_card(img, d, MARGIN + c * (mw + 10), 490 + r * 116, mw, 108,
                     r * 5 + c)
    briefs(d, 722)
    foot = ("Set in one page by an AI agent · Sources: Reuters, AP, BBC, "
            "official statements · entry.png, 1024 x 1024")
    d.text(((W - d.textlength(foot, font=F("sans", 8.5))) / 2, 1010), foot,
           font=F("sans", 8.5), fill=GREY)
    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    import os
    print("entry.png bytes:", os.path.getsize("entry.png"))
