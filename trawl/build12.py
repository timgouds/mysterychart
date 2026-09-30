#!/usr/bin/env python3
"""Batch 10, part one of three: the snapshot forms (treemap, symbol, beeswarm)
and the two deviation charts.

    python3 build12.py --digest     # the data each chart will draw, compactly
    python3 build12.py > b12.js     # the JS fragment for src/puzzles.js

Every value is fetched live and every expected country is asserted. The text
lives in text12.py and was written from the digest, not from screening.
"""
import sys, os, csv, io, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import arr, block, ex, nm
import sources as S

START = 198          # pool index of the first puzzle in this file
EU = ['Belgium', 'Bulgaria', 'Czechia', 'Denmark', 'Germany', 'Estonia', 'Ireland', 'Greece',
      'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania', 'Luxembourg',
      'Hungary', 'Malta', 'Netherlands', 'Austria', 'Poland', 'Portugal', 'Romania', 'Slovenia',
      'Slovakia', 'Finland', 'Sweden']
NON_EU = ('Norway', 'Switzerland', 'Iceland', 'United Kingdom', 'Turkey', 'Serbia', 'North Macedonia',
          'Bosnia and Herzegovina', 'Montenegro', 'Albania', 'Liechtenstein', 'Moldova', 'Ukraine',
          'Georgia', 'Armenia', 'Azerbaijan', 'European Free Trade Association')
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'
OE = ('https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ'
      '&df[id]=%s&df[ag]=%s')


def top(values, n=12, floor=0):
    rows = sorted(((c, v) for c, v in values.items() if v > floor), key=lambda r: -r[1])
    return rows[:n]


def crop(code, y, members=EU):
    d = S.eurostat('apro_cpsh1', [y], crops=code, strucpro='HPRD_HUMD_EU_THS_T', freq='A')
    return {c: v for c, v in S.year(d, y).items() if c in members}


def owid_all(slug, y):
    """{country: value} for one year, every country OWID holds (aggregates dropped)."""
    url = 'https://ourworldindata.org/grapher/%s.csv?csvType=full' % slug
    txt = subprocess.run(['curl', '-s', '--compressed', '-m', '90', url],
                         capture_output=True, text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    if len(rows) < 3:
        S.die('owid %s: %r' % (slug, txt[:80]))
    return {nm(r[0]): float(r[3]) for r in rows[1:]
            if r[2] == str(y) and r[1] and not r[1].startswith('OWID') and r[3]}


# ------------------------------------------------------------------ treemaps
def palm_oil():
    v = {c: x / 1e3 for c, x in owid_all('palm-oil-production', 2023).items()}
    rows = top(v, 12)
    assert rows[0][0] == 'Indonesia' and rows[1][0] == 'Malaysia', rows[:3]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand tonnes', period='2023', src='Our World in Data',
                url='https://ourworldindata.org/grapher/palm-oil-production',
                form='Treemap · the twelve largest, 2023', family='Part-to-whole')


def avocados():
    v = {c: x / 1e3 for c, x in owid_all('avocado-production', 2023).items()}
    rows = top(v, 12)
    assert rows[0][0] == 'Mexico' and 'Dominican Republic' in dict(rows[:4]), rows[:4]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand tonnes', period='2023', src='Our World in Data',
                url='https://ourworldindata.org/grapher/avocado-production',
                form='Treemap · the twelve largest, 2023', family='Part-to-whole')


def goats():
    d = S.eurostat('apro_mt_lsgoat', [2024], animals='A4200', month='M11_M12', unit='THS_HD', freq='A')
    v = {c: x for c, x in S.year(d, '2024').items() if c in EU}
    rows = top(v, 12)
    assert rows[0][0] == 'Greece' and rows[1][0] == 'Spain', rows[:3]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand animals', period='2024', src='Eurostat', url=ES % 'apro_mt_lsgoat',
                form='Treemap · the twelve largest EU herds, 2024', family='Part-to-whole')


def soya():
    rows = top(crop('I1130', 2024), 12, 1)
    assert rows[0][0] == 'Italy' and rows[1][0] == 'France', rows[:3]
    return dict(type='treemap', rows=rows, total=round(sum(r[1] for r in rows)), dec=0,
                unit='thousand tonnes', period='2024', src='Eurostat', url=ES % 'apro_cpsh1',
                form='Treemap · the twelve largest EU growers, 2024', family='Part-to-whole')

# ------------------------------------------------------------------- symbols
def hemp():
    rows = top(crop('I2200', 2024), 12, 0.05)
    assert rows[0][0] == 'France' and rows[1][0] == 'Netherlands', rows[:3]
    return dict(type='symbol', rows=rows, dec=1, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · every EU grower, 2024', family='Magnitude')


def kiwis():
    rows = top(crop('F2200', 2024), 12, 0.05)
    assert rows[0][0] == 'Italy' and rows[1][0] == 'Greece', rows[:3]
    return dict(type='symbol', rows=rows, dec=1, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · every EU grower, 2024', family='Magnitude')


def blackcurrants():
    rows = top(crop('F3110', 2024), 12, 0.3)
    assert rows[0][0] == 'Poland' and rows[0][1] > 5 * rows[1][1], rows[:3]
    return dict(type='symbol', rows=rows, dec=1, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · the largest EU growers, 2024', family='Magnitude')


def mushrooms():
    rows = top(crop('U1000', 2024), 12, 1)
    assert rows[0][0] == 'Poland' and 'Ireland' in dict(rows[:8]), rows[:8]
    return dict(type='symbol', rows=rows, dec=0, unit='thousand tonnes', period='2024',
                src='Eurostat', url=ES % 'apro_cpsh1',
                form='Proportional symbols · the twelve largest EU growers, 2024', family='Magnitude')


def motorways():
    d = S.eurostat('road_if_motorwa', [2023], tra_infr='MWAY', unit='KM', freq='A')
    rows = top(S.year(d, '2023'), 12)
    assert rows[0][0] == 'Spain' and rows[1][0] == 'Germany', rows[:3]
    rows = [('Britain' if c == 'United Kingdom' else c, v) for c, v in rows]
    return dict(type='symbol', rows=rows, dec=0, unit='kilometres', period='2023',
                src='Eurostat', url=ES % 'road_if_motorwa',
                form='Proportional symbols · the twelve longest networks in Europe, 2023',
                family='Magnitude')

# ----------------------------------------------------------------- beeswarms
def swarm(d, y, excl=()):
    return sorted((c, v) for c, v in S.year(d, y).items() if c not in excl)


def caesarean():
    d = S.oecd('OECD.ELS.HD', 'DSD_HEALTH_PROC@DF_KEY_INDIC', 2023, 2023,
               key='.PRC.PRC_10P3BR_L.CM74_CAE....._T.........',
               MEASURE='PRC', UNIT_MEASURE='PRC_10P3BR_L', MEDICAL_PROCEDURE='CM74_CAE', MODE_PROVISION='_T')
    rows = sorted((c, v / 10) for c, v in S.year(d, '2023').items())
    assert dict(rows)['South Korea'] > 60 and dict(rows)['Iceland'] < 16, rows
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of live births', suffix='%',
                period='2023', src='OECD',
                url=OE % ('DSD_HEALTH_PROC%40DF_KEY_INDIC', 'OECD.ELS.HD'),
                form='Beeswarm · every reporting country, 2023', family='Distribution')


def languages():
    d = S.eurostat('edat_aes_l21', [2022], sex='T', age='Y25-64', n_lang='0', unit='PC', freq='A')
    rows = swarm(d, '2022')
    assert dict(rows)['Luxembourg'] < 10 and dict(rows)['Hungary'] > 45
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of people aged 25 to 64', suffix='%',
                period='2022', src='Eurostat', url=ES % 'edat_aes_l21',
                form='Beeswarm · every reporting country, 2022', family='Distribution')


def overcrowding():
    d = S.eurostat('ilc_lvho05a', [2024], rskpovth='TOTAL', age='TOTAL', sex='T', unit='PC', freq='A')
    rows = swarm(d, '2024')
    assert dict(rows)['Romania'] > 35 and dict(rows)['Cyprus'] < 5
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of the population', suffix='%',
                period='2024', src='Eurostat', url=ES % 'ilc_lvho05a',
                form='Beeswarm · every reporting country, 2024', family='Distribution')


def ai_firms():
    d = S.eurostat('isoc_eb_ai', [2025], size_emp='GE10', indic_is='E_AI_TANY', unit='PC_ENT',
                   nace_r2='C10-S951_X_K', freq='A')
    rows = swarm(d, '2025')
    assert dict(rows)['Denmark'] == max(v for _, v in rows)
    return dict(type='beeswarm', rows=rows, dec=1, unit='% of businesses with ten or more staff',
                suffix='%', period='2025', src='Eurostat', url=ES % 'isoc_eb_ai',
                form='Beeswarm · every reporting country, 2025', family='Distribution')

# ---------------------------------------------------------------- deviations
def real_income():
    d = S.eurostat('nasa_10_ki', [2024], na_item='B7G_R_HAB_2010', unit='PC', sector='S14_S15', freq='A')
    v = {c: x for c, x in S.year(d, '2024').items() if c in EU}
    rows = sorted(v.items(), key=lambda r: -r[1])
    assert rows[0][0] == 'Romania' and rows[-1][0] == 'Greece', (rows[:2], rows[-2:])
    return dict(type='deviation', rows=rows, dec=1, reference=100,
                unit='index, 2010 = 100', period='2010 → 2024', src='Eurostat', url=ES % 'nasa_10_ki',
                form='Diverging bar · change since 2010, index 2010 = 100', family='Deviation')


BIRTHS = ['Luxembourg', 'Cyprus', 'Malta', 'Portugal', 'Denmark', 'Netherlands', 'Germany', 'Austria',
          'Belgium', 'Sweden', 'Hungary', 'France', 'Ireland', 'Czechia', 'Finland', 'Spain', 'Italy',
          'Greece', 'Romania', 'Poland', 'Lithuania', 'Latvia']


def births():
    d = S.eurostat('demo_gind', [2014, 2024], indic_de='LBIRTH', freq='A')
    p = S.pair(d, '2014', '2024', BIRTHS)
    rows = sorted(((c, 100 * b / a) for c, (a, b) in p.items()), key=lambda r: -r[1])
    assert rows[-1][0] == 'Latvia' and dict(rows)['Poland'] < 70, rows[-4:]
    return dict(type='deviation', rows=rows, dec=1, reference=100,
                unit='index, 2014 = 100', period='2014 → 2024', src='Eurostat', url=ES % 'demo_gind',
                form='Diverging bar · change since 2014, index 2014 = 100', family='Deviation')


ORDER = [('palm-oil-produced', palm_oil), ('avocados-grown', avocados), ('goats-kept', goats),
         ('soya-grown', soya), ('hemp-grown', hemp), ('kiwis-grown', kiwis),
         ('blackcurrants-grown', blackcurrants), ('mushrooms-grown', mushrooms),
         ('motorway-length', motorways), ('caesarean-births', caesarean),
         ('no-foreign-language', languages), ('overcrowded-homes', overcrowding),
         ('businesses-using-ai', ai_firms), ('real-household-income-change', real_income),
         ('births-change-since-2014', births)]


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
    from text12 import TEXT
    out = [emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)]
    print(',\n'.join(out) + ',')
