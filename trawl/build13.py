#!/usr/bin/env python3
"""Batch 10, part two of three: dumbbells and rank slopes.

    python3 build13.py --digest
    python3 build13.py > b10.js

Text lives in text13.py, written from the digest. Rank slopes rank every
country present in both years and draw a readable selection of them, so a rank
on the chart is a place among all reporting countries, not among those drawn.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import arr, block, ex
import sources as S

START = 213
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'
WB = 'https://data.worldbank.org/indicator/%s'
OE = ('https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ'
      '&df[id]=%s&df[ag]=%s')
NON_EU = ('Norway', 'Switzerland', 'Iceland', 'United Kingdom', 'Turkey', 'Serbia', 'North Macedonia',
          'Bosnia and Herzegovina', 'Montenegro', 'Albania', 'Liechtenstein', 'Moldova', 'Ukraine',
          'Georgia', 'Armenia', 'Azerbaijan', 'Kosovo')


def key(n, **pos):
    """SDMX series key of n dimensions with values at the given positions (p0 = first)."""
    a = [''] * n
    for p, v in pos.items():
        a[int(p[1:])] = v
    return '.'.join(a)


def ratio(num, den, years, scale=100.0):
    return {c: {y: scale * num[c][y] / den[c][y] for y in years if y in num[c] and y in den.get(c, {})}
            for c in num if c in den}


def dumb(d, y1, y2, want, dec, scale=1.0):
    p = S.pair(d, y1, y2, want)
    rows = sorted(((c, a * scale, b * scale) for c, (a, b) in p.items()), key=lambda r: r[2])
    for r in rows:
        assert r[1] >= 0 and r[2] >= 0, ('dumbbells draw from zero', r)
    return rows


# ----------------------------------------------------------------- dumbbells
def hospital_stay():
    d = S.oecd('OECD.ELS.HD', 'DSD_HEALTH_PROC@DF_KEY_INDIC', 2010, 2023,
               key='.STAY.D....._T.HBEDT._T........')
    want = ['Japan', 'South Korea', 'Germany', 'France', 'Hungary', 'United Kingdom', 'Italy',
            'Finland', 'Spain', 'New Zealand', 'Belgium', 'Greece', 'Denmark', 'Sweden', 'Turkey']
    return dict(type='dumbbell', rows=dumb(d, '2010', '2023', want, 1), l=2010, r=2023, dec=1,
                unit='days', src='OECD', url=OE % ('DSD_HEALTH_PROC%40DF_KEY_INDIC', 'OECD.ELS.HD'))


def nurses():
    d = S.oecd('OECD.ELS.HD', 'DSD_HEALTH_REAC_EMP@DF_NURSE', 2010, 2023,
               key=key(9, p2='10P3HB', p5='MINU', p7='P'))
    want = ['Switzerland', 'Norway', 'Finland', 'Germany', 'Austria', 'South Korea', 'United Kingdom',
            'Romania', 'Italy', 'Spain', 'Poland', 'Hungary', 'Latvia', 'Greece', 'Mexico']
    return dict(type='dumbbell', rows=dumb(d, '2010', '2023', want, 1), l=2010, r=2023, dec=1,
                unit='per 1,000 people', src='OECD',
                url=OE % ('DSD_HEALTH_REAC_EMP%40DF_NURSE', 'OECD.ELS.HD'))


def no_upper_secondary():
    d = S.oecd('OECD.EDU.IMEP', 'DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA', 2000, 2024,
               key=key(17, p1='_T', p2='Y25T64', p3='ISCED11A_0T2', p13='OBS'))
    want = ['Mexico', 'Turkey', 'Portugal', 'Spain', 'Italy', 'Greece', 'United Kingdom', 'France',
            'Germany', 'Australia', 'Ireland', 'Sweden', 'South Korea', 'Canada', 'Poland', 'Czechia']
    return dict(type='dumbbell', rows=dumb(d, '2000', '2024', want, 1), l=2000, r=2024, dec=1,
                unit='% of people aged 25 to 64', suffix='%', src='OECD',
                url=OE % ('DSD_EAG_LSO_EA%40DF_LSO_NEAC_DISTR_EA', 'OECD.EDU.IMEP'))


def tertiary_enrolment():
    d = S.worldbank('SE.TER.ENRR', [2000, 2023])
    want = ['Greece', 'Argentina', 'South Korea', 'Chile', 'United Kingdom', 'China', 'Switzerland',
            'Mexico', 'Morocco', 'Indonesia', 'India', 'Vietnam', 'Bangladesh', 'Kenya', 'Tanzania']
    return dict(type='dumbbell', rows=dumb(d, '2000', '2023', want, 0), l=2000, r=2023, dec=0,
                unit='per 100 people of the matching age', src='World Bank', url=WB % 'SE.TER.ENRR')


def manufacturing():
    d = S.worldbank('NV.IND.MANF.ZS', [1995, 2024])
    want = ['Ireland', 'Cambodia', 'South Korea', 'Bangladesh', 'Mexico', 'Japan', 'Germany',
            'Poland', 'Italy', 'India', 'Brazil', 'Spain', 'France', 'United Kingdom', 'Australia']
    return dict(type='dumbbell', rows=dumb(d, '1995', '2024', want, 1), l=1995, r=2024, dec=1,
                unit='% of GDP', suffix='%', src='World Bank', url=WB % 'NV.IND.MANF.ZS')


def refugees():
    iso = dict(Iran='IRN', Turkey='TUR', Germany='DEU', Uganda='UGA', Pakistan='PAK', Chad='TCD',
               Poland='POL', Bangladesh='BGD', Lebanon='LBN', France='FRA', Jordan='JOR', Kenya='KEN',
               **{'United Kingdom': 'GBR', 'United States': 'USA'}, Spain='ESP', Italy='ITA')
    d = S.owid('refugee-population-by-country-or-territory-of-asylum', list(iso.values()), 2010, 2024)
    want = list(iso)
    return dict(type='dumbbell', rows=dumb(d, '2010', '2024', want, 0, 1e-3), l=2010, r=2024, dec=0,
                unit='thousands of people', src='Our World in Data',
                url='https://ourworldindata.org/grapher/refugee-population-by-country-or-territory-of-asylum')


def solar_share():
    ys = ['2014', '2024']
    so = S.eurostat('nrg_bal_peh', ys, nrg_bal='GEP', siec='RA420', unit='GWH', freq='A')
    to = S.eurostat('nrg_bal_peh', ys, nrg_bal='GEP', siec='TOTAL', unit='GWH', freq='A')
    want = ['Hungary', 'Greece', 'Spain', 'Netherlands', 'Germany', 'Italy', 'Portugal', 'Belgium',
            'Denmark', 'Poland', 'Austria', 'Romania', 'France', 'Czechia', 'Ireland', 'Sweden', 'Finland']
    return dict(type='dumbbell', rows=dumb(ratio(so, to, ys), '2014', '2024', want, 1), l=2014, r=2024,
                dec=1, unit='% of electricity generated', suffix='%', src='Eurostat', url=ES % 'nrg_bal_peh')


def holidays_abroad():
    ys = ['2014', '2024']
    f = S.eurostat('tour_dem_tttot', ys, c_dest='FOR', purpose='PER', duration='N_GE1', unit='NR', freq='A')
    w = S.eurostat('tour_dem_tttot', ys, c_dest='WORLD', purpose='PER', duration='N_GE1', unit='NR', freq='A')
    want = ['Luxembourg', 'Belgium', 'Austria', 'Netherlands', 'Ireland', 'Germany', 'Denmark', 'Hungary',
            'Sweden', 'Italy', 'Poland', 'France', 'Greece', 'Spain', 'Romania']
    return dict(type='dumbbell', rows=dumb(ratio(f, w, ys), '2014', '2024', want, 1), l=2014, r=2024,
                dec=1, unit='% of trips', suffix='%', src='Eurostat', url=ES % 'tour_dem_tttot')


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



def gini():
    d = S.eurostat('ilc_di12', [2015, 2024], age='TOTAL', statinfo='GINI_HND', freq='A')
    show = ['Bulgaria', 'Lithuania', 'Romania', 'Italy', 'Malta', 'Spain', 'Estonia', 'France',
            'Germany', 'Ireland', 'Poland', 'Sweden', 'Belgium', 'Slovakia']
    rows, n, v = slope(d, '2015', '2024', show, NON_EU)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2015, r=2024,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'ilc_di12')


def arms():
    d = S.worldbank('MS.MIL.MPRT.KD', [2004, 2024])
    # at 77 places a rank is about five pixels, so neighbours closer than four
    # places collide; these eight are at least four apart in both years
    show = ['Poland', 'China', 'Japan', 'Hungary', 'Israel', 'Vietnam', 'Norway', 'Argentina']
    rows, n, v = slope(d, '2004', '2024', show)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2004, r=2024,
                unit='rank among countries, highest first', src='World Bank', url=WB % 'MS.MIL.MPRT.KD')


def saving():
    d = S.eurostat('nasa_10_ki', [2005, 2024], na_item='SRG_S14_S15', unit='PC', sector='S14_S15', freq='A')
    show = ['Germany', 'Czechia', 'Malta', 'Sweden', 'Denmark', 'Slovenia', 'Belgium', 'Italy',
            'Poland', 'Lithuania', 'Cyprus', 'Romania', 'Greece']
    rows, n, v = slope(d, '2005', '2024', show, NON_EU)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2005, r=2024,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'nasa_10_ki')


def electricity_price():
    d = S.eurostat('nrg_pc_204', [], nrg_cons='KWH2500-4999', tax='I_TAX', currency='EUR', unit='KWH',
                   siec='E7000', freq='S')
    show = ['Germany', 'Denmark', 'Czechia', 'Italy', 'France', 'Poland', 'Estonia', 'Netherlands',
            'Luxembourg', 'Slovakia', 'Malta', 'Bulgaria', 'Hungary']
    rows, n, v = slope(d, '2008-S2', '2024-S2', show, NON_EU)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2008, r=2024,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'nrg_pc_204')


def life_satisfaction():
    d = S.eurostat('ilc_pw01', [2013, 2024], statinfo='AVG', unit='RTG', isced11='TOTAL', life_sat='LIFE',
                   sex='T', age='Y_GE16', freq='A')
    # scores are to one decimal, so ranks tie often; tied labels draw on top of
    # each other, and none of these ten shares a rank with another in either year
    show = ['Finland', 'Sweden', 'Belgium', 'Luxembourg', 'Germany', 'Romania', 'Malta', 'Portugal',
            'Hungary', 'Bulgaria']
    rows, n, v = slope(d, '2013', '2024', show, NON_EU)
    return dict(type='slope', rows=rows, n=n, vals=v, l=2013, r=2024,
                unit='rank among EU countries, highest first', src='Eurostat', url=ES % 'ilc_pw01')


ORDER = [('hospital-average-stay', hospital_stay), ('nurses-per-thousand', nurses),
         ('adults-without-upper-secondary', no_upper_secondary), ('tertiary-enrolment', tertiary_enrolment),
         ('manufacturing-share', manufacturing), ('refugees-hosted', refugees),
         ('solar-share-of-electricity', solar_share), ('holidays-abroad', holidays_abroad),
         ('income-inequality-rank', gini), ('arms-imports-rank', arms),
         ('household-saving-rank', saving), ('electricity-price-rank', electricity_price),
         ('life-satisfaction-rank', life_satisfaction)]


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
    from text13 import TEXT
    print(',\n'.join(emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)) + ',')
