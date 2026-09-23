#!/usr/bin/env python3
"""Batch 9, part three of three: multi-line charts.

    python3 build11.py --digest
    python3 build11.py > b11.js

Lines are drawn from zero unless a baseline is set, so every value must be
non-negative, and a series with a missing year would render as a gap: both are
asserted. Text lives in text11.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import block, ex
import sources as S

START = 191
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'


def series(d, y0, y1, want, scale=1.0):
    out = []
    for c in want:
        vals = []
        for y in range(y0, y1 + 1):
            v = d.get(c, {}).get(str(y))
            if v is None:
                S.die('line: %s has no value for %d' % (c, y))
            vals.append(v * scale)
        assert min(vals) >= 0, ('lines draw from zero', c, min(vals))
        out.append((c, vals))
    return out


def early_leavers():
    d = S.eurostat('edat_lfse_14', [], sex='T', wstatus='POP', age='Y18-24', unit='PC', freq='A')
    return dict(s=series(d, 2004, 2024, ['Malta', 'Portugal', 'Spain', 'Romania', 'Germany']),
                y0=2004, y1=2024, unit='% of 18 to 24 year olds', suffix='%',
                src='Eurostat', url=ES % 'edat_lfse_14')


def bond_yields():
    d = S.eurostat('irt_lt_mcby_a', [], int_rt='MCBY', freq='A')
    return dict(s=series(d, 2005, 2024, ['Greece', 'Portugal', 'Italy', 'Spain', 'Hungary']),
                y0=2005, y1=2024, unit='% a year', suffix='%', src='Eurostat',
                url=ES % 'irt_lt_mcby_a')


def temp_contracts():
    d = S.eurostat('tesem110', [], wstatus='EMP_TEMP', sex='T', age='Y20-64', unit='PC_SAL', freq='A')
    return dict(s=series(d, 2009, 2024, ['Spain', 'Netherlands', 'Portugal', 'Italy', 'Germany']),
                y0=2009, y1=2024, unit='% of employees aged 20 to 64', suffix='%',
                src='Eurostat', url=ES % 'tesem110')


def space():
    d = S.owid('yearly-number-of-objects-launched-into-outer-space',
               ['USA', 'CHN', 'RUS', 'GBR', 'JPN'], 2000, 2025)
    for c in list(d):   # OWID leaves a year out where the count was zero
        for y in range(2000, 2026):
            d[c].setdefault(str(y), 0.0)
    s = [('Britain' if c == 'United Kingdom' else c, v)   # the full name is clipped at compact width
         for c, v in series(d, 2000, 2025, ['United States', 'China', 'Russia', 'United Kingdom', 'Japan'])]
    return dict(s=s,
                y0=2000, y1=2025, unit='number a year', src='Our World in Data',
                url='https://ourworldindata.org/grapher/yearly-number-of-objects-launched-into-outer-space')


def older_workers():
    d = S.eurostat('lfsa_ergan', [], sex='T', age='Y55-64', citizen='TOTAL', unit='PC', freq='A')
    return dict(s=series(d, 2000, 2024, ['Sweden', 'Germany', 'Italy', 'Poland', 'Slovenia']),
                y0=2000, y1=2024, unit='% of people aged 55 to 64', suffix='%',
                src='Eurostat', url=ES % 'lfsa_ergan')


def divorce():
    d = S.eurostat('demo_ndivind', [], indic_de='GDIVRT', freq='A')
    return dict(s=series(d, 1997, 2017, ['Lithuania', 'Czechia', 'Spain', 'Italy', 'Ireland']),
                y0=1997, y1=2017, unit='per 1,000 residents a year', src='Eurostat',
                url=ES % 'demo_ndivind')


def sex_ratio():
    d = S.worldbank('SP.POP.BRTH.MF', list(range(1990, 2024)))
    return dict(s=series(d, 1990, 2023, ['China', 'Azerbaijan', 'India', 'Vietnam', 'South Korea'], 100),
                y0=1990, y1=2023, unit='per 100', baseline=100, src='World Bank',
                url='https://data.worldbank.org/indicator/SP.POP.BRTH.MF')


ORDER = [('early-school-leavers', early_leavers), ('ten-year-bond-yields', bond_yields),
         ('temporary-contracts', temp_contracts), ('objects-launched-into-space', space),
         ('older-workers-in-work', older_workers), ('divorce-rate', divorce),
         ('boys-born-per-100-girls', sex_ratio)]


def digest(slug, o):
    print('\n%s %d-%d | %s' % (slug, o['y0'], o['y1'], o['unit']))
    for c, v in o['s']:
        n = len(v)
        pick = sorted({0, n // 4, n // 2, 3 * n // 4, n - 1})
        mx = max(range(n), key=lambda i: v[i])
        print('  %-14s %s | max %.1f in %d' % (c, ' '.join('%d:%.1f' % (o['y0'] + i, v[i]) for i in pick),
                                               v[mx], o['y0'] + mx))


def emit(i, slug, o, t):
    period = '%d\u2013%d' % (o['y0'], o['y1'])
    b = dict(family='Change over time', form='Multi-line · %s' % period, exhibit=ex(i), type='line',
             diff=t['diff'], truth=t['answer'] + ', ' + period, period=period, unit=o['unit'],
             startYear=o['y0'], series=o['s'], answer=t['answer'], decoys=t['decoys'],
             hints=t['hints'], why=t['why'], slug=slug, source=o['src'], sourceUrl=o['url'])
    if o.get('suffix'):
        b['suffix'] = o['suffix']
    if o.get('baseline') is not None:
        b['baseline'] = o['baseline']
    return block(b)


if __name__ == '__main__':
    built = [(s, f()) for s, f in ORDER]
    if '--digest' in sys.argv:
        for s, o in built:
            digest(s, o)
        sys.exit()
    from text11 import TEXT
    print(',\n'.join(emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)) + ',')
