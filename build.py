#!/usr/bin/env python3
"""
Mystery Chart build.

Assembles the deployable single file from the two sources:

    src/engine.html   renderers, dealer, scoring, chrome, all the chrome and CSS
    src/puzzles.js    the puzzle pool and its data arrays, and nothing else

and writes:

    index.html        what gets uploaded to the repo root

The engine carries one marker line, `  /* @@PUZZLE-DATA@@ */`, and the build
substitutes the pool into it. That is the whole mechanism. The point of the
split is that a new batch of puzzles can no longer reach renderer code, which
is how a stray comma once left a hole in a series array and broke one day in
eight.

Run it from the repo root:

    python3 build.py

Add --check to verify the output against the currently deployed file without
writing anything.
"""

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ENGINE = ROOT / "src" / "engine.html"
PUZZLES = ROOT / "src" / "puzzles.js"
OUTPUT = ROOT / "index.html"

MARKER = "  /* @@PUZZLE-DATA@@ */\n"


def read(path):
    if not path.exists():
        sys.exit("missing: %s" % path)
    return path.read_text(encoding="utf-8")


def assemble():
    engine = read(ENGINE)
    puzzles = read(PUZZLES)

    if engine.count(MARKER) != 1:
        sys.exit(
            "src/engine.html must contain the line %r exactly once (found %d)"
            % (MARKER.strip(), engine.count(MARKER))
        )
    if "var PUZZLES" in engine:
        sys.exit("src/engine.html contains puzzle data; it belongs in src/puzzles.js")
    if "var PUZZLES" not in puzzles:
        sys.exit("src/puzzles.js does not define PUZZLES")

    return engine.replace(MARKER, puzzles)


def report(html):
    """Print the facts worth seeing on every build."""
    pool = len(re.findall(r"\n      slug: ", html))
    launch = re.search(r"var LAUNCH = new Date\(([^)]*)\)", html)
    ramp = re.search(r"var OPTION_COUNT = (\[[^\]]*\])", html)
    print("  pool          %d puzzles" % pool)
    if ramp:
        print("  option ramp   %s" % ramp.group(1))
    if launch:
        print("  launch        new Date(%s)" % launch.group(1))
    print("  size          %.0f KB" % (len(html.encode("utf-8")) / 1024))

    # Fresh material lasts roughly pool / NEW_PER_RUN runs from launch. The
    # engine's own runwayFrom() is exact; this is the cheap approximation, and
    # it is here so a short runway is visible on every build rather than
    # discovered by a player.
    new_per_run = re.search(r"var NEW_PER_RUN = (\d+)", html)
    if new_per_run and pool:
        runs = pool // int(new_per_run.group(1))
        print("  runway        ~%d runs of fresh material from launch" % runs)


def main():
    check_only = "--check" in sys.argv
    html = assemble()

    print("build.py")
    report(html)

    if check_only:
        if not OUTPUT.exists():
            sys.exit("no index.html to check against")
        current = read(OUTPUT)
        same = hashlib.sha256(html.encode()).hexdigest() == hashlib.sha256(
            current.encode()
        ).hexdigest()
        print("  check         %s" % ("identical to index.html" if same else "DIFFERS from index.html"))
        sys.exit(0 if same else 1)

    OUTPUT.write_text(html, encoding="utf-8")
    print("  wrote         index.html")


if __name__ == "__main__":
    main()
