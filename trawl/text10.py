"""Text for build10.py, written from `build10.py --digest` (the final data)."""

TEXT = {
'government-debt': dict(
    diff=2, answer='Government debt as a share of GDP',
    decoys=['Household debt as a share of GDP', 'Government spending as a share of GDP',
            'Exports as a share of GDP', 'Tax revenue as a share of GDP'],
    hints=['Every dumbbell on this chart starts the year before the crash of 2008, and some never recovered from it.',
           'Greece and Italy finish above 130, which no measure of spending or tax could reach, and Denmark sits near the bottom.',
           'A percentage of each country\u2019s annual GDP, in 2007 and 2024.',
           'It is what the state owes, and the eurozone\u2019s rules say it should stay under 60.'],
    why='Greece rises from 104.6 to 154.2 per cent and Spain nearly triples from 35.7 to 101.6, while Estonia ends lowest at 23.5. '
        'Household debt dies on Denmark at 30.5, where households owe more relative to the economy than almost anywhere. '
        'Government spending dies on the top of the chart, since no state spends 154 per cent of its economy in a year. '
        'Exports die on Ireland at 38.3, one of the most export-heavy economies in the world.'),

'part-time-work': dict(
    diff=2, answer='Share of workers who work part-time',
    decoys=['Share of workers with a second job', 'Share of workers in public-sector jobs',
            'Share of workers who are women', 'Share of workers on night shifts'],
    hints=['The Dutch figure has been near the top of every version of this chart since the 1980s.',
           'Bulgaria and Romania end near zero, which no measure of women or public servants in the workforce could do, and the Dutch figure is far too large for second jobs.',
           'A percentage of everyone aged 15 to 64 in work, in 2004 and 2024.',
           'Fewer hours than a full week, by choice or otherwise.'],
    why='The Netherlands leads at 42.7 per cent, down slightly from 45.2, while Austria climbs from 19.9 to 30.5, Germany from 21.9 to 29.0 and Bulgaria falls to 1.5. '
        'Second jobs die on the Dutch figure, since no country has four workers in ten holding two jobs. '
        'Public-sector jobs die on Bulgaria at 1.5, where the state employs far more than that. '
        'Women in work die on the same figure, since women are close to half the workforce everywhere.'),

'organic-farmland': dict(
    diff=3, answer='Share of farmland farmed organically',
    decoys=['Share of farmland that is irrigated', 'Share of farmland used for grazing',
            'Share of farmland planted with cereals', 'Share of farmland under glass'],
    hints=['Portugal\u2019s figure more than tripled in ten years, while Poland\u2019s went backwards.',
           'Estonia leads and Malta is last, the reverse of any chart about watering fields, and Ireland, almost all grass, is near the bottom.',
           'A percentage of all farmland in use, in 2012 and 2022.',
           'No synthetic fertiliser, no synthetic pesticide, and a certificate to prove it.'],
    why='Estonia farms 23.4 per cent of its land this way, Portugal more than triples to 19.3 and Italy roughly doubles to 18.1, while Malta ends at 0.6. '
        'Irrigation dies on that order, since Malta and Spain water far more of their farmland than Estonia. '
        'Grazing dies on Ireland at 2.2, a country almost entirely under grass. '
        'Cereals die on the ceiling: nothing here passes a quarter, when cereals cover far more than that across most of the EU.'),

'bank-account-ownership': dict(
    diff=2, answer='Share of adults with a bank or mobile-money account',
    decoys=['Share of adults who own a smartphone', 'Share of adults who use the internet',
            'Share of adults who can read and write', 'Share of adults who own a car'],
    hints=['India\u2019s figure more than doubled, and most of the rise came inside three years.',
           'Kenya at 90 is far above anything it could reach in smartphones or internet use, and Egypt and Pakistan are too low for reading and writing.',
           'A percentage of everyone aged 15 and over, surveyed in 2011 and 2024.',
           'A savings book, a debit card or a wallet on a phone all count.'],
    why='India climbs from 35.2 to 89.0 per cent after a government drive opened hundreds of millions of accounts, and Kenya reaches 90.1 on the back of mobile money, while Pakistan ends lowest at 27.3. '
        'Smartphones die on Kenya, where far fewer than nine adults in ten own one. '
        'Internet use dies on India in 2011 at 35.2, years before a third of Indians were online. '
        'Literacy dies on Pakistan and Egypt at 27.3 and 43.1, well below the share who can read in either.'),

'women-outlive-men': dict(
    diff=3, answer='Years women can expect to outlive men',
    decoys=['Years by which husbands are older than their wives',
            'Years of schooling women have over men',
            'Years by which men retire later than women',
            'Years by which men\u2019s working lives outlast women\u2019s'],
    hints=['The largest gap at the end belongs to a country at war, and it widened by two years.',
           'The top of the chart is former Soviet republics at ten years or more, far beyond any gap in marriage age, schooling or retirement.',
           'Years, in 2000 and 2023.',
           'It is the difference between two life expectancies, and in Russia much of it is drink, tobacco and accidents among men.'],
    why='Ukraine ends with the largest gap, 13.3 years, widened by the war, and Russia narrows from 13.2 to 10.7, while in India and Bangladesh women outlive men by about three. '
        'The gap in marriage age dies on the top of the chart, since husbands are not typically a decade older than their wives anywhere here. '
        'Schooling dies on the same figures, which no education gap comes near. '
        'Retirement dies there too: no country makes men work ten years longer than women.'),

'energy-imported': dict(
    diff=4, answer='Share of energy that is imported',
    decoys=['Share of energy from renewable sources', 'Share of energy from coal',
            'Share of energy used by industry', 'Share of energy used for heating'],
    hints=['One country here ends almost self-sufficient on a rock that burns.',
           'The Netherlands more than doubles after closing its great gas field, Malta stays near a hundred, and Sweden, full of dams and forests, sits low.',
           'A percentage of all the energy a country uses, in 2004 and 2023.',
           'Pipelines, tankers and cables from abroad supply almost all of Malta\u2019s and almost none of Estonia\u2019s.'],
    why='Malta imports 97.6 per cent of its energy and Estonia only 3.5, running increasingly on its own oil shale, while the Netherlands jumps from 32.1 to 70.4 as the Groningen gas field was wound down. '
        'Renewables die on Sweden at 26.4, a country that gets most of its energy from water, wood and wind. '
        'Coal dies on the Netherlands at 70.4, far above any share coal has had there. '
        'Industry\u2019s share dies on Malta at 97.6, since no country\u2019s factories use nearly all its energy.'),

'household-size': dict(
    diff=3, answer='Average number of people per household',
    decoys=['Average number of rooms per person', 'Average number of cars per household',
            'Average number of televisions per home', 'Average number of bedrooms per home'],
    hints=['Slovakia and Poland went one way over these twenty years, and almost everyone else went the other.',
           'Slovakia has some of the most crowded homes in the EU and tops this chart, and no country has three cars for every home.',
           'People, averaged across every private household, in 2005 and 2024.',
           'The Nordic figure is low because so many there live alone.'],
    why='Slovakia rises from 2.9 to 3.1 and Poland from 2.8 to 2.9, while Bulgaria falls from 2.9 to 2.3 and Finland ends lowest at 1.9. '
        'Rooms per person dies on Slovakia, where homes are among the most crowded in the EU and yet it tops this chart. '
        'Cars and televisions per home both die on Slovakia\u2019s 3.1, since neither reaches three a household anywhere in Europe.'),

'young-graduates-rank': dict(
    diff=3, answer='EU ranking by share of 25 to 34 year olds with a degree',
    decoys=['EU ranking by youth unemployment', 'EU ranking by average income of 25 to 34 year olds',
            'EU ranking by share of 25 to 34 year olds who own their home',
            'EU ranking by share of young adults who smoke'],
    hints=['Finland fell fifteen places without its own figure moving, which says everything about everyone else.',
           'Lithuania, far poorer than most, climbs to fourth, and Romania, where almost everyone owns their home, is last in both years.',
           'A rank among the 27 EU countries by the share of people aged 25 to 34, in 2004 and 2024.',
           'Three years of lectures and a certificate at the end of them.'],
    why='Ireland rises to first with 65.2 per cent and Luxembourg climbs from eleventh to second, while Finland falls from sixth to twenty-first although its own figure barely moved, from 38.2 to 39.1. '
        'Youth unemployment dies on Ireland at the top and on Spain in eighth, when Spain would lead that ranking. '
        'Income dies on Lithuania, fourth here and far from the richest. '
        'Home ownership dies on Romania, last in both years, where almost every household owns its home.'),

'union-membership-rank': dict(
    diff=4, answer='OECD ranking by share of employees who belong to a trade union',
    decoys=['OECD ranking by share of workers covered by collective agreements',
            'OECD ranking by days lost to strikes', 'OECD ranking by paid holiday entitlement',
            'OECD ranking by minimum wage'],
    hints=['The top of this list barely moved in twenty years, and at the very top is a country of under four hundred thousand people.',
           'France, a byword for strikes and for long holidays, is near the bottom, and so is the United States.',
           'A rank among the OECD countries reporting both years, highest first, 2000 and 2019.',
           'In much of Scandinavia it is the union, not the state, that pays out when you lose your job.'],
    why='Iceland is first in both years, with 91.1 per cent of employees in a union by 2019, and the Nordic countries hold most of the next places, while France sits twenty-sixth at 10.1 and Estonia falls to last. '
        'Collective agreements die on France, where they cover almost every employee despite so few members. '
        'Strikes die on the same French figure, near the bottom of a ranking France would lead. '
        'Paid holiday dies on France again, which has some of the most generous leave in the OECD.'),

'average-wage-rank': dict(
    diff=3, answer='OECD ranking by average annual wage, adjusted for prices',
    decoys=['OECD ranking by economic output per person', 'OECD ranking by output per hour worked',
            'OECD ranking by share of workers with a degree', 'OECD ranking by average pension paid'],
    hints=['Iceland climbs to first, and Italy, Japan and Greece each drop nine places or more.',
           'Ireland, near the top of any chart of output per person, is only twelfth, and Japan, full of graduates, falls to twenty-sixth.',
           'A rank among the OECD countries reporting both years, highest first, after adjusting for what money buys at home.',
           'It is what the average full-time job pays in a year.'],
    why='Iceland climbs from fifth to first and Lithuania from thirty-fourth to twenty-fourth, while Italy falls fourteen places and Greece drops to thirty-fifth, its average wage lower in real terms than in 2000. '
        'Output per person dies on Ireland in twelfth, a country near the top of that ranking. '
        'Output per hour dies on the same Irish figure. '
        'Graduates die on Japan, twenty-sixth here and one of the most educated workforces in the OECD.'),

'gender-employment-gap-rank': dict(
    diff=4, answer='EU ranking by the gap between men\u2019s and women\u2019s employment rates',
    decoys=['EU ranking by the gap between men\u2019s and women\u2019s pay',
            'EU ranking by unemployment rate', 'EU ranking by share of women in parliament',
            'EU ranking by birth rate'],
    hints=['Malta started this period first by a distance and has spent fifteen years falling.',
           'Italy, which has one of the smallest pay gaps in the EU, is first, and Czechia, with almost no unemployment, is fifth.',
           'A rank among the 27 EU countries, largest first, measured in percentage points for people aged 20 to 64, 2009 and 2024.',
           'Take the share of men in work and subtract the share of women.'],
    why='Italy ends first with a gap of 19.4 points between the shares of men and women in work, and Malta, first in 2009 at 37.5, falls to fourth at 13.6 as women moved into work; Finland ends last at 0.7. '
        'The pay gap dies on Italy at the top, where the difference in pay is among the smallest in the EU. '
        'Unemployment dies on Czechia in fifth, with one of the lowest jobless rates in Europe. '
        'Women in parliament die on Finland and Sweden near the bottom, when both would lead that ranking.'),

'recycling-rate-rank': dict(
    diff=3, answer='EU ranking by share of household waste recycled',
    decoys=['EU ranking by share of household waste burned for energy',
            'EU ranking by share of household waste sent to landfill',
            'EU ranking by share of electricity from renewable sources',
            'EU ranking by food thrown away per person'],
    hints=['Lithuania rose fifteen places in nineteen years, and Sweden fell twelve.',
           'Sweden, which burns more of its rubbish than almost anyone and runs on hydropower, drops to seventeenth, and Romania is last in both years.',
           'A rank among the EU countries reporting both years, highest first, 2004 and 2023.',
           'Glass, paper, cans and the food caddy, as a share of everything collected from homes.'],
    why='Germany ends first with 68.7 per cent, Slovenia climbs from thirteenth to third and Lithuania from twenty-fifth to tenth, while Sweden falls from fifth to seventeenth. '
        'Burning for energy dies on Sweden, which burns about half its household waste and yet slips down this list. '
        'Landfill dies on Romania, last in both years when it would top any ranking of waste buried. '
        'Renewable electricity dies on the same Swedish fall.'),

'rail-travel-per-person-rank': dict(
    diff=4, answer='EU ranking by distance travelled by train per person',
    decoys=['EU ranking by rail freight per person', 'EU ranking by length of high-speed track',
            'EU ranking by railway track per square kilometre', 'EU ranking by train punctuality'],
    hints=['Greece travels less than half as far this way as it did in 2004, and ends last.',
           'Spain, with the longest high-speed network in Europe, is only eleventh, and Czechia, with one of the densest webs of track, is ninth.',
           'A rank among the EU countries reporting both years, highest first, 2004 and 2023.',
           'Passenger-kilometres divided by population: every journey counted by its length.'],
    why='Austria climbs to first with about 1,585 kilometres a year for every resident, overtaking France, while Greece falls to last as its figure more than halves. '
        'High-speed track dies on Spain in eleventh, the owner of Europe\u2019s longest high-speed network. '
        'Track density dies on Czechia in ninth, one of the most thickly railed countries for its area. '
        'Freight dies on Lithuania near the bottom, one of the heaviest rail freight countries for its size.'),
}
