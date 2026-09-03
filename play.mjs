/* Play a review build from the first chart to the results screen, screenshotting
 * each chart on the way.
 *
 * Doc 16: every bug that round was invisible in code review and only appeared
 * when the specific chart was drawn with the specific data. So this drives the
 * real UI rather than calling renderers directly.
 *
 *     node play.mjs review-batch1.html [light|dark] [width]
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const [, , file, theme = 'light', widthArg = '900'] = process.argv;
const width = Number(widthArg);
const OUT = path.join(process.cwd(), 'shots', `${theme}-${width}`);
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width, height: 1500 },
  colorScheme: theme === 'dark' ? 'dark' : 'light',
});
const errs = [];
page.on('console', m => { if (m.type() === 'error' && !/ERR_CERT|goatcounter|gc\.zgo/.test(m.text())) errs.push(m.text()); });
page.on('pageerror', e => errs.push(String(e)));

await page.goto('file://' + path.join(process.cwd(), file));
await page.click('#start');
await page.waitForTimeout(200);

let i = 0, problems = 0;
for (; i < 40; i++) {
  const done = await page.evaluate(() => {
    const r = document.getElementById('results');
    return getComputedStyle(r).display !== 'none' && r.offsetHeight > 0;
  });
  if (done) break;

  await page.waitForTimeout(140);
  const info = await page.evaluate(() => {
    const svg = document.querySelector('#chart svg');
    const q = document.querySelector('.prompt');
    const opts = [...document.querySelectorAll('#options button')].map(b => b.textContent.trim());
    const texts = svg ? [...svg.querySelectorAll('text')].map(t => t.textContent) : [];
    return {
      hasSvg: !!svg,
      h: svg ? svg.getBoundingClientRect().height : 0,
      question: q ? q.textContent.trim().slice(0, 70) : '',
      nOpts: opts.length,
      blank: texts.filter(t => !t || /undefined|NaN|null/.test(t)).length,
      sample: texts.slice(0, 4),
      overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
    };
  });

  const el = await page.$('#chart');
  await el.screenshot({ path: path.join(OUT, `${String(i).padStart(2, '0')}.png`) });

  const flags = [];
  if (!info.hasSvg) flags.push('NO SVG');
  if (info.h < 60) flags.push('CHART ' + Math.round(info.h) + 'px');
  if (info.blank) flags.push(info.blank + ' BAD LABELS');
  if (info.overflow) flags.push('OVERFLOW');
  if (flags.length) problems++;
  console.log(`${String(i).padStart(2)}  ${info.nOpts} opts  ${String(Math.round(info.h)).padStart(4)}px  ` +
    (flags.length ? '⚠ ' + flags.join(', ') : 'ok') + `   ${info.sample.join(' | ').slice(0, 52)}`);

  /* Answer correctly every time, so the walk reaches all twelve charts and
     each reveal (title, source, licence line) is exercised. The redaction bar
     already holds the true title, so no game internals are needed. */
  const right = await page.evaluate(() => {
    /* Options carry the year-stripped `answer`, the redaction bar carries the
       full `truth`, and the two are not always prefixes of each other
       ("... covered by forest, 1992 to 2022" vs "... covered by forest since
       1992"). Score on shared content words instead of matching literally. */
    const truth = document.getElementById('truth').textContent.toLowerCase();
    const words = s => new Set(s.toLowerCase().replace(/[^a-z0-9\s]/g, ' ')
      .split(/\s+/).filter(w => w.length > 3));
    const T = words(truth);
    const btns = [...document.querySelectorAll('#options button')];
    let best = null, bestScore = -1;
    btns.forEach(b => {
      const W = words(b.textContent.replace(/^[A-H][.)\s]*/, ''));
      let s = 0; W.forEach(w => { if (T.has(w)) s++; });
      s = s - (W.size - s) * 0.5;
      if (s > bestScore) { bestScore = s; best = b; }
    });
    (best || btns[0]).click();
    return bestScore > 0;
  });
  if (!right) { console.log('   ⚠ could not match the true option'); problems++; }

  await page.waitForTimeout(140);
  /* The Next button lives in the outcome panel, which is revealed by class
     rather than by the hidden attribute, so wait on real visibility. */
  await page.waitForFunction(() => {
    const n = document.getElementById('next');
    return n && n.offsetParent !== null;
  }, null, { timeout: 4000 }).catch(() => {});
  await page.evaluate(() => {
    const n = document.getElementById('next');
    if (n && n.offsetParent !== null) n.click();
  });
  await page.waitForTimeout(200);
}

console.log(`\ncharts seen: ${i}   problems: ${problems}`);
console.log(errs.length ? 'JS ERRORS:\n' + errs.slice(0, 6).join('\n') : 'no JS errors');
await browser.close();
