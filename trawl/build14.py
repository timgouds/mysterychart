#!/usr/bin/env python3
"""Batch 10, part three of three: multi-line charts.

    python3 build14.py --digest
    python3 build14.py > b14.js

Same contract as build11.py: lines draw from zero unless a baseline is set, so
every value must be non-negative, and a missing year would render as a gap;
both are asserted. Text lives in text14.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import block, ex
import sources as S
from build11 import series, digest, emit

START = 226
ES = 'https://ec.europa.eu/eurostat/databrowser/view/%s'
WB = 'https://data.worldbank.org/indicator/%s'
OE = ('https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ'
      '&df[id]=%s&df[ag]=%s')


def key(n, **pos):
    a = [''] * n
    for p, v in pos.items():
        a[int(p[1:])] = v
    return '.'.join(a)


def short(s):
    """Long names clip at compact width at the end of a line."""
    return [('Britain' if c == 'United Kingdom' else c, v) for c, v in s]


def warheads():
    d = S.owid('nuclear-warhead-stockpiles', ['USA', 'RUS', 'GBR', 'FRA', 'CHN'], 1945, 2025)
    for c in d:   # OWID leaves a year out where the count was zero
        for y in range(1945, 2026):
            d[c].setdefault(str(y), 0.0)
    s = series(d, 1945, 2025, ['United States', 'Russia', 'United Kingdom', 'France', 'China'])
    return dict(s=short(s), y0=1945, y1=2025, unit='number held', src='Our World in Data',
                url='https://ourworldindata.org/grapher/nuclear-warhead-stockpiles')


def farm_support():
    d = S.oecd('OECD.TAD.ARP', 'DSD_AGR_POLIND@DF_PSE', 1986, 2024, key=key(5, p1='A', p2='PSEP'))
    return dict(s=series(d, 1986, 2024, ['Norway', 'South Korea', 'Japan', 'United States', 'New Zealand']),
                y0=1986, y1=2024, unit='% of farm receipts', suffix='%', src='OECD',
                url=OE % ('DSD_AGR_POLIND%40DF_PSE', 'OECD.TAD.ARP'))


def asylum():
    ys = list(range(2014, 2025))
    a = S.eurostat('migr_asyappctza', ys, citizen='TOTAL', applicant='FRST', sex='T', age='TOTAL',
                   unit='PER', freq='A')
    p = S.eurostat('demo_pjan', ys, sex='T', age='TOTAL', unit='NR', freq='A')
    d = {c: {str(y): 1000 * a[c][str(y)] / p[c][str(y)] for y in ys
             if str(y) in a[c] and str(y) in p.get(c, {})} for c in a}
    return dict(s=series(d, 2014, 2024, ['Hungary', 'Sweden', 'Germany', 'Cyprus', 'Spain']),
                y0=2014, y1=2024, unit='per 1,000 residents a year', src='Eurostat',
                url=ES % 'migr_asyappctza')


def hiv():
    d = S.worldbank('SH.DYN.AIDS.ZS', list(range(2000, 2025)))
    return dict(s=series(d, 2000, 2024, ['Eswatini', 'Botswana', 'South Africa', 'Zimbabwe', 'Kenya']),
                y0=2000, y1=2024, unit='% of people aged 15 to 49', suffix='%', src='World Bank',
                url=WB % 'SH.DYN.AIDS.ZS')


def fibre():
    d = S.oecd('OECD.STI.DEP', 'DSD_BB_DATABASE@DF_BB_TEL_DATABASE', 2010, 2024,
               key=key(7, p1='A', p2='FBB', p3='SUB', p4='FIB', p6='PT_SB_FBB'))
    s = series(d, 2010, 2024, ['Japan', 'South Korea', 'Spain', 'United Kingdom', 'Germany'])
    return dict(s=short(s), y0=2010, y1=2024, unit='% of fixed connections', suffix='%', src='OECD',
                url=OE % ('DSD_BB_DATABASE%40DF_BB_TEL_DATABASE', 'OECD.STI.DEP'))


def sheep():
    d = S.eurostat('apro_mt_lssheep', [], animals='A4100', month='M11_M12', unit='THS_HD', freq='A')
    return dict(s=series(d, 1995, 2024, ['Spain', 'Romania', 'Greece', 'France', 'Ireland']),
                y0=1995, y1=2024, unit='thousands of animals', src='Eurostat', url=ES % 'apro_mt_lssheep')


def cereal():
    d = S.worldbank('AG.YLD.CREL.KG', list(range(1961, 2024)))
    s = series(d, 1961, 2022, ['United States', 'France', 'Egypt', 'China', 'India'], 1e-3)
    return dict(s=short(s), y0=1961, y1=2022, unit='tonnes per hectare', src='World Bank',
                url=WB % 'AG.YLD.CREL.KG')


ORDER = [('nuclear-warheads', warheads), ('farm-support', farm_support),
         ('asylum-applications-per-thousand', asylum), ('hiv-prevalence', hiv),
         ('fibre-broadband-share', fibre), ('sheep-kept', sheep), ('cereal-yield', cereal)]


if __name__ == '__main__':
    built = [(s, f()) for s, f in ORDER]
    if '--digest' in sys.argv:
        for s, o in built:
            digest(s, o)
        sys.exit()
    from text14 import TEXT
    print(',\n'.join(emit(START + k, s, o, TEXT[s]) for k, (s, o) in enumerate(built)) + ',')
