#!/usr/bin/env python3
"""Screen one candidate indicator for puzzle-readiness.

The point of this script is what it does NOT print. Exploring candidates by
fetching them and reading the response puts a few hundred rows of CSV or JSON
into the conversation for every indicator, including the ones that get
rejected. This prints about a dozen lines instead: enough to judge whether
something is puzzle material, and nothing else.

`who.py` already worked this way. This is the same idea for all four sources.

    python3 screen.py wb   SH.MED.BEDS.ZS 2020
    python3 screen.py wb   SP.DYN.LE00.IN 2000 2023     two years: pair mode
    python3 screen.py owid coffee-bean-production 2024
    python3 screen.py owid life-expectancy 1990 2023
    python3 screen.py who  MALARIA_EST_CASES
    python3 screen.py eu   ilc_scp09

Add --bank to append the verdict to bank.tsv, which is the candidate bank
doc 21 asked for and nobody built. Screen twenty things in one cheap pass,
then open a batch session with the bank as the input instead of rediscovering
everything.

The checks are the ones already written down across the docs and applied by
eye until now: the population-ranking test (doc 02), the outlier sanity check
(doc 02), entity continuity across a range (doc 03), and the mixed-reference-
year check (doc 22).
"""
import sys, os, json, subprocess, csv, io, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb
from common import nm, DROP

BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank.tsv')

OWID_AGG = ('World', 'Asia', 'Africa', 'Europe', 'Americas', 'Oceania', 'income',
            'European Union', 'FAO', 'Least developed', 'Land Locked',
            'Small Island', 'Net Food', 'Union', 'G20', 'OECD')


# ----------------------------------------------------------------- fetching
def owid(slug, year):
    url = ('https://ourworldindata.org/grapher/%s.csv?csvType=filtered'
           '&country=~ALL&time=%s' % (slug, year))
    txt = subprocess.run(['curl', '-s', '--compressed', '-m', '90', url],
                         capture_output=True, text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows or rows[0][0].startswith('{') or len(rows) < 3:
        sys.exit('owid %s: no usable rows (%s)' % (slug, txt[:120]))
    out = {}
    for r in rows[1:]:
        if len(r) < 4 or not r[1] or not r[3]:
            continue
        e = nm(r[0])
        if e in DROP or any(a in e for a in OWID_AGG):
            continue
        try:
            out.setdefault(e, {})[int(r[2])] = float(r[3])
        except ValueError:
            continue
    return out


def worldbank(code, years):
    s = wb.series(code, years)
    return {nm(wb.name(k)): v for k, v in s.items() if nm(wb.name(k)) not in DROP}


def who(code):
    url = 'https://ghoapi.azureedge.net/api/' + code
    raw = subprocess.run(['curl', '-s', '--compressed', '-m', '90', url],
                         capture_output=True, text=True).stdout
    rows = json.loads(raw)['value']
    rows = [r for r in rows if r.get('SpatialDimType') == 'COUNTRY']
    if any(r.get('Dim1') == 'BTSX' for r in rows):
        rows = [r for r in rows if r.get('Dim1') == 'BTSX']
    # WHO keys on ISO3. Resolve to display names, or the digest reads as codes
    # and the population test silently matches nothing.
    iso = wb.real_countries()
    out = {}
    for r in rows:
        v, y = r.get('NumericValue'), r.get('TimeDim')
        if v is None or y is None:
            continue
        name = nm(iso.get(r['SpatialDim'], r['SpatialDim']))
        if name in DROP:
            continue
        out.setdefault(name, {})[int(y)] = float(v)
    return out


def eurostat(code):
    import eu
    g = eu.eu_geo(code)
    return {k: {0: float(v)} for k, v in g.items() if v is not None}


# ------------------------------------------------------------------ checks
def spearman(a, b):
    """Rank correlation between two equal-length sequences."""
    def rank(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        r = [0] * len(xs)
        for pos, i in enumerate(order):
            r[i] = pos
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    if n < 3:
        return 0.0
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((x - mb) ** 2 for x in rb))
    return num / (da * db) if da and db else 0.0


_POP = {}


def population(year=2023):
    """Population by display name, cached, for the population-ranking test."""
    if not _POP:
        s = wb.series('SP.POP.TOTL', [year])
        for k, v in s.items():
            if year in v:
                _POP[nm(wb.name(k))] = v[year]
    return _POP


def fmt(v):
    a = abs(v)
    if a >= 1e9:  return '%.1fbn' % (v / 1e9)
    if a >= 1e6:  return '%.1fm' % (v / 1e6)
    if a >= 1e4:  return '%.0fk' % (v / 1e3)
    if a >= 100:  return '%.0f' % v
    if a >= 1:    return '%.1f' % v
    return '%.2f' % v


# ------------------------------------------------------------------- report
def report(src, code, data, years, bank=False):
    """data: {entity: {year: value}}"""
    notes, verdict = [], 'PASS'

    if not data:
        print('%s %s: NO DATA' % (src, code))
        return

    pair = len(years) == 2
    y2 = max(years)
    y1 = min(years)

    have2 = {e: v for e, v in data.items() if y2 in v} if y2 else \
            {e: v for e, v in data.items() if v}
    if not have2:
        # single-year sources (Eurostat collapsed, WHO latest) key on 0 or vary
        allyears = sorted({y for v in data.values() for y in v})
        y2 = allyears[-1] if allyears else 0
        have2 = {e: v for e, v in data.items() if y2 in v}

    rows = sorted(((e, v[y2]) for e, v in have2.items()), key=lambda r: -r[1])
    n = len(rows)

    # --- mixed reference years (doc 22) --------------------------------
    spread = sorted({y for v in data.values() for y in v})
    if not pair and len(spread) > 1:
        notes.append('year spread %d..%d across countries; pin one year'
                     % (spread[0], spread[-1]))

    # --- coverage -------------------------------------------------------
    if n < 25:
        notes.append('only %d countries; thin for a ranking' % n)
        verdict = 'REJECT'

    # --- outlier sanity (doc 02) ---------------------------------------
    ratio = None
    if n >= 3 and rows[1][1]:
        ratio = rows[0][1] / rows[1][1]
        if ratio > 4:
            notes.append('leader is %.1fx the runner-up; check it is real, '
                         'and clip or drop it if drawn' % ratio)

    # --- population-ranking test (doc 02) ------------------------------
    rho = None
    try:
        pop = population()
        common = [(e, v) for e, v in rows if e in pop][:80]
        if len(common) >= 20:
            rho = spearman([v for _, v in common], [pop[e] for e, _ in common])
            if rho > 0.75:
                notes.append('ranking tracks population (rho %.2f); almost any '
                             'metric gives this order' % rho)
                verdict = 'REJECT'
            elif rho > 0.5:
                notes.append('ranking partly tracks population (rho %.2f)' % rho)
    except Exception as e:
        notes.append('population test skipped (%s)' % str(e)[:40])

    # --- entity continuity across a range (doc 03) ---------------------
    missing = []
    if pair:
        top = [e for e, _ in rows[:20]]
        missing = [e for e in top if y1 not in data.get(e, {})]
        if missing:
            notes.append('missing in %d for: %s' % (y1, ', '.join(missing[:6])))
            verdict = 'REJECT' if len(missing) > 3 else verdict

    # --- print ----------------------------------------------------------
    head = '%s %s' % (src, code)
    print('\n' + head)
    print('-' * len(head))
    print('year        : %s' % ('%d vs %d' % (y1, y2) if pair else y2 or 'n/a'))
    print('countries   : %d' % n)
    if ratio:
        print('top/second  : %.2f' % ratio)
    if rho is not None:
        print('pop rank rho: %+.2f' % rho)
    print('top 8       : ' + ', '.join('%s %s' % (e, fmt(v)) for e, v in rows[:8]))
    print('bottom 5    : ' + ', '.join('%s %s' % (e, fmt(v)) for e, v in rows[-5:]))
    if pair:
        movers = [(e, data[e][y2] - data[e][y1]) for e, _ in rows[:40]
                  if y1 in data.get(e, {})]
        movers.sort(key=lambda r: -abs(r[1]))
        print('biggest move: ' + ', '.join('%s %+s' % (e, fmt(d)) for e, d in movers[:5]))
    for m in notes:
        print('  ! ' + m)
    print('VERDICT     : %s' % verdict)

    if bank:
        line = '\t'.join([verdict, src, code,
                          ('%d-%d' % (y1, y2)) if pair else str(y2),
                          str(n),
                          '%+.2f' % rho if rho is not None else '',
                          '%.1f' % ratio if ratio else '',
                          '; '.join('%s %s' % (e, fmt(v)) for e, v in rows[:5]),
                          '; '.join(notes)])
        new = not os.path.exists(BANK)
        with open(BANK, 'a', encoding='utf-8') as fh:
            if new:
                fh.write('verdict\tsource\tcode\tyear\tn\tpop_rho\ttop_ratio\ttop5\tnotes\n')
            fh.write(line + '\n')
        print('  -> appended to bank.tsv')


def main():
    args = [a for a in sys.argv[1:] if a != '--bank']
    bank = '--bank' in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    src, code = args[0], args[1]
    years = [int(a) for a in args[2:] if a.isdigit()]

    if src == 'wb':
        data = worldbank(code, years or [2023])
    elif src == 'owid':
        t = '%d..%d' % (min(years), max(years)) if len(years) == 2 else \
            (str(years[0]) if years else 'latest')
        data = owid(code, t)
    elif src == 'who':
        data = who(code)
        if not years:
            counts = {}
            for v in data.values():
                for y in v:
                    counts[y] = counts.get(y, 0) + 1
            if counts:
                years = [max(counts, key=counts.get)]
    elif src == 'eu':
        data = eurostat(code)
        years = [0]
    else:
        sys.exit('unknown source: %s (wb, owid, who, eu)' % src)

    if not years:
        allyears = sorted({y for v in data.values() for y in v})
        years = [allyears[-1]] if allyears else [0]
    report(src, code, data, years, bank)


if __name__ == '__main__':
    main()
