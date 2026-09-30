"""Text for build14.py, written from `build14.py --digest` (the final data)."""

TEXT = {
'nuclear-warheads': dict(
    diff=1, answer='Nuclear warheads held',
    decoys=['Tanks in service', 'Satellites in orbit', 'Military aircraft in service',
            'Submarines in service'],
    hints=['The line on the left begins at two, and both were used within a month.',
           'Every line but one is at zero in 1945, when tanks and warplanes already numbered in the tens of thousands, and nothing reached orbit until 1957.',
           'The number held each year, 1945 to 2025.',
           'Hiroshima and Nagasaki.'],
    why='Russia peaks at about 40,000 in 1986 and the United States at 31,255 in 1967, and both have cut their stockpiles by roughly nine tenths since the Cold War, while China, alone among the five, is still rising, to 600 in 2025. '
        'Tanks and warplanes die on 1945, when every line but one is at zero and both were counted in tens of thousands. '
        'Satellites die on the United States line starting at two in 1945, twelve years before anything reached orbit.'),

'farm-support': dict(
    diff=4, answer='Government support as a share of farm receipts',
    decoys=['Share of farm receipts from exports', 'Share of farm receipts from dairy',
            'Share of farm receipts from rice', 'Share of farm receipts spent on fertiliser'],
    hints=['In the mid-1980s one of these countries abolished almost all of it at a stroke, and its farmers stayed in business.',
           'New Zealand, which sends most of its butter and lamb abroad, ends near zero, and Norway, without a single paddy field, tops the chart.',
           'A percentage of gross farm receipts, 1986 to 2024.',
           'Paid by taxpayers and shoppers to keep farmers farming.'],
    why='Norway leads in every year but 1995, falling from 70.9 per cent in 1986 to 47.7, with South Korea and Japan close behind, while New Zealand drops from 19.4 to almost nothing after scrapping nearly all of its subsidies in the 1980s. '
        'Exports die on New Zealand at 1.6, when it sells most of what its farms produce abroad. '
        'Dairy dies on the same figure, since milk is New Zealand\u2019s largest farm product. '
        'Rice dies on Norway at the top, which grows none.'),

'asylum-applications-per-thousand': dict(
    diff=2, answer='First-time asylum applications per 1,000 residents',
    decoys=['Births per 1,000 residents', 'Deaths per 1,000 residents',
            'Marriages per 1,000 residents', 'Divorces per 1,000 residents'],
    hints=['One line spikes in 2015 and collapses once a fence goes up along a southern border.',
           'Hungary falls to almost nothing from 2019, which no count of births, deaths or weddings could do in a country of ten million.',
           'Per 1,000 residents each year, 2014 to 2024, counting each person once.',
           'Seeking protection.'],
    why='Hungary peaks at 17.8 per 1,000 residents in 2015, when the route through the Balkans crossed it, and falls to almost nothing once it fenced its border and moved applications to its embassies abroad; Sweden peaks at 16.0 the same year. '
        'Cyprus climbs to 23.2 in 2022, the highest on the chart, as arrivals crossed the line dividing the island, and Spain climbs to 3.4. '
        'Births, deaths and marriages all die on Hungary\u2019s run of near-zeros, since no country of ten million stops being born, dying or marrying.'),

'hiv-prevalence': dict(
    diff=4, answer='HIV prevalence among adults',
    decoys=['Share of adults with diabetes', 'Share of adults with tuberculosis',
            'Share of adults without electricity at home', 'Share of adults who smoke'],
    hints=['In the small kingdom at the top, a generation of grandparents raised their grandchildren.',
           'Eswatini stays above a fifth of all adults for 25 years, far beyond any rate of diabetes or tuberculosis, and Kenya ends at 3.0, though about a quarter of Kenyans still have no power at home.',
           'A percentage of people aged 15 to 49, 2000 to 2024.',
           'A virus first identified in the early 1980s.'],
    why='Eswatini peaks at 29.4 per cent in 2014 and is still at 23.4 in 2024, the highest in the world, while Zimbabwe falls from 25.8 to 9.8 and Kenya from 8.8 to 3.0. '
        'South Africa rises until 2016 because treatment keeps people alive, so fewer leave the count even as new infections fall. '
        'Diabetes and tuberculosis die on the scale, since neither reaches anything like a fifth of adults anywhere. '
        'Electricity dies on Kenya at 3.0, when about a quarter of Kenyans still live without it.'),

'fibre-broadband-share': dict(
    diff=3, answer='Share of fixed broadband connections that are fibre',
    decoys=['Share of households with a broadband connection', 'Share of mobile connections on 5G',
            'Share of people who use the internet every day', 'Share of households with cable TV'],
    hints=['Spain\u2019s line rises through a decade in which its old telephone monopoly dug up nearly every street in the country.',
           'Japan starts at 58, nine years before the first 5G network opened, and Spain starts near zero when most Spanish homes were already online.',
           'A percentage of all fixed broadband subscriptions, 2010 to 2024.',
           'Light, not copper.'],
    why='South Korea ends highest at 90.5 per cent and Spain rises from 0.5 to 89.3, passing Japan, which leads for years from 58.1 and ends at 79.2, while Germany, still largely on copper telephone lines, ends at 13.7 and Britain at 30.4. '
        'Household broadband dies on Spain near zero in 2010, when most Spanish homes were already connected. '
        '5G dies on Japan at 58.1 in 2010, nine years before any 5G network opened. '
        'Daily internet use dies on the same Spanish start.'),

'sheep-kept': dict(
    diff=3, answer='Sheep kept',
    decoys=['Pigs kept', 'Cattle kept', 'Horses kept', 'Dairy cows kept'],
    hints=['Across the Spanish meseta the old droving roads carry fewer animals every year.',
           'Spain\u2019s line falls by more than a third while its pig herd became the largest in the EU, and France, which keeps more cattle than any other EU country, ends below Spain and Romania.',
           'Thousands of animals counted at the end of each year, 1995 to 2024.',
           'Wool, lamb and a great deal of feta.'],
    why='Spain peaks at 24.8 million in 1997 and falls to 13.5 million, while Romania is the only country here to end at its highest, 10.4 million in 2024, and Ireland ends lowest at 3.6 million. '
        'Pigs die on Spain\u2019s falling line, when its pig herd grew to the largest in the EU, and on Greece at 7.8 million, where pigs number well under a million. '
        'Cattle die on France ending below Spain and Romania, when France keeps more cattle than any other EU country. '
        'Horses die on the scale, since no EU country keeps ten million.'),

'cereal-yield': dict(
    diff=4, answer='Cereal yield per hectare',
    decoys=['Wheat yield per hectare', 'Potato yield per hectare', 'Fertiliser used per hectare',
            'Sugar cane yield per hectare'],
    hints=['Egypt\u2019s line rides on the Nile\u2019s silt and on water that never depends on rain.',
           'The United States ends above France, though American wheat fields yield about half as much as French ones, and nothing climbs past nine, far below any harvest of potatoes.',
           'Tonnes per hectare, 1961 to 2022.',
           'Grain harvested from each patch of field.'],
    why='The United States rises from 2.5 to 8.1 tonnes a hectare, mostly on maize, and Egypt, irrigated from the Nile, beats it for much of the period, while China quintuples from 1.2 to 6.4 and India ends lowest at 3.6. '
        'Wheat dies on the United States ending above France, when American wheat yields are about half of French ones. '
        'Potatoes die on the scale, since a field of potatoes yields several times nine tonnes. '
        'Fertiliser dies on the same scale, since it is spread in kilograms per hectare, not tonnes.'),
}
