#!/usr/bin/env python3
"""Batch 9, part one of three: the snapshot forms (treemap, symbol, beeswarm,
deviation). First batch built for the no-recycling dealer.

    python3 build9.py --digest     # the data each chart will draw, compactly
    python3 build9.py > b9.js      # the JS fragment for src/puzzles.js

Every value is fetched live and every expected country is asserted. The text
(decoys, hints, why) lives in text9.py and was written from the digest, i.e.
from the final data, not from the screening pass.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import arr, block, ex
import sources as S

START = 163          # pool index of the first puzzle in this file
EU = ['Belgium', 'Bulgaria', 'Czechia', 'Denmark', 'Germany', 'Estonia', 'Ireland', 'Greece',
      'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania', 'Luxembourg',
      'Hungary', 'Malta', 'Netherlands', 'Austria', 'Poland', 'Portugal', 'Romania', 'Slovenia',
      'Slovakia', 'Finland', 'Sweden']
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'


def top(values, n=12, floor=0):
    rows = sorted(((c, v) for c, v in values.items() if v > floor), key=lambda r: -r[1])
    return rows[:n]


def crop(code, y, members):
    d = S.eurostat('apro_cpsh1', [y], crops=code, strucpro='HPRD_HUMD_EU_THS_T', freq='A')
    return {c: v for c, v in S.year(d, y).items() if c in members}


P = {}

# ------------------------------------------------------------------ treemaps
def olives():
    v = crop('O1000', 2024, EU + ['Turkey', 'Albania'])
    rows = top(v, 12, 1)
    assert rows[0][0] == 'Spain' and rows[1][0] == 'Turkey', rows[:3]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand tonnes', period='2024', src='Eurostat', url=ES % 'apro_cpsh1',
                form='Treemap · EU and candidate countries, 2024', family='Part-to-whole')


def sprouts():
    v = crop('V1200', 2024, EU)
    rows = top(v, 12, 0.1)
    assert rows[0][0] == 'Netherlands' and rows[1][0] == 'Belgium', rows[:3]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=1,
                unit='thousand tonnes', period='2024', src='Eurostat', url=ES % 'apro_cpsh1',
                form='Treemap · share of the EU total, 2024', family='Part-to-whole')


def aquaculture():
    d = S.worldbank('ER.FSH.AQUA.MT', [2022])
    rows = [(c, v / 1e3) for c, v in top(S.year(d, '2022'), 12)]
    assert rows[0][0] == 'China', rows[:2]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand tonnes', period='2022', src='World Bank',
                url='https://data.worldbank.org/indicator/ER.FSH.AQUA.MT',
                form='Treemap · the twelve largest, 2022', family='Part-to-whole')


def sea_passengers():
    d = S.eurostat('mar_pa_aa', [2024], geo_dim='rep_mar', unit='THS_PAS', direct='TOTAL', freq='A')
    v = {c: x / 1e3 for c, x in S.year(d, '2024').items()}
    rows = top(v, 12)
    assert rows[0][0] == 'Italy' and 'Malta' in dict(rows), rows[:4]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=1,
                unit='million passengers', period='2024', src='Eurostat', url=ES % 'mar_pa_aa',
                form='Treemap · the twelve largest, 2024', family='Part-to-whole')

# ------------------------------------------------------------------- symbols
def hops():
    v = crop('I4000', 2024, EU)
    rows = top(v, 12, 0.1)
    assert rows[0][0] == 'Germany' and rows[1][0] == 'Czechia', rows[:3]
    return dict(type='symbol', rows=rows, dec=2, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · every EU grower, 2024', family='Magnitude')


def asparagus():
    v = crop('V2600', 2024, EU)
    rows = top(v, 12, 0.5)
    assert rows[0][0] == 'Germany', rows[:3]
    return dict(type='symbol', rows=rows, dec=1, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · the largest EU growers, 2024', family='Magnitude')


def campsites():
    d = S.eurostat('tour_occ_ninat', [2024], c_resid='TOTAL', nace_r2='I553', unit='NR', freq='A')
    v = {c: x / 1e6 for c, x in S.year(d, '2024').items()}
    rows = top(v, 12)
    assert rows[0][0] == 'France', rows[:2]
    return dict(type='symbol', rows=rows, dec=1, unit='million nights', period='2024',
                src='Eurostat', url=ES % 'tour_occ_ninat',
                form='Proportional symbols · the twelve largest, 2024', family='Magnitude')

# ----------------------------------------------------------------- beeswarms
def swarm(d, y, excl=()):
    return sorted((c, v) for c, v in S.year(d, y).items() if c not in excl)


def ict_women():
    d = S.eurostat('isoc_sks_itsps', [2024], unit='PC', sex='F', freq='A')
    rows = swarm(d, '2024', ('Bosnia and Herzegovina',))
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of the specialists employed',
                suffix='%', period='2024', src='Eurostat', url=ES % 'isoc_sks_itsps',
                form='Beeswarm · every reporting country, 2024', family='Distribution')


def home_ownership():
    d = S.eurostat('ilc_lvho02', [2024], tenure='OWN', rskpovth='TOTAL', hhcomp='TOTAL',
                   unit='PC', freq='A')
    rows = swarm(d, '2024')
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of the population', suffix='%',
                period='2024', src='Eurostat', url=ES % 'ilc_lvho02',
                form='Beeswarm · every reporting country, 2024', family='Distribution')


def cheese():
    ch = S.eurostat('apro_mk_pobta', [2023], dairyprod='D7100', milkitem='PRO', freq='A')
    pop = S.eurostat('demo_pjan', [2023], sex='T', age='TOTAL', unit='NR', freq='A')
    c2, p2 = S.year(ch, '2023'), S.year(pop, '2023')
    rows = sorted((c, c2[c] * 1e6 / p2[c]) for c in c2 if c in p2 and c2[c] > 0
                  and c not in ('Albania', 'Serbia'))
    assert dict(rows)['Denmark'] == max(v for _, v in rows)
    return dict(type='beeswarm', rows=rows, dec=1, unit='kilograms per resident',
                period='2023', src='Eurostat', url=ES % 'apro_mk_pobta',
                form='Beeswarm · every reporting country, 2023', family='Distribution')


def death_rate():
    d = S.worldbank('SP.DYN.CDRT.IN', [2023])
    rows = [r for r in swarm(d, '2023') if '(' not in r[0]]
    assert len(rows) > 150
    return dict(type='beeswarm', rows=rows, dec=1, unit='per 1,000 people a year',
                period='2023', src='World Bank',
                url='https://data.worldbank.org/indicator/SP.DYN.CDRT.IN',
                form='Beeswarm · every country, 2023', family='Distribution')


def min_wage():
    d = S.oecd('OECD.ELS.SAE', 'DSD_EARNINGS@MIN2AVE', 2024, 2024, AGGREGATION_OPERATION='MEDIAN')
    rows = swarm(d, '2024')
    assert dict(rows)['United States'] < 30
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of the median full-time wage',
                suffix='%', period='2024', src='OECD',
                url='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_EARNINGS%40MIN2AVE',
                form='Beeswarm · every OECD country with one, 2024', family='Distribution')


def adult_learning():
    d = S.eurostat('trng_lfse_01', [2024], sex='T', age='Y25-64', unit='PC', freq='A')
    rows = swarm(d, '2024', ('Bosnia and Herzegovina',))
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of people aged 25 to 64',
                suffix='%', period='2024', src='Eurostat', url=ES % 'trng_lfse_01',
                form='Beeswarm · every reporting country, 2024', family='Distribution')

# ---------------------------------------------------------------- deviations
DAC = ['Norway', 'Luxembourg', 'Sweden', 'Denmark', 'Germany', 'Netherlands', 'Ireland',
       'United Kingdom', 'Switzerland', 'France', 'Finland', 'Japan', 'Canada', 'Italy', 'Spain',
       'United States', 'South Korea', 'Australia', 'Greece', 'Hungary']


def aid():
    d = S.oecd('OECD.DCD.FSD', 'DSD_DAC1@DF_DAC1', 2024, 2024, MEASURE='11002')
    v = S.year(d, '2024', DAC)
    rows = sorted(v.items(), key=lambda r: -r[1])
    return dict(type='deviation', rows=rows, dec=2, reference=0.7,
                unit='% of national income, against a 0.7% line', period='2024', src='OECD',
                url='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_DAC1%40DF_DAC1',
                form='Diverging bar · distance from the 0.7% line, 2024', family='Deviation')


GHG = ['Turkey', 'Cyprus', 'Iceland', 'Ireland', 'Spain', 'Portugal', 'Austria', 'Poland', 'Italy',
       'France', 'Netherlands', 'Sweden', 'Denmark', 'Germany', 'Czechia', 'Bulgaria', 'Latvia',
       'Lithuania', 'Romania', 'Estonia']


def ghg():
    d = S.eurostat('sdg_13_10', [2023], src_crf='TOTX4_MEMO', unit='I90', freq='A')
    v = S.year(d, '2023', GHG)
    rows = sorted(v.items(), key=lambda r: -r[1])
    return dict(type='deviation', rows=rows, dec=1, reference=100,
                unit='index, 1990 = 100', period='1990 → 2023', src='Eurostat',
                url=ES % 'sdg_13_10', form='Diverging bar · change since 1990, index 1990 = 100',
                family='Deviation')


ORDER = [('olive-harvest', olives), ('brussels-sprouts-grown', sprouts),
         ('fish-and-seaweed-farmed', aquaculture), ('sea-passengers', sea_passengers),
         ('hops-grown', hops), ('asparagus-grown', asparagus), ('campsite-nights', campsites),
         ('women-in-ict-jobs', ict_women), ('home-ownership', home_ownership),
         ('cheese-made-per-person', cheese), ('crude-death-rate', death_rate),
         ('minimum-wage-to-median', min_wage), ('adult-learning', adult_learning),
         ('aid-share-of-income', aid), ('greenhouse-gas-change-since-1990', ghg)]


def digest(slug, o):
    rows = o['rows']
    if o['type'] == 'beeswarm':
        s = sorted(rows, key=lambda r: -r[1])
        body = ', '.join('%s %s' % (c, round(v, o['dec'])) for c, v in s)
    else:
        body = ', '.join('%s %s' % (c, round(v, o['dec'])) for c, v in rows)
    print('\n%s [%s] %s | %s' % (slug, o['type'], o['period'], o['unit']))
    print('  ' + body + (' | total %s' % o['total'] if 'total' in o else ''))


def emit(i, slug, o, t):
    b = dict(family=o['family'], form=o['form'], exhibit=ex(i), type=o['type'], diff=t['diff'],
             truth=t.get('truth') or t['answer'] + ', ' + o['period'],
             period=o['period'], unit=o['unit'], answer=t['answer'], decoys=t['decoys'],
             hints=t['hints'], why=t['why'], slug=slug, source=o['src'], sourceUrl=o['url'])
    if o.get('suffix'):
        b['suffix'] = o['suffix']
    if 'total' in o:
        b['total'] = o['total']
    if 'reference' in o:
        b['reference'] = o['reference']
    b['data'] = arr([(c, v) for c, v in o['rows']], 4, o['dec'])
    if o['type'] == 'beeswarm':
        b['label'], b['labelSm'] = t['label'], t['labelSm']
        have = {c for c, _ in o['rows']}
        assert set(t['label']) <= have and set(t['labelSm']) <= have, slug
    return block(b)


if __name__ == '__main__':
    built = [(s, f()) for s, f in ORDER]
    if '--digest' in sys.argv:
        for s, o in built:
            digest(s, o)
        sys.exit()
    from text9 import TEXT
    out = [emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)]
    print(',\n'.join(out) + ',')
