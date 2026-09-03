  /* ============================ THE PUZZLES ============================ */

  var ALCOHOL = [["Afghanistan",0.011],["Albania",4.47],["Algeria",0.54],["Andorra",9.68],["Angola",4.13],["Antigua and Barbuda",6.66],["Argentina",8.05],["Armenia",4.28],["Australia",10.29],["Austria",11.51],["Azerbaijan",2.49],["Bahamas",3.65],["Bahrain",1.25],["Bangladesh",0.092],["Barbados",8.22],["Belarus",11.63],["Belgium",9.43],["Belize",3.67],["Benin",8.83],["Bhutan",0.18],["Bolivia",3.59],["Bosnia and Herzegovina",5.87],["Botswana",7.27],["Brazil",7.7],["Brunei",0.51],["Bulgaria",11.62],["Burkina Faso",11.27],["Burundi",4.16],["Cambodia",6.67],["Cameroon",9.6],["Canada",9.89],["Cape Verde",6.01],["Central African Republic",1.75],["Chad",2.91],["Chile",7.56],["China",4.58],["Colombia",4.24],["Comoros",0.23],["Congo",6.05],["Costa Rica",3.4],["Cote d'Ivoire",2.85],["Croatia",7.65],["Cuba",5.38],["Cyprus",6.36],["Czechia",11.99],["Democratic Republic of Congo",1.92],["Denmark",9.49],["Djibouti",0.38],["Dominica",5.02],["Dominican Republic",6.5],["East Timor",0.17],["Ecuador",2.54],["Egypt",0.13],["El Salvador",3.15],["Equatorial Guinea",6.56],["Eritrea",1.07],["Estonia",10.68],["Eswatini",6.79],["Ethiopia",3.06],["Fiji",3.58],["Finland",9.08],["France",10.32],["Gabon",8.14],["Gambia",0.61],["Georgia",14.41],["Germany",11.84],["Ghana",4.26],["Greece",5.81],["Grenada",7.33],["Guatemala",1.54],["Guinea",0.52],["Guinea-Bissau",3.73],["Guyana",5.04],["Haiti",3.11],["Honduras",3.08],["Hungary",9.93],["Iceland",7.94],["India",4.1],["Indonesia",0.074],["Iran",0.51],["Iraq",0.24],["Ireland",10.77],["Israel",2.84],["Italy",6.97],["Jamaica",3.1],["Japan",6.38],["Jordan",0.23],["Kazakhstan",4.52],["Kenya",2.47],["Kiribati",0.72],["Kuwait",0],["Kyrgyzstan",3.63],["Laos",10.82],["Latvia",12.87],["Lebanon",1.26],["Lesotho",4.3],["Liberia",2.86],["Libya",0.012],["Lithuania",12.1],["Luxembourg",10.82],["Madagascar",0.99],["Malawi",3.61],["Malaysia",0.74],["Maldives",1.49],["Mali",5.32],["Malta",7.11],["Mauritania",0],["Mauritius",6.86],["Mexico",4.79],["Micronesia",2.02],["Moldova",11.08],["Mongolia",7.68],["Montenegro",10.34],["Morocco",0.5],["Mozambique",1.89],["Myanmar",1.93],["Namibia",5.05],["Nauru",2.79],["Nepal",1.06],["Netherlands",8.71],["New Zealand",10.02],["Nicaragua",3.67],["Niger",0.13],["Nigeria",3.78],["North Korea",3.87],["North Macedonia",4.36],["Norway",7.38],["Oman",0.51],["Pakistan",0.084],["Panama",4.66],["Papua New Guinea",1.13],["Paraguay",5.62],["Peru",6.45],["Philippines",5.66],["Poland",11.66],["Portugal",8.88],["Qatar",1.05],["Romania",16.8],["Russia",10.53],["Rwanda",2.87],["Saint Kitts and Nevis",4.69],["Saint Lucia",9.28],["Saint Vincent",5.62],["Samoa",2.35],["Sao Tome and Principe",4.79],["Saudi Arabia",0],["Senegal",0.38],["Serbia",7.89],["Seychelles",10.19],["Sierra Leone",0.29],["Singapore",1.81],["Slovakia",10.67],["Slovenia",10.41],["Solomon Islands",1.45],["Somalia",0],["South Africa",7.13],["South Korea",7.79],["Spain",9.16],["Sri Lanka",2.91],["Sudan",0.01],["Suriname",5.93],["Sweden",9.57],["Switzerland",10.07],["Syria",0.092],["Tajikistan",0.74],["Tanzania",10.95],["Thailand",7.99],["Togo",1.44],["Tonga",0.36],["Trinidad and Tobago",6.03],["Tunisia",1.71],["Turkey",1.69],["Turkmenistan",2.62],["Tuvalu",1.26],["Uganda",11.3],["Ukraine",9.24],["United Arab Emirates",2.08],["United Kingdom",10.73],["United States",9.9],["Uruguay",5.61],["Uzbekistan",2.1],["Vanuatu",2.04],["Venezuela",1.99],["Vietnam",8.04],["Yemen",0.044],["Zambia",3.62],["Zimbabwe",2.67]];

  var PUZZLES = [
    {
      family: "Part-to-whole",
      form: "Treemap · share of world total",
      exhibit: "Exhibit A",
      type: "treemap", diff: 2,
      truth: "Cocoa bean production, 2024", period: "2024",
      unit: "tonnes",
      total: 5223191,
      data: [
        ["Côte d'Ivoire",1890442], ["Indonesia",632702], ["Ghana",530000],
        ["Rest of world",480159], ["Ecuador",403699], ["Nigeria",350000],
        ["Cameroon",320000], ["Brazil",297509], ["Peru",157253],
        ["Sierra Leone",93750], ["Colombia",67678]
      ],
      answer: "Cocoa bean production, 2024",
      decoys: [
        "Coffee production, 2024",
        "Palm oil production, 2024",
        "Cashew nut production, 2024",
        "Natural rubber production, 2024",
        "Tea production, 2024",
        "Pineapple production, 2024",
        "Yam production, 2024"
      ],
      hints: [
        "Two neighbours on the Gulf of Guinea between them fill nearly half this square.",
        "It grows only near the equator, yet the countries that consume the most of it are cold, rich and northern.",
        "Measured in tonnes. The largest block alone is more than a third of the world's supply.",
        "It leaves the farm as a bitter bean and reaches you as a sweet bar."
      ],
      why: "Côte d'Ivoire and Ghana together are 46% of world production, a concentration with no parallel in coffee, where Brazil and Vietnam lead and West Africa barely features.",
      slug: "cocoa-bean-production"
    },
    {
      family: "Ranking",
      form: "Rank slope · 1990 → 2024",
      exhibit: "Exhibit B",
      type: "slope", diff: 3,
      truth: "World ranking of coffee-producing countries, 1990 vs 2024", period: "1990 → 2024",
      unit: "rank by tonnes of green coffee",
      leftYear: 1990, rightYear: 2024,
      ranks: [
        ["Brazil", 1, 1], ["Colombia", 2, 3], ["Mexico", 3, 12],
        ["Indonesia", 4, 4], ["Côte d'Ivoire", 5, 17], ["Uganda", 10, 6],
        ["Honduras", 12, 10], ["Vietnam", 17, 2], ["Peru", 19, 8]
      ],
      answer: "World ranking of coffee-producing countries",
      decoys: [
        "World ranking of tea-growing countries",
        "World ranking of cocoa-producing countries",
        "World ranking of sugarcane-growing countries",
        "World ranking of banana-growing countries",
        "World ranking of tobacco-growing countries",
        "World ranking of palm-oil-producing countries",
        "World ranking of rice-growing countries"
      ],
      hints: [
        "The line that climbs fifteen places belongs to a country the world still associated with a war rather than with farming.",
        "Two of the fallers are in Latin America; the steepest faller is in West Africa, which switched to a more profitable bean.",
        "Ranked by tonnes, green and unroasted, before the step that makes it smell like itself.",
        "Brazil has held first place on this list for over 150 years."
      ],
      why: "Vietnam went from 17th to 2nd after the Doi Moi reforms, a rise with no equivalent in tea, sugar or cocoa. Côte d'Ivoire's fall from 5th to 17th is the mirror image: it moved its land into cocoa, where it now leads the world.",
      slug: "coffee-bean-production"
    },
    {
      family: "Change over time",
      form: "Dumbbell · 1970 → 2023",
      exhibit: "Exhibit C",
      type: "dumbbell", diff: 3,
      truth: "Average number of children born per woman, 1970 vs 2023", period: "1970 → 2023",
      unit: "births per woman over a lifetime",
      leftYear: 1970, rightYear: 2023,
      data: [
        ["South Korea", 4.459, 0.72], ["China", 6.085, 0.999], ["Thailand", 5.452, 1.212],
        ["Brazil", 4.934, 1.619], ["Turkey", 5.775, 1.625], ["Iran", 6.798, 1.695],
        ["Mexico", 6.529, 1.91], ["India", 5.624, 1.975], ["Bangladesh", 6.839, 2.163],
        ["Kenya", 7.943, 3.208], ["Nigeria", 6.466, 4.482], ["Niger", 7.514, 6.061]
      ],
      answer: "Average number of children born per woman",
      decoys: [
        "Average number of people living in one household",
        "Average number of years spent in school",
        "Annual deaths per 1,000 people",
        "Average number of rooms in a home",
        "Average hours of unpaid housework a day",
        "Doctors per 10,000 people",
        "Average number of farm animals kept per household"
      ],
      hints: [
        "Only one country here has barely moved in half a century, and it sits in the Sahel.",
        "The country at the very top of the list is now spending billions trying to push its figure back up.",
        "2.1 is the number demographers watch for. Most of this list is now beneath it.",
        "It is counted per woman, across a whole lifetime."
      ],
      why: "South Korea's 0.72 is the lowest national figure ever recorded, and Niger's 6.06 barely moved, a spread no other indicator produces. Household size never falls below about 2, and school years rose over this period rather than falling.",
      slug: "children-per-woman-un"
    },
    {
      family: "Change over time",
      form: "Multi-line · 1970–2024",
      exhibit: "Exhibit D",
      type: "line", diff: 4,
      truth: "Share of children who die before their fifth birthday, 1970–2024", period: "1970–2024",
      unit: "% of live births",
      startYear: 1970,
      series: [
        { name: "Nigeria", values: [38.74,27.63,26.8,25.98,25.15,24.33,23.58,22.88,22.26,21.71,21.29,20.97,20.77,20.67,20.66,20.69,20.75,20.8,20.82,20.8,20.76,20.67,20.57,20.46,20.31,20.1,19.81,19.43,18.94,18.36,17.73,17.05,16.39,15.74,15.14,14.58,14.09,13.65,13.25,12.92,12.63,12.38,12.16,11.99,11.87,11.78,11.74,11.72,11.72,11.74,11.74,11.76,11.75,11.68,11.56] },
        { name: "India", values: [21.44,21.14,20.82,20.45,20.06,19.61,19.13,18.61,18.07,17.52,16.98,16.46,15.98,15.52,15.1,14.68,14.28,13.88,13.48,13.09,12.7,12.34,11.99,11.65,11.31,10.97,10.62,10.27,9.91,9.54,9.18,8.81,8.46,8.11,7.77,7.43,7.1,6.78,6.45,6.12,5.81,5.5,5.2,4.91,4.64,4.37,4.13,3.9,3.69,3.49,3.3,3.12,2.95,2.8,2.66] },
        { name: "Brazil", values: [13.21,12.89,12.56,12.23,11.89,11.54,11.18,10.8,10.41,10,9.58,9.15,8.73,8.33,7.98,7.65,7.36,7.09,6.81,6.55,6.28,6.01,5.71,5.39,5.08,4.77,4.47,4.19,3.93,3.68,3.44,3.22,3.01,2.82,2.63,2.46,2.31,2.17,2.05,1.95,1.86,1.79,1.72,1.67,1.63,1.6,1.68,1.54,1.52,1.5,1.49,1.47,1.46,1.44,1.42] },
        { name: "China", values: [11.21,10.63,10.08,9.52,8.97,8.43,7.91,7.42,6.98,6.59,6.26,5.99,5.77,5.61,5.49,5.42,5.39,5.38,5.39,5.38,5.36,5.3,5.21,5.08,4.92,4.74,4.55,4.35,4.14,3.91,3.66,3.41,3.14,2.88,2.63,2.4,2.19,2.01,1.85,1.71,1.57,1.46,1.35,1.25,1.16,1.07,1,0.93,0.86,0.8,0.75,0.7,0.66,0.61,0.57] },
        { name: "South Korea", values: [6.14,5.72,5.37,5.08,4.83,4.62,4.42,4.24,4.04,3.85,3.63,3.4,3.16,2.93,2.69,2.46,2.24,2.05,1.87,1.71,1.57,1.45,1.33,1.23,1.14,1.05,0.98,0.91,0.85,0.8,0.76,0.72,0.68,0.64,0.6,0.56,0.52,0.48,0.45,0.43,0.41,0.4,0.38,0.37,0.36,0.35,0.34,0.33,0.32,0.31,0.31,0.3,0.29,0.29,0.28] }
      ],
      answer: "Share of children who die before their fifth birthday",
      decoys: [
        "Share of the population living in extreme poverty",
        "Share of the population without access to electricity",
        "Share of adults who cannot read or write",
        "Share of children not in primary school",
        "Share of the population who are undernourished",
        "Share of births without a trained midwife or doctor",
        "Share of the population without clean drinking water"
      ],
      hints: [
        "The cliff at the far left is a war ending, not a policy working.",
        "One line flattens for two decades while the others keep falling. Progress here can stall without anything visibly going wrong.",
        "Measured as a percentage of a cohort, not of a population. Every figure describes a group that was born, not a group that lives somewhere.",
        "Whatever it counts, it has all happened by the age of five."
      ],
      why: "Nigeria's 1970–71 drop is the end of the Biafran war. South Korea's line falling to 0.28% shows the floor a rich country reaches. Poverty and illiteracy don't approach zero that cleanly.",
      slug: "child-mortality"
    },
    {
      family: "Distribution",
      form: "Beeswarm · every country, 2020",
      exhibit: "Exhibit E",
      type: "beeswarm", diff: 2,
      truth: "Litres of pure alcohol drunk per adult, 2020", period: "2020",
      unit: "litres of pure alcohol per adult per year",
      data: ALCOHOL,
      label: ["Somalia", "Saudi Arabia", "Turkey", "India",
              "Japan", "United Kingdom", "Germany", "Georgia", "Romania"],
      labelSm: ["Somalia", "Saudi Arabia", "India", "United Kingdom", "Romania"],
      answer: "Litres of pure alcohol drunk per adult each year",
      decoys: [
        "Kilograms of coffee drunk per person each year",
        "Cigarettes smoked per adult each day",
        "Hours of television watched per person each day",
        "Kilograms of fish eaten per person each month",
        "Doctors per 1,000 people",
        "Litres of petrol used per person each week",
        "Hours of paid work per person each day"
      ],
      hints: [
        "Four countries record exactly zero. Not nearly zero. Zero.",
        "What those four have in common is a law rather than a shortage. The two highest are in the Balkans and the Caucasus.",
        "Measured in litres of the pure substance, per adult, per year, which is why the numbers look modest.",
        "Saudi Arabia, Kuwait, Mauritania and Somalia all sit at zero, for the same legal reason."
      ],
      why: "The cluster at exactly zero is the tell: Saudi Arabia, Kuwait, Mauritania and Somalia prohibit it outright. No consumption measure except alcohol produces a hard floor of true zeroes alongside a Romanian peak of 16.8.",
      slug: "total-alcohol-consumption-per-capita-litres-of-pure-alcohol"
    },
    {
      family: "Ranking", form: "Lollipop · log scale, 2023", exhibit: "Exhibit F",
      type: "lollipop", log: true, diff: 1,
      truth: "People per square kilometre, 2023", period: "2023", unit: "people per square kilometre",
      data: [["Monaco",18704],["Singapore",8063],["Bahrain",1987],["Maldives",1754],
             ["Malta",1666],["Bangladesh",1317],["Taiwan",658],["Barbados",657],
             ["Mauritius",638],["Netherlands",537],["India",484],["Belgium",387],
             ["Japan",341],["United Kingdom",284],["United States",37.5],
             ["Russia",8.9],["Canada",4.5],["Australia",3.4]],
      answer: "People per square kilometre",
      decoys: [
        "Average number of tourists a year, per thousand residents",
        "Cost of a square metre of housing, in hundreds of dollars",
        "Mobile phone subscriptions per hundred people",
        "Average annual rainfall, in millimetres",
        "Visitors a year, in thousands",
        "Average income per person, in dollars",
        "Trees per hectare of land"
      ],
      hints: ["You could drive across anything at the top of this list before lunch. You could not cross anything at the bottom in a week.",
              "Bangladesh sits sixth, and everything above it is either an island or a city state. It is neither rich nor tiny, but it is crowded.",
              "The scale is logarithmic, because the leader is more than five thousand times the last place.",
              "It is simply how many people share each square kilometre."],
      why: "Monaco, Singapore, Bahrain, Malta and the Maldives at the top, with Australia, Canada and Russia at the bottom, is the signature of land area rather than anything economic.",
      slug: "population-density"
    },
    {
      family: "Ranking", form: "Lollipop · 2024", exhibit: "Exhibit G",
      type: "lollipop", diff: 2,
      truth: "People arriving from abroad, 2019", period: "2019", unit: "arrivals from abroad per year",
      /* 2019 rather than the latest year, deliberately. Our World in Data's 2024
         cut of this series is incomplete for several big destinations: France
         drops from 90.9m to 48.4m and Thailand from 39.9m to 0.5m, which are
         reporting gaps rather than real falls. 2019 is the last year the series
         is whole, and it ranks the countries the way the world actually does. */
      data: [["France",90914000],["Spain",83509000],["United States",79442000],
             ["China",65725000],["Italy",64513000],["Turkey",51192000],
             ["Mexico",45024000],["Thailand",39916000],["Germany",39563000],
             ["United Kingdom",39418000],["Austria",31884000],["Greece",31348400]],
      answer: "Number of people arriving from abroad each year",
      decoys: [
        "Number of people born there who now live abroad",
        "Number of people employed in hotels and restaurants",
        "Number of air passengers on domestic flights each year",
        "Number of international students enrolled each year",
        "Number of hotel beds available",
        "Number of passports issued each year",
        "Number of people employed in transport"
      ],
      hints: ["Thailand and Turkey both sit ahead of Britain and Germany, which is not how those four rank on very much else.",
              "Spain's figure is nearly twice the number of people who live in Spain, so this counts events rather than residents.",
              "Counted in millions a year, each one crossing a border in one direction.",
              "It is how many tourists visit."],
      why: "France at 90.9 million against a population of 67 million, and Spain at 83.5 million against 47 million, is the discriminator: no country has more than its own population working in restaurants or living abroad. These are 2019 figures, the last year the series is complete for every major destination.",
      slug: "international-tourism-number-of-arrivals"
    },
    {
      family: "Part-to-whole", form: "Treemap · share of world total", exhibit: "Exhibit H",
      type: "treemap", diff: 2,
      truth: "Wine production, 2023", period: "2023", unit: "tonnes",
      total: 22897819,
      data: [
        ["France",4762507], ["Italy",4249948], ["Spain",2849589],
        ["United States",2083125], ["China",1761139], ["Rest of world",1629638],
        ["Chile",1103023], ["Australia",964000], ["South Africa",922185],
        ["Argentina",881305], ["Portugal",737257], ["Russia",481907],
        ["Germany",472196]
      ],
      answer: "Wine production, 2023",
      decoys: [
        "Olive oil production, 2023",
        "Cheese production, 2023",
        "Beer production, 2023",
        "Tomato production, 2023",
        "Apple production, 2023",
        "Sugar beet production, 2023",
        "Barley production, 2023"
      ],
      hints: ["The top three have been arguing about which of them does this best for roughly two thousand years.",
              "Chile, Australia, South Africa and Argentina all rank high. This followed European settlers wherever the climate would take it.",
              "Measured in tonnes. The top three between them are half the world's supply.",
              "It is made from grapes."],
      why: "France, Italy and Spain in that order is wine's signature. Olive oil would put Spain far ahead with Greece and Turkey close behind; beer would be led by China, the United States and Brazil.",
      slug: "wine-production"
    },
    {
      family: "Change over time", form: "Dumbbell · 2000 → 2025", exhibit: "Exhibit I",
      type: "dumbbell", diff: 3,
      truth: "Share of the population using the internet, 2000 vs 2025",
      period: "2000 → 2025", unit: "% of the population",
      leftYear: 2000, rightYear: 2025,
      data: [["Burundi",0.1,8.6],["Nigeria",0.1,41.2],["India",0.5,70],["Brazil",2.9,84.5],
             ["Japan",30,85.5],["China",1.8,91.6],["United States",43.1,94.7],
             ["United Kingdom",26.8,95.5],["Malaysia",21.4,98],["Norway",52,99],
             ["Denmark",39.2,99.8],["Bahrain",6.2,100],["Saudi Arabia",2.2,100]],
      answer: "Share of the population using the internet",
      decoys: [
        "Share of adults who can read and write",
        "Share of homes with running water",
        "Share of adults in paid employment",
        "Share of the population aged under 30",
        "Share of children vaccinated against measles",
        "Share of journeys made by car",
        "Share of adults who own their home"
      ],
      hints: ["Twenty-five years ago every country on this list was close to zero. Two of them still are.",
              "Even Norway, the highest anywhere in 2000, managed only fifty. Nothing a rich country had already sorted out by then can look like this.",
              "A percentage of the population. The gap between top and bottom is wider now than it was in 2000, not narrower.",
              "The question asked is whether you have been online in the last three months."],
      why: "In 2000 the highest figure anywhere was Norway at 52%, and most of the world was under 1%. Nothing else on the list was that rare that recently: literacy, running water and measles vaccination were long settled in rich countries by then. Burundi at 8.6% today rules them out at the other end too.",
      slug: "share-of-individuals-using-the-internet"
    },
    {
      family: "Ranking", form: "Lollipop · 2025", exhibit: "Exhibit J",
      type: "lollipop", diff: 3,
      truth: "Economic output per person, 2025", period: "2025", unit: "international dollars per person",
      data: [["Singapore",139593],["Ireland",131338],["Luxembourg",127421],["Qatar",110136],
             ["Norway",95173],["Switzerland",85732],["Guyana",83659],["Brunei",78985],
             ["United States",76931],["Denmark",72723],["Netherlands",71378],
             ["United Arab Emirates",69702],["Iceland",68065],["Germany",62824],
             ["United Kingdom",53993],["China",25067],["India",10039]],
      answer: "Economic output per person, in dollars",
      decoys: [
        "Average yearly wage, in dollars",
        "Household savings per adult, in dollars",
        "Value of exports per person, in dollars",
        "Government spending per person, in dollars",
        "Value of goods imported per person, in dollars",
        "Electricity used per person, in kilowatt-hours",
        "Average house price, in dollars"
      ],
      hints: ["Two of the top three are small European countries whose figures have long embarrassed their own statisticians.",
              "Guyana appears seventh. A decade ago it was nowhere near. Then oil was found off its coast.",
              "Ireland's figure is inflated by multinationals booking profits there. The Irish are not twice as rich as the Germans.",
              "It is a country's total output, divided by its people."],
      why: "Ireland and Luxembourg rank this high only on output, not on wages or savings. Their figures are distorted by corporate accounting rather than by how much people actually earn.",
      slug: "gdp-per-capita-worldbank"
    },
    {
      family: "Part-to-whole", form: "Treemap · the twelve largest growers", exhibit: "Exhibit K",
      type: "treemap", diff: 4,
      truth: "Banana production, 2024", period: "2024", unit: "tonnes",
      total: 101616902,
      data: [["India",37614360],["China",11759700],["Indonesia",9260387],["Ecuador",7585653],
             ["Brazil",7046345],["Nigeria",6907143],["Philippines",5641130],["Angola",5213106],
             ["Guatemala",2843487],["Mexico",2670291],["Colombia",2638064],["Rwanda",2437236]],
      answer: "Banana production, 2024",
      decoys: [
        "Mango production, 2024",
        "Rice production, 2024",
        "Sugarcane production, 2024",
        "Cassava production, 2024",
        "Sweet potato production, 2024",
        "Coconut production, 2024",
        "Orange production, 2024"
      ],
      hints: ["Ecuador ranks fourth, despite being far smaller than everything above it.",
              "Ecuador exports more of this than anyone on earth, but Angola in eighth and Rwanda in twelfth eat theirs at home, a starch at every meal rather than a snack.",
              "Measured in tonnes. India alone grows more than the next three put together.",
              "It is yellow, and botanically it is a berry."],
      why: "The top four look like a population ranking, which is the trap. Ecuador in fourth and Angola in eighth are what separate it from rice or sugarcane, both of which would put Thailand, Vietnam or Bangladesh high and leave Ecuador nowhere.",
      slug: "banana-production"
    },
    {
      family: "Ranking", form: "Lollipop · highest and lowest, 2024", exhibit: "Exhibit L",
      type: "lollipop", diff: 3, breakAfter: 10,
      truth: "Share of adults who are obese, 2024", period: "2024", unit: "% of adults",
      suffix: "%",
      data: [["Tonga",72.3],["Nauru",71.4],["Tuvalu",64.7],["Samoa",63.2],["Bahamas",48.4],
             ["Saint Kitts and Nevis",47.9],["Micronesia",46.8],["Kiribati",45.3],
             ["Egypt",42.8],["Qatar",42.4],
             ["United States",41.8],["United Kingdom",29.2],["France",12.5],["Japan",5.2],
             ["Cambodia",4.9],["Madagascar",4.1],["Ethiopia",2.5],["Vietnam",2.5]],
      answer: "Share of adults who are obese",
      decoys: [
        "Share of adults with diabetes",
        "Share of adults with high blood pressure",
        "Share of adults who own a car",
        "Share of adults who smoke",
        "Share of adults who are physically inactive",
        "Share of adults with high cholesterol",
        "Share of adults who drink alcohol every week"
      ],
      hints: ["The top of this list is almost entirely Pacific islands. The bottom is almost entirely South-East Asia and East Africa.",
              "Japan and Vietnam sit under 6% while the United States is above 40%, a gap far too wide for anything mainly genetic.",
              "Measured as a share of adults, using a threshold on a simple height-and-weight formula.",
              "The threshold is a body mass index of 30."],
      why: "Diabetes and high blood pressure would both put different countries on top and compress the range, and neither produces a 70% figure anywhere. The Pacific island cluster is specific to obesity.",
      slug: "share-of-adults-defined-as-obese"
    },
    {
      family: "Deviation", form: "Diverging bar · distance from a reference, 2025", exhibit: "Exhibit M",
      type: "deviation", diff: 3, reference: 2,
      truth: "Military spending as a share of GDP, 2025", period: "2025", unit: "% of GDP, against a 2% reference line",
      data: [["Ukraine",39.6],["Israel",7.8],["Russia",7.5],["Myanmar",6.6],["Qatar",6.5],
             ["Saudi Arabia",6.5],["Azerbaijan",6.5],["Armenia",6.1],["Oman",5.7],
             ["Kuwait",4.7],["Jordan",4.6],["Poland",4.5],["United States",3.1],
             ["United Kingdom",2.4],["Germany",2.3],["China",1.7],["Japan",1.4]],
      answer: "Military spending as a share of GDP",
      decoys: [
        "Share of GDP spent on education",
        "Share of GDP spent on health by government",
        "Share of the workforce employed by the state",
        "Share of GDP spent on pensions",
        "Share of GDP earned from tourism",
        "Share of GDP spent on debt interest",
        "Share of GDP spent on new infrastructure"
      ],
      hints: ["One country here is roughly five times any other. It was invaded three years ago.",
              "The Gulf states all sit above the line while Japan and China sit below it, despite being enormous economies, so this is a share of something rather than a total.",
              "The line everything is measured against is the figure one alliance spent two decades asking its members to reach.",
              "It is the share of national income spent on armed forces."],
      why: "The 2% line is the benchmark NATO set for its members in 2014. Ukraine at 39.6% of GDP has no parallel in any peacetime budget line, and Japan and China sitting below the line despite enormous absolute spending is the giveaway that this is a share, not a total.",
      slug: "military-expenditure-as-a-share-of-gdp"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2023", exhibit: "Exhibit N",
      type: "beeswarm", diff: 5,
      truth: "Kilograms of meat eaten per person, 2023", period: "2023", unit: "kilograms per person per year",
      data: [["Afghanistan",6.4],["Albania",56.7],["Algeria",22.3],["Angola",18.6],["Antigua and Barbuda",96.4],["Argentina",114.9],["Armenia",54.7],["Australia",116.8],["Austria",73.7],["Azerbaijan",39.4],["Bahamas",114.9],["Bahrain",76.3],["Bangladesh",4.5],["Barbados",76.2],["Belarus",111.7],["Belgium",60],["Belize",68.2],["Benin",17.3],["Bhutan",14.7],["Bolivia",84.4],["Bosnia and Herzegovina",51.9],["Botswana",43.3],["Brazil",104.6],["Bulgaria",63.7],["Burkina Faso",23.1],["Burundi",3.6],["Cambodia",16.1],["Cameroon",14.8],["Canada",94.8],["Cape Verde",43.8],["Central African Republic",39.1],["Chad",47],["Chile",98.5],["China",73.5],["Colombia",62.6],["Comoros",26.6],["Congo",55.8],["Costa Rica",64.1],["Cote d'Ivoire",12],["Croatia",99.7],["Cuba",65.7],["Cyprus",77.9],["Czechia",82.3],["Democratic Republic of Congo",3.5],["Denmark",101.3],["Djibouti",14.1],["Dominica",86.4],["Dominican Republic",61.6],["East Timor",31.8],["Ecuador",56.2],["Egypt",27.6],["El Salvador",45.6],["Estonia",64.7],["Eswatini",22.4],["Ethiopia",6.9],["Fiji",63.2],["Finland",69.4],["France",80.3],["Gabon",63.1],["Gambia",19.1],["Georgia",45.4],["Germany",70.7],["Ghana",17.4],["Greece",82],["Grenada",80.5],["Guatemala",54.3],["Guinea",15.2],["Guinea-Bissau",14],["Guyana",88.7],["Haiti",20.7],["Honduras",37.7],["Hungary",76.3],["Iceland",98.1],["India",8.1],["Indonesia",20],["Iran",29.9],["Iraq",21.1],["Ireland",98.4],["Israel",108.7],["Italy",71.2],["Jamaica",67],["Japan",59.9],["Jordan",35.1],["Kazakhstan",64.9],["Kenya",10.2],["Kiribati",45.1],["Kuwait",62.5],["Kyrgyzstan",40],["Laos",31.1],["Latvia",82.7],["Lebanon",38.2],["Lesotho",18.8],["Liberia",12.3],["Libya",43.7],["Lithuania",80.9],["Luxembourg",83],["Madagascar",5.3],["Malawi",28.2],["Malaysia",69.1],["Maldives",29.6],["Mali",7.5],["Malta",71.8],["Marshall Islands",125.6],["Mauritania",36.5],["Mauritius",64.5],["Mexico",78.2],["Micronesia",64],["Moldova",33.9],["Mongolia",136.1],["Montenegro",96.9],["Morocco",32.8],["Mozambique",10.3],["Myanmar",20.9],["Namibia",24.2],["Nauru",109.2],["Nepal",14.5],["Netherlands",71.6],["New Caledonia",89.6],["New Zealand",79.5],["Nicaragua",36.3],["Niger",7.7],["Nigeria",7.1],["North Korea",13.8],["North Macedonia",51.5],["Norway",70.4],["Oman",37.6],["Pakistan",21.2],["Panama",78],["Papua New Guinea",58.5],["Paraguay",26.9],["Peru",55.4],["Philippines",33.6],["Poland",83.3],["Portugal",99.3],["Qatar",71.4],["Romania",72.4],["Russia",84.8],["Rwanda",6.4],["Saint Kitts and Nevis",88.8],["Saint Lucia",90.3],["Saint Vincent and the Grenadines",118.5],["Samoa",109],["Sao Tome and Principe",25.2],["Saudi Arabia",58.1],["Senegal",20],["Serbia",84.2],["Seychelles",70.7],["Sierra Leone",10.8],["Slovakia",70],["Slovenia",60.4],["Solomon Islands",15.6],["Somalia",11.1],["South Africa",58.3],["South Korea",84],["South Sudan",21.4],["Spain",100.8],["Sri Lanka",11.6],["Sudan",18.4],["Suriname",48.5],["Sweden",68.3],["Switzerland",64],["Syria",16.2],["Taiwan",91.5],["Tajikistan",32.9],["Tanzania",12.2],["Thailand",24.5],["Togo",11.7],["Tonga",156.9],["Trinidad and Tobago",65.7],["Tunisia",30.9],["Turkey",49.4],["Turkmenistan",51.2],["Tuvalu",85.1],["Uganda",10.8],["Ukraine",49.5],["United Arab Emirates",67.8],["United Kingdom",84.4],["United States",122.1],["Uruguay",69.3],["Uzbekistan",47.4],["Vanuatu",41],["Venezuela",38],["Vietnam",60.5],["Yemen",13.7],["Zambia",17.6],["Zimbabwe",57.6]],
      label: ["India", "Nigeria", "Japan", "China", "United Kingdom",
              "Brazil", "United States", "Mongolia", "Tonga"],
      labelSm: ["India", "Japan", "United Kingdom", "United States", "Tonga"],
      answer: "Kilograms of meat eaten per person a year",
      decoys: [
        "Kilograms of seafood eaten per person a year",
        "Kilograms of sugar consumed per person a year",
        "Kilograms of grain eaten per person a year",
        "Kilograms of dairy consumed per person a year",
        "Kilograms of vegetables eaten per person a year",
        "Kilograms of fruit eaten per person a year",
        "Kilograms of bread eaten per person a year"
      ],
      hints: ["The two loneliest dots on the right are a Pacific island and a country of vast grassland where almost nothing else will grow.",
              "India sits near the very bottom, far below its poorer neighbours. That is a choice, not a shortage.",
              "Measured in kilograms per person per year. The bulge in the middle is most of Europe.",
              "Beef, pork, chicken and lamb, added together."],
      why: "Mongolia in second and India near the bottom is the pair that settles it: Mongolia's grassland diet and India's vegetarianism. Seafood would put Iceland, the Maldives and Kiribati on top instead, with Mongolia close to last.",
      slug: "meat-supply-per-person"
    },
    {
      family: "Change over time", form: "Dumbbell · 1950 → 2023", exhibit: "Exhibit O",
      type: "dumbbell", diff: 2,
      truth: "Years a newborn can expect to live, 1950 vs 2023", period: "1950 → 2023", unit: "years",
      leftYear: 1950, rightYear: 2023,
      data: [["Nigeria",35.5,54.5],["Ethiopia",35.5,67.3],["India",41.2,72],
             ["Russia",55.5,73.2],["Mexico",43.8,75.1],["Brazil",48.5,75.8],
             ["Turkey",47.3,77.2],["China",43.8,78],["United States",68.1,79.3],
             ["United Kingdom",68.6,81.3],["South Korea",22.2,84.3],["Japan",59.3,84.7]],
      answer: "Years a newborn can expect to live",
      decoys: [
        "The average age of the population",
        "The age at which people stop working",
        "Years of schooling a typical adult completed",
        "The age at which people marry",
        "Years a person spends in paid work",
        "The average age of a member of parliament",
        "The age at which people leave their parents' home"
      ],
      hints: ["One country starts at twenty-two. In 1950 it was in the middle of a war that killed roughly a tenth of its people.",
              "Britain and the United States begin far ahead of everyone else and finish in the middle of the pack. They improved least because they started highest.",
              "Measured in years, counted from birth.",
              "It is how long a baby born in that year could expect to live."],
      why: "South Korea's 22.2 in 1950 is the Korean War, and no other measure collapses to that level and then more than triples. The average age of a population never falls to 22 and then rises to 84.",
      slug: "life-expectancy"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2022", exhibit: "Exhibit P",
      type: "beeswarm", diff: 3,
      truth: "Share of adults who smoke, 2022", period: "2022", unit: "% of adults aged 15 and over",
      suffix: "%",
      data: [["Afghanistan",22.9],["Albania",22.3],["Algeria",22.1],["Andorra",35.4],["Argentina",24.3],["Armenia",26.6],["Australia",12.4],["Austria",25.3],["Azerbaijan",19.3],["Bahamas",17],["Bahrain",15.7],["Bangladesh",33.3],["Belarus",30.2],["Belgium",24],["Belize",8.8],["Benin",7.8],["Bhutan",20.2],["Bolivia",13],["Bosnia and Herzegovina",37.6],["Botswana",18.8],["Brazil",12.5],["Brunei",14.7],["Bulgaria",39.1],["Burkina Faso",12.5],["Burundi",10.9],["Cambodia",19.7],["Cameroon",6.1],["Canada",12.1],["Cape Verde",11],["Chad",7.7],["Chile",27.9],["China",23.1],["Colombia",8.3],["Comoros",10.2],["Congo",15.5],["Costa Rica",8.4],["Cote d'Ivoire",8],["Croatia",34.5],["Cuba",17.3],["Cyprus",32.8],["Czechia",28.8],["Democratic Republic of Congo",12.7],["Denmark",17],["East Timor",48.6],["Ecuador",10.4],["Egypt",24.4],["El Salvador",8.6],["Estonia",27.5],["Eswatini",11.4],["Ethiopia",5.3],["Fiji",26.4],["Finland",22.4],["France",33.7],["Gabon",13.3],["Gambia",11.7],["Georgia",32.8],["Germany",22.8],["Ghana",3.5],["Greece",31.5],["Guatemala",11.4],["Guinea-Bissau",8.6],["Guyana",12.5],["Haiti",8.2],["Honduras",12.4],["Hungary",31.3],["Iceland",10.2],["India",24.4],["Indonesia",31.2],["Iran",12.5],["Iraq",20.2],["Ireland",19.2],["Israel",21.8],["Italy",22.7],["Jamaica",11.9],["Japan",18.5],["Jordan",33.8],["Kazakhstan",22.1],["Kenya",10.2],["Kiribati",39.7],["Kuwait",19.3],["Kyrgyzstan",23],["Laos",26.8],["Latvia",35.3],["Lebanon",45.6],["Lesotho",27.7],["Liberia",5.8],["Libya",24.8],["Lithuania",32.3],["Luxembourg",24.7],["Madagascar",26.8],["Malawi",9.6],["Malaysia",17.4],["Maldives",26.6],["Mali",7.9],["Malta",25],["Marshall Islands",29.6],["Mauritania",10.4],["Mauritius",18.2],["Mexico",16.1],["Moldova",28.3],["Mongolia",29.9],["Montenegro",37.1],["Morocco",13],["Mozambique",11.5],["Myanmar",44.5],["Nauru",36.6],["Nepal",30.4],["Netherlands",21.4],["New Zealand",10.3],["Niger",7.5],["Nigeria",3.3],["North Korea",16.4],["North Macedonia",39.6],["Norway",14.4],["Oman",8.4],["Pakistan",19],["Palau",23.5],["Palestine",34.8],["Panama",5.3],["Papua New Guinea",40.5],["Paraguay",7.3],["Peru",13.4],["Philippines",20.9],["Poland",22.8],["Portugal",28],["Qatar",12.5],["Romania",30.4],["Russia",27.8],["Rwanda",11.6],["Saint Lucia",14.2],["Samoa",24.1],["Sao Tome and Principe",8.1],["Saudi Arabia",14.7],["Senegal",5.9],["Serbia",39.6],["Seychelles",17.8],["Sierra Leone",12.7],["Singapore",14.1],["Slovakia",29.6],["Slovenia",21.2],["Solomon Islands",38.6],["South Africa",23.5],["South Korea",19.6],["Spain",28.1],["Sri Lanka",21.3],["Sweden",21.8],["Switzerland",23.6],["Tanzania",8.6],["Thailand",18.4],["Togo",6.3],["Tonga",32],["Tunisia",25.2],["Turkey",31.1],["Turkmenistan",5.8],["Tuvalu",34.3],["Uganda",8.3],["Ukraine",24.9],["United Arab Emirates",9.4],["United Kingdom",14],["United States",17],["Uruguay",20.3],["Uzbekistan",17],["Vanuatu",25],["Vietnam",21.7],["Zambia",14.6],["Zimbabwe",11.6]],
      label: ["Nigeria", "Ghana", "Australia", "United Kingdom", "United States", "Japan", "Indonesia", "France", "East Timor"],
      labelSm: ["Nigeria", "United Kingdom", "Japan", "France", "East Timor"],
      answer: "Share of adults who smoke",
      decoys: [
          "Share of adults who are obese",
          "Share of adults who drink alcohol every week",
          "Share of adults with a university degree",
          "Share of adults who are out of work",
          "Share of adults with high blood pressure",
          "Share of adults who have never used the internet",
          "Share of adults who hold a passport"
        ],
      hints: [
          "Indonesia, Bangladesh and Jordan sit near the top while the wealthy Gulf states sit low, so money is not what sorts this list.",
          "France stands above Germany, Britain and the United States. Nigeria and Ghana are at the very bottom, near three percent.",
          "Measured as a share of everyone aged fifteen and over, and falling almost everywhere that is rich.",
          "It is the share of adults who use tobacco."
        ],
      why: "The United States at 17% is the discriminator against obesity, where it would be near the top at about 42%. Indonesia, Bangladesh and Jordan high with Ghana and Nigeria at 3% is the tobacco pattern, and no alcohol measure puts Jordan and Palestine above Britain.",
      slug: "share-of-adults-who-smoke"
    },
    {
      family: "Change over time", form: "Dumbbell · 1960 → 2025", exhibit: "Exhibit Q",
      type: "dumbbell", diff: 2,
      truth: "Share of the population living in towns and cities, 1960 vs 2025", period: "1960 → 2025", unit: "% of the population",
      suffix: "%",
      leftYear: 1960, rightYear: 2025,
      data: [
        ["Ethiopia",7.1,24.1], ["India",17.9,35.7], ["Egypt",37.8,42.9],
        ["Indonesia",14.6,59.4], ["Nigeria",14.2,63.8], ["China",19.7,66.3],
        ["Mexico",50.7,80.0], ["United States",70.0,80.2], ["South Korea",27.7,81.2],
        ["United Kingdom",78.6,83.3], ["Brazil",44.7,88.2], ["Japan",63.3,92.3]
      ],
      answer: "Share of the population living in towns and cities",
      decoys: [
          "Share of the population with access to electricity",
          "Share of the population who can read and write",
          "Share of the population in paid work",
          "Share of adults who own their home",
          "Share of the population with a bank account",
          "Share of the population who finished secondary school",
          "Share of the population with running water at home"
        ],
      hints: [
          "One country has barely shifted in sixty-five years. It is neither the poorest here nor the richest.",
          "Britain and the United States begin far ahead of everyone and finish only a little further on. They had almost run out of room in 1960.",
          "Measured as a percentage of the population. Nigeria's jump from 14 to 64 happened without the country becoming notably richer.",
          "It is simply where people live: a town or a city on one side, the countryside on the other."
        ],
      why: "Egypt moving from 37.8% to only 42.9% in sixty-five years is the tell. No literacy, electricity or schooling measure stalls like that, and Britain starting at 78.6% in 1960 rules out anything that was still rare then.",
      slug: "share-of-population-urban"
    },
    {
      family: "Change over time", form: "Dumbbell · 2000 → 2024", exhibit: "Exhibit R",
      type: "dumbbell", diff: 2,
      truth: "Share of people with access to electricity, 2000 vs 2024", period: "2000 → 2024", unit: "% of the population",
      suffix: "%",
      leftYear: 2000, rightYear: 2024,
      data: [
        ["Tanzania",8.7,52.4], ["Uganda",7.4,55.3], ["Ethiopia",12.7,56.6],
        ["Nigeria",43.2,62.5], ["Rwanda",6.2,72.0], ["Kenya",15.2,77.0],
        ["Myanmar",41.9,80.4], ["Afghanistan",4.4,87.8], ["Nepal",29.9,97.9],
        ["Bangladesh",32.0,99.5], ["India",60.3,99.9], ["Indonesia",86.3,99.9]
      ],
      answer: "Share of people with access to electricity",
      decoys: [
          "Share of people who own a mobile phone",
          "Share of people with access to clean drinking water",
          "Share of people who can read and write",
          "Share of children who finish primary school",
          "Share of people with a bank account",
          "Share of people vaccinated against measles",
          "Share of people who own a bicycle"
        ],
      hints: [
          "Indonesia already had this for most of its people in 2000, which rules out anything invented recently.",
          "Nigeria is the laggard: it starts well above Kenya and finishes far below it, despite the oil money.",
          "Measured as a percentage of the population. India has effectively finished the job since 2000.",
          "It is whether the house is connected to power."
        ],
      why: "Indonesia at 86% in 2000 rules out mobile phones and bank accounts, both rare then. Nigeria ending at 62.5% while Bangladesh reaches 99.5% is the grid story, not the literacy one.",
      slug: "share-of-the-population-with-access-to-electricity"
    },
    {
      family: "Part-to-whole", form: "Treemap · the twelve largest growers", exhibit: "Exhibit S",
      type: "treemap", diff: 3,
      truth: "Rice production, 2024", period: "2024", unit: "tonnes",
      total: 707380000,
      data: [
        ["India",217867870], ["China",207530000], ["Bangladesh",60570452],
        ["Indonesia",53142730], ["Vietnam",43450450], ["Thailand",33551336],
        ["Myanmar",27650000], ["Philippines",19087136], ["Pakistan",14585231],
        ["Brazil",10671490], ["Japan",10142000], ["Nigeria",9129900]
      ],
      answer: "Rice production, 2024",
      decoys: [
          "Wheat production, 2024",
          "Maize production, 2024",
          "Sugar cane production, 2024",
          "Soybean production, 2024",
          "Potato production, 2024",
          "Cotton production, 2024",
          "Tea production, 2024"
        ],
      hints: [
          "Ten of the twelve blocks are in Asia, and the two largest are neighbours who between them hold a third of humanity.",
          "The United States, Russia and France are all missing, which rules out the grains that Europe and North America grow at scale.",
          "Measured in tonnes as harvested. Japan appears despite having very little farmland, because this crop is the one it protects at any cost.",
          "It is boiled, steamed or fried, and eaten with almost every meal from Lahore to Tokyo."
        ],
      why: "The absence of the United States, Russia, France and Ukraine rules out wheat and maize. Japan producing 10 million tonnes on very little arable land, and Bangladesh third, is the rice signature.",
      slug: "rice-production"
    },
    {
      family: "Part-to-whole", form: "Treemap · share of world total", exhibit: "Exhibit T",
      type: "treemap", diff: 4,
      truth: "Share of the world's forest area, 2025", period: "2025", unit: "% of the world total",
      total: 100,
      data: [
        ["Rest of world",30.87], ["Russia",20.11], ["Brazil",11.74],
        ["Canada",8.91], ["United States",7.46], ["China",5.49],
        ["DR Congo",3.36], ["Australia",3.23], ["Indonesia",2.32],
        ["India",1.76], ["Peru",1.62], ["Mexico",1.6],
        ["Angola",1.53]
      ],
      answer: "Share of the world's forest area",
      decoys: [
          "Share of the world's farmland",
          "Share of the world's fresh water",
          "Share of the world's land area",
          "Share of the world's coal reserves",
          "Share of the world's cattle",
          "Share of the world's oil reserves",
          "Share of the world's protected land"
        ],
      hints: [
          "Australia is one of the largest countries on earth and gets a small tile. Indonesia, a fraction of its size, is not far behind it.",
          "India, with a seventh of the world's people and a great deal of land under the plough, holds under two percent of this.",
          "The five biggest tiles are all countries with vast cold or wet interiors that nobody has cleared.",
          "It is where the world's trees are."
        ],
      why: "Russia at 20% with Canada third is the boreal signature. Farmland would put India and the United States near the top rather than India at 1.8%, and by land area Russia is 11% of the world, not 20%.",
      slug: "share-global-forest"
    },
    {
      family: "Ranking", form: "Rank slope · 1990 → 2024", exhibit: "Exhibit U",
      type: "slope", diff: 4,
      truth: "World ranking of carbon dioxide emitters, 1990 vs 2024", period: "1990 → 2024", unit: "rank by tonnes emitted in a year",
      leftYear: 1990, rightYear: 2024,
      ranks: [
        ["China",3,1], ["United States",1,2], ["India",7,3],
        ["Russia",2,4], ["Japan",4,5], ["Indonesia",12,6],
        ["Iran",10,7], ["Saudi Arabia",11,8], ["South Korea",8,9],
        ["Germany",5,10], ["Brazil",9,11], ["United Kingdom",6,12]
      ],
      answer: "World ranking of carbon dioxide emitters",
      decoys: [
          "World ranking of steel-producing countries",
          "World ranking of countries by electricity generated",
          "World ranking of countries by number of cars on the road",
          "World ranking of countries by total economic output",
          "World ranking of oil-consuming countries",
          "World ranking of countries by cement produced",
          "World ranking of countries by energy imported"
        ],
      hints: [
          "Britain started the thing that put it sixth in 1990. It is now last of the twelve.",
          "Germany falls five places while Iran and Saudi Arabia climb. Population is not what moves these lines.",
          "One country roughly quintuples and takes first place. This is ranked on an annual national total, not a figure per person.",
          "It is measured in tonnes released into the atmosphere."
        ],
      why: "Britain's fall from 6th to 12th while Saudi Arabia climbs to 8th is the discriminator: on total economic output Britain would still be near the top and Saudi Arabia nowhere near it. China rising from third to first at roughly five times its 1990 figure fits emissions rather than any slower-moving ranking.",
      slug: "annual-co2-emissions-per-country"
    },
    {
      family: "Ranking", form: "Rank slope · 1975 → 2023", exhibit: "Exhibit V",
      type: "slope", diff: 3,
      truth: "World ranking of the most populous countries, 1975 vs 2023", period: "1975 → 2023", unit: "rank by number of people",
      leftYear: 1975, rightYear: 2023,
      ranks: [
        ["India",2,1], ["China",1,2], ["United States",3,3],
        ["Indonesia",5,4], ["Pakistan",9,5], ["Nigeria",10,6],
        ["Brazil",7,7], ["Bangladesh",8,8], ["Russia",4,9],
        ["Mexico",11,10], ["Ethiopia",12,11], ["Japan",6,12]
      ],
      answer: "World ranking of the most populous countries",
      decoys: [
          "World ranking of countries by total economic output",
          "World ranking of countries by number of mobile phones",
          "World ranking of countries by area of farmland",
          "World ranking of countries by births each year",
          "World ranking of countries by size of armed forces",
          "World ranking of countries by electricity generated",
          "World ranking of countries by number of internet users"
        ],
      hints: [
          "Two lines cross at the very top in the early 2020s, and it made headlines when they did.",
          "Japan falls six places without anything happening to Japan. Everyone else simply grew.",
          "Brazil and Bangladesh do not move at all across half a century, which is unusual on any ranking.",
          "It counts heads."
        ],
      why: "India overtaking China, with Japan sliding from 6th to 12th while still holding one of the largest economies, is the population signature. On economic output Japan would remain in the top three and Ethiopia would not appear at all.",
      slug: "population"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2024", exhibit: "Exhibit W",
      type: "beeswarm", diff: 4,
      truth: "Mobile phone subscriptions per 100 people, 2024", period: "2024", unit: "active subscriptions per 100 people",
      data: [["Afghanistan",60.1],["Albania",89.1],["Algeria",115.5],["Andorra",155.7],["Angola",69.7],["Antigua and Barbuda",200.5],["Argentina",140.2],["Armenia",134.9],["Australia",112.6],["Austria",124.5],["Azerbaijan",109.5],["Bahamas",96.7],["Bahrain",159.5],["Bangladesh",108.1],["Barbados",114.6],["Belarus",131.1],["Belgium",103.9],["Belize",67.2],["Benin",125.9],["Bhutan",99.8],["Bolivia",98],["Bosnia and Herzegovina",121.2],["Botswana",164],["Brazil",101.9],["Brunei",118.1],["Bulgaria",118.1],["Burkina Faso",116.6],["Burundi",63.2],["Cambodia",116.1],["Cameroon",108.2],["Canada",94.1],["Cape Verde",111.8],["Central African Republic",38.8],["Chad",72.9],["Chile",132.7],["China",131.8],["Colombia",174.1],["Comoros",109.9],["Congo",95.5],["Costa Rica",136],["Cote d'Ivoire",183.9],["Croatia",121.7],["Cuba",72.9],["Cyprus",156.2],["Czechia",126.6],["Democratic Republic of Congo",58.5],["Denmark",126.7],["Djibouti",48.5],["Dominica",85.2],["Dominican Republic",93.7],["East Timor",116.4],["Ecuador",101.6],["Egypt",97.1],["El Salvador",176.5],["Equatorial Guinea",49.5],["Eritrea",59.1],["Estonia",151.1],["Eswatini",139.8],["Ethiopia",65.1],["Finland",125.9],["France",116.7],["Gabon",125.3],["Gambia",126.2],["Georgia",161.2],["Germany",129.2],["Ghana",113.6],["Greece",113.6],["Greenland",118.6],["Grenada",95.8],["Guatemala",112.5],["Guinea",97.9],["Guinea-Bissau",147.2],["Guyana",112.6],["Haiti",65.2],["Honduras",70.9],["Hungary",104.6],["Iceland",120.9],["India",79.4],["Indonesia",122.5],["Iran",174.1],["Iraq",100.1],["Ireland",112.6],["Israel",177.4],["Italy",132.6],["Jamaica",117.7],["Japan",178.4],["Jordan",69.6],["Kazakhstan",127.1],["Kenya",126.5],["Kiribati",53.5],["Kosovo",34.5],["Kuwait",167.7],["Kyrgyzstan",107.5],["Laos",64.8],["Latvia",121.3],["Lebanon",74],["Lesotho",70.3],["Liberia",32.1],["Libya",193],["Liechtenstein",128.9],["Lithuania",138.7],["Luxembourg",144.5],["Madagascar",75.5],["Malawi",69.3],["Malaysia",139.7],["Maldives",148.1],["Mali",112.1],["Malta",142.1],["Marshall Islands",39.7],["Mauritania",92.1],["Mauritius",172.7],["Mexico",116.5],["Micronesia",20],["Moldova",120.1],["Monaco",107.4],["Mongolia",140.7],["Montenegro",221.7],["Morocco",153.1],["Mozambique",49.5],["Myanmar",114.3],["Namibia",85.2],["Nauru",87.2],["Nepal",99.8],["Netherlands",128.5],["New Caledonia",91.7],["New Zealand",130.1],["Nicaragua",106],["Niger",60.6],["Nigeria",70.8],["North Korea",24.1],["North Macedonia",108.4],["Norway",109.3],["Oman",120.6],["Pakistan",76.9],["Palau",135.4],["Palestine",76.7],["Panama",156.6],["Papua New Guinea",38.8],["Paraguay",126.6],["Peru",124.6],["Philippines",115.3],["Poland",138],["Portugal",124.1],["Puerto Rico",126.4],["Qatar",153.6],["Romania",119.8],["Russia",186.1],["Rwanda",93.2],["Saint Kitts and Nevis",118.9],["Saint Lucia",98.7],["Saint Vincent",108.4],["Samoa",62.4],["San Marino",120.3],["Sao Tome and Principe",62.4],["Saudi Arabia",159.5],["Senegal",123.9],["Serbia",123.8],["Seychelles",125.6],["Sierra Leone",107.9],["Singapore",170.8],["Slovakia",140],["Slovenia",130.9],["Solomon Islands",62.1],["Somalia",54],["South Africa",179.3],["South Korea",172.5],["South Sudan",46.6],["Spain",130.3],["Sri Lanka",132.5],["Sudan",70.2],["Suriname",142.1],["Sweden",140.7],["Switzerland",129.5],["Syria",71.2],["Tajikistan",76.2],["Tanzania",126.6],["Thailand",160.6],["Togo",80.8],["Tonga",61.7],["Trinidad and Tobago",118.8],["Tunisia",117.6],["Turkey",107.8],["Turkmenistan",88.2],["Tuvalu",98.9],["Uganda",83.2],["Ukraine",133.4],["United Arab Emirates",203.2],["United Kingdom",121.6],["United States",113.2],["Uruguay",145.5],["Uzbekistan",110.5],["Vanuatu",89.3],["Venezuela",71],["Vietnam",127.6],["Yemen",50.9],["Zambia",108.7],["Zimbabwe",94.2]],
      label: ["North Korea", "Central African Republic", "India", "United States", "United Kingdom", "China", "Japan", "United Arab Emirates", "Montenegro"],
      labelSm: ["North Korea", "India", "United Kingdom", "Japan", "United Arab Emirates"],
      answer: "Mobile phone subscriptions per 100 people",
      decoys: [
          "Bank accounts per 100 adults",
          "Internet users per 100 people",
          "Cars per 100 people",
          "Televisions per 100 households",
          "Air journeys per 100 people each year",
          "Radios per 100 people",
          "Letters posted per 100 people each week"
        ],
      hints: [
          "Most of the world sits above one hundred, so whatever this counts, people hold more than one each.",
          "North Korea is the loneliest dot on the left at twenty-four, and the Gulf states are furthest right.",
          "Counted per hundred people. It stopped meaning what it used to once people began keeping a second one for work.",
          "It counts active SIM cards."
        ],
      why: "Values above 100 across most of the world rule out anything a person can only have one of, such as internet users or bank accounts. North Korea at 24 with the United Arab Emirates above 200 is the SIM-card pattern.",
      slug: "mobile-cellular-subscriptions-per-100-people"
    },
    {
      family: "Ranking", form: "Lollipop · highest and lowest, 2024", exhibit: "Exhibit X",
      type: "lollipop", diff: 2,
      truth: "Homicides per 100,000 people, 2024", period: "2024", unit: "killings per 100,000 people a year",
      data: [
        ["Saint Kitts and Nevis",64.2], ["Saint Vincent",51.3], ["Jamaica",49.4],
        ["Ecuador",45.7], ["South Africa",43.7], ["Haiti",41.2],
        ["Saint Lucia",39], ["Bahamas",32.2], ["Colombia",24.9],
        ["Mexico",24.9], ["Brazil",19.3], ["Russia",7.8],
        ["United States",5.8], ["India",2.8], ["France",1.4],
        ["United Kingdom",1.1], ["Germany",0.9], ["Australia",0.9],
        ["Japan",0.2], ["Singapore",0.1]
      ],
      answer: "Homicides per 100,000 people",
      decoys: [
          "Road deaths per 100,000 people",
          "Drug overdose deaths per 100,000 people",
          "Suicides per 100,000 people",
          "Prisoners per 10,000 people",
          "Deaths in house fires per 100,000 people",
          "Deaths from snakebite per 100,000 people",
          "Deaths at work per 100,000 workers"
        ],
      hints: [
          "The top of this list is almost entirely small Caribbean islands, with two mainland exceptions.",
          "The United States sits five times above Britain and France, and eight times below Jamaica.",
          "Counted per hundred thousand people a year, from police and coroner records.",
          "Every one of these is a person killed on purpose by another."
        ],
      why: "Small Caribbean islands filling the top with Japan and Singapore near zero is the homicide signature. On prisoners per head the United States would lead everything; on road deaths the list would be led by Africa and the Gulf, not the Caribbean.",
      slug: "homicide-rate-unodc"
    },
    {
      family: "Change over time", form: "Dumbbell · 2001 → 2023", exhibit: "Exhibit Y",
      type: "dumbbell", diff: 5,
      truth: "Share of the population who do not get enough to eat, 2001 vs 2023", period: "2001 → 2023", unit: "% of the population",
      suffix: "%",
      leftYear: 2001, rightYear: 2023,
      data: [
        ["China",10.0,2.5], ["Brazil",10.5,2.5], ["Cambodia",19.7,5.2],
        ["Vietnam",19.5,5.3], ["Ghana",14.8,6.3], ["Indonesia",18.1,6.3],
        ["Peru",20.4,6.9], ["Bangladesh",15.5,10.4], ["India",18.1,12.0],
        ["Ethiopia",46.1,19.7], ["Nigeria",8.7,19.9], ["Kenya",31.8,36.8]
      ],
      answer: "Share of the population who do not get enough to eat",
      decoys: [
          "Share of the population without clean drinking water",
          "Share of adults who cannot read or write",
          "Share of children who do not finish primary school",
          "Share of the population without access to electricity",
          "Share of the population without a toilet at home",
          "Share of adults who are out of work",
          "Share of the population living in the countryside"
        ],
      hints: [
          "Two of the twelve are worse off than they were in 2001, and both are in Africa, though probably not the two you would guess.",
          "Nigeria more than doubles while Ethiopia more than halves, which is the reverse of what happened to their economies.",
          "Measured as a percentage of the population, from national food supply figures and household surveys.",
          "It counts people whose daily calories fall short of what their body needs."
        ],
      why: "Nigeria rising from 8.7% to 19.9% and Kenya from 31.8% to 36.8% while Ethiopia halves is the discriminator: literacy, electricity and schooling all improved in Nigeria and Kenya over the same years. Only hunger went backwards.",
      slug: "prevalence-of-undernourishment"
    },
    {
      family: "Ranking", form: "Lollipop · 2023", exhibit: "Exhibit Z",
      type: "lollipop", diff: 4,
      truth: "Annual hours worked per worker, 2023", period: "2023", unit: "hours a year per person in work",
      data: [
        ["Colombia",2471], ["Costa Rica",2177], ["Chile",1950],
        ["South Korea",1910], ["Greece",1893], ["Poland",1807],
        ["United States",1789], ["Turkey",1747], ["Portugal",1735],
        ["Italy",1701], ["Ireland",1654], ["Japan",1654],
        ["Spain",1638], ["Mexico",1629], ["United Kingdom",1523],
        ["France",1487], ["Netherlands",1439], ["Norway",1412],
        ["Denmark",1380], ["Germany",1335]
      ],
      answer: "Annual hours worked per worker",
      decoys: [
          "Hours of sunshine a year",
          "Hours a year spent watching television per person",
          "Hours a year spent on unpaid housework per adult",
          "Hours a year spent online per person",
          "Hours a year spent caring for children per parent",
          "Litres of petrol used per person a year",
          "Cups of coffee drunk per person a year"
        ],
      hints: [
          "Germany sits at the bottom and Colombia at the top, with Mexico much closer to Germany than you would expect.",
          "Ireland is above the Netherlands and Norway is near the bottom, which rules out anything to do with the weather.",
          "Divide any of these by fifty-two and you get a plausible week. Germany's works out at about twenty-six hours.",
          "It is time spent on the job, averaged across everyone who has one."
        ],
      why: "Ireland above the Netherlands and Norway near the bottom rules out sunshine, the closest-looking alternative. Colombia and Costa Rica on top with Germany and Denmark at the bottom is the OECD hours-worked pattern, which runs almost opposite to productivity.",
      slug: "annual-working-hours-per-worker"
    },
    {
      family: "Change over time", form: "Dumbbell · 1997 → 2025", exhibit: "Exhibit AA",
      type: "dumbbell", diff: 3,
      truth: "Share of parliamentary seats held by women, 1997 vs 2025", period: "1997 → 2025", unit: "% of seats",
      suffix: "%",
      leftYear: 1997, rightYear: 2025,
      data: [
        ["India",7.2,13.8], ["Japan",4.6,15.7], ["United States",11.7,28.9],
        ["United Kingdom",18.2,40.5], ["South Africa",25.0,44.7], ["Costa Rica",14.0,49.1],
        ["United Arab Emirates",0.0,50.0], ["Mexico",14.2,50.2], ["Bolivia",11.5,50.8],
        ["Nicaragua",10.8,55.0], ["Cuba",22.8,55.7], ["Rwanda",17.1,63.8]
      ],
      answer: "Share of parliamentary seats held by women",
      decoys: [
          "Share of company board seats held by women",
          "Share of doctors who are women",
          "Share of university students who are women",
          "Share of the workforce who are women",
          "Share of judges who are women",
          "Share of school teachers who are women",
          "Share of senior civil servants who are women"
        ],
      hints: [
          "One country starts at exactly zero and finishes at exactly fifty, which is what a rule looks like rather than a trend.",
          "The leader is Rwanda, and the reason dates to what happened there in 1994.",
          "Britain more than doubles, the United States roughly triples, and Japan still finishes below twenty percent.",
          "It is the share of seats in the national legislature."
        ],
      why: "The United Arab Emirates moving from 0% to exactly 50% is a quota, not a labour market, and Rwanda leading the world at 63.8% only makes sense for elected seats. University students would put Japan and India far above 14 to 16 percent.",
      slug: "share-of-women-in-parliament"
    },
    {
      family: "Change over time", form: "Multi-line · 2013–2025", exhibit: "Exhibit AB",
      type: "line", diff: 2,
      truth: "Share of new cars sold that are electric, 2013–2025", period: "2013–2025", unit: "% of new car sales",
      suffix: "%",
      startYear: 2013,
      series: [
        { name: "Norway", values: [5.8,15,22,29,39,49,56,75,86,89,90,92,97] },
        { name: "China", values: [0.096,0.41,1.1,1.5,2.4,4.7,5,5.7,16,29,38,48,53] },
        { name: "United Kingdom", values: [0.16,0.59,1.1,1.4,1.9,2.6,3.2,11,18,22,23,27,35] },
        { name: "United States", values: [0.71,0.77,0.7,0.99,1.3,2.3,2.1,2.3,4.7,7.7,9.7,10,10] },
        { name: "India", values: [0.016,0.038,0.017,0.026,0.031,0.03,0.024,0.12,0.41,1.4,2.1,2.1,4] }
      ],
      answer: "Share of new cars sold that are electric",
      decoys: [
          "Share of households with solar panels",
          "Share of electricity generated by wind",
          "Share of electricity generated by solar",
          "Share of city buses that are electric",
          "Share of new homes built without a gas connection",
          "Share of adults who own a bicycle",
          "Share of new cars sold that are diesel"
        ],
      hints: [
          "One line reaches ninety-seven percent. Whatever this measures, one country has essentially finished.",
          "That country has both oil money and hydropower, and spent the first to make the second worth using.",
          "Every line is a share of a flow rather than of a stock, which is why they climb so steeply.",
          "It is the share of new cars sold that plug in."
        ],
      why: "Norway at 97% and China at 53% while the United States stalls near 10% is the new-car-sales pattern: it moves far faster than the share of cars on the road, and no national grid runs at 97% wind or solar.",
      slug: "electric-car-sales-share"
    },
    {
      family: "Deviation", form: "Diverging bar · around zero, 2024", exhibit: "Exhibit AC",
      type: "deviation", reference: 0, diff: 3,
      truth: "Annual population growth, 2024", period: "2024", unit: "% change over one year, against a zero line",
      data: [
        ["Nigeria",2.07], ["Kenya",1.94], ["Egypt",1.65],
        ["India",0.9], ["United Kingdom",0.62], ["United States",0.55],
        ["Brazil",0.4], ["Spain",-0.02], ["South Korea",-0.08],
        ["China",-0.22], ["Italy",-0.31], ["Germany",-0.34],
        ["Japan",-0.51], ["Russia",-0.53], ["Poland",-0.9]
      ],
      answer: "Annual population growth",
      decoys: [
          "Annual economic growth",
          "Annual change in the number of people in work",
          "Annual inflation",
          "Annual change in electricity demand",
          "Annual change in carbon emissions",
          "Annual change in the number of cars on the road",
          "Annual change in average wages"
        ],
      hints: [
          "The whole chart fits inside three percentage points, which rules out anything to do with money.",
          "Britain and the United States are above the line largely because people arrive. Poland is furthest below it.",
          "Measured as a percentage change over a single year, against a line at zero.",
          "It is whether there are more people at the end of the year than at the start."
        ],
      why: "A range of only three points, with Poland, Russia, Japan, Germany, Italy and China all negative while Nigeria and Kenya sit near two percent, is population. India's economy grew by roughly seven percent in 2024, far outside this chart.",
      slug: "population-growth-rates"
    },
    {
      family: "Part-to-whole", form: "Treemap · share of world total", exhibit: "Exhibit AD",
      type: "treemap", diff: 1,
      truth: "Oil production, 2025", period: "2025", unit: "share of world output",
      total: 54015,
      data: [
        ["Rest of world",13877], ["United States",10350], ["Saudi Arabia",6232],
        ["Russia",6085], ["Canada",3514], ["Iran",2816],
        ["China",2513], ["Iraq",2496], ["Brazil",2367],
        ["UAE",2199], ["Kuwait",1566]
      ],
      answer: "Oil production, 2025",
      decoys: [
          "Natural gas production, 2025",
          "Coal production, 2025",
          "Steel production, 2025",
          "Electricity generation, 2025",
          "Copper production, 2025",
          "Wheat production, 2025",
          "Car production, 2025"
        ],
      hints: [
          "Kuwait is on this chart and India, Germany and Japan are not, which is unusual for anything measured by volume.",
          "Five of the ten named blocks are in the Gulf, and Europe does not appear at all.",
          "The United States, Saudi Arabia and Russia between them are about two fifths of the world total.",
          "It comes out of the ground as a black liquid."
        ],
      why: "Kuwait, Iraq and the United Arab Emirates present while India, Germany and Japan are absent rules out coal, steel and electricity, where China alone would take more than half the square and India would rank third.",
      slug: "oil-production-by-country"
    },
    {
      family: "Part-to-whole", form: "Treemap · the eight largest growers", exhibit: "Exhibit AE",
      type: "treemap", diff: 3,
      truth: "Sugar cane production, 2024", period: "2024", unit: "tonnes",
      total: 1598494492,
      data: [
        ["Brazil",759662460], ["India",453158500], ["China",102094400],
        ["Pakistan",84235450], ["Thailand",82435400], ["Mexico",53051360],
        ["Indonesia",32000000], ["Colombia",31856922]
      ],
      answer: "Sugar cane production, 2024",
      decoys: [
          "Maize production, 2024",
          "Cassava production, 2024",
          "Rice production, 2024",
          "Orange production, 2024",
          "Soybean production, 2024",
          "Palm oil production, 2024",
          "Cotton production, 2024"
        ],
      hints: [
          "Two countries take three quarters of the square between them, and no European country appears at all.",
          "The United States is missing entirely, which is rare for a crop measured in hundreds of millions of tonnes.",
          "Measured in tonnes of the raw stalk, before anything has been extracted from it.",
          "Brazil turns much of its share into fuel for cars rather than into food."
        ],
      why: "Brazil alone is nearly half of everything the eight largest growers produce, with India second and Thailand fifth, which is the cane pattern. Rice would put India and China first and second with Brazil far down the list, and maize would be led by the United States, which is absent.",
      slug: "sugar-cane-production"
    },
    {
      family: "Ranking", form: "Lollipop · highest and lowest, 2025", exhibit: "Exhibit AF",
      type: "lollipop", diff: 5,
      truth: "Share of land covered by forest, 2025", period: "2025", unit: "% of land area",
      suffix: "%",
      data: [
        ["Micronesia",92.2], ["Suriname",91.4], ["Gabon",91.4],
        ["Palau",91], ["Solomon Islands",89.8], ["Guyana",87],
        ["Equatorial Guinea",85.8], ["Finland",74.2], ["Sweden",68.6],
        ["Japan",68.3],
        ["Brazil",58.2], ["Russia",50.8], ["Indonesia",50.7],
        ["United States",33.8], ["India",24.5], ["China",24.2],
        ["Australia",17.4], ["United Kingdom",13.6], ["Ireland",12.1]
      ],
      answer: "Share of land covered by forest",
      decoys: [
          "Share of land used for farming",
          "Share of land that is protected",
          "Share of land more than 500 metres above sea level",
          "Share of the population living in the countryside",
          "Share of land that is desert",
          "Share of land that receives more than a metre of rain",
          "Share of electricity from renewable sources"
        ],
      hints: [
          "Japan and Sweden are almost identical here, and Britain and Ireland sit at the very bottom of the rich world.",
          "Suriname, Gabon and Guyana are near ninety percent, while Britain is near thirteen.",
          "Measured as a percentage of land area, which is why Russia is only halfway up despite holding a fifth of the world's total.",
          "It is how much of the country is covered by trees."
        ],
      why: "Ireland below the United Kingdom, and Britain at 13.6% while Japan sits at 68%, is the forest-cover pattern: both islands cleared their woodland centuries ago. Farmland would invert most of this list and put Ireland near the top.",
      slug: "forest-area-as-share-of-land-area"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2020", exhibit: "Exhibit AG",
      type: "beeswarm", diff: 4,
      truth: "Average years of schooling among adults, 2020", period: "2020", unit: "years completed, adults aged 25 and over",
      data: [["Afghanistan",5.69],["Albania",10.32],["Algeria",8.18],["Argentina",9.86],["Armenia",10.54],["Australia",12.93],["Austria",10.39],["Bahrain",8.21],["Bangladesh",7.23],["Barbados",9.67],["Belgium",11.57],["Belize",10.71],["Benin",6.27],["Bolivia",9.06],["Botswana",10.58],["Brazil",8],["Brunei",9.28],["Bulgaria",10.75],["Burundi",5.05],["Cambodia",5.81],["Cameroon",7.37],["Canada",12.93],["Central African Republic",4.64],["Chile",10.74],["China",8.99],["Colombia",10.2],["Congo",6.74],["Costa Rica",9.12],["Cote d'Ivoire",6.05],["Croatia",12.03],["Cuba",11.61],["Cyprus",12.42],["Czechia",12.93],["Democratic Republic of Congo",4.85],["Denmark",11.69],["Dominican Republic",9.04],["Ecuador",9.07],["Egypt",8.01],["El Salvador",8.1],["Estonia",12.29],["Eswatini",6.46],["Fiji",11.52],["Finland",11.05],["France",11.89],["Gabon",10.18],["Gambia",4.92],["Germany",13.1],["Ghana",8.39],["Greece",11.86],["Guatemala",6.26],["Guyana",8.52],["Haiti",5.95],["Honduras",7.51],["Hungary",11.96],["Iceland",13.53],["India",7.8],["Indonesia",9.06],["Iran",9.8],["Iraq",8.27],["Ireland",13.74],["Israel",12.04],["Italy",11.51],["Jamaica",10.1],["Japan",12.83],["Jordan",10.81],["Kazakhstan",11.79],["Kenya",6.73],["Kuwait",6.62],["Kyrgyzstan",11.18],["Laos",6.05],["Latvia",11.96],["Lesotho",6.88],["Liberia",5.8],["Libya",9.57],["Lithuania",12.5],["Luxembourg",11.53],["Malawi",5.41],["Malaysia",11.96],["Maldives",8.06],["Mali",3.55],["Malta",12.09],["Mauritania",5.55],["Mauritius",10.4],["Mexico",10.18],["Moldova",10.84],["Mongolia",10],["Morocco",6.83],["Mozambique",4.22],["Myanmar",6.48],["Namibia",6.88],["Nepal",6.19],["Netherlands",11.82],["New Zealand",10.81],["Nicaragua",7.76],["Niger",3.04],["Norway",12.08],["Pakistan",6.41],["Panama",10.44],["Papua New Guinea",4.84],["Paraguay",8.83],["Peru",9.96],["Philippines",9.44],["Poland",12.01],["Portugal",9.56],["Qatar",8.52],["Romania",11.28],["Russia",11.6],["Rwanda",5.24],["Saudi Arabia",9.86],["Senegal",4.4],["Serbia",11.72],["Sierra Leone",4.99],["Singapore",13.06],["Slovakia",13.14],["Slovenia",12.06],["South Africa",10.47],["South Korea",13.68],["Spain",11.51],["Sri Lanka",10.33],["Sudan",4.38],["Sweden",11.93],["Switzerland",12.97],["Syria",7.92],["Taiwan",12.76],["Tajikistan",10.12],["Tanzania",6.87],["Thailand",9.32],["Togo",7.68],["Tonga",11.42],["Trinidad and Tobago",11.28],["Tunisia",9.29],["Turkey",8.49],["Uganda",6.69],["Ukraine",10.82],["United Arab Emirates",9.57],["United Kingdom",12.9],["United States",13.32],["Uruguay",8.76],["Venezuela",9.33],["Vietnam",8.35],["Yemen",5.56],["Zambia",8.37],["Zimbabwe",8.32]],
      label: ["Niger", "Mali", "India", "Brazil", "China", "Japan", "United Kingdom", "United States", "Ireland"],
      labelSm: ["Niger", "India", "China", "United Kingdom", "Ireland"],
      answer: "Average years of schooling among adults",
      decoys: [
          "Average number of people living in one household",
          "Average number of hours worked a day",
          "Average number of doctors per 10,000 people",
          "Average number of years spent retired",
          "Average number of children born per woman",
          "Average number of rooms in a home",
          "Average number of years lived after the age of 65"
        ],
      hints: [
          "The order runs almost exactly with national income, and the very top is Ireland, South Korea and Iceland rather than the usual large countries.",
          "Nothing is above fourteen and nothing is below three. Whatever this counts, there is a ceiling on how much of it anyone will do.",
          "Measured among adults aged twenty-five and over, so it lags what today's children are doing by decades.",
          "It is counted in years, and for most people it starts at about the age of five."
        ],
      why: "A hard ceiling near 14 with Ireland, South Korea and Iceland on top and Niger and Mali near 3 is schooling. Children per woman runs in exactly the opposite direction, with Niger highest and Ireland low.",
      slug: "mean-years-of-schooling-long-run"
    },
    {
      family: "Change over time", form: "Dumbbell · 1990 → 2024", exhibit: "Exhibit AH",
      type: "dumbbell", diff: 3,
      truth: "Carbon dioxide emitted per person, 1990 vs 2024", period: "1990 → 2024", unit: "tonnes per person a year",
      leftYear: 1990, rightYear: 2024,
      data: [
        ["Ethiopia",0.06,0.14], ["Nigeria",0.4,0.58], ["India",0.67,2.2],
        ["Brazil",1.47,2.28], ["United Kingdom",10.49,4.53], ["Germany",13.23,6.77],
        ["Japan",9.36,7.77], ["China",2.15,8.66], ["United States",20.25,14.2],
        ["Australia",16.24,14.48], ["Saudi Arabia",17.1,20.38], ["Qatar",25.96,41.27]
      ],
      answer: "Carbon dioxide emitted per person",
      decoys: [
          "Kilowatt-hours of electricity used per person each day",
          "Litres of petrol burned per person each week",
          "Kilograms of household waste thrown away per person each week",
          "Kilograms of plastic used per person each month",
          "Kilograms of meat eaten per person each month",
          "Cubic metres of water used per person each week",
          "Kilograms of steel used per person each month"
        ],
      hints: [
          "Britain and Germany both roughly halve, which is not something rich countries usually do to their own consumption of anything.",
          "Qatar's figure is nearly three hundred times Ethiopia's, and unlike most of the rich world it went up.",
          "Measured in tonnes, per person, per year.",
          "It is the greenhouse gas, divided by the population."
        ],
      why: "Britain halving from 10.5 to 4.5 while China quadruples is the emissions story, and it happened because Britain closed its coal power stations. Electricity or petrol use per person did not halve in Britain over the same period.",
      slug: "co-emissions-per-capita"
    },
    {
      family: "Change over time", form: "Dumbbell · 1990 → 2025", exhibit: "Exhibit AI",
      type: "dumbbell", diff: 2,
      truth: "Share of people living in extreme poverty, 1990 vs 2025", period: "1990 → 2025", unit: "% below the international poverty line",
      suffix: "%",
      leftYear: 1990, rightYear: 2025,
      data: [
        ["China",83.1,0.0], ["Vietnam",57.5,1.6], ["Nepal",71.1,2.4],
        ["Brazil",30.3,3.0], ["Indonesia",78.6,4.0], ["India",47.5,5.3],
        ["Bangladesh",51.2,5.9], ["Pakistan",79.5,23.0], ["Ethiopia",73.5,38.6],
        ["Nigeria",55.2,41.8], ["Kenya",32.0,45.5], ["Zambia",63.0,71.7]
      ],
      answer: "Share of people living in extreme poverty",
      decoys: [
          "Share of the population without access to electricity",
          "Share of adults who cannot read or write",
          "Share of the population living in the countryside",
          "Share of the workforce employed in farming",
          "Share of children not in school",
          "Share of the population without a mobile phone",
          "Share of the population aged under fifteen"
        ],
      hints: [
          "One country goes from more than four fifths to effectively nothing in thirty-five years, and it is the largest on the chart.",
          "Two countries move backwards, and both are in Africa. One of them is worse off today than it was in 1990.",
          "Measured as a percentage of the population, against a line that is the same everywhere once local prices are adjusted for.",
          "The line is a few dollars a day."
        ],
      why: "China falling to effectively zero while Zambia rises from 63% to 72% is the poverty pattern. Rural population and the share aged under fifteen never collapse to zero, and no measure of literacy went backwards in Kenya over these years.",
      slug: "share-of-population-in-extreme-poverty"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2020", exhibit: "Exhibit AJ",
      type: "beeswarm", diff: 4,
      truth: "Hospital beds per 1,000 people, 2020", period: "2020", unit: "beds per 1,000 people",
      data: [["Afghanistan",0.33],["Albania",2.9],["Antigua and Barbuda",3.32],["Argentina",3.19],["Armenia",4.45],["Austria",7.05],["Azerbaijan",4.35],["Bahamas",2.76],["Bahrain",1.99],["Bangladesh",0.97],["Barbados",5.64],["Belarus",10.09],["Belgium",5.53],["Belize",0.98],["Benin",0.45],["Bhutan",2.13],["Bolivia",1.37],["Botswana",2.43],["Brazil",2.49],["Brunei",3.84],["Bulgaria",7.82],["Burkina Faso",0.2],["Canada",2.54],["Chad",0.15],["Chile",2.02],["China",5],["Colombia",1.7],["Costa Rica",1.17],["Croatia",5.8],["Cuba",4.23],["Cyprus",2.17],["Czechia",6.63],["Denmark",2.59],["Dominica",3.2],["Dominican Republic",1.42],["East Timor",0.4],["Ecuador",1.32],["Egypt",1.11],["El Salvador",1.09],["Eritrea",1.08],["Estonia",4.46],["Finland",2.75],["France",5.86],["Gambia",1.14],["Georgia",4.9],["Germany",7.77],["Greece",4.2],["Guatemala",0.43],["Guyana",2.22],["Haiti",5.06],["Honduras",0.71],["Hungary",6.76],["Iceland",2.83],["India",1.61],["Indonesia",1.38],["Ireland",2.89],["Israel",3.06],["Italy",3.16],["Jamaica",1.71],["Japan",12.62],["Jordan",1.38],["Kazakhstan",6.54],["Kuwait",2.33],["Kyrgyzstan",4.04],["Laos",1.27],["Latvia",5.28],["Lebanon",2.73],["Libya",3.2],["Lithuania",6.01],["Luxembourg",4.19],["Malaysia",1.93],["Maldives",5.04],["Malta",4.36],["Mauritius",3.68],["Mexico",1],["Moldova",5.59],["Mongolia",8.23],["Montenegro",3.94],["Morocco",0.74],["Mozambique",0.71],["Myanmar",1.07],["Nepal",0.28],["Netherlands",2.88],["New Zealand",2.5],["Nicaragua",0.97],["Niger",0.28],["North Macedonia",4.76],["Norway",3.4],["Oman",1.16],["Pakistan",0.63],["Palestine",1.28],["Panama",1.92],["Paraguay",1.01],["Peru",1.67],["Philippines",0.99],["Poland",6.15],["Portugal",3.47],["Romania",7.07],["Russia",7.05],["Rwanda",0.74],["Saint Kitts and Nevis",4.39],["Saint Lucia",1.75],["Saint Vincent",4.02],["Saudi Arabia",2.54],["Serbia",5.69],["Seychelles",2.8],["Singapore",2.77],["Slovakia",5.69],["Slovenia",4.28],["South Korea",12.65],["Spain",2.94],["Sri Lanka",3.87],["Sudan",0.66],["Suriname",2.87],["Sweden",2.05],["Switzerland",4.48],["Syria",1.39],["Tajikistan",4.26],["Tanzania",0.64],["Thailand",2.32],["Togo",0.37],["Trinidad and Tobago",1.97],["Tunisia",2.42],["Turkey",2.92],["Turkmenistan",3.68],["Ukraine",6.15],["United Arab Emirates",1.91],["United Kingdom",2.42],["United States",2.71],["Uruguay",2.52],["Uzbekistan",4.77],["Venezuela",0.99]],
      label: ["Nepal", "Mexico", "India", "United Kingdom", "United States", "France", "Germany", "Belarus", "South Korea"],
      labelSm: ["Nepal", "United Kingdom", "Germany", "Belarus", "South Korea"],
      answer: "Hospital beds per 1,000 people",
      decoys: [
          "Doctors per 1,000 people",
          "Nurses per 1,000 people",
          "Deaths per 1,000 people each year",
          "Rooms per person in the average home",
          "Pharmacies per 10,000 people",
          "Cars per 10 people",
          "Ambulances per 100,000 people"
        ],
      hints: [
          "South Korea and Japan are more than four times Britain and America, and Sweden sits near the bottom of Europe.",
          "Belarus, Bulgaria and Romania are high while the Nordics are low. This is one of the few measures where the old Eastern bloc still leads.",
          "Counted per thousand people. Rich countries are scattered across the whole range, so this is a decision about how care is organised rather than how much money there is.",
          "It is what a health service has when you need to stay the night."
        ],
      why: "South Korea at 12.65 and Japan at 12.62 with Sweden at 2.05 is the giveaway, because wealth does not sort this list at all: Sweden treats people at home, Japan keeps them in. Doctors per head would put Greece and Cuba on top, and neither leads here.",
      slug: "SH.MED.BEDS.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SH.MED.BEDS.ZS"
    },
    {
      family: "Deviation", form: "Diverging bar · around zero, 2023", exhibit: "Exhibit AK",
      type: "deviation", reference: 0, diff: 3,
      truth: "Net migration, 2023", period: "2023", unit: "people, arrivals minus departures, against a zero line",
      data: [
        ["United States",1322668], ["Syria",757309], ["Germany",609553],
        ["United Kingdom",445523], ["Canada",433842], ["Egypt",305006],
        ["Japan",175003], ["Italy",150189], ["Australia",140232],
        ["Spain",119099], ["Russia",27807], ["Poland",-7824],
        ["Mexico",-101044], ["Venezuela",-112899], ["Philippines",-164284],
        ["Ukraine",-299961], ["Turkey",-318070], ["Nepal",-409782],
        ["India",-979179], ["Pakistan",-1619557]
      ],
      answer: "Net migration over one year",
      decoys: [
          "Change in population over one year",
          "Number of refugees newly recognised in a year",
          "Change in the number of people in work over one year",
          "Number of students who moved abroad to study",
          "Change in the number of people aged over 65",
          "Number of passports issued in a year",
          "Change in the number of births against a decade earlier"
        ],
      hints: [
          "Pakistan is furthest below the line and India is next, yet both countries grew by millions of people that year.",
          "Syria is near the top, which is the opposite of what a decade of headlines would lead you to expect.",
          "Measured as a number of people across a single year, and it can fall below zero, which rules out anything that only counts arrivals.",
          "It is arrivals minus departures."
        ],
      why: "Pakistan at minus 1.6 million and India at minus 979,000 while both populations still grew is the tell: this counts movement across a border in both directions, not population change. Anything that only counted arrivals could never go below the line.",
      slug: "SM.POP.NETM",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SM.POP.NETM"
    },
    {
      family: "Ranking", form: "Lollipop · 2023", exhibit: "Exhibit AL",
      type: "lollipop", diff: 2,
      truth: "Passengers carried by a country's own airlines, 2023", period: "2023", unit: "passengers carried in a year",
      data: [
        ["United States",941557000], ["China",619215886], ["Ireland",192528432],
        ["India",180415784], ["Turkey",125940241], ["Japan",120305972],
        ["United Kingdom",118945920], ["Russia",98872628], ["Indonesia",97045785],
        ["Brazil",95398485], ["Spain",94101520], ["Canada",88618000],
        ["Germany",80199572], ["Mexico",78763320], ["Australia",68958577],
        ["France",64644716], ["Vietnam",55114832], ["Colombia",42399044]
      ],
      answer: "Passengers carried by a country's own airlines",
      decoys: [
          "Passengers passing through a country's airports",
          "Tourists arriving from abroad each year",
          "International air journeys taken by residents",
          "Flights taking off each year",
          "Tonnes of air freight carried in a year",
          "Passport holders in each country",
          "Rail passengers carried each year"
        ],
      hints: [
          "One country on this chart has five million residents and sits third, above India.",
          "That country is not a destination. It is where a very large low-cost fleet happens to be registered.",
          "Counted in passengers a year and attributed to the airline's home country rather than to the airport it flew from.",
          "It counts everyone who flew with that country's own carriers."
        ],
      why: "Ireland third, above India and Japan, is the whole puzzle: Ryanair's fleet is Irish-registered, so its passengers are counted as Ireland's. Airport traffic would put Germany and Britain far above Ireland, and tourist arrivals would be led by France and Spain.",
      slug: "IS.AIR.PSGR",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/IS.AIR.PSGR"
    },
    {
      family: "Ranking", form: "Lollipop · Europe, 2024", exhibit: "Exhibit AM",
      type: "lollipop", diff: 2,
      truth: "Age at which young Europeans leave their parents\' home, 2024", period: "2024", unit: "years old, national average",
      data: [
        ["Croatia",31.3], ["Slovakia",30.9], ["Greece",30.7],
        ["Serbia",30.2], ["Italy",30.1], ["Spain",30],
        ["Portugal",28.9], ["Bulgaria",28.2], ["Malta",28.1],
        ["Ireland",26.8], ["Poland",26.7], ["Belgium",26.2],
        ["Austria",25.3], ["Germany",23.9], ["France",23.5],
        ["Netherlands",23.2], ["Estonia",22.4], ["Sweden",21.9],
        ["Denmark",21.7], ["Finland",21.4]
      ],
      answer: "Age at which young Europeans leave their parents\' home",
      decoys: [
          "Age at which Europeans first marry",
          "Age of European mothers at a first birth",
          "Age at which Europeans buy a first home",
          "Age at which Europeans start a first full-time job",
          "Age at which Europeans pass a driving test",
          "Age at which Europeans first vote in an election",
          "Age at which Europeans buy a first car"
        ],
      hints: [
          "The Nordic countries sit at the very bottom of this chart and the Mediterranean at the very top, the reverse of how most league tables on this continent run.",
          "Croatia and Finland are ten years apart. Whatever this is, it happens once, and in some countries the state pays for it while in others the family does.",
          "Measured in years as a national average. Nothing here is below twenty-one or above thirty-two.",
          "It is when they finally move out."
        ],
      why: "Finland at 21.4 and Croatia at 31.3, with the whole Nordic bloc low and southern and eastern Europe high, is the leaving-home pattern. Age at first marriage runs the other way, with Sweden and Denmark among the latest in Europe.",
      slug: "yth_demo_030",
      source: "Eurostat", sourceUrl: "https://ec.europa.eu/eurostat/databrowser/view/yth_demo_030/default/table"
    },
    {
      family: "Ranking", form: "Lollipop · highest and lowest, 2024", exhibit: "Exhibit AN",
      type: "lollipop", diff: 3,
      truth: "Share of women in work or looking for work, 2024", period: "2024", unit: "% of women aged 15 and over",
      suffix: "%",
      data: [
        ["Madagascar",82.9], ["Tanzania",80.3], ["Iceland",70.3],
        ["Vietnam",68.9], ["Netherlands",62.9], ["Sweden",61.7],
        ["China",59.4], ["United Kingdom",57.5], ["Rwanda",57.1],
        ["United States",56.6], ["Japan",55.6], ["Brazil",53.6],
        ["Mexico",47.4], ["Italy",41], ["Turkey",36.8],
        ["India",32.4], ["Pakistan",24], ["Egypt",18.5],
        ["Algeria",14.3], ["Iraq",11], ["Afghanistan",5.1],
        ["Yemen",4.7]
      ],
      answer: "Share of women in work or looking for work",
      decoys: [
          "Share of women who can read and write",
          "Share of women who have a bank account",
          "Share of women who finished secondary school",
          "Share of women who own a mobile phone",
          "Share of women who vote in national elections",
          "Share of women who are married by thirty",
          "Share of women who have given birth"
        ],
      hints: [
          "Madagascar and Tanzania are at the top, above Iceland and Sweden, so money is not what sorts this list.",
          "Italy sits twenty points below the Netherlands, closer to Turkey than to any other country in western Europe.",
          "Measured as a share of all women aged fifteen and over, from modelled labour statistics.",
          "It is whether she has a job, or is looking for one."
        ],
      why: "Madagascar and Tanzania above Iceland and Sweden is the participation pattern: in the poorest economies almost nobody can afford not to work. Literacy or bank accounts would put the Nordic countries on top and Madagascar near the bottom.",
      slug: "SL.TLF.CACT.FE.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SL.TLF.CACT.FE.ZS"
    },
    {
      family: "Ranking", form: "Lollipop · 2023", exhibit: "Exhibit AO",
      type: "lollipop", diff: 4,
      truth: "Share of a country's city dwellers who live in its largest city, 2023", period: "2023", unit: "% of the urban population",
      suffix: "%",
      data: [
        ["Mongolia",68.21], ["Panama",67.32], ["Uruguay",54.81],
        ["Latvia",48.25], ["Chile",39.54], ["Ireland",37.3],
        ["Argentina",36.9], ["Japan",32.44], ["Denmark",26.22],
        ["France",20.81], ["Canada",19.28], ["Spain",17.43],
        ["United Kingdom",16.93], ["Italy",10.52], ["Poland",8.18],
        ["United States",7.02], ["Germany",5.24], ["China",3.16]
      ],
      answer: "Share of a country's city dwellers who live in its largest city",
      decoys: [
          "Share of the population that lives in cities",
          "Share of the population born abroad",
          "Share of the population who own their home",
          "Share of the population living within 50km of the coast",
          "Share of national income earned in the largest city",
          "Share of the workforce in public administration",
          "Share of the population who commute by train"
        ],
      hints: [
          "Mongolia and Panama are at the top and Germany and China are at the bottom, which is nothing to do with how rich or how crowded they are.",
          "Germany is near the floor not because Germans avoid towns, but because it has no single dominant one. Berlin, Hamburg, Munich and Cologne share the load.",
          "It is a share of one group within another, and the denominator is the point: the countries at the bottom are not rural.",
          "One city, as a fraction of everyone in that country who lives in a city at all."
        ],
      why: "Germany at 5.2% and China at 3.2% beside Mongolia at 68% is the tell: neither is a rural country, they simply have no dominant city. A share of the whole population living in cities would put Germany near 80%.",
      slug: "EN.URB.LCTY.UR.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/EN.URB.LCTY.UR.ZS"
    },
    {
      family: "Ranking", form: "Lollipop · 2022", exhibit: "Exhibit AP",
      type: "lollipop", diff: 2,
      truth: "Health spending per person, 2022", period: "2022", unit: "US dollars per person a year",
      data: [
        ["United States",12586], ["Switzerland",10930], ["Norway",8693],
        ["Germany",6226], ["United Kingdom",5112], ["Japan",4202],
        ["South Korea",3079], ["Poland",1219], ["Brazil",871],
        ["China",755], ["Mexico",651], ["Indonesia",127],
        ["Nigeria",90], ["India",82], ["Pakistan",39],
        ["Ethiopia",27]
      ],
      answer: "Health spending per person, in dollars",
      decoys: [
          "Government spending per person on education, in dollars",
          "Spending on food per person a year, in dollars",
          "Average annual rent, in dollars",
          "Income tax paid per person a year, in dollars",
          "Spending on transport per person a year, in dollars",
          "Value of exports per person, in dollars",
          "Savings per person a year, in dollars"
        ],
      hints: [
          "The United States is not merely first here. It is about fifteen per cent clear of Switzerland and double Germany, and on almost every other measure of this kind those three sit close together.",
          "Six countries are pinned flat against the axis. Ethiopia is at twenty-seven a year against more than twelve thousand at the top, a gap of more than four hundred times.",
          "Every figure is per person per year in current dollars, and it counts what the state and the household lay out together.",
          "It is what a country lays out on keeping people well."
        ],
      why: "The United States at $12,586, about fifteen per cent clear of Switzerland and double Germany, is the health-spending signature. On education or food, America sits alongside other rich countries rather than far above them.",
      slug: "SH.XPD.CHEX.PC.CD",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD"
    },
    {
      family: "Deviation", form: "Diverging bar · around zero, 2023", exhibit: "Exhibit AQ",
      type: "deviation", reference: 0, diff: 4,
      truth: "Exports minus imports as a share of the economy, 2023", period: "2023", unit: "% of GDP, against a zero line",
      suffix: "%",
      data: [
        ["Singapore",37.16], ["Ireland",33.4], ["Norway",15.41],
        ["Switzerland",10.9], ["Netherlands",9.94], ["Denmark",9],
        ["Vietnam",8.48], ["Poland",5.74], ["Germany",3.97],
        ["Brazil",2.27], ["China",2.07], ["Italy",1.56],
        ["United Kingdom",-1.17], ["Mexico",-1.44], ["Japan",-1.48],
        ["India",-1.61], ["Turkey",-1.86], ["United States",-2.83],
        ["Ethiopia",-7.41], ["Pakistan",-7.48]
      ],
      answer: "Exports minus imports as a share of the economy",
      decoys: [
          "Government surplus or deficit as a share of the economy",
          "Net foreign investment as a share of the economy",
          "Growth of the economy over the year, in per cent",
          "Household savings as a share of income",
          "Government debt interest as a share of the economy",
          "Change in the value of the currency, in per cent",
          "Share of the economy earned from tourism"
        ],
      hints: [
          "Singapore and Ireland are far clear of everyone else, and both are places where goods and profits pass through rather than stop.",
          "Britain, America, Japan and India all sit below the line, and all four have done for decades.",
          "Measured against a line at zero, as a percentage of national income, and it is negative as often as not.",
          "It is what a country sells abroad minus what it buys."
        ],
      why: "Singapore at +37% and Ireland at +33%, with the United States, Britain, Japan and India all below zero, is the trade-balance pattern: both small economies re-export heavily and book multinational profits. A budget balance would not put Ireland thirty points clear of Germany.",
      slug: "NE.RSB.GNFS.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/NE.RSB.GNFS.ZS"
    },
    {
      family: "Change over time", form: "Dumbbell · 1990 → 2024", exhibit: "Exhibit AR",
      type: "dumbbell", diff: 3,
      truth: "Share of the population aged 65 and over, 1990 vs 2024", period: "1990 → 2024", unit: "% of the population",
      suffix: "%",
      leftYear: 1990, rightYear: 2024,
      data: [
        ["Uganda",3.06,2.19], ["Kenya",2.16,2.97], ["Nigeria",3.14,3.05],
        ["India",4.04,7.15], ["Turkey",4.74,10.28], ["Brazil",4.12,11.05],
        ["China",5.35,14.67], ["United States",12.31,17.93], ["United Kingdom",15.87,19.5],
        ["Germany",14.87,23.2], ["Italy",14.96,24.62], ["Japan",12.16,29.78]
      ],
      answer: "Share of the population aged 65 and over",
      decoys: [
          "Share of the population who have retired",
          "Share of the population receiving a state pension",
          "Share of the population with a long-term illness",
          "Share of the population living alone",
          "Share of the population who own their home outright",
          "Share of the population who have grandchildren",
          "Share of the population who need daily care"
        ],
      hints: [
          "Japan starts below Britain, Germany and Italy and finishes ten points above all three. Nothing else about Japan moved that far in the same years.",
          "One country here went backwards. It is in east Africa, and its birth rate is among the highest in the world.",
          "Measured as a percentage of everyone alive, at two dates thirty-four years apart.",
          "It is how much of a country has passed its sixty-fifth birthday."
        ],
      why: "Japan going from 12.2%, below Britain and Italy, to 29.8% in thirty-four years is the ageing signature, and Uganda falling from 3.1% to 2.2% is the tell: a country whose birth rate stays very high gets younger, not older.",
      slug: "SP.POP.65UP.TO.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SP.POP.65UP.TO.ZS"
    },
    {
      family: "Ranking", form: "Rank slope · 1990 → 2024", exhibit: "Exhibit AS",
      type: "slope", diff: 3,
      truth: "World ranking of the largest economies, 1990 vs 2024", period: "1990 → 2024", unit: "rank by GDP in current dollars",
      leftYear: 1990, rightYear: 2024,
      ranks: [
        ["United States",1,1], ["China",10,2], ["Germany",3,3],
        ["Japan",2,4], ["India",11,5], ["United Kingdom",6,6],
        ["France",4,7], ["Italy",5,8], ["Canada",7,9],
        ["Russia",8,10], ["Brazil",9,11], ["South Korea",12,12]
      ],
      answer: "World ranking of the largest economies",
      decoys: [
          "World ranking of countries by manufacturing output",
          "World ranking of countries by exports",
          "World ranking of countries by stock market value",
          "World ranking of countries by government spending",
          "World ranking of countries by energy used",
          "World ranking of countries by company headquarters",
          "World ranking of countries by patents filed"
        ],
      hints: [
          "Two lines climb almost the full height of the chart, and between them those two countries hold a third of everyone alive.",
          "The steepest faller is Japan, and it did not shrink. It stood still for thirty years while the others grew.",
          "Ranked on an annual total in current dollars, so exchange rates move these lines as much as growth does.",
          "It is the size of the economy."
        ],
      why: "China rising from tenth to second and India from eleventh to fifth while the United States holds first is the GDP pattern. On manufacturing output China was already high in 1990 and would now lead by a distance rather than sit second.",
      slug: "NY.GDP.MKTP.CD",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"
    },
    {
      family: "Part-to-whole", form: "Treemap · the twelve largest exporters", exhibit: "Exhibit AT",
      type: "treemap", diff: 3,
      truth: "Value of goods exported, 2023", period: "2023", unit: "US dollars",
      total: 12978367000000,
      data: [
        ["China",3379044000000], ["United States",2018059000000], ["Germany",1702278000000],
        ["Netherlands",935047000000], ["Japan",717256000000], ["Italy",676724000000],
        ["France",651122000000], ["South Korea",632226000000], ["Mexico",593001000000],
        ["Belgium",578515000000], ["Canada",570079000000], ["United Kingdom",525016000000]
      ],
      answer: "Value of goods exported, 2023",
      decoys: [
          "Value of goods imported, 2023",
          "Size of the economy, 2023",
          "Value of services exported, 2023",
          "Manufacturing output, 2023",
          "Government spending, 2023",
          "Value of oil and gas imported, 2023",
          "Value of goods sold online, 2023"
        ],
      hints: [
          "The Netherlands is fourth and Belgium tenth, both far above their weight. Look at what the two have in common on a map.",
          "India is missing altogether, and it has a bigger economy than eight of the twelve here.",
          "Counted in dollars for the year, and it counts things that travel in containers rather than anything done over a wire.",
          "It is what each country sells abroad."
        ],
      why: "Rotterdam and Antwerp put the Netherlands fourth and Belgium tenth, far above their economic weight, because goods landing there are re-exported. On imports the United States would lead comfortably; here it is second to China.",
      slug: "TX.VAL.MRCH.CD.WT",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/TX.VAL.MRCH.CD.WT"
    },
    {
      family: "Ranking", form: "Lollipop · 2021", exhibit: "Exhibit AU",
      type: "lollipop", diff: 2,
      truth: "Deaths on the roads per 100,000 people, 2021", period: "2021", unit: "deaths per 100,000 people a year",
      data: [
        ["Zimbabwe",29.9], ["South Africa",24.5], ["Iran",20.6],
        ["Vietnam",17.7], ["China",17.4], ["Nigeria",17.2],
        ["India",14.6], ["United States",14.2], ["Mexico",12],
        ["Russia",10.6], ["Australia",4.5], ["Japan",2.7],
        ["United Kingdom",2.4], ["Sweden",2.1]
      ],
      answer: "Deaths on the roads per 100,000 people",
      decoys: [
          "Murders per 100,000 people",
          "Deaths from air pollution per 100,000 people",
          "Deaths at work per 100,000 workers",
          "Deaths from drowning per 100,000 people",
          "Deaths in fires per 100,000 people",
          "Deaths from falls per 100,000 people",
          "Deaths from snakebite per 100,000 people"
        ],
      hints: [
          "The United States is six times Britain and Sweden here, and level with India. Very few measures of this kind put it in that company.",
          "Sweden is lowest because of a policy its parliament adopted in 1997 and named after the number it was aiming at.",
          "Counted per hundred thousand people a year. Top to bottom is a fourteen-fold gap.",
          "Every one of these happened in traffic."
        ],
      why: "The United States at 14.2, six times Britain and level with India, is the road-death pattern rather than the murder one: America's homicide rate is under six, and Zimbabwe does not lead the world in murder. Sweden's 2.1 is Vision Zero, adopted in 1997.",
      slug: "RS_198",
      source: "WHO Global Health Observatory", sourceUrl: "https://www.who.int/data/gho"
    },
    {
      family: "Change over time", form: "Dumbbell · 1991 → 2024", exhibit: "Exhibit AV",
      type: "dumbbell", diff: 3,
      truth: "Share of workers employed in farming, 1991 vs 2024", period: "1991 → 2024", unit: "% of everyone in work",
      suffix: "%",
      leftYear: 1991, rightYear: 2024,
      data: [
        ["United Kingdom",2.42,0.87], ["United States",2.94,1.57], ["Portugal",6.56,2.86],
        ["Poland",26.27,6.5], ["Brazil",16.1,7.72], ["Turkey",46.06,14.55],
        ["China",59.64,22.22], ["Vietnam",73.99,25.87], ["Indonesia",47.66,27.96],
        ["India",63.13,42.35], ["Ethiopia",77.15,61.01], ["Uganda",62.38,65.41]
      ],
      answer: "Share of workers employed in farming",
      decoys: [
          "Share of the population living in the countryside",
          "Share of workers employed in factories",
          "Share of national income earned from farming",
          "Share of land used for farming",
          "Share of workers who are self-employed",
          "Share of workers with no written contract",
          "Share of workers who are women"
        ],
      hints: [
          "One country on this chart moved the wrong way across thirty-three years, and it is in east Africa.",
          "Vietnam fell from three quarters to a quarter inside a single working lifetime.",
          "Measured as a share of everyone in work rather than of everyone alive, which is how Britain gets below one percent.",
          "It counts the people who grow the food."
        ],
      why: "Uganda rising from 62% to 65% while Vietnam falls from 74% to 26% is the tell, and Britain at 0.87% shows this is a share of the workforce rather than of the population: far more than one percent of Britons live in the countryside.",
      slug: "SL.AGR.EMPL.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/SL.AGR.EMPL.ZS"
    },
    {
      family: "Distribution", form: "Beeswarm · every country, 2023", exhibit: "Exhibit AW",
      type: "beeswarm", diff: 3,
      truth: "Kilograms of fish and seafood eaten per person, 2023", period: "2023", unit: "kilograms per person a year",
      data: [["Afghanistan",0.38],["Albania",8.6],["Algeria",2.75],["Angola",14.34],["Antigua and Barbuda",54.51],["Argentina",7.11],["Armenia",4.86],["Australia",24.24],["Austria",14.12],["Azerbaijan",2.14],["Bahamas",27.68],["Bahrain",19.76],["Bangladesh",26.98],["Barbados",43.16],["Belarus",12.46],["Belgium",23.93],["Belize",16.94],["Benin",14.82],["Bhutan",6.26],["Bolivia",2.12],["Bosnia and Herzegovina",5.86],["Botswana",2.22],["Brazil",8.18],["Bulgaria",7.18],["Burkina Faso",10.49],["Burundi",2.4],["Cambodia",39.42],["Cameroon",18.12],["Canada",20.82],["Cape Verde",10.67],["Chad",5.61],["Chile",14.36],["China",41.68],["Colombia",10.31],["Comoros",16.98],["Congo",23.19],["Costa Rica",17.83],["Cote d'Ivoire",23.7],["Croatia",19.89],["Cyprus",17.96],["Czechia",10.37],["Democratic Republic of Congo",3.29],["Denmark",22.56],["Djibouti",5.31],["Dominica",25.58],["Dominican Republic",17.14],["East Timor",6.97],["Ecuador",6.45],["Egypt",20.5],["El Salvador",7.22],["Estonia",12.7],["Eswatini",3.79],["Ethiopia",0.5],["Fiji",27.95],["Finland",31.49],["France",32.64],["Gabon",27.03],["Gambia",20.17],["Georgia",10.33],["Germany",12.98],["Ghana",23.62],["Greece",19.63],["Grenada",20.33],["Guatemala",3.77],["Guinea",10.65],["Guinea-Bissau",2.35],["Guyana",24.76],["Haiti",5.42],["Honduras",4.39],["Hungary",6.46],["Iceland",83.81],["India",8.73],["Indonesia",40.42],["Iran",11.3],["Iraq",2.27],["Ireland",19.27],["Israel",24.75],["Italy",29.39],["Jamaica",27.85],["Japan",44.98],["Jordan",4.77],["Kazakhstan",3.93],["Kenya",2.86],["Kiribati",72.27],["Kuwait",12.97],["Kyrgyzstan",1.46],["Laos",28.52],["Latvia",24.49],["Lebanon",4.74],["Lesotho",1.92],["Liberia",4.75],["Libya",12.88],["Lithuania",28.51],["Luxembourg",30.29],["Madagascar",3.67],["Malawi",8.77],["Malaysia",51.03],["Maldives",79.74],["Mali",8.64],["Malta",31.1],["Marshall Islands",44.55],["Mauritania",7.6],["Mauritius",29.4],["Mexico",13.55],["Micronesia",48.98],["Moldova",16.3],["Mongolia",1.03],["Montenegro",11.92],["Morocco",16.71],["Mozambique",12.87],["Myanmar",40.35],["Namibia",9.67],["Nauru",26.02],["Nepal",4.28],["Netherlands",19.08],["New Zealand",24.61],["Nicaragua",7.34],["Niger",1.87],["Nigeria",6.9],["North Macedonia",8.01],["Norway",49.1],["Oman",28.15],["Pakistan",1.35],["Panama",14.89],["Papua New Guinea",7.1],["Paraguay",5.33],["Peru",25.94],["Philippines",26.34],["Poland",11.15],["Portugal",53.49],["Qatar",22.03],["Romania",8.7],["Russia",22.8],["Rwanda",5.15],["Saint Kitts and Nevis",36.4],["Saint Lucia",24.95],["Saint Vincent",20.05],["Samoa",46.62],["Sao Tome and Principe",26.52],["Saudi Arabia",12.92],["Senegal",13.75],["Serbia",8.45],["Seychelles",42.91],["Sierra Leone",24.45],["Slovakia",10.61],["Slovenia",11.21],["Solomon Islands",30.49],["Somalia",1.68],["South Africa",5.59],["South Korea",52.82],["South Sudan",3],["Spain",36.8],["Sri Lanka",22.73],["Sudan",0.89],["Suriname",16.67],["Sweden",30.62],["Switzerland",16.46],["Syria",0.8],["Taiwan",30.4],["Tajikistan",0.91],["Tanzania",6.4],["Thailand",28.62],["Togo",9.58],["Tonga",28.58],["Trinidad and Tobago",17.96],["Tunisia",15.88],["Turkey",5.32],["Turkmenistan",2.36],["Tuvalu",55.82],["Uganda",15.41],["Ukraine",16.86],["United Arab Emirates",23.11],["United Kingdom",17.7],["United States",21.94],["Uruguay",11.93],["Uzbekistan",5.21],["Vanuatu",30.04],["Venezuela",8.75],["Vietnam",40.06],["Yemen",2.02],["Zambia",12.89],["Zimbabwe",2.63]],
      label: ["Mongolia", "Ethiopia", "India", "United Kingdom", "United States", "Norway", "Japan", "Portugal", "Iceland"],
      labelSm: ["Mongolia", "India", "United Kingdom", "Japan", "Iceland"],
      answer: "Kilograms of fish and seafood eaten per person a year",
      decoys: [
          "Kilograms of meat eaten per person a year",
          "Kilograms of rice eaten per person a year",
          "Kilograms of cheese eaten per person a year",
          "Litres of milk drunk per person a year",
          "Kilograms of fruit eaten per person a year",
          "Kilograms of potatoes eaten per person a year",
          "Kilograms of bread eaten per person a year"
        ],
      hints: [
          "Iceland, the Maldives and Kiribati are the three loneliest dots on the right, and Mongolia is almost at zero.",
          "Portugal sits above Japan, which surprises everyone except the Portuguese.",
          "Measured in kilograms per person per year, from national food supply figures rather than from asking anyone.",
          "It all comes out of the water."
        ],
      why: "Iceland at 83.8kg, the Maldives at 79.7 and Kiribati at 72.3, with landlocked Mongolia at 1.0, is the seafood pattern. Meat would put Mongolia near the very top instead of the very bottom.",
      slug: "fish-and-seafood-consumption-per-capita"
    },
    {
      family: "Ranking", form: "Lollipop · 2020", exhibit: "Exhibit AX",
      type: "lollipop", diff: 4,
      truth: "Share of the workforce serving in the armed forces, 2020", period: "2020", unit: "% of the total labour force",
      suffix: "%",
      data: [
        ["Eritrea",13.29], ["North Korea",8.62], ["Israel",4.23],
        ["Jordan",3.98], ["Greece",3.2], ["South Korea",2.01],
        ["Russia",1.98], ["Singapore",1.72], ["Turkey",1.61],
        ["France",1], ["United States",0.84], ["Brazil",0.76],
        ["India",0.58], ["United Kingdom",0.45], ["Germany",0.42],
        ["Japan",0.38], ["China",0.33], ["Nigeria",0.23]
      ],
      answer: "Share of the workforce serving in the armed forces",
      decoys: [
          "Share of national income spent on defence",
          "Share of the workforce employed by the government",
          "Share of the workforce in the police",
          "Share of adults who have done military service",
          "Share of the workforce working abroad",
          "Share of the workforce in farming",
          "Share of young men in full-time education"
        ],
      hints: [
          "The United States is eleventh, below Greece and Jordan, and China is second from last.",
          "The two countries at the top both require every young person to serve, and in one of them that service has no fixed end.",
          "Measured as a share of everyone in work. This is a headcount, not a budget.",
          "It counts soldiers, sailors and air crew."
        ],
      why: "China second from last and the United States eleventh is the giveaway that this counts people rather than money: both have enormous forces in absolute terms and enormous workforces to divide them by. On defence spending as a share of income the United States would be near the top.",
      slug: "MS.MIL.TOTL.TF.ZS",
      source: "World Bank", sourceUrl: "https://data.worldbank.org/indicator/MS.MIL.TOTL.TF.ZS"
    }
  ];