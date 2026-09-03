#!/usr/bin/env python3
"""Assemble batch three (12 puzzles, indices 74 to 85).

Form mix is deliberately skewed away from dumbbell (19 in the pool) and
lollipop (17), towards symbol (1), line (4), slope (6) and deviation (6).
"""
import wb, eu, sys, json
from common import ex, num, arr, NICE, nm, DROP, block

AGG = ('European Union', 'Euro area', 'EU27', 'EA19', 'EA20', 'European Economic Area')
EUNAME = {'Türkiye': 'Turkey', 'Germany (until 1990 former territory of the FRG)': 'Germany'}
WBU = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)
EUS = lambda c: ('Eurostat', 'https://ec.europa.eu/eurostat/databrowser/view/%s/default/table' % c)


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


def big(code, y, keep=12):
    rows = [(nm(n), v) for n, v in wb.snap(code, y) if nm(n) not in DROP]
    return rows[:keep]


P = []

# ------------------------------------------------------- 74 patents (slope)
a00 = {nm(n): i + 1 for i, (n, v) in enumerate(wb.snap('IP.PAT.RESD', 2000))}
b20 = [(nm(n), i + 1) for i, (n, v) in enumerate(wb.snap('IP.PAT.RESD', 2020))][:11]
miss = [n for n, _ in b20 if n not in a00]
assert not miss, 'patent rank continuity: ' + str(miss)
b20 = [(n, r) for n, r in b20 if a00[n] <= 20]
assert len(b20) >= 9, b20
P.append(dict(
    family='Ranking', form='Rank slope · 2000 → 2020', type='slope', diff=3,
    truth='World ranking by patents applied for at home, 2000 vs 2020',
    period='2000 → 2020', unit='rank by applications filed by residents',
    leftYear=2000, rightYear=2020,
    ranks=arr([(n, a00[n], r) for n, r in b20], 3, 0),
    answer='World ranking by patents applied for at home',
    decoys=[
        'World ranking by spending on research',
        'World ranking by the number of scientists',
        'World ranking by the number of university students',
        'World ranking by exports of electronics',
        'World ranking by the number of engineers trained each year',
        'World ranking by spending on higher education',
        'World ranking by the number of new companies registered'],
    hints=[
        'India climbs eleven places. Japan falls from first to third without changing anything at all about the way it files.',
        'Russia sixth and India seventh, both above France and the United Kingdom, is not the order of research budgets or of university systems. Nor is the country that climbed from fifth to first and now files five times as many as the one behind it.',
        'A ranking, so the chart carries no units. First place lodged about 1.3 million of them in 2020.',
        'It counts the forms filed at a national office by people trying to stop somebody else copying their invention.'],
    why='China moved from fifth to first and now files roughly five times as many as the United States, which is more than any measure of research spending or scientific output would show. Filings at a home office are cheap and are counted whether or not anything is granted, so the ranking reflects domestic filing habits and state targets as much as invention. Russia sixth and India seventh, above France and the United Kingdom, is the giveaway that this is not a money ranking.',
    slug='IP.PAT.RESD', source=WBU('IP.PAT.RESD')[0], sourceUrl=WBU('IP.PAT.RESD')[1]))

# ---------------------------------------------------------- 75 aid received
aid = big('DC.DAC.TOTL.CD', 2023)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=3,
    truth='Foreign aid received, 2023', period='2023', unit='US dollars a year',
    data=arr([(n, int(v)) for n, v in aid], 3, 0),
    answer='Foreign aid received',
    decoys=[
        'Money borrowed from the International Monetary Fund',
        'Money sent home by workers abroad',
        'Foreign investment arriving each year',
        'Money spent on food imports',
        'Debt owed to foreign governments',
        'Money spent by visitors from abroad',
        'Value of goods exported'],
    hints=[
        'One circle is nearly ten times the size of the next, and the year is 2023.',
        'Ukraine is the largest by a distance, with Syria, Afghanistan, Jordan and Yemen all present. Every one of them either has a war or borders one, which is not how money that follows opportunity behaves.',
        'Counted in US dollars in a single year. The largest circle is 38.7 billion and the smallest here is under two.',
        'It is what donor governments hand over, and in 2023 one recipient took more than the next nine put together.'],
    why='Ukraine received 38.7 billion dollars in 2023, roughly ten times India in second place, because Western governments were funding a state at war. That concentration is the tell: investment, remittances and exports all follow population and opportunity, so India, Mexico and China would lead them and no single country would take a tenth of the total, let alone half.',
    slug='DC.DAC.TOTL.CD', source=WBU('DC.DAC.TOTL.CD')[0], sourceUrl=WBU('DC.DAC.TOTL.CD')[1]))

# -------------------------------------------------------------- 76 fish
fish = big('ER.FSH.CAPT.MT', 2021)
P.append(dict(
    family='Magnitude', form='Proportional symbols · the twelve largest',
    type='symbol', diff=3,
    truth='Fish caught at sea, 2021', period='2021', unit='tonnes landed a year',
    data=arr([(n, int(v)) for n, v in fish], 3, 0),
    answer='Fish caught at sea',
    decoys=[
        'Fish farmed rather than caught',
        'Tonnes of shipping built',
        'Salt produced from seawater',
        'Seaweed harvested',
        'Tonnes of grain exported by sea',
        'Whales taken each year',
        'Sand dredged from the seabed'],
    hints=[
        'Peru is third here, ahead of Russia, India and the United States, and it is not a big country by any other measure.',
        'Peru third and Norway ninth is a coastline ranking, not a population one. Both sit on a cold current where the water rises from the deep, and neither farms what is being counted.',
        'Counted in tonnes landed in a year. The largest is 13.1 million tonnes and Peru alone is 6.6 million.',
        'Peru is third because of the anchoveta, a small oily fish that mostly ends up as feed for farmed salmon and for chickens.'],
    why='China leads at 13.1 million tonnes, but Peru at third is what settles it: the Humboldt Current lifts cold nutrient-rich water up the Peruvian coast and supports the largest single-species fishery on earth. Farmed fish would put Indonesia, India and Vietnam far higher and Peru nowhere, because almost nothing Peru lands is farmed.',
    slug='ER.FSH.CAPT.MT', source=WBU('ER.FSH.CAPT.MT')[0], sourceUrl=WBU('ER.FSH.CAPT.MT')[1]))

# ------------------------------------------------------ 77 remittances sent
sent = big('BM.TRF.PWKR.CD.DT', 2023)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=3,
    truth='Money sent abroad by workers, 2023', period='2023',
    unit='US dollars a year', total=sum(int(v) for _, v in sent),
    data=arr([(n, int(v)) for n, v in sent], 3, 0),
    answer='Money sent abroad by workers',
    decoys=[
        'Foreign aid given',
        'Money spent by tourists abroad',
        'Money invested in other countries',
        'Value of goods imported',
        'Money spent on foreign students',
        'Money paid in interest to foreign lenders',
        'Money spent on imported oil'],
    hints=[
        'Luxembourg has a block here, and it is a bigger one than China\u2019s.',
        'The United Arab Emirates is second and Saudi Arabia third, both ahead of Germany and France. Luxembourg, with 700,000 residents, is seventh. What these four have in common is who works there rather than what they buy.',
        'Counted in US dollars in a single year. The largest block is 98 billion and Luxembourg\u2019s is 18.',
        'It is the mirror of a chart you may have already seen: the money leaving, rather than the money arriving.'],
    why='The United States sends out 98 billion dollars a year, nearly twice the United Arab Emirates behind it, simply because it hosts more foreign-born workers than any other country: the same 52 million people who make it the largest block on the migrant chart. Luxembourg seventh is the other discriminator. Nearly half the people working there commute in from Belgium, France and Germany and are paid into accounts abroad, so a country of 700,000 sends out more than China does. Aid, imports and investment would all follow the size of the economy and put Luxembourg nowhere near this list.',
    slug='BM.TRF.PWKR.CD.DT', source=WBU('BM.TRF.PWKR.CD.DT')[0],
    sourceUrl=WBU('BM.TRF.PWKR.CD.DT')[1]))

# ------------------------------------------------ 78 life expectancy, covid
le = {nm(n): (x, y) for n, x, y in wb.pair('SP.DYN.LE00.IN', 2019, 2021)}
LEW = ['Australia', 'South Korea', 'Norway', 'Japan', 'China', 'Germany', 'France',
       'United Kingdom', 'Italy', 'Spain', 'Brazil', 'India', 'Russia',
       'United States', 'Peru', 'Mexico']
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=3,
    truth='Change in life expectancy between 2019 and 2021', period='2019 → 2021',
    unit='change in years of life expectancy',
    data=arr([(c, round(le[c][1] - le[c][0], 1)) for c in LEW if c in le], 3, 1),
    answer='Change in life expectancy between 2019 and 2021',
    decoys=[
        'Change in the average age of the population',
        'Change in the average number of years spent in education',
        'Change in the average age at retirement',
        'Change in the average number of children per woman',
        'Change in the average age of mothers at first birth',
        'Change in the number of years lived after 65',
        'Change in the average length of the working week'],
    hints=[
        'Almost everything on this chart points the wrong way, and the two years being compared are 2019 and 2021.',
        'Australia, South Korea, Norway and Japan are the only ones on the positive side, and Mexico and Peru are the worst by a distance. The countries that closed their borders hardest are the ones that gained.',
        'Measured as a change in years, against a line at zero. The largest fall is nearly five years and the largest rise under half a year.',
        'Two years is far too short for any of this to be demography. It was a pandemic.'],
    why='Mexico falls by 4.8 years and Peru by 4.7, the largest peacetime falls recorded anywhere, while Australia, Japan, South Korea and Norway all rose because closed borders and low transmission also cut flu deaths and road deaths. Nothing about education, retirement or fertility moves several years in twenty-four months, which is what rules the whole decoy set out on scale alone.',
    slug='SP.DYN.LE00.IN-change', source=WBU('SP.DYN.LE00.IN')[0], sourceUrl=WBU('SP.DYN.LE00.IN')[1]))

# ------------------------------------------------------- 79 current account
ca = {nm(n): v for n, v in wb.snap('BN.CAB.XOKA.GD.ZS', 2023)}
CAW = ['Norway', 'Singapore', 'Netherlands', 'Switzerland', 'Germany', 'Japan',
       'Russia', 'South Korea', 'China', 'Italy', 'India', 'France', 'Brazil',
       'United States', 'United Kingdom', 'Turkey', 'Romania']
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=4,
    truth='Current account balance as a share of the economy, 2023',
    period='2023', unit='% of GDP', suffix='%',
    data=arr([(c, round(ca[c], 1)) for c in CAW if c in ca], 3, 1),
    answer='Current account balance as a share of the economy',
    decoys=[
        'Government budget surplus or deficit, as a share of the economy',
        'Change in the size of the economy over the year',
        'Inflation above or below the central bank target',
        'Change in the value of the currency over the year',
        'Net migration as a share of the population',
        'Change in house prices over the year',
        'Government spending above or below its income from tax'],
    hints=[
        'Norway and Singapore are at one end. The United States and the United Kingdom are near the other, alongside Turkey and Romania.',
        'Germany, the Netherlands and Japan are all comfortably positive while the United States and the United Kingdom are negative. This has run in the same direction for those six countries for two decades, which no annual growth or price figure does.',
        'Measured as a percentage of everything the country produces, against a line at zero. The range runs from plus 17 to minus 7.',
        'It is the difference between what a country earns from the rest of the world and what it pays out to it.'],
    why='The same countries sit on the same side of this line year after year: Norway from oil, Singapore and the Netherlands from trade, Germany and Japan from manufacturing, against the deficit countries that consume more than they sell. A budget balance would look nothing like it, since Norway runs a large government surplus and Japan a very large deficit, yet both are positive here.',
    slug='BN.CAB.XOKA.GD.ZS', source=WBU('BN.CAB.XOKA.GD.ZS')[0],
    sourceUrl=WBU('BN.CAB.XOKA.GD.ZS')[1]))

# ------------------------------------------------- 80 European population
a13 = eu_slice('demo_pjan', 2013, sex='T', age='TOTAL')
b24 = eu_slice('demo_pjan', 2024, sex='T', age='TOTAL')
POPW = ['Malta', 'Luxembourg', 'Ireland', 'Cyprus', 'Sweden', 'Norway', 'Turkey',
        'Belgium', 'Austria', 'Spain', 'France', 'Netherlands', 'Germany',
        'Italy', 'Poland', 'Portugal', 'Greece', 'Romania', 'Lithuania',
        'Latvia', 'Croatia', 'Bulgaria']
rows = sorted([(c, round(100 * (b24[c] - a13[c]) / a13[c], 1))
               for c in POPW if c in a13 and c in b24],
              key=lambda r: -r[1])
assert len(rows) >= 18, rows
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=3,
    truth='Change in population between 2013 and 2024', period='2013 → 2024',
    unit='% change in population', suffix='%',
    data=arr(rows, 3, 1),
    answer='Change in population between 2013 and 2024',
    decoys=[
        'Change in the number of people in work',
        'Change in the number of births each year',
        'Change in the number of people aged over 65',
        'Change in average income',
        'Change in the number of households',
        'Change in the number of people living in cities',
        'Change in the number of school-age children'],
    hints=[
        'Malta is at one end and Bulgaria, Croatia and Latvia are at the other. The eleven years span the opening of several labour markets.',
        'Malta and Luxembourg are the two smallest countries on the chart and the two largest risers, while the Baltic and Balkan states all fall. The people leaving one end of this chart are arriving at the other.',
        'Measured as a percentage change over eleven years, against a line at zero. The largest rise is over 30 per cent and the largest fall over 10.',
        'Free movement inside the European Union moved several million people west and south, and the countries they left are the negative bars.'],
    why='Malta grew by a third and Luxembourg by a quarter, almost entirely through arrivals rather than births, while Bulgaria, Croatia and Latvia lost a tenth of their people to emigration. Births fell almost everywhere over this period, including in Malta and Ireland, so a chart with large positive bars cannot be counting them: this is migration inside a single free-movement area.',
    slug='demo_pjan', source=EUS('demo_pjan')[0], sourceUrl=EUS('demo_pjan')[1]))

# ---------------------------------------------------------- 81 renewables
s = wb.series('EG.ELC.RNEW.ZS', [2000, 2020])
RSER = [('Denmark', 'DNK'), ('United Kingdom', 'GBR'), ('Germany', 'DEU'),
        ('France', 'FRA'), ('United States', 'USA')]
for lab, iso in RSER:
    m = [y for y in range(2000, 2021) if y not in s[iso]]
    assert not m, (lab, m)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2020', type='line', diff=3,
    truth='Share of electricity generated from renewable sources, 2000 to 2020',
    period='2000–2020', unit='% of electricity generated', suffix='%', startYear=2000,
    series=[(lab, [s[iso][y] for y in range(2000, 2021)]) for lab, iso in RSER],
    answer='Share of electricity generated from renewable sources',
    decoys=[
        'Share of electricity generated from coal',
        'Share of electricity generated from nuclear power',
        'Share of homes with solar panels',
        'Share of electricity that is imported',
        'Share of electricity used by industry',
        'Share of energy used for heating',
        'Share of electricity lost in transmission'],
    hints=[
        'One line quintuples and finishes at nearly 80. Another sits almost flat in the low twenties for two decades, and it belongs to the country with the most nuclear power in Europe.',
        'Every line rises and none of them falls, which rules out anything being replaced. France is the flattest and lowest riser of the six, which is exactly wrong for the low-carbon reading you might reach for first.',
        'Measured as a percentage of all electricity generated in a year. Denmark ends near 80 and the United States near 20.',
        'Denmark is the line at the top, and the reason is standing in the North Sea with three blades on it.'],
    why='France flat near 20 is what separates this from any low-carbon measure: France generates about 70 per cent of its electricity from nuclear, which is not renewable and so does not count here. Denmark rising from 15 to nearly 80 on wind, and the United Kingdom from 3 to 40, are the two fastest grid transitions in the world over this period.',
    slug='EG.ELC.RNEW.ZS', source=WBU('EG.ELC.RNEW.ZS')[0], sourceUrl=WBU('EG.ELC.RNEW.ZS')[1]))

# ------------------------------------------- 82 births outside marriage
d, ids = eu.eurostat('demo_find')
gi, ti, ii = ids.index('geo'), ids.index('time'), ids.index('indic_de')
nmar = {}
for k, v in d.items():
    if k[ii][0] == 'NMARPCT':
        nmar.setdefault(EUNAME.get(k[gi][1], k[gi][1]), {})[int(k[ti][0])] = v
BSER = ['France', 'Sweden', 'Spain', 'Italy', 'Greece']
# Sweden is missing 2021, and Sweden holding flat above 54 is the whole point of
# the chart, so the window stops at 2020 rather than the series being dropped.
Y0, Y1 = 2000, 2020
for c in BSER:
    m = [y for y in range(Y0, Y1 + 1) if y not in nmar.get(c, {})]
    assert not m, (c, m)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2020', type='line', diff=4,
    truth='Share of babies born to parents who are not married, 2000 to 2020',
    period='2000–2020', unit='% of live births', suffix='%', startYear=2000,
    series=[(c, [round(nmar[c][y], 1) for y in range(Y0, Y1 + 1)]) for c in BSER],
    answer='Share of babies born to parents who are not married',
    decoys=[
        'Share of adults who live alone',
        'Share of households with only one parent',
        'Share of marriages that end in divorce',
        'Share of couples who live together before marrying',
        'Share of women who have no children by forty',
        'Share of adults who describe themselves as religious',
        'Share of births in a hospital rather than at home'],
    hints=[
        'One line begins the century above 55 and is still there in 2023, having barely moved. Every other line climbs towards it.',
        'Sweden starts high and stays flat while Greece starts at 4 and Spain at 18. Whatever this is, the north reached its ceiling before 2000 and the Catholic south spent twenty years catching up.',
        'Measured as a percentage of live births in a year. France passes 60 before the end, which means most of them.',
        'It is the share of babies whose parents had not been to a registry office or a church first.'],
    why='Sweden flat above 54 for the whole period while Greece climbs from 4 to about 12 and Spain from 18 to 47 is a convergence story, not a social breakdown one: cohabiting parents in Sweden had already become normal by the 1990s, so there was nothing left to change. France passing 60 means an outright majority of French children are now born to unmarried parents, which is what makes the ceiling on this chart so much higher than any divorce or lone-parent measure could reach.',
    slug='demo_find-NMARPCT', source=EUS('demo_find')[0], sourceUrl=EUS('demo_find')[1]))

# -------------------------------------------------- 83 living with parents
lwp = eu_slice('ilc_lvps08', 2024, age='Y25-29', sex='T', unit='PC')
lwp = sorted((k, round(v, 1)) for k, v in lwp.items())
assert len(lwp) >= 25, len(lwp)
P.append(dict(
    family='Distribution', form='Beeswarm · every country reporting, 2024',
    type='beeswarm', diff=3,
    truth='Share of 25 to 29 year olds still living with their parents, 2024',
    period='2024', unit='% of 25 to 29 year olds', suffix='%',
    data=arr(lwp, 4, 1),
    label=['Croatia', 'Greece', 'Italy', 'Spain', 'Poland', 'Germany', 'France',
           'Sweden', 'Denmark'],
    labelSm=['Croatia', 'Italy', 'Germany', 'Sweden', 'Denmark'],
    answer='Share of 25 to 29 year olds still living with their parents',
    decoys=[
        'Share of 25 to 29 year olds who are unmarried',
        'Share of 25 to 29 year olds who rent rather than own',
        'Share of 25 to 29 year olds still in education',
        'Share of 25 to 29 year olds without a full-time job',
        'Share of 25 to 29 year olds with no children',
        'Share of 25 to 29 year olds who have never left their home region',
        'Share of 25 to 29 year olds living in a city'],
    hints=[
        'Denmark is at the far left at four in a hundred. Croatia is at the far right at nearly eight in ten.',
        'The swarm splits cleanly north from south: the Nordic countries are all under 13 and the Mediterranean and Balkan countries all above 65. A twentyfold gap between Denmark and Croatia is too wide for anything about jobs or study, which vary by a factor of two or three at most.',
        'Measured as a percentage of one five year age band. The two ends are 4.3 and 78.6.',
        'In Denmark students get a state grant and move out at eighteen. In Croatia and Italy they stay in the family flat until they marry.'],
    why='A range from 4 to 79 per cent is the tell: employment, study and renting all vary far less than that across Europe. The clean north-south split is the signature of housing costs and state student support, not of anything individual, and Denmark at the bottom is the country that pays its students to live independently.',
    slug='ilc_lvps08', source=EUS('ilc_lvps08')[0], sourceUrl=EUS('ilc_lvps08')[1]))

# ------------------------------------------------------- 84 meeting friends
mf = eu_slice('ilc_scp09', 2022, sex='T', age='Y_GE16', isced11='TOTAL',
              frequenc='WEEK', unit='PC')
mf = sorted(((k, round(v, 1)) for k, v in mf.items() if v > 0), key=lambda x: -x[1])[:14]
assert len(mf) == 14, len(mf)
P.append(dict(
    family='Ranking', form='Lollipop · the fourteen highest, 2022',
    type='lollipop', diff=4,
    truth='Share of adults who meet friends or family at least weekly, 2022',
    period='2022', unit='% of adults aged 16 and over', suffix='%',
    data=arr(mf, 3, 1),
    answer='Share of adults who meet friends or family at least weekly',
    decoys=[
        'Share of adults who take part in a sport at least weekly',
        'Share of adults who attend a religious service at least monthly',
        'Share of adults who volunteer at least once a year',
        'Share of adults who eat out at least weekly',
        'Share of adults who speak to a neighbour most days',
        'Share of adults who belong to a club or society',
        'Share of adults who telephone a relative most days'],
    hints=[
        'Cyprus is first and Norway is second, which is not a pairing you would expect from anything cultural.',
        'The top of this list mixes Cyprus and Malta with Norway, Switzerland and the Netherlands, and none of them clears 50 per cent. A ceiling that low rules out anything most people do as a matter of routine.',
        'Measured as a percentage of everyone aged 16 and over, from the same European survey that asks about trust. Nothing on the chart reaches 51.',
        'The survey asks how often you get together with friends or relatives, and even at the top only half of adults manage it every week.'],
    why='The ceiling is the evidence. Nobody clears 51 per cent, which is far too low for eating out or speaking to a relative and far too high for volunteering or club membership. Cyprus and Malta at the top alongside Norway and Switzerland also rules out any north-south cultural reading, which is what makes this one hard.',
    slug='ilc_scp09', source=EUS('ilc_scp09')[0], sourceUrl=EUS('ilc_scp09')[1]))

# ------------------------------------------------------------- 85 scientists
pap = big('IP.JRN.ARTC.SC', 2020)
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=2,
    truth='Scientific papers published, 2020', period='2020',
    unit='journal articles a year', total=sum(int(v) for _, v in pap),
    data=arr([(n, int(v)) for n, v in pap], 3, 0),
    answer='Scientific papers published',
    decoys=[
        'Patents granted',
        'University students enrolled',
        'Money spent on research',
        'Books published',
        'Doctorates awarded',
        'Prizes won in international science competitions',
        'Laboratories in operation'],
    hints=[
        'The United Kingdom and Italy both have larger blocks than South Korea, and Russia has a larger one than Brazil.',
        'The United Kingdom is fifth with 67 million people, ahead of Japan and well ahead of South Korea. English is doing some of the work here, because what is counted has to be published in a journal that indexes it.',
        'Counted as articles in indexed journals in one year. The largest block is 672,000 and the smallest here is about 50,000.',
        'They are papers, not products: the currency is publication rather than anything anyone can sell.'],
    why='The United Kingdom fifth and Italy eighth, both ahead of South Korea, is what separates this from patents or research spending, where Korea and Japan sit far higher and Britain and Italy far lower. Publication counts reward volume in English-language indexed journals, so countries with old universities and English as a working language do better here than their research budgets alone would predict.',
    slug='IP.JRN.ARTC.SC', source=WBU('IP.JRN.ARTC.SC')[0], sourceUrl=WBU('IP.JRN.ARTC.SC')[1]))

for i, o in enumerate(P):
    o['exhibit'] = ex(74 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
