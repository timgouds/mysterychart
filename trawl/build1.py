#!/usr/bin/env python3
"""Assemble batch one (12 puzzles) as a JS block ready to append to src/puzzles.js."""
import wb, json, subprocess, sys

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


WB = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)
P = []

# ---------------------------------------------------------------- 50 landlines
src, url = WB('IT.MLT.MAIN.P2')
P.append(dict(
    family='Change over time', form='Dumbbell · 2000 → 2023', type='dumbbell', diff=3,
    truth='Landline telephone connections per 100 people, 2000 vs 2023',
    period='2000 → 2023', unit='connections per 100 people',
    leftYear=2000, rightYear=2023,
    data=arr(dumb('IT.MLT.MAIN.P2', 2000, 2023, [
        'United States', 'Germany', 'United Kingdom', 'South Korea', 'France',
        'Japan', 'Poland', 'Turkey', 'Brazil', 'Mexico', 'China', 'India',
        'Kenya', 'Nigeria'], 1), 3, 1),
    answer='Landline telephone connections per 100 people',
    decoys=[
        'Daily newspapers sold per 100 people',
        'Personal computers per 100 people',
        'Cars per 100 people',
        'Televisions per 100 households',
        'Fixed broadband connections per 100 people',
        'Letters posted per person each year',
        'Post offices per 100,000 people'],
    hints=[
        'France ends almost exactly where it began. Nearly everywhere else on this list, something was quietly given up.',
        'Kenya and Nigeria are near nothing in both years, and lower in 2023 than in 2000. Whatever this is, the poorer countries never took it up and then skipped it altogether.',
        'Counted per 100 people, so a figure near 60 means roughly one for every household.',
        'It sits in the hall, it is attached to the wall, and almost nobody under thirty has one.'],
    why='The United States falls from 68 to 25 while France holds at 56, and Kenya and Nigeria finish at effectively zero. Only a superseded technology produces both patterns at once: computers, broadband and televisions all rose in Africa over the same period.',
    slug='IT.MLT.MAIN.P2', source=src, sourceUrl=url))

# ------------------------------------------------------------- 51 remittances
src, url = WB('BX.TRF.PWKR.DT.GD.ZS')
P.append(dict(
    family='Change over time', form='Dumbbell · 2000 → 2023', type='dumbbell', diff=4,
    truth='Money sent home by workers abroad, as a share of the economy, 2000 vs 2023',
    period='2000 → 2023', unit='% of GDP', suffix='%',
    leftYear=2000, rightYear=2023,
    data=arr(dumb('BX.TRF.PWKR.DT.GD.ZS', 2000, 2023, [
        'Nepal', 'Honduras', 'El Salvador', 'Jamaica', 'Philippines', 'Morocco',
        'Pakistan', 'Bangladesh', 'Egypt', 'Mexico', 'India', 'Poland',
        'Germany', 'United States'], 2), 3, 2),
    answer='Money sent home by workers abroad, as a share of the economy',
    decoys=[
        'Foreign aid received, as a share of the economy',
        'Earnings from tourism, as a share of the economy',
        'Clothing exports, as a share of the economy',
        'Foreign investment arriving each year, as a share of the economy',
        'Government spending on health, as a share of the economy',
        'Oil and gas exports, as a share of the economy',
        'Interest paid on foreign debt, as a share of the economy'],
    hints=[
        'The United States is at the very bottom of this chart, and it is not close.',
        'The leaders are not the poorest countries: El Salvador and Jamaica sit far above India and Bangladesh. Whatever fills a quarter of Nepal\u2019s economy is not produced inside it.',
        'Measured as a percentage of everything a country produces in a year. Nepal has gone from 2 per cent to 26.',
        'It is what a nurse in the Gulf and a builder in Spain wire back to their families each month.'],
    why='Aid would put the poorest countries on top and these are middle income; tourism cannot explain landlocked Nepal at 26 per cent; and the United States and Germany at the bottom rule out anything measuring economic activity in general. Only earnings made abroad and sent back fit all three ends of the chart.',
    slug='BX.TRF.PWKR.DT.GD.ZS', source=src, sourceUrl=url))

# ------------------------------------------------------- 52 adolescent births
src, url = WB('SP.ADO.TFRT')
P.append(dict(
    family='Change over time', form='Dumbbell · 1990 → 2023', type='dumbbell', diff=4,
    truth='Births to girls aged 15 to 19, per 1,000 girls, 1990 vs 2023',
    period='1990 → 2023', unit='births per 1,000 girls aged 15 to 19',
    leftYear=1990, rightYear=2023,
    data=arr(dumb('SP.ADO.TFRT', 1990, 2023, [
        'South Korea', 'Japan', 'France', 'China', 'United Kingdom',
        'United States', 'India', 'Brazil', 'Mexico', 'Bangladesh', 'Nigeria',
        'Angola', 'Niger', 'Mozambique'], 1), 3, 1),
    answer='Births to girls aged 15 to 19, per 1,000',
    decoys=[
        'Children out of primary school, per 1,000 children',
        'New tuberculosis cases per 1,000 people',
        'Children who die before their first birthday, per 1,000 births',
        'People without electricity at home, per 1,000',
        'Households without running water, per 1,000',
        'Doctors per 1,000 people',
        'Road deaths per 1,000 vehicles'],
    hints=[
        'India has fallen by nine tenths since 1990. Mozambique has barely moved at all.',
        'Mexico and Brazil now sit well above India, which is the wrong way round for anything to do with dying or with being poor. South Korea ends at one half of one.',
        'Counted per 1,000 of a single five year age band, not per 1,000 of the population.',
        'It is the teenage birth rate, and India\u2019s collapse is the largest of any big country.'],
    why='Latin America above South Asia is the tell. On every mortality, schooling or poverty measure India in 2023 sits above Mexico and Brazil; here it is a tenth of them. South Korea at 0.5 also rules out infant mortality, which has a floor near 2 even in the richest countries.',
    slug='SP.ADO.TFRT', source=src, sourceUrl=url))

# --------------------------------------------------------------- 53 PM2.5
src, url = WB('EN.ATM.PM25.MC.M3')
P.append(dict(
    family='Change over time', form='Dumbbell · 2000 → 2020', type='dumbbell', diff=3,
    truth='Fine particle air pollution, 2000 vs 2020', period='2000 → 2020',
    unit='micrograms of PM2.5 per cubic metre',
    leftYear=2000, rightYear=2020,
    data=arr(dumb('EN.ATM.PM25.MC.M3', 2000, 2020, [
        'Finland', 'Australia', 'United States', 'Germany', 'United Kingdom',
        'Italy', 'Poland', 'South Korea', 'China', 'Egypt', 'India', 'Nigeria',
        'Saudi Arabia', 'Bangladesh'], 1), 3, 1),
    answer='Fine particle air pollution',
    decoys=[
        'Carbon dioxide emitted per person each year, in tonnes',
        'Share of electricity generated from coal',
        'Deaths from smoking per 100,000 people',
        'Cars per 1,000 people',
        'Industrial output per person, in hundreds of dollars',
        'Days above 35 degrees each year',
        'Cigarettes smoked per adult each week'],
    hints=[
        'Australia is the only rich country here that ends higher than it started, and the year being measured is 2020.',
        'Saudi Arabia is second from the top, above India and Nigeria, while the United States is near the bottom. Deserts make this as readily as factories do, and being rich does not produce it.',
        'Measured in micrograms per cubic metre. The World Health Organization guideline is 5, and only Finland is close.',
        'It is what a mask filters out, and what turns a Delhi winter sky brown.'],
    why='Saudi Arabia above India, and the United States below Poland, breaks every emissions and energy reading: on carbon dioxide per person the Americans and Australians would lead and Bangladesh would be last. Desert dust and cooking fires put the same particles in the air as coal does, which is why the ranking looks nothing like an industrial one.',
    slug='EN.ATM.PM25.MC.M3', source=src, sourceUrl=url))

# ------------------------------------------------------------ 54 self-employed
src, url = WB('SL.EMP.SELF.ZS')
se = full('SL.EMP.SELF.ZS', 2024, 1)
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2024', type='beeswarm', diff=3,
    truth='Share of workers who work for themselves, 2024', period='2024',
    unit='% of everyone in work', suffix='%',
    data=arr(se, 4, 1),
    label=['Chad', 'Niger', 'Nigeria', 'India', 'Brazil', 'Italy', 'France',
           'United States', 'Qatar'],
    labelSm=['Chad', 'India', 'France', 'United States', 'Qatar'],
    answer='Share of workers who work for themselves',
    decoys=[
        'Share of adults without a bank account',
        'Share of workers employed by the government',
        'Share of workers who are paid in cash',
        'Share of adults living outside a town or city',
        'Share of workers with no schooling beyond primary',
        'Share of adults who are in work at all',
        'Share of the workforce that is female'],
    hints=[
        'Qatar is at the far left at under one in a hundred. Chad is at the far right at nine in ten.',
        'The Gulf states are all bunched at the bottom, because nearly everyone working there arrived on a contract to work for somebody else. Italy sits well above Japan, so this is not a ranking of wealth.',
        'Counted as a share of everyone in work. The two ends of the swarm are 1 per cent and 92 per cent.',
        'It counts market traders, smallholders and anyone else with no employer above them.'],
    why='Qatar, Bahrain and Kuwait at the very bottom is the discriminator: their workforces are overwhelmingly migrant employees, so any measure of exclusion or informality would put them high, not last. Norway at 4.9 also rules out government employment, where it would be among the highest in the world.',
    slug='SL.EMP.SELF.ZS', source=src, sourceUrl=url))

# ---------------------------------------------------------------- 55 doctors
src, url = WB('SH.MED.PHYS.ZS')
ph = full('SH.MED.PHYS.ZS', 2021, 2)
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2021', type='beeswarm', diff=2,
    truth='Practising doctors per 1,000 people, 2021', period='2021',
    unit='doctors per 1,000 people',
    data=arr(ph, 4, 2),
    # India has no 2021 figure in this series, so labelling it drew nothing.
    label=['Cuba', 'Greece', 'Russia', 'Germany', 'United Kingdom',
           'United States', 'China', 'Indonesia', 'Chad'],
    labelSm=['Cuba', 'Germany', 'United States', 'Indonesia', 'Chad'],
    answer='Practising doctors per 1,000 people',
    decoys=[
        'Nurses and midwives per 1,000 people',
        'Teachers per 1,000 people',
        'Pharmacies per 10,000 people',
        'University graduates per 100 adults',
        'Police officers per 1,000 people',
        'Dentists per 10,000 people',
        'Cars per 10 people'],
    hints=[
        'One country sits alone out on the right, half as far again as anything else, and it is not a rich one.',
        'Greece is second and Russia is close behind, while the United States and the United Kingdom are unremarkable in the middle. Whatever this counts, money does not buy it.',
        'Counted per 1,000 of the population. The leader is at 9.5 and the last country at 0.02.',
        'Cuba trains more of them than it needs and sends them abroad as a matter of foreign policy.'],
    why='Cuba alone at 9.5 with Greece second is the signature of this particular series and of almost nothing else. Nurses would put Norway, Switzerland and Finland at the front; anything tracking national income would put the United States far higher than the middle of the pack.',
    slug='SH.MED.PHYS.ZS', source=src, sourceUrl=url))

# --------------------------------------------------------- 56 container ports
src, url = WB('IS.SHP.GOOD.TU')
rows, tot = tree('IS.SHP.GOOD.TU', 2023)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=3,
    truth='Container traffic through a country\u2019s ports, 2023', period='2023',
    unit='twenty-foot containers handled', total=tot,
    data=arr(rows, 3, 0),
    answer='Container traffic through a country\u2019s ports',
    decoys=[
        'Manufacturing output',
        'Shipbuilding output',
        'Steel production',
        'Air freight carried',
        'Cement production',
        'Crude oil shipped by sea',
        'Value of electronics exported'],
    hints=[
        'One country holds a third of this square. The next eleven put together do not match it.',
        'Singapore, Malaysia and the United Arab Emirates all take bigger blocks than Germany, and the Netherlands is not far behind. None of them is a large country; all four sit on a strait or a canal mouth.',
        'Counted in twenty-foot steel boxes. The leader handles 279 million of them in a year.',
        'Each one is lifted off a ship by a gantry crane, and about a third of them pass through China.'],
    why='China takes a third of the world\u2019s boxes because it holds seven of the ten busiest container ports on earth: Shanghai alone handles almost as many as the entire United States. Singapore and the Netherlands above Germany is the other giveaway. Both are transhipment hubs, where boxes come off one ship and go straight onto another without the country making or consuming anything, so any measure of what a country actually produces would put Germany and Japan far ahead of them.',
    slug='IS.SHP.GOOD.TU', source=src, sourceUrl=url))

# --------------------------------------------------------------- 57 migrants
src, url = WB('SM.POP.TOTL')
rows2, tot2 = tree('SM.POP.TOTL', 2024)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=2,
    truth='People living in a country other than the one they were born in, 2024',
    period='2024', unit='people',
    data=arr(rows2, 3, 0),
    answer='People living in a country other than the one they were born in',
    decoys=[
        'Visitors arriving from abroad each year',
        'People who have left this country to live elsewhere',
        'Refugees being housed',
        'Students enrolled from abroad',
        'People holding two passports',
        'Foreign workers on temporary permits',
        'Passengers passing through a country\u2019s airports'],
    hints=[
        'Saudi Arabia takes the third largest block, ahead of the United Kingdom and France.',
        'Australia and Canada are both here while India, China, Indonesia and Nigeria are nowhere at all. This counts people who came, not people who are there.',
        'A headcount rather than a rate. The largest circle is 52 million people, and the world total is 302 million.',
        'Every one of them holds a passport issued somewhere other than where they now sleep.'],
    why='The four most populous countries in the world are absent and Australia is present, which rules out anything that scales with population. Saudi Arabia and the United Arab Emirates so high rules out tourism, where Spain and France lead; and the United States first rules out the mirror-image reading of people leaving.',
    slug='SM.POP.TOTL', source=src, sourceUrl=url))

# ------------------------------------------------------------- 58 wine price
WINE = [('Indonesia', 23.08), ('Singapore', 22.87), ('Qatar', 20.75),
        ('Iceland', 20.61), ('United Arab Emirates', 20.03), ('Jordan', 19.28),
        ('Norway', 16.33), ('Thailand', 15.43), ('United States', 12.6),
        ('Australia', 11.4), ('United Kingdom', 10.64), ('Italy', 8.45),
        ('Spain', 7.61), ('France', 5.85), ('Chile', 5.34), ('Moldova', 2.24)]
P.append(dict(
    family='Ranking', form='Lollipop · ranked, 2016', type='lollipop', diff=3,
    truth='Price of a 750ml bottle of wine, 2016', period='2016',
    unit='US dollars',
    data=arr(WINE, 3, 2),
    answer='Price of a 750ml bottle of wine',
    decoys=[
        'Wine drunk per adult each year, in litres',
        'Wine produced per person, in litres',
        'Price of a packet of 20 cigarettes, in dollars',
        'Price of a Big Mac, in dollars',
        'Price of a litre of petrol, in dollars',
        'Cost of a restaurant meal, in dollars',
        'Tourist spending per visitor, in hundreds of dollars'],
    hints=[
        'Four of the top six are on the Arabian peninsula or in the tropics. Moldova is last, and Chile is second to last.',
        'The countries that actually make the stuff are all at the wrong end: Italy, Spain, France and Chile sit in the bottom five. This is not a measure of how much there is.',
        'Measured in US dollars for one standard bottle. The range runs from 2.24 to 23.08.',
        'In Indonesia the excise duty runs to roughly 150 per cent, which is why a bottle there costs ten times what it costs in Moldova.'],
    why='France, Italy and Spain in the bottom five is the whole puzzle. They are the three largest producers on earth, so any measure of volume, output or consumption would put them at the very top. Sorted by price they fall to the bottom, because what is being ranked is really alcohol duty.',
    slug='SA_0000001830', source='WHO Global Health Observatory',
    sourceUrl='https://www.who.int/data/gho/data/indicators'))

# ----------------------------------------------------------- 59 armed forces
src, url = WB('MS.MIL.TOTL.P1')
a95 = {nm(n): i + 1 for i, (n, v) in enumerate(wb.snap('MS.MIL.TOTL.P1', 1995))}
b20 = {nm(n): i + 1 for i, (n, v) in enumerate(wb.snap('MS.MIL.TOTL.P1', 2020))}
order = [n for n, _ in sorted(b20.items(), key=lambda k: k[1])[:12]]
assert all(n in a95 for n in order), 'entity continuity'
P.append(dict(
    family='Ranking', form='Rank slope · 1995 → 2020', type='slope', diff=3,
    truth='World ranking by the number of people in the armed forces, 1995 vs 2020',
    period='1995 → 2020', unit='rank by number of serving personnel',
    leftYear=1995, rightYear=2020,
    ranks=arr([(n, a95[n], b20[n]) for n in order], 3, 0),
    answer='World ranking by the number of people in the armed forces',
    decoys=[
        'World ranking by military spending',
        'World ranking by number of people',
        'World ranking by number of police officers',
        'World ranking by prison population',
        'World ranking by number of civil servants',
        'World ranking by number of people in work',
        'World ranking by number of university students'],
    hints=[
        'Indonesia climbs eight places and Egypt five. Iran and Turkey both slide down the board.',
        'North Korea is third, above Russia and the United States, and Germany, Japan, France and the United Kingdom appear nowhere at all. This is a headcount, and it is not a budget.',
        'A ranking, so the chart carries no units. First place is a little over two million people.',
        'It counts everyone in uniform: soldiers, sailors and air crew, conscript or volunteer.'],
    why='North Korea third with 26 million people is the single visible fact that kills almost every alternative. On spending it would not be near the top ten, and on population, workforce or students it would not appear at all. The absence of Germany, Japan and the United Kingdom rules out anything measuring money.',
    slug='MS.MIL.TOTL.P1', source=src, sourceUrl=url))

# ------------------------------------------------------------ 60 unemployment
src, url = WB('SL.UEM.TOTL.ZS')
s = wb.series('SL.UEM.TOTL.ZS', [2000, 2024])
# Five series maximum: the categorical palette has five slots.
SER = [('South Africa', 'ZAF'), ('Spain', 'ESP'), ('Greece', 'GRC'),
       ('United States', 'USA'), ('Japan', 'JPN')]
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2024', type='line', diff=4,
    truth='Share of the workforce out of a job, 2000 to 2024', period='2000–2024',
    unit='% of the labour force', suffix='%', startYear=2000,
    series=[(lab, [s[iso][y] for y in range(2000, 2025)]) for lab, iso in SER],
    answer='Share of the workforce out of a job',
    decoys=[
        'Share of adults living in poverty',
        'Government debt as a share of the economy',
        'Share of workers on temporary contracts',
        'Inflation, per cent a year',
        'Share of adults who rent rather than own',
        'Share of workers in part-time jobs',
        'Share of adults with no qualifications'],
    hints=[
        'Two of these lines climb a mountain that peaks in 2013. One has a single needle in 2020 and is back down within a year.',
        'The line that finishes highest, above 30 per cent, has risen almost throughout and never had a crisis to blame it on. Japan finishes at 2.5, which is too low a floor for most things you could put on this axis.',
        'Measured as a percentage of everyone in the labour force, so people who are not looking are not counted.',
        'It is the figure that jumps when a factory closes and falls when it reopens.'],
    why='Japan at 2.5 rules out poverty, renting and low qualifications, none of which reaches that floor in any rich country. The 2020 needle in the American line, gone within twelve months, is the shape of a lockdown rather than of a recession, and government debt would run to 250 per cent for Japan and burst the axis.',
    slug='SL.UEM.TOTL.ZS', source=src, sourceUrl=url))

# ------------------------------------------------------------ 61 forest change
src, url = WB('AG.LND.FRST.K2')
fr = wb.pair('AG.LND.FRST.K2', 1992, 2022)
ch = {nm(n): round(100 * (b - a) / a, 1) for n, a, b in fr if a > 5000}
FW = ['Vietnam', 'China', 'Spain', 'Italy', 'France', 'India', 'Turkey',
      'United States', 'Brazil', 'Democratic Republic of Congo', 'Indonesia',
      'Myanmar', 'Paraguay', 'Nicaragua', "Côte d'Ivoire"]
# The diverging bar's gutter is 148px and this name overruns it. Doc 16 hit the
# same name in the beeswarm lane; shortening the label is the safe fix here.
SHORT = {'Democratic Republic of Congo': 'DR Congo'}
P.append(dict(
    family='Deviation', form='Diverging bar · change against zero', type='deviation',
    reference=0, diff=3,
    truth='Change in the area covered by forest, 1992 to 2022', period='1992 → 2022',
    unit='% change since 1992', suffix='%',
    data=arr([(SHORT.get(c, c), ch[c]) for c in FW if c in ch], 3, 1),
    answer='Change in the area covered by forest since 1992',
    decoys=[
        'Change in the area used for farming',
        'Change in the number of people living in the countryside',
        'Change in the number of people',
        'Change in carbon dioxide emissions',
        'Change in the amount of grain harvested',
        'Change in the number of cattle kept',
        'Change in the area under irrigation'],
    hints=[
        'Vietnam and China are at one end. At the other, one West African country has lost nearly two thirds of what it had in 1992.',
        'Spain, Italy and France are all firmly on the positive side while Brazil and Indonesia are negative. The rich countries did their losing a century ago and have spent the last thirty years going the other way.',
        'Measured as a percentage change over thirty years, against a line at zero rather than an axis at zero.',
        'Côte d\u2019Ivoire cleared most of its share to plant cocoa, and it is now the world\u2019s largest grower.'],
    why='Every country on this chart grew its population between 1992 and 2022, so a negative half rules that reading out immediately. Europe positive and South East Asia negative also rules out farmland and cattle, which moved the other way. The pattern is the forest transition: countries reforest once they are rich enough to stop clearing.',
    slug='AG.LND.FRST.K2', source=src, sourceUrl=url))

for i, o in enumerate(P):
    o['exhibit'] = ex(50 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
