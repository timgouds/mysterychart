"""Strict fetchers for batch builders from batch 9 on.

The explorers used while screening collapse a dataset to {country: value} and,
when a dataset has more than one combination of its other dimensions, keep
whichever value arrived last. That is fine for a glance and wrong for a chart.
Everything here pins every dimension and fails if more than one value survives
for a country and year, so a filter that is too loose stops the build instead
of quietly drawing the wrong series.
"""
import csv, io, json, subprocess, sys, time, os
import eu, wb
from common import nm

# Eurostat and OECD spell some names differently from the rest of the pool.
RENAME = {'Türkiye': 'Turkey', 'Slovak Republic': 'Slovakia', 'Korea': 'South Korea',
          'Czech Republic': 'Czechia', 'Germany (until 1990 former territory of the FRG)': 'Germany'}
SKIP = ('European Union', 'Euro area', 'Germany including former GDR', 'Metropolitan France',
        'Kosovo', 'OECD', 'DAC', 'G7', 'EU27', 'EA20', 'EU28')


def name(s):
    s = RENAME.get(s, s)
    return nm(s)


def keep(s):
    return not any(k in s for k in SKIP)


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def eurostat(code, years, geo_dim='geo', **pin):
    """{country: {year: value}} with every non-geo, non-time dimension pinned.

    A few datasets key countries on something other than geo (maritime uses
    rep_mar, which also lists ports and regions); only two-letter country codes
    are kept from those."""
    data, ids = eu.eurostat(code, **pin)
    gi, ti = ids.index(geo_dim), ids.index('time')
    if geo_dim != 'geo':
        data = {k: v for k, v in data.items() if len(k[gi][0]) == 2}
    free = [ids[i] for i in range(len(ids)) if i not in (gi, ti)
            and len({k[i][0] for k in data}) > 1]
    if free:
        die('%s: dimensions not pinned: %s' % (code, free))
    out = {}
    for k, v in data.items():
        g, t = k[gi][1], k[ti][0]
        if not keep(g) or v is None:
            continue
        if years and t not in [str(y) for y in years]:
            continue
        out.setdefault(name(g), {})[t] = float(v)
    return out


def oecd(agency, flow, start, end, **pin):
    """Same contract as eurostat(), from an OECD SDMX flow, with retries."""
    url = ('https://sdmx.oecd.org/public/rest/data/%s,%s,/all?format=csvfilewithlabels'
           '&startPeriod=%s&endPeriod=%s' % (agency, flow, start, end))
    path = os.path.join(eu.CACHE, 'oecd_%s_%s_%s.csv' % (flow.replace('@', '_'), start, end))
    for attempt in range(5):
        if os.path.exists(path) and open(path, encoding='utf-8', errors='replace').read(9) == 'STRUCTURE':
            break
        subprocess.run(['curl', '-s', '--compressed', '-m', '150', url, '-o', path])
        time.sleep(6)
    txt = open(path, encoding='utf-8', errors='replace').read()
    if not txt.startswith('STRUCTURE'):
        die('%s: OECD returned %r' % (flow, txt[:80]))
    rows = list(csv.DictReader(io.StringIO(txt)))
    rows = [r for r in rows if r['OBS_VALUE'] and all(r.get(k) == v for k, v in pin.items())]
    out = {}
    for r in rows:
        area = r.get('Reference area') or r.get('Donor') or r['REF_AREA']
        if not keep(area):
            continue
        c, t = name(area), r['TIME_PERIOD']
        if t in out.get(c, {}):
            die('%s: two values for %s %s; pin more dimensions' % (flow, c, t))
        out.setdefault(c, {})[t] = float(r['OBS_VALUE'])
    return out


def worldbank(code, years):
    s = wb.series(code, years)
    from common import DROP
    out = {}
    for k, v in s.items():
        c = nm(wb.name(k))
        if c in DROP:
            continue
        out[c] = {str(y): float(x) for y, x in v.items()}
    return out


def owid(slug, countries, t0, t1, col=3):
    url = ('https://ourworldindata.org/grapher/%s.csv?csvType=full&country=%s&time=%d..%d'
           % (slug, '~'.join(countries), t0, t1))
    txt = subprocess.run(['curl', '-s', '--compressed', '-m', '90', url],
                         capture_output=True, text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    if len(rows) < 3:
        die('owid %s: %r' % (slug, txt[:80]))
    out = {}
    for r in rows[1:]:
        out.setdefault(r[0], {})[r[2]] = float(r[col])
    return out


def year(d, y, want=None):
    """{country: value} for one year; asserts every wanted country is present."""
    y = str(y)
    if want:
        miss = [c for c in want if y not in d.get(c, {})]
        if miss:
            die('missing %s for %s' % (y, miss))
        return {c: d[c][y] for c in want}
    return {c: v[y] for c, v in d.items() if y in v}


def pair(d, y1, y2, want):
    a, b = year(d, y1, want), year(d, y2, want)
    return {c: (a[c], b[c]) for c in want}


def ranks(values):
    """{country: rank} with 1 the largest. Ties share the better rank."""
    order = sorted(values.items(), key=lambda kv: -kv[1])
    out, prev, r = {}, None, 0
    for i, (c, v) in enumerate(order):
        if v != prev:
            r = i + 1
        out[c], prev = r, v
    return out
