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

Batches 1 to 8 were one script of about twelve puzzles each. From batch 9 a
weekly batch of 35 is split across three scripts (`build9.py` snapshots,
`build10.py` dumbbells and slopes, `build11.py` lines) so one bad fetch does not
sink the lot. Each fetches its own data live, asserts it, and prints a JS
fragment for `src/puzzles.js`. The player-facing text lives beside each script
in `textN.py`, written from the script's `--digest` output, which prints the
final data compactly, so the reveal and the hints are written from what will be
drawn rather than from the screening pass:

    python3 build9.py --digest
    python3 build9.py > b9.js

`sources.py` holds the strict fetchers used from batch 9 on. They pin every
dimension of a dataset and stop the build if more than one value survives for a
country and year; the screening explorers do not, and quietly keep whichever
value arrived last. Two traps it handles: Eurostat's maritime data keys
countries on `rep_mar` rather than `geo`, and the OECD API often answers with an
internal server error, so it retries.

`common.py` holds the shared emitters. `wb.py`, `eu.py` and `who.py` are the
World Bank, Eurostat and WHO fetchers (no new WHO charts until its licence is settled). Two things worth knowing: Eurostat
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
