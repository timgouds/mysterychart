# src/

The game is built from two files. Never edit `index.html` at the repo root by
hand: it is generated, and the next build will overwrite whatever you typed.

| File | What it holds |
|---|---|
| `engine.html` | The page, the chart renderers, the dealer, scoring, the chrome. |
| `puzzles.js` | The puzzle pool, and nothing else. |

`build.py` substitutes `puzzles.js` into the `/* @@PUZZLE-DATA@@ */` marker in
`engine.html` and writes `../index.html`.

## Why they are separate

Adding puzzles must never be able to touch renderer code. In doc 20 a generator
emitted a stray comma into a series array and one chart silently failed to
render on day 5 only. It was found by an eight-day sweep, not by reading the
file. With the data in its own file that whole class of bug cannot reach the
machinery.

## To ship a change

```
python3 build.py        # assemble index.html and report
node preflight.mjs      # 12 content and dealer checks; exit 1 blocks the ship
```

Then upload `index.html` to the repo root. `python3 build.py --check` tells you
whether the committed `index.html` still matches the sources without writing.

## Adding puzzles

Append to the end of `PUZZLES` in `puzzles.js`. Never insert or reorder: the
broadcast history in `engine.html` is keyed on slug so a reorder will not
corrupt it silently, but the dealer treats position as stable and there is no
reason to disturb it.

Each puzzle needs a unique `slug`, a `truth`, a `period`, exactly seven
`decoys` ordered strongest first, exactly four `hints`, a `diff` of 1 to 5, and
the fields its chart form requires. `preflight.mjs` checks all of that.

## After a batch

The deal is a function of the whole pool, so adding puzzles moves every future
run. Regenerate the catalogue spreadsheet and re-record the runway.
