# Mystery Chart

A daily chart guessing game. Five real charts a day, built from public data.
The title is blacked out; you work out what the chart measures from the
countries, the years and the numbers, which are all exactly as published.

**Play: https://mysterychart.net**

## Repo layout

| Path | What it is |
|---|---|
| `index.html` | The built game. Generated. Do not edit by hand. |
| `src/engine.html` | Page, chart renderers, dealer, scoring. |
| `src/puzzles.js` | The puzzle pool, and nothing else. |
| `build.py` | Assembles `index.html` from the two source files. |
| `preflight.mjs` | Content and dealer checks. Exit 1 blocks a ship. |
| `review.py` | Builds a standalone playable file holding one batch, for review. |
| `play.mjs` | Drives a review build in a real browser and screenshots every chart. |
| `trawl/` | The batch builders. One script per batch, plus the source fetchers. |
| `CNAME` | The custom domain. One line: `mysterychart.net`. |
| `sitemap.xml`, `social-card.png` | Search listing and the link preview image. |
| `play/index.html` | Redirect to `/`, keeping an old link alive. |

## Shipping a change

```
python3 build.py        # assemble index.html
node preflight.mjs      # checks; must pass
```

Then commit `index.html` along with the changed source. `python3 build.py --check`
reports whether the committed `index.html` still matches the sources.

See `src/README.md` for why the sources are split and how to add puzzles.

## Adding a batch of puzzles

```
python3 trawl/build6.py > batch6.js     # fetch live data, assert, emit JS
                                        # append the output to src/puzzles.js
python3 build.py
node preflight.mjs
python3 review.py 110 121 review-batch6.html   # the batch as one playable run
node play.mjs review-batch6.html               # click through it, screenshot each chart
```

Append to the end of `PUZZLES`. Never insert or reorder: the broadcast history
is keyed on slug, but the dealer treats position as stable.

`review.py` takes a range of pool indices and narrows the real game down to
those puzzles as a single run, so a whole batch can be played in one sitting
instead of waiting for the dealer to spread it over days. Everything else is
the real game: the real renderers, the real scoring, the real hint ladder.

`play.mjs` answers every chart correctly and screenshots it, flagging a missing
SVG, a collapsed chart, `undefined`/`NaN` in a label, horizontal overflow or a
console error. Doc 16: every bug that round was invisible in code review and
only appeared when the specific chart was drawn with the specific data.

See `trawl/README.md` for the fetchers and the two format traps.

## What preflight checks

Content: required fields, exactly seven decoys and four hints, no duplicate
options, no em-dashes in player-facing text, no answer word leaking into hint 1,
no decoy that is another puzzle's answer anywhere in the pool, and a reveal that
names any entity dominating its chart.

Dealer: determinism, five charts a run, difficulty never falling within a run,
form variety, and the broadcast history still resolving.

Runway: the last run carrying four new charts, and how many days that leaves.
Under seven days warns; already exhausted fails.

Every rule exists because something went wrong once. The doc reference in the
source says where.

## Data

Charts are drawn from Our World in Data, the World Bank, WHO and Eurostat.
OWID and World Bank data are CC BY 4.0; each chart carries its own source and
link on the results screen, with the licence where one applies.
