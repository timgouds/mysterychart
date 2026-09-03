"""Shared helpers for the batch builders."""
import json, sys
import wb

NICE = {'Korea, Rep.': 'South Korea', "Korea, Dem. People's Rep.": 'North Korea',
        'Russian Federation': 'Russia', 'Egypt, Arab Rep.': 'Egypt',
        'Iran, Islamic Rep.': 'Iran', 'Viet Nam': 'Vietnam',
        'Congo, Dem. Rep.': 'Democratic Republic of Congo',
        "Cote d'Ivoire": "Côte d'Ivoire", 'Turkiye': 'Turkey',
        'Syrian Arab Republic': 'Syria', 'Yemen, Rep.': 'Yemen',
        'Venezuela, RB': 'Venezuela', 'Lao PDR': 'Laos',
        'Hong Kong SAR, China': 'Hong Kong', 'Macao SAR, China': 'Macao',
        'Slovak Republic': 'Slovakia', 'Gambia, The': 'Gambia',
        'Bahamas, The': 'Bahamas', 'Kyrgyz Republic': 'Kyrgyzstan',
        'Brunei Darussalam': 'Brunei', 'Cabo Verde': 'Cape Verde',
        'Timor-Leste': 'East Timor', 'Naoero': 'Nauru',
        'Somalia, Fed. Rep.': 'Somalia', 'Micronesia, Fed. Sts.': 'Micronesia',
        'Congo, Rep.': 'Congo', 'St. Lucia': 'Saint Lucia',
        'West Bank and Gaza': 'Palestine',
        'St. Vincent and the Grenadines': 'Saint Vincent',
        'St. Kitts and Nevis': 'Saint Kitts and Nevis'}
nm = lambda s: NICE.get(s, s)

DROP = {'Channel Islands', 'Isle of Man', 'Faroe Islands', 'Greenland', 'Bermuda',
        'Cayman Islands', 'British Virgin Islands', 'Turks and Caicos Islands',
        'Sint Maarten (Dutch part)', 'St. Martin (French part)', 'Curacao',
        'New Caledonia', 'French Polynesia', 'Gibraltar', 'Monaco', 'Liechtenstein',
        'San Marino', 'Andorra', 'Nauru', 'Tuvalu', 'Palau',
        'Northern Mariana Islands', 'Guam', 'American Samoa',
        'Virgin Islands (U.S.)', 'Puerto Rico', 'Macao', 'Aruba',
        'Marshall Islands', 'Kosovo', 'Palestine'}


def ex(i):
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return 'Exhibit ' + s


def num(v, dec):
    v = round(v, dec)
    return str(int(v)) if v == int(v) else str(v)


def arr(rows, per, dec):
    items = []
    for r in rows:
        parts = [json.dumps(r[0], ensure_ascii=False)] + [num(x, dec) for x in r[1:]]
        items.append('[' + ','.join(parts) + ']')
    out, line = [], []
    for it in items:
        line.append(it)
        if len(line) == per:
            out.append('        ' + ', '.join(line)); line = []
    if line:
        out.append('        ' + ', '.join(line))
    return ',\n'.join(out)


def dumb(code, y1, y2, want, dec=1):
    d = {nm(n): (a, b) for n, a, b in wb.pair(code, y1, y2)}
    miss = [c for c in want if c not in d]
    if miss:
        sys.exit('MISSING in %s: %s' % (code, miss))
    rows = [(c, round(d[c][0], dec), round(d[c][1], dec)) for c in want]
    rows.sort(key=lambda r: r[2])
    return rows


def full(code, y, dec=2):
    r = [(nm(n), round(v, dec)) for n, v in wb.snap(code, y) if nm(n) not in DROP]
    r.sort(key=lambda x: x[0])
    return r


def tree(code, y, keep=12):
    """The twelve largest, totalled among themselves.

    Doc 15: the banana treemap was 52% "Rest of world" and the evidence the
    puzzle depended on was squashed into unlabelled slivers. A leftover block
    bigger than the real ones hides exactly what the player is meant to read,
    so it is dropped and the square becomes the top twelve."""
    rows = [(nm(n), int(v)) for n, v in wb.snap(code, y)]
    top = sorted(rows[:keep], key=lambda r: -r[1])
    return top, sum(v for _, v in top)


def block(o):
    L = []
    L.append('    {')
    L.append('      family: %s,' % json.dumps(o['family'], ensure_ascii=False))
    L.append('      form: %s,' % json.dumps(o['form'], ensure_ascii=False))
    L.append('      exhibit: %s,' % json.dumps(o['exhibit']))
    head = '      type: %s, diff: %d,' % (json.dumps(o['type']), o['diff'])
    if 'reference' in o:
        head = '      type: %s, reference: %s, diff: %d,' % (
            json.dumps(o['type']), o['reference'], o['diff'])
    L.append(head)
    L.append('      truth: %s, period: %s,' % (json.dumps(o['truth'], ensure_ascii=False),
                                               json.dumps(o['period'], ensure_ascii=False)))
    L.append('      unit: %s,' % json.dumps(o['unit'], ensure_ascii=False))
    if o.get('suffix'):
        L.append('      suffix: %s,' % json.dumps(o['suffix']))
    if 'total' in o:
        L.append('      total: %d,' % o['total'])
    if 'leftYear' in o:
        L.append('      leftYear: %d, rightYear: %d,' % (o['leftYear'], o['rightYear']))
    if 'startYear' in o:
        L.append('      startYear: %d,' % o['startYear'])
    if 'baseline' in o:
        L.append('      baseline: %d,' % o['baseline'])
    if 'series' in o:
        L.append('      series: [')
        L.append(',\n'.join(
            '        { name: %s, values: [%s] }' % (json.dumps(s[0], ensure_ascii=False), ','.join(num(v, 1) for v in s[1]))
            for s in o['series']))
        L.append('      ],')
    key = 'ranks' if o['type'] == 'slope' else 'data'
    if key in o:
        L.append('      %s: [' % key)
        L.append(o[key])
        L.append('      ],')
    if 'label' in o:
        L.append('      label: %s,' % json.dumps(o['label'], ensure_ascii=False))
        L.append('      labelSm: %s,' % json.dumps(o['labelSm'], ensure_ascii=False))
    L.append('      answer: %s,' % json.dumps(o['answer'], ensure_ascii=False))
    L.append('      decoys: [')
    L.append(',\n'.join('        ' + json.dumps(d, ensure_ascii=False) for d in o['decoys']))
    L.append('      ],')
    L.append('      hints: [')
    L.append(',\n'.join('        ' + json.dumps(h, ensure_ascii=False) for h in o['hints']))
    L.append('      ],')
    L.append('      why: %s,' % json.dumps(o['why'], ensure_ascii=False))
    L.append('      slug: %s,' % json.dumps(o['slug']))
    L.append('      source: %s, sourceUrl: %s' % (json.dumps(o['source']),
                                                  json.dumps(o['sourceUrl'])))
    L.append('    }')
    return '\n'.join(L)


