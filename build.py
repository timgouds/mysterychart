#!/usr/bin/env python3
"""Mystery Chart build.

Assembles src/engine.html + src/puzzles.js into the single index.html that
gets uploaded to the repo root.

The split exists so that adding puzzles can never touch renderer code. That is
not hypothetical: a generator once emitted a stray comma into a series array
and one chart silently failed to render on day 5 only (doc 20). Keep the data
and the machinery in separate files and that class of bug cannot happen.

    python3 build.py            build and report
    python3 build.py --check    build to a temp buffer and diff against the
                                committed index.html without writing

Run `node preflight.mjs` after this. build.py checks that the file is
well-formed; preflight checks that the puzzles and the dealer are sound.
"""

import sys, os, re, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(ROOT, 'src', 'engine.html')
PUZZLES = os.path.join(ROOT, 'src', 'puzzles.js')
OUTPUT = os.path.join(ROOT, 'index.html')
PLACEHOLDER = '  /* @@PUZZLE-DATA@@ */'


def die(msg):
    print('BUILD FAILED: ' + msg, file=sys.stderr)
    sys.exit(1)


def read(path, label):
    if not os.path.exists(path):
        die('%s is missing (%s)' % (label, path))
    text = open(path, encoding='utf-8').read()
    if not text.strip():
        die('%s is empty' % label)
    return text


def build():
    engine = read(ENGINE, 'src/engine.html')
    puzzles = read(PUZZLES, 'src/puzzles.js')

    n = engine.count(PLACEHOLDER)
    if n != 1:
        die('expected exactly one %s in the engine, found %d' % (PLACEHOLDER, n))

    # The data file must not carry machinery, and the engine must not carry data.
    for token in ('function dealRun', 'function drawTreemap', 'addEventListener'):
        if token in puzzles:
            die('engine code found in src/puzzles.js: %s' % token)
    if 'var PUZZLES = [' in engine:
        die('puzzle data found in src/engine.html; it belongs in src/puzzles.js')

    out = engine.replace(PLACEHOLDER, puzzles)

    # Structural assertions on the assembled page.
    checks = [
        (out.startswith('<!doctype html>'), 'output does not start with <!doctype html>'),
        (out.count('var PUZZLES = [') == 1, 'PUZZLES array is not present exactly once'),
        ('@@' not in out, 'an unsubstituted @@marker@@ survived into the output'),
        (out.count('<script') == out.count('</script>'), 'unbalanced <script> tags'),
        ('function dealRun' in out, 'the dealer is missing from the output'),
        ('HISTORY_SLUGS' in out, 'the broadcast history is missing from the output'),
        (out.rstrip().endswith('</html>'), 'output does not end with </html>'),
    ]
    for ok, msg in checks:
        if not ok:
            die(msg)

    count = len(re.findall(r'^      family:', puzzles, re.M))
    if count < 5:
        die('only %d puzzles found; that is too few to deal a run' % count)

    return out, count


def main():
    out, count = build()
    digest = hashlib.md5(out.encode('utf-8')).hexdigest()
    previous = None
    if os.path.exists(OUTPUT):
        previous = open(OUTPUT, encoding='utf-8').read()

    if '--check' in sys.argv:
        if previous is None:
            print('index.html does not exist yet; build would create it')
        elif previous == out:
            print('index.html is up to date (%s)' % digest[:12])
        else:
            print('index.html DIFFERS from a fresh build.')
            print('  committed: %d bytes  %s' % (len(previous), hashlib.md5(previous.encode()).hexdigest()[:12]))
            print('  would be : %d bytes  %s' % (len(out), digest[:12]))
            sys.exit(1)
        return

    open(OUTPUT, 'w', encoding='utf-8').write(out)

    print('built index.html')
    print('  puzzles   %d' % count)
    print('  size      %d bytes' % len(out))
    print('  md5       %s' % digest)
    if previous is not None and previous != out:
        print('  changed   %+d bytes against the previous build' % (len(out) - len(previous)))
    elif previous == out:
        print('  unchanged')
    print('\nNext: node preflight.mjs')


if __name__ == '__main__':
    main()
