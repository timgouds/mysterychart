"""Text for build9.py, written from `build9.py --digest` (the final data)."""

TEXT = {
'olive-harvest': dict(
    diff=1, answer='Olives harvested',
    decoys=['Grapes grown for wine', 'Hazelnuts harvested', 'Cork stripped from trees',
            'Lemons grown'],
    hints=['A crop that outlives the people who plant it, sometimes by a thousand years.',
           'France, which makes more wine than almost anyone, barely registers, and Portugal is only fifth.',
           'Thousand tonnes harvested in 2024, across the EU and the countries hoping to join it.',
           'Most of it is pressed rather than eaten, and the province of Jaén alone accounts for a large part of the biggest block.'],
    why='Spain harvests 8.3 million tonnes, more than twice Turkey and nearly half of everything on the chart. '
        'Grapes for wine die on France at 28 thousand tonnes, a country that could not make its wine from so little. '
        'Hazelnuts die on the order, since Turkey grows most of the world\u2019s hazelnuts and here trails Spain by more than half. '
        'Cork dies on Portugal in fifth place, when it strips about half the world\u2019s cork on its own.'),

'brussels-sprouts-grown': dict(
    diff=2, answer='Brussels sprouts grown',
    decoys=['Chicory grown', 'Cauliflower and broccoli grown', 'Tulip bulbs grown', 'Leeks grown'],
    hints=['The two largest blocks are almost exactly the same size, and they belong to neighbours who have disagreed about most things.',
           'Spain and Italy, two of Europe\u2019s great vegetable gardens, hardly feature: this is a crop for cold, wet, northern fields.',
           'Thousand tonnes harvested in 2024, EU countries only.',
           'The Belgian capital lends it its name, and the Dutch grow slightly more of it.'],
    why='The Netherlands grows 64.7 thousand tonnes and Belgium 63.7, so the vegetable named after the Belgian capital is grown in greatest quantity just over the border. '
        'Chicory dies on that order, since Belgium grows several times as much of it as the Netherlands. '
        'Cauliflower and broccoli die on Spain at 3.2 and Italy at 6.5, both among the largest growers of each. '
        'Tulip bulbs die on Belgium matching the Netherlands almost exactly, when the Dutch grow most of the world\u2019s bulbs.'),

'fish-and-seaweed-farmed': dict(
    diff=2, answer='Fish, shellfish and seaweed farmed',
    decoys=['Fish and seafood eaten', 'Fish and seafood exported', 'Rice grown', 'Fertiliser used'],
    hints=['The Mekong, the Ganges and the Nile each run through at least one of these blocks.',
           'Norway, Chile and Ecuador are here and none of them grows rice worth mentioning; Japan and the United States are nowhere.',
           'Thousand tonnes in 2022, counted by live weight and including plants.',
           'Norway\u2019s block is almost all salmon, and much of Indonesia\u2019s is seaweed.'],
    why='China produces 75.4 million tonnes, five times Indonesia and more than the other eleven blocks put together. '
        'Fish and seafood eaten dies on the absence of Japan and the United States, two of the largest markets for it. '
        'Exports die on Norway, the world\u2019s second largest seafood exporter and only eighth here, behind Bangladesh and the Philippines. '
        'Rice dies on Norway, Chile and Ecuador, which grow almost none. '
        'Indonesia is second because seaweed counts, and Norway\u2019s figure is nearly all salmon.'),

'sea-passengers': dict(
    diff=2, answer='Passengers passing through seaports',
    decoys=['Goods handled at seaports', 'Passengers passing through airports',
            'Nights spent by tourists', 'Cruise ships calling'],
    hints=['Some of the busiest crossings on this chart take less time than the queue to board them.',
           'The Netherlands, which handles more cargo than any other country in Europe, is nowhere, while Malta outranks Finland.',
           'Millions, counting everyone who boarded or left a ship in the country\u2019s ports in 2024, so a single crossing is counted at both ends.',
           'Think of the Strait of Messina, the \u00d8resund and the hop from Helsinki to Tallinn.'],
    why='Italy leads with 93.5 million, much of it crossings to Sicily, Sardinia and the islands of the Bay of Naples, with Greece close behind on its island ferries. '
        'Goods handled at seaports dies on the absence of the Netherlands, home to Europe\u2019s largest port. '
        'Air passengers die on Germany and France, with the continent\u2019s busiest airports and only sixth and eighth here. '
        'Tourist nights die on Denmark in third place, above Spain and France, a ranking made by short sea crossings rather than stays.'),

'hops-grown': dict(
    diff=2, answer='Hops grown',
    decoys=['Beer brewed', 'Barley grown for malting', 'Tobacco grown', 'Sugar beet grown'],
    hints=['A single valley in Bavaria accounts for most of the largest circle.',
           'Belgium, the Netherlands and Ireland are nowhere, which would be strange for anything poured into a glass.',
           'Thousand tonnes harvested in 2024, from the only EU countries that grow any.',
           'It climbs wires strung high above the field, is picked in late summer, and the brewers of Munich and Pilsen buy almost all of it.'],
    why='Germany grows 46.5 thousand tonnes, seven times Czechia and about three quarters of everything here. '
        'Beer brewed dies on the absence of Belgium, the Netherlands and Ireland, and on Slovenia in fourth place. '
        'Barley for malting dies on France, one of the world\u2019s largest growers of it and sixth here with 0.67. '
        'Tobacco dies on Italy, the EU\u2019s largest tobacco grower and last on this chart.'),

'asparagus-grown': dict(
    diff=2, answer='Asparagus grown',
    decoys=['Strawberries grown', 'Leeks grown', 'Peaches grown', 'Cabbages grown'],
    hints=['For about ten weeks every spring, restaurants across the largest country here print a separate menu.',
           'Germany, which grows almost no peaches, is first by a distance, and Belgium is ninth.',
           'Thousand tonnes harvested in 2024, the largest growers in the EU.',
           'It is cut by hand from mounded soil, white if it never sees the light and green if it does.'],
    why='Germany grows 108.1 thousand tonnes, nearly twice Italy and more than Spain and France together. '
        'Strawberries die on Spain, the EU\u2019s largest grower of them, third here at barely half the German figure. '
        'Leeks die on Belgium at 2.9, ninth here and one of the two largest leek growers in the EU. '
        'Peaches die on Germany itself, too far north to grow many.'),

'campsite-nights': dict(
    diff=2, answer='Nights spent at campsites',
    decoys=['Nights spent in hotels', 'Nights spent in youth hostels', 'Ski lift passes sold',
            'Nights spent on cruise ships'],
    hints=['The largest circle is almost three times the size of the next, and the next is Italy.',
           'Austria and Switzerland, with the best of the Alps, are near the bottom, and Greece is nowhere for all its hotel coast.',
           'Millions of nights in 2024, counted from every guest who stayed, whether they lived in the country or not.',
           'Pitches, awnings and a shared shower block.'],
    why='France records 147.8 million nights, nearly three times Italy, on a coastline and countryside laid out for it. '
        'Hotel nights die on the absence of Greece, which fills far more hotel beds than the Netherlands, fifth here. '
        'Youth hostels die on Germany, home of the largest hostel network in the world and fourth on this chart. '
        'Ski passes die on Austria and Switzerland, ninth and twelfth.'),

'women-in-ict-jobs': dict(
    diff=4, answer='Share of computing and IT specialists who are women',
    decoys=['Share of company board seats held by women', 'Share of doctors who are women',
            'Share of airline pilots who are women', 'Share of engineering graduates who are women'],
    label=['Estonia', 'Romania', 'Bulgaria', 'Sweden', 'France', 'Czechia'],
    labelSm=['Estonia', 'France', 'Czechia'],
    hints=['Four of the top five were in the Warsaw Pact or the Soviet Union itself.',
           'France and Norway, which both legislated for women on company boards, are stuck in the middle, and nothing here reaches thirty per cent.',
           'A percentage of everyone employed in one occupational group, 2024.',
           'They write the code, run the networks and fix the laptop.'],
    why='Estonia has the highest share at 27.6 per cent and Czechia the lowest at 13.0, so even at best fewer than three in ten of these jobs go to women. '
        'Board seats die on France at 19.3 and Norway at 21.3, both with legal quotas pushing that figure towards forty per cent. '
        'Doctors die on the ceiling, since women are most of the doctors in much of eastern Europe and nothing here passes 28. '
        'Pilots die on the floor: Czechia\u2019s 13 per cent would be several times any country\u2019s share of women in the cockpit.'),

'home-ownership': dict(
    diff=2, answer='Share of people living in a home their household owns',
    decoys=['Share of people with a mortgage', 'Share of households with a car',
            'Share of adults who are married', 'Share of adults who own a smartphone'],
    label=['Romania', 'Slovakia', 'Norway', 'Italy', 'France', 'Germany', 'Switzerland'],
    labelSm=['Romania', 'Germany', 'Switzerland'],
    hints=['The bottom two are among the richest countries on the chart; the top one is among the poorest in the EU.',
           'Romania at 94 cannot be counting mortgages, which few households there have, and Germany at 47 cannot be counting cars.',
           'A percentage of the whole population, by the household they live in, 2024.',
           'After 1990 many eastern European governments sold flats to the families living in them, for next to nothing.'],
    why='Romania is highest at 94.3 per cent and Switzerland lowest at 42.0, with Germany just above it at 47.2. '
        'Mortgages die on Romania, where few households borrow to buy and yet almost everyone is counted here. '
        'Car ownership dies on Germany, one of the most motorised countries in Europe and second from bottom. '
        'Marriage dies on the top of the chart, since no country has 94 per cent of its people married. '
        'The eastern lead dates from the 1990s, when state flats were sold cheaply to the people living in them.'),

'cheese-made-per-person': dict(
    diff=2, answer='Cheese made per resident',
    decoys=['Cheese eaten per resident', 'Pork produced per resident', 'Butter made per resident',
            'Milk drunk per resident'],
    label=['Denmark', 'Netherlands', 'Cyprus', 'France', 'Italy', 'Switzerland'],
    labelSm=['Denmark', 'France', 'Switzerland'],
    hints=['The largest figure belongs to a country of six million people, and the fourth largest to an island of about one.',
           'Spain, which keeps more pigs than any other EU country, is near the bottom, and the leader\u2019s figure is more than anyone could eat.',
           'Kilograms per resident in 2023, from what the country\u2019s dairies produced.',
           'Halloumi explains fourth place; Gouda and Edam explain second.'],
    why='Denmark makes 83.7 kilograms for every resident, while France, with its hundreds of named varieties, makes 27.9 and is ninth; Switzerland is fourteenth. '
        'Cheese eaten dies on Denmark itself, since no population eats anything like 84 kilograms of it a year. '
        'Pork dies on Spain, the EU\u2019s largest pig producer and near the bottom here at 11.1. '
        'Butter dies on the same Danish figure, several times what Denmark\u2019s dairies turn into butter.'),

'crude-death-rate': dict(
    diff=3, answer='Deaths each year per 1,000 people',
    decoys=['New cancer cases each year per 1,000 people', 'People emigrating each year per 1,000 people',
            'Marriages each year per 1,000 people', 'Immigrants arriving each year per 1,000 people'],
    label=['Bulgaria', 'Japan', 'Nigeria', 'Germany', 'Qatar'],
    labelSm=['Bulgaria', 'Japan', 'Qatar'],
    hints=['Japan and Nigeria sit almost side by side, for completely different reasons.',
           'Nigeria is near the top, which rules out anything that needs a rich country\u2019s hospitals to count it, and Japan\u2019s figure is far too high for anything to do with leaving.',
           'Per 1,000 people living in the country, over one year, 2023.',
           'Young populations score low on this even when they are poor, and old ones score high even when they are rich.'],
    why='Bulgaria is highest at 15.7 per 1,000, and Qatar and the United Arab Emirates lowest at 0.9, because most of their residents are young workers from abroad. '
        'Japan at 13.0 and Nigeria at 11.7 sit close together: one population is very old, the other faces high mortality at every age. '
        'New cancer cases die on Nigeria, where diagnosis is too scarce to produce a figure that high. '
        'Emigration dies on Japan, from which almost nobody leaves. '
        'Marriages die on Bulgaria at the top, a country with one of the lowest marriage rates in Europe.'),

'minimum-wage-to-median': dict(
    diff=4, answer='Minimum wage as a share of the median full-time wage',
    decoys=['Unemployment benefit as a share of the median full-time wage',
            'Average rent as a share of the median full-time wage',
            'Income tax paid as a share of the median full-time wage',
            'State pension as a share of the median full-time wage'],
    label=['Colombia', 'Costa Rica', 'Mexico', 'France', 'Germany', 'United States'],
    labelSm=['Colombia', 'France', 'United States'],
    hints=['The three highest figures are all in Latin America, and the lowest belongs to the largest economy on the chart.',
           'Colombia at 92 cannot be an income tax bill, and a country with little unemployment insurance cannot top a chart of it.',
           'A percentage of what the middle full-time earner is paid, 2024.',
           'It is the lowest rate an employer may legally pay, set against a typical wage.'],
    why='Colombia\u2019s legal floor is 92.3 per cent of the median full-time wage, so the minimum and the typical wage are almost the same thing, while the United States, whose federal rate has not risen since 2009, sits alone at 25.0. '
        'Unemployment benefit dies on Colombia, which pays very little of it and tops this chart. '
        'Rent dies on the same figure, since no country\u2019s renters hand over 92 per cent of a middle wage. '
        'Income tax dies there too: no worker pays 92 per cent of their wage in tax.'),

'adult-learning': dict(
    diff=3, answer='Share of adults who took part in education or training in the last four weeks',
    decoys=['Share of adults who hold a university degree', 'Share of adults who are out of work',
            'Share of adults who used the internet in the last four weeks',
            'Share of adults who did voluntary work in the last four weeks'],
    label=['Sweden', 'Denmark', 'Ireland', 'Germany', 'Greece', 'Bulgaria'],
    labelSm=['Sweden', 'Germany', 'Bulgaria'],
    hints=['The Nordic countries take the top three places, and Germany sits in the bottom third.',
           'Ireland, with more graduates for its size than almost anywhere in Europe, is only in the middle, and Greece, with some of the highest unemployment, is near the bottom.',
           'A percentage of people aged 25 to 64, asked about the previous four weeks, 2024.',
           'An evening class, a course at work or a language lesson all count; a degree finished years ago does not.'],
    why='Sweden leads at 37.5 per cent and Bulgaria trails at 1.8, a twentyfold gap in how many adults were being taught something in a given month. '
        'A degree dies on Ireland at 14.7, which has one of the most educated workforces in Europe. '
        'Being out of work dies on Greece at 4.4, near the bottom despite one of the highest jobless rates in the EU. '
        'Internet use dies on the top of the chart, since 37.5 per cent would be far too few for anywhere in Europe.'),

'aid-share-of-income': dict(
    diff=2, answer='Foreign aid given, as a share of national income',
    decoys=['Military spending, as a share of national income',
            'Spending on research, as a share of national income',
            'Spending on unemployment benefits, as a share of national income',
            'Public spending on culture, as a share of national income'],
    hints=['Norway and Luxembourg are level at the top, and Hungary is last.',
           'The United States and South Korea are near the bottom, which rules out anything about armies or laboratories.',
           'A percentage of gross national income in 2024, drawn against a 0.7% line.',
           'The line is a target the United Nations set in 1970, and most rich countries have never reached it.'],
    why='Norway gives 1.02 per cent of its national income and Luxembourg exactly 1; only Sweden and Denmark join them above the 0.7 per cent line, with Germany just short at 0.68. '
        'Military spending dies on the United States at 0.23, a country that spends about fifteen times that share on defence. '
        'Research dies on South Korea at 0.21, one of the heaviest research spenders in the world. '
        'Unemployment benefits die on Spain at 0.25, a country with long-standing high unemployment.'),

'greenhouse-gas-change-since-1990': dict(
    diff=3, answer='Greenhouse gas emissions compared with 1990',
    truth='Greenhouse gas emissions compared with 1990, 1990 \u2192 2023',
    decoys=['Energy used compared with 1990', 'Economic output compared with 1990',
            'Cars on the road compared with 1990', 'Population compared with 1990'],
    hints=['Every country at the bottom of this chart left the Soviet Union or the Warsaw Pact within two years of the starting date.',
           'Germany has roughly halved, yet its economy is far larger than in 1990, so this is not a measure of output or of how many cars are on the road.',
           'An index on which each country\u2019s 1990 figure is 100, measured in 2023.',
           'Carbon dioxide from burning fuel is most of it, with methane from farms and landfill much of the rest.'],
    why='Turkey stands at 242.5, more than doubled since 1990 as its economy and population grew, while Estonia is at 27.0, having cut the oil-shale power generation it inherited from the Soviet Union. '
        'Energy use dies on Germany at 53.4, where consumption has fallen by around a fifth, not by half. '
        'Economic output dies on the same German figure, since the economy is far bigger than in 1990. '
        'Cars on the road die on Latvia at 38.0, where car ownership has risen steeply since independence.'),
}
