#!/usr/bin/env python3
"""Assemble batch eight (31 puzzles, indices 134 to 164).

Sources: WHO 9, Eurostat 13, OECD 7, OWID 2. No World Bank and no lollipops,
both deliberate: the pool was 69% World Bank and OWID, and lollipop was 24 of
134. Forms are dumbbell 10, diverging bar 6, rank slope 4, line 3, beeswarm 3,
treemap 2, connected scatter 2, proportional symbols 1. 21 of the 31 use a time
range. Nine are written to the deadpan brief.

Three things this batch changed elsewhere, recorded here because a future batch
will hit them too:

  - Four decoys, not seven. Only SHOWN_DECOYS (3) are ever rendered, so decoys
    five to seven have never been seen by anybody. preflight.mjs now wants at
    least four rather than exactly seven.
  - The connected scatterplot is new. Both its axes are measures, so they carry
    units only and the redacted title names the pairing; common.block() grew one
    branch for it and engine.html grew drawScatter with its compact variant.
  - A chart of change cannot be a beeswarm. drawBeeswarm maps x from zero, so a
    fall of -29 lands off the canvas. Both change charts here are diverging bars
    around a zero line, the same fix build7 made for temperature.

Every reveal names all three decoys the player saw and every number in a reveal
is a number on that chart. WORLD_CLAIMS below lists everything the text asserts
that the chart cannot show, so the unverifiable surface can be read in one pass.

    python3 trawl/build8.py > batch8.js     # append the output to src/puzzles.js
    python3 build.py
    node preflight.mjs
"""
import csv, io, json, os, re, subprocess, sys
from common import ex, block, arr, num

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE, exist_ok=True)


def get(name, url):
    """Fetch once, cache, and refuse to proceed on an empty body.

    A 200 with 89 bytes is an empty WHO indicator, not a success: three codes
    that looked right in the indicator list (MDG_0000000027, OA_DMFT,
    DSD_PDB@DF_PDB_LV) return nothing or 500. Always -L: OWID answers a bare CSV
    request with a 301 and curl without it writes a zero-byte file and exits 0.
    """
    p = os.path.join(CACHE, name)
    if not os.path.exists(p) or os.path.getsize(p) < 200:
        subprocess.run(['curl', '-sSL', '--compressed', '-m', '180', url, '-o', p],
                       check=True)
    if os.path.getsize(p) < 200:
        sys.exit('empty payload for %s' % name)
    return p


W = 'https://ghoapi.azureedge.net/api'
E = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data'
O = 'https://sdmx.oecd.org/public/rest/data'
G = 'https://ourworldindata.org/grapher'
OQ = 'format=jsondata&dimensionAtObservation=AllDimensions'

SOURCES = [
    ('who_countries.json', W + '/DIMENSION/COUNTRY/DimensionValues'),
    ('who_tb.json',        W + '/MDG_0000000020'),
    ('who_measles.json',   W + '/WHS8_110'),
    ('who_maternal.json',  W + '/MDG_0000000026'),
    ('who_stunting.json',  W + '/NUTSTUNTINGPREV'),
    ('who_bp.json',        W + '/BP_04'),
    ('who_cleanfuels.json', W + '/PHE_HHAIR_PROP_POP_CLEAN_FUELS'),
    ('who_water.json',     W + '/WSH_WATER_SAFELY_MANAGED'),
    ('who_le60.json',      W + '/WHOSIS_000015'),
    ('who_caries.json',    W + '/ORALHEALTH_UNTREATEDCARIESPERMANENT'),
    ('es_telework.json',   E + '/lfsa_ehomp?format=JSON&lang=EN&time=2019&time=2024'),
    ('es_waste.json',      E + '/env_wasmun?format=JSON&lang=EN&time=2005&time=2023&wst_oper=GEN'),
    ('es_flats.json',      E + '/ilc_lvho01?format=JSON&lang=EN&time=2024'),
    ('es_windelec.json',   E + '/nrg_ind_pehnf?format=JSON&lang=EN&time=2024'),
    ('es_nights.json',     E + '/tour_occ_ninat?format=JSON&lang=EN&time=2024'),
    ('es_railfreight.json', E + '/rail_go_total?format=JSON&lang=EN&time=2023'),
    ('es_pricelevel.json', E + '/prc_ppp_ind?format=JSON&lang=EN&time=2024'),
    ('es_neet.json',       E + '/edat_lfse_20?format=JSON&lang=EN&time=2010&time=2024'),
    ('es_cars.json',       E + '/road_eqs_carhab?format=JSON&lang=EN&time=2013&time=2023'),
    ('es_agriout.json',    E + '/aact_eaa01?format=JSON&lang=EN&time=1995&time=2024'),
    ('es_books.json',      E + '/ilc_scp33?format=JSON&lang=EN'),
    ('es_fertility.json',  E + '/demo_find?format=JSON&lang=EN'),
    ('es_fememp.json',     E + '/lfsi_emp_a?format=JSON&lang=EN'),
    ('oecd_hours.json',    O + '/OECD.ELS.SAE,DSD_HW@DF_AVG_ANN_HRS_WKD,/all?' + OQ + '&startPeriod=1970'),
    ('oecd_prod.json',     O + '/OECD.SDD.TPS,DSD_PDB@DF_PDB,/all?' + OQ + '&startPeriod=1970'),
    ('oecd_consult.json',  O + '/OECD.ELS.HD,DSD_HEALTH_PROC@DF_CONSULT,/all?' + OQ + '&startPeriod=2000'),
    ('oecd_medtech.json',  O + '/OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_MED_TECH,/all?' + OQ + '&startPeriod=2010'),
    ('oecd_wagegap.json',  O + '/OECD.ELS.SAE,DSD_EARNINGS@GENDER_WAGE_GAP,/all?' + OQ + '&startPeriod=2000'),
    ('oecd_msti.json',     O + '/OECD.STI.STP,DSD_MSTI@DF_MSTI,/all?' + OQ + '&startPeriod=2000'),
    ('oecd_pag.json',      O + '/OECD.ELS.SPD,DSD_PAG@DF_PAG,/all?' + OQ + '&startPeriod=2000'),
    ('owid_coal_full.csv', G + '/share-electricity-coal.csv?csvType=full'),
    ('owid_height.csv',    G + '/average-height-of-men.csv?csvType=filtered&country=~ALL&time=1900..1996'),
]

TIDY = {}


def fetch_all():
    for name, url in SOURCES:
        get(name, url)


SKIP = {
    'EU27_2020', 'EU28', 'EU27_2007', 'EA', 'EA19', 'EA20', 'EA12', 'EU15', 'EU',
    'EEA', 'EFTA', 'GLOBAL', 'WORLD', 'World', 'Africa', 'Asia', 'Europe',
    'European Union (27)', 'North America', 'South America', 'Oceania',
    'High-income countries', 'Low-income countries', 'Upper-middle-income countries',
    'Lower-middle-income countries', 'European Union (27) (GCP)', 'OECD', 'G7', 'G20',
}

def save(name, subject, unit, years, rows, note=''):
    """Keep a series in memory and report its top and tail on stderr.

    The tail is always printed. The bottom of a chart is where decoys die, and
    it is the half that is easy to forget while authoring.
    """
    rows = [r for r in rows if all(v is not None for v in r[1:])]
    rows.sort(key=lambda r: -r[1])
    TIDY[name] = {'subject': subject, 'unit': unit, 'years': years, 'rows': rows}
    if not rows:
        sys.exit('EMPTY series: ' + name)
    f = lambda r: '%s %g' % (r[0], r[1])
    sys.stderr.write('%-22s n=%3d %-10s top: %s || tail: %s\n' % (
        name, len(rows), unit, ', '.join(map(f, rows[:3])), ', '.join(map(f, rows[-3:]))))

# ------------------------------------------------------------------ WHO GHO
WHO_NAME = {}
TOTALS = {None, '', 'BTSX', 'SEX_BTSX', 'TOTL', 'RESIDENCEAREATYPE_TOTL'}

def who(name, fn, subject, unit, years):
    if not WHO_NAME:
        for r in json.load(open(get('who_countries.json', dict(SOURCES)['who_countries.json'])))['value']:
            WHO_NAME[r['Code']] = r['Title']
    by = {}
    for r in json.load(open(get(fn, dict(SOURCES)[fn])))['value']:
        if r.get('SpatialDimType') != 'COUNTRY' or r.get('Dim1') not in TOTALS:
            continue
        y, v = str(r.get('TimeDim')), r.get('NumericValue')
        if y in years and v is not None:
            by.setdefault(WHO_NAME.get(r['SpatialDim'], r['SpatialDim']), {})[y] = v
    save(name, subject, unit, years, [[c] + [v.get(y) for y in years] for c, v in by.items()])

# ------------------------------------------------------- Eurostat JSON-stat
def es(name, fn, subject, unit, sel, years=None, ratio_of=None):
    d = json.load(open(get(fn, dict(SOURCES)[fn])))
    ids, size, vals = d['id'], d['size'], d['value']
    idx = {k: d['dimension'][k]['category']['index'] for k in ids}
    for k in idx:
        if isinstance(idx[k], list):
            idx[k] = {c: i for i, c in enumerate(idx[k])}
    lab = d['dimension']['geo']['category'].get('label', {})
    strides = [1] * len(ids)
    for i in range(len(ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * size[i + 1]
    times = sorted(idx['time'], key=lambda t: idx['time'][t]) if 'time' in ids else [None]
    years = years or times

    def at(geo, t, sel):
        pos = 0
        for i, k in enumerate(ids):
            code = geo if k == 'geo' else (t if k == 'time' else sel.get(k))
            if code is None:
                code = sorted(idx[k], key=lambda c: idx[k][c])[0]
            if code not in idx[k]:
                return None
            pos += idx[k][code] * strides[i]
        return vals.get(str(pos))

    rows = []
    for g in sorted(idx['geo'], key=lambda g: idx['geo'][g]):
        if g in SKIP or len(g) > 3:
            continue
        series = [at(g, y, sel) for y in years]
        if ratio_of:
            den = [at(g, y, ratio_of) for y in years]
            series = [None if (a is None or not b) else 100.0 * a / b
                      for a, b in zip(series, den)]
        rows.append([lab.get(g, g)] + series)
    save(name, subject, unit, years, rows)

# ------------------------------------------- OECD SDMX-JSON (AllDimensions)
_cache = {}
def _oecd(fn):
    if fn not in _cache:
        d = json.load(open(get(fn, dict(SOURCES)[fn])))['data']
        _cache[fn] = d['structure'] if 'structure' in d else d['structures'][0], d['dataSets'][0]
    return _cache[fn]

def oecd(name, fn, subject, unit, years, want):
    struct, ds = _oecd(fn)
    dims = struct['dimensions']['observation']
    names = [x['id'] for x in dims]
    codes = [[v['id'] for v in x['values']] for x in dims]
    labs = [{v['id']: v.get('name', v['id']) for v in x['values']} for x in dims]
    ai, ti = names.index('REF_AREA'), names.index('TIME_PERIOD')
    by = {}
    for key, o in ds['observations'].items():
        k = [int(x) for x in key.split(':')]
        if any(codes[names.index(dim)][k[names.index(dim)]] != val
               for dim, val in want.items() if dim in names):
            continue
        y = codes[ti][k[ti]]
        if y not in years:
            continue
        area = codes[ai][k[ai]]
        if area in SKIP or len(area) > 3:
            continue
        by.setdefault(labs[ai].get(area, area), {})[y] = o[0]
    save(name, subject, unit, years, [[c] + [v.get(y) for y in years] for c, v in by.items()])

def oecd_dims(fn):
    struct, _ = _oecd(fn)
    for x in struct['dimensions']['observation']:
        vs = x['values']
        if x['id'] in ('REF_AREA', 'TIME_PERIOD'):
            print('   %-22s %d values' % (x['id'], len(vs))); continue
        print('   %-22s %d | %s' % (x['id'], len(vs),
              ', '.join('%s=%s' % (v['id'], v.get('name', '')[:22]) for v in vs[:6])))

def oecd_coverage(fn, want, lo=1970):
    """How many countries report in each year, so year choice is evidence-led."""
    struct, ds = _oecd(fn)
    dims = struct['dimensions']['observation']
    names = [x['id'] for x in dims]
    codes = [[v['id'] for v in x['values']] for x in dims]
    ti = names.index('TIME_PERIOD')
    cnt = {}
    for key in ds['observations']:
        k = [int(x) for x in key.split(':')]
        if any(codes[names.index(d)][k[names.index(d)]] != v
               for d, v in want.items() if d in names):
            continue
        y = codes[ti][k[ti]]
        if y.isdigit() and int(y) >= lo:
            cnt[y] = cnt.get(y, 0) + 1
    print('   ', ' '.join(f'{y}:{n}' for y, n in sorted(cnt.items())))

# ----------------------------------------------------------------- OWID CSV
def owid(name, fn, subject, unit, years, col=3):
    by = {}
    for r in csv.reader(open(get(fn, dict(SOURCES)[fn]))):
        if not r or r[0] == 'Entity' or len(r) <= col or not r[1] or r[0] in SKIP:
            continue
        if r[2] in years:
            try:
                by.setdefault(r[0], {})[r[2]] = float(r[col])
            except ValueError:
                pass
    save(name, subject, unit, years, [[c] + [v.get(y) for y in years] for c, v in by.items()])


Y = lambda *a: [str(x) for x in a]

def extract():
    who('tb',        'who_tb.json',         'Tuberculosis cases per 100,000',   'per 100k', Y(2000, 2023))
    who('measles',   'who_measles.json',    'Measles first-dose coverage',      '%',        Y(2000, 2023))
    who('maternal',  'who_maternal.json',   'Maternal deaths per 100,000',      'per 100k', Y(2000, 2023))
    who('stunting',  'who_stunting.json',   'Under-five stunting',              '%',        Y(2000, 2022))
    who('bp',        'who_bp.json',         'Raised blood pressure',            '%',        Y(1990, 2019))
    who('cleanfuel', 'who_cleanfuels.json', 'Cooking with clean fuels',         '%',        Y(2000, 2022))
    who('water',     'who_water.json',      'Safely managed drinking water',    '%',        Y(2000, 2022))
    who('le60',      'who_le60.json',       'Life expectancy at 60',            'years',    Y(2000, 2021))
    who('caries',    'who_caries.json',     'Untreated caries, adult teeth',    '%',        Y(2019))

    es('telework',  'es_telework.json',   'Usually working from home', '%',
       dict(unit='PC', sex='T', frequenc='USU', age='Y15-64', wstatus='EMP'), Y(2019, 2024))
    es('waste',     'es_waste.json',      'Municipal waste per person', 'kg',
       dict(unit='KG_HAB', wst_oper='GEN'), Y(2005, 2023))
    es('flats',     'es_flats.json',      'Population living in flats', '%',
       dict(unit='PC', building='FLAT', deg_urb='TOTAL', rskpovth='TOTAL'), Y(2024))
    es('wind',      'es_windelec.json',   'Wind electricity generated', 'GWh',
       dict(siec='RA300', nrg_bal='GEP', plants='ELC', operator='TOTAL', unit='GWH'), Y(2024))
    es('nights',    'es_nights.json',     'Nights in tourist accommodation per 1,000 people',
       'nights per 1,000', dict(c_resid='TOTAL', unit='P_THAB', nace_r2='I551-I553'), Y(2024))
    es('railgoods', 'es_railfreight.json','Rail freight moved', 'mio tkm',
       dict(unit='MIO_TKM'), Y(2023))
    es('foodprice', 'es_pricelevel.json', 'Food price level, EU27 = 100', 'index',
       dict(na_item='PLI_EU27_2020', ppp_cat='A0101'), Y(2024))
    es('neet',      'es_neet.json',       'Young people not in work or study', '%',
       dict(sex='T', age='Y15-29', wstatus='NEMP', training='NO_FE_NO_NFE', unit='PC'), Y(2010, 2024))
    es('cars',      'es_cars.json',       'Passenger cars per 1,000 people', 'cars',
       dict(unit='NR'), Y(2013, 2023))
    es('flowers',   'es_agriout.json',    'Flowers and plants, share of farm output', '%',
       dict(am_item='AM042000', indic_agr='PRD_BP', unit='MIO_EUR'), Y(1995, 2024),
       ratio_of=dict(am_item='AM160000', indic_agr='PRD_BP', unit='MIO_EUR'))
    es('books',     'es_books.json',      'Read no books in a year', '%',
       dict(n_book='0', lev_limit='TOTAL', sex='T', age='Y_GE16', unit='PC'), Y(2022))
    es('fertility', 'es_fertility.json',  'Total fertility rate', 'births',
       dict(indic_de='TOTFERRT'), Y(1990, 2023))
    es('fememp',    'es_fememp.json',     "Women's employment rate, 20-64", '%',
       dict(indic_em='EMP_LFS', sex='F', age='Y20-64', unit='PC_POP'), Y(2009, 2024))

    oecd('hours',   'oecd_hours.json',    'Annual hours worked per worker', 'hours',
         Y(1970, 2023), dict(MEASURE='HW', WORKER_STATUS='_T'))
    oecd('prod',    'oecd_prod.json',     'GDP per hour worked', 'USD PPP',
         Y(1970, 2023), dict(MEASURE='GDPHRS', UNIT_MEASURE='USD_PPP_H', ACTIVITY='_T',
              TRANSFORMATION='N', PRICE_BASE='V', CONVERSION_TYPE='PPP', ASSET_CODE='_Z'))
    oecd('consult', 'oecd_consult.json',  'Doctor consultations per person', 'per year',
         Y(2000, 2023), dict(OCCUPATION='OC221', CONSULTATION_TYPE='CIP'))
    oecd('mri',     'oecd_medtech.json',  'MRI units per million people', 'per 1m',
         Y(2010, 2023), dict(MEDICAL_TECH='MRI', UNIT_MEASURE='10P6HB', HEALTH_CARE_PROVIDER='_T'))
    oecd('wagegap', 'oecd_wagegap.json',  'Gender wage gap, median', '%',
         Y(2002, 2023), dict(AGGREGATION_OPERATION='MEDIAN'))
    oecd('gerd',    'oecd_msti.json',     'R&D spending as a share of GDP', '%',
         Y(2000, 2023), dict(MEASURE='G', UNIT_MEASURE='PT_B1GQ'))
    oecd('retage',  'oecd_pag.json',      'Effective labour market exit age', 'years',
         Y(2000, 2022), dict(MEASURE='ELMEA', UNIT_MEASURE='Y'))

    es('drinkprice','es_pricelevel.json','Alcohol and tobacco price level, EU27 = 100', 'index',
       dict(na_item='PLI_EU27_2020', ppp_cat='A0102'), Y(2024))
    oecd('pensions', 'oecd_pag.json',     'Public spending on pensions', '% of GDP',
         Y(2000, 2021), dict(MEASURE='PEP', UNIT_MEASURE='PT_B1GQ'))
    owid('coal',   'owid_coal_full.csv', 'Electricity from coal', '%', Y(2000, 2024))
    owid('height', 'owid_height.csv',    'Mean height of adult men', 'cm', Y(1900, 1996))



def extract_series():
    """Annual series for the forms that need a path rather than two endpoints."""
    who('cleanfuel_s', 'who_cleanfuels.json', 'Cooking with clean fuels', '%',
        Y(*range(2000, 2023)))
    who('water_s',     'who_water.json',      'Safely managed drinking water', '%',
        Y(*range(2000, 2023)))
    owid('coal_s',     'owid_coal_full.csv',  'Electricity from coal', '%',
         Y(*range(2000, 2025)))
    es('fertility_s',  'es_fertility.json',   'Total fertility rate', 'births',
       dict(indic_de='TOTFERRT'), Y(*range(2009, 2024)))
    es('fememp_s',     'es_fememp.json',      "Women's employment rate", '%',
       dict(indic_em='EMP_LFS', sex='F', age='Y20-64', unit='PC_POP'), Y(*range(2009, 2024)))
    oecd('hours_s',    'oecd_hours.json',     'Annual hours worked', 'hours',
         Y(*range(1995, 2024)), dict(MEASURE='HW', WORKER_STATUS='_T'))
    oecd('prod_s',     'oecd_prod.json',      'GDP per hour worked', 'USD PPP',
         Y(*range(1995, 2024)), dict(MEASURE='GDPHRS', UNIT_MEASURE='USD_PPP_H',
         ACTIVITY='_T', TRANSFORMATION='N', PRICE_BASE='V', CONVERSION_TYPE='PPP',
         ASSET_CODE='_Z'))


SPECS = [

# ------------------------------------------------------------------ WHO GHO
dict(slug='tb-incidence', src='tb', type='dumbbell', diff=3,
     family='Change over time', form='Dumbbell · 2000 → 2023',
     truth='New tuberculosis cases per 100,000 people, 2000 vs 2023',
     answer='New tuberculosis cases per 100,000 people',
     period='2000 → 2023', unit='new cases per 100,000 people a year',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/incidence-of-tuberculosis-per-100-000-population-per-year',
     pick=('list', ['Djibouti', 'Kiribati', 'Philippines', 'Cambodia', 'South Africa',
                    'Indonesia', 'India', 'Peru', 'Romania', 'Portugal',
                    'United Kingdom of Great Britain and Northern Ireland', 'Sweden']),
     decoys=['Malaria cases per 100,000 people',
             'Deaths from air pollution per 100,000 people',
             'Road deaths per 100,000 people',
             'People living with HIV per 100,000 people'],
     hints=['Kiribati sits in the middle of the Pacific, four thousand kilometres from '
            'the nearest mosquito worth worrying about.',
            'Three of these are European and all three have fallen a long way; whatever '
            'this is, it answers to housing and to antibiotics.',
            'Counted per 100,000 people per year. The top bar runs past 500.',
            'A bacterial lung infection, curable since the 1950s, still the deadliest '
            'infection on earth in most years.'],
     why='Tuberculosis incidence, from the WHO Global Health Observatory. The Pacific '
         'islands at the top rule out malaria, which does not reach them, and the '
         'European countries near the bottom have fallen by more than half since 2000.'),

dict(slug='measles-first-dose', src='measles', type='dumbbell', diff=2,
     family='Change over time', form='Dumbbell · 2000 → 2023',
     truth='Share of one-year-olds given a first dose of measles vaccine, 2000 vs 2023',
     answer='Share of one-year-olds given a first dose of measles vaccine',
     period='2000 → 2023', unit='% of one-year-olds',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/measles-containing-vaccine-first-dose-(mcv1)-immunization-coverage-among-1-year-olds-(-)',
     pick=('list', ['Hungary', 'Kazakhstan', 'Rwanda', 'Bangladesh', 'Brazil', 'India',
                    'Indonesia', 'Ethiopia', 'Nigeria', 'Democratic Republic of the Congo',
                    'Somalia', 'Chad']),
     decoys=['Share of births attended by a trained health worker',
             'Share of one-year-olds given a first dose of polio vaccine',
             'Share of children who reach their fifth birthday',
             'Share of households with a mosquito net'],
     hints=['Rwanda is near the top, which is not where a country with its recent history '
            'is expected to be.',
            'The gap between the two dots is widest in the countries with the least of '
            'everything else, and several sit above ninety in both years.',
            'A percentage of children of a single age, counted at twelve months.',
            'One jab, given at about a year old, against a disease that was universal '
            'within living memory.'],
     why='First-dose measles coverage. Rwanda near the top kills anything that tracks '
         'national income, and the ceiling at 99% rules out measures that have no '
         'natural maximum.'),

dict(slug='maternal-deaths-rank', src='maternal', type='slope', diff=4,
     family='Ranking', form='Rank slope · 2000 → 2023',
     truth='World ranking by deaths in childbirth per 100,000 births, 2000 vs 2023',
     answer='World ranking by deaths in childbirth per 100,000 births',
     period='2000 → 2023', unit='rank, worst first',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/maternal-mortality-ratio-(per-100-000-live-births)',
     pick=('rank', ['South Sudan', 'Chad', 'Nigeria', 'Sierra Leone', 'Afghanistan',
                    'Somalia', 'Central African Republic', 'Rwanda', 'Cambodia',
                    'Bangladesh']),
     decoys=['World ranking by deaths from malaria per 100,000 people',
             'World ranking by the share of children who are underweight',
             'World ranking by deaths from unsafe water per 100,000 people',
             'World ranking by the share of births in a hospital'],
     hints=['Rwanda and Cambodia both climb away from the top of this list, and both '
            'ended a war in the decade before it starts.',
            'Afghanistan holds its position while its neighbours improve, which points at '
            'something that needs a clinic rather than a drug.',
            'A rank, worst first, out of every country with an estimate.',
            'It is measured per 100,000 live births, and it is counted only among women.'],
     why='Maternal mortality ranking. Counting per live birth rather than per head is the '
         'giveaway, and the two countries that climb fastest are the two that rebuilt '
         'rural health services after a war.'),

dict(slug='under-five-stunting-change', src='stunting', type='deviation', diff=3,
     reference=0,
     family='Deviation', form='Diverging bar · change between 2000 and 2022',
     truth='Change in the share of under-fives who are too short for their age, 2000 to 2022',
     answer='Change in the share of under-fives who are too short for their age',
     period='2000 → 2022', unit='percentage points, 2000 to 2022', delta=True,
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/gho-jme-stunting-prevalence',
     pick=('list', ['Australia', 'Germany', 'Peru', 'China', 'Viet Nam',
                    'Bangladesh', 'Nepal', 'Cambodia', 'Rwanda', 'Ethiopia', 'Burundi',
                    'Nigeria', 'India', 'Indonesia', 'Egypt', 'Mexico', 'Guatemala',
                    'Malawi', 'Yemen', 'United Republic of Tanzania']),
     decoys=['Change in the share of under-fives who are underweight',
             'Change in the share of adults who cannot read',
             'Change in the share of people without enough to eat',
             'Change in the share of children out of school'],
     hints=['Almost every bar points the same way, which is rarer in this game than it '
            'ought to be.',
            'The bars nearest the line belong to the rich countries, not because nothing '
            'changed there but because there was nothing left to change.',
            'Percentage points, not per cent: the difference between two shares taken '
            'twenty-two years apart.',
            'It is measured with a tape rather than a set of scales, and it is the slow '
            'measure, not the emergency one.'],
     why='Change in stunting prevalence. Height for age is the chronic measure and weight '
         'for height is the acute one; the near-universal improvement is what rules out '
         'the hunger measures, which did not move like this.'),

dict(slug='raised-blood-pressure', src='bp', type='deviation', diff=4,
     family='Deviation', form='Diverging bar · distance from the world average, 2019',
     truth='Share of adults with raised blood pressure, 2019', reference=31,
     answer='Share of adults with raised blood pressure',
     period='2019', unit='% of adults, against a 31% world average', suffix='%',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/raised-blood-pressure-(sbp-140-or-dbp-90)-(age-standardized-estimate)',
     pick=('list', ['Lithuania', 'Belarus', 'Republic of Moldova', 'Croatia',
                    'Hungary', 'Poland', 'Romania', 'Nigeria', 'South Africa', 'Germany',
                    'France', 'Brazil', 'India', 'China', 'Peru', 'Ecuador', 'Japan',
                    'United States of America',
                    'United Kingdom of Great Britain and Northern Ireland', 'Canada']),
     decoys=['Share of adults with high cholesterol',
             'Share of adults with diabetes',
             'Share of adults with anaemia',
             'Share of adults who have never had a health check'],
     hints=['The countries furthest above the line are the ones where the Soviet Union '
            'used to be.',
            'China and Peru sit furthest below the line, and neither is a country anyone '
            'would nominate as the healthiest on the chart.',
            'A percentage of all adults, measured against a world average of 31.',
            'It is diagnosed with a cuff, it usually has no symptoms, and it is the '
            'largest single cause of death on earth.'],
     why='Raised blood pressure, age-standardised. The eastern European countries at the '
         'top and the wealthy ones below the line are the wrong way round for obesity or '
         'inactivity, which is what rules those two out.'),

dict(slug='clean-cooking-fuels', src='cleanfuel', type='line', diff=2,
     family='Change over time', form='Multi-line · 2000–2022', startYear=2000,
     truth='Share of people who cook with clean fuels, 2000–2022',
     answer='Share of people who cook with clean fuels',
     period='2000–2022', unit='% of the population', suffix='%',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/proportion-of-population-with-primary-reliance-on-clean-fuels-and-technologies-for-cooking-(-)',
     pick=('series', ['Indonesia', 'India', 'China', 'Nigeria', 'Ethiopia']),
     decoys=['Share of people with electricity at home',
             'Share of people with a bank account',
             'Share of people using the internet',
             'Share of people with a flushing toilet'],
     hints=['Indonesia climbs almost vertically in the middle of the 2000s, which is what '
            'a government deciding something looks like.',
            'Ethiopia barely moves while everything else in the chart improves, and that '
            'flat line is a rural population that still burns wood.',
            'A percentage of the whole population, from 2000 to 2022.',
            'It is about what happens in the kitchen, and the alternative fills the room '
            'with smoke.'],
     why='Clean cooking fuel access. Indonesia\'s near-vertical climb is the 2007 kerosene '
         'to LPG conversion programme; electricity access does not have that shape.'),

dict(slug='safely-managed-water', src='water', type='line', diff=3,
     family='Change over time', form='Multi-line · 2000–2022', startYear=2000,
     truth='Share of people with safely managed drinking water, 2000–2022',
     answer='Share of people with safely managed drinking water',
     period='2000–2022', unit='% of the population', suffix='%',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/population-using-safely-managed-drinking-water-services-(-)',
     pick=('series', ['United Kingdom of Great Britain and Northern Ireland',
                      'Mexico', 'India', 'Uganda', 'United Republic of Tanzania']),
     decoys=['Share of people with a toilet connected to a sewer',
             'Share of people with electricity at home',
             'Share of people living in a city',
             'Share of people with a mobile phone'],
     hints=['Two of these lines sit below ten for the whole period, which is a very low '
            'floor for anything a household can simply buy.',
            'India climbs steeply after 2014 while Tanzania stays flat, and the thing '
            'being counted has to be delivered to the house rather than carried to it.',
            'A percentage of the whole population, from 2000 to 2022.',
            'Available when needed, free from contamination, and on the premises: all '
            'three conditions, or it does not count.'],
     why='Safely managed drinking water. The three-part definition is strict enough that '
         'rich countries sit near 100 and the East African floor stays near zero, which '
         'no mobile phone or electricity series does.'),

dict(slug='life-expectancy-at-60', src='le60', type='dumbbell', diff=4,
     family='Change over time', form='Dumbbell · 2000 → 2021',
     truth='Years a sixty-year-old can expect to live, 2000 vs 2021',
     answer='Years a sixty-year-old can expect to live',
     period='2000 → 2021', unit='further years of life at age 60',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/life-expectancy-at-age-60-(years)',
     pick=('list', ['Japan', 'Switzerland', 'Australia', 'Spain', 'United States of America',
                    'China', 'Brazil', 'India', 'South Africa', 'Nigeria',
                    'Central African Republic', 'Somalia']),
     decoys=['Years a person can expect to live in good health',
             'Years a person can expect to spend in retirement',
             'Average age at death',
             'Average age of retirement'],
     hints=['The whole chart is squeezed into a band about twelve units wide, which is '
            'narrow for a measure that usually separates Japan from Somalia by forty.',
            'Nothing on this chart is above twenty-five, and the poorest countries are '
            'closer to the richest here than they are on almost any other health measure.',
            'Measured in years, and the largest value is under twenty-five.',
            'It starts counting at sixty rather than at birth, which is why the range is '
            'so compressed.'],
     why='Life expectancy at sixty. The magnitude does all the work: a chart topping out '
         'near 25 cannot be life expectancy at birth, and the compression is the point.'),

dict(slug='untreated-caries', src='caries', type='beeswarm', diff=3, deadpan=True,
     family='Distribution', form='Beeswarm · every country, 2019',
     truth='Share of people with untreated decay in their adult teeth, 2019',
     answer='Share of people with untreated decay in their adult teeth',
     period='2019', unit='% of people aged five and over', suffix='%',
     source='WHO Global Health Observatory',
     sourceUrl='https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-untreated-caries-of-permanent-teeth-in-people-5-years-(-)',
     pick=('all',),
     label=['Chile', 'Romania', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland', 'Nigeria', 'Malaysia'],
     labelSm=['Chile', 'United States of America', 'Malaysia'],
     decoys=['Share of adults who have lost all their natural teeth',
             'Share of adults who see a dentist in a given year',
             'Share of adults who are short-sighted',
             'Share of children with decay in their milk teeth'],
     hints=['The spread from one end of this chart to the other is about twenty-eight '
            'points, which is a remarkably even distribution of human misfortune.',
            'Rich and poor countries are mixed together from one end of the chart to the '
            'other, so money does not buy a way out of this one.',
            'A percentage of everyone aged five and over, in a single year.',
            'It is the commonest disease on the planet, and it is treated with a drill.'],
     why='Untreated caries in permanent teeth. The lack of an income gradient is the '
         'discriminator: tooth loss and dentist visits both sort by wealth, and this '
         'does not.'),

# ------------------------------------------------------------------ Eurostat
dict(slug='usually-working-from-home', src='telework', type='dumbbell', diff=2,
     family='Change over time', form='Dumbbell · 2019 → 2024',
     truth='Share of employed people who usually work from home, 2019 vs 2024',
     answer='Share of employed people who usually work from home',
     period='2019 → 2024', unit='% of people in work', suffix='%',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/lfsa_ehomp',
     pick=('list', ['Netherlands', 'Finland', 'Luxembourg', 'Ireland', 'Belgium', 'Sweden',
                    'France', 'Germany', 'Spain', 'Italy', 'Poland', 'Romania', 'Bulgaria']),
     decoys=['Share of employed people who are self-employed',
             'Share of employed people on a temporary contract',
             'Share of employed people working part time',
             'Share of employed people in the public sector'],
     hints=['Every dot on this chart moved the same way between the two years, and the '
            'reason had a name.',
            'The bottom of the chart is under one per cent in the first year, which no '
            'ordinary feature of a labour market ever is.',
            'A percentage of everyone in work, in 2019 and again in 2024.',
            'The rise is not evenly spread: it went to the countries with the most desks '
            'and the fastest broadband.'],
     why='Usually working from home. The floor below one per cent in 2019 rules out '
         'part-time and temporary work, neither of which was ever that rare anywhere.'),

dict(slug='municipal-waste-rank', src='waste', type='slope', diff=3, deadpan=True,
     family='Ranking', form='Rank slope · 2005 → 2023',
     truth='European ranking by household waste thrown away per person, 2005 vs 2023',
     answer='European ranking by household waste thrown away per person',
     period='2005 → 2023', unit='rank, most first',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/env_wasmun',
     pick=('rank', ['Denmark', 'Ireland', 'Cyprus', 'Austria', 'Germany', 'France',
                    'Italy', 'Spain', 'Poland', 'Czechia', 'Slovakia', 'Romania']),
     decoys=['European ranking by electricity used per person',
             'European ranking by water used per person',
             'European ranking by packaging recycled per person',
             'European ranking by money spent on food per person'],
     hints=['The countries at the top of this list are the ones that would score best on '
            'almost any environmental measure you could name.',
            'Romania and Slovakia sit at the bottom, and it is not because they are '
            'careful.',
            'A rank, most first, among the European countries that report it.',
            'It is weighed at the kerb, in kilograms per person per year, and the number '
            'goes up as a country gets richer.'],
     why='Municipal waste generated per person. The ranking is close to the income '
         'ranking, which is the joke: the countries at the top are the ones with the best '
         'recycling rates and the most rubbish.'),

dict(slug='population-living-in-flats', src='flats', type='beeswarm', diff=2, deadpan=True,
     family='Distribution', form='Beeswarm · every reporting country, 2024',
     truth='Share of people who live in a flat rather than a house, 2024',
     answer='Share of people who live in a flat rather than a house',
     period='2024', unit='% of the population', suffix='%',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/ilc_lvho01',
     pick=('all',),
     label=['Spain', 'Latvia', 'Germany', 'France', 'Netherlands', 'Ireland'],
     labelSm=['Spain', 'Germany', 'Ireland'],
     decoys=['Share of people who rent rather than own their home',
             'Share of people living in a household of one',
             'Share of people living in a home built since 2000',
             'Share of people living in an overcrowded home'],
     hints=['Spain and Latvia sit side by side at the top of this chart, which is not a '
            'pairing that many measures produce.',
            'Ireland is alone at the bottom, under ten, and the Netherlands is not far '
            'above it.',
            'A percentage of the whole population, in a single year.',
            'It is about the building rather than the household, and the answer is either '
            'one storey of it or all of them.'],
     why='Population living in flats. Spain and Latvia together rule out tenure and '
         'household size, which sort those two countries very differently; Ireland at '
         'under ten is the killer for anything about age or crowding of housing.'),

dict(slug='eu-wind-electricity', src='wind', type='treemap', diff=3,
     family='Part-to-whole', form='Treemap · share of the European total, 2024',
     truth='Electricity generated from wind, by country, 2024',
     answer='Electricity generated from wind, by country',
     period='2024', unit='gigawatt hours',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_pehnf',
     pick=('top', 12),
     decoys=['Electricity generated from water, by country',
             'Electricity generated from the sun, by country',
             'Electricity generated from nuclear power, by country',
             'Electricity generated from gas, by country'],
     hints=['Denmark is far larger here than a country of six million has any business '
            'being.',
            'France is third rather than first, which settles one of the four options on '
            'its own, and Norway and Austria are nowhere.',
            'Gigawatt hours in a single year, summing to the European total.',
            'The countries that do best are flat, coastal and windy, and the mountainous '
            'ones are missing.'],
     why='Wind generation by country. France third rather than first rules out nuclear; '
         'the absence of Norway and Austria, the two hydro giants, rules out water; and '
         'Denmark far above its weight is the signature of wind.'),

dict(slug='eu-rail-freight', src='railgoods', type='treemap', diff=3,
     family='Part-to-whole', form='Treemap · share of the European total, 2023',
     truth='Goods moved by rail, by country, 2023',
     answer='Goods moved by rail, by country',
     period='2023', unit='million tonne-kilometres',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/rail_go_total',
     pick=('top', 12),
     decoys=['Goods moved by lorry, by country',
             'Goods moved through seaports, by country',
             'Length of motorway, by country',
             'Passengers carried by rail, by country'],
     hints=['The second largest block belongs to a country at war, and the freight kept '
            'moving.',
            'Poland is enormous here and the Netherlands is small, which is the reverse of '
            'how goods usually rank in Europe.',
            'Million tonne-kilometres in a year: a tonne carried a kilometre, summed.',
            'The countries that dominate are the ones with coal, heavy industry and a '
            'nineteenth-century network still in daily use.'],
     why='Rail freight in tonne-kilometres. The Netherlands being small rules out '
         'seaports and lorries, both of which it leads per head; Ukraine second is the '
         'shape of a coal and grain network.'),

dict(slug='eu-tourist-nights', src='nights', type='symbol', diff=2, deadpan=True,
     family='Magnitude', form='Proportional symbols · the twelve largest, 2024',
     truth='Nights spent in tourist accommodation per 1,000 residents, 2024',
     answer='Nights spent in tourist accommodation per 1,000 residents',
     period='2024', unit='nights per 1,000 residents',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/tour_occ_ninat',
     pick=('top', 12),
     decoys=['Visitors arriving from abroad per 1,000 residents',
             'Money spent by visitors from abroad per resident',
             'Hotel beds per 1,000 residents',
             'People working in hotels and restaurants per 1,000 residents'],
     hints=['Malta is smaller than the Isle of Wight and it is second on this chart.',
            'The big countries are missing altogether, so whatever this is has been '
            'divided by the number of people who live there.',
            'A count per 1,000 residents, summed across every hotel, campsite and '
            'holiday let.',
            'A fortnight on a beach counts fourteen times; a weekend in a capital counts '
            'twice.'],
     why='Nights in tourist accommodation per 1,000 residents. Dividing by population '
         'is what puts Croatia, Malta and Cyprus at the top and leaves the large '
         'countries off the chart entirely.'),

dict(slug='food-price-level', src='foodprice', type='deviation', diff=3,
     family='Deviation', form='Diverging bar · distance from the European average, 2024',
     truth='Cost of the same basket of food, 2024', reference=100,
     answer='Cost of the same basket of food',
     period='2024', unit='price level, EU average = 100',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/prc_ppp_ind',
     pick=('list', ['Switzerland', 'Iceland', 'Norway', 'Luxembourg', 'Denmark',
                    'Ireland', 'Austria', 'Finland', 'Sweden', 'Germany', 'France', 'Italy',
                    'Netherlands', 'Spain', 'Greece', 'Czechia', 'Poland', 'Hungary',
                    'Romania', 'Türkiye']),
     decoys=['Average wage, against the European average',
             'Cost of the same basket of clothes',
             'Share of household spending that goes on food',
             'Cost of renting the same flat'],
     hints=['Switzerland is a long way out on its own, further than any member of the '
            'union it is not in.',
            'Romania and Poland sit well below the line while their wages sit further '
            'below it still.',
            'An index with the European average set at 100.',
            'It is the same trolley in every country, priced in a common currency, with '
            'nothing about what anyone earns.'],
     why='Food price level index, EU27 = 100. The eastern countries are much closer to '
         'the line on prices than on wages, which is what rules out the earnings decoy.'),

dict(slug='drink-price-level', src='drinkprice', type='deviation', diff=3,
     family='Deviation', form='Diverging bar · distance from the European average, 2024',
     truth='Cost of the same drink and cigarettes, 2024', reference=100,
     answer='Cost of the same drink and cigarettes',
     period='2024', unit='price level, EU average = 100',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/prc_ppp_ind',
     pick=('list', ['Iceland', 'Norway', 'Ireland', 'Finland', 'Sweden', 'Denmark',
                    'France', 'Germany', 'Netherlands', 'Austria', 'Italy', 'Spain',
                    'Greece', 'Czechia', 'Poland', 'Hungary', 'Romania', 'Bulgaria',
                    'Portugal', 'Türkiye']),
     decoys=['Price of the same litre of petrol',
             'Price of the same restaurant meal',
             'Duty collected per adult',
             'Money spent in pubs and bars per adult'],
     hints=['Ireland and Finland sit far above a line that Germany and Italy sit close to, '
            'and none of it is about how the stuff is made.',
            'The spread here is wider than for food, and the countries at the top are the '
            'ones with the strongest temperance movements.',
            'An index with the European average set at 100.',
            'Almost all of the difference between the top and the bottom of this chart is '
            'duty.'],
     why='Price level index for alcohol and tobacco. Excise duty, not production cost, '
         'sets the order, which is why the Nordic countries and Ireland sit so far above '
         'a line that the wine-growing countries sit below.'),

dict(slug='neet-change', src='neet', type='deviation', diff=3, reference=0,
     family='Deviation', form='Diverging bar · change between 2010 and 2024',
     truth='Change in the share of young people not in work or education, 2010 to 2024',
     answer='Change in the share of young people not in work or education',
     period='2010 → 2024', unit='percentage points, 2010 to 2024', delta=True,
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20',
     pick=('list', ['Türkiye', 'North Macedonia', 'Serbia', 'Italy', 'Spain', 'Romania',
                    'Bulgaria', 'Greece', 'France', 'Poland', 'Germany', 'Netherlands',
                    'Sweden', 'Ireland', 'Portugal', 'Czechia', 'Hungary', 'Croatia',
                    'Norway', 'Denmark']),
     decoys=['Change in the share of young people living with their parents',
             'Change in the share of young people in higher education',
             'Change in the share of workers on a temporary contract',
             'Change in the share of young people out of work'],
     hints=['The starting year was chosen badly on purpose: it is the worst year Europe '
            'had in a generation.',
            'Almost every bar points the same way, and the longest of them belong to the '
            'countries that had the furthest to fall.',
            'Percentage points between two years, not a level.',
            'It counts the people who are doing neither of the two things a person that '
            'age is expected to be doing.'],
     why='Change in the NEET rate for 15 to 29 year olds. The measure counts people in '
         'neither employment nor education, which is why it is not the same as youth '
         'unemployment: a student without a job is not counted here.'),

dict(slug='passenger-cars-per-thousand', src='cars', type='dumbbell', diff=2, deadpan=True,
     family='Change over time', form='Dumbbell · 2013 → 2023',
     truth='Passenger cars per 1,000 people, 2013 vs 2023',
     answer='Passenger cars per 1,000 people',
     period='2013 → 2023', unit='cars per 1,000 people',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carhab',
     pick=('list', ['Luxembourg', 'Italy', 'Finland', 'Poland', 'Germany', 'Austria',
                    'Spain', 'France', 'Netherlands', 'Denmark', 'Hungary', 'Romania',
                    'Latvia', 'Türkiye']),
     decoys=['Households with a washing machine per 1,000 people',
             'Mobile phone contracts per 1,000 people',
             'Bicycles sold per 1,000 people',
             'Households per 1,000 people'],
     hints=['Every single value on this chart is under eight hundred, and most of them '
            'went up over the ten years.',
            'The Netherlands and Denmark sit well below Poland, which is not where the '
            'rich countries usually are.',
            'A count per 1,000 people, in 2013 and again in 2023.',
            'Luxembourg is first partly because a great many of them are registered to '
            'companies rather than to people.'],
     why='Passenger cars per 1,000 inhabitants. The ceiling under 800 rules out mobile '
         'contracts, which pass 1,000 in several of these countries, and the cycling '
         'countries sitting low is the shape that fits cars.'),

dict(slug='flowers-share-of-farm-output', src='flowers', type='dumbbell', diff=4, deadpan=True,
     family='Change over time', form='Dumbbell · 1995 → 2024',
     truth='Share of a country\'s farm output that is flowers and ornamental plants, 1995 vs 2024',
     answer='Share of a country\'s farm output that is flowers and ornamental plants',
     period='1995 → 2024', unit='% of the value of agricultural output', suffix='%',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/aact_eaa01',
     pick=('list', ['Netherlands', 'Italy', 'Germany', 'Belgium', 'Denmark', 'France',
                    'Spain', 'Portugal', 'Ireland', 'Lithuania', 'Bulgaria']),
     decoys=['Share of a country\'s farm output that is fruit',
             'Share of a country\'s farm output that is wine',
             'Share of a country\'s farm output that is milk',
             'Share of a country\'s farm output that is sold abroad'],
     hints=['One of these is four times the next, and it built the world\'s largest '
            'auction house for the purpose.',
            'Spain and Italy are near the bottom, which rules out anything that needs '
            'sun.',
            'A percentage of the value of everything the country\'s farms produce.',
            'It is grown under glass, sold by the stem, and worth more per hectare than '
            'anything else in the accounts.'],
     why='Flowers and ornamental plants as a share of agricultural output. The '
         'Netherlands at four times the next country is the Aalsmeer auction; the '
         'Mediterranean countries sitting low is what rules out fruit and wine.'),

dict(slug='read-no-books', src='books', type='beeswarm', diff=2, deadpan=True,
     family='Distribution', form='Beeswarm · every reporting country, 2022',
     truth='Share of adults who read no books in a year, 2022',
     answer='Share of adults who read no books in a year',
     period='2022', unit='% of people aged 16 and over', suffix='%',
     source='Eurostat', sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/ilc_scp33',
     pick=('all',),
     label=['Romania', 'Türkiye', 'Italy', 'France', 'Denmark', 'Switzerland'],
     labelSm=['Romania', 'Italy', 'Switzerland'],
     decoys=['Share of adults who did not go to a cinema, theatre or concert in a year',
             'Share of adults who did not take a holiday in a year',
             'Share of adults who never use the internet',
             'Share of adults with no qualifications'],
     hints=['The best-performing country on this chart still has nearly one adult in five '
            'on the wrong side of it.',
            'Even the Nordic countries cannot get below a quarter, which puts a floor '
            'under this that the internet measure does not have.',
            'A percentage of everyone aged sixteen and over, asked about the last twelve '
            'months.',
            'One in the twelve months is enough to be counted on the right side of it.'],
     why='Share reading no books in the previous year. The floor near twenty is the '
         'discriminator: never using the internet is in low single figures across the '
         'Nordics, and this cannot get anywhere near that.'),

dict(slug='births-and-womens-work', src=('fememp', 'fertility'), type='scatter', diff=4,
     family='Change over time', form='Connected scatterplot · 2009 → 2023',
     truth='Births per woman against the share of women in work, 2009 to 2023',
     answer='Births per woman against the share of women in work',
     period='2009 → 2023',
     unit='horizontal: % of women aged 20 to 64 in work. vertical: births per woman',
     xUnit='%', yUnit='births',
     source='Eurostat',
     sourceUrl='https://ec.europa.eu/eurostat/databrowser/view/demo_find',
     pick=('paths', ['Germany', 'Spain', 'Sweden', 'Poland', 'Italy', 'Hungary']),
     decoys=['Births per woman against the share of women in higher education',
             'Age at first birth against the share of women in work',
             'Births per woman against the share of births outside marriage',
             'Births per woman against average household income'],
     hints=['Every path here drifts to the right over the fifteen years, and most of them '
            'drift downwards at the same time.',
            'Hungary is the one path that climbs, and it did so while spending more on '
            'families than any other country in Europe.',
            'The horizontal axis is a percentage and runs to the high seventies; the '
            'vertical one never passes two.',
            'The old story was that one of these two things had to fall for the other to '
            'rise. The chart says otherwise.'],
     why='Fertility against female employment, 2009 to 2023, one path per country. The '
         'vertical axis topping out below two rules out anything measured in years or '
         'percentages, and Hungary is the only country whose path climbs.'),

# ---------------------------------------------------------------------- OECD
dict(slug='hours-and-output', src=('hours', 'prod'), type='scatter', diff=5,
     family='Change over time', form='Connected scatterplot · 1995 → 2023',
     truth='Hours worked against output per hour, 1995 to 2023',
     answer='Hours worked against output per hour',
     period='1995 → 2023',
     unit='horizontal: hours worked a year per worker. vertical: US dollars of output an hour',
     xUnit='hours', yUnit='$',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_PDB%40DF_PDB',
     pick=('paths', ['Germany', 'Japan', 'United States', 'Mexico', 'Netherlands',
                     'France']),
     decoys=['Hours worked against average pay',
             'Hours worked against the share of workers in industry',
             'Days of holiday against output per hour',
             'Hours worked against the share of workers who are women'],
     hints=['The Mexican path sits further right than anything else here and has spent '
            'thirty years going almost nowhere.',
            'Every path moves left over time, and the vertical axis is denominated in the '
            'same thing everywhere because it has been converted.',
            'The horizontal axis is a count of hours in a year and runs past two thousand; '
            'the vertical one is in US dollars.',
            'Divide the second by nothing and you get the first back: one is time, the '
            'other is what the time produced.'],
     why='Annual hours worked against GDP per hour, PPP converted. The horizontal axis '
         'running past 2,000 can only be hours in a year, which rules out the holiday '
         'and pay readings.'),

dict(slug='doctor-consultations', src='consult', type='dumbbell', diff=2, deadpan=True,
     family='Change over time', form='Dumbbell · 2000 → 2023',
     truth='Times a year the average person sees a doctor, 2000 vs 2023',
     answer='Times a year the average person sees a doctor',
     period='2000 → 2023', unit='in-person consultations per person per year',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_HEALTH_PROC%40DF_CONSULT',
     pick=('list', ['Japan', 'Hungary', 'Germany', 'Netherlands', 'France', 'Poland',
                    'Canada', 'Portugal', 'United States', 'Mexico', 'Chile',
                    'Costa Rica']),
     decoys=['Prescriptions filled per person per year',
             'Nights spent in hospital per person per year',
             'Trips to a dentist per person per year',
             'Visits to a pharmacy per person per year'],
     hints=['The top of this chart is roughly once a month, every month, for everybody.',
            'The United States is in the lower half, well below Hungary, which is not the '
            'order that spending per head would give you.',
            'A count per person per year, in 2000 and again in 2023.',
            'It is the appointment itself that is counted, not what was written at the '
            'end of it.'],
     why='Japan\'s 12.4 visits a year is about one a month for every person in the '
         'country, and it holds because appointments need no referral, cost the patient '
         'little and are correspondingly short. The United States sits at 3.6 while '
         'spending more per head on health than anyone else on the chart, which is the '
         'clearest evidence in the pool that this measures how a system is paid rather '
         'than how good it is: fee-per-visit systems count many short appointments, '
         'salaried and capitated ones count few long ones. The Netherlands nearly doubled '
         'over the period, almost all of it telephone and video contacts that the count '
         'now includes.'),

dict(slug='mri-scanners', src='mri', type='dumbbell', diff=3, deadpan=True,
     family='Change over time', form='Dumbbell · 2010 → 2023',
     truth='MRI scanners per million people, 2010 vs 2023',
     answer='MRI scanners per million people',
     period='2010 → 2023', unit='machines per million people',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_HEALTH_REAC_HOSP%40DF_MED_TECH',
     pick=('list', ['Germany', 'Greece', 'Italy', 'Korea', 'Austria', 'Finland',
                    'Spain', 'France', 'Netherlands', 'Ireland', 'Poland', 'Mexico']),
     decoys=['Hospitals per million people',
             'Ambulances per million people',
             'Operating theatres per million people',
             'Pharmacies per million people'],
     hints=['Greece is second on this chart and has been since the machines arrived, '
            'which is not a story about the strength of its health service.',
            'Nothing on this chart passes thirty per million, so whatever is being '
            'counted is expensive and there is not much of it.',
            'A count per million people, in 2010 and again in 2023.',
            'It is a magnet the size of a room, and the queue for it is the usual '
            'political argument.'],
     why='MRI units per million. The magnitude under thirty rules out pharmacies and '
         'hospitals; Greece second is a well-known artefact of private clinics buying '
         'machines faster than the state could regulate them.'),

dict(slug='gender-wage-gap-rank', src='wagegap', type='slope', diff=3,
     family='Ranking', form='Rank slope · 2002 → 2023',
     truth='Ranking by the gap between men\'s and women\'s median pay, 2002 vs 2023',
     answer='Ranking by the gap between men\'s and women\'s median pay',
     period='2002 → 2023', unit='rank, widest gap first',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_EARNINGS%40GENDER_WAGE_GAP',
     pick=('rank', ['Korea', 'Japan', 'United States', 'United Kingdom', 'Finland',
                    'Germany', 'Austria', 'Italy', 'Hungary', 'Czechia']),
     decoys=['Ranking by the share of managers who are women',
             'Ranking by the gap between graduate and non-graduate pay',
             'Ranking by the share of women working part time',
             'Ranking by the share of parliamentary seats held by women'],
     hints=['Korea has held first place on this list for the whole of the present '
            'century.',
            'Italy is near the bottom, and it is not a country anyone would nominate as '
            'the most equal in Europe.',
            'A rank, largest first, among the countries that report it.',
            'It compares the middle man with the middle woman and reports the difference '
            'as a share of his pay.'],
     why='Gender wage gap at the median. Italy near the bottom is the trap: a low gap '
         'there reflects how few women are in the measured workforce, which is why the '
         'managers and part-time decoys sort differently.'),

dict(slug='rd-spending-deviation', src='gerd', type='deviation', diff=3,
     family='Deviation', form='Diverging bar · distance from the OECD average, 2023',
     truth='Spending on research and development, 2023', reference=2.0,
     answer='Spending on research and development',
     period='2023', unit='% of GDP, against a 2% reference line', suffix='%',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_MSTI%40DF_MSTI',
     pick=('list', ['Israel', 'Korea', 'Japan', 'United States', 'Germany',
                    'Austria', 'Belgium', 'Finland', 'France', 'Netherlands',
                    'United Kingdom', 'Switzerland', 'Iceland', 'Italy', 'Spain', 'Czechia',
                    'Portugal', 'Poland', 'Hungary', 'Romania']),
     decoys=['Government spending on universities',
             'Spending on defence',
             'Spending on machinery and equipment by business',
             'Money received from patents and licences'],
     hints=['Israel and Korea are first and second, and neither of them is large.',
            'The countries below the line include several with large armies, which '
            'settles one of the options.',
            'A percentage of GDP, drawn against a 2% line.',
            'Most of the money in this measure is spent by companies rather than by '
            'governments.'],
     why='Gross domestic expenditure on R&D as a share of GDP. Israel and Korea at the '
         'top with their defence-heavy neighbours below the line is what rules out the '
         'military reading.'),

dict(slug='retirement-age-rank', src='retage', type='slope', diff=4,
     family='Ranking', form='Rank slope · 2000 → 2022',
     truth='Ranking by the age at which people actually stop working, 2000 vs 2022',
     answer='Ranking by the age at which people actually stop working',
     period='2000 → 2022', unit='rank, latest first',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_PAG%40DF_PAG',
     pick=('rank', ['Indonesia', 'Korea', 'Japan', 'Mexico', 'United States', 'Sweden',
                    'Germany', 'France', 'Slovenia', 'Hungary']),
     decoys=['Ranking by the official state pension age',
             'Ranking by the share of over-65s still in work',
             'Ranking by years spent in retirement',
             'Ranking by the age at which people leave education'],
     hints=['The countries at the top of this list are not the ones with the oldest '
            'pension ages; several of them barely have a state pension at all.',
            'France and Slovenia sit at the bottom in both years, and France\'s official '
            'figure is nowhere near that low.',
            'A rank, latest first, among the OECD countries.',
            'It is measured from what people did, not from what the law says they should '
            'do.'],
     why='Effective labour market exit age. The whole puzzle is the gap between the '
         'statutory pension age and the age people actually leave, which is why the '
         'official-age decoy sorts the countries quite differently.'),

dict(slug='pension-spending', src='pensions', type='dumbbell', diff=3,
     family='Change over time', form='Dumbbell · 2000 → 2021',
     truth='Public spending on pensions as a share of the economy, 2000 vs 2021',
     answer='Public spending on pensions as a share of the economy',
     period='2000 → 2021', unit='% of GDP', suffix='%',
     source='OECD', sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_PAG%40DF_PAG',
     pick=('list', ['Italy', 'Greece', 'France', 'Austria', 'Portugal', 'Germany', 'Japan',
                    'Poland', 'United Kingdom', 'United States', 'Korea', 'Ireland',
                    'Mexico']),
     decoys=['Public spending on health as a share of the economy',
             'Public spending on education as a share of the economy',
             'Public spending on unemployment benefits as a share of the economy',
             'Total tax collected as a share of the economy'],
     hints=['Korea and Mexico are at the bottom of this chart and both are ageing faster '
            'than the countries at the top.',
            'The United States sits mid-table while spending more than anyone on the '
            'thing one of the other options describes.',
            'A percentage of GDP, in 2000 and again in 2021.',
            'It is the largest single line in the budget of most of the countries at the '
            'top of this chart.'],
     why='Public pension expenditure. The United States mid-table is the discriminator: '
         'on health it would be first by a distance, and on pensions it is unremarkable.'),

# ---------------------------------------------------------------------- OWID
dict(slug='electricity-from-coal', src='coal', type='line', diff=3, startYear=2000,
     family='Change over time', form='Multi-line · 2000–2024',
     truth='Share of electricity generated from coal, 2000–2024',
     answer='Share of electricity generated from coal',
     period='2000–2024', unit='% of electricity generated', suffix='%',
     source='Our World in Data', sourceUrl='https://ourworldindata.org/grapher/share-electricity-coal',
     pick=('series', ['Poland', 'China', 'India', 'Germany', 'United Kingdom']),
     decoys=['Share of electricity generated from gas',
             'Share of electricity generated from oil',
             'Share of electricity generated from fossil fuels of all kinds',
             'Share of a country\'s energy that is imported'],
     hints=['The British line falls off a cliff after 2012 and does not come back.',
            'India climbs while Germany halves, and China stays above every European line '
            'for the whole period.',
            'A percentage of all electricity generated, from 2000 to 2024.',
            'Poland was built on a seam of it, and still is.'],
     why='Share of electricity from coal. The British collapse after 2012 is the carbon '
         'price floor; a chart of all fossil fuels together would not fall anything like '
         'that far, because gas took up the slack.'),

dict(slug='mean-male-height', src='height', type='dumbbell', diff=3,
     family='Change over time', form='Dumbbell · 1900 → 1996',
     truth='Average height of adult men, 1900 vs 1996',
     answer='Average height of adult men',
     period='1900 → 1996', unit='centimetres', baseline=140,
     source='Our World in Data', sourceUrl='https://ourworldindata.org/grapher/average-height-of-men',
     pick=('list', ['Netherlands', 'Sweden', 'Norway', 'United States', 'Japan',
                    'South Korea', 'Spain', 'Brazil', 'India', 'Guatemala', 'Laos',
                    'East Timor']),
     decoys=['Average weight of adult men, in kilograms',
             'Average age of men at first marriage',
             'Average years of schooling among men',
             'Average waist measurement of adult men, in centimetres'],
     hints=['The Dutch were not first in the world in 1900. The Americans were.',
            'Every value on this chart sits between about 150 and 185, a range of under '
            'forty across the whole world and a whole century.',
            'Centimetres, measured in 1900 and again in 1996.',
            'South Korea moves further than almost anyone here, and it is not because '
            'Koreans changed.'],
     why='Mean height of adult men by birth cohort. The narrow band between 150 and 185 '
         'is what rules out weight and schooling, both of which vary by much more than '
         'that between these countries.'),
]


WHY = {

'tb-incidence':
    "Djibouti falls from 2,700 per 100,000 to 477, and Sweden from 6.7 to 3.8, so the top "
    "of this chart is some seven hundred times the bottom. Road deaths and deaths from air "
    "pollution both die on that top figure: no death rate from anything reaches 2,700 per "
    "100,000, and these are new cases rather than deaths. Malaria dies on Kiribati, high on "
    "the chart and sitting in the mid-Pacific, where malaria does not occur.",

'measles-first-dose':
    "Kazakhstan falls from 99 per cent to 69 while Rwanda climbs from 74 to 96, so this is "
    "something a government can lose as well as build. Children reaching their fifth "
    "birthday dies on Somalia at 24, which would mean three quarters of its children dying. "
    "Births attended by a trained health worker dies on the same Kazakh collapse, which no "
    "country's hospital birth rate has done. Polio dies on timing, its first dose being "
    "given within weeks of birth rather than at about a year.",

'maternal-deaths-rank':
    "Rwanda moves from tenth worst in the world to thirty-fifth and Bangladesh from "
    "thirty-first to sixty-third, while Nigeria goes from eighth to first. Underweight "
    "children, malaria and deaths from unsafe water all die on the same denominator: those "
    "are counted per head of population, and this is counted per live birth and only among "
    "women, which is why two countries with similar child nutrition can sit at opposite "
    "ends of it.",

'under-five-stunting-change':
    "Nepal and Bangladesh each take 29 percentage points off this in twenty-two years, "
    "while Australia and Germany drift up by one or two, which is noise at their level. "
    "Undernourishment dies on the direction, having risen in several of these countries "
    "over the period while almost every bar here points one way. Underweight children dies "
    "on the same near-uniformity, being the measure that moves with harvests and prices. "
    "Adult illiteracy dies on arithmetic, because an adult population changes only as one "
    "generation replaces another.",

'raised-blood-pressure':
    "Lithuania at 55 per cent is nearly three times Peru at 19, in a condition that usually "
    "has no symptoms at all. Diabetes dies on China and Mexico, both at the bottom of this "
    "chart and both among the worst in the world for it. Cholesterol dies on the top of the "
    "chart, which is Baltic and eastern rather than western European. Anaemia dies on "
    "Nigeria, mid-chart here and near the top of any anaemia ranking.",

'clean-cooking-fuels':
    "Indonesia goes from 6 per cent to 87, almost all of it in a single vertical climb in "
    "the second half of the 2000s. Internet use and bank accounts both die on China, which "
    "starts this chart at 38 per cent in 2000, when very few Chinese households had either. "
    "Electricity at home dies on Ethiopia, which ends at 7 per cent here and has a far "
    "larger share than that connected to a grid.",

'safely-managed-water':
    "Tanzania goes from 1.3 per cent to 30 and India from 38 to 73, while Mexico sits in "
    "the low forties for the whole period. Living in a city dies on the United Kingdom at "
    "99.8, well above its urban share. Electricity at home dies on India, which reached "
    "effectively universal supply while this measure was still at 73. A toilet connected to "
    "a sewer dies on Mexico, where sewer connection is far higher than the low forties.",

'life-expectancy-at-60':
    "A Japanese sixty-year-old can expect another 26.6 years and a Somali 12.3, a narrower "
    "gap than the same two countries show at birth. Average age at death dies on magnitude, "
    "since nothing here passes 27. Years spent in retirement dies on Somalia and the "
    "Central African Republic, neither of which has a pension system to retire into. Years "
    "in good health dies on being the lower of the two figures everywhere, and this is the "
    "upper one.",

'untreated-caries':
    "Every country on earth sits between about 22 and 50 per cent, with rich and poor mixed "
    "along the whole length of it, which is true of almost nothing else in this game. "
    "Losing all your natural teeth, seeing a dentist and short-sightedness all die on the "
    "same absence: each of the three would separate rich countries from poor ones or east "
    "from west somewhere along the chart, and this one has no gradient at all.",

'usually-working-from-home':
    "Bulgaria records half of one per cent in 2019 and Ireland goes from 7 per cent to "
    "20.6, which is the pandemic arriving in a labour statistic. Self-employment dies on "
    "that Bulgarian floor, as do temporary contracts and part-time work: all three describe "
    "how a large minority of Europeans are employed, and none of them could start at half "
    "of one per cent in any country, let alone quadruple in five years.",

'municipal-waste-rank':
    "Austria climbs from tenth to first and Ireland falls from second to tenth, while "
    "Romania stays at the bottom throughout. Electricity per person dies on France, which "
    "heats with it and would lead any such ranking while sitting mid-table here. Water per "
    "person dies on Cyprus and Denmark ranking together near the top, one of them among the "
    "most water-stressed countries in Europe and the other not. Packaging recycled dies on "
    "Germany, which leads Europe on recycling and is not at the top of this.",

'population-living-in-flats':
    "The chart runs from under 10 per cent to over 65, the widest housing split in Europe. "
    "Renting dies on Spain at 65.3, which has one of the highest home-ownership rates on "
    "the continent and tops this anyway. One-person households die on Sweden at 48.4, "
    "mid-chart, when Sweden leads Europe on living alone. Homes built since 2000 die on "
    "Ireland at 9.7, having built more of them per head than almost anywhere in the period.",

'eu-wind-electricity':
    "Germany generates 138,914 gigawatt hours, more than twice Spain, and Denmark manages "
    "20,553 from a far smaller population than either. Nuclear dies on France, third here at 47,499 when it "
    "would lead any nuclear chart by a distance. Water dies on Norway, second from bottom "
    "at 14,929 and below Denmark, when Norway leads Europe on hydro. The sun dies on Sweden "
    "at 40,621, fourth here and the wrong latitude to be fourth on solar.",

'eu-rail-freight':
    "Ukraine is second at 90,632 million tonne-kilometres, more than twice France, in a "
    "third year of full-scale war. Goods moved by lorry dies on Spain and the "
    "Netherlands, the two "
    "road-freight heavyweights of Europe, neither near the top here. Seaports die on the "
    "Netherlands again, which handles more port tonnage than any country in Europe and is "
    "absent. Motorway length dies on Ukraine itself, which has very little of it and is "
    "second.",

'eu-tourist-nights':
    "Croatia records 24,248 nights per 1,000 residents, about 24 a head, against 7,905 for "
    "Italy. Foreign arrivals die on the unit, since an arrival counts a day tripper and "
    "this counts only people who stayed the night. Hotel beds die on Italy, which has more "
    "of them than any country in the EU and is eleventh here, because a bed counts whether "
    "or not anyone sleeps in it. Visitor spending dies on Cyprus and Malta ranking above "
    "Greece and Italy, an ordering about nights rather than money.",

'food-price-level':
    "The same trolley costs 158.5 in Switzerland and 75.5 in Romania against a European "
    "average of 100, so it is more than twice the price at one end of the continent as the "
    "other. Average wages die on the gap, since the eastern countries sit at 75 to 87 here "
    "and much further below the average on pay. Clothes die on tradability, being shipped "
    "and therefore far flatter in price across Europe. The share of household spending that "
    "goes on food dies on Romania, which has the highest such share in the EU and is last "
    "on this chart.",

'drink-price-level':
    "Iceland is at 219.1 and Turkey at 59.6 against a European average of 100, a spread "
    "nearly four times wide. Petrol dies on Turkey at 59.6, the cheapest on this chart and "
    "nowhere near the cheapest place in Europe to fill a tank. A restaurant meal dies on "
    "Ireland at 204.5, above Norway, when restaurant prices follow wages and Norwegian "
    "wages are higher. Duty collected per adult dies on the axis, since this is an index against an "
    "average of 100 rather than an amount of money.",

'neet-change':
    "Ireland takes 14.1 percentage points off this between 2010 and 2024, and only Romania "
    "ends the period worse than it started, at 0.5. Higher education dies on direction, "
    "having risen almost everywhere, which would point every bar the other way. Young "
    "people living with their parents dies on southern Europe, where that share rose over "
    "the same years. Temporary contracts die on the uniformity, moving in both directions "
    "across Europe while this moves in one.",

'passenger-cars-per-thousand':
    "Italy reaches 694 cars per 1,000 people and Turkey 178, and every country on the chart "
    "rises over the decade. Mobile contracts die on the ceiling, exceeding 1,000 per 1,000 "
    "people in much of Europe while nothing here passes 700. Washing machines die on the "
    "spread, since a household owns one of those whether it is rich or poor and this chart "
    "runs almost fourfold. Bicycles sold die on the Netherlands and Denmark, which would "
    "lead any such list and sit mid-table here.",

'flowers-share-of-farm-output':
    "Flowers and ornamental plants are 22.6 per cent of everything the Netherlands' farms "
    "produce, "
    "more than four times Italy at 5. Fruit dies on Spain, which leads Europe on it and is "
    "near the bottom here. Wine dies on France and Italy for the same reason. Milk dies on "
    "Ireland at 0.74, where dairy is a large share of farm output.",

'read-no-books':
    "Switzerland has the best figure in Europe at 19.4 per cent and Albania the worst at "
    "70.8, so even at its best one adult in five read nothing at all in a year. Never using "
    "the internet dies on Switzerland at 19.4, which would mean a fifth of Swiss adults had "
    "never been online. Not taking a holiday dies on the same figure, in one of the "
    "countries best able to afford one. Not going to a cinema, theatre or concert dies on "
    "Albania at 70.8 being the worst on the chart, when skipping live culture altogether is "
    "commoner than that across most of Europe.",

'births-and-womens-work':
    "Every path drifts right as women's employment rises, and Hungary alone climbs, from "
    "1.32 births to 1.55 while its employment rate goes from 58.6 to 76.1. Women in higher "
    "education dies on the horizontal axis, which reaches 80 per cent. Age at first birth "
    "dies on the vertical axis, which never passes two and would need to sit near thirty. "
    "Births outside marriage dies there too, that share being over half in several of these "
    "countries.",

'hours-and-output':
    "Mexico works 2,228 hours a year for 38.7 dollars an hour; Germany works 1,339 for "
    "97.9. Average pay dies on the vertical axis, which is in tens of dollars rather than "
    "the tens of thousands a salary needs. The share of workers in industry dies there too, "
    "because a share cannot reach 98. Days of holiday die on the horizontal axis, which "
    "runs past 2,000.",

'doctor-consultations':
    "Japan's 12.4 visits a year is about one a month for every person in the country, and "
    "the Netherlands nearly doubles over the period, from 5.9 to 10.1. Nights in hospital "
    "and trips to a dentist both die on that Japanese figure, which would have the average "
    "Japanese person in a hospital bed for a fortnight a year or in a dentist's chair "
    "monthly. Prescriptions die the other way: a good many visits end with one written, so "
    "that chart would sit above this one rather than on top of it.",

'mri-scanners':
    "Greece reaches 39.2 scanners per million people, ahead of Germany at 37.1, while "
    "Mexico is at 2.9. Hospitals, ambulances and operating theatres all die on the same "
    "ceiling: nothing on this chart passes 39.2 per million, and a health system with only "
    "that many of any of the three would not be able to use the scanners it has.",

'gender-wage-gap-rank':
    "Korea is first in both years and Hungary climbs from twenty-second to eighth. Women in "
    "management dies on the United States, fifth here, which has one of the highest shares "
    "of women managers in the OECD, so the two rank in opposite directions. The graduate "
    "pay premium dies on Korea holding first place, its premium being unremarkable. "
    "Part-time work dies on Hungary and Czechia, which have little of it and sit at "
    "opposite ends of this chart.",

'rd-spending-deviation':
    "Israel spends 3.82 per cent of its economy on this and Romania 0.37, a tenfold spread "
    "around a 2 per cent line. Defence dies on Poland at 0.64 and Romania at 0.37, both "
    "substantial military spenders and both far below the line. University funding and "
    "business spending on machinery both die on that same 0.37, since no country runs "
    "either at a third of one per cent of its economy.",

'retirement-age-rank':
    "Indonesia is first in both years and Slovenia is forty-sixth, while Korea climbs from "
    "tenth to third. The official state pension age dies on Indonesia, which has barely any "
    "state pension to draw. Years spent in retirement dies on Japan, fourth here, which "
    "would also be near the top of that list, and the two cannot both hold. Over-65s still "
    "in work dies on the shape, being a percentage rather than an age.",

'pension-spending':
    "Greece goes from 10.5 per cent of its economy to 16.2 and Italy from 13.5 to 16.1, "
    "while Korea is at 3.8 and Mexico 5.3. Health dies on the United States, mid-table "
    "here, which would lead any health-spending chart by a wide margin. Unemployment "
    "benefits and education both die on Greece at 16.2, since no country spends a sixth of "
    "its entire economy on either of them.",

'electricity-from-coal':
    "Britain goes from 31.8 per cent to 0.67 while India rises from 68.3 to 74.5. Gas dies "
    "on the British line, since Britain's gas share rose over the same years that this "
    "collapsed. All fossil fuels together dies there too, Britain still generating a large "
    "share from gas, so that line would flatten well above zero. Oil dies on magnitude, "
    "having been in low single figures in all six of these countries throughout.",

'mean-male-height':
    "Dutch men gain 12.4 centimetres in a century, from 170.1 to 182.5, overtaking Sweden "
    "and the United States on the way. Weight dies on the floor of 153, since no population "
    "has ever averaged 153 kilograms. Age at first marriage dies on the same floor from the "
    "other direction, sitting in the twenties. Years of schooling dies there too: nobody "
    "has 153 years of it.",
}

# Every assertion in the text above that the chart cannot show and this pipeline
# cannot check. Read this list, not the prose, when fact-checking a batch. Each is
# chosen to be stable and widely known; none is a statistic quoted to a decimal.
WORLD_CLAIMS = {
    'tb-incidence': ['malaria does not occur in Kiribati'],
    'measles-first-dose': ['the first polio dose is given within weeks of birth, the first '
                           'measles dose at about a year'],
    'maternal-deaths-rank': [],
    'under-five-stunting-change': ['undernourishment rose in several countries over the period',
                                   'underweight is the acute measure, stunting the chronic one'],
    'raised-blood-pressure': ['China and Mexico have high diabetes prevalence',
                              'cholesterol is highest in western Europe',
                              'anaemia is high in Nigeria'],
    'clean-cooking-fuels': ['Chinese internet and bank account use was low in 2000',
                            'more than 7 per cent of Ethiopia has a grid connection'],
    'safely-managed-water': ['the UK is less than 99.8 per cent urban',
                             'India reached near-universal electrification',
                             'Mexican sewer connection exceeds 43 per cent'],
    'life-expectancy-at-60': ['healthy life expectancy is always below life expectancy',
                              'Somalia and the CAR have no functioning pension system',
                              'the Japan to Somalia gap is wider at birth than at sixty'],
    'untreated-caries': ['each of the three decoys sorts by income or region'],
    'usually-working-from-home': ['self-employment, temporary and part-time work each cover a\n'
                                  '                                  large minority of European workers'],
    'municipal-waste-rank': ['France leads Europe on electricity per person',
                             'Cyprus is water-stressed and Denmark is not',
                             'Germany leads Europe on recycling'],
    'population-living-in-flats': ['Spain has high home ownership',
                                   'Sweden leads Europe on living alone',
                                   'Ireland built a lot of housing after 2000'],
    'eu-wind-electricity': ['France leads Europe on nuclear generation',
                            'Norway leads Europe on hydro',
                            'Sweden is the wrong latitude to rank fourth on solar'],
    'eu-rail-freight': ['Spain and the Netherlands lead European road freight',
                        'the Netherlands leads European port tonnage',
                        'Ukraine has little motorway'],
    'eu-tourist-nights': ['an arrival counts a day visitor; a night does not',
                          'Italy has the most hotel beds in the EU'],
    'food-price-level': ['eastern European wages sit further below the EU average than their '
                         'food prices do',
                         'clothing prices are flatter across Europe than food prices',
                         'Romania has the highest share of spending going on food in the EU'],
    'drink-price-level': ['Turkey is not the cheapest place in Europe for petrol',
                          'Norwegian wages exceed Irish wages'],
    'neet-change': ['higher education participation rose across Europe 2010 to 2024',
                    'young people living with parents rose in southern Europe'],
    'passenger-cars-per-thousand': ['mobile contracts exceed 1,000 per 1,000 people in much '
                                    'of Europe',
                                    'a household owns one washing machine regardless of income',
                                    'the Netherlands and Denmark lead European cycling'],
    'flowers-share-of-farm-output': ['Spain leads Europe on fruit',
                                     'France and Italy lead Europe on wine',
                                     'dairy is a large share of Irish farm output'],
    'read-no-books': ['skipping all live culture is commoner across Europe than 70.8 per cent'],
    'births-and-womens-work': ['no country has 80 per cent of women holding a degree',
                               'births outside marriage exceed half in several EU countries'],
    'hours-and-output': [],
    'doctor-consultations': ['a good many consultations end in a prescription'],
    'mri-scanners': ['a health system needs more than 39 ambulances and theatres per million\n'
                     '                     to use its scanners'],
    'gender-wage-gap-rank': ['the United States has a high share of women managers',
                             'Korea has an unremarkable graduate pay premium',
                             'Hungary and Czechia have little part-time work'],
    'rd-spending-deviation': ['Poland and Romania are substantial military spenders'],
    'retirement-age-rank': ['Indonesia has minimal state pension provision',
                            'Japan ranks high on years spent in retirement'],
    'pension-spending': ['the United States leads the OECD on health spending'],
    'electricity-from-coal': ["Britain's gas share rose as its coal share fell",
                              'oil generation has been negligible in these countries'],
    'mean-male-height': [],
}


NAME = {
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'United States of America': 'United States',
    'Republic of Korea': 'South Korea',
    'Korea': 'South Korea',
    'Netherlands (Kingdom of the)': 'Netherlands',
    'United Republic of Tanzania': 'Tanzania',
    'Democratic Republic of the Congo': 'DR Congo',
    "Lao People's Democratic Republic": 'Laos',
    'Viet Nam': 'Vietnam',
    'Russian Federation': 'Russia',
    'Iran (Islamic Republic of)': 'Iran',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Syrian Arab Republic': 'Syria',
    'Naoero': 'Nauru',
    'Czechia': 'Czechia',
    'Türkiye': 'Turkey',
    'Kosovo*': 'Kosovo',
    'East Timor': 'Timor-Leste',
    'Republic of Moldova': 'Moldova',
    'Timor-Leste': 'Timor-Leste',
}
nice = lambda s: NAME.get(s, s)

def load(name):
    return TIDY[name]

def rows_of(series):
    return {r[0]: r[1:] for r in series['rows']}

def require(spec, series, names):
    have = rows_of(series)
    missing = [n for n in names if n not in have]
    if missing:
        raise SystemExit(f"{spec['slug']}: not in series: {missing[:6]}")
    return have

def spread(series, n):
    """n rows spread evenly across the sorted range, both extremes kept."""
    rows = series['rows']
    if len(rows) <= n:
        return rows
    step = (len(rows) - 1) / (n - 1)
    idxs = sorted({int(round(i * step)) for i in range(n)})
    return [rows[i] for i in idxs]

def build(spec):
    t = spec['type']
    p = {
        'family': spec['family'], 'form': spec['form'], 'exhibit': 'Exhibit A',
        'type': t, 'diff': spec['diff'], 'truth': spec['truth'],
        'period': spec['period'], 'unit': spec['unit'],
    }
    pick = spec['pick']

    if t == 'scatter':
        xs, ys = load(spec['src'][0] + '_s'), load(spec['src'][1] + '_s')
        xr, yr = rows_of(xs), rows_of(ys)
        y0 = max(int(xs['years'][0]), int(ys['years'][0]))
        y1 = min(int(xs['years'][-1]), int(ys['years'][-1]))
        xi, yi = xs['years'].index(str(y0)), ys['years'].index(str(y0))
        span = y1 - y0 + 1
        ser = []
        for nm in pick[1]:
            if nm not in xr or nm not in yr:
                raise SystemExit(f"{spec['slug']}: no path for {nm}")
            pts = [[round(xr[nm][xi + k], 2), round(yr[nm][yi + k], 3)] for k in range(span)]
            ser.append({'name': nice(nm), 'points': pts})
        p.update(series=ser, startYear=y0, xUnit=spec['xUnit'], yUnit=spec['yUnit'])

    elif t == 'line':
        s = load(spec['src'] + '_s')
        have = require(spec, s, pick[1])
        p.update(startYear=int(s['years'][0]),
                 series=[{'name': nice(nm), 'values': [round(v, 2) for v in have[nm]]}
                         for nm in pick[1]])

    elif t == 'slope':
        s = load(spec['src'])
        have = require(spec, s, pick[1])
        order_a = sorted(s['rows'], key=lambda r: -r[1])
        order_b = sorted(s['rows'], key=lambda r: -r[2])
        ra = {r[0]: i + 1 for i, r in enumerate(order_a)}
        rb = {r[0]: i + 1 for i, r in enumerate(order_b)}
        p.update(leftYear=int(s['years'][0]), rightYear=int(s['years'][1]),
                 ranks=[[nice(nm), ra[nm], rb[nm]] for nm in pick[1]])

    elif t == 'dumbbell':
        s = load(spec['src'])
        have = require(spec, s, pick[1])
        p.update(leftYear=int(s['years'][0]), rightYear=int(s['years'][1]),
                 data=[[nice(nm), round(have[nm][0], 2), round(have[nm][1], 2)]
                       for nm in pick[1]])
        if 'baseline' in spec:
            p['baseline'] = spec['baseline']

    elif t in ('treemap', 'symbol'):
        s = load(spec['src'])
        rows = s['rows'][:pick[1]]
        data = [[nice(r[0]), round(r[1])] for r in rows]
        p['data'] = data
        if t == 'treemap':
            p['total'] = sum(d[1] for d in data)

    elif t == 'beeswarm':
        s = load(spec['src'])
        rows = s['rows']
        if spec.get('delta'):
            data = [[nice(r[0]), round(r[2] - r[1], 2)] for r in rows]
        else:
            data = [[nice(r[0]), round(r[1], 2)] for r in rows]
        data.sort(key=lambda d: d[0])
        p['data'] = data
        p['label'] = [nice(x) for x in spec['label']]
        p['labelSm'] = [nice(x) for x in spec['labelSm']]

    elif t == 'deviation':
        s = load(spec['src'])
        if pick[0] == 'list':
            have = require(spec, s, pick[1])
            rows = [[nm] + have[nm] for nm in pick[1]]
        else:
            rows = spread(s, pick[1])
        if spec.get('delta'):
            # Change charts are drawn against a zero line rather than a level,
            # because the beeswarm renderer cannot place a negative value and a
            # fall is the whole point of the chart.
            vals = [[r[0], r[2] - r[1]] for r in rows]
        else:
            vals = [[r[0], r[1]] for r in rows]
        vals.sort(key=lambda r: -r[1])
        p['data'] = [[nice(r[0]), round(r[1], 2)] for r in vals]
        p['reference'] = spec['reference']
        if spec.get('delta'):
            p['delta'] = True

    else:
        raise SystemExit('unknown type ' + t)

    if spec.get('suffix'):
        p['suffix'] = spec['suffix']
    p.update(answer=spec['answer'], decoys=spec['decoys'], hints=spec['hints'],
             why=WHY.get(spec['slug'], spec['why']), slug=spec['slug'],
             source=spec['source'],
             sourceUrl=spec['sourceUrl'])
    if spec.get('deadpan'):
        p['deadpan'] = True
    return p



# --------------------------------------------------------------------- emit
def as_js(p):
    """Hand the puzzle to common.block(), which wants data and ranks as text."""
    o = dict(p)
    if 'data' in o:
        dec = 0 if o['type'] in ('treemap', 'symbol') else 2
        o['data'] = arr(o['data'], 2 if o['type'] == 'dumbbell' else 3, dec)
    if 'ranks' in o:
        o['ranks'] = arr(o['ranks'], 3, 0)
    if 'series' in o and 'xUnit' not in o:
        o['series'] = [(s['name'], s['values']) for s in o['series']]
    elif 'series' in o:
        o['series'] = [(s['name'], s['points']) for s in o['series']]
    return block(o)


def main():
    fetch_all()
    extract()
    extract_series()
    P = [build(s) for s in SPECS]
    for i, o in enumerate(P):
        o['exhibit'] = ex(134 + i)
        o.pop('deadpan', None)
    print(',\n'.join(as_js(o) for o in P))
    sys.stderr.write('built %d puzzles\n' % len(P))


if __name__ == '__main__':
    main()
