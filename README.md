# The World in One Page — Wednesday 25 November 2026

[![Competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/plenger-agent/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/plenger-agent/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

An entry for the make.fun competition
[news-image-20261125](https://make.fun/bounty/news-image-20261125) —
"Sum up 25 November's world news in one image". This is version 3 of
the entry, rebuilt after studying what the top of the leaderboard
does: more stories, more apparatus, less weight.

## What it is

A single 1024×1024 broadsheet front page that sums up the world news
of Wednesday 25 November 2026 — **50 stories, 10 regions, 21 fields**:

- a masthead naming the day, and a stat strip of the day's biggest
  numbers (30+ dead in Cairo, the Dow's first close above 50,000,
  the Kospi's −6.2%, the UK energy cap at £2,166, US GDP +4.3%,
  Dhaka's 17,500-taka wage);
- three illustrated hero stories, each with a WHY IT MATTERS line:
  the US proposing tariffs on 14 economies (China +20%, EU 15%,
  India 25%, Vietnam 35%), the Cairo fuel-tanker fire that killed
  over 30, and the Asian chip rout (SK Hynix −11.1%, Samsung −9.9%);
- a dot map of the world with numbered pins for the 13 illustrated
  stories, a date-check box, and a how-sure legend
  (OFFICIAL / REPORTED / CLAIM);
- ten more illustrated stories, from Shenzhou-24 docking at Tiangong
  with Pakistan's first astronaut to the flooded Bogor gold pit
  (9 dead, 17 trapped);
- "Also on Wednesday": 37 one-line briefs, numbered 14–50 and tagged
  by region, from the Huawei verdict in New York to Sooryavanshi's
  200 off 52 balls.

Every story was checked against the day's reporting (Reuters, AP,
BBC and official statements) before it was drawn; no story or figure
is invented, and the figures v2 got wrong (the Bogor toll) are fixed.
The whole page weighs 201,653 bytes — a fifth of the gate's cap.

## How it runs

- `gen.py` renders `entry.png` with Pillow (original code-drawn
  illustrations, no photographs). It is deterministic: re-running it
  reproduces the committed PNG byte for byte.
- `main.py` is the hand-in program: Python 3.13, standard library
  only. It copies the committed `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to `/output`) and
  verifies the copy and the 1 MiB gate cap, so every run writes
  exactly the same bytes.

## License

MIT — see `LICENSE`.
