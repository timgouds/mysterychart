# Batch builders

One script per batch of twelve puzzles. Each fetches its own data live, asserts
the data is usable, and prints a JS fragment for `src/puzzles.js`:

    python3 build4.py > batch4.js

`common.py` holds the shared emitters. `wb.py`, `eu.py` and `who.py` are the
World Bank, Eurostat and WHO fetchers. Two things worth knowing: Eurostat
arrives as JSON-stat and has to be decoded by computing the cube's strides
rather than read from a summary (doc 22 records what happens otherwise), and
OECD CSV is gzip, so curl needs `--compressed`.

The asserts are the point of these scripts. Every batch hit at least one dataset
where an entity was missing from one end of a time range: Ethiopia before 1993,
Sudan before 2012, Russia's 2000 fuel exports, Germany's age-at-first-child
before 2009. Without the assert each of those becomes a chart that is wrong in a
way no player could detect.

Rebuilding re-fetches live data, so figures may shift as sources revise. Re-run
`preflight.mjs` and the screenshot pass afterwards.
