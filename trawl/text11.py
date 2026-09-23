"""Text for build11.py, written from `build11.py --digest` (the final data)."""

TEXT = {
'early-school-leavers': dict(
    diff=3, answer='Share of 18 to 24 year olds who left school early and are not in training',
    decoys=['Share of 18 to 24 year olds who are unemployed', 'Share of 18 to 24 year olds who smoke',
            'Share of 18 to 24 year olds living with their parents',
            'Share of 18 to 24 year olds who are married'],
    hints=['Two small southern countries started this period with four young people in ten on the wrong side of it.',
           'Spain falls steadily through years when its youth unemployment doubled, and Germany is the one line that ends higher than it began.',
           'A percentage of everyone aged 18 to 24, 2004 to 2024.',
           'They finished at most the first years of secondary school and are no longer studying anything.'],
    why='Portugal falls from 39.3 per cent to 6.6 and Malta from 42.1 to 9.5, while Germany ends slightly higher than it began, at 13.5. '
        'Youth unemployment dies on Spain, whose line falls steadily from 32.2 to 13.0 through years when joblessness among the young more than doubled. '
        'Smoking dies on Germany, rising at the end when smoking among the young has fallen almost everywhere. '
        'Living with parents dies on the ceiling, since far more than 42 per cent of young adults in Malta and Portugal live at home.'),

'ten-year-bond-yields': dict(
    diff=3, answer='Interest rate on ten-year government bonds',
    decoys=['Central bank interest rate', 'Inflation rate', 'Government deficit as a share of GDP',
            'Growth in average wages'],
    hints=['One line climbs past twenty in a single year and is back below two within a decade.',
           'Greece, Portugal, Italy and Spain share a currency and a central bank, yet their lines split apart, and the Greek peak came in a year when prices there were barely rising.',
           'A percentage a year, the annual average, 2005 to 2024.',
           'It is what markets charged each government to borrow for a decade.'],
    why='Greece peaks at 22.5 per cent in 2012 and Portugal at 10.6, as markets priced in the chance of default, before the European Central Bank promised to stand behind the euro and brought them down. '
        'Hungary, outside the euro, ends highest at 6.5. '
        'A central bank\u2019s rate dies on the four euro countries, which share one and yet split apart. '
        'Inflation dies on Greece in 2012, when prices there were barely rising. '
        'The deficit dies on the same peak, since Greece was not borrowing 22 per cent of its economy that year.'),

'temporary-contracts': dict(
    diff=3, answer='Share of employees on temporary contracts',
    decoys=['Share of employees working from home', 'Share of employees earning the minimum wage',
            'Share of employees in public-sector jobs', 'Share of employees working night shifts'],
    hints=['One line holds steady for twelve years and then drops by more than a third in three.',
           'Nothing jumps in 2020, when office workers went home, and Germany already stood at 13 in 2009, six years before it had a legal minimum wage.',
           'A percentage of all employees aged 20 to 64, 2009 to 2024.',
           'A contract with an end date: seasonal, fixed-term or through an agency.'],
    why='Spain holds near a quarter for twelve years, then drops from 24.9 per cent in 2021 to 15.5 after a 2022 law restricted fixed-term hiring, leaving the Netherlands highest at 22.6. '
        'Working from home dies on 2020, when no line jumps. '
        'The minimum wage dies on Germany at 13.0 in 2009, six years before it had one. '
        'Public-sector jobs die on the Spanish fall, since Spain did not lose a third of its public servants in three years.'),

'objects-launched-into-space': dict(
    diff=2, answer='Objects launched into space each year',
    decoys=['Rocket launches each year', 'Satellites in orbit', 'Astronauts sent into space each year',
            'Airliners delivered each year'],
    hints=['One line spends two decades near the floor and then leaves the chart behind in about six years.',
           'The British line leaps to nearly three hundred in 2021 and falls back, which nothing that only accumulates could do, and no country launches ten rockets a day.',
           'A count per year, 2000 to 2025.',
           'Most of the American total is one company\u2019s broadband satellites, and the British spike is a rival network\u2019s.'],
    why='The United States goes from 56 in 2000 to 3,708 in 2025, most of them satellites for one company\u2019s broadband network, and the British spike to 289 in 2021 is a rival network registered there. '
        'Rocket launches die on the American figure, since no country flies ten rockets a day. '
        'Satellites in orbit die on the British line, which falls after 2021 when a running total cannot. '
        'Astronauts die on magnitude: fewer than a hundred people go to space in a year.'),

'older-workers-in-work': dict(
    diff=3, answer='Share of 55 to 64 year olds in work',
    decoys=['Share of 55 to 64 year olds with a university degree',
            'Share of 55 to 64 year olds who own their home',
            'Share of 55 to 64 year olds living alone',
            'Share of 55 to 64 year olds who are overweight'],
    hints=['Germany\u2019s line doubles over a quarter of a century and ends within touching distance of Sweden\u2019s.',
           'Sweden starts at 64, far above any share of that age group holding degrees, and Slovenia starts at 22, far below any share owning a home.',
           'A percentage of everyone aged 55 to 64, 2000 to 2024.',
           'Pension reforms raised the age at which people could stop, and people stopped later.'],
    why='Germany doubles from 37.4 per cent to 75.0 and Slovenia rises from 22.3 to 56.3 as pension ages rose across Europe, while Sweden, already at 64.3 in 2000, reaches 78.1. '
        'A degree dies on Sweden in 2000, since nothing like 64 per cent of that generation went to university. '
        'Home ownership dies on Slovenia at 22.3, a country where most people own their home. '
        'Living alone dies on Sweden\u2019s 78.1, far above any share of that age group living by themselves.'),

'divorce-rate': dict(
    diff=3, answer='Divorces each year per 1,000 residents',
    decoys=['Marriages each year per 1,000 residents', 'Emigrants each year per 1,000 residents',
            'Suicides each year per 1,000 residents', 'Civil partnerships each year per 1,000 residents'],
    hints=['One line begins at exactly zero, for a reason once written into a constitution.',
           'Ireland at zero in 1997 rules out anything that happens in every country every year, like weddings or people leaving, and Spain triples in under ten years.',
           'Per 1,000 residents, over a year, 1997 to 2017.',
           'Spain made it quicker in 2005, Italy in 2015, and Ireland made it possible at all in 1997.'],
    why='Ireland starts at zero in 1997, the year its first divorces were granted after a 1995 referendum, and Spain triples from 0.9 to 2.9 by 2006 after a 2005 law removed the need to separate first, while Lithuania and Czechia stay highest at around three. '
        'Marriages die on Ireland\u2019s zero, since Irish couples were marrying in 1997. '
        'Emigration dies there too, in a country people have never stopped leaving. '
        'Suicides die on magnitude: three per 1,000 would be far beyond the real rate anywhere.'),

'boys-born-per-100-girls': dict(
    diff=3, answer='Boys born for every 100 girls',
    decoys=['Men for every 100 women in the population', 'Children born for every 100 women',
            'Male smokers for every 100 female smokers', 'Men for every 100 women at university'],
    hints=['South Korea begins as the highest line and ends as the lowest.',
           'India sits below China, which rules out anything to do with how many children women have, and South Korea moves ten points, far too much for a whole population\u2019s balance of men and women.',
           'A ratio per 100, 1990 to 2023, drawn from a floor of 100.',
           'Nature\u2019s figure is about 105; everything above it on this chart was chosen.'],
    why='China peaks at 117.8 in 2004 and Azerbaijan at 116.8, against a natural figure of about 105, while South Korea falls from 115.7 in 1990 to 105.8 as the preference for sons faded. '
        'The population as a whole dies on the South Korean fall, far too fast for a whole country\u2019s balance of men and women. '
        'Children per woman die on India sitting below China, when Indian women have about twice as many. '
        'Male smokers die on magnitude, since men outnumber women among smokers many times over in all five.'),
}
