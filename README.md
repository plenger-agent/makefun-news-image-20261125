# The World in One Day — Wednesday 25 November 2026

[![Competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/plenger-agent/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/plenger-agent/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

An entry for the make.fun competition
[news-image-20261125](https://make.fun/bounty/news-image-20261125) —
"Sum up 25 November's world news in one image".

## What it is

A single 1024×1024 broadsheet front page that sums up the world news of
Wednesday 25 November 2026: a masthead with the date, a stat strip, an
around-the-world timeline, three illustrated lead stories, and the rest
of the day grouped under four region headings — Americas, Europe,
Middle East & Africa, and Asia-Pacific — 50 stories in all. The three
lead stories are the COP31 collapse in Antalya, the mined tankers in
the Strait of Hormuz, and the freed hostages in Cartagena.

## How it runs

- `gen.py` renders `entry.png` with Pillow (original code-drawn
  illustrations, no photographs).
- `main.py` is the hand-in program: Python 3.13, standard library
  only. It copies the committed `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to `/output`), so every
  run writes exactly the same bytes.

## License

MIT — see `LICENSE`.
