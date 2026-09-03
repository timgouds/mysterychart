#!/usr/bin/env python3
"""World Bank indicator fetch + screen.

Doc 22: "World Bank is reliable when asked for a named list of countries, or
for every non-null row. Asking for 'the top N' invites an invented ordering."
So we always pull every row and do the ordering here, in code.

Aggregates come mixed in with countries and must be filtered out; the API
marks them by giving them a region of 'NA' in the country endpoint, so we
fetch the country list once and keep only real ones.
"""
import json, subprocess, os, functools

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE, exist_ok=True)


def get(url, name):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        subprocess.run(['curl', '-s', '--compressed', '-m', '120', url, '-o', p],
                       check=True)
    return open(p, encoding='utf-8').read()


@functools.lru_cache(1)
def real_countries():
    """ISO3 -> name, aggregates excluded."""
    out = {}
    for page in (1, 2):
        d = json.loads(get(
            'https://api.worldbank.org/v2/country?format=json&per_page=300&page=%d' % page,
            'countries_%d.json' % page))
        for c in d[1]:
            if c['region']['id'] != 'NA':
                out[c['id']] = c['name']
    return out


def series(code, years):
    """{iso3: {year: value}} for real countries only."""
    date = '%d:%d' % (min(years), max(years)) if len(years) > 1 else str(years[0])
    txt = get('https://api.worldbank.org/v2/country/all/indicator/%s'
              '?format=json&per_page=20000&date=%s' % (code, date),
              'wb_%s_%s.json' % (code.replace('.', '_'), date.replace(':', '-')))
    d = json.loads(txt)
    if len(d) < 2 or not d[1]:
        return {}
    ok = real_countries()
    out = {}
    for r in d[1]:
        iso, v = r['countryiso3code'], r['value']
        if iso in ok and v is not None:
            out.setdefault(iso, {})[int(r['date'])] = v
    return out


def name(iso):
    return real_countries().get(iso, iso)


def pair(code, y1, y2, minc=40):
    """Countries having BOTH years. Returns sorted [(name, v1, v2)]."""
    s = series(code, [y1, y2])
    rows = [(name(k), v[y1], v[y2]) for k, v in s.items() if y1 in v and y2 in v]
    return sorted(rows, key=lambda r: -r[2])


def snap(code, y):
    s = series(code, [y])
    return sorted([(name(k), v[y]) for k, v in s.items() if y in v], key=lambda r: -r[1])
