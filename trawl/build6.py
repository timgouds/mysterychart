#!/usr/bin/env python3
"""Assemble batch six (12 puzzles, indices 110 to 121). The last of the sixty.

Six at difficulty 1 or 2, because the pool is short of gentle openers and Tim
asked for more easy ones. Four at difficulty 4, because batch five tipped the
balance the other way and preflight then reported the dealer running short of
hard closers instead.
"""
import wb, subprocess, csv, io, sys
from common import ex, num, arr, block

WBU = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)
OW = ('Our World in Data', 'https://ourworldindata.org/grapher/%s')
NICE = {'Korea, Rep.': 'South Korea', 'Russian Federation': 'Russia',
        'Viet Nam': 'Vietnam', 'Turkiye': 'Turkey', 'Egypt, Arab Rep.': 'Egypt',
        'Iran, Islamic Rep.': 'Iran', 'Congo, Dem. Rep.': 'DR Congo',
        'Venezuela, RB': 'Venezuela', 'Syrian Arab Republic': 'Syria',
        'Somalia, Fed. Rep.': 'Somalia', 'Central African Republic': 'Central African Rep.',
        'Lao PDR': 'Laos', "Cote d'Ivoire": "Côte d'Ivoire",
        'Kyrgyz Republic': 'Kyrgyzstan', 'Slovak Republic': 'Slovakia'}
nm = lambda s: NICE.get(s, s)
SK = {'Monaco', 'San Marino', 'Andorra', 'Liechtenstein', 'Macao', 'Hong Kong',
      'Bermuda', 'Greenland', 'Faroe Islands', 'Nauru', 'Naoero', 'Tuvalu',
      'Palau', 'Kosovo', 'Channel Islands', 'Isle of Man', 'Aruba', 'Curacao',
      'Gibraltar', 'New Caledonia', 'French Polynesia', 'Cayman Islands',
      'Marshall Islands', 'Northern Mariana Islands', 'Guam', 'American Samoa',
      'Virgin Islands (U.S.)', 'Puerto Rico', 'Sint Maarten (Dutch part)',
      'St. Martin (French part)', 'Turks and Caicos Islands',
      'British Virgin Islands', 'West Bank and Gaza', 'Micronesia, Fed. Sts.'}
OWAGG = ('World', 'Asia', 'Africa', 'Europe', 'Americas', 'Oceania', 'income',
         'European Union', 'FAO', 'Least developed', 'Land Locked',
         'Small Island', 'Net Food', 'Union')


def owid(slug, time='2022'):
    txt = subprocess.run(['curl', '-s', '-m', '60',
        'https://ourworldindata.org/grapher/%s.csv?csvType=filtered&country=~ALL&time=%s'
        % (slug, time)], capture_output=True, text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows or rows[0][0].startswith('{'):
        sys.exit(slug + ': ' + txt[:120])
    out = {}
    for r in rows[1:]:
        if len(r) < 4 or not r[1] or not r[3]:
            continue
        e = nm(r[0])
        if e in SK or any(a in e for a in OWAGG):
            continue
        out[e] = float(r[3])
    return out


def snap(code, y):
    return [(nm(a), b) for a, b in wb.snap(code, y) if nm(a) not in SK]


def desc(d, keep=None):
    r = sorted(d.items(), key=lambda x: -x[1])
    return r[:keep] if keep else r


P = []

# ------------------------------------------------------- 110 land area (easy)
land = desc(dict(snap('AG.LND.TOTL.K2', 2022)), 12)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=1,
    truth='Land area, 2022', period='2022', unit='square kilometres',
    data=arr([(n, int(v)) for n, v in land], 3, 0),
    answer='Land area',
    decoys=[
        'Number of people',
        'Size of the economy',
        'Area of farmland',
        'Length of coastline',
        'Area covered by forest',
        'Length of the railway network',
        'Number of cities over a million people'],
    hints=[
        'Kazakhstan and Algeria both have circles here. Between them they hold about sixty million people.',
        'Kazakhstan, Algeria and Saudi Arabia are all present while Japan, Germany, Nigeria and Indonesia are not. Most of what is being counted here is empty.',
        'Counted in square kilometres. The largest is over sixteen million of them.',
        'Russia has twice as much of it as the next country, and most of that is Siberia.'],
    why='Russia has almost twice as much as Canada behind it, and the great bulk of that is Siberia: forest and tundra where barely anybody lives. Kazakhstan, Algeria and Saudi Arabia appearing while Japan, Germany, Nigeria and Indonesia do not is the whole thing. Three of the biggest circles are mostly steppe or desert, and the countries missing are among the most populous and richest on earth. Anything counting people, money or farmland would invert most of this list.',
    slug='AG.LND.TOTL.K2', source=WBU('AG.LND.TOTL.K2')[0], sourceUrl=WBU('AG.LND.TOTL.K2')[1]))

# --------------------------------------------------- 111 under fifteen (easy)
u15 = sorted((n, round(v, 1)) for n, v in snap('SP.POP.0014.TO.ZS', 2023))
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2023', type='beeswarm', diff=2,
    truth='Share of the population under fifteen, 2023', period='2023',
    unit='% of the population', suffix='%',
    data=arr(u15, 4, 1),
    label=['Niger', 'Chad', 'Nigeria', 'India', 'Brazil', 'United States',
           'China', 'Italy', 'Japan'],
    labelSm=['Niger', 'Nigeria', 'United States', 'China', 'Japan'],
    answer='Share of the population under fifteen',
    decoys=[
        'Share of the population in school',
        'Share of the population living in the countryside',
        'Share of the population without access to electricity',
        'Share of the population who cannot read',
        'Share of the population working in farming',
        'Share of the population born abroad',
        'Share of the population living in poverty'],
    hints=[
        'Japan and Italy are at the far left, and every country at the far right is in the Sahel.',
        'The whole swarm sits between about 11 and 49 per cent, and nothing goes near zero or a hundred. Italy and Japan at the bottom and Niger at the top is an age story, not a wealth one.',
        'Measured as a percentage of everybody alive in the country, sliced by a single birthday.',
        'Niger has nearly half its people below the age at which British children finish secondary school.'],
    why='The band from 11 to 49 per cent is the evidence: it never reaches zero and never approaches a hundred, which rules out schooling, electricity and literacy, all of which run from near nothing to near everything across this same set of countries. Japan and Italy at the bottom with Niger and Chad at the top is what a birth rate looks like carried forward fifteen years.',
    slug='SP.POP.0014.TO.ZS', source=WBU('SP.POP.0014.TO.ZS')[0],
    sourceUrl=WBU('SP.POP.0014.TO.ZS')[1]))

# ------------------------------------------------------- 112 oranges (easy)
orn = desc(owid('orange-production'), 12)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=2,
    truth='Oranges grown, 2022', period='2022', unit='tonnes a year',
    total=sum(int(v) for _, v in orn),
    data=arr([(n, int(v)) for n, v in orn], 3, 0),
    answer='Oranges grown',
    decoys=[
        'Lemons grown',
        'Bananas grown',
        'Grapes grown',
        'Olives grown',
        'Coffee grown',
        'Sugar cane grown',
        'Tea grown'],
    hints=[
        'Brazil has much the largest block, and Spain, Italy and Egypt all appear.',
        'Spain, Italy and Egypt are here while Poland, Germany and Russia are not, and neither is anywhere north of the Mediterranean. This wants a mild winter rather than a cold one.',
        'Counted in tonnes harvested in a year. The largest block is about seventeen million tonnes.',
        'Brazil grows about a third of the world supply and most of it is squeezed rather than eaten.'],
    why='Spain, Italy and Egypt present with no northern European country anywhere is the discriminator. Apples would put Poland, Turkey and Russia high and drop Brazil a long way; bananas would be tropical and lose Spain and Italy entirely. A Mediterranean and subtropical list led by Brazil is citrus, and most of Brazil\u2019s crop goes straight to juice concentrate.',
    slug='orange-production', source=OW[0], sourceUrl=OW[1] % 'orange-production'))

# ------------------------------------------------------- 113 spirits (easy)
sp = owid('spirits-consumption-per-person')
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022', type='beeswarm', diff=2,
    truth='Spirits drunk per adult, 2022', period='2022',
    unit='litres of pure alcohol per adult per year',
    data=arr(sorted((n, round(v, 2)) for n, v in sp.items()), 4, 2),
    label=['Belarus', 'Russia', 'Bulgaria', 'South Korea', 'Germany',
           'United States', 'France', 'Italy', 'Saudi Arabia'],
    labelSm=['Belarus', 'Russia', 'Germany', 'United States', 'Saudi Arabia'],
    answer='Spirits drunk per adult',
    decoys=[
        'Cigarettes smoked per adult',
        'Coffee drunk per adult',
        'Sugar eaten per adult',
        'Bottled water drunk per adult',
        'Fruit juice drunk per adult',
        'Tea drunk per adult',
        'Salt eaten per adult'],
    hints=[
        'A long tail sits at exactly zero, and the right-hand end is entirely eastern European with one exception from East Asia.',
        'Belarus and Russia lead, South Korea is close behind, and France and Italy are unremarkable in the middle. The countries at zero are dry by law rather than by preference.',
        'Measured in litres of pure alcohol per adult per year, which is why the leader reads under eight rather than in the hundreds.',
        'Vodka in the east, soju in Korea, and nothing at all in the countries sitting on zero.'],
    why='The cluster at exactly zero appears on every alcohol chart and nowhere else, because no other measure has a legally enforced floor. Within that, the eastern European lead with South Korea alongside is what separates this from wine, which puts Portugal, France and Italy at the front, and from beer, which puts Czechia and Austria there.',
    slug='spirits-consumption-per-person', source=OW[0],
    sourceUrl=OW[1] % 'spirits-consumption-per-person'))

# --------------------------------------------------------- 114 wheat (easy)
wht = desc(owid('wheat-production'), 12)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=2,
    truth='Wheat grown, 2022', period='2022', unit='tonnes a year',
    total=sum(int(v) for _, v in wht),
    data=arr([(n, int(v)) for n, v in wht], 3, 0),
    answer='Wheat grown',
    decoys=[
        'Rice grown',
        'Maize grown',
        'Rye grown',
        'Barley grown',
        'Soybeans grown',
        'Sugar beet grown',
        'Cotton grown'],
    hints=[
        'Russia, France, Canada, Australia and Ukraine all have blocks here, and none of them is tropical.',
        'France and Canada are both present while Indonesia, Vietnam, Bangladesh and the Philippines are absent altogether. That rules out the crop most of Asia actually lives on.',
        'Counted in tonnes harvested in a year. The largest block is about 138 million tonnes.',
        'It is the one that becomes bread, and Russia is the largest exporter of it in the world.'],
    why='The absence of Indonesia, Vietnam, Bangladesh and the Philippines is the tell: all four are enormous rice producers and none grows much of this. France, Canada, Australia and Ukraine appearing instead marks out the temperate grain belt, and Russia leads the world in exporting it, which is why the 2022 invasion moved bread prices everywhere.',
    slug='wheat-production', source=OW[0], sourceUrl=OW[1] % 'wheat-production'))

# ---------------------------------------------- 115 population change (easy)
pc = wb.pair('SP.POP.TOTL', 2000, 2023)
ch = {nm(n): 100 * (b - a) / a for n, a, b in pc if nm(n) not in SK and a > 2e6}
PW = ['Niger', 'Uganda', 'Angola', 'Iraq', 'Nigeria', 'Kenya', 'Saudi Arabia',
      'Egypt', 'Israel', 'Australia', 'India', 'Mexico', 'United States',
      'Brazil', 'France', 'China', 'Germany', 'Italy', 'Japan', 'Poland',
      'Portugal', 'Romania', 'Ukraine']
rows = sorted(((c, round(ch[c], 1)) for c in PW if c in ch), key=lambda r: -r[1])
assert len(rows) >= 20, len(rows)
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=2,
    truth='Change in the number of people since 2000', period='2000 → 2023',
    unit='% change since 2000', suffix='%',
    data=arr(rows, 3, 1),
    answer='Change in the number of people since 2000',
    decoys=[
        'Change in the number of births each year since 2000',
        'Change in average income since 2000',
        'Change in the number of people in work since 2000',
        'Change in the number of homes since 2000',
        'Change in the number of children in school since 2000',
        'Change in the size of the economy since 2000',
        'Change in the number of people living in cities since 2000'],
    hints=[
        'Niger and Uganda have more than doubled. Ukraine, Romania and Japan are all on the other side of the line.',
        'The negative bars are eastern and southern Europe plus Japan, and the positive ones are the Sahel and the Gulf. Nothing here has grown by more than about 130 per cent in twenty-three years, which is slow for anything to do with money.',
        'Measured as a percentage change over twenty-three years, against a line at zero.',
        'Niger has gone from eleven million people to twenty-six, and Ukraine has gone the other way.'],
    why='Very few economies shrank between 2000 and 2023, so a chart with eight countries below the line rules out income, output and employment straight away. The ceiling is the other half: money measures would show several countries up by three or four hundred per cent over that span, and nothing here passes 130. This is headcount, and Japan, Italy and eastern Europe are all shrinking.',
    slug='SP.POP.TOTL', source=WBU('SP.POP.TOTL')[0], sourceUrl=WBU('SP.POP.TOTL')[1]))

# ------------------------------------------------------------ 116 tax (hard)
tax = desc(dict(snap('GC.TAX.TOTL.GD.ZS', 2022)), 16)
P.append(dict(
    family='Ranking', form='Lollipop · the sixteen highest, 2022', type='lollipop', diff=4,
    truth='Tax collected by central government, as a share of the economy, 2022',
    period='2022', unit='% of GDP', suffix='%',
    data=arr([(n, round(v, 1)) for n, v in tax], 3, 1),
    answer='Tax collected by central government, as a share of the economy',
    decoys=[
        'Government spending, as a share of the economy',
        'Public debt, as a share of the economy',
        'Social security contributions, as a share of the economy',
        'Government spending on health, as a share of the economy',
        'Exports, as a share of the economy',
        'Money held in savings, as a share of the economy',
        'Government spending on pensions, as a share of the economy'],
    hints=[
        'Lesotho and Namibia are both near the top of this list. Germany, Japan and the United States do not appear on it at all.',
        'Nothing here reaches 40 per cent, and France, Germany and Italy are all absent despite being famously heavy on this. The reason is the word "central": in those countries a great deal is collected by regions or by separate social funds instead.',
        'Measured as a percentage of everything the country produces in a year. The highest figure is close to 31.',
        'Lesotho is high because most of what it collects arrives through a customs union with South Africa.'],
    why='This is a narrower thing than it looks, which is what makes it hard: it counts only what central government collects, so federal countries and those with separate social insurance funds score far lower than their real tax burden. That is why Germany and France are missing while Lesotho and Namibia are near the top, both of them collecting most of their revenue as customs receipts through the Southern African Customs Union.',
    slug='GC.TAX.TOTL.GD.ZS', source=WBU('GC.TAX.TOTL.GD.ZS')[0],
    sourceUrl=WBU('GC.TAX.TOTL.GD.ZS')[1]))

# --------------------------------------------------------- 117 arable (hard)
arb = sorted((n, round(v, 1)) for n, v in snap('AG.LND.ARBL.ZS', 2022))
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022', type='beeswarm', diff=4,
    truth='Share of a country\u2019s land that is used for crops, 2022', period='2022',
    unit='% of land area', suffix='%',
    data=arr(arb, 4, 1),
    label=['Bangladesh', 'Denmark', 'Ukraine', 'India', 'France', 'United States',
           'Brazil', 'Russia', 'Egypt'],
    labelSm=['Bangladesh', 'Denmark', 'France', 'Brazil', 'Egypt'],
    answer='Share of a country\u2019s land that is used for crops',
    decoys=[
        'Share of a country\u2019s land that is forest',
        'Share of a country\u2019s workers in farming',
        'Share of a country\u2019s land that is built on',
        'Share of a country\u2019s food that is grown at home',
        'Share of a country\u2019s land that is grazed',
        'Share of a country\u2019s exports that is food',
        'Share of a country\u2019s land that is desert'],
    hints=[
        'Denmark is second in the world at this, and Brazil, Russia and Canada are all a long way down.',
        'Denmark and Bangladesh at the top, with Brazil and Russia near the bottom, is the reverse of any ranking by how much a country actually grows. This is a share of the country rather than a quantity.',
        'Measured as a percentage of the country\u2019s total land area. The highest is about 61 per cent and the tail runs down towards zero.',
        'Denmark is small and almost entirely flat and fertile, so nearly two thirds of it is under the plough.'],
    why='Brazil and Russia near the bottom is the discriminator, and it catches almost everybody: both are agricultural giants, but they are also enormous, so the fraction of their land under crops is small. Denmark and Bangladesh top it by being small, flat and fertile with nothing else to do with the space. Workers in farming would invert the list entirely and put Denmark near the bottom.',
    slug='AG.LND.ARBL.ZS', source=WBU('AG.LND.ARBL.ZS')[0], sourceUrl=WBU('AG.LND.ARBL.ZS')[1]))

# ---------------------------------------------------------- 118 trade (hard)
s = wb.series('NE.TRD.GNFS.ZS', [2000, 2020])
TSER = [('Singapore', 'SGP'), ('Germany', 'DEU'), ('China', 'CHN'),
        ('Brazil', 'BRA'), ('United States', 'USA')]
for lab, iso in TSER:
    m = [y for y in range(2000, 2021) if y not in s[iso]]
    assert not m, (lab, m)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2022', type='line', diff=4,
    truth='Trade as a share of the economy, 2000 to 2022', period='2000–2022',
    unit='% of GDP', suffix='%', startYear=2000,
    series=[(lab, [round(s[iso][y], 1) for y in range(2000, 2021)]) for lab, iso in TSER],
    answer='Trade as a share of the economy',
    decoys=[
        'Government spending as a share of the economy',
        'Manufacturing as a share of the economy',
        'Investment as a share of the economy',
        'Services as a share of the economy',
        'Household spending as a share of the economy',
        'Debt as a share of the economy',
        'Wages as a share of the economy'],
    hints=[
        'One line spends the whole period above 300 per cent, which is a strange thing for a share of anything to do.',
        'The top line runs above 300 per cent throughout, so this is not a slice of the economy but a flow measured against it. Germany sits well clear of the other three, and the United States is the lowest of all five.',
        'Measured against the size of the economy, which is why a figure above 100 is possible at all.',
        'Singapore is above 300 because goods land there, are counted, and leave again.'],
    why='A figure above 300 per cent is the whole puzzle and it rules out every decoy at a glance: nothing that is genuinely a slice of the economy can exceed 100. Imports and exports are both counted in full against a much smaller domestic economy, so Singapore, a port that re-exports most of what arrives, runs over three times its own size. China\u2019s long fall after 2006 is its domestic market growing faster than its trade.',
    slug='NE.TRD.GNFS.ZS', source=WBU('NE.TRD.GNFS.ZS')[0], sourceUrl=WBU('NE.TRD.GNFS.ZS')[1]))

# ---------------------------------------------------- 119 wheat rank (slope)
w95 = owid('wheat-production', '1995')
w22 = owid('wheat-production', '2022')
r95 = {k: i + 1 for i, (k, v) in enumerate(desc(w95))}
order = [(k, i + 1) for i, (k, v) in enumerate(
    [x for x in desc(w22) if x[0] in r95 and r95[x[0]] <= 20][:12])]
assert len(order) >= 10, order
P.append(dict(
    family='Ranking', form='Rank slope · 1995 → 2022', type='slope', diff=3,
    truth='World ranking of wheat-growing countries, 1995 vs 2022',
    period='1995 → 2022', unit='rank by tonnes of wheat harvested',
    leftYear=1995, rightYear=2022,
    ranks=arr([(k, r95[k], r) for k, r in order], 3, 0),
    answer='World ranking of wheat-growing countries',
    decoys=[
        'World ranking of rice-growing countries',
        'World ranking of maize-growing countries',
        'World ranking by the amount of farmland',
        'World ranking by food exported',
        'World ranking by fertiliser used',
        'World ranking of barley-growing countries',
        'World ranking by the number of farms'],
    hints=[
        'Russia and Ukraine both climb. Argentina and Australia move around in the middle of the board.',
        'France, Canada and Australia are all in the top ten while Indonesia, Vietnam and Bangladesh are absent entirely. That is the wrong list for the grain most of Asia eats.',
        'A ranking, so the chart shows no units. First place harvests about 138 million tonnes.',
        'Russia\u2019s climb is why an invasion of Ukraine in 2022 moved the price of bread everywhere.'],
    why='France, Canada and Australia in the top ten with no south east Asian country anywhere marks this out as the temperate grain rather than rice or maize. Russia\u2019s rise is the story: it was a net importer in the 1990s and is now the largest exporter in the world, which is precisely why the war in Ukraine reached into shops thousands of miles away.',
    slug='wheat-production-rank', source=OW[0], sourceUrl=OW[1] % 'wheat-production'))

# ------------------------------------------------------ 120 freshwater (hard)
fw = desc(dict(snap('ER.H2O.FWTL.K3', 2021)), 12)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=4,
    truth='Fresh water taken from rivers and wells each year, 2021',
    period='2021', unit='cubic kilometres a year',
    data=arr([(n, round(v, 1)) for n, v in fw], 3, 1),
    answer='Fresh water taken from rivers and wells each year',
    decoys=[
        'Rainfall each year',
        'Water supplied to homes each year',
        'Electricity generated from water each year',
        'Volume of river flow reaching the sea',
        'Water lost to leaks each year',
        'Bottled water drunk each year',
        'Waste water treated each year'],
    hints=[
        'Pakistan and Iran both have circles larger than Japan\u2019s, and Egypt is here too.',
        'Pakistan, Iran and Egypt are all present and all three are dry countries. Whatever this counts, having little of it does not keep you off the list, which rules out anything that falls from the sky.',
        'Counted in cubic kilometres a year. The largest is about 647 of them, which is more than twice Lake Erie.',
        'Roughly seventy per cent of it goes on irrigation, which is why the dry farming countries are at the top.'],
    why='Egypt, Pakistan and Iran are among the driest countries on the list and are near the top, which is the opposite of how rainfall or river flow would rank. That is because this counts what is taken out rather than what is there, and about seventy per cent of it is used to irrigate crops. India first reflects the largest irrigated area in the world drawing hard on groundwater.',
    slug='ER.H2O.FWTL.K3', source=WBU('ER.H2O.FWTL.K3')[0],
    sourceUrl=WBU('ER.H2O.FWTL.K3')[1]))

# ---------------------------------------------------------- 121 hydro (hard)
hy = sorted((n, round(v, 1)) for n, v in snap('EG.ELC.HYRO.ZS', 2015))
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2015', type='beeswarm', diff=4,
    truth='Share of electricity generated from water, 2015', period='2015',
    unit='% of electricity generated', suffix='%',
    data=arr(hy, 4, 1),
    label=['Paraguay', 'Norway', 'Brazil', 'Canada', 'Sweden', 'China',
           'United States', 'Germany', 'Saudi Arabia'],
    labelSm=['Paraguay', 'Norway', 'Canada', 'United States', 'Saudi Arabia'],
    answer='Share of electricity generated from water',
    decoys=[
        'Share of electricity generated from coal',
        'Share of electricity generated from gas',
        'Share of electricity generated by wind',
        'Share of electricity that is imported',
        'Share of homes connected to the grid',
        'Share of electricity lost before it arrives',
        'Share of electricity used by industry'],
    hints=[
        'A cluster of countries sit at or very near 100, and another cluster sits at exactly zero.',
        'Norway, Paraguay, Nepal and Bhutan are all at or near 100, while the Gulf states are all at zero. Mountains and rainfall put a country at one end of this and flat desert puts it at the other.',
        'Measured as a percentage of all electricity generated. Both ends of the swarm are occupied: some countries are at 100 and some at 0.',
        'It needs a river with a drop in it, which is why Norway and Nepal are at one end and Saudi Arabia at the other.'],
    why='Both ends being fully occupied is what makes this readable: several countries generate essentially all their electricity this way and several generate none at all, which no fuel achieves so completely. Norway, Paraguay, Nepal and Bhutan are mountainous and wet; the Gulf states are flat and dry and sit at exactly zero. Wind would put Denmark at the top and nobody near 100.',
    slug='EG.ELC.HYRO.ZS', source=WBU('EG.ELC.HYRO.ZS')[0], sourceUrl=WBU('EG.ELC.HYRO.ZS')[1]))

for i, o in enumerate(P):
    o['exhibit'] = ex(110 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
