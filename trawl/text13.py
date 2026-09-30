"""Text for build13.py, written from `build13.py --digest` (the final data)."""

TEXT = {
'hospital-average-stay': dict(
    diff=2, answer='Average length of a hospital stay',
    decoys=['Average wait for planned surgery', 'Paid holiday days a year',
            'Average hospital stay after giving birth', 'Days of sick leave per worker a year'],
    hints=['At the top, a system in which a ward bed has long doubled as a care home for the very old.',
           'Denmark and Sweden end at 5.4, a quarter of the paid holiday every EU worker is owed, and nothing on the chart reaches a month.',
           'Days, averaged across all patients, in 2010 and 2023.',
           'The time between admission and discharge.'],
    why='Japan leads at 26.3 days, down from 32.5, because its hospitals long kept elderly patients in beds that elsewhere would be care-home places. '
        'South Korea, second at 17.5, rose by 1.7 days, and Turkey ends lowest at 4.2. '
        'Surgical waits die on the scale, since waits for a new hip run to months and nothing here reaches a month. '
        'Paid holiday dies on Denmark and Sweden at 5.4 days, a quarter of the 20 days EU law guarantees. '
        'A stay after giving birth dies on Japan\u2019s 26.3, when even long maternity stays last about a week.'),

'nurses-per-thousand': dict(
    diff=3, answer='Practising nurses per 1,000 people',
    decoys=['Practising doctors per 1,000 people', 'Hospital beds per 1,000 people',
            'Pharmacists per 1,000 people', 'Dentists per 1,000 people'],
    hints=['The leader fills many of these posts with people who cross its borders every morning.',
           'Greece sits second from the bottom though it has more doctors per head than anyone here, and the top figure of 18.8 is far beyond any count of pharmacists.',
           'People working in the profession per 1,000 inhabitants, in 2010 and 2023.',
           'Florence Nightingale\u2019s profession.'],
    why='Switzerland leads at 18.8 and Norway follows at 15.6, while South Korea more than doubles from 4.6 to 9.5 and Mexico ends lowest at 3.0. '
        'Doctors die on Switzerland, since no country has 19 doctors per 1,000 people, and on Greece at 4.1, second from the bottom, when it has more doctors per head than any other country here. '
        'Hospital beds die on the direction: beds per head have been cut across most of Europe since 2010, while 12 of these 15 dumbbells rise. '
        'Pharmacists die on the scale, since they number about one per 1,000 people almost everywhere.'),

'adults-without-upper-secondary': dict(
    diff=3, answer='Adults who never finished upper secondary school',
    decoys=['Adults with a university degree', 'Adults working in agriculture',
            'Adults who speak only one language', 'Adults who smoke daily'],
    hints=['Portugal starts this chart barely a generation after a dictatorship that sent most of its children out to work young.',
           'South Korea and Canada, among the best-qualified countries on earth, finish near the bottom, and Portugal starts at 80.6, far more than ever worked the land.',
           'A percentage of everyone aged 25 to 64, in 2000 and 2024.',
           'They left the classroom before the final exams of their teens.'],
    why='Portugal falls furthest, from 80.6 to 38.5 per cent, and South Korea from 31.8 to 6.5, as the generations who left school young age out of the band. '
        'Mexico ends highest at 54.4 and Poland lowest at 5.2. '
        'A university degree dies on South Korea and Canada near the bottom, two of the most highly qualified populations in the world. '
        'Farm work dies on Portugal\u2019s 80.6 in 2000, when its farms employed nowhere near four adults in five. '
        'Speaking one language dies on the United Kingdom at 17.1, below Spain and Italy, when Britons are the likeliest people here to speak nothing else.'),

'tertiary-enrolment': dict(
    diff=5, answer='Students in higher education per 100 people of university age',
    decoys=['Internet users per 100 people', 'Teenagers in secondary school per 100 people of that age',
            'Mobile phone subscriptions per 100 people', 'Children in pre-school per 100 people of that age'],
    hints=['In Greece a place, once won, can be kept on the books for life.',
           'Greece passes 100, which no count of people online could do, and the United Kingdom\u2019s 80 is too low for teenagers, who stay in education to 18 in England, or for mobile phones, which outnumber Britons.',
           'Enrolments per 100 people of the matching age, in 2000 and 2023. Anyone enrolled counts, whatever their age, so the figure can pass 100.',
           'Lecture halls and degrees.'],
    why='Greece rises from 53 to 165, because students who stop attending stay enrolled and every student is counted against a single five-year age band; Argentina, South Korea and Chile also pass 100. '
        'China climbs from 8 to 75 and Tanzania ends lowest at 5. '
        'Internet use dies on Greece, since no country has more users than people. '
        'Secondary school dies on the United Kingdom at 80, where teenagers in England stay in education or training until 18, and on Tanzania at 5. '
        'Mobile phones die on the same British figure, since subscriptions there outnumber people.'),

'manufacturing-share': dict(
    diff=3, answer='Manufacturing as a share of GDP',
    decoys=['Tax revenue as a share of GDP', 'Agriculture as a share of GDP',
            'Exports as a share of GDP', 'Tourism as a share of GDP'],
    hints=['The top figure is swollen by a handful of foreign firms that book their patents and drug output in a small island.',
           'France ends under 10, where the state takes over 40 per cent of the economy in tax, and Germany and Japan sit near 19, far too high for farming.',
           'A percentage of GDP, in 1995 and 2024.',
           'What factories add to an economy.'],
    why='Ireland leads at 29.6 per cent, up from 20.7, largely because multinational drug and electronics makers book their output there, and Cambodia climbs from 9.1 to 27.8 on the back of garment factories. '
        'Australia ends lowest at 5.4, down from 13.0, and the United Kingdom roughly halves to 8.0. '
        'Tax dies on France at 9.6, where tax takes over 40 per cent of the economy. '
        'Agriculture dies on Germany at 18.0 and Japan at 18.8. '
        'Exports die on Ireland\u2019s 29.6, when its exports are worth more than its entire GDP.'),

'refugees-hosted': dict(
    diff=2, answer='Refugees hosted',
    decoys=['Immigrants living in the country', 'Foreign tourists received a year',
            'Migrants arriving by boat', 'Foreign students enrolled'],
    hints=['Much of this chart moved in a few weeks of 2022, across a single border in Europe.',
           'The United States ends near 435,000, far too few for its foreign-born, and Chad and Uganda, with no coastline, sit near the top.',
           'Thousands of people, counted in 2010 and 2024.',
           'They fled across a border and cannot safely go home.'],
    why='Iran ends highest at 3.5 million, most of them Afghans, with Turkey at 2.9 million, up from 10,000 before the war across its southern border, and Germany at 2.7 million. '
        'Poland jumps from 16,000 to just over a million after the full-scale war next door in 2022. '
        'Immigrants die on the United States at 435,000, a country home to tens of millions of people born abroad. '
        'Tourists die on Spain and France, which receive tens of millions of visitors a year, not a few hundred thousand. '
        'Boat arrivals die on Chad and Uganda, which have no coast.'),

'solar-share-of-electricity': dict(
    diff=3, answer='Share of electricity generated by solar power',
    decoys=['Share of electricity generated by wind', 'Share of electricity generated by nuclear power',
            'Share of electricity generated by hydropower', 'Share of electricity generated by gas'],
    hints=['In ten years the rooftops of the Hungarian plain turned dark and glassy.',
           'Denmark sits mid-table and Ireland near the bottom, though turbines supply a third or more of their power, France ends at 4.4, and Poland rises from nothing without ever having run a reactor.',
           'A percentage of all electricity generated, in 2014 and 2024.',
           'Panels facing south.'],
    why='Hungary leads at 24.2 per cent, up from 0.2, just ahead of Greece at 19.4 and Spain at 18.7, while Finland ends lowest at 1.1. '
        'Wind dies on Denmark at 10.7 and Ireland at 3.5, where turbines produce well over a third of the power. '
        'Nuclear dies on France at 4.4, which gets about two thirds of its electricity from reactors, and on Poland, which has none and still climbs to 10.2. '
        'Hydropower dies on Sweden at 2.4 and Austria at 9.9, where rivers supply far more.'),

'holidays-abroad': dict(
    diff=2, answer='Share of personal trips that went abroad',
    decoys=['Share of trips taken by plane', 'Share of trips taken for business',
            'Share of trips taken by train', 'Share of trips spent camping'],
    hints=['From the top country, a drive of forty minutes in almost any direction reaches a frontier.',
           'Nobody makes 95 per cent of their journeys by plane or on business, and Spain and Greece, where so much of the summer is spent at home, sit near the bottom.',
           'A percentage of all trips of one night or more taken for personal reasons, in 2014 and 2024.',
           'A passport, or at least a border crossed.'],
    why='Luxembourg leads at 95.0 per cent, down from 98.3, because almost any trip from a country that size ends across a border, and Belgium is second at 76.1. '
        'Romania ends lowest at 10.6 and Spain at 11.6, countries big and warm enough to holiday at home. '
        'Planes die on Luxembourg\u2019s 95, since nobody flies for almost every trip, and trains die on the same figure. '
        'Business trips die too, because these are trips people took for their own reasons.'),

'income-inequality-rank': dict(
    diff=4, answer='Income inequality (Gini coefficient)',
    decoys=['Unemployment rate', 'Home ownership rate',
            'Household debt as a share of GDP', 'Share of people aged over 65'],
    hints=['Along the Black Sea coast, a flat tax meets some of the lowest wages in Europe.',
           'Spain is never higher than sixth, which no measure of joblessness in 2015 could allow, and Germany sits mid-table though fewer Germans own their home than anyone else in the EU.',
           'Rank among the 27 EU countries, highest first, in 2015 and 2024. The figures behind the ranks run from 0 to 100.',
           'How far a country\u2019s incomes are from being equally shared.'],
    why='Bulgaria climbs to first, at 38.4 on a scale where 0 means everyone has the same income, while Romania falls from second to 17th as its minimum wage rose several times over, and Slovakia is the most equal, last in both years. '
        'Unemployment dies on Spain, which had one of the two highest jobless rates in the EU in 2015 and is only sixth here. '
        'Home ownership dies on Germany in mid-table, where fewer people own their home than anywhere else in the EU. '
        'Household debt dies on Bulgaria at the top, where households borrow little.'),

'arms-imports-rank': dict(
    diff=3, answer='Arms imports',
    decoys=['Arms exports', 'Military spending', 'Oil imports', 'Soldiers in the armed forces'],
    hints=['In 2004 the top country was re-equipping from Moscow; twenty years later it made almost everything itself.',
           'China drops from first to 40th in years when it outspent every country but one on its forces, bought more oil than anyone and began selling its own weapons abroad.',
           'Rank among the 77 countries with a figure in both years, largest first, 2004 and 2024.',
           'Weapons bought from other countries.'],
    why='Poland climbs from 26th to first as it rearmed after 2022, Hungary from 40th to 13th and Norway from 71st to 22nd, while China falls from first to 40th because it now builds its own. '
        'Arms exports die on the Chinese fall, when China has become one of the largest sellers of weapons in the world, and on Poland at the top, which sells few. '
        'Military spending dies on China at 40th, the second-largest spender in the world. '
        'Oil imports die on the same Chinese fall, since China buys more oil than any country on earth.'),

'household-saving-rank': dict(
    diff=5, answer='Household saving rate',
    decoys=['Household debt as a share of income', 'Home ownership rate',
            'Share of income spent on food', 'Share of people aged over 65'],
    hints=['In the Greek crisis years families lived on what they had put by, and never rebuilt it.',
           'Germany finishes first, where people borrow little and fewer own their home than anywhere else in the EU, and Romania sits near the bottom.',
           'Rank among the 26 EU countries with a figure in both years, highest first, 2005 and 2024.',
           'What is left of disposable income once it has been spent.'],
    why='Germany ranks first at 20.0 per cent of disposable income, Malta climbs from 24th to 4th, and Sweden and Denmark rise sharply, while Italy falls from third to 17th and Greece and Romania end below zero, spending more than they earned. '
        'Household debt dies on Germany at the top, where households borrow less than almost anywhere in northern Europe. '
        'Home ownership dies on the same German first place, since Germans are the least likely in the EU to own their home. '
        'Food spending dies on Germany too, and on Romania near the bottom, where food takes a larger share of spending than anywhere else in the EU.'),

'electricity-price-rank': dict(
    diff=4, answer='Household electricity prices',
    decoys=['Share of electricity from renewables', 'Petrol prices', 'Household gas prices',
            'Average household energy use'],
    hints=['Hungary finishes last in 2024 because a government decree has held one bill down for a decade.',
           'Germany ranks first although coal and gas still run much of its grid, Czechia climbs to fourth, and the Netherlands falls to 18th, where fuel at the pump is among the dearest in Europe.',
           'Rank among the 27 EU countries, dearest first, in the second half of 2008 and of 2024, for a home using 2,500 to 4,999 kilowatt hours a year, taxes included.',
           'The bill for keeping the lights on.'],
    why='Germany rises to first, at 39.4 euro cents a kilowatt hour with taxes, Czechia climbs from 16th to 4th and France from 19th to 8th, while Hungary drops from 12th to last under a price cap and Malta, with state-set tariffs, falls to 25th. '
        'Renewables die on Czechia at fourth, which still burns coal for much of its power, and on Germany ranking above Denmark. '
        'Petrol dies on the Netherlands at 18th, where fuel at the pump is among the dearest in Europe. '
        'Gas dies on the same Dutch place, since Dutch households pay some of the highest gas bills in the EU.'),

'life-satisfaction-rank': dict(
    diff=4, answer='Life satisfaction',
    decoys=['Household income per person', 'Life expectancy', 'Trust in government',
            'Share of adults who exercise weekly'],
    hints=['In the top country\u2019s far north, midwinter passes for weeks without a sunrise.',
           'Romania climbs to joint second and Luxembourg, the richest country in the EU, sinks to 16th, which rules out anything measured in money or years of life.',
           'Rank among the 27 EU countries, highest first, 2013 and 2024, from average scores out of ten given by people aged 16 and over.',
           'All things considered, how content they say they are.'],
    why='Finland ranks first in both years, at 7.8 out of 10 in 2024, Romania climbs from 11th to joint second and Portugal from 23rd to 14th as the crisis years fade, while Sweden falls from third to 11th, Germany from 9th to 24th, and Bulgaria is last in both years, though its score rose most. '
        'Income dies on Luxembourg at 16th and on Romania at second, one of the EU\u2019s poorer countries. '
        'Life expectancy dies on Romania too, where lives are among the shortest in the EU. '
        'Trust in government dies on the same Romanian place, as Romanians report some of the lowest trust in their politicians in Europe.'),
}
