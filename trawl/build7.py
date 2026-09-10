#!/usr/bin/env python3
"""Assemble batch seven (12 puzzles, indices 122 to 133).

Six at difficulty 1 or 2: preflight reports the dealer running short of gentle
openers, with only 34 of 122 puzzles pitched that easily.

Three departures from the brief, each forced by something the screening found:

  - Temperature cannot be a beeswarm. drawBeeswarm maps x from zero
    (X = mL + v/top * plotW), so Canada at -1.7 and Russia at -2.3 land at
    negative x and fall off the canvas. Drawn as a diverging bar around a line
    at zero instead, which handles negatives and value-labels every row, so the
    sub-zero tail is visible evidence rather than a missing dot.
  - Transmission losses therefore takes the beeswarm, at 2014 levels. A
    diverging bar of the 2000 to 2014 change is a muddle (Congo -42 beside
    Iraq +42); the levels have a clean floor at 2 and a clean ceiling at 78.
  - Kuwait is out of the fertiliser slope. It is the biggest riser, 77 to 3,
    but drawSlope scales on maxRank, so a rank of 77 crushes ranks 1 to 20
    into the top quarter of the chart. Vietnam, 20 to 8, carries the story.

Also: EG.ELC.NUCL.ZS starts in 1990, not 1985.
"""
import wb, eu, subprocess, csv, io, sys, json
from common import ex, num, arr, block, nm, DROP

WBU = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)
OW = ('Our World in Data', 'https://ourworldindata.org/grapher/%s')
EUS = lambda c: ('Eurostat',
                 'https://ec.europa.eu/eurostat/databrowser/view/%s/default/table' % c)
WHOS = ('WHO Global Health Observatory', 'https://www.who.int/data/gho/data/indicators')

OWAGG = ('World', 'Asia', 'Africa', 'Europe', 'Americas', 'Oceania', 'income',
         'European Union', 'FAO', 'Least developed', 'Land Locked',
         'Small Island', 'Net Food', 'Union', 'G20', 'OECD')
EUAGG = {'EU', 'EU27_2020', 'EU28', 'EU27_2007', 'EA', 'EA18', 'EA19', 'EA20', 'EA21'}
EUNAME = {'Türkiye': 'Turkey'}


def owid(slug, time):
    txt = subprocess.run(['curl', '-s', '--compressed', '-m', '90',
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
        if e in DROP or any(a in e for a in OWAGG):
            continue
        out[e] = float(r[3])
    return out


def eugeo(code, **f):
    """Eurostat, collapsed to {country: value} with the aggregates dropped."""
    data, ids = eu.eurostat(code, **f)
    gi = ids.index('geo')
    out = {}
    for k, v in data.items():
        c, lab = k[gi]
        if c in EUAGG:
            continue
        out[EUNAME.get(lab, lab)] = v
    return out


def wbsnap(code, y):
    return [(nm(a), b) for a, b in wb.snap(code, y) if nm(a) not in DROP]


def pick(d, names, dec, label=''):
    """Rows for a chosen country list, asserting every one is present."""
    miss = [n for n in names if n not in d]
    if miss:
        sys.exit('%s: missing %s' % (label, miss))
    return [(n, round(d[n], dec)) for n in names]


def pairpick(a, b, names, dec, label=''):
    miss = [n for n in names if n not in a or n not in b]
    if miss:
        sys.exit('%s: missing %s' % (label, miss))
    rows = [(n, round(a[n], dec), round(b[n], dec)) for n in names]
    rows.sort(key=lambda r: r[2])
    return rows


P = []

# ------------------------------------------------- 122 temperature (easy)
tmp = owid('average-annual-surface-temperature', '2024')
TW = ['Djibouti', 'Mali', 'United Arab Emirates', 'Nigeria', 'Kenya',
      'Indonesia', 'Brazil', 'India', 'Egypt', 'Australia', 'Spain', 'France',
      'Japan', 'Germany', 'United States', 'United Kingdom', 'China', 'Sweden',
      'Iceland', 'Canada', 'Russia']
trows = pick(tmp, TW, 1, 'temperature')
assert trows[-1][1] < 0 and trows[-2][1] < 0, trows[-3:]
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=1,
    truth='Average annual temperature, 2024', period='2024',
    unit='degrees Celsius',
    data=arr(sorted(trows, key=lambda r: -r[1]), 3, 1),
    answer='Average annual temperature',
    decoys=[
        'Average age of everyone living there',
        'Deaths from infectious disease per 100,000 people',
        'Average number of people in each household',
        'Average number of hours worked each week',
        'Average number of days of frost each year',
        'Average time spent travelling to work, in minutes',
        'Average number of years spent in school'],
    hints=[
        'Djibouti and Mali are level at the top and there is nothing between them. Two countries sit on the far side of the line.',
        'Canada and Russia are on the negative side, so whatever is counted here can be less than nothing. Mali and Nigeria lead a list they would be at the bottom of if this were about people or about money.',
        'Measured in degrees Celsius, as one figure for a whole country across a whole year.',
        'Djibouti is desert on the Red Sea, and most of Russia is Siberia.'],
    why='Two bars pointing the other way is the whole puzzle: almost nothing measured country by country can be less than zero, and the two that are here are the two largest and coldest countries on earth. Djibouti and Mali are level at the top at 29.7, which is a national figure rather than a summer afternoon. Iceland at 0.9 sits between the two groups and is the reason the scale has to run through zero rather than start at it.',
    slug='average-annual-temperature', source=OW[0],
    sourceUrl=OW[1] % 'average-annual-surface-temperature'))

# ------------------------------------------------ 123 walk or cycle (easy)
pe = eugeo('hlth_ehis_pe6e', isced11='TOTAL', sex='T', age='TOTAL',
           unit='PC', time='2019')
pe = sorted(pe.items(), key=lambda x: -x[1])
assert len(pe) >= 30, len(pe)
assert min(v for _, v in pe) > 0, 'a reported zero: check it is not missing data'
pew = [(n, round(v, 1)) for n, v in pe[:12] + pe[-6:]]
P.append(dict(
    family='Ranking', form='Lollipop · highest and lowest, 2019', type='lollipop',
    diff=2, breakAfter=12,
    truth='Share of Europeans who walk or cycle at least 30 minutes a day, 2019',
    period='2019', unit='% of adults', suffix='%',
    data=arr(pew, 3, 1),
    answer='Share of Europeans who walk or cycle at least 30 minutes a day',
    decoys=[
        'Share of Europeans who travel to work by car',
        'Share of Europeans who commute by train',
        'Share of Europeans who eat fruit and vegetables every day',
        'Share of Europeans who own the home they live in',
        'Share of Europeans who live in a flat',
        'Share of Europeans who work from home',
        'Share of Europeans who belong to a sports club'],
    hints=[
        'Cyprus reports one tenth of one per cent. The Netherlands reports more than four in ten.',
        'The bottom of the chart is Cyprus, Malta, Portugal and Spain, all close to nothing at all, so this is not something every household has some of. Slovakia and Poland sitting above France and Italy rules out money as well.',
        'Measured as a percentage of adults answering a European health survey in 2019. The threshold is half an hour, every day.',
        'The Dutch do it on two wheels and the Danes and the Finns do it on two feet.'],
    why='The Netherlands is far out in front at 44 per cent, roughly one and a half times Slovakia behind it, and the reason is that cycling there is transport rather than exercise. The bottom of the chart is the discriminator: Cyprus at 0.1 and Malta at 2.4 rule out anything a household either has or does not have, because no measure of cars, homes or meals collapses that far. Slovakia, Hungary and Poland above France and Spain rules out wealth in the other direction.',
    slug='walking-and-cycling', source=EUS('hlth_ehis_pe6e')[0],
    sourceUrl=EUS('hlth_ehis_pe6e')[1]))

# ----------------------------------------------- 124 bath or shower (easy)
E1 = dict(hhcomp='TOTAL', rskpovth='TOTAL', sex='T', age='TOTAL', unit='PC')
b10 = eugeo('ilc_mdho02', time='2010', **E1)
b20 = eugeo('ilc_mdho02', time='2020', **E1)
BW = ['Romania', 'Latvia', 'Bulgaria', 'Lithuania', 'Estonia', 'North Macedonia',
      'Poland', 'Hungary', 'Portugal', 'Italy', 'France', 'Spain',
      'Netherlands', 'Germany']
brows = pairpick(b10, b20, BW, 1, 'bath')
P.append(dict(
    family='Change over time', form='Dumbbell · 2010 and 2020', type='dumbbell',
    diff=2, leftYear=2010, rightYear=2020,
    truth='Share of Europeans with no bath or shower at home, 2010 vs 2020',
    period='2010 → 2020', unit='% of the population', suffix='%',
    data=arr(brows, 3, 1),
    answer='Share of Europeans with no bath or shower at home',
    decoys=[
        'Share of Europeans who have never used the internet',
        'Share of Europeans who rent rather than own their home',
        'Share of Europeans living in an overcrowded home',
        'Share of Europeans living in a home with a leaking roof',
        'Share of Europeans who live in a flat rather than a house',
        'Share of Europeans who moved home in the past year',
        'Share of Europeans living in a home built before 1946'],
    hints=[
        'Germany, Spain and the Netherlands all report either nothing or a tenth of one per cent. Romania reports twenty one.',
        'Half the countries here are pinned against zero and stay there, which no measure of renting, crowding or damp ever does, because those never reach nothing anywhere. Everything that moves at all moves the same way.',
        'Measured as a percentage of the population, from the annual European survey of living conditions.',
        'Romania has spent twenty years plumbing its villages, and has halved the figure without closing the gap.'],
    why='Romania is more than twice Latvia behind it and about a hundred times Germany, and the reason is rural: a third of Romanians live in villages where mains water arrived late or has not arrived. The floor is what gives the chart away. Germany, the Netherlands and Malta report zero, and almost nothing else measured across Europe reaches zero at all, because renting, crowding and damp exist everywhere. What is left is a piece of plumbing that rich countries finished installing decades ago.',
    slug='no-bath-or-shower', source=EUS('ilc_mdho02')[0],
    sourceUrl=EUS('ilc_mdho02')[1]))

# --------------------------------------------------- 125 nuclear (easy)
nuc = wb.series('EG.ELC.NUCL.ZS', [1990, 2015])
NSER = [('France', 'FRA'), ('Lithuania', 'LTU'), ('Japan', 'JPN'),
        ('Germany', 'DEU'), ('United States', 'USA')]
for lab, iso in NSER:
    miss = [y for y in range(1990, 2016) if y not in nuc[iso]]
    assert not miss, (lab, miss)
assert nuc['LTU'][2011] == 0 and nuc['JPN'][2014] == 0
P.append(dict(
    family='Change over time', form='Multi-line · 1990 to 2015', type='line',
    diff=2, startYear=1990,
    truth='Share of electricity generated from nuclear power, 1990 to 2015',
    period='1990–2015', unit='% of electricity generated', suffix='%',
    series=[(lab, [round(nuc[iso][y], 1) for y in range(1990, 2016)])
            for lab, iso in NSER],
    answer='Share of electricity generated from nuclear power',
    decoys=[
        'Share of electricity generated from coal',
        'Share of electricity generated from gas',
        'Share of electricity generated from oil',
        'Share of electricity generated by wind',
        'Share of electricity that is imported',
        'Share of electricity used by industry',
        'Share of homes connected to the grid'],
    hints=[
        'One line runs almost flat for twenty five years. Two others fall off a cliff, one year apart, and neither comes back.',
        'Lithuania goes to zero in 2010 and Japan very close to it in 2011. Nothing that is bought, burnt or traded behaves like that: those are switches being thrown, not markets moving.',
        'Measured as a percentage of everything the country generates in a year. France sits above 70 throughout.',
        'Lithuania closed Ignalina as a condition of joining the European Union. Japan turned everything off after Fukushima.'],
    why='The two cliffs are a year apart and neither recovers, which is the tell: a fuel loses share gradually, but a fleet of reactors can be switched off in a single year by a decision. Lithuania shut Ignalina at the end of 2009 as a condition of European Union membership and went from about 70 per cent to nothing. Japan idled every reactor after Fukushima in 2011. France, meanwhile, has not moved: it built its way to three quarters in the 1980s and has stayed there ever since. The series ends in 2015, which is where the World Bank stops.',
    slug='nuclear-electricity', source=WBU('EG.ELC.NUCL.ZS')[0],
    sourceUrl=WBU('EG.ELC.NUCL.ZS')[1]))

# ----------------------------------------------------- 126 books (easy)
bk = sorted(owid('new-books-per-million', '2009').items(), key=lambda x: -x[1])
assert bk[0][0] == 'Iceland', bk[:3]
P.append(dict(
    family='Ranking', form='Lollipop · the sixteen highest, 2009', type='lollipop',
    diff=2,
    truth='New book titles published for every million people, 2009',
    period='2009', unit='titles a year per million inhabitants',
    data=arr([(n, int(round(v))) for n, v in bk[:16]], 3, 0),
    answer='New book titles published for every million people',
    decoys=[
        'University students for every million people',
        'Road deaths for every million people',
        'New films released for every million people',
        'Museums open for every million people',
        'Court cases brought for every million people',
        'Newspapers printed for every million people',
        'Marriages registered for every million people'],
    hints=[
        'Iceland is first by half as much again, and five of the next six are Nordic. Germany and France are not on the chart at all.',
        'The leader records 5,677 for every million inhabitants. That is far too few to be students and far too many to be anything that kills, and Cyprus and Estonia sitting above Spain and Austria rules out size.',
        'Counted per million inhabitants in 2009, which is why Iceland, with a third of a million people, comes first.',
        'Icelanders give them to each other on Christmas Eve and spend the night reading.'],
    why='Iceland publishes 5,677 for every million inhabitants, roughly one and three quarter times Norway behind it, and the reason is arithmetic as much as culture: a population of about 330,000 that still expects a full national literature in its own language produces a very large number per head. The Christmas Eve book flood, jolabokaflod, is the visible form of it. Dividing by population is also why Germany and France are missing while Estonia, Slovenia and Cyprus are here. The figures are for 2009, the last year with wide international coverage.',
    slug='new-books-published', source=OW[0],
    sourceUrl=OW[1] % 'new-books-per-million'))

# -------------------------------------------------- 127 rainfall (easy)
rn = sorted(owid('average-precipitation-per-year', '2025').items(),
            key=lambda x: -x[1])
rnw = [(n, round(v, 1)) for n, v in rn[:10] + rn[-8:]]
assert rnw[-1][0] == 'Egypt' and rnw[-1][1] < 10, rnw[-1]
P.append(dict(
    family='Ranking', form='Lollipop · log scale, wettest and driest, 2025',
    type='lollipop', diff=2, breakAfter=10, log=True,
    truth='Rainfall each year, 2025', period='2025', unit='millimetres a year',
    data=arr(rnw, 3, 1),
    answer='Rainfall each year',
    decoys=[
        'Kilometres of coastline',
        'Hours of sunshine each year',
        'Tonnes of fish caught each year',
        'Metres above sea level',
        'Species of bird recorded',
        'Hectares of rice planted each year',
        'Kilometres of navigable river'],
    hints=[
        'Papua New Guinea and the Solomon Islands are level at the top. Egypt is at the other end with a figure six hundred times smaller.',
        'Egypt, Libya and the Gulf states are last, which is exactly the wrong way round for anything to do with sun. They are not short of coast either, and no country has six kilometres of it.',
        'Measured in millimetres totted up over a year, on a scale where each step is ten times the last, because the range is too wide for anything else.',
        'In parts of the Sahara there are years when none of it arrives at all.'],
    why='The range is the point: the top of this chart is roughly six hundred and fifty times the bottom, which is why it has to be drawn on a logarithmic scale. Papua New Guinea and the Solomon Islands sit in the wettest belt on earth, where warm ocean air is pushed up over mountains and drops what it is carrying. Egypt at 6.4 millimetres is a whole country living off a river that rises somewhere else. The wet end being islands is the trap: it looks like a coastline ranking until you notice Libya and Egypt, which have plenty of coast, at the bottom.',
    slug='rainfall-each-year', source=OW[0],
    sourceUrl=OW[1] % 'average-precipitation-per-year'))

# ------------------------------------------------------- 128 noise (mid)
E2 = dict(hhcomp='TOTAL', rskpovth='TOTAL', unit='PC')
n13 = eugeo('ilc_mddw01', time='2013', **E2)
n23 = eugeo('ilc_mddw01', time='2023', **E2)
NW = ['Malta', 'Luxembourg', 'Portugal', 'Netherlands', 'Germany', 'Spain',
      'Finland', 'France', 'Austria', 'Italy', 'Sweden', 'Poland', 'Bulgaria',
      'Croatia', 'North Macedonia']
nrows = pairpick(n13, n23, NW, 1, 'noise')
P.append(dict(
    family='Change over time', form='Dumbbell · 2013 and 2023', type='dumbbell',
    diff=3, leftYear=2013, rightYear=2023,
    truth='Share of Europeans reporting noise from neighbours or the street, 2013 vs 2023',
    period='2013 → 2023', unit='% of households', suffix='%',
    data=arr(nrows, 3, 1),
    answer='Share of Europeans reporting noise from neighbours or the street',
    decoys=[
        'Share of Europeans who live in a town or city',
        'Share of Europeans living in an overcrowded home',
        'Share of Europeans living in a home with a leaking roof',
        'Share of Europeans behind with a bill or a rent payment',
        'Share of Europeans who live in a flat rather than a house',
        'Share of Europeans who moved home in the last five years',
        'Share of Europeans with no garden or balcony'],
    hints=[
        'Luxembourg has gone from eighteen per cent to thirty in ten years. Finland has nearly doubled. North Macedonia and Croatia have fallen, and sit at five and seven.',
        'Malta, Luxembourg, the Netherlands and Germany are at the top and North Macedonia, Croatia and Bulgaria are at the bottom. Every measure of hardship in Europe runs the other way round, and nothing here passes thirty two, which is far too low for a count of who lives in a town.',
        'Measured as the percentage of households answering yes to one question in the annual European survey of living conditions.',
        'It is the complaint you acquire once you live somewhere dense, expensive and very close to other people.'],
    why='This is the one deprivation question in the European survey that the rich countries lead. Malta and Luxembourg are the two most crowded countries in the European Union, and the Netherlands and Germany are not far behind; North Macedonia, Croatia and Bulgaria, which top nearly every other hardship measure, are at the bottom. The reason is that the answer depends on having neighbours close enough to hear and a street busy enough to hear from, so it tracks density and traffic rather than money. Luxembourg has risen twelve points in a decade while its population grew by a quarter.',
    slug='noise-at-home', source=EUS('ilc_mddw01')[0],
    sourceUrl=EUS('ilc_mddw01')[1]))

# -------------------------------------------------- 129 keeping warm (mid)
w10 = eugeo('ilc_mdes01', time='2010', **E2)
w24 = eugeo('ilc_mdes01', time='2024', **E2)
WW = ['North Macedonia', 'Bulgaria', 'Greece', 'Lithuania', 'Spain', 'Portugal',
      'Cyprus', 'France', 'Romania', 'Italy', 'Poland', 'Estonia', 'Finland',
      'Norway']
wrows = pairpick(w10, w24, WW, 1, 'warm')
assert w10['Bulgaria'] > 60 and w24['Spain'] > w10['Spain']
P.append(dict(
    family='Change over time', form='Dumbbell · 2010 and 2024', type='dumbbell',
    diff=3, leftYear=2010, rightYear=2024,
    truth='Share of Europeans who cannot keep their home warm enough, 2010 vs 2024',
    period='2010 → 2024', unit='% of households', suffix='%',
    data=arr(wrows, 3, 1),
    answer='Share of Europeans who cannot keep their home warm enough',
    decoys=[
        'Share of Europeans who cannot afford to replace worn out furniture',
        'Share of Europeans with no internet connection at home',
        'Share of Europeans who cannot afford meat or fish every other day',
        'Share of Europeans behind with the rent or the mortgage',
        'Share of Europeans living in a home built before 1946',
        'Share of Europeans with no washing machine',
        'Share of Europeans sharing a bathroom with another household'],
    hints=[
        'Bulgaria was at sixty six per cent in 2010 and is at nineteen now. Spain and France have gone the other way.',
        'Greece, Spain, Portugal and Cyprus all sit above Poland, Estonia and Romania, and Norway and Finland are at the bottom. That ordering is wrong for anything measuring money on its own, and half the chart has got worse since 2010, which nothing to do with connections or appliances has.',
        'Measured as the percentage of households answering yes in the European survey of living conditions. Norway reports 2.2.',
        'The Mediterranean built for summer, so heating a house there is expensive, inefficient and often not really attempted.'],
    why='The ordering is upside down and that is the puzzle. Spain, Greece, Portugal and Cyprus are all above Poland, Estonia and Romania, and Norway and Finland are near the bottom, because the countries that get properly cold built for it: insulation, double glazing and central heating are standard in the north and often absent around the Mediterranean. North Macedonia leads at 27 per cent. Bulgaria is the great improver, down from 66 per cent, while Spain and France have got worse since 2010, most of that arriving with the energy prices of 2022.',
    slug='cannot-keep-home-warm', source=EUS('ilc_mdes01')[0],
    sourceUrl=EUS('ilc_mdes01')[1]))

# ------------------------------------------------- 130 not active (mid)
def who(code, year):
    raw = subprocess.run(['curl', '-s', '--compressed', '-m', '90',
                          'https://ghoapi.azureedge.net/api/' + code],
                         capture_output=True, text=True).stdout
    rows = [r for r in json.loads(raw)['value']
            if r.get('SpatialDimType') == 'COUNTRY' and r.get('Dim1') == 'SEX_BTSX'
            and r.get('TimeDim') == year and r.get('NumericValue') is not None]
    iso = wb.real_countries()
    out = {}
    for r in rows:
        name = nm(iso.get(r['SpatialDim'], r['SpatialDim']))
        if name not in DROP:
            out[name] = float(r['NumericValue'])
    return out

pac = who('NCD_PAC', 2022)
assert len(pac) > 150, len(pac)
PACL = ['United Arab Emirates', 'Cuba', 'Kuwait', 'South Korea', 'Portugal',
        'India', 'United States', 'Germany', 'Malawi']
for n in PACL:
    assert n in pac, n
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2022', type='beeswarm',
    diff=3,
    truth='Share of adults who are physically inactive, 2022', period='2022',
    unit='% of adults', suffix='%',
    data=arr(sorted((n, round(v, 1)) for n, v in pac.items()), 4, 1),
    label=PACL, labelSm=['Cuba', 'India', 'United States', 'Germany', 'Malawi'],
    answer='Share of adults who are physically inactive',
    decoys=[
        'Share of adults who are in paid work',
        'Share of adults who travel to work by car',
        'Share of adults who live in a town or city',
        'Share of adults who own a television',
        'Share of adults who use the internet every day',
        'Share of adults who sleep less than seven hours a night',
        'Share of adults who have never left their own country'],
    hints=[
        'The United Arab Emirates, Cuba and Kuwait are within a fraction of each other at one end. Malawi is at the other, thirty times lower.',
        'Germany sits at fifteen per cent, well below India at forty nine and the United States at thirty six, while Malawi, Tanzania and Uganda are all under five. A rich country beneath a poor one rules out anything bought, and nothing in the swarm approaches a hundred, so it is not work or cities either.',
        'Measured by the World Health Organization as the percentage of adults falling short of its weekly guideline.',
        'If your work is done by hand in a field, and you walk to the field, you will never fall short of it.'],
    why='The bottom of the swarm is the evidence. Malawi at 2.1 per cent, Tanzania and Uganda are among the poorest countries on earth, and the reason they sit there is that most work is farming done on foot, so the weekly guideline is met without anybody intending it. The top three, the United Arab Emirates, Cuba and Kuwait, are separated by less than a point. Germany at 15 below India at 49 is the line that kills the money answers: this tracks what work and travel are made of rather than what a country can afford, which is also why Portugal is the odd one out in western Europe.',
    slug='physical-inactivity', source=WHOS[0], sourceUrl=WHOS[1]))

# ---------------------------------------------- 131 cropland per head (mid)
arb = {nm(a): (b, c) for a, b, c in wb.pair('AG.LND.ARBL.HA.PC', 2000, 2022)
       if nm(a) not in DROP}
assert 'Sudan' not in arb, 'Sudan should fail entity continuity across 2011'
AW = ['Kazakhstan', 'Australia', 'Canada', 'Argentina', 'Russia', 'Ukraine',
      'Niger', 'United States', 'France', 'Brazil', 'Nigeria', 'India',
      'China', 'Japan', 'Kuwait', 'Singapore']
a0 = {k: v[0] for k, v in arb.items()}
a2 = {k: v[1] for k, v in arb.items()}
arows = pairpick(a0, a2, AW, 2, 'arable')
fell = sum(1 for _, x, y in arows if y < x)
assert fell >= 11, fell
P.append(dict(
    family='Change over time', form='Dumbbell · 2000 and 2022', type='dumbbell',
    diff=3, leftYear=2000, rightYear=2022,
    truth='Hectares of cropland for each person, 2000 vs 2022',
    period='2000 → 2022', unit='hectares per inhabitant',
    data=arr(arows, 3, 2),
    answer='Hectares of cropland for each person',
    decoys=[
        'Cubic metres of water used by each person',
        'Square metres of housing for each person',
        'Hectares of forest for each person',
        'Head of cattle for each person',
        'Kilograms of grain harvested for each person',
        'Hectares of protected land for each person',
        'Litres of milk produced for each person'],
    hints=[
        'Kazakhstan leads and Australia is second. Kuwait and Singapore both read 0.00, and almost every country on the chart has less of it now than in 2000.',
        'Two countries read exactly nothing, so this is not something everybody must have some of. Almost everything has moved the same way in twenty two years, and it is the dividing that has changed rather than the thing being divided.',
        'Measured in hectares and divided by the number of inhabitants. Kazakhstan has about one and a half of them each.',
        'Kazakhstan has an enormous grain steppe and only twenty million people to share it between.'],
    why='Kazakhstan leads with about one and a half hectares a head, a little over Australia behind it, because it inherited a vast Soviet grain steppe and has a small population to divide it among. The near universal fall is the giveaway and it is almost entirely the denominator: the world added two billion people between 2000 and 2022 while the area under crops barely moved, so the share each person gets has shrunk nearly everywhere. Niger, which has fallen fastest, has more cropland than in 2000 and more than twice as many people. Kuwait and Singapore round to nothing at all.',
    slug='cropland-per-person', source=WBU('AG.LND.ARBL.HA.PC')[0],
    sourceUrl=WBU('AG.LND.ARBL.HA.PC')[1]))

# ------------------------------------------------- 132 fertiliser (hard)
frt = [(nm(a), b, c) for a, b, c in wb.pair('AG.CON.FERT.ZS', 2002, 2022)
       if nm(a) not in DROP and nm(a) != 'Hong Kong']
assert 'Seychelles' not in [r[0] for r in frt], 'Seychelles has no 2002 figure'
r02 = {a: i + 1 for i, (a, _) in
       enumerate(sorted([(a, b) for a, b, _ in frt], key=lambda x: -x[1]))}
r22 = {a: i + 1 for i, (a, _) in
       enumerate(sorted([(a, c) for a, _, c in frt], key=lambda x: -x[1]))}
FW = ['New Zealand', 'Malaysia', 'Ireland', 'Costa Rica', 'Egypt', 'Vietnam',
      'Colombia', 'China', 'Oman', 'United Arab Emirates', 'South Korea',
      'Netherlands']
frows = sorted([(a, r02[a], r22[a]) for a in FW], key=lambda r: r[2])
assert max(max(r[1], r[2]) for r in frows) <= 22, frows
assert r02['Vietnam'] - r22['Vietnam'] >= 10
P.append(dict(
    family='Ranking', form='Rank slope · 2002 → 2022', type='slope', diff=4,
    truth='World ranking by fertiliser used on each hectare of cropland, 2002 vs 2022',
    period='2002 → 2022', unit='rank by kilograms applied per hectare',
    leftYear=2002, rightYear=2022,
    ranks=arr(frows, 3, 0),
    answer='World ranking by fertiliser used on each hectare of cropland',
    decoys=[
        'World ranking by the amount of farmland',
        'World ranking by the value of food exported',
        'World ranking by the share of workers in farming',
        'World ranking by water used to irrigate crops',
        'World ranking by the number of tractors',
        'World ranking by greenhouse gases from farming',
        'World ranking by the amount of grain harvested'],
    hints=[
        'New Zealand and Malaysia have not moved off first and second in twenty years. The Netherlands has dropped ten places and Vietnam has climbed twelve.',
        'Ireland and New Zealand are at the top with Malaysia and Costa Rica beside them, and India, Brazil, Russia and the United States are nowhere on the board. This is not a ranking by how much anybody grows, and the Dutch fall is a rule being obeyed rather than a market being lost.',
        'A ranking, so the chart carries no units at all. First place puts more than sixteen hundred kilograms on every hectare in a year.',
        'Grass in New Zealand and Ireland, oil palm in Malaysia, and Dutch farmers capped by a European limit on nitrates.'],
    why='This is intensity rather than quantity, which is why the giants are missing: India, Brazil, China and the United States buy far more of it in total, but they spread it over enormous areas. New Zealand and Ireland are at the top because heavily grazed grass is fed almost like a crop; Malaysia and Costa Rica because oil palm, bananas and coffee are grown hard on the same ground year after year. The Dutch fall from eleventh to twenty first is the European Union nitrates directive working. Vietnam climbing twelve places is three rice harvests a year on the same paddy. Kuwait, which would be third in 2022 and seventy seventh in 2002, is left off so the rest of the board stays legible.',
    slug='fertiliser-ranking', source=WBU('AG.CON.FERT.ZS')[0],
    sourceUrl=WBU('AG.CON.FERT.ZS')[1]))

# --------------------------------------------- 133 electricity lost (hard)
los = wbsnap('EG.ELC.LOSS.ZS', 2014)
assert len(los) > 120, len(los)
LOSL = ['Benin', 'Iraq', 'Venezuela', 'Namibia', 'Brazil', 'India',
        'United States', 'Germany', 'Singapore']
names = set(n for n, _ in los)
for n in LOSL:
    assert n in names, n
P.append(dict(
    family='Distribution', form='Beeswarm · every country, 2014', type='beeswarm',
    diff=4,
    truth='Share of electricity lost in transmission, 2014', period='2014',
    unit='% of electricity put into the network', suffix='%',
    data=arr(sorted((n, round(v, 1)) for n, v in los), 4, 1),
    label=LOSL,
    labelSm=['Benin', 'Venezuela', 'India', 'Germany', 'Singapore'],
    answer='Share of electricity lost in transmission',
    decoys=[
        'Share of electricity generated from coal',
        'Share of homes connected to the grid',
        'Share of electricity that is imported',
        'Share of electricity used by industry',
        'Share of electricity generated from oil',
        'Share of electricity used by households',
        'Share of households behind on the electricity bill'],
    hints=[
        'Benin is at seventy eight and Singapore at two. Iraq and Venezuela are up near Benin, and Slovakia and Iceland are down beside Singapore.',
        'Nothing in this swarm reaches a hundred and nothing reaches zero, which rules out a fuel and rules out a connection: countries with no coal sit at zero on one and every European country sits at a hundred on the other. Whatever this counts, everybody has a little of it and nobody has all of it.',
        'Measured as a percentage of everything put into the network in 2014, the last year the World Bank series runs to.',
        'Part of it is heat in the wires. The rest is people connected to the network who are not paying for it.',
    ],
    why='Benin loses 78 per cent of everything put into its network, about one and a half times Iraq behind it, and a figure that large is not physics. Engineers split these losses in two. Technical losses are resistance in long, thin, overloaded lines and run to perhaps six or eight per cent even on a bad grid. Everything above that is non-technical: meters that are broken, bills that are never collected, and households wired straight into the line. That is why the top of the swarm is Benin, Iraq, Congo and Venezuela rather than the largest or the most remote countries, and why Singapore, a small dense grid with a working billing system, is at 2.0.',
    slug='electricity-lost-in-transmission', source=WBU('EG.ELC.LOSS.ZS')[0],
    sourceUrl=WBU('EG.ELC.LOSS.ZS')[1]))

for i, o in enumerate(P):
    o['exhibit'] = ex(122 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
