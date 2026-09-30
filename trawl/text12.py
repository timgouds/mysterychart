"""Text for build12.py, written from `build12.py --digest` (the final data)."""

TEXT = {
'palm-oil-produced': dict(
    diff=1, answer='Palm oil produced',
    decoys=['Natural rubber produced', 'Cocoa beans produced', 'Coffee produced', 'Bananas grown'],
    hints=['Two neighbours facing each other across the Strait of Malacca fill most of this square, much of it on land that was rainforest within living memory.',
           'Brazil, which grows more coffee than anyone, is ninth, and C\u00f4te d\u2019Ivoire, the great cocoa grower, is tenth.',
           'Thousand tonnes produced in 2023, the twelve largest producers.',
           'It is in about half the packaged goods in a supermarket, from biscuits to shampoo, and it is pressed from the fruit of a tree.'],
    why='Indonesia produces 47.1 million tonnes, two and a half times Malaysia, and the two together make up 86% of the square. '
        'No country harvests anything like 47 million tonnes of rubber, cocoa or coffee, and the order kills them too. '
        'Rubber dies on Thailand, the world\u2019s largest grower of it, in a distant third. '
        'Cocoa dies on C\u00f4te d\u2019Ivoire in tenth place and coffee on Brazil in ninth, each the largest grower of its crop on earth.'),

'avocados-grown': dict(
    diff=2, answer='Avocados grown',
    decoys=['Coffee grown', 'Cocoa grown', 'Mangoes grown', 'Pineapples grown'],
    hints=['A fruit that will not ripen until it has been picked.',
           'Brazil and Vietnam, the two largest coffee growers in the world, sit well down the order, and India is nowhere.',
           'Thousand tonnes harvested in 2023, the twelve largest growers.',
           'Most of the largest block is trucked north across the border and mashed with lime and salt.'],
    why='Mexico grows 3 million tonnes, nearly three times Colombia, and most of it is sold north of the border. '
        'Coffee dies on Brazil in seventh place and Vietnam in tenth, the two largest coffee growers on earth. '
        'Cocoa dies because C\u00f4te d\u2019Ivoire and Ghana are absent, the two largest growers of it. '
        'Mangoes die on the absence of India, which grows more of them than the rest of the world put together.'),

'goats-kept': dict(
    diff=2, answer='Goats kept',
    decoys=['Sheep kept', 'Cattle kept', 'Pigs kept', 'Horses kept'],
    hints=['Much of the largest block lives on hillsides too steep and dry for anything heavier.',
           'Ireland is nowhere, for all its flocks, and Germany, which keeps one of Europe\u2019s largest cattle herds, is ninth.',
           'Thousands of animals counted at the end of 2024, the twelve largest herds in the EU.',
           'Feta may be up to 30% their milk, and the Netherlands keeps most of its herd indoors to make cheese.'],
    why='Greece keeps 2.6 million and Spain 2.4 million, nearly half of everything on the chart between them. '
        'Sheep die on the absence of Ireland, and on Greece ahead of Spain, when Spain keeps far more sheep than Greece does. '
        'Cattle die on Germany in ninth place, and pigs on the absence of Denmark, which keeps one of the EU\u2019s largest pig herds. '
        'The Netherlands is sixth because its goats are dairy animals, kept in barns for their milk.'),

'soya-grown': dict(
    diff=3, answer='Soya beans grown',
    decoys=['Rice grown', 'Sunflower seed grown', 'Rapeseed grown', 'Grain maize grown'],
    hints=['Most of the largest block comes from the flat, irrigated valley of a single river.',
           'Spain, the EU\u2019s second-largest rice grower, is last, and Germany, one of its two great rapeseed growers, is only eighth.',
           'Thousand tonnes harvested in 2024, the twelve largest growers in the EU, and the whole square is small beside what the Americas grow.',
           'It is the bean behind tofu and most animal feed, and Europe imports far more of it than it grows.'],
    why='Italy grows 1.13 million tonnes, nearly three times France and more than a third of the square, most of it in the Po valley. '
        'Rice dies on Spain in last place, the EU\u2019s second-largest rice grower, and on the absence of Greece. '
        'Sunflower seed dies on the absence of Bulgaria, one of the two largest sunflower growers in the EU. '
        'Rapeseed dies on Germany in eighth, when only France grows more of it in the EU.'),

'hemp-grown': dict(
    diff=2, answer='Hemp grown',
    decoys=['Flax grown for fibre', 'Hops grown', 'Tobacco grown', 'Sugar beet grown'],
    hints=['A tall crop cut in late summer, its stalks left to rot in the field and its seeds pressed for oil.',
           'Belgium is absent though it is one of Europe\u2019s largest flax growers, and the Netherlands is a clear second.',
           'Thousand tonnes harvested in 2024, from every EU country that grows any.',
           'The Dutch crop is entirely legal, bred for fibre and seed with almost none of the compound that made the plant notorious.'],
    why='France grows 144 thousand tonnes, nearly six times the Netherlands and more than three quarters of everything here, most of it in Champagne for insulation, paper and animal bedding. '
        'The Dutch crop in second place is industrial, grown for fibre and seed. '
        'Flax dies on the absence of Belgium, and hops on the absence of Germany, which grows most of the EU\u2019s. '
        'Tobacco dies on France in first place, which grows a fraction of Italy\u2019s tobacco, and on Italy, the EU\u2019s largest tobacco grower, down in fourth.'),

'kiwis-grown': dict(
    diff=1, answer='Kiwifruit grown',
    decoys=['Lemons grown', 'Peaches and nectarines grown', 'Oranges grown', 'Figs grown'],
    hints=['Its vines climb pergolas south of Rome and across the plains of northern Greece, and it reached both only in the 1970s.',
           'Spain, which grows more citrus and stone fruit than any other country in Europe, is only fifth.',
           'Thousand tonnes harvested in 2024, every EU country that grows any.',
           'It was sold as the Chinese gooseberry until exporters on the far side of the world renamed it after a flightless bird.'],
    why='Italy grows 464 thousand tonnes and Greece 342, together more than nine tenths of the EU crop. '
        'Lemons, oranges and peaches all die on Spain in fifth place, the EU\u2019s largest grower of each. '
        'The fruit is named after a bird from the other side of the world, and the EU grows most of its crop in two Mediterranean countries.'),

'blackcurrants-grown': dict(
    diff=2, answer='Blackcurrants grown',
    decoys=['Raspberries grown', 'Strawberries grown', 'Apples grown', 'Cherries grown'],
    hints=['A bush fruit too sharp to eat raw, banned for much of the last century in parts of North America because it spreads a disease of pine trees.',
           'Spain and Portugal, which grow most of Europe\u2019s soft summer berries, are absent, and Greece barely registers.',
           'Thousand tonnes harvested in 2024, the largest growers in the EU.',
           'Its French name is cassis, and Burgundy turns part of the second circle into a liqueur.'],
    why='Poland grows 67.9 thousand tonnes, eight times France and about three quarters of the EU crop. '
        'Raspberries die on the absence of Portugal and Spain, the EU\u2019s second and third growers of them. '
        'Strawberries die on the absence of Spain, which grows more of them than any other EU country. '
        'Apples die on the absence of Italy, and on Poland\u2019s figure, a sliver of the millions of tonnes of apples it picks each year.'),

'mushrooms-grown': dict(
    diff=3, answer='Mushrooms grown',
    decoys=['Apples grown', 'Tomatoes grown', 'Potatoes grown', 'Cabbages grown'],
    hints=['Parisian growers once farmed it in the old quarries beneath the city, and one variety still carries the capital\u2019s name.',
           'Italy, Europe\u2019s orchard and tomato field, is only eighth, Germany, its great potato grower, fifth, and Ireland sixth.',
           'Thousand tonnes harvested in 2024, the twelve largest growers in the EU.',
           'Ireland\u2019s crop is almost all white button caps, and most of it is sold across the Irish Sea.'],
    why='Poland grows 255 thousand tonnes, ahead of the Netherlands and Spain, and exports much of it. '
        'Apples die on Italy in eighth place, the EU\u2019s second-largest apple grower, and tomatoes on Italy too, which grows more tomatoes than any other EU country. '
        'Potatoes die on Germany in fifth, the EU\u2019s largest potato grower. '
        'All three die on Ireland in sixth, a country that grows little of any of them.'),

'motorway-length': dict(
    diff=2, answer='Length of motorway',
    decoys=['Length of railway line', 'Length of coastline', 'Length of navigable waterway',
            'Length of cycle path'],
    hints=['Much of the longest network was built in the 1990s and 2000s, with a good deal of the money coming from Brussels.',
           'Spain comes first, ahead of Germany, which has about twice as much railway, and Greece, with thousands of kilometres of shoreline, is ninth.',
           'Kilometres in 2023, the twelve longest networks among the countries Eurostat reports.',
           'The Autobahn is the famous one; the Spanish autov\u00edas are longer.'],
    why='Spain has 15,892 km, more than Germany\u2019s 13,210, most of it dual carriageway built since the late 1980s. '
        'Railway dies on the order, since Germany has about twice Spain\u2019s track and would lead by a distance. '
        'Coastline dies on Greece in ninth, which has the longest coast in the EU. '
        'Waterways die on the Netherlands in eighth, a country laced with more navigable canal and river than almost anywhere in Europe.'),

'caesarean-births': dict(
    diff=3, answer='Share of babies delivered by caesarean section',
    decoys=['Share of babies born to mothers over 35', 'Share of babies born to unmarried parents',
            'Share of babies born before term', 'Share of babies born in hospital'],
    hints=['In several of the countries at the top, it is common for the date of a birth to be chosen in advance.',
           'Iceland, where most babies are born to unmarried parents, is last, and Turkey, where mothers are young, is near the top.',
           'Per cent of live births in 2023, every country reporting to the OECD, so South Korea\u2019s dot means nearly two in three.',
           'The operation is named, probably wrongly, after Julius Caesar.'],
    label=['South Korea', 'Turkey', 'Greece', 'Mexico', 'United Kingdom', 'France', 'Netherlands', 'Iceland'],
    labelSm=['South Korea', 'Turkey', 'Iceland'],
    why='South Korea delivers 64% of babies this way, Cyprus 62% and Turkey 61.5%, against 14% in Iceland and 16% in the Netherlands and Israel, where midwives lead most births. '
        'Mothers over 35 die on Turkey near the top, where mothers are among the youngest in the OECD. '
        'Unmarried parents die on Iceland at the bottom, where more than two thirds of babies are born outside marriage. '
        'Premature births die on magnitude: no country\u2019s rate is much above one in eight, and more than half of this chart sits above 30%.'),

'no-foreign-language': dict(
    diff=3, answer='Share of adults who speak no foreign language',
    decoys=['Share of adults who have never used the internet', 'Share of adults who never finished secondary school',
            'Share of adults who live alone', 'Share of adults who smoke every day'],
    hints=['Most of the lowest dots belong to small countries with large neighbours.',
           'Ireland, one of the richest countries here, is sixth from the top, just behind Spain.',
           'Per cent of 25 to 64 year olds in 2022, from a survey asked every five or six years.',
           'Ireland\u2019s figure is high because its people already speak the language the rest of Europe learns.'],
    label=['Bulgaria', 'Hungary', 'Spain', 'Ireland', 'France', 'Germany', 'Sweden', 'Norway'],
    labelSm=['Hungary', 'Ireland', 'Norway'],
    why='Half of all adults in Bulgaria, Hungary and Romania speak no language but their own, against about 4% in Sweden and Slovenia and under 2% in Norway. '
        'Never using the internet dies on Ireland and Spain near the top, both almost entirely online. '
        'Unfinished schooling dies on Ireland again and on Hungary in second place, where only about one adult in eight left school early. '
        'Living alone dies on Norway at the bottom, where it is more common than almost anywhere in Europe.'),

'overcrowded-homes': dict(
    diff=3, answer='Share of people living in an overcrowded home',
    decoys=['Share of people who cannot afford to heat their home', 'Share of young adults living with their parents',
            'Share of people living in a flat', 'Share of people who rent their home'],
    hints=['Many of the highest dots belong to countries where blocks of flats were put up quickly in the 1960s and 1970s and handed out by the state.',
           'Sweden sits above Spain and Portugal, and Cyprus is at the very bottom.',
           'Per cent of the population in 2024, every country in the EU\u2019s household survey and some of its neighbours.',
           'It counts households with fewer rooms than a simple rule allows: one for a couple, one for each other adult, one for every two children.'],
    label=['Montenegro', 'Romania', 'Latvia', 'Poland', 'Italy', 'Sweden', 'Spain', 'Cyprus'],
    labelSm=['Romania', 'Sweden', 'Cyprus'],
    why='Montenegro, Serbia and Romania top the chart at 41 to 53%, where large households share flats built for small ones, while Cyprus, Malta and the Netherlands sit under 5%. '
        'Unaffordable heating dies on Cyprus at the bottom and Portugal low in the order, both among the worst in Europe for cold homes. '
        'Living with parents dies on Spain at 9%, where most people in their late twenties still do. '
        'Flats die on Spain too, where about two people in three live in one.'),

'businesses-using-ai': dict(
    diff=3, answer='Share of businesses using artificial intelligence',
    decoys=['Share of businesses with a website', 'Share of businesses selling online',
            'Share of businesses using robots', 'Share of businesses using 3D printing'],
    hints=['Eurostat has asked this only since 2021, and in most countries the answer has at least doubled since.',
           'Ireland, where more businesses sell online than anywhere else in the EU, is only fifteenth, and Romania\u2019s figure is barely one in twenty.',
           'Per cent of businesses with ten or more staff in 2025, outside farming and finance.',
           'It counts firms using any of chatbots, text generation, image or speech recognition, or machine learning.'],
    label=['Denmark', 'Finland', 'Belgium', 'Germany', 'Ireland', 'Italy', 'Poland', 'Romania'],
    labelSm=['Denmark', 'Ireland', 'Romania'],
    why='Denmark leads at 42%, with Finland, Sweden and the Benelux close behind, while Romania trails at 5%. '
        'A website dies on Romania, since about three quarters of European firms have one. '
        'Selling online dies on Ireland in fifteenth, the EU\u2019s leader in e-commerce. '
        'Robots die on Denmark at 42%, far above the share of firms in any country that use them.'),

'real-household-income-change': dict(
    diff=3, answer='Change in household income per person, after inflation',
    decoys=['Change in population', 'Change in house prices', 'Change in life expectancy',
            'Change in the number of people in work'],
    hints=['Greece is the only country still short of where it started, fifteen years on from a bailout that cut a quarter from its economy.',
           'Romania, Lithuania and Latvia, which have all lost people since 2010, are near the top.',
           'An index with 2010 set at 100, adjusted for prices and measured per person, for every EU country with data.',
           'It measures what households can spend after taxes and benefits, plus the public services they receive, once inflation is taken out.'],
    why='Romanian households are 81% better off per person than in 2010, with Malta, Hungary and Poland not far behind, while Italy is barely ahead at 101 and Greece is still 4% below. '
        'Population dies on Romania, Lithuania and Latvia near the top, all of which have shrunk since 2010. '
        'House prices die on Luxembourg and Ireland in the lower half, two of the steepest property booms in Europe. '
        'Life expectancy dies on magnitude: nowhere has it moved more than a few per cent in fifteen years, and Romania here is up 81%.'),

'births-change-since-2014': dict(
    diff=4, answer='Change in the number of babies born',
    decoys=['Change in population', 'Change in the number of deaths', 'Change in the number of people over 65',
            'Change in the number of doctors'],
    hints=['The small countries at the top all grew fast over the decade, largely by bringing people in from abroad.',
           'Ireland, whose population has grown by about a seventh since 2014, sits 21 points below the line, and almost every bar points the same way.',
           'An index with 2014 set at 100, counting events in each calendar year, for most of the EU.',
           'Latvia now records three fifths as many as a decade earlier, and maternity wards have closed across the Baltic states and Poland.'],
    why='Latvia has 41% fewer than in 2014, Lithuania 35% and Poland 33%, while only Luxembourg, Cyprus, Malta, Portugal and Denmark are at or above where they were. '
        'Population dies on Ireland, which has grown by about a seventh and still sits 21 points down. '
        'Deaths and the number of over-65s both rose almost everywhere over the decade, so both die on nearly every bar falling below the line.'),
}
