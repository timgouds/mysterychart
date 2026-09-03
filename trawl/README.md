# Batch builders

## Screening comes first

`screen.py` decides whether an indicator is worth a puzzle, and prints about a
dozen lines instead of the few hundred rows a raw fetch returns. That
difference is the whole point: exploring candidates by fetching and reading
them costs the same for the ones you reject as for the ones you keep.

    python3 screen.py wb   SH.MED.BEDS.ZS 2020
    python3 screen.py wb   SP.DYN.LE00.IN 2000 2023     two years: pair mode
    python3 screen.py owid coffee-bean-production 2024
    python3 screen.py who  MALARIA_EST_CASES
    python3 screen.py eu   ilc_scp09

It runs the checks that were previously applied by eye: the population-ranking
test (doc 02), the outlier sanity check (doc 02), entity continuity across a
range (doc 03), and the mixed-reference-year check (doc 22). A ranking that
tracks population too closely is rejected outright, because almost any metric
would produce that order.

Add `--bank` to append the verdict to `bank.tsv`. Screen twenty candidates in
one cheap pass, then open the batch session with the bank as its input rather
than rediscovering everything. This is the candidate bank doc 21 asked for.

## Building a batch

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

Slugs must be readable words, not the source's indicator code: the slug is the
analytics key and it prints on the results screen. `preflight.mjs` enforces it.
