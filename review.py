#!/usr/bin/env python3
"""Build a standalone playable review build holding one batch of puzzles.

    python3 review.py 50 61 review-batch1.html

Takes the built index.html and narrows it to the given pool indices, so Tim can
play a whole batch in one sitting instead of waiting for the dealer to spread it
over three days. Everything else is the real game: the real renderers, the real
scoring, the real hint ladder. Only the pool, the run length and the broadcast
history are swapped.

Nothing here writes to src/ or index.html.
"""
import re, sys, json, subprocess, os

ROOT = os.path.dirname(os.path.abspath(__file__))
lo, hi, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
n = hi - lo + 1

html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# --- narrow the pool, using node so the array is parsed rather than regexed ---
js = r'''
const fs=require('fs'),vm=require('vm');
const h=fs.readFileSync(process.argv[1],'utf8');
const a=h.indexOf('  /* ============================ THE PUZZLES');
const b=h.indexOf('  /* ========================= DEALING THE DAY');
const s={};vm.createContext(s);vm.runInContext(h.slice(a,b)+'\nthis.P=PUZZLES;',s);
const sel=s.P.slice(+process.argv[2], +process.argv[3]+1);
process.stdout.write(JSON.stringify(sel));
'''
sel = json.loads(subprocess.run(
    ['node', '-e', js, os.path.join(ROOT, 'index.html'), str(lo), str(hi)],
    capture_output=True, text=True, check=True).stdout)
assert len(sel) == n, len(sel)

start = html.index('  /* ============================ THE PUZZLES')
end = html.index('  /* ========================= DEALING THE DAY')
pool = ('  /* ============================ THE PUZZLES ============================ */\n'
        '  var PUZZLES = ' + json.dumps(sel, ensure_ascii=False, indent=2) + ';\n\n')
html = html[:start] + pool + html[end:]

# --- one run holding the whole batch --------------------------------------
sub = [
    (r'var RUN_SIZE = 5;', 'var RUN_SIZE = %d;' % n),
    (r'var NEW_PER_RUN = 4;', 'var NEW_PER_RUN = %d;' % n),
    # the deal must not be constrained by what has already aired
    (r'var HISTORY_SLUGS = \[.*?\n  \];', 'var HISTORY_SLUGS = [];'),
    # every chart in the batch gets a fair number of options
    (r'var OPTION_COUNT = \[4, 4, 4, 6, 6\];',
     'var OPTION_COUNT = [' + ', '.join(['4'] * 4 + ['6'] * (n - 4)) + '];'),
    (r'var MULTIPLIER   = \[1, 1\.5, 2, 2\.5, 3\];',
     'var MULTIPLIER   = [' + ', '.join(['1'] * n) + '];'),
]
for pat, rep in sub:
    html, k = re.subn(pat, rep, html, flags=re.S)
    if not k:
        sys.exit('review.py: pattern not found: ' + pat[:40])

# Every chart worth the same in a review build: the point is to see all twelve,
# not to reproduce the daily ramp.
html = html.replace('var PERFECT_BONUS = 200;', 'var PERFECT_BONUS = 0;')
html = re.sub(r'var RAMP_WORDS = \[.*?\n  \];',
              'var RAMP_WORDS = ["Review build. Every chart is worth the same."];',
              html, flags=re.S)
html = html.replace('Mystery Chart | The daily chart guessing game',
                    'Mystery Chart | batch review')

# Every review build is served from the same origin, so they all shared the
# three localStorage keys. Finishing one batch then told the next batch that
# today's run was already complete, and it opened on "See today's result".
# Namespace the keys per batch, and clear the completion flag on load so a
# review build can always be replayed. Mid-run progress still survives a
# reload, because only the done-flag is cleared, not the saved run.
ns = 'mysterychart.rev%d_%d' % (lo, hi)
for base in ('progress', 'done', 'v1'):
    html, k = re.subn(r'"mysterychart\.%s"' % base, '"%s.%s"' % (ns, base), html)
    if not k:
        sys.exit('review.py: storage key not found: ' + base)
html = html.replace(
    '  var STORE = "%s.v1";' % ns,
    '  var STORE = "%s.v1";\n'
    '  /* Review build: today\'s result is not final, so the run can be replayed. */\n'
    '  try { localStorage.removeItem("%s.done"); } catch (e) {}' % (ns, ns))

open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(html)
print('wrote %s: %d puzzles, one run of %d' % (out, len(sel), n))
for i, p in enumerate(sel):
    print('   %2d  %-9s d%d  %s' % (lo + i, p['type'], p['diff'], p['truth'][:60]))
