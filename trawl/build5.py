#!/usr/bin/env python3
"""Assemble batch five (12 puzzles, indices 98 to 109).

Deliberately easy: preflight reported the dealer running out of gentle openers
(only 20 of 98 puzzles at difficulty 2 or less). These are food, drink and farm
animals, where the top of the ranking is iconic and one inferential step from
the answer, which is what doc 08 found difficulty actually turns on.

Snapshots outnumber time series here, against the doc 16 preference. That is the
trade: a ranking whose leader you recognise instantly is the easy shape, and
easy is what the pool is short of.
"""
import subprocess, csv, io, sys, json
from common import ex, num, arr, block

OW = ('Our World in Data', 'https://ourworldindata.org/grapher/%s')
AGG = ('World', 'Asia', 'Africa', 'Europe', 'Americas', 'Oceania', 'income',
       'European Union', 'FAO', 'Least developed', 'Land Locked', 'Small Island',
       'Net Food', 'High-income', 'Low-income', 'Middle-income', 'Union')
SKIP = {'Monaco', 'San Marino', 'Andorra', 'Liechtenstein', 'Macao', 'Bermuda',
        'Greenland', 'Faroe Islands', 'Nauru', 'Tuvalu', 'Palau', 'Kosovo',
        'Northern Cyprus', 'Micronesia (country)'}
NAME = {'Democratic Republic of Congo': 'DR Congo', 'Cote d\'Ivoire': "Côte d'Ivoire",
        'United States': 'United States', 'Czechia': 'Czechia'}


def owid(slug, time='2022'):
    """Fetch one OWID grapher as {entity: value}. country=~ALL because a
    filtered request otherwise honours the chart's own preset selection and
    silently returns a handful of countries (doc 07)."""
    url = ('https://ourworldindata.org/grapher/%s.csv?csvType=filtered'
           '&country=~ALL&time=%s' % (slug, time))
    txt = subprocess.run(['curl', '-s', '-m', '60', url], capture_output=True,
                         text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows or rows[0][0].startswith('{'):
        sys.exit('%s: %s' % (slug, txt[:120]))
    out = {}
    for r in rows[1:]:
        if len(r) < 4 or not r[1] or not r[3]:
            continue
        e = NAME.get(r[0], r[0])
        if e in SKIP or any(a in e for a in AGG):
            continue
        out[e] = float(r[3])
    return out


def owid_years(slug):
    """Every year for every entity, from one request.

    The line renderer walks values annually from startYear, so a series sampled
    every four years silently drew a 33 year span as a 9 year one and the axis
    read 1990 to 1998. Fetch the whole series instead of sampling it."""
    txt = subprocess.run(['curl', '-s', '-m', '90',
        'https://ourworldindata.org/grapher/%s.csv?csvType=full' % slug],
        capture_output=True, text=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    out = {}
    for r in rows[1:]:
        if len(r) < 4 or not r[1] or not r[3]:
            continue
        e = NAME.get(r[0], r[0])
        if e in SKIP or any(a in e for a in AGG):
            continue
        out.setdefault(e, {})[int(r[2])] = float(r[3])
    return out


def desc(d, keep=None):
    r = sorted(d.items(), key=lambda x: -x[1])
    return r[:keep] if keep else r


P = []

# ------------------------------------------------------------------ 98 wine
wine = owid('wine-consumption-per-capita')
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022', type='beeswarm', diff=2,
    truth='Wine drunk per adult, 2022', period='2022',
    unit='litres of pure alcohol per adult per year',
    data=arr(sorted((k, round(v, 2)) for k, v in wine.items()), 4, 2),
    label=['Portugal', 'France', 'Italy', 'Australia', 'Germany',
           'United States', 'China', 'India', 'Saudi Arabia'],
    labelSm=['Portugal', 'France', 'Germany', 'United States', 'Saudi Arabia'],
    answer='Wine drunk per adult',
    decoys=[
        'Cigarettes smoked per adult',
        'Coffee drunk per adult',
        'Chocolate eaten per adult',
        'Bottled water drunk per adult',
        'Milk drunk per adult',
        'Fruit juice drunk per adult',
        'Tea drunk per adult'],
    hints=[
        'A long tail of countries sit at exactly zero, and Portugal is out on its own at the far right.',
        'Portugal, France and Italy are the top three, with Moldova among them. That is a very particular strip of Europe, and it is not the one that would top a chart about beer.',
        'Measured in litres of pure alcohol per adult per year, so the figures look small: the leader is under seven.',
        'Portugal drinks more of it per head than anyone, and the countries at zero are dry for legal rather than cultural reasons.'],
    why='Portugal, France and Italy at the very top is about as iconic an ordering as this game offers. Beer would put Czechia, Austria and Poland at the front and drop France well down; spirits would put Belarus and the Baltic states there. The cluster at exactly zero is the same set of countries that appears on any alcohol chart, where the reason is prohibition rather than taste.',
    slug='wine-consumption-per-capita', source=OW[0], sourceUrl=OW[1] % 'wine-consumption-per-capita'))

# ------------------------------------------------------------------ 99 beer
beer = owid('beer-consumption-per-person')
P.append(dict(
    family='Ranking', form='Lollipop · the sixteen highest, 2022', type='lollipop', diff=2,
    truth='Beer drunk per adult, 2022', period='2022',
    unit='litres of pure alcohol per adult per year',
    data=arr([(k, round(v, 2)) for k, v in desc(beer, 16)], 3, 2),
    answer='Beer drunk per adult',
    decoys=[
        'Bottled water drunk per adult',
        'Coffee drunk per adult',
        'Sparkling wine drunk per adult',
        'Cigarettes smoked per adult',
        'Sugar eaten per adult',
        'Milk drunk per adult',
        'Chocolate eaten per adult'],
    hints=[
        'Czechia is first, and has been for as long as anybody has kept the figures. Namibia is second.',
        'Czechia, Austria, Poland and Croatia fill the top, while France, Italy and Portugal are nowhere on this list at all. Those three would head almost any other drinking chart in Europe.',
        'Measured in litres of pure alcohol per adult per year, which is why the leader reads under seven rather than in the hundreds.',
        'Czechia has topped this table every year it has been counted, and Namibia is second because of who colonised it.'],
    why='Czechia first and no French, Italian or Portuguese entry anywhere on the list is the whole puzzle: those three lead the wine chart and are absent here. Namibia second is the oddity worth keeping, and it is a colonial inheritance, since German brewers set up there before 1915 and the taste stayed.',
    slug='beer-consumption-per-person', source=OW[0], sourceUrl=OW[1] % 'beer-consumption-per-person'))

# ------------------------------------------------------------------ 100 milk
milk = owid('per-capita-milk-consumption')
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022', type='beeswarm', diff=2,
    truth='Milk and dairy consumed per person, 2022', period='2022',
    unit='kilograms per person per year',
    data=arr(sorted((k, round(v, 1)) for k, v in milk.items()), 4, 1),
    label=['Ireland', 'Denmark', 'Netherlands', 'Switzerland', 'India',
           'United States', 'Brazil', 'China', 'Nigeria'],
    labelSm=['Ireland', 'Netherlands', 'United States', 'China', 'Nigeria'],
    answer='Milk and dairy consumed per person',
    decoys=[
        'Cheese eaten per person',
        'Sugar eaten per person',
        'Potatoes eaten per person',
        'Bread eaten per person',
        'Coffee drunk per person',
        'Eggs eaten per person',
        'Fish eaten per person'],
    hints=[
        'Ireland and Denmark are away on the right, and China and most of East Asia are bunched at the left.',
        'The gap between Ireland and China is roughly thirty to one, and the countries at the bottom are almost all East and South East Asian. Something about that part of the world makes this particular thing hard to digest.',
        'Measured in kilograms per person per year. The leader is close to 600, which is more than a litre and a half a day.',
        'Most adults in East Asia are lactose intolerant, and the chart is essentially a map of who can drink it comfortably.'],
    why='Ireland at nearly 600 kilograms a head against China under 20 is a thirtyfold gap, far wider than any other staple food produces. It follows lactase persistence: north western Europeans kept the ability to digest this into adulthood and most of East Asia did not. Cheese would put France and Greece at the top rather than Ireland and Denmark.',
    slug='per-capita-milk-consumption', source=OW[0], sourceUrl=OW[1] % 'per-capita-milk-consumption'))

# ------------------------------------------------------------------ 101 pigs
pigs = owid('pig-livestock-count-heads', '2023')
pt = desc(pigs, 12)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=2,
    truth='Number of pigs, 2023', period='2023', unit='head of livestock',
    total=sum(int(v) for _, v in pt),
    data=arr([(k, int(v)) for k, v in pt], 3, 0),
    answer='Number of pigs',
    decoys=[
        'Number of sheep',
        'Number of chickens',
        'Number of goats',
        'Number of donkeys',
        'Number of horses',
        'Number of farms',
        'Number of tractors'],
    hints=[
        'One country holds about half this square. Spain, Germany and Denmark all have blocks, and Denmark has under six million people.',
        'India, Pakistan, Nigeria, Indonesia and Turkey are all absent, and between them they hold about a quarter of humanity. That is not an accident of farming.',
        'Counted as live animals at a single moment. The largest block is over 400 million of them.',
        'Every country missing from this square is either Muslim or, in India\u2019s case, largely Hindu.'],
    why='The absence is the evidence. India, Indonesia, Pakistan, Bangladesh, Nigeria, Egypt and Turkey are all missing, which no other farm animal would produce: cattle would put India first outright, and sheep would put China, India and Nigeria in the top five. Denmark appearing with fewer than six million people is the other tell, since it raises roughly twelve million of these at a time.',
    slug='pig-livestock-count-heads', source=OW[0], sourceUrl=OW[1] % 'pig-livestock-count-heads'))

# ---------------------------------------------------------------- 102 cattle
cattle = owid('cattle-livestock-count-heads', '2023')
ct = desc(cattle, 12)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=2,
    truth='Number of cattle, 2023', period='2023', unit='head of livestock',
    data=arr([(k, int(v)) for k, v in ct], 3, 0),
    answer='Number of cattle',
    decoys=[
        'Number of sheep',
        'Number of goats',
        'Number of water buffalo',
        'Tonnes of beef eaten',
        'Number of dairy farms',
        'Tonnes of milk produced',
        'Number of horses'],
    hints=[
        'Brazil and India have the two largest circles, and Ethiopia has a bigger one than Argentina.',
        'India is at the top rather than at the bottom, which rules out anything about eating them. Ethiopia and Sudan both appear, and neither exports much of anything.',
        'Counted as live animals at a single moment. The two largest are each around 200 million.',
        'India has more of them than anywhere on earth and eats almost none, because they are sacred.'],
    why='India second with roughly 190 million is the discriminator, and it is exactly why this cannot be a chart about beef or dairy exports: most of those animals are never eaten. Brazil first, Ethiopia fourth and Sudan in the list is a herd ranking rather than an industry one, and pigs would drop India, Ethiopia and Sudan off it entirely.',
    slug='cattle-livestock-count-heads', source=OW[0], sourceUrl=OW[1] % 'cattle-livestock-count-heads'))

# -------------------------------------------------------------- 103 potatoes
pot = owid('potato-production')
ptt = desc(pot, 12)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=2,
    truth='Potatoes grown, 2022', period='2022', unit='tonnes a year',
    total=sum(int(v) for _, v in ptt),
    data=arr([(k, int(v)) for k, v in ptt], 3, 0),
    answer='Potatoes grown',
    decoys=[
        'Rice grown',
        'Maize grown',
        'Sugar beet grown',
        'Turnips grown',
        'Onions grown',
        'Cabbages grown',
        'Cassava grown'],
    hints=[
        'Ukraine, Poland, Germany and the Netherlands all have blocks here, and so do China and India.',
        'Ukraine, Belarus and Poland together take a large share, and Belarus has nine million people. This is a crop that does well in cold, damp ground where wheat struggles.',
        'Counted in tonnes harvested in a year. The largest block is about 95 million tonnes.',
        'It came from the Andes, it saved and then starved Ireland, and eastern Europe grows more of it per head than anyone.'],
    why='Belarus and the Netherlands appearing beside China and India is what settles it. Rice would be almost entirely Asian and drop every European entry; wheat would put Russia, the United States, France and Canada at the front. A crop that thrives in cool wet soil is the only thing that puts Ukraine, Poland, Belarus and the Netherlands on the same square as the two giants.',
    slug='potato-production', source=OW[0], sourceUrl=OW[1] % 'potato-production'))

# ---------------------------------------------------------------- 104 apples
app = owid('apple-production')
at = desc(app, 12)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=1,
    truth='Apples grown, 2022', period='2022', unit='tonnes a year',
    data=arr([(k, int(v)) for k, v in at], 3, 0),
    answer='Apples grown',
    decoys=[
        'Pears grown',
        'Bananas grown',
        'Grapes grown',
        'Mangoes grown',
        'Olives grown',
        'Coffee grown',
        'Pineapples grown'],
    hints=[
        'One circle is larger than all the others put together. Poland has the second or third biggest.',
        'Poland, Italy and France are all here while Brazil, Indonesia and the Philippines are not. This grows in a cold winter, not a warm one.',
        'Counted in tonnes harvested in a year. The leader grows about 48 million tonnes of them.',
        'It needs a proper frost to fruit well, which is why Poland is near the top and the tropics are absent.'],
    why='China grows about half the world total, but the useful evidence is Poland second and Turkey, Italy and France all present while Brazil, India and the tropics are largely absent. This is a temperate fruit that needs winter chilling, so bananas, mangoes and pineapples are ruled out by the geography of the list alone.',
    slug='apple-production', source=OW[0], sourceUrl=OW[1] % 'apple-production'))

# -------------------------------------------------------------- 105 tomatoes
tom = owid('tomato-production')
tt = desc(tom, 12)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=3,
    truth='Tomatoes grown, 2022', period='2022', unit='tonnes a year',
    total=sum(int(v) for _, v in tt),
    data=arr([(k, int(v)) for k, v in tt], 3, 0),
    answer='Tomatoes grown',
    decoys=[
        'Onions grown',
        'Cucumbers grown',
        'Peppers grown',
        'Aubergines grown',
        'Watermelons grown',
        'Courgettes grown',
        'Olives grown'],
    hints=[
        'Turkey, Egypt and Italy all have blocks, and so do China, India and the United States.',
        'Italy and Spain are both here and Egypt is high, while northern Europe is absent entirely. This one likes heat and, in Italy\u2019s case, ends up in a tin.',
        'Counted in tonnes harvested in a year. The largest block is about 68 million tonnes.',
        'Italy grows them to process rather than to sell whole, which is why it outranks countries with far more farmland.'],
    why='China grows about a third of the world\u2019s tomatoes, three times the next country, mostly for domestic use across an enormous population. But Italy fifth is the tell, and it is a processing industry rather than a salad one: most of the Italian crop is canned or turned into paste. Turkey and Egypt high, with no northern European entry at all, rules out onions and cucumbers, both of which grow perfectly well in cooler climates and would put the Netherlands and Poland on the board.',
    slug='tomato-production', source=OW[0], sourceUrl=OW[1] % 'tomato-production'))

# ------------------------------------------------------------------ 106 meat
meat = owid('meat-production-tonnes')
mt = desc(meat, 12)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=2,
    truth='Meat produced, 2022', period='2022', unit='tonnes a year',
    data=arr([(k, int(v)) for k, v in mt], 3, 0),
    answer='Meat produced',
    decoys=[
        'Grain harvested',
        'Milk produced',
        'Fish caught',
        'Vegetables grown',
        'Fruit grown',
        'Eggs produced',
        'Animal feed imported'],
    hints=[
        'Brazil has the third largest circle and Argentina is here too, but India, which has more farm animals than anywhere, is well down the list.',
        'India is far smaller here than its herds would suggest, while Brazil and Argentina are large. Whatever this counts, having the animals is not the same as using them this way.',
        'Counted in tonnes produced in a year. The largest is around 95 million tonnes.',
        'India keeps the world\u2019s largest cattle herd and turns almost none of it into this.',
        ],
    why='China produces roughly twice as much as the United States behind it, on the back of a pig herd of over 400 million animals. India is the more useful giveaway: it holds the largest cattle herd on earth and roughly a fifth of the world\u2019s farm animals, yet sits well down this list, because most of those animals are kept for milk and draught rather than slaughtered. Brazil and Argentina punching above their population is the mirror image of the same point.',
    slug='meat-production-tonnes', source=OW[0], sourceUrl=OW[1] % 'meat-production-tonnes'))

# ------------------------------------------------ 107 cattle rank over time
# Doc 03's entity-continuity trap, twice over: Ethiopia is absent before 1993
# (pre-split figures sit under "Ethiopia PDR") and Sudan before 2012 (the South
# seceded in 2011). 1995 clears Ethiopia; Sudan is dropped rather than shortening
# the window to eleven years, which would leave too little movement to read.
c90 = owid('cattle-livestock-count-heads', '1995')
c23 = owid('cattle-livestock-count-heads', '2023')
r90 = {k: i + 1 for i, (k, v) in enumerate(desc(c90))}
order = [(k, i + 1) for i, (k, v) in enumerate(
    [x for x in desc(c23) if x[0] in r90 and r90[x[0]] <= 18][:12])]
assert len(order) >= 10, order
P.append(dict(
    family='Ranking', form='Rank slope · 1995 → 2023', type='slope', diff=3,
    truth='World ranking by the size of the cattle herd, 1995 vs 2023',
    period='1995 → 2023', unit='rank by head of cattle',
    leftYear=1995, rightYear=2023,
    ranks=arr([(k, r90[k], r) for k, r in order], 3, 0),
    answer='World ranking by the size of the cattle herd',
    decoys=[
        'World ranking by beef eaten',
        'World ranking by milk produced',
        'World ranking by area of farmland',
        'World ranking by number of farmers',
        'World ranking by grain harvested',
        'World ranking by leather exported',
        'World ranking by rural population'],
    hints=[
        'Pakistan and Tanzania both climb several places. The two at the top swap around and nobody else gets near them.',
        'Ethiopia is fourth and Tanzania is in the top ten, while Germany, France and the United Kingdom are nowhere. A ranking led by Brazil and India, with Ethiopia fourth, is about the animals rather than about what is done with them.',
        'A ranking, so the chart shows no units. First and second are each close to 200 million.',
        'India and Brazil hold roughly a fifth of the world\u2019s herd between them, and India eats almost none of its share.'],
    why='India at or near the top throughout is what rules out beef, leather and most of the rest: the herd is enormous and is not eaten. Ethiopia fourth is the other half of the same argument, since it has no meat or dairy industry of any global size. The climbers are all African and South Asian, which is where herds have grown with population.',
    slug='cattle-livestock-count-heads-rank', source=OW[0],
    sourceUrl=OW[1] % 'cattle-livestock-count-heads'))

# ------------------------------------------------------- 108 milk over time
mall = owid_years('per-capita-milk-consumption')
Y0, Y1 = 1990, 2020
MC = ['Ireland', 'Netherlands', 'United States', 'Brazil', 'China']
for c in MC:
    miss = [y for y in range(Y0, Y1 + 1) if y not in mall.get(c, {})]
    assert not miss, (c, miss[:4])
P.append(dict(
    family='Change over time', form='Multi-line · 1990 to 2020', type='line', diff=3,
    truth='Milk and dairy consumed per person, 1990 to 2020', period='1990–2022',
    unit='kilograms per person per year', startYear=1990,
    series=[(c, [round(mall[c][y], 1) for y in range(Y0, Y1 + 1)]) for c in MC],
    answer='Milk and dairy consumed per person',
    decoys=[
        'Meat eaten per person',
        'Sugar eaten per person',
        'Fish eaten per person',
        'Cheese eaten per person',
        'Eggs eaten per person',
        'Vegetables eaten per person',
        'Bread eaten per person'],
    hints=[
        'One line loses a third of its height, bottoms out around 2010 and then climbs steeply past where it began. The lowest line has quietly multiplied several times over.',
        'The Netherlands and the United States drift gently down across the whole period while China climbs steadily from almost nothing. Whatever this is, the rich countries had reached their limit by 1990 and China had not started.',
        'Measured in kilograms per person per year, and it counts everything made from it rather than just what is poured into a glass.',
        'China\u2019s climb is the story of a country that historically could not digest it deciding to drink it anyway.'],
    why='China multiplying from almost nothing is the clearest signal: no other staple has that shape, because no other staple was so nearly absent from the Chinese diet in 1990. Ireland is the oddity worth knowing about. Its late climb is not people drinking more but the end of European milk quotas in 2015, after which Irish output rose sharply, and this series counts national supply in milk equivalent rather than what anybody actually pours.',
    slug='per-capita-milk-consumption-time', source=OW[0],
    sourceUrl=OW[1] % 'per-capita-milk-consumption'))

# --------------------------------------------------- 109 wine, then and now
w00 = owid('wine-consumption-per-capita', '2000')
w22 = wine
WW = ['China', 'Russia', 'United States', 'Australia', 'Sweden', 'Netherlands',
      'Germany', 'United Kingdom', 'Spain', 'Argentina', 'Portugal', 'France',
      'Italy']
rows = sorted(((c, round(w22[c] - w00[c], 2)) for c in WW if c in w00 and c in w22),
              key=lambda r: -r[1])
assert len(rows) >= 11, rows
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=3,
    truth='Change in wine drunk per adult since 2000', period='2000 → 2022',
    unit='change in litres of pure alcohol per adult',
    data=arr(rows, 3, 2),
    answer='Change in wine drunk per adult since 2000',
    decoys=[
        'Change in beer drunk per adult since 2000',
        'Change in spirits drunk per adult since 2000',
        'Change in coffee drunk per adult since 2000',
        'Change in sugar eaten per adult since 2000',
        'Change in cigarettes smoked per adult since 2000',
        'Change in milk drunk per adult since 2000',
        'Change in bottled water drunk per adult since 2000'],
    hints=[
        'France and Italy are the two deepest bars on the negative side. China and Russia are on the other.',
        'The countries that fall hardest are exactly the ones that still lead the chart in absolute terms. They are not giving it up because they never liked it.',
        'Measured as a change in litres of pure alcohol per adult, against a line at zero, over twenty-two years.',
        'French consumption has been falling since the 1960s, and it is still among the highest in the world.'],
    why='France and Italy falling furthest while China and Russia rise is a convergence pattern, and it is specific to wine: the traditional producers have been drinking steadily less since the 1960s as daily table wine gave way to occasional drinking, while newer markets grow from almost nothing. Beer over the same period rose in China and fell only modestly in Europe, so it would not produce this shape.',
    slug='wine-consumption-per-capita-change', source=OW[0],
    sourceUrl=OW[1] % 'wine-consumption-per-capita'))

for i, o in enumerate(P):
    o['exhibit'] = ex(98 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
