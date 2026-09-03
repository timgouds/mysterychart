#!/usr/bin/env python3
"""Eurostat (JSON-stat) and OECD (labelled CSV) fetchers.

Doc 22: Eurostat JSON-stat cannot be read from a summary. Asked for a table it
returned smoothly ascending numbers that were entirely wrong. So this decodes
the cube properly: it reads dimension.<id>.category.index, works out the
row-major strides itself, and looks each cell up by its computed offset.

Doc 21/25: OECD csvfilewithlabels is gzip, not binary. curl --compressed reads
it, which makes the dimension-index decoder unnecessary.
"""
import json, subprocess, os, itertools

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE, exist_ok=True)


def _get(url, name):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        subprocess.run(['curl', '-s', '--compressed', '-m', '120', url, '-o', p], check=True)
    return open(p, encoding='utf-8', errors='replace').read()


# ----------------------------------------------------------------- Eurostat
EU_BASE = ('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
           '%s?format=JSON&lang=EN%s')


def eurostat(code, **filters):
    """Return {(dim=cat, ...): value} with every dimension resolved by label."""
    q = ''.join('&%s=%s' % (k, v) for k, v in filters.items())
    key = 'eu_%s_%s.json' % (code, abs(hash(q)) % 10 ** 8)
    d = json.loads(_get(EU_BASE % (code, q), key))
    if 'value' not in d:
        raise RuntimeError(code + ': ' + str(d)[:200])

    ids, size = d['id'], d['size']
    # row-major strides, last dimension fastest
    strides = [1] * len(size)
    for i in range(len(size) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]

    cats = []
    for dim in ids:
        c = d['dimension'][dim]['category']
        inv = {v: k for k, v in c['index'].items()}
        labels = c.get('label', {})
        cats.append([(inv[i], labels.get(inv[i], inv[i])) for i in range(len(inv))])

    out = {}
    for combo in itertools.product(*[range(n) for n in size]):
        off = sum(combo[i] * strides[i] for i in range(len(size)))
        v = d['value'].get(str(off))
        if v is None:
            continue
        out[tuple(cats[i][combo[i]] for i in range(len(size)))] = v
    return out, ids


def eu_geo(code, **filters):
    """Collapse to {country label: value}, once the other dims are pinned."""
    data, ids = eurostat(code, **filters)
    gi = ids.index('geo')
    out = {}
    for keyv, v in data.items():
        out[keyv[gi][1]] = v
    return out


# --------------------------------------------------------------------- OECD
def oecd(agency, flow, version='1.0', filt='all', extra=''):
    url = ('https://sdmx.oecd.org/public/rest/data/%s,%s,%s/%s'
           '?format=csvfilewithlabels%s' % (agency, flow, version, filt, extra))
    name = 'oecd_%s_%s.csv' % (flow.replace('@', '_'), abs(hash(filt + extra)) % 10 ** 6)
    return _get(url, name)


if __name__ == '__main__':
    import sys, csv, io
    if sys.argv[1] == 'eu':
        g = eu_geo(*sys.argv[2:3], **dict(a.split('=') for a in sys.argv[3:]))
        for k, v in sorted(g.items(), key=lambda x: -x[1]):
            print('%-40s %s' % (k, v))
