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

  /* Work through the options until the chart resolves, so the walk reaches
     every chart and each reveal (title, source, licence line) is exercised.

     This used to read the true title straight out of the redaction bar and
     click the matching option. That stopped working, deliberately: the bar
     now carries a mask until the answer is revealed, because at opacity 0 the
     real title was being lifted by Ctrl+A and read out by screen readers on
     an unanswered puzzle. A harness that can see the answer is the same hole
     a player can see through, so it clicks instead of peeking. */
  const solved = await page.evaluate(async () => {
    const done = () => {
      const n = document.getElementById('next');
      return n && n.offsetParent !== null;
    };
    const btns = () => [...document.querySelectorAll('#options button:not([disabled])')];
    let clicks = 0;
    while (!done() && btns().length && clicks < 10) {
      btns()[0].click();
      clicks++;
      await new Promise(r => setTimeout(r, 120));
    }
    return { resolved: done(), clicks };
  });
  if (!solved.resolved) { console.log('   ⚠ chart never resolved'); problems++; }

  /* The title is only in the page once the bar is off; read it now as a check
     that the reveal actually populated it. */
  const revealed = await page.evaluate(() => {
    const t = document.getElementById('truth');
    return { text: t.textContent, masked: /\u2588/.test(t.textContent),
             aria: t.getAttribute('aria-hidden') };
  });
  if (revealed.masked || !revealed.text.trim() || revealed.aria === 'true') {
    console.log('   ⚠ reveal did not restore the title: ' + JSON.stringify(revealed));
    problems++;
  }

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
