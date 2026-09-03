#!/usr/bin/env python3
"""Assemble batch two (12 puzzles, indices 62 to 73).

Source mix per doc 25: Eurostat 4, OECD 1, WHO 1, World Bank 6. No OWID.
"""
import wb, eu, json, csv, subprocess, sys
from common import ex, num, arr, NICE, nm, DROP, block

AGG = ('European Union', 'Euro area', 'EU27', 'EA19', 'EA20', 'European Economic Area')
EUNAME = {'Türkiye': 'Turkey', 'Czechia': 'Czechia',
          'Germany (until 1990 former territory of the FRG)': 'Germany',
          'Kosovo*': 'Kosovo', 'North Macedonia': 'North Macedonia'}


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
        name = EUNAME.get(key[gi][1], key[gi][1])
        if any(s in name for s in AGG):
            continue
        out[name] = v
    return out


def eu_pair(code, y1, y2, want, dec=1, **pins):
    a, b = eu_slice(code, y1, **pins), eu_slice(code, y2, **pins)
    miss = [c for c in want if c not in a or c not in b]
    if miss:
        sys.exit('%s missing in one year: %s' % (code, miss))
    rows = [(c, round(a[c], dec), round(b[c], dec)) for c in want]
    rows.sort(key=lambda r: r[2])
    return rows


P = []
EUS = ('Eurostat', 'https://ec.europa.eu/eurostat/databrowser/view/%s/default/table')
WBU = lambda c: ('World Bank', 'https://data.worldbank.org/indicator/' + c)

# ------------------------------------------------ 62 no week away from home
P.append(dict(
    family='Change over time', form='Dumbbell · 2007 → 2024', type='dumbbell', diff=3,
    truth='Share of people who cannot afford a week away from home, 2007 vs 2024',
    period='2007 → 2024', unit='% of the population', suffix='%',
    leftYear=2007, rightYear=2024,
    data=arr(eu_pair('ilc_mdes02', 2007, 2024, [
        'Romania', 'Bulgaria', 'Hungary', 'Greece', 'Poland', 'Portugal', 'Latvia',
        'Italy', 'Spain', 'Ireland', 'France', 'Germany', 'Sweden', 'Norway'],
        1, hhcomp='TOTAL', rskpovth='TOTAL'), 3, 1),
    answer='Share of people who cannot afford a week away from home',
    decoys=[
        'Share of people living below the poverty line',
        'Share of people behind on a utility bill',
        'Share of people who cannot afford to heat their home',
        'Share of people renting rather than owning',
        'Share of people with no savings at all',
        'Share of people who have never flown',
        'Share of people without a passport'],
    hints=[
        'Almost every line has moved left since 2007. Norway is the exception, and it has gone the other way.',
        'Bulgaria has halved, from four in five to two in five, in seventeen years. Sweden and Norway sit under 12 in both years, which is too high a floor for real destitution and too low for anything most people simply choose not to do.',
        'Measured as a percentage of the whole population, from a survey that asks whether a household could meet the cost, not whether it went.',
        'The question is whether a household could pay for seven nights somewhere else, once a year.'],
    why='This is an affordability question, not a poverty count: Sweden and Norway never fall below about 9 per cent, and no rich country has that share in real poverty. Bulgaria and Romania halving between 2007 and 2024 is the shape of Eastern Europe getting richer rather than of any policy aimed at holidays.',
    slug='ilc_mdes02', source=EUS[0], sourceUrl=EUS[1] % 'ilc_mdes02'))

# ---------------------------------------------- 63 age at first marriage
P.append(dict(
    family='Change over time', form='Dumbbell · 1990 → 2023', type='dumbbell', diff=3,
    truth='Average age of women at their first marriage, 1990 vs 2023',
    period='1990 → 2023', unit='years of age',
    leftYear=1990, rightYear=2023,
    data=arr(eu_pair('demo_nind', 1990, 2023, [
        'Spain', 'Sweden', 'Italy', 'Luxembourg', 'Belgium', 'Austria', 'Finland',
        'Greece', 'Switzerland', 'Slovenia', 'Czechia', 'Hungary', 'Bulgaria',
        'Romania'], 1, indic_de='FAGEMAR1'), 3, 1),
    answer='Average age of women at their first marriage',
    decoys=[
        'Average age of women when their youngest child leaves school',
        'Average age at which women leave their parents\u2019 home',
        'Average age at which women finish full-time education',
        'Average age of women at retirement',
        'Average age at which women buy their first home',
        'Average age of women when they first vote',
        'Average age of women at their first full-time job'],
    hints=[
        'Every country on this chart has moved right, and none by less than four years. Spain has moved by nine.',
        'The whole list now sits between 28 and 35, and in 1990 it sat between 21 and 28. Nothing to do with school or with retirement moves through that particular window.',
        'Measured in years of age. The earliest figure on the chart is 21.5 and the latest is 34.9.',
        'It is the age at which a woman first signs the register.'],
    why='The window is the giveaway. Leaving home and finishing education both happen well before 25 in this group of countries, and retirement well after 55. Only two events sit in the late twenties and early thirties and move together, and the first birth in Southern Europe now comes after this figure rather than before it.',
    slug='demo_nind', source=EUS[0], sourceUrl=EUS[1] % 'demo_nind'))

# ------------------------------------------------------- 64 trust in others
tr = eu_slice('ilc_pw03', 2022, sex='T', isced11='TOTAL', age='Y_GE16',
              statinfo='AVG', unit='RTG', domain='OTH')
trs = sorted(tr.items())
P.append(dict(
    family='Distribution', form='Beeswarm · every country reporting, 2022',
    type='beeswarm', diff=4,
    truth='How much people say they trust others, on a scale of 0 to 10, 2022',
    period='2022', unit='average rating from 0 to 10',
    data=arr(trs, 4, 2),
    label=['Romania', 'Finland', 'Ireland', 'Netherlands', 'Germany', 'Italy',
           'France', 'Cyprus', 'Turkey'],
    labelSm=['Romania', 'Finland', 'Germany', 'France', 'Turkey'],
    answer='How much people say they trust others, on a scale of 0 to 10',
    decoys=[
        'How satisfied people say they are with their lives, from 0 to 10',
        'How satisfied people say they are with their government, from 0 to 10',
        'How satisfied people say they are with their home, from 0 to 10',
        'How safe people say they feel walking alone at night, from 0 to 10',
        'How satisfied people say they are with their job, from 0 to 10',
        'How satisfied people say they are with their commute, from 0 to 10',
        'How healthy people say they feel, from 0 to 10'],
    hints=[
        'Romania is at the right-hand end of this swarm, ahead of Finland and the Netherlands. France is down at the other end, below Slovenia.',
        'The order does not follow income at all: Romania and Poland are at the top, France near the bottom. Every satisfaction measure in this survey runs with national income, and this one plainly does not.',
        'An average rating on a scale of 0 to 10, from the same European survey that asks about life satisfaction. The range here is only 3.4 to 7.1.',
        'The question asks whether most people can be relied on, or whether you cannot be too careful.'],
    why='Every wellbeing rating in this survey correlates strongly with income, which is why Romania first and France near last rules them all out. This one measures a belief about other people rather than about your own circumstances, and it tracks culture rather than money.',
    slug='ilc_pw03', source=EUS[0], sourceUrl=EUS[1] % 'ilc_pw03'))

# ------------------------------------------------- 65 sugary drinks (funny)
sd = eu_slice('hlth_ehis_fv7e', 2019, frequenc='GE1D', sex='T', age='TOTAL',
              isced11='TOTAL', unit='PC')
sdr = sorted(sd.items(), key=lambda x: -x[1])[:12]
P.append(dict(
    # Rendered as circles first and it read wrong: 20.4 against 9.0 is only a
    # 2.3x area difference, so every symbol looked much the same. Proportional
    # symbols are for "one of these dwarfs the others"; a close ranking is a
    # lollipop.
    family='Ranking', form='Lollipop · the twelve highest, 2019',
    type='lollipop', diff=4,
    truth='Share of adults who drink a sugary soft drink every day, 2019',
    period='2019', unit='% of adults', suffix='%',
    data=arr(sdr, 3, 1),
    answer='Share of adults who drink a sugary soft drink every day',
    decoys=[
        'Share of adults who eat no fruit or vegetables on a normal day',
        'Share of adults who drink alcohol every day',
        'Share of adults who smoke every day',
        'Share of adults who take no exercise in a normal week',
        'Share of adults who eat a takeaway every week',
        'Share of adults who drink coffee more than four times a day',
        'Share of adults who skip breakfast'],
    hints=[
        'Belgium is at the top of this list by a clear margin, more than half as far again as the country behind it.',
        'Portugal, Spain, Italy and Greece are all absent from this list, and Germany, Hungary and Poland are all on it. Whatever is being counted, the Mediterranean does less of it than the north and the east.',
        'Measured as a percentage of adults doing this on a daily basis. The highest figure is 20.4 per cent and the lowest on the chart is 9.',
        'It is fizzy, it is sweetened, and Belgium gets through more of it than anywhere else in Europe.'],
    why='Belgium at 20.4 per cent is not a young person\u2019s habit that drags the average up: it leads every single age band in the survey, and Belgians aged 65 to 74 report a higher daily rate (11.8 per cent) than Italians aged 15 to 24 (9.5 per cent). As for the ordering, daily alcohol would put Portugal and Spain at the very top and daily smoking would put Greece and Bulgaria there. Both are absent or low, and a northern and eastern list with the wine-growing south missing is the signature of sweetened soft drinks.',
    slug='hlth_ehis_fv7e', source=EUS[0], sourceUrl=EUS[1] % 'hlth_ehis_fv7e'))

# ----------------------------------------------------------- 66 dentists
cn = {c['Code']: c['Title'] for c in json.load(open('who_countries.json'))['value']}
raw = subprocess.run(['curl', '-s', '-m', '60', 'https://ghoapi.azureedge.net/api/HWF_0010'],
                     capture_output=True, text=True).stdout
DEN_NAME = {'United States of America': 'United States',
            'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
            'Russian Federation': 'Russia', 'Republic of Korea': 'South Korea',
            'Iran (Islamic Republic of)': 'Iran', 'Viet Nam': 'Vietnam',
            'Republic of Moldova': 'Moldova', 'United Republic of Tanzania': 'Tanzania',
            'Bolivia (Plurinational State of)': 'Bolivia', 'Türkiye': 'Turkey',
            'Venezuela (Bolivarian Republic of)': 'Venezuela',
            'Democratic Republic of the Congo': 'Democratic Republic of Congo',
            "Côte d’Ivoire": "Côte d'Ivoire", 'Czechia': 'Czechia',
            "Democratic People's Republic of Korea": 'North Korea',
            'Syrian Arab Republic': 'Syria', 'Netherlands (Kingdom of the)': 'Netherlands'}
den = []
for r in json.loads(raw)['value']:
    if r.get('SpatialDimType') != 'COUNTRY' or r.get('TimeDim') != 2018:
        continue
    if r.get('NumericValue') is None:
        continue
    n = cn.get(r['SpatialDim'], r['SpatialDim'])
    n = DEN_NAME.get(n, n)
    if n in DROP:
        continue
    den.append((n, round(r['NumericValue'], 2)))
den = sorted(set(den))
P.append(dict(
    family='Distribution', form='Beeswarm · every country reporting, 2018',
    type='beeswarm', diff=3,
    truth='Dentists per 10,000 people, 2018', period='2018',
    unit='dentists per 10,000 people',
    data=arr(den, 4, 2),
    label=['Cuba', 'Greece', 'Brazil', 'Germany', 'United States', 'United Kingdom',
           'India', 'Nigeria', 'Niger'],
    labelSm=['Cuba', 'Germany', 'United States', 'India', 'Niger'],
    answer='Practising dentists per 10,000 people',
    decoys=[
        'Vets per 10,000 people',
        'Pharmacists per 10,000 people',
        'Midwives per 10,000 people',
        'Opticians per 10,000 people',
        'Physiotherapists per 10,000 people',
        'Psychiatrists per 100,000 people',
        'Hospitals per million people'],
    hints=[
        'Greece is fourth and the United Kingdom is nowhere near the front. Several countries at the left-hand end report a figure of 0.01.',
        'Cuba and Chile are near the top while Germany and the United States sit in the middle of the pack. The very bottom of the swarm is a hundredth of one per ten thousand, which is a profession that some countries effectively do without.',
        'Counted per 10,000 of the population. The leader is at 17.4 and the last five countries are at 0.01.',
        'Greece has roughly one for every 800 people, which is more than any other country in Europe.'],
    why='A tail at 0.01 per 10,000 is the tell: an entire country with a handful of practitioners. Midwives and pharmacists never fall that far because both are essential to basic care, and the World Health Organization records them in the hundreds even in the poorest countries. This is a profession the poorest countries go without almost entirely.',
    slug='HWF_0010', source='WHO Global Health Observatory',
    sourceUrl='https://www.who.int/data/gho/data/indicators'))

# ------------------------------------------------------- 67 unpaid work
rows = list(csv.DictReader(open('tu.csv')))
OE = {'Korea': 'South Korea', 'China (People\u2019s Republic of)': 'China',
      'T\u00fcrkiye': 'Turkey'}
up = sorted([(OE.get(x['Reference area'], x['Reference area']), round(float(x['OBS_VALUE'])))
             for x in rows if x['Measure'] == 'Unpaid work' and x['Sex'] == 'Total'],
            key=lambda k: -k[1])
KEEP = ['Mexico', 'Poland', 'Australia', 'Hungary', 'Italy', 'Spain', 'Germany',
        'United Kingdom', 'France', 'United States', 'Netherlands', 'Norway',
        'China', 'South Korea', 'Japan']
upk = [r for r in up if r[0] in KEEP]
P.append(dict(
    family='Ranking', form='Lollipop · ranked, 2024', type='lollipop', diff=3,
    truth='Minutes a day spent on unpaid work, 2024', period='2024',
    unit='minutes per day',
    data=arr(upk, 3, 0),
    answer='Minutes a day spent on unpaid work',
    decoys=[
        'Minutes a day spent watching television',
        'Minutes a day spent eating and drinking',
        'Minutes a day spent travelling to and from work',
        'Minutes a day spent on paid work',
        'Minutes a day spent asleep in the afternoon',
        'Minutes a day spent on the phone',
        'Minutes a day spent shopping'],
    hints=[
        'Japan and South Korea are at the bottom of this list, and Mexico is at the top by some distance.',
        'The whole list sits between two and four and a half hours a day, every day, averaged across everyone including those who do none of it. Paid work would be far higher and commuting far lower.',
        'Measured in minutes per day, from national time-use diaries. The range runs from 125 to 256.',
        'It is cooking, cleaning, laundry, childcare and the shopping that goes with them, and nobody is paid for any of it.'],
    why='Two to four hours a day is too much for eating, television or travel and far too little for paid work, which rules out the whole set by scale alone. Mexico at the top and Japan and Korea at the bottom also matches nothing about wealth: it tracks how much household work is done at home rather than bought in.',
    slug='DSD_TIME_USE', source='OECD',
    sourceUrl='https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_TIME_USE%40DF_TIME_USE'))

# ------------------------------------------------- 68 military spending treemap
ms = [(nm(n), int(v)) for n, v in wb.snap('MS.MIL.XPND.CD', 2023) if nm(n) not in DROP]
mst = sorted(ms[:12], key=lambda r: -r[1])
P.append(dict(
    family='Part-to-whole', form='Treemap · the twelve largest', type='treemap', diff=3,
    truth='Money spent on the armed forces, 2023', period='2023',
    unit='US dollars a year', total=sum(v for _, v in mst),
    data=arr(mst, 3, 0),
    answer='Money spent on the armed forces',
    decoys=[
        'Money spent on foreign aid',
        'Money spent on space programmes',
        'Money spent on police and prisons',
        'Money spent on medical research',
        'Money spent on building roads and railways',
        'Money spent on farm subsidies',
        'Money spent on universities'],
    hints=[
        'One block is half the square. Ukraine has a larger block than France.',
        'Ukraine sits eighth, above France, Japan and Italy, and Saudi Arabia is fifth. Neither is a large economy, and 2023 is the clue to why one of them is here at all.',
        'Counted in US dollars in a single year. The largest block is 916 billion and the total across all twelve is over 1.8 trillion.',
        'Ukraine reached eighth in the world in 2023 for the most obvious reason imaginable.'],
    why='The United States takes almost half the square on its own, spending more than the next nine countries here put together, on a scale no other state attempts: a standing force of well over a million people and a network of overseas bases nobody else maintains. Ukraine eighth and Saudi Arabia fifth is what separates this from every other kind of national spending, since on aid, research, universities or infrastructure neither country would appear at all.',
    slug='MS.MIL.XPND.CD', source=WBU('MS.MIL.XPND.CD')[0], sourceUrl=WBU('MS.MIL.XPND.CD')[1]))

# ------------------------------------------------------- 69 cereal rank slope
c23 = [(nm(n), v) for n, v in wb.snap('AG.PRD.CREL.MT', 2023)]
a95 = {nm(n): i + 1 for i, (n, v) in enumerate(wb.snap('AG.PRD.CREL.MT', 1995))}
order = [n for n, _ in c23[:12]]
assert all(n in a95 for n in order), [n for n in order if n not in a95]
P.append(dict(
    family='Ranking', form='Rank slope · 1995 → 2023', type='slope', diff=3,
    truth='World ranking of grain-growing countries, 1995 vs 2023',
    period='1995 → 2023', unit='rank by tonnes of cereal harvested',
    leftYear=1995, rightYear=2023,
    ranks=arr([(n, a95[n], i + 1) for i, (n, _) in enumerate(c23[:12])], 3, 0),
    answer='World ranking of grain-growing countries',
    decoys=[
        'World ranking by the amount of farmland',
        'World ranking by the number of farmers',
        'World ranking by the amount of meat produced',
        'World ranking by the amount of fertiliser used',
        'World ranking by the number of tractors',
        'World ranking by the amount of water used for irrigation',
        'World ranking by the value of food exported'],
    hints=[
        'Argentina climbs eleven places and Bangladesh seven. France slips three.',
        'France ninth and Ukraine tenth, with Canada and Australia just behind, is a list of exporters rather than of large countries. Nigeria and Ethiopia, which have plenty of both land and farmers, do not appear.',
        'A ranking, so the chart shows no units. First place harvests about 640 million tonnes a year.',
        'It counts wheat, rice, maize and barley together, by weight, straight off the field.'],
    why='France, Ukraine, Canada, Argentina and Australia all appearing while Nigeria and Ethiopia do not is the discriminator. Those five have modest populations and modest amounts of farmland but enormous yields per hectare, which is a signature of mechanised grain rather than of land, labour or livestock.',
    slug='AG.PRD.CREL.MT', source=WBU('AG.PRD.CREL.MT')[0], sourceUrl=WBU('AG.PRD.CREL.MT')[1]))

# ------------------------------------------------------------- 70 inflation
s = wb.series('FP.CPI.TOTL.ZG', [2000, 2024])
SER = [('Turkey', 'TUR'), ('United Kingdom', 'GBR'), ('United States', 'USA'),
       ('Japan', 'JPN'), ('Switzerland', 'CHE')]
for lab, iso in SER:
    miss = [y for y in range(2000, 2025) if y not in s[iso]]
    assert not miss, (lab, miss)
P.append(dict(
    family='Change over time', form='Multi-line · 2000 to 2024', type='line', diff=4,
    truth='How fast prices rose each year, 2000 to 2024', period='2000–2024',
    unit='% change in consumer prices over a year', suffix='%', startYear=2000,
    series=[(lab, [s[iso][y] for y in range(2000, 2025)]) for lab, iso in SER],
    answer='How fast prices rose each year',
    decoys=[
        'Interest rates set by the central bank',
        'Annual growth in the economy',
        'Annual growth in average wages',
        'Government borrowing as a share of the economy',
        'Annual growth in house prices',
        'Unemployment as a share of the workforce',
        'Annual growth in the money supply'],
    hints=[
        'One line starts above 50 in 2000, spends fifteen quiet years in single figures, then returns to where it began.',
        'Four of the five lines sit almost on top of each other for two decades and then all lift together in 2022. Japan spends most of the period slightly below zero, which very few things can do.',
        'Measured as a percentage change over the previous year. The axis has to reach past 70 for one country.',
        'The shared spike in 2022 is what put central banks up in arms and mortgages up in price.'],
    why='Japan sitting a little under zero for most of two decades rules out growth, wages, borrowing and the money supply, none of which behave that way for that long. The simultaneous 2022 lift across four unrelated economies is the signature of a global price shock rather than of anything set country by country.',
    slug='FP.CPI.TOTL.ZG', source=WBU('FP.CPI.TOTL.ZG')[0], sourceUrl=WBU('FP.CPI.TOTL.ZG')[1]))

# --------------------------------------------------------- 71 growth in 2020
g = {nm(n): v for n, v in wb.snap('NY.GDP.MKTP.KD.ZG', 2020)}
GW = ['Guyana', 'Ireland', 'Ethiopia', 'China', 'Vietnam', 'Turkey', 'Norway',
      'Japan', 'United States', 'Germany', 'Brazil', 'France', 'India', 'Italy',
      'United Kingdom', 'Spain']
P.append(dict(
    family='Deviation', form='Diverging bar · against a line at zero',
    type='deviation', reference=0, diff=2,
    truth='How much each economy grew or shrank in 2020', period='2020',
    unit='% change over the year', suffix='%',
    data=arr([(c, round(g[c], 1)) for c in GW if c in g], 3, 1),
    answer='How much each economy grew or shrank in 2020',
    decoys=[
        'Change in the number of people in work during 2020',
        'Change in government spending during 2020',
        'Change in carbon dioxide emissions during 2020',
        'Change in the number of births during 2020',
        'Change in house prices during 2020',
        'Change in the number of people arriving from abroad during 2020',
        'Change in average wages during 2020'],
    hints=[
        'Spain is at the bottom of this chart and Guyana is at the top, and the year is 2020.',
        'Spain, the United Kingdom and Italy are the worst three, and China and Vietnam are positive. The countries that lost most are the ones that make their living from visitors and from restaurants, not the ones that had the worst epidemic.',
        'Measured as a percentage change across a single year, against a line at zero rather than an axis at zero.',
        'Guyana is at the top because it had just started pumping oil, and everyone else is where the pandemic left them.'],
    why='Guyana grew by 43.5 per cent in the worst year the world economy had seen since the war for a reason that had nothing to do with the pandemic: the Stabroek oilfield off its coast produced its first oil in December 2019, so 2020 was its first full year of pumping, and a country of 800,000 people had simply become an oil exporter. Everyone else is where the pandemic left them. Arrivals from abroad fell by 70 or 80 per cent almost everywhere that year, so a chart whose worst figure is about 11 per cent cannot be measuring visitors: Spain, Italy and the United Kingdom at the bottom is the shape of economies weighted towards tourism and hospitality meeting a year of closed borders.',
    slug='NY.GDP.MKTP.KD.ZG', source=WBU('NY.GDP.MKTP.KD.ZG')[0],
    sourceUrl=WBU('NY.GDP.MKTP.KD.ZG')[1]))

# ------------------------------------------------------ 72 fuel export share
def wpair(code, y1, y2, want, dec=1):
    d = {nm(n): (a, b) for n, a, b in wb.pair(code, y1, y2)}
    miss = [c for c in want if c not in d]
    if miss:
        sys.exit('%s missing: %s' % (code, miss))
    rows = [(c, round(d[c][0], dec), round(d[c][1], dec)) for c in want]
    rows.sort(key=lambda r: r[2])
    return rows

P.append(dict(
    family='Change over time', form='Dumbbell · 2000 → 2023', type='dumbbell', diff=4,
    truth='Share of a country\u2019s exports that is oil, gas or coal, 2000 vs 2023',
    period='2000 → 2023', unit='% of goods exported', suffix='%',
    leftYear=2000, rightYear=2023,
    data=arr(wpair('TX.VAL.FUEL.ZS.UN', 2000, 2023, [
        'Kuwait', 'Nigeria', 'Azerbaijan', 'Guyana', 'Saudi Arabia', 'Norway',
        'Kazakhstan', 'Colombia', 'Australia', 'Canada', 'Indonesia', 'Brazil',
        'United States', 'Germany'], 1), 3, 1),
    answer='Share of a country\u2019s exports that is oil, gas or coal',
    decoys=[
        'Share of a country\u2019s exports that is food',
        'Share of a country\u2019s electricity that comes from fossil fuels',
        'Share of a country\u2019s exports that is machinery',
        'Share of a country\u2019s government income that comes from tax',
        'Share of a country\u2019s exports that goes to China',
        'Share of a country\u2019s energy that is imported',
        'Share of a country\u2019s exports that is raw materials of any kind'],
    hints=[
        'One country on this chart starts at effectively zero in 2000 and ends above 85. It found something in 2015 and started selling it in 2019.',
        'Germany sits under 3 in both years, and Kuwait above 94 in both. Germany burned a great deal of coal across this whole period, so this is about what a country sells abroad rather than what it uses at home.',
        'Measured as a percentage of the value of everything a country sells abroad. Kuwait is above 94 in both years.',
        'Guyana is the country that went from nothing to almost everything, and the reason is an oilfield the size of the country itself.'],
    why='Germany near zero rules out anything about electricity or energy use, since Germany burned plenty of coal in both years. A measure where Kuwait is at 95 and Germany under 5 has to be about the composition of exports, and only one commodity dominates a national export list that completely.',
    slug='TX.VAL.FUEL.ZS.UN', source=WBU('TX.VAL.FUEL.ZS.UN')[0],
    sourceUrl=WBU('TX.VAL.FUEL.ZS.UN')[1]))

# ----------------------------------------------------------- 73 bank branches
P.append(dict(
    family='Change over time', form='Dumbbell · 2010 → 2023', type='dumbbell', diff=4,
    truth='Bank branches per 100,000 adults, 2010 vs 2023', period='2010 → 2023',
    unit='branches per 100,000 adults',
    leftYear=2010, rightYear=2023,
    data=arr(wpair('FB.CBK.BRCH.P5', 2010, 2023, [
        'Bulgaria', 'Mongolia', 'Spain', 'Portugal', 'Italy', 'France', 'Japan',
        'United States', 'Russia', 'Poland', 'Brazil', 'Germany', 'India',
        'Ethiopia', 'Kenya', 'Nigeria'], 1), 3, 1),
    answer='Bank branches per 100,000 adults',
    decoys=[
        'Cash machines per 100,000 adults',
        'Post offices per 100,000 adults',
        'Pubs and bars per 100,000 adults',
        'Petrol stations per 100,000 adults',
        'Pharmacies per 100,000 adults',
        'Police stations per 100,000 adults',
        'Public libraries per 100,000 adults'],
    hints=[
        'Spain has lost two thirds of them since 2010. Ethiopia has more than ten times as many as it had.',
        'Germany has fallen by more than half and Portugal and Italy are close behind, while India and Ethiopia have gone the other way entirely. The rich countries are shutting these while the poorer ones are still opening them, which is the opposite of how a count of buildings usually behaves.',
        'Counted per 100,000 adults rather than per head of population, because the thing being counted is for grown-ups.',
        'They are shutting at a rate of several hundred a year across Western Europe, because almost everybody now does it on a phone.'],
    why='Rich countries falling while poorer ones climb rules out pharmacies, petrol stations and post offices, which either track population or fall everywhere. Mongolia and Bulgaria high is the giveaway: both built out dense retail banking networks in the 2000s just as Western Europe began dismantling its own.',
    slug='FB.CBK.BRCH.P5', source=WBU('FB.CBK.BRCH.P5')[0], sourceUrl=WBU('FB.CBK.BRCH.P5')[1]))

for i, o in enumerate(P):
    o['exhibit'] = ex(62 + i)

print(',\n'.join(block(o) for o in P))
sys.stderr.write('built %d puzzles\n' % len(P))
