[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aziraiga21/world-in-one-day-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aziraiga21/world-in-one-day-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — Monday 23 November 2026

A single 1024x1024 PNG newspaper front page summing up the world news of
Monday 23 November 2026: 35 stories across 6 regions, drawn entirely in code
(Python + Pillow). Lead stories: Iran readies tankers to break the US blockade,
COP31 collapses in Antalya, and Zelensky counts 109 bridge strikes. Every
story happened, or was first reported, on Monday 23 November 2026 — the
date-check footer on the page says which three were reported Monday but
happened Sunday, and which Sunday stories were left out.

## How to run

```sh
python3 draw.py        # regenerate entry.png (1024x1024, under 1 MiB)
python3 main.py        # copy entry.png to $MAKEFUN_OUTPUT_DIR (default: output)
```

`draw.py` is deterministic: no random values, no timestamps, no network. It
self-checks that every text block fits its box and that the numbered map dots
stay at least 10 px apart.

## Files

- `draw.py` — the Pillow program that draws the page and saves `entry.png`
- `entry.png` — the front page (1024x1024)
- `main.py` — entrypoint: copies `entry.png` to the output directory
- `README.md` — this file
- `LICENSE` — MIT license
