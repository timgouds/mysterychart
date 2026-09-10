/*
 * Mystery Chart pre-flight.
 *
 *     node check.mjs
 *
 * Reads src/puzzles.js and runs the mechanical checks from SPEC.md section 7.
 * Exit 1 blocks the ship. Every check here exists because something once got
 * through: a sparse series array, a slope puzzle with no leftYear, a treemap
 * whose largest tile was unlabelled, a first hint that named the answer.
 *
 * What this cannot do is judge a puzzle. The discriminator rule, the
 * population-ranking test and the outlier check all need a reader. This
 * catches the failures that are decidable by code, so that human review is
 * spent on the ones that are not.
 */

import fs from "node:fs";

const src = fs.readFileSync("src/puzzles.js", "utf8");
const PUZZLES = new Function(src + "\n;return PUZZLES;")();

const problems = [];
const warnings = [];
const fail = (p, i, msg) => problems.push(`#${i} ${p.slug || p.truth || "?"}: ${msg}`);
const warn = (p, i, msg) => warnings.push(`#${i} ${p.slug || p.truth || "?"}: ${msg}`);

/* Fields every puzzle needs, then the extras each form needs on top. */
const REQUIRED = ["family", "form", "type", "diff", "truth", "period", "answer", "decoys", "hints", "why", "slug"];
const PER_FORM = {
  treemap: ["data", "total"],
  dumbbell: ["data", "leftYear", "rightYear"],
  slope: ["ranks", "leftYear", "rightYear"],
  line: ["series", "startYear"],
  beeswarm: ["data", "label"],
  lollipop: ["data"],
  deviation: ["data"],
  symbol: ["data"]
};

const STOPWORDS = new Set(
  ("the a an of in on at to for per and or by with from as is are was were that this " +
   "who which their its it not more most least than every each any all some one two " +
   "share number rate people population country countries year years total average " +
   "world other others").split(" ")
);

const words = (s) =>
  String(s).toLowerCase().replace(/[^a-z\s]/g, " ").split(/\s+/)
    .filter((w) => w.length > 3 && !STOPWORDS.has(w))
    .map((w) => w.replace(/(ies|es|s)$/, ""));

/* Every answer in the pool, so a decoy that is another puzzle's answer is caught. */
const answers = new Map();
PUZZLES.forEach((p, i) => answers.set(String(p.answer).trim().toLowerCase(), i));

const slugs = new Map();

PUZZLES.forEach((p, i) => {
  REQUIRED.forEach((f) => {
    if (p[f] === undefined || p[f] === null || p[f] === "") fail(p, i, `missing ${f}`);
  });
  (PER_FORM[p.type] || []).forEach((f) => {
    if (p[f] === undefined) fail(p, i, `${p.type} needs ${f}`);
  });
  if (!(p.diff >= 1 && p.diff <= 5)) fail(p, i, `diff out of range: ${p.diff}`);

  /* Decoys. Four is the current target: three shown, one spare for review.
     Seven is the legacy count and is fine, just wasteful to write. */
  const d = Array.isArray(p.decoys) ? p.decoys : [];
  if (d.length < 4) fail(p, i, `${d.length} decoys, need at least 4`);

  const options = [p.answer, ...d].map((o) => String(o).trim().toLowerCase());
  const seen = new Set();
  options.forEach((o) => {
    if (seen.has(o)) fail(p, i, `duplicate option: ${o}`);
    seen.add(o);
  });
  /* A decoy that is another puzzle's answer is only fatal if the two can share
     a run, which the dealer decides. Outside that it is a soft collision: a
     player who has met the other chart may recognise the option. Warn. */
  d.forEach((x) => {
    const hit = answers.get(String(x).trim().toLowerCase());
    if (hit !== undefined && hit !== i) warn(p, i, `decoy is puzzle #${hit}'s answer: ${x}`);
  });

  /* Hints. */
  const h = Array.isArray(p.hints) ? p.hints : [];
  if (h.length !== 4) fail(p, i, `${h.length} hints, need 4`);
  const answerWords = new Set(words(p.answer));
  words(h[0]).forEach((w) => {
    if (answerWords.has(w)) fail(p, i, `hint 1 leaks "${w}" from the answer`);
  });

  /* House style: no em-dashes in anything a player reads. */
  [p.answer, p.truth, p.why, ...d, ...h].forEach((s) => {
    if (typeof s === "string" && s.includes("\u2014")) fail(p, i, "em-dash in player-facing text");
  });

  /* Slugs identify a puzzle in the dealer's history and in analytics, so a
     duplicate silently merges two charts. */
  if (slugs.has(p.slug)) fail(p, i, `slug already used by #${slugs.get(p.slug)}`);
  slugs.set(p.slug, i);

  /* Attribution. Anything without a source falls back to an OWID credit, which
     is a misattribution for the 79 puzzles that are not OWID. */
  if (p.source && !p.sourceUrl) fail(p, i, "source without sourceUrl");

  /* Form-specific data shapes. */
  if (p.type === "treemap" && Array.isArray(p.data)) {
    const vals = p.data.map((r) => r[1]);
    for (let k = 1; k < vals.length; k++) {
      if (vals[k] > vals[k - 1]) { fail(p, i, "treemap not sorted descending; layout will squash a tile"); break; }
    }
    const sum = vals.reduce((a, b) => a + b, 0);
    if (p.total && sum > p.total * 1.001) fail(p, i, `treemap parts (${sum.toFixed(1)}) exceed total (${p.total})`);
  }

  if (p.type === "beeswarm" && Array.isArray(p.data)) {
    const names = new Set(p.data.map((r) => r[0]));
    new Set([].concat(p.label || [], p.labelSm || [])).forEach((n) => {
      if (!names.has(n)) fail(p, i, `beeswarm labels "${n}", which is not in the data`);
    });
  }

  if (p.type === "line" && Array.isArray(p.series)) {
    p.series.forEach((s) => {
      const v = s.values || s[1];
      if (Array.isArray(v)) {
        for (let k = 0; k < v.length; k++) {
          if (v[k] === undefined) { fail(p, i, "sparse array in a line series"); break; }
        }
      }
    });
  }

  /* Not fatal, but the two standing biases from SPEC.md section 9. */
  if (!/[\u2013\u2192-]/.test(String(p.period))) warn(p, i, "snapshot, not a period");
  if (p.type === "lollipop") warn(p, i, "lollipop");
});

/* Report. */
const forms = {};
PUZZLES.forEach((p) => (forms[p.type] = (forms[p.type] || 0) + 1));

console.log(`check.mjs — ${PUZZLES.length} puzzles`);
console.log("  forms        ", Object.entries(forms).map(([k, v]) => `${k} ${v}`).join(", "));
console.log(`  snapshots    ${warnings.filter((w) => w.endsWith("snapshot, not a period")).length} of ${PUZZLES.length}`);
console.log(`  lollipops    ${warnings.filter((w) => w.endsWith("lollipop")).length} of ${PUZZLES.length}`);

const collisions = warnings.filter((w) => w.includes("'s answer:"));
if (collisions.length) {
  console.log(`\n  ${collisions.length} decoy collision${collisions.length === 1 ? "" : "s"} with another puzzle's answer:`);
  collisions.forEach((w) => console.log("    " + w));
}

if (problems.length) {
  console.log(`\n  ${problems.length} problem${problems.length === 1 ? "" : "s"}:`);
  problems.forEach((p) => console.log("    " + p));
  process.exit(1);
}
console.log("\n  all checks pass");
