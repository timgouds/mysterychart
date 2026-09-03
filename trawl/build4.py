#!/usr/bin/env python3
"""Assemble batch four (12 puzzles, indices 86 to 97).

Sources: World Bank 7, Eurostat 2, WHO 1, OECD 1, plus one more Eurostat.
Forms skew to symbol / line / beeswarm and away from dumbbell and lollipop.
"""
import wb, eu, sys, json, csv, subprocess, collections
from common import ex, num, arr, NICE, nm, DROP, block

AGG = ('European Union', 'Euro area', 'EU27', 'EA19', 'EA20', 'European Economic Area')
EUNAME = {'Türkiye': 'Turkey', 'Germany (until 1990 former territory of the FRG)': 'Germany'}
WBU = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)
EUS = lambda c: ('Eurostat', 'https://ec.europa.eu/eurostat/databrowser/view/%s/default/table' % c)
# Territories and microstates distort every ranking and mean nothing to a player.
SKIP = set(DROP) | {'French Polynesia', 'New Caledonia', 'Bermuda', 'Cayman Islands'}


def top(code, y, keep=12):
    return [(nm(n), v) for n, v in wb.snap(code, y) if nm(n) not in SKIP][:keep]


def eu_slice(code, year, **pins):
    d, ids = eu.eurostat(code)
    gi, ti = ids.index('geo'), ids.index('time')
    idx = {k: ids.index(k) for k in pins}
    out = {}
    for key, v in d.items():
        if key[ti][0] != str(year):
            continue
        if any(key[idx[k]][0] != val for k, val in pins.items()):
            continue
        n = EUNAME.get(key[gi][1], key[gi][1])
        if any(s in n for s in AGG):
            continue
        out[n] = v
    return out


P = []

# ------------------------------------------------------------- 86 air freight
af = top('IS.AIR.GOOD.MT.K1', 2023)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=3,
    truth='Air freight flown by a country\u2019s airlines, 2023', period='2023',
    unit='million tonne-kilometres a year',
    data=arr([(n, int(v)) for n, v in af], 3, 0),
    answer='Air freight flown by a country\u2019s airlines',
    decoys=[
        'Passengers flown by a country\u2019s airlines',
        'Goods carried by a country\u2019s railways',
        'Goods carried by lorry',
        'Post handled each year',
        'Value of goods flown out of the country',
        'Aircraft registered in the country',
        'Cargo handled at a country\u2019s airports'],
    hints=[
        'Qatar is third and the United Arab Emirates fourth, both ahead of Germany, Japan and the United Kingdom.',
        'Qatar has under three million people and no manufacturing to speak of, yet it is third. Whatever this counts belongs to the airline rather than to the country, and two Gulf carriers have built their whole business on being a stop in the middle.',
        'Counted in millions of tonne-kilometres: one tonne carried one kilometre. The leader records 42,760 million of them.',
        'Qatar Airways and Emirates fly other people\u2019s cargo between other people\u2019s countries, and it is counted against the flag on the tail.'],
    why='The United States is first, at roughly 1.6 times China, because its carriers fly the largest domestic network in the world before they carry anything abroad. But Qatar third with a population of under three million is the real puzzle. This is measured by the nationality of the airline, not by what the country makes or buys, so Doha and Dubai score enormously as connecting hubs between Asia and Europe. Anything counting goods that actually enter or leave the country would put Germany and Japan far above both.',
    slug='IS.AIR.GOOD.MT.K1', source=WBU('IS.AIR.GOOD.MT.K1')[0],
    sourceUrl=WBU('IS.AIR.GOOD.MT.K1')[1]))

# ---------------------------------------------------------------- 87 reserves
res = top('FI.RES.TOTL.CD', 2023)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=3,
    truth='Foreign currency and gold held by the central bank, 2023',
    period='2023', unit='US dollars held in reserve',
    data=arr([(n, int(v)) for n, v in res], 3, 0),
    answer='Foreign currency and gold held by the central bank',
    decoys=[
        'Government debt owed to foreigners',
        'Value of goods exported each year',
        'Money held in savings accounts by households',
        'Value of the stock market',
        'Money invested abroad by pension funds',
        'Annual government spending',
        'Value of the country\u2019s oil reserves'],
    hints=[
        'Switzerland is fourth here, above Russia, South Korea and Saudi Arabia, and it exports almost nothing by weight.',
        'Switzerland and Hong Kong both appear high while the United States does not lead. Whatever this counts, the country that issues the world\u2019s main currency has the least need of it.',
        'Counted in US dollars held at a single moment rather than earned over a year. The largest is 3.4 trillion.',
        'It is the pile a central bank keeps so that it can defend its own currency if it has to.'],
    why='China holds 3.4 trillion dollars, roughly three times Japan, because two decades of trade surpluses were recycled into dollar assets rather than spent. The United States being unremarkable here is the tell: it prints the currency everyone else is holding, so it has little reason to stockpile anyone else\u2019s. Switzerland fourth comes from years of buying foreign currency to stop the franc rising.',
    slug='FI.RES.TOTL.CD', source=WBU('FI.RES.TOTL.CD')[0], sourceUrl=WBU('FI.RES.TOTL.CD')[1]))

# ----------------------------------------------------------------- 88 malaria
cn = {c['Code']: c['Title'] for c in json.load(open('who_countries.json'))['value']}
WHONAME = {'Democratic Republic of the Congo': 'DR Congo',
           'United Republic of Tanzania': 'Tanzania', "Côte d’Ivoire": "Côte d'Ivoire",
           'Cote d\'Ivoire': "Côte d'Ivoire", 'Niger': 'Niger'}
raw = subprocess.run(['curl', '-s', '-m', '90',
                      'https://ghoapi.azureedge.net/api/MALARIA_EST_CASES'],
                     capture_output=True, text=True).stdout
mal = [r for r in json.loads(raw)['value']
       if r.get('SpatialDimType') == 'COUNTRY' and r.get('TimeDim') == 2021
       and r.get('NumericValue')]
mal = sorted(((WHONAME.get(cn.get(r['SpatialDim'], r['SpatialDim']),
                           cn.get(r['SpatialDim'], r['SpatialDim'])), int(r['NumericValue']))
              for r in mal), key=lambda x: -x[1])[:12]
assert len(mal) == 12 and mal[0][1] > 5e7, mal[:3]
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=3,
    truth='Estimated malaria cases, 2021', period='2021',
    unit='cases a year', total=sum(v for _, v in mal),
    data=arr(mal, 3, 0),
    answer='Estimated malaria cases',
    decoys=[
        'Estimated tuberculosis cases',
        'People living with HIV',
        'Reported cholera cases',
        'Children not vaccinated against measles',
        'People without access to clean water',
        'Deaths of children under five',
        'People displaced by conflict'],
    hints=[
        'Every block on this square is in sub-Saharan Africa. India, China and Indonesia, which between them hold a third of humanity, are nowhere.',
        'Uganda is third and Burkina Faso and Mali are both here, while South Africa and Ethiopia are absent. The dividing line is not poverty but altitude and rainfall: this needs warm, wet, low-lying ground.',
        'Counted as estimated cases in a single year. The largest block alone is 65 million.',
        'It is carried by a mosquito that cannot breed in the cool highlands, which is why Ethiopia and South Africa escape the list.'],
    why='Nigeria alone accounts for about a quarter of the world total, and the first two blocks together for close to half. The absence of Ethiopia and South Africa is the discriminator: both are poor enough to head a list of tuberculosis, water or child mortality, but the highlands of one and the temperate south of the other are too cool for the anopheles mosquito to breed.',
    slug='MALARIA_EST_CASES', source='WHO Global Health Observatory',
    sourceUrl='https://www.who.int/data/gho/data/indicators'))

# ------------------------------------------------------------ 89 services
sv = top('BX.GSR.NFSV.CD', 2023)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=4,
    truth='Value of services sold abroad, 2023', period='2023',
    unit='US dollars a year', total=sum(int(v) for _, v in sv),
    data=arr([(n, int(v)) for n, v in sv], 3, 0),
    answer='Value of services sold abroad',
    decoys=[
        'Value of goods sold abroad',
        'Value of manufactured goods produced',
        'Money spent by visitors from abroad',
        'Value of financial assets held by foreigners',
        'Money spent on imports',
        'Value of software and technology exported',
        'Value of oil and gas exported'],
    hints=[
        'Ireland has the fourth largest block here, ahead of France, Singapore and China.',
        'Ireland fourth and Singapore sixth, with China only eighth and Germany above Japan, is the wrong order for anything made in a factory. China leads the world in goods by a distance and is nowhere near the top of this.',
        'Counted in US dollars in a single year. The largest block is just over a trillion.',
        'Nothing on this chart is a thing you can drop on your foot: it is banking, shipping, insurance, software licensing and tourism.'],
    why='The United States sells over a trillion dollars of services abroad, nearly twice the United Kingdom, on the strength of finance, cloud computing, software licensing and university fees. China eighth is the giveaway. It is comfortably the largest exporter of goods in the world, so any chart where it sits below Ireland, Singapore and the United Kingdom cannot be counting physical trade. Ireland is fourth because so much global software and pharmaceutical licensing is booked through Dublin for tax reasons, which inflates a country of five million into the top five.',
    slug='BX.GSR.NFSV.CD', source=WBU('BX.GSR.NFSV.CD')[0], sourceUrl=WBU('BX.GSR.NFSV.CD')[1]))

# ---------------------------------------------------------------- 90 tax wedge
tw = [x for x in csv.DictReader(open('o_DSD_TAX_PIT_DF_PIT_AV.csv'))
      if x['Measure'] == 'Tax wedge' and x['TIME_PERIOD'] == '2024'
      and x['INCOME_PRINCIPAL'] == 'AW100']
OEN = {'Türkiye': 'Turkey', 'Korea': 'South Korea', 'Slovak Republic': 'Slovakia',
       'Czechia': 'Czechia'}
twd = sorted({OEN.get(x['Reference area'], x['Reference area']): round(float(x['OBS_VALUE']), 1)
              for x in tw}.items())
assert len(twd) >= 30, len(twd)
P.append(dict(
    family='Distribution', form='Beeswarm · every OECD country, 2024',
    type='beeswarm', diff=4,
    truth='Share of the cost of employing someone that goes to the state, 2024',
    period='2024', unit='% of total labour cost', suffix='%',
    data=arr(twd, 4, 1),
    label=['Belgium', 'Germany', 'France', 'Italy', 'Sweden', 'United Kingdom',
           'United States', 'Chile', 'Colombia'],
    labelSm=['Belgium', 'Germany', 'United Kingdom', 'United States', 'Colombia'],
    answer='Share of the cost of employing someone that goes to the state',
    decoys=[
        'Share of national income collected in tax',
        'Top rate of income tax',
        'Rate of value added tax',
        'Share of workers who belong to a union',
        'Share of government spending that goes on pensions',
        'Employer pension contributions as a share of pay',
        'Share of the workforce employed by the state'],
    hints=[
        'Colombia sits at exactly zero and Chile at seven. Belgium, at the other end, is above half.',
        'The two lowest are in Latin America and the highest are all in continental Europe, but the United Kingdom and the United States sit closer to the bottom than the top. A floor of zero rules out anything every country must have.',
        'Measured as a percentage of what it costs an employer to put one average single worker on the payroll. The range runs from 0 to 52.',
        'Take the total cost of employing someone, subtract what actually reaches their bank account, and this is what is left.'],
    why='Colombia at zero is the discriminator, and it is real: a single worker on the average wage there pays no income tax and no employee social contribution, and the employer contributions are excluded from this measure. No country has a top income tax rate or a value added tax rate of zero, so any decoy of that kind dies on the left-hand end of the swarm alone.',
    slug='DSD_TAX_PIT', source='OECD',
    sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_TAX_PIT%40DF_PIT_AV'))

# ------------------------------------------------------- 91 out-of-pocket
oop = sorted((nm(n), round(v, 1)) for n, v in wb.snap('SH.XPD.OOPC.CH.ZS', 2022)
             if nm(n) not in SKIP)
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022',
    type='beeswarm', diff=3,
    truth='Share of health spending paid directly by patients, 2022',
    period='2022', unit='% of all health spending', suffix='%',
    data=arr(oop, 4, 1),
    label=['Nigeria', 'Bangladesh', 'India', 'Mexico', 'Greece', 'Germany',
           'United Kingdom', 'United States', 'Cuba'],
    labelSm=['Nigeria', 'India', 'Germany', 'United States', 'Cuba'],
    answer='Share of health spending paid directly by patients',
    decoys=[
        'Share of health spending that goes on medicines',
        'Share of health spending funded by government',
        'Share of the population with health insurance',
        'Share of health spending that goes on hospitals',
        'Share of doctors working privately',
        'Share of health spending funded from abroad',
        'Share of adults who saw a doctor in the last year'],
    hints=[
        'The United States is well down the left-hand half of this swarm, below Greece, Spain and Portugal.',
        'Cuba is at the very bottom and the United Kingdom is near it, while Nigeria and Bangladesh are at the top. The countries at the right-hand end are not the ones that spend most on health. They are the ones with the least organised way of paying for it.',
        'Measured as a percentage of everything spent on health in the country, from any source. The two ends are under 10 and nearly 80.',
        'It is the money that comes out of a patient\u2019s own pocket at the moment of treatment, with nothing standing between them and the bill.'],
    why='The United States sitting low is what makes this hard and what settles it. American health care is famously expensive, but most of the bill is paid by insurers and by government rather than at the counter, so it scores well here. The top of the swarm is countries with no functioning insurance system at all, where treatment is bought in cash or not bought.',
    slug='SH.XPD.OOPC.CH.ZS', source=WBU('SH.XPD.OOPC.CH.ZS')[0],
    sourceUrl=WBU('SH.XPD.OOPC.CH.ZS')[1]))

# --------------------------------------------------- 92 health spending line
s = wb.series('SH.XPD.CHEX.GD.ZS', [2000, 2020])
# Five series maximum: the palette has five categorical slots and a sixth line
# was silently drawn with no stroke at all.
HSER = [('United States', 'USA'), ('Germany', 'DEU'), ('United Kingdom', 'GBR'),
        ('Japan', 'JPN'), ('India', 'IND')]
for lab, iso in HSER:
    m = [y for y in range(2000, 2021) if y not in s[iso]]
    assert not m, (lab, m)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2020', type='line', diff=3,
    truth='Health spending as a share of the economy, 2000 to 2020',
    period='2000–2020', unit='% of GDP', suffix='%', startYear=2000,
    series=[(lab, [s[iso][y] for y in range(2000, 2021)]) for lab, iso in HSER],
    answer='Health spending as a share of the economy',
    decoys=[
        'Government spending on pensions, as a share of the economy',
        'Spending on education, as a share of the economy',
        'Spending on defence, as a share of the economy',
        'Household spending on food, as a share of the economy',
        'Spending on housing, as a share of the economy',
        'Government borrowing, as a share of the economy',
        'Spending on research, as a share of the economy'],
    hints=[
        'Every line ends higher than it starts, and every one of them lifts sharply in the final year shown.',
        'The top line reaches nearly 18 per cent, roughly double the next country, and India sits under 4. A single category taking a sixth of one rich country\u2019s entire economy narrows things sharply.',
        'Measured as a percentage of everything the country produces. The line ends in 2020.',
        'The jump at the end is the pandemic, and the line at the top belongs to the country that spends most and covers fewest.'],
    why='The lift in the final year is visible in all five lines at once, which points at something every country suddenly spent more on in the same year. The United States near 18 per cent, about double Britain and Japan and more than four times India, is the single most quoted statistic in health policy: it spends far more of its national income on this than anyone else without covering everybody.',
    slug='SH.XPD.CHEX.GD.ZS', source=WBU('SH.XPD.CHEX.GD.ZS')[0],
    sourceUrl=WBU('SH.XPD.CHEX.GD.ZS')[1]))

# ------------------------------------------------------------ 93 birth rate
s2 = wb.series('SP.DYN.CBRT.IN', [2000, 2023])
BSER = [('Nigeria', 'NGA'), ('India', 'IND'), ('United States', 'USA'),
        ('China', 'CHN'), ('South Korea', 'KOR')]
for lab, iso in BSER:
    m = [y for y in range(2000, 2024) if y not in s2[iso]]
    assert not m, (lab, m)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2023', type='line', diff=4,
    truth='Babies born each year per 1,000 people, 2000 to 2023',
    period='2000–2023', unit='births per 1,000 people', startYear=2000,
    series=[(lab, [round(s2[iso][y], 1) for y in range(2000, 2024)]) for lab, iso in BSER],
    answer='Babies born each year per 1,000 people',
    decoys=[
        'Deaths each year per 1,000 people',
        'People leaving the country each year per 1,000',
        'Marriages each year per 1,000 people',
        'Children starting school each year per 1,000 people',
        'People arriving from abroad each year per 1,000',
        'Households formed each year per 1,000 people',
        'Cars sold each year per 1,000 people'],
    hints=[
        'One line ends below five, less than a third of where it began, and no other line is close to it.',
        'The top line stays above 35 for the whole period while the bottom line falls under five. Nigeria and South Korea are the two ends, and the gap between them widens rather than closes.',
        'Counted per 1,000 people per year, so a figure of 40 means one person in twenty-five.',
        'South Korea is the line at the bottom, and the reason is the lowest fertility rate ever recorded anywhere.'],
    why='South Korea ending under five per 1,000 is the lowest such figure recorded in any country in peacetime, and the collapse from about 13 in 2000 is far faster than deaths, marriages or migration move. Nigeria holding above 35 across the same twenty-three years is the other end of the same story: the two lines diverge, which rules out anything driven by a shared global trend.',
    slug='SP.DYN.CBRT.IN', source=WBU('SP.DYN.CBRT.IN')[0], sourceUrl=WBU('SP.DYN.CBRT.IN')[1]))

# ------------------------------------------------- 94 age at first child
d, ids = eu.eurostat('demo_find')
gi, ti, ii = ids.index('geo'), ids.index('time'), ids.index('indic_de')
am = {}
for k, v in d.items():
    if k[ii][0] == 'AGEMOTH1':
        am.setdefault(EUNAME.get(k[gi][1], k[gi][1]), {})[int(k[ti][0])] = v
# Germany's series starts in 2009, Ireland's in 2007 and France has a six year
# hole from 2007. Six countries with no gaps, over the window they all share.
ASER = ['Italy', 'Spain', 'Portugal', 'Hungary', 'Bulgaria']
Y0, Y1 = 2003, 2022
for c in ASER:
    m = [y for y in range(Y0, Y1 + 1) if y not in am.get(c, {})]
    assert not m, (c, m, sorted(am.get(c, {}))[:3])
P.append(dict(
    family='Change over time', form='Multi-line · 2003 to 2022', type='line', diff=4,
    truth='Average age of women at the birth of their first child, 2003 to 2022',
    period='2003–2022', unit='years of age', startYear=Y0, baseline=24,
    series=[(c, [round(am[c][y], 1) for y in range(Y0, Y1 + 1)]) for c in ASER],
    answer='Average age of women at the birth of their first child',
    decoys=[
        'Average age of women when they stop working',
        'Average age at which women leave their parents\u2019 home',
        'Average age at which women finish education',
        'Average age of women at the birth of their last child',
        'Average age at which women start their first job',
        'Average age of women when they first buy a home',
        'Average age of men at the birth of their first child'],
    hints=[
        'Every line climbs, and none of them crosses another. The gap between the top line and the bottom one is about six years throughout.',
        'The whole set moves within a band from 25 to 32, and it moves slowly and steadily rather than in steps. Bulgaria is the lowest throughout and Italy the highest, which is an east to west split rather than a rich to poor one.',
        'Measured in years of age, from national birth registers rather than from a survey.',
        'It is the age at which a woman becomes a mother for the first time, and in Italy it is now over 31.'],
    why='The narrow band is the evidence. Twenty-five to thirty-two is too old for leaving home or finishing education and too young for a last child, and the lines move by only two or three years across twenty years, which is the pace of a demographic trend rather than a policy. Italy above 31 is the highest in Europe, and Bulgaria the lowest, an east to west gradient that has held for the whole period.',
    slug='demo_find-AGEMOTH1', source=EUS('demo_find')[0], sourceUrl=EUS('demo_find')[1]))

# ---------------------------------------------- 95 life expectancy ranks
a00 = {nm(n): i + 1 for i, (n, v) in enumerate(
    [x for x in wb.snap('SP.DYN.LE00.IN', 2000) if nm(x[0]) not in SKIP])}
b23 = [(nm(n), i + 1) for i, (n, v) in enumerate(
    [x for x in wb.snap('SP.DYN.LE00.IN', 2023) if nm(x[0]) not in SKIP])][:12]
b23 = [(n, r) for n, r in b23 if a00.get(n, 99) <= 22]
assert len(b23) >= 10, b23
P.append(dict(
    family='Ranking', form='Rank slope · 2000 → 2023', type='slope', diff=4,
    truth='World ranking by how long people live, 2000 vs 2023',
    period='2000 → 2023', unit='rank by life expectancy at birth',
    leftYear=2000, rightYear=2023,
    ranks=arr([(n, a00[n], r) for n, r in b23], 3, 0),
    answer='World ranking by how long people live',
    decoys=[
        'World ranking by income per person',
        'World ranking by spending on health per person',
        'World ranking by years of schooling',
        'World ranking by doctors per head',
        'World ranking by how safe people feel',
        'World ranking by how happy people say they are',
        'World ranking by the share of people over 65'],
    hints=[
        'Luxembourg climbs twelve places and Malta seven. Japan slips from first to fourth without anything going wrong there.',
        'Malta and Singapore are both in the top twelve while the United States, Germany and the United Kingdom are all absent. Money clearly helps, but it plainly is not what is being ranked.',
        'A ranking, so the chart carries no units. The gap between first and twelfth is under two years.',
        'The top of this list is a Mediterranean or East Asian diet, and the United States is nowhere near it.'],
    why='Hong Kong first, and Spain and Italy in the top eight, is a Mediterranean and East Asian pattern rather than a wealthy one. The absence of the United States, which spends more per head on health than anyone, is what rules out the money and health-spending readings: it sits around 40th on this ranking.',
    slug='SP.DYN.LE00.IN-rank', source=WBU('SP.DYN.LE00.IN')[0], sourceUrl=WBU('SP.DYN.LE00.IN')[1]))

# ------------------------------------------------------------ 96 house prices
hp15 = eu_slice('prc_hpi_a', 2015, unit='I15_A_AVG', purchase='TOTAL')
hp24 = eu_slice('prc_hpi_a', 2024, unit='I15_A_AVG', purchase='TOTAL')
both = sorted(set(hp15) & set(hp24))
# Turkey is excluded: this index is nominal, and with lira inflation running
# above 50 per cent a year its figure measures the currency rather than the
# housing market. Leaving it in would have made every other bar a stub.
rows = sorted(((c, round(hp24[c] - 100, 1)) for c in both
               if abs(hp15[c] - 100) < 0.01 and c != 'Turkey'),
              key=lambda r: -r[1])[:16]
assert len(rows) == 16, (len(rows), rows[:4])
P.append(dict(
    # Drawn as a diverging bar first, but nothing is negative: Finland is the
    # lowest at +1.3. A diverging bar with no bars below the line is a ranking
    # wearing the wrong form, so this is a lollipop.
    family='Ranking', form='Lollipop · ranked, 2024', type='lollipop', diff=3,
    truth='Change in house prices since 2015', period='2015 → 2024',
    unit='% change since 2015', suffix='%',
    data=arr(rows, 3, 1),
    answer='Change in house prices since 2015',
    decoys=[
        'Change in rents since 2015',
        'Change in average wages since 2015',
        'Change in the number of homes built since 2015',
        'Change in the cost of living since 2015',
        'Change in the number of households since 2015',
        'Change in mortgage interest rates since 2015',
        'Change in the share of people who own their home since 2015'],
    hints=[
        'The three largest rises are all in central or eastern Europe, and the figures are well over 100 per cent in nine years.',
        'Hungary has more than trebled while Italy has barely moved, a spread of nearly two hundred points over nine years. Wages and the cost of living moved within a far narrower band than that everywhere in Europe.',
        'Measured as a percentage change against an index set to 100 in 2015, so zero is where things stood that year.',
        'Hungary and the Baltic states more than doubled theirs, and Italy is the country that barely moved at all.'],
    why='Hungary at 210 per cent against Italy at 12 is a spread no wage or price index in Europe came close to over the same nine years. Italy has had almost no house price growth since the financial crisis, while central Europe and the Baltics had the fastest on the continent, which is why this looks so much more violent than a cost of living chart. Turkey is left off deliberately: its index is nominal and lira inflation would have put it above 600 per cent, measuring the currency rather than the housing market.',
    slug='prc_hpi_a', source=EUS('prc_hpi_a')[0], sourceUrl=EUS('prc_hpi_a')[1]))

# ------------------------------------------------------- 97 protected land
pl = sorted((nm(n), round(v, 1)) for n, v in wb.snap('ER.LND.PTLD.ZS', 2022)
            if nm(n) not in SKIP)
assert len(pl) >= 100, len(pl)
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022',
    type='beeswarm', diff=4,
    truth='Share of a country\u2019s land that is legally protected, 2022',
    period='2022', unit='% of land area', suffix='%',
    data=arr(pl, 4, 1),
    label=['Venezuela', 'Bhutan', 'Germany', 'Brazil', 'United Kingdom',
           'United States', 'India', 'Turkey', 'Iraq'],
    labelSm=['Venezuela', 'Germany', 'United States', 'India', 'Iraq'],
    answer='Share of a country\u2019s land that is legally protected',
    decoys=[
        'Share of a country\u2019s land that is forest',
        'Share of a country\u2019s land used for farming',
        'Share of a country\u2019s land that is mountainous',
        'Share of a country\u2019s land that is desert',
        'Share of a country\u2019s land that is publicly owned',
        'Share of a country\u2019s land that is built on',
        'Share of a country\u2019s land that is above 1,000 metres'],
    hints=[
        'Germany is high in this swarm, well above Brazil and the United States, which is not where you would expect a crowded country to sit.',
        'Germany above Brazil, and the United Kingdom above India, is the wrong way round for anything geographical. This is a matter of designation rather than of terrain, and Europe has designated a great deal of ordinary countryside.',
        'Measured as a percentage of total land area. The swarm runs from nearly zero to over half.',
        'Europe scores highly because its national parks and nature reserves are drawn around farmland and villages, not around wilderness.'],
    why='Germany and the United Kingdom sitting above Brazil is the discriminator, and it is a definitional artefact rather than a conservation triumph. European protected areas are landscape designations that include farms, roads and towns, while a Brazilian or American national park is closer to genuine wilderness. Anything measuring actual terrain would put the Europeans far below the tropics.',
    slug='ER.LND.PTLD.ZS', source=WBU('ER.LND.PTLD.ZS')[0], sourceUrl=WBU('ER.LND.PTLD.ZS')[1]))

for i, o in enumerate(P):
    o['exhibit'] = ex(86 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
