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
python3 trawl/build9.py --digest        # the data each chart will draw
python3 trawl/build9.py > b9.js         # fetch live data, assert, emit JS
                                        # append the output to src/puzzles.js
python3 build.py
node preflight.mjs
python3 review.py 163 197 review-b9.html     # the batch as one playable run
node play.mjs review-b9.html                 # click through it, screenshot each chart
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

Content: required fields, at least four decoys and exactly four hints, readable
slugs, no duplicate options, no em-dashes in player-facing text, no answer word
leaking into hint 1, a reveal that names any entity dominating its chart, and
every country a reveal or hint places on a chart actually being on it. A shown
decoy that is another puzzle's answer is reported as a warning, not a failure;
the dealer keeps such pairs apart.

Dealer: determinism, five charts a run, form variety, no clashing pairs dealt
together, four options per chart, no line chart with more series than colours,
gentle openers and hard closers (a warning), and the broadcast history still
resolving.

Runway: charts are never recycled, so every new run takes five charts nobody
has seen and the pool has to stay ahead of the calendar. Preflight reports the
last fully fresh run and its date. Under fourteen days warns; under seven days
fails, and so does any run in the coming week that would need the emergency
fill from old charts.

Every rule exists because something went wrong once. The doc reference in the
source says where.

## Data

Charts are drawn from Our World in Data, the World Bank, WHO, Eurostat and the OECD.
OWID and World Bank data are CC BY 4.0; each chart carries its own source and
link on the results screen, with the licence where one applies.
