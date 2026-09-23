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
  from('  /* Four options on every chart.', '  /* Points fall with every mistake');
vm.createContext(sandbox);
vm.runInContext(code + '\nthis.P = PUZZLES; this.dealRun = dealRun; this.runCost = runCost;'
  + ' this.HISTORY = HISTORY; this.clash = clash; this.SHOWN_DECOYS = SHOWN_DECOYS;'
  + ' this.OPTION_COUNT = OPTION_COUNT; this.FRESH_PER_RUN = FRESH_PER_RUN;'
  + ' this.LAST_AIRED_RUN = LAST_AIRED_RUN; this.lastFreshRun = lastFreshRun;', sandbox);
const { P, dealRun, runCost, HISTORY, clash, SHOWN_DECOYS, OPTION_COUNT,
        FRESH_PER_RUN, LAST_AIRED_RUN, lastFreshRun } = sandbox;

const RUN_SIZE = 5;
const [LY, LM, LD] = html.match(/var LAUNCH = new Date\((\d+), (\d+), (\d+)\)/).slice(1).map(Number);
const LAUNCH = new Date(LY, LM, LD);
const dayMs = 86400000;
const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
const today = Math.round((startOfDay(new Date()) - LAUNCH) / dayMs) + 1;
const dateOf = (n) => new Date(LY, LM, LD + n - 1)
  .toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
/* Everything the pool can actually deal without repeating a chart. Dealer
 * quality is measured over this span: past it, runs come from the emergency
 * path and preflight has already failed. */
const lastFresh = lastFreshRun();
const horizon = Math.max(lastFresh, today + 7);
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
  /* Four, not seven. Only SHOWN_DECOYS (3) are ever rendered, so decoys 5 to 7
     were written for every puzzle and seen by nobody. Four leaves one spare for
     one rejected at review and degrades safely if the option ramp widens. The
     original 134 still carry seven; both pass. */
  if (!Array.isArray(q.decoys) || q.decoys.length < 4) bad.push(id + `: ${q.decoys ? q.decoys.length : 0} decoys, want at least 4`);
  if (!Array.isArray(q.hints) || q.hints.length !== 4) bad.push(id + `: ${q.hints ? q.hints.length : 0} hints, want 4`);
  const opts = [q.truth].concat(q.decoys || []);
  if (new Set(opts).size !== opts.length) bad.push(id + ': an option is duplicated');
  (NEEDS[q.type] || []).forEach(f => {
    if (q[f] === undefined || q[f] === null) bad.push(id + `: ${q.type} needs ${f}`);   /* doc 23 */
  });
  if (Array.isArray(q.series) && q.series.some(s => (s.values || s).some?.(v => v === undefined)))
    bad.push(id + ': sparse array in series');                                          /* doc 20 */
});
check(!bad.length, `all ${P.length} puzzles carry their required fields`, 'field problems:\n         ' + bad.join('\n         '));

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

/* One chart's answer offered as a wrong option on another.
 *
 * This used to fail the build. It should not, and the reason is arithmetic:
 * there are seven decoys for every answer, so a pool-wide ban lets throwaway
 * wrong options retire subjects roughly seven times faster than answers can
 * use them, and the retiring is done by the least considered text in the file.
 * Five of twelve candidates for batch seven were blocked that way, by lines
 * nobody had reviewed as answers.
 *
 * The harm it was guarding against is real but narrow: seeing the same sentence
 * twice in one sitting, right on one chart and wrong on another. That depends on
 * the deal, not the pool, so the dealer now prices it in runCost and keeps such
 * pairs apart. What is left here is a report, not a gate. A clash sitting past
 * SHOWN_DECOYS is invisible to players and free; one inside it is worth either
 * demoting into the unshown tail or leaving to the dealer to route around. */
const answersOf = (q) => [q.truth, q.answer].filter(Boolean);
const answerIndex = new Map();
P.forEach((q, i) => answersOf(q).forEach(a => answerIndex.set(a.toLowerCase().trim(), i)));
const shownClash = [], dark = [];
P.forEach((q, i) => (q.decoys || []).forEach((d, k) => {
  const j = answerIndex.get(String(d).toLowerCase().trim());
  if (j === undefined || j === i) return;
  (k < SHOWN_DECOYS ? shownClash : dark).push(
    `[${i}] decoy ${k} "${String(d).slice(0, 44)}" is [${j}]'s answer`);
}));
if (!shownClash.length) pass(`no shown decoy repeats another chart's answer (${dark.length} in the unshown tail)`);
else warn(`${shownClash.length} shown decoys repeat another chart's answer, ${dark.length} more in the tail:`
  + '\n         ' + shownClash.join('\n         '));

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

/* Every country a reveal or hint places on the chart must be on the chart.
 *
 * Seventeen puzzles shipped with reveals or discriminator hints built on
 * countries that were not drawn: "Italy at 12" on a chart with no Italy, "the
 * presence of Norway" on a chart with no Norway, and the reverse, "France and
 * Italy are absent" on a chart showing both. A player who checks the chart
 * against the explanation finds the explanation wrong. SPEC section 7, item 11.
 *
 * Absence is read from grammar, not from a keyword anywhere in the sentence: a
 * list of names directly followed by "absent", "missing", "nowhere", "escape"
 * or a bare "are not", or directly preceded by "absence of", "missing:" or
 * "without". Names in such a list must not be drawn; every other name must be.
 * A clause that supposes a different chart ("rice would put...") is skipped.
 * It cannot resolve pronouns ("both are absent"), so it is a net, not a proof.
 *
 * ENTITY_OK holds mentions reviewed as deliberate: a country named as the
 * origin of something, or on a different chart being compared. Add to it only
 * after reading the sentence. */
const ENTITY_OK = new Set([
  'cocoa-bean-production/why/Vietnam',          // coffee's leaders, by comparison
  'remittances-received/hint 4/Spain',          // where the builder works
  'remittances-sent/why/Belgium',               // where Luxembourg's commuters live
  'pig-livestock-count-heads/hint 4/India',     // "in India's case"
  'potato-production/hint 4/Ireland',           // the famine
  'eu-rail-freight/why/Netherlands',            // "which handles ... and is absent"
  'eu-rail-freight/why/Spain',                  // "one of the largest ... and absent here"
  'apple-production/why/Brazil',                // "Brazil, Indonesia and the rest of the tropics are absent"
  'apple-production/why/Indonesia',
  'life-expectancy-ranking/hint 4/United States', // "nowhere near it", and not drawn
]);
const entityProblems = (() => {
  const labels = (q) => {
    const out = [];
    [q.data, q.ranks, q.series].forEach(rows => (Array.isArray(rows) ? rows : []).forEach(r => {
      if (Array.isArray(r) && typeof r[0] === 'string') out.push(r[0]);
      else if (r && typeof r === 'object' && typeof (r.name || r.label) === 'string') out.push(r.name || r.label);
    }));
    return out;
  };
  const ALIAS = { Britain: 'United Kingdom', America: 'United States', UAE: 'United Arab Emirates' };
  const names = new Set([...Object.keys(ALIAS), ...Object.values(ALIAS)]);
  P.forEach(q => labels(q).forEach(n => { if (/^[A-Z]/.test(n) && !/\d|^Rest of/i.test(n)) names.add(n); }));
  const byLength = [...names].sort((x, y) => y.length - x.length);
  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const NOT_A_COUNTRY = /\b(New Mexico|Gulf of Guinea|Papua New Guinea|(Latin|North|South|Central) America|New South Wales)\b/g;
  const NAME = '(?:the )?(?:' + byLength.map(esc).join('|') + ')';
  const LIST = NAME + '(?:(?:, | and | or | nor )' + NAME + ')*';
  const AFTER = new RegExp('(' + LIST + ')(?:, which [^,.;]*,)?\\s+(?:(?:is|are|was|were|do|does)\\s+)?'
    + '(?:(?:all|both|each|also|entirely|altogether|largely)\\s+)?'
    + '(?:absent|missing|nowhere(?! near)|appear nowhere|escape|not(?=[.,;]|$| (?:on|here|there|appear|present|at all|is)\\b))', 'g');
  const BEFORE = new RegExp('(?:absence of|missing:|absent:|without)\\s+(' + LIST + ')', 'g');
  const HYPOTHETICAL = /\b(would|could|if)\b/i;
  const out = [];
  P.forEach((q, i) => {
    const on = new Set(labels(q));
    const drawn = (n) => on.has(n) || on.has(ALIAS[n]) ||
      Object.keys(ALIAS).some(a => ALIAS[a] === n && on.has(a));
    const namesIn = (t) => {
      const found = []; let s = t;
      byLength.forEach(n => {
        const re = new RegExp('\\b' + esc(n) + '\\b', 'g');
        if (re.test(s)) { found.push(n); s = s.replace(re, ' '); }
      });
      return found;
    };
    const ok = (n, where) => ENTITY_OK.has(q.slug + '/' + where + '/' + n);
    [['why', q.why], ...(q.hints || []).map((h, k) => ['hint ' + (k + 1), h])].forEach(([where, text]) => {
      (text || '').split(/(?<=[.;!?])\s+|;\s*|,? (?:while|whereas) /).forEach(raw => {
        if (!raw || HYPOTHETICAL.test(raw)) return;
        let clause = raw.replace(NOT_A_COUNTRY, ' ');
        const absent = [];
        [AFTER, BEFORE].forEach(re => {
          clause = clause.replace(re, (m, list) => { absent.push(...namesIn(list)); return m.replace(list, ' '); });
        });
        absent.forEach(n => { if (drawn(n) && !ok(n, where)) out.push(`[${i}] ${q.slug} ${where}: calls ${n} absent, but it is on the chart`); });
        namesIn(clause).forEach(n => { if (!drawn(n) && !ok(n, where)) out.push(`[${i}] ${q.slug} ${where}: names ${n}, which is not on the chart`); });
      });
    });
  });
  return out;
})();
check(!entityProblems.length, 'every country a reveal or hint places on a chart is on it',
  'reveal or hint contradicts the chart:\n         ' + entityProblems.join('\n         '));

console.log('\n=== DEALER ===');
check(FRESH_PER_RUN === RUN_SIZE, `every new run takes all ${RUN_SIZE} charts from the unseen queue`,
  `FRESH_PER_RUN is ${FRESH_PER_RUN}; the no-recycling rule needs ${RUN_SIZE}`);
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
const firstNew = LAST_AIRED_RUN + 1, span = Math.max(0, lastFresh - LAST_AIRED_RUN);
for (let n = firstNew; n <= lastFresh; n++) {
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
const pairs = Math.max(1, span * (RUN_SIZE - 1));
const spanTxt = `runs ${firstNew}-${lastFresh}`;
if (!adjacent && !tripled) pass(`form variety: no run repeats a form back to back (${spanTxt})`);
else if (adjacent / pairs < 0.02 && !tripled)
  warn(`form variety: ${adjacent} adjacent same-form pair(s) in ${pairs} neighbours`
    + ' (best effort, per doc 23)');
else check(false, 'form variety',
  `${adjacent} adjacent pairs and ${tripled} forms appearing three times in ${spanTxt}`);

/* The dealer is now the thing standing between a player and the same sentence
 * twice in one sitting, so it has to be measured rather than assumed. Unlike
 * form variety this is a fairness property, so a single leak is reported by
 * name: with only 240 seeded draws per run the dealer can be cornered, and if
 * it ever is, the fix is to demote the offending decoy into the unshown tail. */
const met = [];
for (let n = 1; n <= horizon; n++) {
  const r = dealRun(n);
  for (let i = 0; i < r.length; i++)
    for (let j = i + 1; j < r.length; j++)
      if (clash(r[i], r[j])) met.push(`run ${n}: [${r[i]}] and [${r[j]}]`);
}
check(!met.length, `no run puts a chart beside another that offers its answer as a decoy (runs 1-${horizon})`,
  'clashing pairs dealt together:\n         ' + met.slice(0, 8).join('\n         '));

check(OPTION_COUNT.length === RUN_SIZE && OPTION_COUNT.every(n => n === 4),
  `every chart offers ${OPTION_COUNT[0]} options, so ${SHOWN_DECOYS} decoys are shown`,
  `option counts are ${OPTION_COUNT.join(',')}, expected five fours`);

/* Only five categorical colours exist and a line chart has nothing else to tell
 * its series apart, so a sixth line is either invisible or a duplicate colour. */
const overSeries = P.map((q, i) => [i, q])
  .filter(([, q]) => q.type === 'line' && (q.series || []).length > 5)
  .map(([i, q]) => `[${i}] ${q.series.length} series: ${q.truth.slice(0, 40)}`);
check(!overSeries.length, 'no line chart has more series than the palette has colours',
  'too many series:\n         ' + overSeries.join('\n         '));

/* Without recycling the dealer can only balance runs out of what the unseen
 * queue holds, so a shortage of gentle openers is a batch problem, not a
 * dealer one: each weekly batch needs one diff 1-2 chart per run. */
if (!hardOpen && !easyClose) pass(`every run opens easy and closes hard (${spanTxt})`);
else warn(`${hardOpen}/${span} runs open above difficulty 2 and ${easyClose}/${span} close below 4 (${spanTxt}).\n`
  + '         The unseen queue is short of gentle openers or hard closers; the next batch\n'
  + '         should carry at least one diff 1-2 chart per run.');

/* The frozen history must still resolve. doc 25 */
check(HISTORY.length === LAST_AIRED_RUN && HISTORY.every(r => r.length === RUN_SIZE),
  `broadcast history intact: ${HISTORY.length} runs frozen`,
  'a run in HISTORY_SLUGS no longer resolves; a puzzle was renamed or removed');

console.log('\n=== RUNWAY ===');
/* No chart is ever recycled. Every run after the frozen history takes five
 * charts nobody has seen, and the weekly batch has to keep the pool ahead of
 * the calendar. If it falls behind, the dealer fills the gap from the charts
 * unseen longest so the page still plays; that is an emergency, so a run in
 * the coming week that would need it fails the build. */
const everSeen = new Set();
for (let n = 1; n <= LAST_AIRED_RUN; n++) dealRun(n).forEach(i => everSeen.add(i));
const unseenNow = P.length - everSeen.size;
const left = lastFresh - today;
console.log(`  ${unseenNow} charts unseen after run ${LAST_AIRED_RUN}; today is run ${today} (${dateOf(today)})`);
console.log(`  run ${lastFresh} is the last fully fresh run: ${dateOf(lastFresh)}`);
const netRuns = [];
{
  const seenSoFar = new Set();
  for (let n = 1; n <= today + 7; n++) {
    const r = dealRun(n);
    if (n > LAST_AIRED_RUN && n >= today) {
      const reused = r.filter(i => seenSoFar.has(i));
      if (reused.length) netRuns.push(`run ${n} (${dateOf(n)}) repeats ${reused.map(i => P[i].slug).join(', ')}`);
    }
    r.forEach(i => seenSoFar.add(i));
  }
}
check(!netRuns.length, 'no run in the next 7 days needs the emergency path',
  'these runs would repeat a chart:\n         ' + netRuns.join('\n         '));
if (left < 7) fail(`only ${left} days of fresh material left. A batch must ship before this does.`);
else if (left < 14) warn(`${left} days of fresh material left, under two weeks. Build the next batch now.`);
else pass(`${left} days of fresh material remain`);

console.log('');
if (failures) { console.log(`FAILED: ${failures} problem(s), ${warnings} warning(s). Do not ship.`); process.exit(1); }
console.log(`Passed with ${warnings} warning(s).`);
