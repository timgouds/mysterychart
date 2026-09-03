#!/usr/bin/env python3
"""Screen a WHO GHO indicator for puzzle-readiness.

Checks the things that have bitten us before:
  - mixed reference years across countries (doc 22, the dentists chart)
  - too few countries
  - a value column that is a string rather than a number (doc 22, RS_208)

Usage:  python3 who.py INDICATOR_CODE [year]
"""
import json, sys, subprocess, collections

AGG = ('GLOBAL', 'WB_LI', 'WB_LMI', 'WB_UMI', 'WB_HI', 'EUR', 'AFR', 'AMR',
       'SEAR', 'WPR', 'EMR', 'EU', 'WB_LDC', 'OECD')


def fetch(code):
    url = 'https://ghoapi.azureedge.net/api/' + code
    raw = subprocess.run(['curl', '-s', '-m', '90', url],
                         capture_output=True, text=True).stdout
    return json.loads(raw)['value']


def screen(code, year=None, sex='BTSX', show=12):
    rows = fetch(code)
    rows = [r for r in rows if r.get('SpatialDimType') == 'COUNTRY']
    if any(r.get('Dim1') == sex for r in rows):
        rows = [r for r in rows if r.get('Dim1') == sex]
    if year:
        rows = [r for r in rows if str(r.get('TimeDim')) == str(year)]
    else:
        yrs = collections.Counter(r.get('TimeDim') for r in rows)
        if yrs:
            year = yrs.most_common(1)[0][0]
            rows = [r for r in rows if r.get('TimeDim') == year]

    vals = []
    for r in rows:
        v = r.get('NumericValue')
        if v is None:
            continue
        vals.append((r['SpatialDim'], r.get('Value'), v, r.get('TimeDim')))

    yrs = set(v[3] for v in vals)
    print('%s  year=%s  countries=%d  year-spread=%d' %
          (code, year, len(vals), len(yrs)))
    if not vals:
        print('   NO NUMERIC DATA')
        return []
    vals.sort(key=lambda x: -x[2])
    print('   top:', ', '.join('%s %s' % (v[0], v[2]) for v in vals[:show]))
    print('   bot:', ', '.join('%s %s' % (v[0], v[2]) for v in vals[-6:]))
    return vals


if __name__ == '__main__':
    screen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
