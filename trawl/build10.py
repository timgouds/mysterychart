#!/usr/bin/env python3
"""Batch 9, part two of three: dumbbells and rank slopes.

    python3 build10.py --digest
    python3 build10.py > b10.js

Text lives in text10.py, written from the digest. Rank slopes rank every
country present in both years and draw a readable selection of them, so a rank
on the chart is a place among all reporting countries, not among those drawn.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import arr, block, ex
import sources as S

START = 178
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'
WB = 'https://data.worldbank.org/indicator/%s'


def dumb(d, y1, y2, want, dec, scale=1.0):
    p = S.pair(d, y1, y2, want)
    rows = sorted(((c, a * scale, b * scale) for c, (a, b) in p.items()), key=lambda r: r[2])
    for r in rows:
        assert r[1] >= 0 and r[2] >= 0, ('dumbbells draw from zero', r)
    return rows


# ----------------------------------------------------------------- dumbbells
def debt():
    d = S.eurostat('gov_10dd_edpt1', [2007, 2024], unit='PC_GDP', sector='S13', na_item='GD', freq='A')
    want = ['Greece', 'Italy', 'France', 'Belgium', 'Spain', 'Portugal', 'Finland', 'Austria',
            'Germany', 'Netherlands', 'Ireland', 'Sweden', 'Denmark', 'Bulgaria', 'Estonia']
    return dict(type='dumbbell', rows=dumb(d, '2007', '2024', want, 1), l=2007, r=2024, dec=1,
                unit='% of GDP', suffix='%', src='Eurostat', url=ES % 'gov_10dd_edpt1')


def part_time():
    d = S.eurostat('lfsa_eppga', [2004, 2024], sex='T', age='Y15-64', unit='PC', freq='A')
    want = ['Netherlands', 'Switzerland', 'Austria', 'Germany', 'Denmark', 'Belgium', 'Norway',
            'Sweden', 'France', 'Italy', 'Spain', 'Poland', 'Greece', 'Romania', 'Bulgaria']
    return dict(type='dumbbell', rows=dumb(d, '2004', '2024', want, 1), l=2004, r=2024, dec=1,
                unit='% of people in work', suffix='%', src='Eurostat', url=ES % 'lfsa_eppga')


def organic():
    d = S.eurostat('sdg_02_40', [2012, 2022], unit='PC_UAA', crops='UAAXK0000', agprdmet='TOTAL', freq='A')
    want = ['Estonia', 'Sweden', 'Portugal', 'Italy', 'Czechia', 'Latvia', 'Finland', 'Denmark',
            'Spain', 'Germany', 'France', 'Netherlands', 'Poland', 'Ireland', 'Bulgaria', 'Malta']
    return dict(type='dumbbell', rows=dumb(d, '2012', '2022', want, 1), l=2012, r=2022, dec=1,
                unit='% of farmland', suffix='%', src='Eurostat', url=ES % 'sdg_02_40')


def accounts():
    d = S.worldbank('FX.OWN.TOTL.ZS', [2011, 2024])
    want = ['India', 'China', 'Kenya', 'Thailand', 'Brazil', 'Turkey', 'Indonesia', 'Mexico',
            'Nigeria', 'Egypt', 'Pakistan', 'Vietnam', 'Philippines', 'Germany']
    return dict(type='dumbbell', rows=dumb(d, '2011', '2024', want, 1), l=2011, r=2024, dec=1,
                unit='% of people aged 15 and over', suffix='%', src='World Bank',
                url=WB % 'FX.OWN.TOTL.ZS')


def women_outlive():
    f = S.worldbank('SP.DYN.LE00.FE.IN', [2000, 2023])
    m = S.worldbank('SP.DYN.LE00.MA.IN', [2000, 2023])
    want = ['Russia', 'Belarus', 'Ukraine', 'Lithuania', 'Latvia', 'Kazakhstan', 'Poland',
            'France', 'Japan', 'United States', 'Germany', 'United Kingdom', 'Sweden',
            'India', 'Bangladesh']
    g = {c: {y: f[c][y] - m[c][y] for y in ('2000', '2023')} for c in want if c in f and c in m}
    return dict(type='dumbbell', rows=dumb(g, '2000', '2023', want, 1), l=2000, r=2023, dec=1,
                unit='years', src='World Bank', url=WB % 'SP.DYN.LE00.FE.IN')


def energy_imports():
    d = S.eurostat('nrg_ind_id', [2004, 2023], siec='TOTAL', unit='PC', freq='A')
    want = ['Malta', 'Cyprus', 'Ireland', 'Italy', 'Belgium', 'Netherlands', 'Lithuania', 'Germany',
            'Spain', 'Poland', 'France', 'Czechia', 'Latvia', 'Sweden', 'Estonia']
    return dict(type='dumbbell', rows=dumb(d, '2004', '2023', want, 1), l=2004, r=2023, dec=1,
                unit='% of energy used', suffix='%', src='Eurostat', url=ES % 'nrg_ind_id')


def household_size():
    d = S.eurostat('ilc_lvph01', [2005, 2024], unit='AVG', freq='A')
    want = ['Slovakia', 'Poland', 'Ireland', 'Spain', 'Cyprus', 'Malta', 'Portugal', 'Greece',
            'Bulgaria', 'Italy', 'Czechia', 'France', 'Netherlands', 'Germany', 'Denmark', 'Finland']
    return dict(type='dumbbell', rows=dumb(d, '2005', '2024', want, 1), l=2005, r=2024, dec=1,
                unit='people', src='Eurostat', url=ES % 'ilc_lvph01')


# -------------------------------------------------------------------- slopes
def slope(d, y1, y2, show, excl=()):
    a, b = S.year(d, y1), S.year(d, y2)
    both = [c for c in a if c in b and c not in excl]
    ra = S.ranks({c: a[c] for c in both})
    rb = S.ranks({c: b[c] for c in both})
    miss = [c for c in show if c not in both]
    if miss:
        S.die('slope: not in both years: %s' % miss)
    rows = sorted(((c, ra[c], rb[c]) for c in show), key=lambda r: r[2])
    vals = {c: (round(a[c], 1), round(b[c], 1)) for c in show}
    return rows, len(both), vals


def tertiary():
    d = S.eurostat('edat_lfse_03', [2004, 2024], sex='T', age='Y25-34', isced11='ED5-8', unit='PC', freq='A')
    show = ['Ireland', 'Luxembourg', 'Cyprus', 'Lithuania', 'Netherlands', 'France', 'Spain',
            'Belgium', 'Portugal', 'Finland', 'Czechia', 'Italy', 'Romania']
    rows, n, v = slope(d, '2004', '2024', show, ('Norway', 'Switzerland', 'Iceland', 'United Kingdom',
                                               'Turkey', 'Serbia', 'North Macedonia', 'Bosnia and Herzegovina', 'Montenegro'))
    return dict(type='slope', rows=rows, n=n, vals=v, l=2004, r=2024,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'edat_lfse_03')


def union():
    d = S.oecd('OECD.ELS.SAE', 'DSD_TUD_CBC@DF_TUD', 2000, 2022)
    show = ['Iceland', 'Sweden', 'Finland', 'Denmark', 'Belgium', 'Norway', 'Italy', 'Ireland',
            'Canada', 'Japan', 'Germany', 'United States', 'France', 'Estonia']
    rows, n, v = slope(d, '2000', '2019', show, ('India', 'Indonesia'))
    return dict(type='slope', rows=rows, n=n, vals=v, l=2000, r=2019,
                unit='rank among OECD countries, highest first', src='OECD',
                url='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_TUD_CBC%40DF_TUD')


def wages():
    d = S.oecd('OECD.ELS.SAE', 'DSD_EARNINGS@AV_AN_WAGE', 2000, 2024, UNIT_MEASURE='USD_PPP', PRICE_BASE='Q')
    show = ['Iceland', 'Luxembourg', 'Switzerland', 'United States', 'Netherlands', 'Germany',
            'Ireland', 'Canada', 'South Korea', 'France', 'Turkey', 'Lithuania', 'Italy',
            'Japan', 'Greece']
    rows, n, v = slope(d, '2000', '2024', show)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2000, r=2024,
                unit='rank among OECD countries, highest first', src='OECD',
                url='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_EARNINGS%40AV_AN_WAGE')


def gender_gap():
    d = S.eurostat('tesem060', [2009, 2024], indic_em='EMP_LFS', age='Y20-64', unit='PC_POP', freq='A')
    show = ['Malta', 'Greece', 'Italy', 'Romania', 'Czechia', 'Poland', 'Ireland', 'Spain',
            'Netherlands', 'Germany', 'France', 'Sweden', 'Lithuania', 'Finland']
    rows, n, v = slope(d, '2009', '2024', show, ('Norway', 'Switzerland', 'Iceland', 'United Kingdom',
                                               'Turkey', 'Serbia', 'North Macedonia', 'Bosnia and Herzegovina', 'Montenegro'))
    return dict(type='slope', rows=rows, n=n, vals=v, l=2009, r=2024,
                unit='rank among EU countries, largest first', src='Eurostat', url=ES % 'tesem060')


def recycling():
    d = S.eurostat('cei_wm011', [2004, 2023], wst_oper='RCY', unit='PC', freq='A')
    show = ['Germany', 'Austria', 'Slovenia', 'Netherlands', 'Belgium', 'Italy', 'Lithuania',
            'Slovakia', 'Denmark', 'Spain', 'France', 'Sweden', 'Poland', 'Greece', 'Romania']
    rows, n, v = slope(d, '2004', '2023', show, ('Norway', 'Switzerland', 'Iceland', 'United Kingdom',
                                               'Turkey', 'Serbia', 'North Macedonia', 'Bosnia and Herzegovina',
                                               'Montenegro', 'Albania'))
    return dict(type='slope', rows=rows, n=n, vals=v, l=2004, r=2023,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'cei_wm011')


def rail():
    pk = S.eurostat('rail_pa_total', [2004, 2023], unit='MIO_PKM', freq='A')
    pop = S.eurostat('demo_pjan', [2004, 2023], sex='T', age='TOTAL', unit='NR', freq='A')
    d = {c: {y: pk[c][y] * 1e6 / pop[c][y] for y in ('2004', '2023')}
         for c in pk if c in pop and all(y in pk[c] and y in pop[c] for y in ('2004', '2023'))}
    show = ['Austria', 'France', 'Sweden', 'Germany', 'Czechia', 'Netherlands', 'Denmark', 'Spain',
            'Italy', 'Finland', 'Slovakia', 'Romania', 'Greece', 'Lithuania']
    rows, n, v = slope(d, '2004', '2023', show, ('Norway', 'Switzerland', 'Turkey', 'Liechtenstein',
                                               'Montenegro', 'North Macedonia', 'Bosnia and Herzegovina'))
    return dict(type='slope', rows=rows, n=n, vals=v, l=2004, r=2023,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'rail_pa_total')


ORDER = [('government-debt', debt), ('part-time-work', part_time), ('organic-farmland', organic),
         ('bank-account-ownership', accounts), ('women-outlive-men', women_outlive),
         ('energy-imported', energy_imports), ('household-size', household_size),
         ('young-graduates-rank', tertiary), ('union-membership-rank', union),
         ('average-wage-rank', wages), ('gender-employment-gap-rank', gender_gap),
         ('recycling-rate-rank', recycling), ('rail-travel-per-person-rank', rail)]


def digest(slug, o):
    print('\n%s [%s] %s -> %s | %s' % (slug, o['type'], o['l'], o['r'], o['unit']))
    if o['type'] == 'dumbbell':
        print('  ' + ', '.join('%s %.1f>%.1f' % r for r in o['rows']))
    else:
        print('  of %d: ' % o['n'] + ', '.join('%s %d>%d (%s>%s)' % (c, a, b, *o['vals'][c])
                                             for c, a, b in o['rows']))


def emit(i, slug, o, t):
    period = '%d \u2192 %d' % (o['l'], o['r'])
    fam = 'Change over time' if o['type'] == 'dumbbell' else 'Ranking'
    form = ('Dumbbell · %s' % period) if o['type'] == 'dumbbell' else ('Rank slope · %s' % period)
    b = dict(family=fam, form=form, exhibit=ex(i), type=o['type'], diff=t['diff'],
             truth=t['answer'] + ', %d vs %d' % (o['l'], o['r']), period=period, unit=o['unit'],
             leftYear=o['l'], rightYear=o['r'], answer=t['answer'], decoys=t['decoys'],
             hints=t['hints'], why=t['why'], slug=slug, source=o['src'], sourceUrl=o['url'])
    if o.get('suffix'):
        b['suffix'] = o['suffix']
    if o['type'] == 'dumbbell':
        b['data'] = arr(o['rows'], 3, o['dec'])
    else:
        b['ranks'] = arr(o['rows'], 3, 0)
    return block(b)


if __name__ == '__main__':
    built = [(s, f()) for s, f in ORDER]
    if '--digest' in sys.argv:
        for s, o in built:
            digest(s, o)
        sys.exit()
    from text10 import TEXT
    print(',\n'.join(emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)) + ',')
