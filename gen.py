#!/usr/bin/env python3
"""Render entry.png: a one-page broadsheet summing up the world news of
Wednesday 25 November 2026 for make.fun competition news-image-20261125.

Layout: masthead + stat strip + around-the-world timeline + three
illustrated lead stories + the rest of the day grouped under four
region headings (Americas / Europe / Middle East & Africa /
Asia-Pacific). 50 stories in all. All illustrations are original and
drawn in code with Pillow; no photographs are used.

Run locally to (re)generate entry.png. The hand-in program (main.py)
only copies the committed PNG and needs no third-party packages.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAD = 20
CW = W - 2 * PAD

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"

PAPER = (246, 239, 221)
INK = (25, 21, 16)
FAINT = (178, 164, 128)
WHITE = (252, 250, 244)

C_AME = (29, 78, 216)      # Americas - blue
C_EUR = (109, 40, 217)     # Europe - violet
C_MEA = (180, 83, 9)       # Middle East & Africa - amber
C_APA = (4, 120, 87)       # Asia-Pacific - green

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(text, fnt):
    return d.textlength(text, font=fnt)


def center(text, y, fnt, fill=INK):
    d.text(((W - tw(text, fnt)) / 2, y), text, font=fnt, fill=fill)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def check(text, fnt, max_w, what):
    if tw(text, fnt) > max_w:
        WARNINGS.append(f"OVERFLOW {what}: {text!r} {tw(text, fnt):.0f}>{max_w}")


# ---------------------------------------------------------------- masthead
center("THE WORLD IN ONE DAY", 12, font(SERIF_B, 47))
center("WEDNESDAY 25 NOVEMBER 2026", 66, font(SANS_B, 25))
center("50 STORIES  ·  FOUR REGIONS  ·  ONE DAY  ·  FROM WEDNESDAY'S WORLD WIRES",
       95, font(SANS, 12), fill=(90, 78, 52))
d.rectangle([PAD, 112, W - PAD, 115], fill=INK)
d.line([PAD, 118, W - PAD, 118], fill=INK, width=1)

# ---------------------------------------------------------------- stat strip
STATS = [
    ("-2.8%", "NIKKEI 225 CLOSE"),
    ("$87.49", "BRENT CRUDE / BARREL"),
    ("7,201", "S&P 500, -0.5% ON DAY"),
    ("20", "HOSTAGES FREED, COLOMBIA"),
    ("+36%", "BANGLADESH TEXTILE WAGE"),
]
f_num, f_lab = font(SANS_B, 23), font(SANS, 9)
cell = CW / len(STATS)
for i, (num, lab) in enumerate(STATS):
    cx = PAD + cell * i + cell / 2
    d.text((cx - tw(num, f_num) / 2, 126), num, font=f_num, fill=INK)
    d.text((cx - tw(lab, f_lab) / 2, 156), lab, font=f_lab, fill=(90, 78, 52))
    if i:
        d.line([PAD + cell * i, 128, PAD + cell * i, 168], fill=FAINT, width=1)
d.line([PAD, 176, W - PAD, 176], fill=FAINT, width=1)

# ---------------------------------------------------------------- timeline
f_place, f_ev = font(SANS_B, 11), font(SANS, 10)
NODES = [
    ("CARTAGENA", "Hostages freed", C_AME),
    ("ANTALYA", "COP31 collapses", C_EUR),
    ("HORMUZ", "Tankers mined", C_MEA),
    ("KHARTOUM", "Drones condemned", C_MEA),
    ("DHAKA", "Wages up 36%", C_APA),
    ("CANBERRA", "Security treaty", C_APA),
]
AXIS_Y = 208
d.line([PAD + 10, AXIS_Y, W - PAD - 10, AXIS_Y], fill=FAINT, width=2)
for i, (place, ev, col) in enumerate(NODES):
    x = 70 + i * 176
    d.text((x - tw(place, f_place) / 2, 186), place, font=f_place, fill=col)
    d.ellipse([x - 5, AXIS_Y - 5, x + 5, AXIS_Y + 5], fill=col)
    d.text((x - tw(ev, f_ev) / 2, 218), ev, font=f_ev, fill=INK)
d.line([PAD, 238, W - PAD, 238], fill=FAINT, width=1)

# ---------------------------------------------------------------- leads
LEAD_Y, LEAD_H, LEAD_W, LEAD_GAP = 246, 214, 320, 12


def ill_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 233, 245))
    d.ellipse([x + w - 78, y + 10, x + w - 34, y + 54], fill=(244, 197, 66))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 113, 96))
    for cx, chw, cht in ((x + 52, 30, 52), (x + 118, 24, 38)):
        d.rectangle([cx, y + h - 16 - cht, cx + chw, y + h - 16], fill=(74, 70, 64))
        for sx, sy, sr in ((cx + 4, y + h - 30 - cht, 13), (cx + 22, y + h - 44 - cht, 17),
                          (cx + 44, y + h - 56 - cht, 21)):
            d.ellipse([sx, sy, sx + 2 * sr, sy + sr], fill=(238, 240, 242))


def ill_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 216, 234))
    d.polygon([(x, y), (x + 108, y), (x + 62, y + 34), (x, y + 40)], fill=(222, 198, 148))
    d.polygon([(x + w, y), (x + w - 108, y), (x + w - 62, y + 34), (x + w, y + 40)],
              fill=(222, 198, 148))
    d.rectangle([x, y + 40, x + w, y + h], fill=(106, 164, 204))
    for wx in range(x + 8, x + w - 20, 34):
        d.arc([wx, y + h - 18, wx + 24, y + h - 4], 0, 180, fill=(230, 244, 250), width=2)
    hx, hy = x + w // 2, y + 52
    d.polygon([(hx - 62, hy + 16), (hx + 62, hy + 16), (hx + 46, hy + 30), (hx - 46, hy + 30)],
              fill=(52, 52, 56))
    d.rectangle([hx - 40, hy + 4, hx + 34, hy + 16], fill=(178, 60, 44))
    d.rectangle([hx + 38, hy - 6, hx + 50, hy + 16], fill=(90, 90, 96))
    for mx, my in ((x + 56, y + 62), (x + w - 66, y + 70)):
        d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(40, 40, 44))
        for dx, dy in ((0, -14), (10, -10), (14, 0), (10, 10), (0, 14), (-10, 10), (-14, 0), (-10, -10)):
            d.line([mx, my, mx + dx, my + dy], fill=(40, 40, 44), width=2)


def ill_colombia(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 196))
    d.rectangle([x + 26, y + 26, x + w - 26, y + h], fill=(233, 220, 192))
    for i in range(9):
        col = (178, 60, 44) if i % 2 == 0 else (252, 250, 244)
        d.rectangle([x + 26 + i * 30, y + 14, x + 56 + i * 30, y + 30], fill=col)
    d.rectangle([x + 40, y + 44, x + 104, y + 76], fill=(150, 186, 205))
    d.rectangle([x + w - 104, y + 44, x + w - 40, y + 76], fill=(150, 186, 205))
    d.rectangle([x + w // 2 - 17, y + 40, x + w // 2 + 17, y + h], fill=(110, 78, 52))
    for px in (x + 66, x + 96, x + w - 96):
        d.ellipse([px - 6, y + 62, px + 6, y + 74], fill=(70, 54, 40))
        d.rectangle([px - 5, y + 74, px + 5, y + 90], fill=(70, 90, 140))
    gx, gy = x + w - 52, y + 22
    d.ellipse([gx - 17, gy - 17, gx + 17, gy + 17], fill=(4, 120, 87))
    d.line([gx - 8, gy, gx - 2, gy + 7], fill=WHITE, width=4)
    d.line([gx - 2, gy + 7, gx + 10, gy - 8], fill=WHITE, width=4)


LEADS = [
    (C_EUR, "CLIMATE · ANTALYA, TÜRKIYE", "COP31 TALKS COLLAPSE IN ANTALYA",
     "Saudi Arabia and oil producers blocked any mention of phasing out "
     "fossil fuels, pushing carbon capture instead.", ill_cop31),
    (C_MEA, "IRAN WAR · STRAIT OF HORMUZ", "TANKERS HIT MINES IN HORMUZ",
     "Two tankers struck mines in the strait, the Revolutionary Guards "
     "said. Tehran wants US troops out and Hormuz under its control; "
     "phosphate fertiliser supplies are down 40%.", ill_hormuz),
    (C_AME, "COLOMBIA · HOSTAGE SIEGE ENDS", "20 HOSTAGES FREED IN CARTAGENA",
     "Armed men seized about 20 people inside a Cartagena supermarket. "
     "Every hostage was freed and there were no casualties, officials "
     "said.", ill_colombia),
]
f_tag, f_head, f_sum = font(SANS_B, 10), font(SANS_B, 16), font(SANS, 12)
for i, (col, tag, head, summ, ill) in enumerate(LEADS):
    x = PAD + i * (LEAD_W + LEAD_GAP)
    d.rectangle([x, LEAD_Y, x + LEAD_W, LEAD_Y + LEAD_H], outline=FAINT, width=1)
    ill(x + 1, LEAD_Y + 1, LEAD_W - 2, 92)
    ty = LEAD_Y + 100
    d.rectangle([x + 10, ty + 1, x + 13, ty + 12], fill=col)
    d.text((x + 18, ty), tag, font=f_tag, fill=col)
    ty += 17
    for line in wrap(head, f_head, LEAD_W - 20):
        d.text((x + 10, ty), line, font=f_head, fill=INK)
        ty += 21
    ty += 2
    for line in wrap(summ, f_sum, LEAD_W - 20):
        d.text((x + 10, ty), line, font=f_sum, fill=INK)
        ty += 15

# ---------------------------------------------------------------- regions
REGIONS = [
    ("AMERICAS", C_AME, [
        "Nvidia falls 7% as US lawmakers question Trump's Huang role",
        "Anthropic, OpenAI staff fear new models too unsafe to ship",
        "Democrats win House majority of at least 259 seats",
        "US readies new global tariffs; South Korea in the frame",
        "Ábrego García leaves the US for Spain",
        "Pentagon faults Canada's military spending",
        "Small plane crashes in Gulf of Mexico; six dead",
        "WHO chief urges end to US fuel blockade on Cuba",
        "Colombia car bomb injures at least 23 people",
    ]),
    ("EUROPE", C_EUR, [
        "Ukraine strikes Russian warship off Libya; 2 Libyans dead",
        "Spain heads for a snap election",
        "Real Madrid rout PSV 5-1: Bellingham stunner, Mbappé brace",
        "Turkish army helicopter crashes; at least 5 killed",
        "Murmansk governor held over financial misconduct",
        "Sarkozy and Bruni face trial in Libya funding case",
        "Germany puts €34m into Ukrainian Babka drones for Kyiv",
        "Ex-UK PM: Trump's warm words to Putin are 'unsettling'",
        "Zelenskyy: 'Invite Putin to Kyiv'; presses NATO bid",
        "Sweden's MPs to vote on Kristersson staying as PM",
        "Latvia's president sees a 'crucial moment' in the war",
    ]),
    ("MIDDLE EAST & AFRICA", C_MEA, [
        "Yemen: coalition hits Hodeidah; Houthis threaten Jeddah",
        "Senegal regain CAN-2025 crown after a CAS ruling",
        "Iran flogs singer 74 times over an unveiled concert",
        "DR Congo: army plane missing; rebels claim a downing",
        "Zambia indicts opposition leader on treason charges",
        "Drone attacks on Khartoum condemned; Blue Nile abductions",
        "Iraq orders federal forces to seize Kurdish oilfields",
        "Iran drug shortage leaves patients hunting medicines",
        "Cameroon separatist leader in Norway war-crimes court",
        "Nigerian emir suspended after an assault allegation",
        "Ebola-hit DR Congo: violence against women is rising",
        "Gaza: three Palestinians killed in an Israeli strike",
        "Israeli strike kills Hamas spokesman and his family",
        "Britain sanctions the Houthis and 4 top rebel officials",
    ]),
    ("ASIA-PACIFIC", C_APA, [
        "Nepal exits COP31 without flood aid; 7,000 homes wrecked",
        "Huawei guilty in US of conspiracy to steal trade secrets",
        "Pakistan's first astronaut reaches China's space station",
        "Bangladesh lifts textile minimum wage 36% after protests",
        "Indonesia mine rescue: dozens trapped 100 m down",
        "Solomon Islands, Australia sign no-foreign-bases treaty",
        "China investigates Shanghai party chief Chen Jining",
        "World court genocide ruling on Myanmar faces a key test",
        "Qianfan: China's answer to Starlink takes shape",
        "Hong Kong marks one year since the Tai Po fire",
        "Xiamen Airlines orders 50 Boeing 737-8 jets",
        "Indonesia's vice-president resigns amid political strain",
    ]),
]
f_rhead, f_rcount, f_story = font(SANS_B, 14), font(SANS, 10), font(SANS, 13)
ROW_H = 16.0
y = 466.0
for name, col, stories in REGIONS:
    d.rectangle([PAD, y, W - PAD, y + 25], fill=col)
    d.text((PAD + 10, y + 5), name, font=f_rhead, fill=WHITE)
    cnt = f"{len(stories)} STORIES"
    d.text((W - PAD - 10 - tw(cnt, f_rcount), y + 7), cnt, font=f_rcount, fill=WHITE)
    y += 27
    half = (len(stories) + 1) // 2
    cols = (stories[:half], stories[half:])
    top = y
    for ci, colstories in enumerate(cols):
        cx = PAD if ci == 0 else PAD + CW // 2 + 12
        maxw = CW // 2 - 12 - 14 if ci == 0 else CW - CW // 2 - 12 - 14
        cy = top
        for s in colstories:
            check(s, f_story, maxw, name)
            d.rectangle([cx, cy + 4, cx + 7, cy + 11], fill=col)
            d.text((cx + 14, cy), s, font=f_story, fill=INK)
            cy += ROW_H
    y = top + half * ROW_H + 5
    d.line([PAD + CW // 2, top - 2, PAD + CW // 2, y - 7], fill=FAINT, width=1)
print(f"regions end y = {y:.0f}")

# ---------------------------------------------------------------- footer
d.line([PAD, 994, W - PAD, 994], fill=INK, width=1)
center("All stories dated 25 November 2026 · Compiled 25 Nov 2026 · Sources: the day's world news wires",
       999, font(SANS, 10), fill=(90, 78, 52))

for wtext in WARNINGS:
    print("WARN:", wtext)
img.save("entry.png", optimize=True)
import os
print("entry.png bytes:", os.path.getsize("entry.png"))
