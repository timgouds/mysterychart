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

## Shipping a change

```
python3 build.py        # assemble index.html
node preflight.mjs      # 12 checks; must pass
```

Then commit `index.html` along with the changed source. `python3 build.py --check`
reports whether the committed `index.html` still matches the sources.

See `src/README.md` for why the sources are split and how to add puzzles.

## Data

Charts are drawn from Our World in Data, the World Bank, WHO and Eurostat.
OWID and World Bank data are CC BY 4.0; each chart carries its own source and
link on the results screen.
