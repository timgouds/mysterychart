/* Mystery Chart preflight.
 *
 * Run after `python3 build.py`. Exits 1 if anything would ship broken.
 *
 * build.py checks the file is well-formed. This checks the puzzles are sound
 * and the dealer behaves. Every rule here exists because something went wrong
 * once; the doc reference says where.
 *
 *     node preflight.mjs
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import vm from 'vm';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

let failures = 0, warnings = 0;
const fail = (m) => { console.log('  FAIL   ' + m); failures++; };
const warn = (m) => { console.log('  WARN   ' + m); warnings++; };
const pass = (m) => console.log('  ok     ' + m);
const check = (cond, ok, bad) => cond ? pass(ok) : fail(bad);

/* ---- load the pool and the dealer out of the built file ----------------- */
const sandbox = { console, window: { console }, module: {} };
const from = (marker, until) => {
  const a = html.indexOf(marker), b = html.indexOf(until);
  if (a < 0 || b < 0 || b < a) throw new Error('cannot locate ' + marker);
  return html.slice(a, b);
};
const code =
  from('function seededShuffle', 'var LETTERS') +
  from('  /* ============================ THE PUZZLES', '  /* ========================= DEALING THE DAY') +
  from('  var RUN_SIZE = 5;', '  var OPTION_COUNT');
vm.createContext(sandbox);
vm.runInContext(code + '\nthis.P = PUZZLES; this.dealRun = dealRun; this.runCost = runCost; this.HISTORY = HISTORY;', sandbox);
const { P, dealRun, runCost, HISTORY } = sandbox;

const RUN_SIZE = 5, NEW_PER_RUN = 4;
const NEEDS = {
  treemap:   ['data', 'total', 'unit'],
  lollipop:  ['data', 'unit'],
  beeswarm:  ['data', 'unit'],
  dumbbell:  ['data', 'leftYear', 'rightYear'],
  slope:     ['ranks', 'leftYear', 'rightYear'],
  line:      ['series', 'startYear'],
  deviation: ['data', 'unit'],
  symbol:    ['data', 'unit'],
};

console.log('\n=== CONTENT ===');
check(P.length >= 5, `pool holds ${P.length} puzzles`, `pool is only ${P.length}, too few to deal`);

const slugs = new Set(), truths = new Set();
let bad = [];
P.forEach((q, i) => {
  const id = `[${i}] ${(q.truth || 'UNTITLED').slice(0, 34)}`;
  if (!q.truth) bad.push(id + ': no truth');
  if (!q.slug) bad.push(id + ': no slug');
  if (slugs.has(q.slug)) bad.push(id + ': duplicate slug ' + q.slug);
  if (truths.has(q.truth)) bad.push(id + ': duplicate answer');
  slugs.add(q.slug); truths.add(q.truth);
  if (!(q.diff >= 1 && q.diff <= 5)) bad.push(id + ': diff out of range');
  if (!q.period) bad.push(id + ': no period');            /* doc 10 */
  if (!Array.isArray(q.decoys) || q.decoys.length !== 7) bad.push(id + `: ${q.decoys ? q.decoys.length : 0} decoys, want 7`);
  if (!Array.isArray(q.hints) || q.hints.length !== 4) bad.push(id + `: ${q.hints ? q.hints.length : 0} hints, want 4`);
  const opts = [q.truth].concat(q.decoys || []);
  if (new Set(opts).size !== opts.length) bad.push(id + ': an option is duplicated');
  (NEEDS[q.type] || []).forEach(f => {
    if (q[f] === undefined || q[f] === null) bad.push(id + `: ${q.type} needs ${f}`);   /* doc 23 */
  });
  if (Array.isArray(q.series) && q.series.some(s => (s.values || s).some?.(v => v === undefined)))
    bad.push(id + ': sparse array in series');                                          /* doc 20 */
});
check(!bad.length, 'all 50 puzzles carry their required fields', 'field problems:\n         ' + bad.join('\n         '));

/* Slugs must be readable words, not raw source codes.
 *
 * The slug is not internal: the results screen prints it as the link text
 * beside the source credit, so a World Bank indicator code ships to the player
 * as "IS.SHP.GOOD.TU". It is also the analytics key, so chart/<slug>/<tier>
 * is unreadable on the dashboard without a lookup. 70 of 122 puzzles were in
 * this state before the batch-seven pass; the batch builders emit the source
 * code by default, so without this check they come straight back. */
const rawSlug = P.map((q, i) => [i, q])
  .filter(([, q]) => q.slug && (/[._]/.test(q.slug) || /[A-Z]/.test(q.slug)))
  .map(([i, q]) => `[${i}] "${q.slug}" (${q.truth.slice(0, 40)})`);
check(!rawSlug.length, 'every slug is readable rather than a source code',
  'raw source codes used as slugs:\n         ' + rawSlug.join('\n         '));

/* House style: no em-dashes anywhere a player can see. doc 11 */
const emdash = [];
P.forEach((q, i) => {
  [q.truth, q.why, ...(q.decoys || []), ...(q.hints || [])].forEach(s => {
    if (typeof s === 'string' && s.includes('\u2014')) emdash.push(`[${i}] ${s.slice(0, 46)}`);
  });
});
check(!emdash.length, 'no em-dashes in player-facing text', 'em-dashes found:\n         ' + emdash.join('\n         '));

/* Hint 1 must not contain a content word from the answer. doc 09
 * Two refinements learned the hard way:
 *   - match whole words, or "Ireland" trips the check on "land";
 *   - ignore words that appear in every option, since a word shared by the
 *     answer and all seven decoys cannot narrow anything down. */
const STOP = new Set(('a an the of in on at to for and or by per from with as is are was were '
  + 'that this these those it its their his her share total number rate people population world '
  + 'country countries year years each every most least more less than over under between').split(' '));
const words = (s) => (s || '').toLowerCase().replace(/[^a-z\s]/g, ' ').split(/\s+/).filter(Boolean);
const leaks = [];
P.forEach((q, i) => {
  if (!q.hints || !q.hints[0]) return;
  const h = q.hints[0].toLowerCase();
  const decoyWordSets = (q.decoys || []).map(d => new Set(words(d)));
  words(q.truth)
    .filter(w => w.length > 3 && !STOP.has(w))
    .filter(w => !decoyWordSets.every(s => s.has(w)))
    .forEach(w => {
      if (new RegExp('\\b' + w + '\\b').test(h)) leaks.push(`[${i}] "${w}" appears in hint 1`);
    });
});
check(!leaks.length, 'no answer word leaks into hint 1', 'leaks:\n         ' + leaks.join('\n         '));

/* A decoy must never be another puzzle's answer in the same run. Doc 16 ran
 * this as a one-off script and it was never ported here; with the pool more
 * than doubling it is now the likeliest way to ship an unfair puzzle, because
 * the player would see the same sentence twice and one of them would be wrong.
 * Checked across the whole pool rather than against the current deal. Two
 * puzzles that do not meet today will meet eventually, and every new batch
 * re-deals every future run, so a deal-scoped check passes one week and fails
 * the next for reasons nobody changed. */
const answersOf = (q) => [q.truth, q.answer].filter(Boolean);
const answerIndex = new Map();
P.forEach((q, i) => answersOf(q).forEach(a => answerIndex.set(a.toLowerCase().trim(), i)));
const collisions = [];
P.forEach((q, i) => (q.decoys || []).forEach(d => {
  const j = answerIndex.get(d.toLowerCase().trim());
  if (j !== undefined && j !== i)
    collisions.push(`[${i}] offers "${d}" as a decoy, but it is [${j}]'s answer`);
}));
check(!collisions.length, 'no decoy is another chart\'s answer anywhere in the pool',
  'decoy collisions:\n         ' + collisions.join('\n         '));

/* When one entity dominates a chart, the reveal text has to say why.
 *
 * Tim, 2 Sep: "I think it's good practice to explain the outlier in the trivia
 * bit at the end. Otherwise people won't learn." There is a sharper reason too:
 * a player who names the chart on the first guess never sees a single hint, so
 * anything explained only on rung 4 is invisible to precisely the people who
 * read the chart best. The `why` is the only text every player sees.
 *
 * Naming the entity is a proxy for explaining it, not proof, but it is
 * mechanical and it caught seven puzzles the first time it was run. */
const leader = (q) => {
  if (q.type === 'slope' || !Array.isArray(q.data)) return null;
  let rows;
  if (q.type === 'dumbbell') rows = q.data.map(d => [d[0], d[2]]);
  else if (q.type === 'deviation') rows = q.data.map(d => [d[0], Math.abs(d[1] - (q.reference || 0))]);
  else rows = q.data.map(d => [d[0], d[1]]);
  rows = rows.filter(r => !/^rest of/i.test(r[0])).sort((x, y) => y[1] - x[1]);
  if (rows.length < 3 || !rows[1][1]) return null;
  return { name: rows[0][0], ratio: rows[0][1] / rows[1][1] };
};
const unexplained = [];
P.forEach((q, i) => {
  const L = leader(q);
  if (!L || L.ratio < 1.6) return;
  if (!(q.why || '').toLowerCase().includes(L.name.toLowerCase()))
    unexplained.push(`[${i}] ${L.name} is ${L.ratio.toFixed(1)}x the next but the reveal never names it`
      + ` (${q.truth.slice(0, 38)})`);
});
check(!unexplained.length, 'every dominant outlier is explained in the reveal',
  'unexplained outliers:\n         ' + unexplained.join('\n         '));

console.log('\n=== DEALER ===');
const a = Array.from({ length: 60 }, (_, i) => dealRun(i + 1).join(','));
const b = Array.from({ length: 60 }, (_, i) => dealRun(i + 1).join(','));
check(a.join('|') === b.join('|'), 'the deal is deterministic across 60 runs', 'the deal is not deterministic');

let sizeBad = 0, diffBad = 0, costs = [];
for (let n = 1; n <= 40; n++) {
  const r = dealRun(n);
  if (r.length !== Math.min(RUN_SIZE, P.length)) sizeBad++;
  for (let i = 1; i < r.length; i++) if (P[r[i]].diff < P[r[i - 1]].diff) diffBad++;
  costs.push(runCost(r));
}
check(!sizeBad, 'every run deals five charts', `${sizeBad} runs dealt the wrong number of charts`);
/* Form variety and difficulty shape are different failures and were being
 * reported as one number. Zero-cost runs fell from 39/40 to 33/40 as the pool
 * grew, which looked like a variety regression; it was not. Split them. */
let adjacent = 0, tripled = 0, hardOpen = 0, easyClose = 0;
for (let n = 1; n <= 200; n++) {
  const r = dealRun(n).map(i => P[i]);
  for (let k = 1; k < r.length; k++) if (r[k].type === r[k - 1].type) adjacent++;
  const c = {};
  r.forEach(p => { c[p.type] = (c[p.type] || 0) + 1; });
  Object.values(c).forEach(v => { if (v >= 3) tripled++; });
  if (r[0].diff > 2) hardOpen++;
  if (r[r.length - 1].diff < 4) easyClose++;
}
/* Doc 23 makes form variety best-effort by design: the dealer tries 240 seeded
 * draws per run and keeps the cheapest, but coverage and the difficulty ramp
 * come first. A stray pair in a thousand neighbours is not worth blocking a
 * ship over; a systematic breakdown is. */
const pairs = 200 * (RUN_SIZE - 1);
if (!adjacent && !tripled) pass('form variety: no run repeats a form back to back');
else if (adjacent / pairs < 0.02 && !tripled)
  warn(`form variety: ${adjacent} adjacent same-form pair(s) in ${pairs} neighbours`
    + ' (best effort, per doc 23)');
else check(false, 'form variety',
  `${adjacent} adjacent pairs and ${tripled} forms appearing three times in 200 runs`);

/* Only five categorical colours exist and a line chart has nothing else to tell
 * its series apart, so a sixth line is either invisible or a duplicate colour. */
const overSeries = P.map((q, i) => [i, q])
  .filter(([, q]) => q.type === 'line' && (q.series || []).length > 5)
  .map(([i, q]) => `[${i}] ${q.series.length} series: ${q.truth.slice(0, 40)}`);
check(!overSeries.length, 'no line chart has more series than the palette has colours',
  'too many series:\n         ' + overSeries.join('\n         '));

const easy = P.filter(p => p.diff <= 2).length;
if (!hardOpen && !easyClose) pass('every run opens easy and closes hard');
else warn(`${hardOpen}/200 runs open above difficulty 2 and ${easyClose}/200 close below 4.\n`
  + `         Only ${easy} of ${P.length} puzzles are difficulty 2 or less, so the dealer\n`
  + '         runs out of gentle openers. Future batches need easier charts.');

/* The frozen history must still resolve. doc 25 */
check(HISTORY.length && HISTORY.every(r => r.length === RUN_SIZE),
  `broadcast history intact: ${HISTORY.length} runs frozen`,
  'a run in HISTORY_SLUGS no longer resolves; a puzzle was renamed or removed');

console.log('\n=== RUNWAY ===');
const seen = new Set();
let lastFresh = 0;
for (let n = 1; n <= 400; n++) {
  const r = dealRun(n);
  const fresh = r.filter(i => !seen.has(i)).length;
  r.forEach(i => seen.add(i));
  if (fresh >= NEW_PER_RUN) lastFresh = n;
  if (seen.size === P.length && n > lastFresh) break;
}
const today = Math.floor((Date.now() - new Date(2026, 7, 26).getTime()) / 86400000) + 1;
const left = lastFresh - today;
console.log(`  run ${lastFresh} is the last with ${NEW_PER_RUN} new charts (today is run ${today})`);
if (left < 0) fail(`fresh material ran out ${-left} days ago; every chart is now a repeat`);
else if (left < 7) warn(`only ${left} days of fresh material left. Build the next batch now.`);
else pass(`${left} days of fresh material remain`);

console.log('');
if (failures) { console.log(`FAILED: ${failures} problem(s), ${warnings} warning(s). Do not ship.`); process.exit(1); }
console.log(`Passed with ${warnings} warning(s).`);
