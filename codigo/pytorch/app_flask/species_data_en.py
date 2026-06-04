"""
raptors-cnn — English translations of SPECIES_DETAILS.

Mirrors the structure of `species_data.py`. Used by `species_info.py` when the
active locale is `en` (with silent per-field fallback to Spanish if missing).

All 53 diurnal raptors of Mexico (AOS 2024) are translated. Numeric fields
(`length_cm`, `wingspan_cm`) are language-independent and remain in the Spanish
file only.

Status: 53 / 53 species translated as of June 2026.
"""
from __future__ import annotations

SPECIES_DETAILS_EN: dict[str, dict[str, str]] = {

    # ──────────────────────────────────────────────────────────────────────
    "Accipiter_striatus": {
        "distribution":
            "Breeds in boreal and temperate forests of North America; migrates "
            "south and crosses all of Mexico in autumn. The Veracruz corridor "
            "concentrates the main flow between September and November.",
        "diet":
            "Small birds taken in fast ambushes through forest; occasionally "
            "bats and large insects.",
        "behavior":
            "Fast flight with rapid wingbeats and short glides. Solitary in "
            "migration. Hard to distinguish from Cooper's Hawk at distance.",
        "migration":
            "Complete migrator. Migration peak: mid-October to early November.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Short rounded wings, long square tail. Small size. Proportionally "
            "smaller head than Cooper's Hawk.",
        "best_months": "October-November",
        "did_you_know":
            "It is the smallest of the Nearctic accipiters. When attacking, it "
            "can manoeuvre between branches at extremely high speeds.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Aquila_chrysaetos": {
        "distribution":
            "Holarctic distribution. In Mexico it inhabits arid mountain "
            "ranges of Chihuahua, Sonora, Durango, Coahuila, Zacatecas and "
            "Hidalgo, up to the Trans-Mexican Volcanic Belt.",
        "diet":
            "Medium-sized mammals (rabbits, hares, ground squirrels), "
            "occasionally reptiles and carrion in winter.",
        "behavior":
            "Powerful soaring flight with wings held in a slight dihedral. "
            "Defends large territories. Pairs often hunt cooperatively.",
        "migration":
            "Partial migrator. Adults from the north can reach central "
            "Mexico in winter.",
        "iucn_status": "Least Concern (regionally declining)",
        "diagnostic":
            "Golden nape, long broad wings with fingered tips. Long tail "
            "(longer than in Bald Eagle).",
        "best_months": "Year-round in north-central sierras",
        "did_you_know":
            "Pre-Hispanic national bird of Mexico, depicted on the flag. "
            "It can dive at over 320 km/h when attacking prey.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_atricapillus": {
        "distribution":
            "Boreal and temperate forests of North America. In Mexico, "
            "observation is rare, mainly in conifer forests of the northern "
            "Sierra Madre.",
        "diet":
            "Medium-sized birds and mammals taken in forest. Aggressive in "
            "defence of breeding territory.",
        "behavior":
            "Powerful flight through dense forest. Aggressive territorial "
            "defence during breeding season.",
        "migration":
            "Partial migration. Rarely reaches the Neotropics — exceptional records.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Large size for an Accipiter (now Astur per AOS 2023). Wide rounded "
            "tail, very marked white supercilium in adults.",
        "best_months": "October-February (occasional winter records)",
        "did_you_know":
            "Reclassified from genus Accipiter to genus Astur by the AOS in "
            "2023, together with Cooper's Hawk, based on phylogenomic studies. "
            "Its English common name was also changed to 'American Goshawk' to "
            "distinguish it from the Eurasian one.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_cooperii": {
        "distribution":
            "Deciduous and mixed forests of North America. Migrates to Mexico "
            "and Central America in winter. Common on migration and as an "
            "urban resident in many Mexican cities.",
        "diet":
            "Medium-sized birds (doves, blackbirds, quail) and small mammals.",
        "behavior":
            "Similar to Sharp-shinned Hawk but larger and with straighter "
            "flight. Ambush hunter on forest edges.",
        "migration":
            "Complete migrator. Migration peak: October-November.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Larger than Sharp-shinned, head noticeably larger, long rounded "
            "tail (not square). Dark crown contrasting with paler nape.",
        "best_months": "October-November",
        "did_you_know":
            "Reclassified from Accipiter cooperii to Astur cooperii by the AOS "
            "in 2023. One of the raptors that has adapted best to urban environments.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Busarellus_nigricollis": {
        "distribution":
            "Tropical lowlands from Mexico (Gulf and southern Pacific slopes) "
            "to Argentina. In Mexico: Veracruz, Tabasco, Chiapas, Oaxaca and "
            "southern Sinaloa.",
        "diet":
            "Fish specialist; also amphibians, aquatic reptiles and "
            "crustaceans. Hunts from a perch by plunging into water.",
        "behavior":
            "Solitary. Perches on emergent trees over wetlands, rivers and "
            "mangroves. Relatively slow flight with deep wingbeats.",
        "migration":
            "Sedentary resident with local dispersal between wetlands.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Intense reddish-cinnamon plumage with white head and a distinctive "
            "black collar. Broad wings, short tail. Tarsi with rough scales for "
            "gripping fish.",
        "best_months": "Year-round (tropical wetlands)",
        "did_you_know":
            "Its tarsi bear small spicules (similar to those of the Osprey) "
            "that allow it to grip slippery fish — one of the few New World "
            "birds outside Pandion with this adaptation.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_albonotatus": {
        "distribution":
            "Southwestern USA, Mexico, Central America and northern South "
            "America. In Mexico: canyons, pine-oak forests and dry forests "
            "across most of the country.",
        "diet":
            "Reptiles, small mammals and birds. Surprises prey by mimicking "
            "the Turkey Vulture.",
        "behavior":
            "Aggressive mimicry: flies in a shallow dihedral, almost identical "
            "to a Turkey Vulture, to approach prey that ignore vultures.",
        "migration":
            "Partial migrator. Resident populations across much of Mexico.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Entirely black plumage, tail with broad white bands. Small "
            "vulture-like head. V-shaped flight profile.",
        "best_months": "March-October (local resident)",
        "did_you_know":
            "Classic case of aggressive Batesian mimicry: it imitates the "
            "Turkey Vulture (a visually similar non-threat) to approach victims "
            "undetected.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_brachyurus": {
        "distribution":
            "Southern Florida, Mexico and Central America to Argentina. In "
            "Mexico it inhabits tropical evergreen forests and cloud forests "
            "of the Gulf and southern Pacific slopes.",
        "diet":
            "Small birds caught in flight; occasionally mammals and arboreal "
            "lizards.",
        "behavior":
            "Hunts from height — circles high and stoops on prey. Exists in "
            "two morphs: light and dark.",
        "migration":
            "Mostly sedentary with local altitudinal dispersal.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Short tail for a Buteo. Light morph with white breast; dark morph "
            "uniformly black.",
        "best_months": "Year-round (resident)",
        "did_you_know":
            "One of the smallest raptors in the Buteo genus. Its high-altitude "
            "stoop hunting technique distinguishes it from other Buteos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_jamaicensis": {
        "distribution":
            "All of North America and Mexico to Panama. Partial migrator; "
            "common resident in temperate and semi-arid zones, and wintering "
            "in southern Mexico.",
        "diet":
            "Small mammals (mice, ground squirrels), reptiles and birds.",
        "behavior":
            "Generalist hunter. Broad thermal soaring, long glide, perch hunting.",
        "migration":
            "Partial migrator. Migration peak in the Gulf corridor: October-November.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Red tail in adults (immediate diagnostic mark). Broad wings with "
            "fingered tips, dark belly band.",
        "best_months": "October-March",
        "did_you_know":
            "Its hunting call is one of the most widely used in cinema as a "
            "generic eagle sound. It shows the greatest plumage variation of "
            "any Buteo (12+ subspecies/morphs).",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_lagopus": {
        "distribution":
            "Breeds in circumpolar Arctic tundra. Migrates to the southern USA "
            "and northern Mexico in winter. In Mexico: rare winter visitor in "
            "Chihuahua, Sonora and northern Coahuila.",
        "diet":
            "Small mammals, especially lemmings on breeding grounds; voles "
            "on wintering grounds.",
        "behavior":
            "Only Nearctic Buteo that regularly hovers. Hunts on the wing "
            "over open country.",
        "migration":
            "Complete migrator. Reaches the south only in extreme winters.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Tarsi feathered down to the toes (hence the name). Dark subterminal "
            "tail band, dark carpal patch.",
        "best_months": "December-February (irregular)",
        "did_you_know":
            "It is the only Buteo that routinely hovers without wind. Its "
            "Arctic distribution makes it a raptor adapted to extreme temperatures.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_lineatus": {
        "distribution":
            "Moist deciduous forests of the eastern USA and northeastern "
            "Mexico. In Mexico: winter migrant and local resident in Tamaulipas, "
            "Nuevo León and northern Veracruz.",
        "diet":
            "Reptiles (lizards, snakes), amphibians, small mammals and birds.",
        "behavior":
            "Perch hunter in riparian forest. High-pitched, repeated call very "
            "distinctive on territory.",
        "migration":
            "Partial migrator. Light peak in Veracruz: October-November.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Translucent 'crescents' on inner primaries (visible against the "
            "light). Reddish shoulders in adults, rufous-barred breast.",
        "best_months": "October-March",
        "did_you_know":
            "One of the few raptors that holds lifelong breeding territories, "
            "returning to the same nest for up to 20 consecutive years.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_plagiatus": {
        "distribution":
            "Riparian forests and tropical lowland forests of southern USA, "
            "Mexico and Central America. In Mexico: widely distributed across "
            "tropical and subtropical lowlands.",
        "diet":
            "Reptiles (especially iguanas), amphibians, small mammals.",
        "behavior":
            "Hunts from a perch and on low glides. Vocalises with a unique "
            "descending whistle.",
        "migration":
            "Sedentary with local dispersal. Partial migration in the north of "
            "its range.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Uniform pale grey plumage in adults. Tail with two broad white "
            "bands. Formerly Buteo nitidus — split in 2012 (B. plagiatus in "
            "North America, B. nitidus in South America).",
        "best_months": "Year-round (resident)",
        "did_you_know":
            "Previously considered the same species as B. nitidus from South "
            "America. Genetic studies showed in 2012 that they are distinct "
            "species (AOS split).",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_platypterus": {
        "distribution":
            "Temperate forests of eastern North America. Migrates to the "
            "Neotropics in autumn. STAR of the Veracruz corridor — millions "
            "per season.",
        "diet":
            "Reptiles, amphibians, small mammals, large insects during migration.",
        "behavior":
            "Flight in large 'kettles' (thermal spirals) during migration. "
            "Conserves energy by soaring almost without flapping.",
        "migration":
            "Complete and obligate migrator. Extreme peak in Veracruz: "
            "September 15-25, up to 30,000 individuals/hour.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Short broad wings, tail with broad white and black bands. Smaller "
            "than most Buteos.",
        "best_months": "September (peak) - October",
        "did_you_know":
            "Forms the largest documented migratory kettles in the world. 99% "
            "of the global population passes through the Gulf corridor during "
            "migration.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_regalis": {
        "distribution":
            "Prairies and semi-deserts of western North America. In Mexico: "
            "regular winter visitor in grasslands of Chihuahua, Sonora, "
            "Durango and the northern Bajío.",
        "diet":
            "Medium-sized mammals (prairie dogs, rabbits, marmots), "
            "occasionally birds.",
        "behavior":
            "Hunts from a perch or on the wing. Powerful flight, long glide.",
        "migration":
            "Partial migrator. Juveniles travel farther south than adults.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Largest North American Buteo. Ferruginous (reddish-brown) "
            "colouration on wings and legs. Whitish tail with rufous tint.",
        "best_months": "November-February",
        "did_you_know":
            "It is the largest Buteo in North America. Its feathered tarsi "
            "(like B. lagopus) are an adaptation to the cold of the Great Plains.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_swainsoni": {
        "distribution":
            "Breeds in prairies of western North America. MIGRATES all the way "
            "to Argentina — one of the longest journeys of any Buteo.",
        "diet":
            "Large insects (grasshoppers, dragonflies) during migration; small "
            "mammals and reptiles on breeding grounds.",
        "behavior":
            "Forms large migratory 'kettles' together with Broad-winged Hawk. "
            "Adults barely eat during the journey.",
        "migration":
            "Extreme complete migrator: up to 14,000 km round trip. "
            "Peak in Veracruz: October.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Long pointed wings. Typical adult with reddish chest, light belly, "
            "dark primaries. Significant polymorphism.",
        "best_months": "October",
        "did_you_know":
            "It performs one of the longest migrations of any raptor: 14,000 km "
            "round trip between North America and Argentina each year.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_anthracinus": {
        "distribution":
            "Tropical and subtropical lowlands from Mexico to South America. "
            "In Mexico: coastal wetlands, mangroves and tropical riparian zones "
            "of the Gulf and Pacific.",
        "diet":
            "Crabs, fish, amphibians and reptiles. Riparian specialist.",
        "behavior":
            "Solitary. Hunts from a low perch over water. Slow flight, broad "
            "wings and short tail. Vocalises with prolonged whistles.",
        "migration":
            "Mostly resident; some populations in northern Mexico are partial "
            "migrators.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Matte black plumage. One broad white band in the centre of the "
            "tail (plus a thin one at the tip). Long yellow legs; bicoloured "
            "bill.",
        "best_months": "Year-round",
        "did_you_know":
            "Part of the 'black hawk complex' together with B. urubitinga and "
            "B. solitarius. To distinguish juveniles, fine analysis of the tail "
            "pattern and underwing coverts is required.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_solitarius": {
        "distribution":
            "Montane forests and ravines from Mexico to Argentina. In Mexico: "
            "rare and scattered records in the Sierra Madre Oriental, Occidental "
            "and del Sur, Chiapas and Oaxaca. Poorly known species.",
        "diet":
            "Snakes, medium-sized arboreal mammals and birds. Cryptic habits.",
        "behavior":
            "Solitary and silent. High soaring over canyons and forested slopes. "
            "Rarely seen perched.",
        "migration":
            "Sedentary resident.",
        "iucn_status": "Near Threatened",
        "diagnostic":
            "Adult entirely dark slate grey, short tail with a single broad "
            "white band. Wings extraordinarily broad and short, projecting well "
            "beyond the tail in glide.",
        "best_months": "Year-round (extremely difficult to observe)",
        "did_you_know":
            "Status poorly known in Mexico; the few confirmed records are at "
            "mid altitudes in cloud forest and remote ravines. Listed as 'Near "
            "Threatened' by IUCN and 'Endangered' (P) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_urubitinga": {
        "distribution":
            "Tropical lowlands from Mexico (Gulf and southern Pacific slopes) "
            "to Argentina. More common south of Veracruz, in Chiapas, Oaxaca "
            "and Yucatán.",
        "diet":
            "Reptiles, amphibians, crabs, fish and small birds. Occasional carrion.",
        "behavior":
            "Similar to B. anthracinus but larger and with more forest-oriented "
            "habits. Hunts from a low perch, also patrols shorelines and roads.",
        "migration":
            "Sedentary resident.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Black plumage. Tail with TWO broad white bands (vs. one in B. "
            "anthracinus). Yellow feet and cere, bicoloured bill. Clearly larger size.",
        "best_months": "Year-round (highest concentration in tropical wetlands)",
        "did_you_know":
            "In 2018 a vagrant individual appeared in Maine, USA, generating a "
            "stir among American birders, but its usual range ends right at "
            "southeastern Mexico.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Caracara_plancus": {
        "distribution":
            "Almost all of Mexico except the great northern Altiplano deserts. "
            "Especially common in grasslands, savannas and scrublands with "
            "human presence.",
        "diet":
            "Carrion, reptiles, amphibians, large insects, small mammals and "
            "eggs. Total opportunist.",
        "behavior":
            "Walks extensively on the ground. Forms groups at carcasses together "
            "with vultures. Direct flight with slow wingbeats; rarely soars in "
            "thermals like a Buteo.",
        "migration":
            "Sedentary resident. Local movements following food availability.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Large bluish-grey bill, bare red face, black crest; white chest "
            "and neck barred in black; wings with light primaries visible in flight.",
        "best_months": "Year-round",
        "did_you_know":
            "Featured in many Mesoamerican mythologies. It is the only "
            "Neotropical raptor that regularly walks on the ground to forage, "
            "behaviour inherited from its common ancestor with the falcons.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Cathartes_aura": {
        "distribution":
            "Broad distribution across the Americas. Very common throughout "
            "Mexico both as a resident and as a northern migrant.",
        "diet":
            "Almost exclusively carrion. Extraordinary sense of smell to detect "
            "decomposition gases.",
        "behavior":
            "Constant soaring in a marked dihedral (V). Characteristic lateral "
            "rocking. Forms communal roosts.",
        "migration":
            "Partial migration. Northern populations migrate en masse through "
            "Veracruz in October.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Marked V-shaped flight, small bare red head in adults. Long wings "
            "with silvery secondaries seen from below.",
        "best_months": "Year-round, migration peak October",
        "did_you_know":
            "Has one of the finest senses of smell among birds — it can detect "
            "carrion at over 1 km. The only Cathartidae that uses smell for foraging.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Cathartes_burrovianus": {
        "distribution":
            "Tropical savannas and wetlands of Mexico (Veracruz, Tabasco, "
            "Campeche, Quintana Roo, Chiapas) to South America. Ecologically "
            "replaces C. aura in low grasslands.",
        "diet":
            "Carrion, mainly small animals recently dead in grasslands and "
            "wetlands. Like C. aura, locates prey by smell.",
        "behavior":
            "Marked V-shaped flight, very low (1-3 m above grass). Solitary or "
            "in pairs; does not form kettles. Yellow-coloured head instead of red.",
        "migration":
            "Sedentary; local movements depending on humidity.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Bare yellow head with orange/blue tints; dark brown plumage; "
            "shorter tail than C. aura. Low flight over grasslands (not high soaring).",
        "best_months": "Year-round in southeastern wetlands",
        "did_you_know":
            "One of three vultures that smell out carrion — the other Cathartes "
            "(C. melambrotus, from the Amazon) does not reach Mexico. Its "
            "preference for flooded grasslands makes it a good indicator of "
            "healthy wetlands.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Chondrohierax_uncinatus": {
        "distribution":
            "Tropical forests from Mexico to Argentina. In Mexico: tropical "
            "evergreen forests of the Gulf and southern Pacific.",
        "diet":
            "Almost exclusively arboreal snails. Extreme specialist.",
        "behavior":
            "Solitary, secretive. Forages among bromeliads and dense trees. "
            "Hypertrophied bill adapted to extract snails from their shells.",
        "migration":
            "Sedentary with local dispersal.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Large curved bill (diagnostic trait). Broad rounded wings. Bare "
            "yellowish-white face in adults.",
        "best_months": "Year-round (uncommon resident)",
        "did_you_know":
            "Its bill evolved specifically to extract arboreal snails of the "
            "genus Bulimulus. It is one of the few raptors with such a "
            "specialised diet.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Circus_hudsonius": {
        "distribution":
            "Breeds in prairies and marshes of North America. Migrates to the "
            "southern USA, Mexico and the Caribbean. Common winter visitor in "
            "grasslands and wetlands throughout Mexico.",
        "diet":
            "Small mammals (mice) and grassland birds.",
        "behavior":
            "Low coursing flight over grasslands and wetlands. Marked sexual "
            "dimorphism: females brown, males grey.",
        "migration":
            "Complete migrator. Peak in Veracruz: October-November.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Long wings in a shallow V. WHITE PATCH on the rump — immediate "
            "diagnostic. Low oscillating flight over grasslands.",
        "best_months": "October-March",
        "did_you_know":
            "It has an owl-like facial disc that helps it locate prey by sound. "
            "It is the only diurnal raptor in the New World with this auditory "
            "adaptation.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Coragyps_atratus": {
        "distribution":
            "Southern USA to Argentina. In Mexico it is the most abundant "
            "raptor in tropical and subtropical zones; tolerates urban and "
            "rural environments well.",
        "diet":
            "Carrion; also garbage, decomposing fruit, eggs, chicks and "
            "vulnerable livestock young. More aggressive than C. aura in groups.",
        "behavior":
            "Sociable and gregarious. Forms thermal kettles and communal roosts "
            "of hundreds of individuals. Flight with rapid wingbeats interspersed "
            "with flat glides.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Glossy black plumage, bare grey head. Short square tail. "
            "Silver-white patch ONLY at wingtips (primaries) seen in flight.",
        "best_months": "Year-round",
        "did_you_know":
            "Lacks the fine sense of smell of Cathartes; locates carrion "
            "visually or by following the Turkey Vulture in flight. One of the "
            "dominant species of the urban avian landscape in Mexican cities.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Daptrius_americanus": {
        "distribution":
            "Tropical rainforests of southeastern Mexico (Lacandona Forest, "
            "Calakmul) to Bolivia. Historically more widely distributed, "
            "today very localised and rare in Mexico.",
        "diet":
            "Wasps and wasp nests (only raptor specialised in raiding wasp "
            "combs), large fruits, lizards and bird nestlings.",
        "behavior":
            "Loud and very social; lives in groups of 3-10 related individuals "
            "that cooperate in raiding hives. Vocalises with a strident scream "
            "resembling loud laughter.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern (declining)",
        "diagnostic":
            "Glossy black plumage; white belly and undertail; red face and "
            "throat; thick yellow bill. General appearance like a large dark "
            "caracara.",
        "best_months": "Year-round (remote rainforest)",
        "did_you_know":
            "It is the only bird in the world that systematically raids "
            "colonies of social wasps. It has disappeared from much of its "
            "historic Mexican range due to rainforest loss. Listed as "
            "'Endangered' (P) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Elanoides_forficatus": {
        "distribution":
            "Southern USA, Mexico, Central and South America. In Mexico, "
            "summer breeder in Gulf tropical forests and a common migrant.",
        "diet":
            "Large flying insects, small arboreal vertebrates, frogs.",
        "behavior":
            "Extraordinarily agile and elegant flight. Captures insects in mid "
            "air. Migrates in social groups.",
        "migration":
            "Complete migrator. Peak in Veracruz: August-September and March.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Deeply forked tail (unique trait). Contrasting black and white "
            "plumage. Elegant flight 'like a giant swallow'.",
        "best_months": "August-September (migration peak)",
        "did_you_know":
            "Its forked tail gives it one of the most agile manoeuvring "
            "capabilities among raptors. It is one of the few raptors that "
            "feeds exclusively in the air or on foliage.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Elanus_leucurus": {
        "distribution":
            "Disjunct distribution in the Americas: western and southern USA, "
            "Mexico, Central America and the Southern Cone. In Mexico: open "
            "grasslands, savannas and scrublands of the Bajío, Gulf slope and "
            "Pacific.",
        "diet":
            "Small mammals, especially voles; large insects; occasionally "
            "very small birds.",
        "behavior":
            "Prolonged hovering over grasslands — the only Elanus that does "
            "it well. Characteristic 'raised shoulders' posture. Forms communal "
            "roosts in trees.",
        "migration":
            "Mostly sedentary; local movements following rodent irruptions.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Pearl-grey plumage with white belly and tail. Very marked black "
            "shoulders and wing band. Red eyes. Systematic hovering.",
        "best_months": "Year-round (most visible in grasslands)",
        "did_you_know":
            "Its populations can multiply rapidly in years of rodent irruptions, "
            "a phenomenon documented both in California and in the Mexican Bajío.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_columbarius": {
        "distribution":
            "Breeds in boreal forests and northern prairies. Migrates to the "
            "southern USA, Mexico and Central America.",
        "diet":
            "Small birds caught in fast flight over open spaces.",
        "behavior":
            "Extremely fast and direct flight, with powerful wingbeats. "
            "Aggressive hunter specialised in grassland birds.",
        "migration":
            "Complete migrator. Peak in Veracruz: October.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Small size, pointed wings. Tail with pale grey bands. Darker and "
            "more compact than the Kestrel.",
        "best_months": "October-March",
        "did_you_know":
            "Despite its small size, it is one of the fiercest hunters of its "
            "size. Historically used in European falconry, known as 'merlin' "
            "since the Middle Ages.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_deiroleucus": {
        "distribution":
            "Very local distribution in tropical forests with cliffs, from "
            "southern Mexico (Chiapas, Tabasco, inland Veracruz) to Argentina. "
            "One of the rarest and most enigmatic raptors of the Neotropics.",
        "diet":
            "Medium-to-large birds (doves, partridges, parrots) taken in "
            "powerful stoops. Bats at dusk.",
        "behavior":
            "Solitary or in territorial pairs. Nests on cliffs emergent over "
            "forest. Powerful and fast flight, similar to the Peregrine but "
            "with a more robust head.",
        "migration":
            "Sedentary.",
        "iucn_status": "Near Threatened",
        "diagnostic":
            "Intense orange-rufous chest and neck contrasting with black-barred "
            "belly and white throat. Large head, blue-black back. Robust "
            "bulldog-like appearance.",
        "best_months": "Year-round (but extremely difficult to observe)",
        "did_you_know":
            "Its world population is estimated at fewer than 1,000 individuals. "
            "The Mesoamerican Population (including Mexico) has been the target "
            "of The Peregrine Fund's most intensive rescue programme. Listed as "
            "'Endangered' (P) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_femoralis": {
        "distribution":
            "Open grasslands and scrublands of the southwestern USA (where it "
            "was reintroduced), Mexico and South America. In Mexico: grasslands "
            "of the northern Altiplano, Gulf coast and southern Pacific. Slowly "
            "recovering after nearly being extirpated from the country.",
        "diet":
            "Small and medium-sized birds, lizards, large insects. Hunts in "
            "cooperative pairs.",
        "behavior":
            "Agile and fast. Often hunts in pairs, one chasing and the other "
            "cutting off escape routes. Perches on the tops of shrubs, posts "
            "and isolated trees.",
        "migration":
            "Resident; some altitudinal and local movements.",
        "iucn_status": "Least Concern (regionally recovering)",
        "diagnostic":
            "Slender, long wings and tail. White breast with a broad black "
            "belly band, cinnamon thighs; white face with a thin black "
            "moustache; prominent white supercilium.",
        "best_months": "Year-round in northern grasslands",
        "did_you_know":
            "Nearly extirpated from North America in the mid 20th century, "
            "its recovery in Texas and Chihuahua is one of the most recent "
            "raptor conservation successes. Listed as 'Threatened' (A) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_peregrinus": {
        "distribution":
            "Cosmopolitan. Breeds on cliffs, mountains and urban buildings. "
            "In Mexico: winter visitor and local resident on coasts, sierras "
            "and large cities.",
        "diet":
            "Almost exclusively birds taken in flight — from doves to ducks.",
        "behavior":
            "Vertical stoop at over 320 km/h — the fastest animal on the "
            "planet. Solitary hunter, attacks from great height.",
        "migration":
            "Partial migrator. Peak in Veracruz: October.",
        "iucn_status": "Least Concern (recovered post-DDT)",
        "diagnostic":
            "Very marked black 'hood'. Long pointed wings. Relatively short "
            "tail. Powerful, direct flight.",
        "best_months": "October-March",
        "did_you_know":
            "It is the fastest animal in the world: reaches 389 km/h in its "
            "stoop. Almost went extinct due to DDT but recovered after its ban.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_rufigularis": {
        "distribution":
            "Tropical lowlands from Mexico (Tamaulipas, Veracruz, Tabasco, "
            "Chiapas, Yucatán, Oaxaca, Jalisco southward) to Argentina. Forest "
            "edges and agricultural areas with emergent trees.",
        "diet":
            "Bats and small birds caught at dawn and dusk; large insects "
            "(dragonflies, butterflies, cicadas) during the day.",
        "behavior":
            "Perches very high, generally on exposed branches at the top of "
            "emergent trees. Hunts in short fast flights. Crepuscular, "
            "especially for bats.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Small and compact. Black hood, white throat and collar, "
            "black-barred chest, intense rufous belly. Long wings and tail "
            "relative to body.",
        "best_months": "Year-round",
        "did_you_know":
            "It is one of the few falcons in the world that systematically "
            "hunts bats at dusk, occupying a niche similar to that of the "
            "Old World forest falcons and bat hawks.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_sparverius": {
        "distribution":
            "Wide distribution across the Americas. Resident and migratory "
            "across almost all of Mexico.",
        "diet":
            "Large insects, mice, lizards, very small birds.",
        "behavior":
            "Hovering flight over grasslands — the only small raptor that "
            "does it well. Hunts from a perch on power lines.",
        "migration":
            "Partial migrator.",
        "iucn_status": "Least Concern (declining)",
        "diagnostic":
            "Small size, pointed wings, rufous tail with a black terminal "
            "band. Double black moustache on face. Male with rufous back and "
            "blue wings.",
        "best_months": "Year-round, migration peak October-November",
        "did_you_know":
            "It is the smallest raptor in North America. Its populations have "
            "declined by 50% in the last 50 years — exact causes still under "
            "investigation.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Geranoaetus_albicaudatus": {
        "distribution":
            "Open grasslands and scrub of southern Texas, Mexico and South "
            "America. In Mexico: Gulf coast, Pacific, Mezquital Valley and "
            "southern Altiplano.",
        "diet":
            "Small and medium-sized mammals, reptiles, grassland birds, large "
            "insects. Strikingly, it congregates at grass fires to catch prey "
            "fleeing the flames.",
        "behavior":
            "Elegant soaring with broad short wings. Solitary or in pairs. "
            "Follows agricultural machinery and fires to catch disturbed prey.",
        "migration":
            "Resident.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Adult: dark grey upperparts, white chest, white tail with a thin "
            "black subterminal band; well-defined reddish shoulder. Broad wings "
            "that appear 'block-cut'.",
        "best_months": "Year-round",
        "did_you_know":
            "Reclassified from the genus Buteo to Geranoaetus in 2014 based on "
            "molecular phylogenetics. Together with G. melanoleucus (South "
            "America) and G. polyosoma, it forms the Andean-hawk group, although "
            "it inhabits lowlands.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Geranospiza_caerulescens": {
        "distribution":
            "Tropical lowlands from southern Mexico (Gulf slope from Tamaulipas, "
            "and Pacific from Sinaloa) to Argentina.",
        "diet":
            "Cavity-nesting birds, nestlings, reptiles, amphibians, bats "
            "extracted from cavities in trees, branches and palms.",
        "behavior":
            "Solitary. Walks on branches and approaches cavities to extract "
            "prey with its extremely long tarsi and bendable tibio-tarsal "
            "joint (unique).",
        "migration":
            "Resident.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Uniform slate grey plumage; long tail with two white bands; "
            "extra-long orange tarsi. Slender, almost wader-like appearance "
            "(hence its Spanish name 'gavilán zancón').",
        "best_months": "Year-round",
        "did_you_know":
            "It possesses an unusual double joint between the tibia and the "
            "tarsus that lets it bend its leg backwards, unique among raptors; "
            "this allows it to reach deep into cavities to extract bird "
            "nestlings and bats.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Haliaeetus_leucocephalus": {
        "distribution":
            "All of North America, especially coasts and large lakes. In "
            "Mexico: rare winter visitor on the Pacific coast and northern "
            "Baja California; exceptional records on the Gulf slope.",
        "diet":
            "Mainly fish; also waterbirds, carrion and small mammals.",
        "behavior":
            "Elegant soaring over water bodies. Occasionally pirates prey "
            "from Osprey. Pair-bonds for life.",
        "migration":
            "Partial migrator. Adults can be sedentary.",
        "iucn_status": "Least Concern (recovered post-DDT)",
        "diagnostic":
            "White head and tail in adults (juveniles entirely brown). Huge "
            "yellow bill. One of the largest raptors in the Americas.",
        "best_months": "December-February (rare winter records)",
        "did_you_know":
            "National bird of the USA. Nearly went extinct due to DDT in the "
            "1960s — fewer than 500 pairs remained in the 48 contiguous states. "
            "Today there are over 70,000.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Harpagus_bidentatus": {
        "distribution":
            "Tropical rainforests from southern Mexico (Veracruz, Oaxaca, "
            "Chiapas, Tabasco, Campeche, Quintana Roo) to Bolivia.",
        "diet":
            "Large insects (beetles, mantises, grasshoppers) and small "
            "lizards. Follows troops of white-faced capuchins that flush "
            "insects as they move through the canopy.",
        "behavior":
            "Sits quietly under the canopy. Follows mixed flocks of birds "
            "and primate troops ('beater flocks') to capture fleeing prey. "
            "Fast and direct flight.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Small, bluish-grey on the back, breast with finely barred rufous "
            "tint, white belly; tail with pale bands. Pure white edge to "
            "undertail feathers. Two small 'teeth' on each side of the upper "
            "mandible (the trait it takes its name from).",
        "best_months": "Year-round",
        "did_you_know":
            "It associates its foraging with troops of white-faced capuchins "
            "(Cebus capucinus) and other understory birds, demonstrating one "
            "of the best-documented indirect kleptoparasitism relationships "
            "between raptors and primates.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Harpia_harpyja": {
        "distribution":
            "Continuous humid forests from southern Mexico (Lacandona Forest, "
            "Chiapas; northern Oaxaca; Calakmul, Campeche) to Bolivia and "
            "northern Argentina. In Mexico practically extirpated from its "
            "historical range.",
        "diet":
            "Sloths and arboreal monkeys; coatis, kinkajous, large iguanas "
            "and large birds (curassows, toucans). One of the most powerful "
            "raptors in the world.",
        "behavior":
            "Solitary and silent. Hunts from a high perch in the canopy. "
            "Territorial pairs very faithful to a single nest across decades. "
            "Raises only one chick every 2-3 years.",
        "migration":
            "Sedentary; requires extensive areas of intact forest.",
        "iucn_status": "Vulnerable",
        "diagnostic":
            "Massive. Slate grey back, white belly with a broad black breast "
            "band; double crest of feathers on the head; extremely robust tarsi "
            "the thickness of a human wrist, with talons up to 13 cm long.",
        "best_months": "Year-round (practically impossible without dedicated search)",
        "did_you_know":
            "Its talons are larger than those of a grizzly bear. Very little "
            "population remains in Mexico — perhaps fewer than 20 confirmed "
            "breeding pairs. Listed as 'Endangered' (P) in NOM-059 and "
            "'Vulnerable' by IUCN.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Herpetotheres_cachinnans": {
        "distribution":
            "Tropical forests and semi-humid woodlands from Mexico (Sinaloa, "
            "San Luis Potosí, Tamaulipas southward) to Argentina.",
        "diet":
            "Snake specialist (including venomous: fer-de-lance, coral snakes), "
            "occasionally large lizards.",
        "behavior":
            "Sits quietly on semi-concealed perches, dropping rapidly onto "
            "snakes. Vocalises loudly at dawn and dusk: the 'wahcoh-wahcoh' "
            "(hence its Spanish name 'guaco'), associated by rural people "
            "with the presence of snakes.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Large head, dark eyes with a wide black mask; cream crown and "
            "neck; cream-white belly; dark brown barred wings and tail. "
            "Unmistakable laughing call.",
        "best_months": "Year-round",
        "did_you_know":
            "Its Spanish name 'guaco' is onomatopoeic of its call, and "
            "Mexican folk belief holds that its song warns of the presence "
            "of vipers. It is one of the few falconids in the world specialised "
            "in hunting snakes.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Ictinia_mississippiensis": {
        "distribution":
            "South-central USA. Migrates to South America. Strong migration "
            "peak through the Veracruz corridor.",
        "diet":
            "Large flying insects (dragonflies, cicadas, beetles) caught in "
            "the air.",
        "behavior":
            "Extraordinarily agile flight. Catches insects on the wing. "
            "Colonises urban environments in the USA (small towns of the "
            "central south).",
        "migration":
            "Complete migrator. Peak in Veracruz: September-October.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Small, long pointed wings, long dark tail. Contrasting pale head. "
            "Agile flight almost swift-like.",
        "best_months": "September-October",
        "did_you_know":
            "It is one of the most insectivorous kites — 90% of its diet is "
            "large insects. Migrates in large social groups with Buteo "
            "platypterus and B. swainsoni.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Ictinia_plumbea": {
        "distribution":
            "Replaces the Mississippi Kite in the tropics: Mexico (Veracruz, "
            "Tabasco, Oaxaca, Chiapas, Yucatán) to Argentina. Summer breeder "
            "in Mexico.",
        "diet":
            "Large flying insects (dragonflies, cicadas, butterflies), small "
            "bats and very small birds. All caught in flight.",
        "behavior":
            "Elegant and agile flight. Forms loose aggregations, especially "
            "during migration. Breeds in emergent canopy trees.",
        "migration":
            "Partial migrator: Mexican populations migrate south after the "
            "breeding season.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Uniform plumbeous grey; rufous primaries (visible in flight); "
            "long black tail with TWO white bands (vs. I. mississippiensis "
            "which has a single subterminal band).",
        "best_months": "April-September (breeding season)",
        "did_you_know":
            "It is the tropical version of the Mississippi Kite: morphologically "
            "very similar but distinguished by the two-banded tail and the "
            "rufous primaries visible in flight.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Leptodon_cayanensis": {
        "distribution":
            "Tropical forests and gallery forests from southern Mexico "
            "(southeastern San Luis Potosí, Veracruz, Tabasco, Chiapas, "
            "Yucatán) to Argentina.",
        "diet":
            "Wasps, wasp larvae and bees extracted from nests; arboreal frogs, "
            "lizards, nestlings. Hive specialist.",
        "behavior":
            "Solitary; undulating, silent flight. Performs spectacular "
            "courtship displays with circling flights and dives. Sits "
            "quietly under the canopy.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Pale grey head marked with a darker face, blue-black back, white "
            "belly; tail with black and white bands. Bluish bill markedly "
            "bicoloured.",
        "best_months": "Year-round",
        "did_you_know":
            "Its courtship behaviour includes very high circular flights "
            "accompanied by vocalisations and vertical dives, one of the most "
            "spectacular displays among Neotropical kites.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Micrastur_ruficollis": {
        "distribution":
            "Tropical rainforests and cloud forests from southern Mexico "
            "(Veracruz, Chiapas, Tabasco, Oaxaca) to Argentina.",
        "diet":
            "Small understory birds, lizards, small mammals and large "
            "insects. Follows army ant swarms to catch fleeing prey.",
        "behavior":
            "Shy and difficult to observe. Hunts from a low perch in the "
            "understory with very short, accurate flights. Vocalises with "
            "an accelerating 'kaa-kaa-kaa' at dawn.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Small, long tail, long yellow tarsi. Slate grey back, white "
            "breast and belly finely barred in black. Dark eyes, bare yellow "
            "face.",
        "best_months": "Year-round (more often heard than seen)",
        "did_you_know":
            "Part of the enigmatic group of forest-falcons of the genus "
            "Micrastur, with short wings and long tails adapted to manoeuvre "
            "between dense trees — ecological convergence with the Astur and "
            "Accipiter of the Old World.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Micrastur_semitorquatus": {
        "distribution":
            "Tropical forests and cloud forests from Mexico (Sinaloa, "
            "Tamaulipas and southern country) to Argentina.",
        "diet":
            "Medium-to-large birds (doves, tinamous, chachalacas), arboreal "
            "mammals, reptiles. One of the most versatile forest raptors.",
        "behavior":
            "Stealthy; chases prey by running along the rainforest floor or "
            "along branches, not only in flight. Vocalises with a characteristic "
            "descending 'kak-kak-kak-aaaa'.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Three morphs (light, intermediate and dark). Neck with light "
            "yellow collar (in the light morph); long tail with white bands; "
            "long yellow tarsi. Much larger than M. ruficollis.",
        "best_months": "Year-round",
        "did_you_know":
            "One of the few falcons in the world that chases prey by running "
            "along the ground and climbing branches, behaviour more typical "
            "of Old World forest raptors. Its long tarsi are an adaptation to "
            "this hunting style.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Morphnus_guianensis": {
        "distribution":
            "Continuous humid forests from southern Mexico (Lacandona, Chiapas; "
            "southeastern Oaxaca; Calakmul) to Argentina. Extremely rare in "
            "Mexico and in steep decline.",
        "diet":
            "Arboreal mammals (small monkeys, kinkajous, weasels), large "
            "reptiles (iguanas), medium-sized birds. More versatile but less "
            "powerful than its congener the Harpy Eagle.",
        "behavior":
            "Solitary. Hunts from a perch in the canopy. Raises only one chick "
            "every 2-3 years. Extremely extensive territories (up to 50 km²).",
        "migration":
            "Sedentary.",
        "iucn_status": "Near Threatened",
        "diagnostic":
            "Large, slender. Pointed crest (finer than the double crest of the "
            "Harpy Eagle). Slate grey back, white breast tinted cinnamon "
            "depending on morph; long tail with broad bands; feathered tarsi.",
        "best_months": "Year-round (dedicated search)",
        "did_you_know":
            "Together with Harpia harpyja it forms the closest sister genus "
            "within the subfamily Harpiinae. It is in competitive interaction "
            "with the Harpy Eagle where they coexist. Listed as 'Endangered' "
            "(P) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Pandion_haliaetus": {
        "distribution":
            "Cosmopolitan. In Mexico, winter visitor along the coast and "
            "rivers; rare resident on the Baja California peninsula, Sonora "
            "and the tropical Pacific coast.",
        "diet":
            "Almost exclusively fish, caught by plunging into water.",
        "behavior":
            "Flies over water bodies, hovers and dives. Unique among raptors "
            "— feet with spicules to grip slippery fish.",
        "migration":
            "Complete migrator. Peak in Veracruz: October.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Long wings with a kink at the wrist (M shape). White breast with "
            "a dark band. Very marked black eye stripe.",
        "best_months": "October-March",
        "did_you_know":
            "It is the only raptor in the world whose feet have spicules "
            "(spiny papillae) on the pads — an adaptation for gripping "
            "slippery fish. Monotypic family.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Parabuteo_unicinctus": {
        "distribution":
            "Deserts, xerophytic scrub and semi-arid savannas of the "
            "southwestern USA, Mexico (especially Sonora, Chihuahua, Coahuila, "
            "Tamaulipas, Bajío, southern country) to Argentina.",
        "diet":
            "Rabbits, ground squirrels, grassland birds and reptiles. Hunts "
            "in cooperative family groups of 2-7 individuals — unique among "
            "birds of prey.",
        "behavior":
            "COOPERATIVE hunting in family groups: a technique in which several "
            "individuals surround and flush the prey for another to capture. "
            "Socio-hunter behaviour unique among raptors.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Dark chocolate brown; intense reddish-cinnamon shoulders and "
            "thighs; tail with broad white base and tip. Compact and muscular "
            "appearance.",
        "best_months": "Year-round",
        "did_you_know":
            "It is the only raptor in the world that regularly hunts in "
            "cooperative family groups, behaviour more typical of canids. "
            "For this reason it is the most widely used raptor in modern "
            "falconry.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Pseudastur_albicollis": {
        "distribution":
            "Tropical rainforests and cloud forests from southern Mexico "
            "(Veracruz, Oaxaca, Chiapas, Tabasco, Quintana Roo) to Brazil.",
        "diet":
            "Reptiles (iguanas, snakes), small arboreal mammals, understory "
            "birds. Follows monkey troops to catch what they flush.",
        "behavior":
            "Perches high in the canopy. Elegant soaring. Often follows army "
            "ants and white-faced capuchin troops.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Unmistakable appearance: plumage almost entirely white; wings "
            "with black terminal and trailing-edge bands; tail with a broad "
            "black subterminal band and white tip. Yellow legs.",
        "best_months": "Year-round",
        "did_you_know":
            "Reclassified from the genus Leucopternis to Pseudastur (2014). "
            "Forms associations with spider and howler monkeys: as the "
            "primates move through the canopy, they flush small prey that "
            "the bird captures.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Rostrhamus_sociabilis": {
        "distribution":
            "Tropical and subtropical wetlands from Florida and Mexico "
            "(Veracruz, Tabasco, Campeche, Yucatán, Chiapas, Sinaloa) to "
            "Argentina.",
        "diet":
            "Extreme specialist on aquatic snails of the genus Pomacea (apple "
            "snails). Eats almost nothing else.",
        "behavior":
            "Sociable and gregarious. Forms communal roosts of hundreds of "
            "individuals. Slow flight over wetlands. Perches on stakes and "
            "reeds to extract snails with its curved bill.",
        "migration":
            "Sedentary but with local movements depending on water levels and "
            "snail abundance.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Extraordinarily curved narrow bill. Male dark slate grey almost "
            "black; female brown with streaked belly; both with conspicuous "
            "white tail base.",
        "best_months": "Year-round in Gulf and southern Pacific wetlands",
        "did_you_know":
            "Its bill evolved specifically to extract Pomacea snails from "
            "their shells without breaking them. It is one of the few "
            "documented cases of coevolution between a raptor and its main prey.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Rupornis_magnirostris": {
        "distribution":
            "One of the most common raptors in tropical and subtropical zones "
            "of the Americas. In Mexico: Gulf lowlands (Tamaulipas-Chiapas) "
            "and tropical Pacific (Sinaloa southward).",
        "diet":
            "Lizards, large insects, amphibians, mice, nestlings and fledglings. "
            "Generalist.",
        "behavior":
            "Often seen on posts and isolated trees along rural roads (hence "
            "its name). Tolerates human presence well. Flight with slow "
            "wingbeats and short glides.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern",
        "diagnostic":
            "Medium-small size. Brownish-grey head and chest, whitish belly "
            "barred with cinnamon; tail with alternating dark and pale bands. "
            "Pale yellowish iris.",
        "best_months": "Year-round",
        "did_you_know":
            "Until 2014 it was placed in the genus Buteo; phylogenetic analyses "
            "separated it into its own genus Rupornis. It is the Neotropical "
            "Buteonine most adaptable to human-modified landscapes.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Sarcoramphus_papa": {
        "distribution":
            "Tropical forests and wooded savannas from southern Mexico "
            "(Veracruz, Chiapas, Tabasco, Oaxaca, Yucatán, southern Quintana "
            "Roo) to Argentina. Localised and rare in Mexico.",
        "diet":
            "Carrion; it typically opens large carcasses with its powerful "
            "bill, subsequently allowing access for other vultures unable to "
            "break the skin.",
        "behavior":
            "Solitary or in pairs. Majestic flight in very high thermals. "
            "Arrives at carcasses attracted by prior congregations of Coragyps "
            "and Cathartes.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern (declining in Mexico)",
        "diagnostic":
            "Cream-white plumage with black wings and tail. Bare multicoloured "
            "head (red, orange, yellow, purple) with a fleshy orange caruncle "
            "above the bill. Unmistakable as an adult.",
        "best_months": "Year-round (southeastern forests)",
        "did_you_know":
            "It is the most colourful raptor in the world and the only member "
            "of its genus. In Mayan mythology it was considered a messenger "
            "between the gods and humans. Listed as 'Endangered' (P) in NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_melanoleucus": {
        "distribution":
            "Forests and montane forests from southern Mexico (Veracruz, "
            "Oaxaca, Chiapas) to Argentina. Rare and local in Mexico.",
        "diet":
            "Medium-to-large birds (doves, oropendolas, small toucans), "
            "reptiles and arboreal mammals.",
        "behavior":
            "Very high soaring over the canopy — more often seen in flight "
            "than perched. Solitary or in pairs. Vocalises with a long "
            "descending whistle.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern (regionally rare)",
        "diagnostic":
            "Head, neck and belly pure white; contrasting black back and wings; "
            "short black eye-mask. Short crest. Majestic flight with long wings.",
        "best_months": "Year-round (extremely difficult)",
        "did_you_know":
            "Previously placed in the genus Spizastur. Its highly contrasting "
            "plumage is unique among the Mexican Spizaetus and allows it to be "
            "identified from kilometres away when soaring over the canopy.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_ornatus": {
        "distribution":
            "Tropical rainforests and cloud forests of southern Mexico "
            "(Veracruz, Oaxaca, Chiapas, Tabasco, Quintana Roo) to Brazil. "
            "Rare in Mexico due to habitat loss.",
        "diet":
            "Medium-sized birds (chachalacas, toucans, parrots, large doves), "
            "small mammals and reptiles. Hunts from a perch with powerful flights.",
        "behavior":
            "Solitary. Hunts from a perch in the canopy. Vocalises with high "
            "descending whistles. Powerful flight with broad wings and long tail.",
        "migration":
            "Sedentary.",
        "iucn_status": "Near Threatened",
        "diagnostic":
            "Long erect pointed crest. Face, sides of neck and chest intense "
            "rufous; black crown; intense white belly with fine black bars; "
            "tail with pale and dark bands. One of the most spectacular raptors "
            "in the Americas.",
        "best_months": "Year-round (dedicated search in tall forest)",
        "did_you_know":
            "Considered by many ornithologists the most beautiful raptor in "
            "the Americas because of its colour combination and erectable "
            "crest. Listed as 'Endangered' (P) in NOM-059 and 'Near Threatened' "
            "by IUCN.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_tyrannus": {
        "distribution":
            "Tropical rainforests and montane forests of southern Mexico "
            "(Veracruz, Oaxaca, Chiapas, Tabasco, Yucatán) to Argentina.",
        "diet":
            "Arboreal mammals (kinkajous, small monkeys), medium-sized birds "
            "(parrots, oropendolas), large reptiles.",
        "behavior":
            "Solitary. High circular flights over the canopy accompanied by "
            "loud high-pitched vocalisations. Elusive habits despite its size.",
        "migration":
            "Sedentary.",
        "iucn_status": "Least Concern (regionally rare)",
        "diagnostic":
            "Entirely black plumage; feathered tarsi with fine white barring; "
            "short crest. In flight: long wings with fingered tips, long tail "
            "with 3-4 white bands. Overall pattern similar to a Buteogallus "
            "but with longer wings and a longer tail.",
        "best_months": "Year-round (tall forest)",
        "did_you_know":
            "Its loud, prolonged vocalisation is one of the iconic sounds of "
            "Mexico's tall rainforests in areas like Calakmul and the Lacandona, "
            "where it is often heard more easily than seen.",
    },

}


# ──────────────────────────────────────────────────────────────────────────
# Auto-translation maps for short status strings (used by species_info.py).
# ──────────────────────────────────────────────────────────────────────────

IUCN_STATUS_EN: dict[str, str] = {
    "Least Concern":                "Least Concern",
    "Near Threatened":              "Near Threatened",
    "Vulnerable":                   "Vulnerable",
    "Endangered":                   "Endangered",
    "Critically Endangered":        "Critically Endangered",
    "Data Deficient":               "Data Deficient",
    "Not Evaluated":                "Not Evaluated",
    # Spanish IUCN labels seen in species_data.py
    "Preocupación Menor":           "Least Concern",
    "Casi Amenazada":               "Near Threatened",
    "Vulnerable (NOM-059)":         "Vulnerable (NOM-059)",
    "Amenazada":                    "Threatened",
    "Sujeta a protección especial": "Subject to Special Protection",
    "En peligro de extinción":      "Endangered",
}


SHORT_PHRASE_EN: dict[str, str] = {
    "Distribución holártica":               "Holarctic distribution",
    "Reproductor en bosques":               "Breeds in forests",
    "Bosques boreales y templados":         "Boreal and temperate forests",
    "Migrador completo":                    "Complete migrant",
    "Migrador parcial":                     "Partial migrant",
    "Residente":                            "Resident",
    "Residente tropical":                   "Tropical resident",
    "Selva tropical":                       "Tropical forest",
    "Bosque seco":                          "Dry forest",
    "Humedales":                            "Wetlands",
    "Costas":                               "Coastal areas",
    "Zonas áridas":                         "Arid zones",
    "Norteamérica":                         "North America",
    "Centroamérica":                        "Central America",
    "Sudamérica":                           "South America",
    "México":                               "Mexico",
}
