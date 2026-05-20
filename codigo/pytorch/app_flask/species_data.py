"""
raptors-cnn — Perfiles enriquecidos por especie (estilo Merlin Bird ID)

Proyecto: Sistema de Identificación de Aves Rapaces por Silueta y
Comportamiento de Vuelo Utilizando IA y Diseño de Lenguaje de Señas
para su Comunicación y Reconocimiento.

Adaptado de raptor_australia/gui/species_data.py para las 53 rapaces
diurnas documentadas en México (todas las Cathartidae, Pandionidae,
Accipitridae y Falconidae nacionales).

V1.1 (mayo 2026) — cambio de alcance respecto a V1 (23 VRR) a México completo.
Ver `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md`.

Cada perfil sigue la misma forma para que la plantilla pueda renderizar
las 53 especies uniformemente. Las claves de cada entrada son:
    distribution, diet, behavior, migration, iucn_status,
    length_cm, wingspan_cm, diagnostic, best_months, did_you_know

Referencias consultadas:
  - Howell, S. N. G., & Webb, S. (1995). A Guide to the Birds of Mexico and
    Northern Central America. Oxford University Press.
  - Berlanga et al. (2019). Aves de México: Guía de Campo. CONABIO.
  - Bildstein, K. L. (2006). Migrating raptors of the world. Cornell Univ. Press.
  - Howell, S. N. G. (2012). Raptors: Annual cycle, age determination, migration.
  - Liguori, J. (2005, 2011). Hawks from every angle / Hawks at a distance.
  - Pronatura Veracruz (2020). Manual de rapaces migratorias del corredor de Veracruz.
  - Ferguson-Lees & Christie (2001). Raptors of the World. Christopher Helm.
  - del Hoyo, Elliott & Sargatal (1994). Handbook of the Birds of the World, vol. 2.
  - IUCN Red List (2025).
  - AOS (2023). Check-list of North and Middle American Birds — 64th Supplement.
  - AOS (2024). 65th Supplement.
"""

SPECIES_DETAILS: dict[str, dict] = {

    # ──────────────────────────────────────────────────────────────────────
    "Accipiter_striatus": {  # SSHA — Sharp-shinned Hawk — Gavilán pajarero
        "distribution":
            "Reproductor en bosques boreales y templados de Norteamérica; migra al sur "
            "y atraviesa todo México en otoño. El corredor de Veracruz concentra el flujo "
            "principal entre septiembre y noviembre.",
        "diet":
            "Aves pequeñas atrapadas en emboscadas rápidas en bosque; "
            "ocasionalmente murciélagos y grandes insectos.",
        "behavior":
            "Vuelo veloz con aleteos rápidos y planeos cortos. Solitario en migración. "
            "Difícil de distinguir del Gavilán de Cooper a distancia.",
        "migration":
            "Migrador completo. Pico migratorio: mediados de octubre a inicios de noviembre.",
        "iucn_status": "Least Concern",
        "length_cm": "24-34 cm",
        "wingspan_cm": "53-65 cm",
        "diagnostic":
            "Alas cortas redondeadas, cola larga cuadrada. Tamaño pequeño. "
            "Cabeza más pequeña proporcionalmente que en Cooper's.",
        "best_months": "Octubre-Noviembre",
        "did_you_know":
            "Es la rapaz más pequeña de los Accipiter neárticos. Cuando ataca, "
            "puede maniobrar entre ramas a velocidades altísimas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Aquila_chrysaetos": {  # GOEA — Golden Eagle — Águila real
        "distribution":
            "Distribución holártica. En México habita zonas montañosas áridas de "
            "Chihuahua, Sonora, Durango, Coahuila, Zacatecas e Hidalgo, hasta el "
            "Eje Neovolcánico. Símbolo nacional.",
        "diet":
            "Mamíferos medianos (conejos, liebres, marmotas), aves grandes y carroña.",
        "behavior":
            "Soberbia voladora en térmicas altas. Territorial extremo. "
            "Pareja de por vida; reusa nidos por décadas.",
        "migration":
            "Parcialmente migradora. Adultos del norte pueden alcanzar México central en invierno.",
        "iucn_status": "Least Concern (declinante regional)",
        "length_cm": "66-102 cm",
        "wingspan_cm": "180-234 cm",
        "diagnostic":
            "Nuca dorada, alas largas y anchas con punta digitada. "
            "Cola larga (más larga que en Bald Eagle).",
        "best_months": "Año redondo en sierras del centro-norte",
        "did_you_know":
            "Ave nacional de México prehispánica y representada en la bandera. "
            "Pueden bajar en picada a más de 320 km/h al atacar presas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_atricapillus": {  # NOGO — American Goshawk — Gavilán azor americano
        "distribution":
            "Bosques boreales y templados de Norteamérica. En México observación rara, "
            "principalmente en bosques de coníferas del norte (Sierra Madre Occidental) "
            "y registros invernales hasta Veracruz.",
        "diet":
            "Aves grandes (palomas, urracas, grouse) y mamíferos pequeños.",
        "behavior":
            "Cazadora aérea poderosa. Vuelo de aleteos cortos + planeos largos. "
            "Agresiva en defensa del territorio reproductor.",
        "migration":
            "Migración parcial. Rara vez alcanza el Neotrópico — registros excepcionales.",
        "iucn_status": "Least Concern",
        "length_cm": "46-69 cm",
        "wingspan_cm": "89-127 cm",
        "diagnostic":
            "Tamaño grande para Accipiter (ahora Astur por AOS 2023). "
            "Cola redondeada amplia, ceja blanca muy marcada en adultos.",
        "best_months": "Octubre-Febrero (registros invernales esporádicos)",
        "did_you_know":
            "Reclasificada del género Accipiter al género Astur por la AOS en 2023, "
            "junto con Cooper's Hawk, basado en estudios filogenómicos. Su nombre común en "
            "inglés también cambió a 'American Goshawk' para distinguirla del eurasiático.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_cooperii": {  # COHA — Cooper's Hawk — Gavilán de Cooper
        "distribution":
            "Bosques caducifolios y mixtos de Norteamérica. Migra a México y "
            "Centroamérica en invierno. Común en migración y como residente urbano "
            "en muchas ciudades mexicanas.",
        "diet":
            "Aves medianas (palomas, mirlos, codornices) y pequeños mamíferos.",
        "behavior":
            "Similar a SS pero más grande y de vuelo más recto. "
            "Cazador de emboscada en bordes de bosque.",
        "migration":
            "Migrador completo. Pico migratorio: octubre-noviembre.",
        "iucn_status": "Least Concern",
        "length_cm": "37-47 cm",
        "wingspan_cm": "62-94 cm",
        "diagnostic":
            "Más grande que SS, cabeza notoriamente más grande, "
            "cola larga redondeada (no cuadrada). Capirote oscuro contrastante con la nuca.",
        "best_months": "Octubre-Noviembre",
        "did_you_know":
            "Reclasificada de Accipiter cooperii a Astur cooperii por la AOS en 2023. "
            "Es una de las rapaces que mejor se ha adaptado a ambientes urbanos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Busarellus_nigricollis": {  # BCHA — Black-collared Hawk — Aguililla canela
        "distribution":
            "Tierras bajas tropicales desde México (vertiente del Golfo y Pacífico sur) hasta "
            "Argentina. En México: Veracruz, Tabasco, Chiapas, Oaxaca, sur de Sinaloa.",
        "diet":
            "Especialista en peces; también anfibios, reptiles acuáticos y crustáceos. "
            "Caza desde percha lanzándose al agua.",
        "behavior":
            "Solitaria. Posa en árboles emergentes sobre humedales, ríos y manglares. "
            "Vuelo relativamente lento con aleteos profundos.",
        "migration":
            "Residente sedentaria con dispersión local entre humedales.",
        "iucn_status": "Least Concern",
        "length_cm": "46-51 cm",
        "wingspan_cm": "120-143 cm",
        "diagnostic":
            "Plumaje canela rojizo intenso con cabeza blanca y collar negro distintivo. "
            "Alas anchas, cola corta. Patas con escamas rugosas para sujetar peces.",
        "best_months": "Año redondo (humedales tropicales)",
        "did_you_know":
            "Sus tarsos tienen pequeñas espículas (similares a las del Águila pescadora) que "
            "le permiten sujetar peces resbalosos — una de las pocas aves del Nuevo Mundo "
            "fuera de Pandion con esta adaptación.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_albonotatus": {  # ZTHA — Zone-tailed Hawk — Aguililla aura
        "distribution":
            "Suroeste de EE.UU., México, Centroamérica y norte de Sudamérica. "
            "En México: cañones, bosques de pino-encino y selvas secas de casi todo el país.",
        "diet":
            "Reptiles, mamíferos pequeños y aves. Sorprende a sus presas imitando al Turkey Vulture.",
        "behavior":
            "Mimetismo agresivo: vuela en V poco marcada, casi idéntica al Turkey Vulture, "
            "para acercarse a presas que ignoran a los zopilotes.",
        "migration":
            "Parcialmente migradora. Poblaciones residentes en gran parte de México.",
        "iucn_status": "Least Concern",
        "length_cm": "48-56 cm",
        "wingspan_cm": "121-140 cm",
        "diagnostic":
            "Plumaje completamente negro, cola con bandas blancas anchas. "
            "Cabeza pequeña como zopilote. Vuelo en V.",
        "best_months": "Marzo-Octubre (residente local)",
        "did_you_know":
            "Caso clásico de mimetismo batesiano agresivo: imita al zopilote aura "
            "(presa visualmente similar) para acercarse a sus víctimas inadvertida.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_brachyurus": {  # STHA — Short-tailed Hawk — Aguililla cola corta
        "distribution":
            "Florida sur, México y Centroamérica hasta Argentina. En México habita "
            "bosques tropicales perennifolios y bosques de niebla del Golfo y el Pacífico sur.",
        "diet":
            "Aves pequeñas atrapadas en vuelo, ocasionalmente mamíferos y lagartijas arborícolas.",
        "behavior":
            "Caza desde altura — gira en círculos altos y se lanza en picada. "
            "Existe en dos morfos: claro y oscuro.",
        "migration":
            "Mayormente sedentaria con dispersión local altitudinal.",
        "iucn_status": "Least Concern",
        "length_cm": "38-43 cm",
        "wingspan_cm": "82-103 cm",
        "diagnostic":
            "Cola corta para un Buteo. Morfo claro con pecho blanco; morfo oscuro completamente negro.",
        "best_months": "Año redondo (residente)",
        "did_you_know":
            "Una de las rapaces más pequeñas del género Buteo. Su técnica de caza por picada "
            "desde altura la diferencia del resto de Buteos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_jamaicensis": {  # RTHA — Red-tailed Hawk — Aguililla cola roja
        "distribution":
            "Toda Norteamérica y México hasta Panamá. Migración parcial; "
            "residente común en zonas templadas y semiáridas, e invernante en el sur del país.",
        "diet":
            "Mamíferos pequeños (ratones, ardillas), reptiles y aves.",
        "behavior":
            "Cazadora generalista. Térmica amplia, planeo largo, caza desde percha.",
        "migration":
            "Parcialmente migradora. Pico migratorio en el corredor del Golfo: octubre-noviembre.",
        "iucn_status": "Least Concern",
        "length_cm": "45-65 cm",
        "wingspan_cm": "110-141 cm",
        "diagnostic":
            "Cola roja en adultos (rasgo diagnóstico inmediato). "
            "Alas anchas con punta digitada, vientre con banda oscura.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Su llamado de caza es uno de los más usados en cine como sonido genérico de águila. "
            "Tiene la mayor variación de plumaje de cualquier Buteo (12+ subespecies/morfos).",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_lagopus": {  # RLHA — Rough-legged Hawk — Aguililla ártica
        "distribution":
            "Reproduce en tundra ártica circumpolar. Migra al sur de EE.UU. y norte de México en "
            "invierno. En México: visitante invernal raro en Chihuahua, Sonora y norte de Coahuila.",
        "diet":
            "Mamíferos pequeños, especialmente lemmings en zona de cría; "
            "ratones de campo en zonas de invernada.",
        "behavior":
            "Único Buteo neártico que practica vuelo cernido (hovering) regular. "
            "Caza desde el aire en zonas abiertas.",
        "migration":
            "Migrador completo. Llega al sur solo en inviernos extremos.",
        "iucn_status": "Least Concern",
        "length_cm": "46-60 cm",
        "wingspan_cm": "120-153 cm",
        "diagnostic":
            "Tarsos emplumados hasta los dedos (de ahí el nombre). "
            "Banda subterminal oscura en cola, parche oscuro en muñeca.",
        "best_months": "Diciembre-Febrero (irregular)",
        "did_you_know":
            "Es el único Buteo que rutinariamente practica vuelo cernido sin viento. "
            "Su distribución ártica lo hace una rapaz adaptada a temperaturas extremas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_lineatus": {  # RSHA — Red-shouldered Hawk — Aguililla pecho rojo
        "distribution":
            "Bosques caducifolios húmedos de EE.UU. y noreste de México. "
            "En México: migrante invernal e individuos residentes locales en Tamaulipas, "
            "Nuevo León y norte de Veracruz.",
        "diet":
            "Reptiles (lagartijas, serpientes), anfibios, mamíferos pequeños y aves.",
        "behavior":
            "Caza desde percha en bosque ribereño. "
            "Vocalización aguda y repetida muy distintiva en territorio.",
        "migration":
            "Parcialmente migradora. Pico ligero en Veracruz: octubre-noviembre.",
        "iucn_status": "Least Concern",
        "length_cm": "38-58 cm",
        "wingspan_cm": "94-111 cm",
        "diagnostic":
            "Alas con 'ventanas' translúcidas en primarias internas (visible al contraluz). "
            "Hombros rojizos en adultos, pecho rojizo barrado.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Es una de las pocas rapaces que mantiene territorios reproductores de por vida, "
            "regresando al mismo nido por hasta 20 años consecutivos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_plagiatus": {  # GRHA — Gray Hawk — Aguililla gris
        "distribution":
            "Bosques ribereños y selvas bajas del sur de EE.UU., México y Centroamérica. "
            "En México: ampliamente distribuida en tierras bajas tropicales y subtropicales.",
        "diet":
            "Reptiles (especialmente iguanas), anfibios, mamíferos pequeños.",
        "behavior":
            "Caza desde percha y en planeo bajo. Vocaliza con un silbido descendente único.",
        "migration":
            "Sedentaria con dispersión local. Migración parcial en el norte de su distribución.",
        "iucn_status": "Least Concern",
        "length_cm": "38-46 cm",
        "wingspan_cm": "82-94 cm",
        "diagnostic":
            "Plumaje gris pálido uniforme en adultos. Cola con 2 bandas blancas anchas. "
            "Antes Buteo nitidus — split en 2012 (B. plagiatus en Norteamérica, B. nitidus en Sudamérica).",
        "best_months": "Año redondo (residente)",
        "did_you_know":
            "Antes considerada la misma especie que B. nitidus de Sudamérica. "
            "Estudios genéticos demostraron en 2012 que son especies distintas (split AOS).",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_platypterus": {  # BWHA — Broad-winged Hawk — Aguililla ala ancha
        "distribution":
            "Bosques templados del este de Norteamérica. Migra al Neotrópico en otoño. "
            "ESTRELLA del corredor de Veracruz — millones por temporada.",
        "diet":
            "Reptiles, anfibios, mamíferos pequeños, insectos grandes durante migración.",
        "behavior":
            "Vuelo en grandes 'kettles' (espirales en térmicas) durante migración. "
            "Conserva energía planeando casi sin batir alas.",
        "migration":
            "Migrador completo y obligado. Pico extremo en Veracruz: 15-25 de septiembre, "
            "hasta 30,000 individuos/hora.",
        "iucn_status": "Least Concern",
        "length_cm": "34-44 cm",
        "wingspan_cm": "81-100 cm",
        "diagnostic":
            "Alas cortas y anchas, cola con bandas blancas y negras anchas. "
            "Más pequeña que la mayoría de Buteos.",
        "best_months": "Septiembre (pico) - Octubre",
        "did_you_know":
            "Forma los kettles migratorios más grandes documentados en el mundo. "
            "El 99% de la población global pasa por el corredor del Golfo durante migración.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_regalis": {  # FEHA — Ferruginous Hawk — Aguililla real
        "distribution":
            "Praderas y semidesiertos del oeste de Norteamérica. En México: visitante invernal "
            "regular en pastizales de Chihuahua, Sonora, Durango y norte del Bajío.",
        "diet":
            "Mamíferos medianos (perritos llaneros, conejos, marmotas), ocasionalmente aves.",
        "behavior":
            "Caza desde percha o aérea. Vuelo poderoso, planeo largo.",
        "migration":
            "Parcialmente migradora. Juveniles llegan más al sur que adultos.",
        "iucn_status": "Least Concern",
        "length_cm": "51-69 cm",
        "wingspan_cm": "133-152 cm",
        "diagnostic":
            "Buteo más grande de Norteamérica. Coloración ferruginosa (rojiza-marrón) en alas "
            "y patas. Cola blancuzca con tinte rojizo.",
        "best_months": "Noviembre-Febrero",
        "did_you_know":
            "Es el Buteo más grande de Norteamérica. Sus tarsos emplumados (como B. lagopus) "
            "son una adaptación al frío de las grandes planicies.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_swainsoni": {  # SWHA — Swainson's Hawk — Aguililla de Swainson
        "distribution":
            "Reproduce en praderas del oeste de Norteamérica. "
            "MIGRA hasta Argentina — uno de los viajes más largos del Buteo.",
        "diet":
            "Insectos grandes (saltamontes, libélulas) durante migración; "
            "mamíferos pequeños y reptiles en reproducción.",
        "behavior":
            "Forma grandes 'kettles' migratorios junto con BW. "
            "Adultos casi no comen durante el viaje.",
        "migration":
            "Migrador completo extremo: hasta 14,000 km redondo. "
            "Pico en Veracruz: octubre.",
        "iucn_status": "Least Concern",
        "length_cm": "43-56 cm",
        "wingspan_cm": "117-137 cm",
        "diagnostic":
            "Alas largas y puntiagudas. Adulto típico con pecho rojizo, "
            "vientre claro, primarias oscuras. Polimorfismo importante.",
        "best_months": "Octubre",
        "did_you_know":
            "Realiza una de las migraciones más largas de cualquier rapaz: 14,000 km "
            "redondos entre Norteamérica y Argentina cada año.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_anthracinus": {  # COBH — Common Black Hawk — Aguililla negra menor
        "distribution":
            "Tierras bajas tropicales y subtropicales de México a Sudamérica. En México: "
            "humedales costeros, manglares y riberas tropicales del Golfo y el Pacífico.",
        "diet":
            "Cangrejos, peces, anfibios y reptiles. Especialista de ribera.",
        "behavior":
            "Solitaria. Caza desde percha baja sobre el agua. Vuelo lento, "
            "alas anchas y cola corta. Vocaliza con silbidos prolongados.",
        "migration":
            "Mayormente residente; algunas poblaciones del norte de México son migradoras parciales.",
        "iucn_status": "Least Concern",
        "length_cm": "43-53 cm",
        "wingspan_cm": "100-130 cm",
        "diagnostic":
            "Plumaje negro mate. Una banda blanca ancha en el centro de la cola (otra fina en la "
            "punta). Patas amarillas largas; pico bicolor.",
        "best_months": "Año redondo",
        "did_you_know":
            "Forma parte del 'complejo de aguilillas negras' junto con B. urubitinga y B. solitarius. "
            "Para distinguirlas en juveniles se requiere análisis fino del patrón de cola y "
            "del plumaje de las cobertoras infraalares.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_solitarius": {  # SOEA — Solitary Eagle — Águila solitaria
        "distribution":
            "Bosques montanos y barrancas de México a Argentina. En México: registros raros "
            "y dispersos en Sierra Madre Oriental, Occidental y del Sur, Chiapas y Oaxaca. "
            "Especie poco conocida.",
        "diet":
            "Serpientes, mamíferos medianos arborícolas y aves. Hábitos cripticos.",
        "behavior":
            "Solitaria y silenciosa. Soaring elevado sobre cañones y laderas boscosas. "
            "Rara vez observada en percha.",
        "migration":
            "Residente sedentaria.",
        "iucn_status": "Near Threatened",
        "length_cm": "63-78 cm",
        "wingspan_cm": "150-188 cm",
        "diagnostic":
            "Adulto totalmente gris pizarra oscuro, cola corta con una sola banda blanca ancha. "
            "Alas extraordinariamente anchas y cortas, sobresalen mucho más allá de la cola en planeo.",
        "best_months": "Año redondo (extremadamente difícil de observar)",
        "did_you_know":
            "Estatus poco conocido en México; los pocos registros confirmados están en altitudes "
            "medias de bosque mesófilo y barrancas remotas. Categorizada como 'Near Threatened' "
            "por la IUCN y 'En peligro de extinción' (P) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteogallus_urubitinga": {  # GBHA — Great Black Hawk — Aguililla negra mayor
        "distribution":
            "Tierras bajas tropicales desde México (vertiente del Golfo y Pacífico sur) hasta "
            "Argentina. Más común al sur de Veracruz, en Chiapas, Oaxaca y Yucatán.",
        "diet":
            "Reptiles, anfibios, cangrejos, peces y aves pequeñas. Carroña ocasional.",
        "behavior":
            "Similar a B. anthracinus pero más grande y de hábitos más boscosos. "
            "Caza desde percha baja, también recorre orillas y caminos.",
        "migration":
            "Residente sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "55-70 cm",
        "wingspan_cm": "135-160 cm",
        "diagnostic":
            "Plumaje negro. Cola con DOS bandas blancas anchas (vs. una en B. anthracinus). "
            "Pies y cera amarillos, pico bicolor. Tamaño claramente mayor.",
        "best_months": "Año redondo (mayor concentración en humedales tropicales)",
        "did_you_know":
            "En 2018 un individuo errante apareció en Maine (EE.UU.), generando furor entre los "
            "observadores estadounidenses, pero su rango habitual termina justo en el sureste mexicano.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Caracara_plancus": {  # CRCA — Crested Caracara — Caracara quebrantahuesos
        "distribution":
            "Casi todo México excepto los grandes desiertos del Altiplano Norte. "
            "Especialmente común en pastizales, sabanas y matorrales con presencia humana.",
        "diet":
            "Carroña, reptiles, anfibios, insectos grandes, mamíferos pequeños y huevos. "
            "Oportunista total.",
        "behavior":
            "Camina mucho en el suelo. Forma grupos en cadáveres junto con zopilotes. "
            "Vuelo directo con aleteos pausados; rara vez planea en térmicas como un Buteo.",
        "migration":
            "Residente sedentaria. Movimientos locales por disponibilidad de alimento.",
        "iucn_status": "Least Concern",
        "length_cm": "50-65 cm",
        "wingspan_cm": "118-132 cm",
        "diagnostic":
            "Pico azul-grisáceo grande, cara desnuda roja, cresta negra; pecho y cuello blancos "
            "barrados de negro; alas con primarias claras vistas al vuelo.",
        "best_months": "Año redondo",
        "did_you_know":
            "Aparece en muchas mitologías mesoamericanas. Es la única rapaz neotropical que "
            "regularmente camina en el suelo para forrajear, comportamiento heredado de su "
            "ancestro común con los halcones.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Cathartes_aura": {  # TUVU — Turkey Vulture — Zopilote aura
        "distribution":
            "Distribución amplia en América. Muy común en todo México "
            "tanto como residente como migrante norteño.",
        "diet":
            "Carroña casi exclusivamente. Olfato extraordinario para detectar gases de descomposición.",
        "behavior":
            "Soaring constante en V marcada (diédrico). Balanceo lateral característico. "
            "Forma dormideros comunales.",
        "migration":
            "Migración parcial. Las poblaciones del norte migran masivamente por Veracruz en octubre.",
        "iucn_status": "Least Concern",
        "length_cm": "62-81 cm",
        "wingspan_cm": "160-183 cm",
        "diagnostic":
            "Vuelo en V marcada, cabeza pequeña roja desnuda en adultos. "
            "Alas largas con secundarias plateadas vistas desde abajo.",
        "best_months": "Año redondo, pico migratorio octubre",
        "did_you_know":
            "Tiene uno de los olfatos más finos de las aves — puede detectar carroña "
            "a más de 1 km de distancia. Único Cathartidae que usa olor para forrajear.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Cathartes_burrovianus": {  # LYHV — Lesser Yellow-headed Vulture — Zopilote sabanero
        "distribution":
            "Sabanas y humedales tropicales de México (Veracruz, Tabasco, Campeche, Quintana Roo, "
            "Chiapas) hasta Sudamérica. Reemplaza ecológicamente a C. aura en pastizales bajos.",
        "diet":
            "Carroña, principalmente animales pequeños recién muertos en pastizales y humedales. "
            "Como C. aura, localiza presas por olfato.",
        "behavior":
            "Vuelo en V marcada, muy bajo (1-3 m sobre el pasto). Solitario o en parejas; "
            "no forma kettles. Cabeza coloreada de amarillo en lugar de rojo.",
        "migration":
            "Sedentario; movimientos locales según humedad.",
        "iucn_status": "Least Concern",
        "length_cm": "53-65 cm",
        "wingspan_cm": "150-165 cm",
        "diagnostic":
            "Cabeza desnuda amarilla con tintes anaranjados/azules; plumaje café oscuro; cola "
            "más corta que C. aura. Vuelo bajo sobre pastizales (no soaring elevado).",
        "best_months": "Año redondo en humedales del sureste",
        "did_you_know":
            "Es uno de los tres zopilotes que olfatean carroña — el otro Cathartes (C. melambrotus, "
            "del Amazonas) no llega a México. Su preferencia por pastizales inundables lo hace un "
            "buen indicador de humedales sanos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Chondrohierax_uncinatus": {  # HBKI — Hook-billed Kite — Gavilán pico de gancho
        "distribution":
            "Selvas tropicales de México a Argentina. "
            "En México: bosques tropicales perennifolios del Golfo y Pacífico sur.",
        "diet":
            "Caracoles arbóreos casi exclusivamente. Especialista extremo.",
        "behavior":
            "Solitario, sigiloso. Forrajea entre bromelias y árboles densos. "
            "Pico hipertrofiado adaptado para sacar caracoles de sus conchas.",
        "migration":
            "Sedentaria con dispersión local.",
        "iucn_status": "Least Concern",
        "length_cm": "38-51 cm",
        "wingspan_cm": "78-99 cm",
        "diagnostic":
            "Pico grande y curvo (rasgo diagnóstico). Alas anchas redondeadas. "
            "Cara desnuda blanco-amarilla en adultos.",
        "best_months": "Año redondo (residente raro)",
        "did_you_know":
            "Su pico evolucionó específicamente para sacar caracoles arbóreos del género Bulimulus. "
            "Es uno de los pocos rapaces con dieta tan especializada.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Circus_hudsonius": {  # NOHA — Northern Harrier — Aguilucho norteño
        "distribution":
            "Reproduce en praderas y pantanos de Norteamérica. Migra al sur de EE.UU., "
            "México y Caribe. Invernante común en pastizales y humedales de todo México.",
        "diet":
            "Pequeños mamíferos (ratones) y aves de pastizal.",
        "behavior":
            "Vuelo bajo y planeador sobre pastizales y humedales. "
            "Dimorfismo sexual marcado: hembras café, machos grises.",
        "migration":
            "Migrador completo. Pico en Veracruz: octubre-noviembre.",
        "iucn_status": "Least Concern",
        "length_cm": "41-50 cm",
        "wingspan_cm": "97-122 cm",
        "diagnostic":
            "Alas largas en V poco marcada. PARCHE BLANCO en la rabadilla — diagnóstico inmediato. "
            "Vuelo bajo y oscilante sobre pastizales.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Tiene un disco facial similar a una lechuza, que le ayuda a localizar presas por sonido. "
            "Es la única rapaz diurna del Nuevo Mundo con esta adaptación auditiva.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Coragyps_atratus": {  # BLVU — Black Vulture — Zopilote común
        "distribution":
            "Sur de EE.UU. hasta Argentina. En México es la rapaz más abundante en zonas "
            "tropicales y subtropicales; tolera bien ambientes urbanos y rurales.",
        "diet":
            "Carroña; también basura, frutos en descomposición, huevos, polluelos y crías "
            "vulnerables de ganado. Más agresivo que C. aura en grupos.",
        "behavior":
            "Sociable y gregario. Forma kettles en térmicas y dormideros comunales de cientos "
            "de individuos. Vuelo con aleteos rápidos intercalados con planeo plano.",
        "migration":
            "Sedentario.",
        "iucn_status": "Least Concern",
        "length_cm": "56-74 cm",
        "wingspan_cm": "133-167 cm",
        "diagnostic":
            "Plumaje negro lustroso, cabeza desnuda gris. Cola corta y cuadrada. "
            "Parche blanco-plateado SOLO en las puntas (primarias) vistas en vuelo.",
        "best_months": "Año redondo",
        "did_you_know":
            "Carece del olfato fino de los Cathartes; localiza carroña visualmente o siguiendo "
            "al zopilote aura en vuelo. Es una de las especies dominantes del paisaje aviar "
            "en ciudades mexicanas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Daptrius_americanus": {  # RTCA — Red-throated Caracara — Caracara comecacao
        "distribution":
            "Selvas tropicales lluviosas del sureste de México (selva Lacandona, Calakmul) "
            "hasta Bolivia. Históricamente más distribuido, hoy muy localizado y raro en México.",
        "diet":
            "Avispas y avispero (única rapaz que se especializa en saqueo de panales), "
            "frutos grandes, lagartijas y crías de aves.",
        "behavior":
            "Ruidosa y muy social; vive en grupos de 3-10 individuos relacionados que cooperan "
            "en el ataque a colmenas. Vocaliza con un grito estridente parecido a una risa fuerte.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern (declinante)",
        "length_cm": "51-58 cm",
        "wingspan_cm": "110-125 cm",
        "diagnostic":
            "Plumaje negro brillante; vientre y plumas inferiores de la cola blancas; "
            "cara y garganta rojas; pico amarillo grueso. Aspecto general como un caracara grande oscuro.",
        "best_months": "Año redondo (selvas remotas)",
        "did_you_know":
            "Es la única ave del mundo que ataca colmenas de avispas sociales de manera sistemática. "
            "Ha desaparecido de gran parte de su distribución histórica en México por pérdida de "
            "selva alta. Categorizada como 'En peligro' (P) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Elanoides_forficatus": {  # STKI — Swallow-tailed Kite — Milano tijereta
        "distribution":
            "Sur de EE.UU., México, Centro y Sudamérica. "
            "En México reproductor estival en selvas tropicales del Golfo y migratorio común.",
        "diet":
            "Insectos voladores grandes, pequeños vertebrados arbóreos, ranas.",
        "behavior":
            "Vuelo extraordinariamente ágil y elegante. Captura insectos en el aire. "
            "Migra en grupos sociales.",
        "migration":
            "Migrador completo. Pico en Veracruz: agosto-septiembre y marzo.",
        "iucn_status": "Least Concern",
        "length_cm": "52-65 cm",
        "wingspan_cm": "112-136 cm",
        "diagnostic":
            "Cola profundamente ahorquillada (rasgo único). Plumaje blanco y negro contrastante. "
            "Vuelo elegante 'como golondrina gigante'.",
        "best_months": "Agosto-Septiembre (pico migratorio)",
        "did_you_know":
            "Su cola ahorquillada le da una de las maniobras más ágiles entre las rapaces. "
            "Es una de las pocas rapaces que come exclusivamente en el aire o el follaje.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Elanus_leucurus": {  # WTKI — White-tailed Kite — Milano coliblanco
        "distribution":
            "Distribución disjunta en América: oeste y sur de EE.UU., México, Centroamérica "
            "y región del Cono Sur. En México: pastizales abiertos, sabanas y matorrales del "
            "Bajío, vertiente del Golfo y Pacífico.",
        "diet":
            "Mamíferos pequeños, especialmente ratones de campo; insectos grandes; "
            "ocasionalmente aves muy pequeñas.",
        "behavior":
            "Cernido prolongado (hovering) sobre pastizales — único Elanus que lo hace bien. "
            "Postura de 'hombros elevados' característica. Forma dormideros comunales en árboles.",
        "migration":
            "Mayormente sedentario; movimientos locales por irrupciones de roedores.",
        "iucn_status": "Least Concern",
        "length_cm": "35-43 cm",
        "wingspan_cm": "88-105 cm",
        "diagnostic":
            "Plumaje gris perla con vientre y cola blancos. Hombros y banda en el ala negras "
            "muy marcadas. Ojos rojos. Cernido sistemático.",
        "best_months": "Año redondo (más visible en pastizales)",
        "did_you_know":
            "Sus poblaciones pueden multiplicarse rápidamente en años de irrupciones de ratones, "
            "fenómeno documentado tanto en California como en el Bajío mexicano.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_columbarius": {  # MERL — Merlin — Esmerejón
        "distribution":
            "Reproduce en bosques boreales y praderas norteñas. "
            "Migra al sur de EE.UU., México y Centroamérica.",
        "diet":
            "Aves pequeñas atrapadas en vuelo rápido sobre espacios abiertos.",
        "behavior":
            "Vuelo extremadamente rápido y directo, con aleteos potentes. "
            "Cazador agresivo y especializado en aves de pastizal.",
        "migration":
            "Migrador completo. Pico en Veracruz: octubre.",
        "iucn_status": "Least Concern",
        "length_cm": "24-33 cm",
        "wingspan_cm": "53-69 cm",
        "diagnostic":
            "Tamaño pequeño, alas puntiagudas. Cola con bandas grises pálidas. "
            "Más oscuro y compacto que el Kestrel.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Aunque pequeño, es uno de los más feroces de su tamaño. "
            "Históricamente usado en cetrería europea, conocido como 'merlin' desde la Edad Media.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_deiroleucus": {  # OBFA — Orange-breasted Falcon — Halcón pechirrufo
        "distribution":
            "Distribución muy local en selvas tropicales con acantilados, desde el sur de México "
            "(Chiapas, Tabasco, Veracruz interior) hasta Argentina. Una de las rapaces más raras "
            "y enigmáticas del Neotrópico.",
        "diet":
            "Aves de tamaño mediano-grande (palomas, perdices, loros) atrapadas en picada potente. "
            "Murciélagos al crepúsculo.",
        "behavior":
            "Solitario o en parejas territoriales. Nidifica en acantilados emergentes sobre selva. "
            "Vuela poderoso y veloz, similar al peregrino pero con cabeza más robusta.",
        "migration":
            "Sedentario.",
        "iucn_status": "Near Threatened",
        "length_cm": "35-40 cm",
        "wingspan_cm": "85-95 cm",
        "diagnostic":
            "Pecho y cuello anaranjado-rufo intensos contrastando con vientre negro barrado y "
            "garganta blanca. Cabeza grande, espalda azul-negra. Apariencia robusta tipo bulldog.",
        "best_months": "Año redondo (pero extremadamente difícil de observar)",
        "did_you_know":
            "Su población mundial se estima en menos de 1,000 individuos. La Mesoamerican "
            "Population (incluyendo México) ha sido objeto del programa de rescate más intensivo "
            "de The Peregrine Fund. Categorizada como 'En peligro' (P) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_femoralis": {  # APFA — Aplomado Falcon — Halcón fajado
        "distribution":
            "Pastizales abiertos y matorrales del suroeste de EE.UU. (donde fue reintroducido), "
            "México y Sudamérica. En México: pastizales del altiplano norte, costa del Golfo "
            "y Pacífico sur. Se recupera lentamente tras casi extirparse del país.",
        "diet":
            "Aves pequeñas y medianas, lagartijas, insectos grandes. Caza en parejas cooperativas.",
        "behavior":
            "Ágil y rápido. Suele cazar en pareja, una persiguiendo y la otra cortando rutas de "
            "escape. Posa en partes altas de arbustos, postes y árboles aislados.",
        "migration":
            "Residente; algunos movimientos altitudinales y locales.",
        "iucn_status": "Least Concern (en recuperación regional)",
        "length_cm": "35-45 cm",
        "wingspan_cm": "78-102 cm",
        "diagnostic":
            "Esbelto, alas y cola largas. Pecho blanco con banda negra ancha en el vientre, "
            "muslos canela; cara blanca con bigote negro fino; ceja blanca prominente.",
        "best_months": "Año redondo en pastizales norteños",
        "did_you_know":
            "Casi extirpado de Norteamérica a mediados del siglo XX, su recuperación en Texas "
            "y Chihuahua es uno de los éxitos más recientes de conservación de rapaces. "
            "Categorizada como 'Amenazada' (A) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_peregrinus": {  # PEFA — Peregrine Falcon — Halcón peregrino
        "distribution":
            "Cosmopolita. Reproduce en acantilados, montañas y edificios urbanos. "
            "En México: invernante y residente local en costas, sierras y grandes ciudades.",
        "diet":
            "Casi exclusivamente aves atrapadas en vuelo — desde palomas hasta patos.",
        "behavior":
            "Stoop (picada vertical) a más de 320 km/h — el animal más rápido del planeta. "
            "Caza solitaria, ataca desde gran altura.",
        "migration":
            "Migrador parcial. Pico en Veracruz: octubre.",
        "iucn_status": "Least Concern (recuperado tras DDT)",
        "length_cm": "34-58 cm",
        "wingspan_cm": "74-120 cm",
        "diagnostic":
            "'Capucha' negra muy marcada. Alas largas y puntiagudas. Cola relativamente corta. "
            "Vuelo poderoso y directo.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Es el animal más rápido del mundo: alcanza 389 km/h en su picada (stoop). "
            "Casi se extingue por el DDT pero se recuperó tras su prohibición.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_rufigularis": {  # BAFA — Bat Falcon — Halcón murcielaguero
        "distribution":
            "Tierras bajas tropicales desde México (Tamaulipas, Veracruz, Tabasco, Chiapas, "
            "Yucatán, Oaxaca, Jalisco hacia el sur) hasta Argentina. Bordes de selva y áreas "
            "agrícolas con árboles emergentes.",
        "diet":
            "Murciélagos y aves pequeñas atrapadas al amanecer y atardecer; insectos grandes "
            "(libélulas, mariposas, cigarras) durante el día.",
        "behavior":
            "Posa muy alto, generalmente en ramas expuestas en lo alto de árboles emergentes. "
            "Caza en vuelos cortos y rápidos. Crepuscular, especialmente para murciélagos.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "24-30 cm",
        "wingspan_cm": "65-72 cm",
        "diagnostic":
            "Pequeño y compacto. Capucha negra, garganta y collar blancos, pecho negro barrado, "
            "vientre rufo intenso. Alas y cola largas relativas al cuerpo.",
        "best_months": "Año redondo",
        "did_you_know":
            "Es uno de los pocos halcones del mundo que caza murciélagos sistemáticamente al "
            "anochecer, ocupando un nicho similar al de los halcones forestales y los "
            "halcones del pantano del Viejo Mundo.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Falco_sparverius": {  # AMKE — American Kestrel — Cernícalo americano
        "distribution":
            "Amplia distribución en América. Residente y migratorio en casi todo México.",
        "diet":
            "Insectos grandes, ratones, lagartijas, aves muy pequeñas.",
        "behavior":
            "Vuelo cernido (hovering) sobre pastizales — única rapaz pequeña que lo hace bien. "
            "Caza desde percha en líneas de alta tensión.",
        "migration":
            "Parcialmente migradora.",
        "iucn_status": "Least Concern (declinante)",
        "length_cm": "22-31 cm",
        "wingspan_cm": "51-61 cm",
        "diagnostic":
            "Tamaño pequeño, alas puntiagudas, cola rufa con banda terminal negra. "
            "Doble bigote negro en cara. Macho con espalda rojiza y alas azules.",
        "best_months": "Año redondo, pico migratorio octubre-noviembre",
        "did_you_know":
            "Es la rapaz más pequeña de Norteamérica. Sus poblaciones han declinado un 50% "
            "en los últimos 50 años — causas exactas aún investigándose.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Geranoaetus_albicaudatus": {  # WTHA — White-tailed Hawk — Aguililla cola blanca
        "distribution":
            "Pastizales y matorrales abiertos del sur de Texas, México y Sudamérica. "
            "En México: costa del Golfo, Pacífico, Valle del Mezquital y altiplano sur.",
        "diet":
            "Mamíferos pequeños y medianos, reptiles, aves de pastizal, insectos grandes. "
            "Llamativamente, congrega en quemas de pastos para cazar lo que huye del fuego.",
        "behavior":
            "Soaring elegante con alas anchas y cortas. Solitario o en parejas. Sigue maquinaria "
            "agrícola y fuegos para atrapar presas perturbadas.",
        "migration":
            "Residente.",
        "iucn_status": "Least Concern",
        "length_cm": "44-60 cm",
        "wingspan_cm": "118-143 cm",
        "diagnostic":
            "Adulto: parte superior gris oscura, pecho blanco, cola blanca con banda subterminal "
            "negra fina; hombro rojizo bien delimitado. Alas anchas que parecen 'cortadas en bloque'.",
        "best_months": "Año redondo",
        "did_you_know":
            "Reclasificada del género Buteo a Geranoaetus en 2014 con base en filogenia molecular. "
            "Junto con G. melanoleucus (Sudamérica) y G. polyosoma, forma el grupo de las "
            "aguilillas andinas, aunque ella habita tierras bajas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Geranospiza_caerulescens": {  # CRHA — Crane Hawk — Gavilán zancón
        "distribution":
            "Tierras bajas tropicales desde el sur de México (vertiente del Golfo desde Tamaulipas, "
            "y Pacífico desde Sinaloa) hasta Argentina.",
        "diet":
            "Aves anidadoras en cavidades, polluelos, reptiles, anfibios, murciélagos extraídos "
            "de huecos en árboles, ramas y palmas.",
        "behavior":
            "Solitario. Camina sobre ramas y se acerca a cavidades para extraer presas con sus "
            "tarsos extremadamente largos y articulación tibio-tarsiana doblable (única).",
        "migration":
            "Residente.",
        "iucn_status": "Least Concern",
        "length_cm": "38-54 cm",
        "wingspan_cm": "82-112 cm",
        "diagnostic":
            "Plumaje gris pizarra uniforme; cola larga con dos bandas blancas; tarsos extra "
            "largos color anaranjado. Aspecto esbelto, casi de zancudo (de ahí su nombre).",
        "best_months": "Año redondo",
        "did_you_know":
            "Posee una articulación doble inusual entre la tibia y el tarso que le permite doblar "
            "la pata hacia atrás y atrás, único entre las rapaces; le sirve para meter la pata "
            "en huecos profundos y extraer crías de aves y murciélagos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Haliaeetus_leucocephalus": {  # BAEA — Bald Eagle — Águila calva
        "distribution":
            "Toda Norteamérica, especialmente costas y grandes lagos. En México: invernante "
            "raro en costa del Pacífico y norte de Baja California; registros excepcionales "
            "en la vertiente del Golfo.",
        "diet":
            "Peces principalmente; también aves acuáticas, carroña y mamíferos pequeños.",
        "behavior":
            "Soaring elegante sobre cuerpos de agua. Roba presas de Osprey ocasionalmente. "
            "Pareja de por vida.",
        "migration":
            "Parcialmente migrador. Adultos pueden ser sedentarios.",
        "iucn_status": "Least Concern (recuperado tras DDT)",
        "length_cm": "70-102 cm",
        "wingspan_cm": "180-244 cm",
        "diagnostic":
            "Cabeza y cola blancas en adultos (juveniles totalmente cafés). "
            "Pico amarillo enorme. Una de las rapaces más grandes de América.",
        "best_months": "Diciembre-Febrero (registros invernales raros)",
        "did_you_know":
            "Ave nacional de EE.UU. Casi se extinguió por el DDT en los años 60 — quedaban "
            "menos de 500 parejas en los 48 estados continentales. Hoy hay >70,000.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Harpagus_bidentatus": {  # DTKI — Double-toothed Kite — Gavilán bidentado
        "distribution":
            "Selvas tropicales lluviosas desde el sur de México (Veracruz, Oaxaca, Chiapas, "
            "Tabasco, Campeche, Quintana Roo) hasta Bolivia.",
        "diet":
            "Insectos grandes (escarabajos, mantis, saltamontes) y lagartijas pequeñas. "
            "Sigue tropas de monos cariblanco que perturban insectos al moverse en el dosel.",
        "behavior":
            "Posa quieto bajo el dosel. Sigue grupos mixtos de aves y de primates ('beater flocks') "
            "para capturar presas que huyen. Vuelo rápido y directo.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "30-36 cm",
        "wingspan_cm": "65-75 cm",
        "diagnostic":
            "Pequeño, gris azulado en la espalda, pecho con tinte rufo barrado finamente, "
            "vientre blanco; cola con bandas claras. Borde de plumas inferiores de la cola blanco-puro. "
            "Dos pequeños 'dientes' en cada borde de la mandíbula superior (rasgo del que toma su nombre).",
        "best_months": "Año redondo",
        "did_you_know":
            "Asocia su forrajeo con las tropas de monos cariblanco (Cebus capucinus) y otras aves "
            "del sotobosque tropical, demostrando una de las relaciones de cleptoparasitismo "
            "indirecto mejor documentadas entre rapaces y primates.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Harpia_harpyja": {  # HAEA — Harpy Eagle — Águila arpía
        "distribution":
            "Selvas húmedas continuas desde el sur de México (selva Lacandona, Chiapas; norte de "
            "Oaxaca; Calakmul, Campeche) hasta Bolivia y norte de Argentina. En México prácticamente "
            "extirpada de su distribución histórica.",
        "diet":
            "Perezosos y monos arborícolas; coatíes, kinkajous, iguanas grandes y aves de gran "
            "tamaño (curasows, tucanes). Una de las rapaces más poderosas del mundo.",
        "behavior":
            "Solitaria y silenciosa. Caza desde percha alta en el dosel. Pareja territorial muy "
            "fiel a un nido durante décadas. Sólo cría un polluelo cada 2-3 años.",
        "migration":
            "Sedentaria; necesita extensas áreas de selva intacta.",
        "iucn_status": "Vulnerable",
        "length_cm": "86-107 cm",
        "wingspan_cm": "176-224 cm",
        "diagnostic":
            "Inmensa. Dorso gris pizarra, vientre blanco con banda pectoral negra ancha; doble "
            "cresta de plumas en la cabeza; tarsos extremadamente robustos del grosor de una "
            "muñeca humana, con garras de hasta 13 cm.",
        "best_months": "Año redondo (prácticamente imposible sin búsqueda dedicada)",
        "did_you_know":
            "Sus garras son más grandes que las de un oso grizzly. En México queda muy poca "
            "población — quizá menos de 20 parejas reproductoras confirmadas. Categorizada como "
            "'En peligro' (P) en la NOM-059 y 'Vulnerable' por la IUCN.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Herpetotheres_cachinnans": {  # LAFA — Laughing Falcon — Halcón guaco
        "distribution":
            "Selvas tropicales y bosques semihúmedos desde México (Sinaloa, San Luis Potosí, "
            "Tamaulipas hacia el sur) hasta Argentina.",
        "diet":
            "Especialista en serpientes (incluidas venenosas: nauyacas, coralillos), "
            "ocasionalmente lagartijas grandes.",
        "behavior":
            "Posa quieto en perchas semicubiertas, dejando caer rápidamente sobre serpientes. "
            "Vocaliza fuerte y largamente al amanecer y atardecer: el 'guaco-guaco-guaco' que "
            "le da su nombre y que rurales asocian con presencia de serpientes.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "43-56 cm",
        "wingspan_cm": "79-94 cm",
        "diagnostic":
            "Cabeza grande, ojos oscuros con antifaz negro ancho; corona y cuello cremoso; "
            "vientre crema-blanco; alas y cola café oscuras barradas. Llamado risueño inconfundible.",
        "best_months": "Año redondo",
        "did_you_know":
            "Su nombre 'guaco' viene de la onomatopeya de su llamado y existe la creencia popular "
            "mexicana de que su canto avisa la presencia de víboras. Es uno de los pocos falcónidos "
            "del mundo especializados en cazar serpientes.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Ictinia_mississippiensis": {  # MIKI — Mississippi Kite — Milano de Mississippi
        "distribution":
            "Sur central de EE.UU. Migra a Sudamérica. "
            "Pico migratorio fuerte por el corredor de Veracruz.",
        "diet":
            "Insectos grandes (libélulas, cigarras, escarabajos) atrapados en el aire.",
        "behavior":
            "Vuelo extraordinariamente ágil. Caza insectos en vuelo. "
            "Coloniza ambientes urbanos en EE.UU. (pueblos pequeños del centro-sur).",
        "migration":
            "Migrador completo. Pico en Veracruz: septiembre-octubre.",
        "iucn_status": "Least Concern",
        "length_cm": "29-37 cm",
        "wingspan_cm": "75-91 cm",
        "diagnostic":
            "Pequeña, alas largas y puntiagudas, cola larga y oscura. "
            "Cabeza pálida contrastante. Vuelo ágil casi como vencejo.",
        "best_months": "Septiembre-Octubre",
        "did_you_know":
            "Es uno de los milanos más insectívoros — su dieta es 90% insectos grandes. "
            "Migra en grandes grupos sociales con Buteo platypterus y B. swainsoni.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Ictinia_plumbea": {  # PLKI — Plumbeous Kite — Milano plomizo
        "distribution":
            "Sustituye al milano de Mississippi en los trópicos: México (Veracruz, Tabasco, "
            "Oaxaca, Chiapas, Yucatán) hasta Argentina. Reproductor estival en México.",
        "diet":
            "Insectos voladores grandes (libélulas, cigarras, mariposas), murciélagos pequeños "
            "y aves muy pequeñas. Captura todo en vuelo.",
        "behavior":
            "Vuelo elegante y ágil. Forma agrupaciones laxas, sobre todo durante migración. "
            "Reproductor en árboles emergentes del dosel.",
        "migration":
            "Migrador parcial: poblaciones mexicanas migran al sur tras la temporada reproductiva.",
        "iucn_status": "Least Concern",
        "length_cm": "33-38 cm",
        "wingspan_cm": "82-95 cm",
        "diagnostic":
            "Gris plomizo uniforme; primarias rufas (visibles al vuelo); cola larga negra con "
            "DOS bandas blancas (vs. I. mississippiensis que tiene una sola banda subterminal).",
        "best_months": "Abril-Septiembre (temporada reproductora)",
        "did_you_know":
            "Es la versión tropical del milano de Mississippi: morfológicamente muy similar pero "
            "se distingue por la cola con dos bandas blancas y las primarias rufas visibles en vuelo.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Leptodon_cayanensis": {  # GHKI — Gray-headed Kite — Milano cabecigris
        "distribution":
            "Selvas tropicales y bosques de galería desde el sur de México (sureste de "
            "San Luis Potosí, Veracruz, Tabasco, Chiapas, Yucatán) hasta Argentina.",
        "diet":
            "Avispas, larvas de avispas y abejas extraídas de nidos; ranas arborícolas, "
            "lagartijas, polluelos. Especialista en colmenas.",
        "behavior":
            "Solitario; vuelo ondulante y silencioso. Hace exhibiciones espectaculares de "
            "cortejo con vuelos en círculos y picadas. Posa quieto bajo el dosel.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "46-53 cm",
        "wingspan_cm": "90-110 cm",
        "diagnostic":
            "Cabeza gris pálida marcada con cara más oscura, dorso negro azulado, vientre blanco; "
            "cola con bandas negras y blancas. Pico azulado claramente bicolor.",
        "best_months": "Año redondo",
        "did_you_know":
            "Su comportamiento de cortejo incluye vuelos en círculos altísimos acompañados de "
            "vocalizaciones y picadas verticales, uno de los espectáculos más vistosos entre los "
            "milanos neotropicales.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Micrastur_ruficollis": {  # BFFA — Barred Forest-Falcon — Halcón selvático barrado
        "distribution":
            "Selvas tropicales lluviosas y bosques mesófilos desde el sur de México (Veracruz, "
            "Chiapas, Tabasco, Oaxaca) hasta Argentina.",
        "diet":
            "Aves pequeñas del sotobosque, lagartijas, mamíferos pequeños e insectos grandes. "
            "Sigue tropas de hormigas legionarias para atrapar presas que huyen.",
        "behavior":
            "Tímido y difícil de observar. Caza desde percha baja en el sotobosque con vuelos "
            "muy cortos y certeros. Vocaliza con un 'kaa-kaa-kaa' acelerado al amanecer.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "31-38 cm",
        "wingspan_cm": "55-67 cm",
        "diagnostic":
            "Pequeño, cola larga, tarsos largos amarillos. Espalda gris pizarra, pecho y vientre "
            "blancos finamente barrados de negro. Ojos oscuros, cara desnuda amarilla.",
        "best_months": "Año redondo (más oído que visto)",
        "did_you_know":
            "Forma parte del enigmático grupo de halcones selváticos del género Micrastur, con "
            "alas cortas y cola larga adaptadas para maniobrar entre árboles densos — convergencia "
            "ecológica con los Astur y Accipiter del Viejo Mundo.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Micrastur_semitorquatus": {  # CFFA — Collared Forest-Falcon — Halcón selvático de collar
        "distribution":
            "Selvas tropicales y bosques mesófilos desde México (Sinaloa, Tamaulipas y sur "
            "del país) hasta Argentina.",
        "diet":
            "Aves medianas y grandes (palomas, tinámidos, chachalacas), mamíferos arborícolas, "
            "reptiles. Una de las rapaces forestales más versátiles.",
        "behavior":
            "Sigiloso; persigue presas corriendo por el suelo de la selva o por ramas, no solo "
            "en vuelo. Vocaliza con un característico 'kak-kak-kak-aaaa' descendente.",
        "migration":
            "Sedentario.",
        "iucn_status": "Least Concern",
        "length_cm": "46-58 cm",
        "wingspan_cm": "72-86 cm",
        "diagnostic":
            "Tres morfos (claro, intermedio y oscuro). Cuello con collar amarillo claro "
            "(en el morfo claro); cola larga con bandas blancas; tarsos largos amarillos. "
            "Mucho más grande que M. ruficollis.",
        "best_months": "Año redondo",
        "did_you_know":
            "Uno de los pocos halcones del mundo que persigue presas corriendo por el suelo y "
            "trepando por ramas, comportamiento más típico de las rapaces forestales del Viejo "
            "Mundo. Sus largos tarsos son una adaptación a este estilo de caza.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Morphnus_guianensis": {  # CREA — Crested Eagle — Águila monera
        "distribution":
            "Selvas húmedas continuas desde el sur de México (selva Lacandona, Chiapas; sureste "
            "de Oaxaca; Calakmul) hasta Argentina. Extremadamente rara en México y en franca "
            "declinación.",
        "diet":
            "Mamíferos arborícolas (monos pequeños, kinkajous, comadrejas), reptiles grandes "
            "(iguanas), aves medianas. Más versátil pero menos potente que su congénere arpía.",
        "behavior":
            "Solitaria. Caza desde percha en el dosel. Sólo cría un polluelo cada 2-3 años. "
            "Territorios extremadamente extensos (hasta 50 km²).",
        "migration":
            "Sedentaria.",
        "iucn_status": "Near Threatened",
        "length_cm": "71-89 cm",
        "wingspan_cm": "140-180 cm",
        "diagnostic":
            "Grande, esbelta. Cresta puntiaguda (más fina que la doble cresta del águila arpía). "
            "Dorso gris pizarra, pecho blanco con tinte canela según morfo; cola larga con bandas "
            "anchas; tarsos plumosos.",
        "best_months": "Año redondo (búsqueda dedicada)",
        "did_you_know":
            "Junto con Harpia harpyja forma el género hermano más cercano dentro de la subfamilia "
            "Harpiinae. Es presa de competencia con el águila arpía donde coexisten. "
            "Categorizada como 'En peligro' (P) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Pandion_haliaetus": {  # OSPR — Osprey — Águila pescadora
        "distribution":
            "Cosmopolita. En México invernante a lo largo de la costa y ríos; residente raro "
            "en la península de Baja California, Sonora y costa del Pacífico tropical.",
        "diet":
            "Peces casi exclusivamente, atrapados en picada al agua.",
        "behavior":
            "Vuela sobre cuerpos de agua, se cierne y se lanza en picada. "
            "Único entre las rapaces — pies con espículas para sujetar peces resbalosos.",
        "migration":
            "Migrador completo. Pico en Veracruz: octubre.",
        "iucn_status": "Least Concern",
        "length_cm": "50-66 cm",
        "wingspan_cm": "127-180 cm",
        "diagnostic":
            "Alas largas con quiebre en muñeca (forma de M). Pecho blanco con banda oscura. "
            "Banda ocular negra muy marcada.",
        "best_months": "Octubre-Marzo",
        "did_you_know":
            "Es la única rapaz mundial cuyos pies tienen espículas (papilas espinosas) en las "
            "almohadillas — adaptación para sujetar peces resbalosos. Familia monotípica.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Parabuteo_unicinctus": {  # HASH — Harris's Hawk — Aguililla rojinegra
        "distribution":
            "Desiertos, matorrales xerófilos y sabanas semiáridas del suroeste de EE.UU., "
            "México (especialmente Sonora, Chihuahua, Coahuila, Tamaulipas, Bajío, sur del país) "
            "hasta Argentina.",
        "diet":
            "Conejos, ardillas terrestres, aves de pastizal y reptiles. Caza en grupos "
            "familiares cooperativos de 2-7 individuos — único entre las aves de presa.",
        "behavior":
            "Caza COOPERATIVA en grupos familiares: una técnica donde varios individuos rodean "
            "y empujan a la presa para que otro la atrape. Comportamiento socio-cazador único "
            "entre las rapaces.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "45-59 cm",
        "wingspan_cm": "103-120 cm",
        "diagnostic":
            "Café chocolate oscuro; hombros y muslos canela rojizos intensos; cola con base y "
            "punta blancas anchas. Aspecto compacto y musculoso.",
        "best_months": "Año redondo",
        "did_you_know":
            "Es la única rapaz del mundo que caza regularmente en grupos cooperativos familiares, "
            "comportamiento más típico de los cánidos. Por esta razón es la rapaz más usada en "
            "cetrería moderna.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Pseudastur_albicollis": {  # WHHA — White Hawk — Aguililla blanca
        "distribution":
            "Selvas tropicales lluviosas y bosques mesófilos desde el sur de México (Veracruz, "
            "Oaxaca, Chiapas, Tabasco, Quintana Roo) hasta Brasil.",
        "diet":
            "Reptiles (iguanas, serpientes), mamíferos arborícolas pequeños, aves del sotobosque. "
            "Sigue tropas de monos para capturar lo que perturban.",
        "behavior":
            "Posa en lo alto del dosel. Soaring elegante. Suele seguir a hormigas legionarias y "
            "tropas de monos cariblancos.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "48-56 cm",
        "wingspan_cm": "110-125 cm",
        "diagnostic":
            "Aspecto inconfundible: plumaje casi enteramente blanco; alas con banda terminal y "
            "borde posterior negros; cola con banda subterminal negra ancha y punta blanca. "
            "Patas amarillas.",
        "best_months": "Año redondo",
        "did_you_know":
            "Reclasificada del género Leucopternis a Pseudastur (2014). Forma asociaciones con "
            "monos araña y aulladores: cuando los primates se desplazan por el dosel, perturban "
            "presas pequeñas que el ave captura.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Rostrhamus_sociabilis": {  # SNKI — Snail Kite — Caracolero común
        "distribution":
            "Humedales tropicales y subtropicales desde Florida y México (Veracruz, Tabasco, "
            "Campeche, Yucatán, Chiapas, Sinaloa) hasta Argentina.",
        "diet":
            "Especialista extremo en caracoles acuáticos del género Pomacea (manzanas o jutes). "
            "Casi no come otra cosa.",
        "behavior":
            "Sociable y gregario. Forma dormideros comunales de cientos de individuos. Vuelo "
            "lento sobre humedales. Posa en estacas y juncos para extraer caracoles con su pico curvado.",
        "migration":
            "Sedentaria pero con movimientos locales según niveles de agua y abundancia de caracoles.",
        "iucn_status": "Least Concern",
        "length_cm": "36-48 cm",
        "wingspan_cm": "100-120 cm",
        "diagnostic":
            "Pico estrecho extraordinariamente curvado. Macho gris pizarra oscuro casi negro; "
            "hembra café con vientre estriado; ambos con base de la cola blanca evidente.",
        "best_months": "Año redondo en humedales del Golfo y Pacífico sur",
        "did_you_know":
            "Su pico evolucionó específicamente para extraer caracoles Pomacea de sus conchas "
            "sin romperlas. Es uno de los pocos casos documentados de coevolución entre un "
            "rapaz y su presa principal.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Rupornis_magnirostris": {  # ROHA — Roadside Hawk — Aguililla caminera
        "distribution":
            "Una de las rapaces más comunes en zonas tropicales y subtropicales de América. "
            "En México: tierras bajas del Golfo (Tamaulipas-Chiapas) y Pacífico tropical "
            "(Sinaloa al sur).",
        "diet":
            "Lagartijas, insectos grandes, anfibios, ratones, polluelos y pichones. Generalista.",
        "behavior":
            "Vista a menudo en postes y árboles aislados junto a caminos rurales (de ahí su nombre). "
            "Tolera bien la presencia humana. Vuelo con aleteos pausados y planeos cortos.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern",
        "length_cm": "33-41 cm",
        "wingspan_cm": "70-94 cm",
        "diagnostic":
            "Tamaño mediano-pequeño. Cabeza y pecho café-grisáceos, vientre blanquecino barrado "
            "de canela; cola con bandas oscuras y claras alternas. Iris pálido amarillento.",
        "best_months": "Año redondo",
        "did_you_know":
            "Hasta 2014 fue ubicada en el género Buteo; análisis filogenéticos la separaron en su "
            "propio género Rupornis. Es la rapaz Buteonine más adaptable a paisajes antropizados "
            "del Neotrópico.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Sarcoramphus_papa": {  # KIVU — King Vulture — Zopilote rey
        "distribution":
            "Selvas tropicales y sabanas arboladas desde el sur de México (Veracruz, Chiapas, "
            "Tabasco, Oaxaca, Yucatán, sur de Quintana Roo) hasta Argentina. Localizado y raro "
            "en México.",
        "diet":
            "Carroña; suele abrir cadáveres grandes con su pico potente, permitiendo después "
            "el acceso a otros zopilotes que no pueden romper la piel.",
        "behavior":
            "Solitario o en parejas. Vuelo majestuoso en términos altísimas. Llega a cadáveres "
            "atraído por congregaciones previas de Coragyps y Cathartes.",
        "migration":
            "Sedentario.",
        "iucn_status": "Least Concern (declinante en México)",
        "length_cm": "67-81 cm",
        "wingspan_cm": "170-200 cm",
        "diagnostic":
            "Plumaje crema-blanco con alas y cola negras. Cabeza desnuda multicolor (rojo, "
            "naranja, amarillo, púrpura) con carúncula carnosa anaranjada sobre el pico. "
            "Inconfundible adulto.",
        "best_months": "Año redondo (selvas del sureste)",
        "did_you_know":
            "Es la rapaz más colorida del mundo y único miembro de su género. En la mitología "
            "maya era considerado mensajero entre los dioses y los humanos. Categorizada como "
            "'En peligro' (P) en la NOM-059.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_melanoleucus": {  # BAWE — Black-and-white Hawk-Eagle — Águila blanquinegra
        "distribution":
            "Selvas y bosques montanos desde el sur de México (Veracruz, Oaxaca, Chiapas) hasta "
            "Argentina. Rara y local en México.",
        "diet":
            "Aves medianas y grandes (palomas, oropéndolas, tucanes pequeños), reptiles y "
            "mamíferos arborícolas.",
        "behavior":
            "Soaring muy alto sobre el dosel — más a menudo visto en vuelo que perchada. "
            "Solitaria o en pareja. Vocaliza con un silbido descendente largo.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern (rara regionalmente)",
        "length_cm": "50-60 cm",
        "wingspan_cm": "115-135 cm",
        "diagnostic":
            "Cabeza, cuello y vientre blancos puros; espalda y alas negras contrastantes; "
            "antifaz negro corto en la cara. Cresta corta. Vuelo majestuoso con alas largas.",
        "best_months": "Año redondo (extremadamente difícil)",
        "did_you_know":
            "Anteriormente ubicada en el género Spizastur. Su plumaje altamente contrastante es "
            "único entre los Spizaetus mexicanos y permite identificarla a kilómetros de distancia "
            "cuando hace soaring sobre el dosel.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_ornatus": {  # ORHE — Ornate Hawk-Eagle — Águila elegante
        "distribution":
            "Selvas tropicales lluviosas y bosques mesófilos del sur de México (Veracruz, "
            "Oaxaca, Chiapas, Tabasco, Quintana Roo) hasta Brasil. Rara en México por pérdida "
            "de hábitat.",
        "diet":
            "Aves medianas (chachalacas, tucanes, loros, palomas grandes), mamíferos pequeños "
            "y reptiles. Caza desde percha con vuelos potentes.",
        "behavior":
            "Solitaria. Caza desde percha en el dosel. Vocaliza con silbidos altos y descendentes. "
            "Vuelo poderoso con alas anchas y cola larga.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Near Threatened",
        "length_cm": "56-66 cm",
        "wingspan_cm": "117-142 cm",
        "diagnostic":
            "Cresta larga puntiaguda erecta. Cara, lados del cuello y pecho rufo intenso; corona "
            "negra; vientre blanco intenso con barras negras finas; cola con bandas claras y oscuras. "
            "Una de las rapaces más espectaculares de América.",
        "best_months": "Año redondo (búsqueda dedicada en selva alta)",
        "did_you_know":
            "Considerada por muchos ornitólogos como la rapaz más bella de América por su "
            "combinación de colores y la cresta erguible. Categorizada como 'En peligro' (P) "
            "en la NOM-059 y 'Casi amenazada' por la IUCN.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Spizaetus_tyrannus": {  # BLHE — Black Hawk-Eagle — Águila tirana
        "distribution":
            "Selvas tropicales lluviosas y bosques montanos del sur de México (Veracruz, Oaxaca, "
            "Chiapas, Tabasco, Yucatán) hasta Argentina.",
        "diet":
            "Mamíferos arborícolas (kinkajous, monos pequeños), aves medianas (loros, oropéndolas), "
            "reptiles grandes.",
        "behavior":
            "Solitaria. Vuelos en círculos altos sobre el dosel acompañados de vocalizaciones "
            "fuertes y agudas. Hábitos esquivos pese a su tamaño.",
        "migration":
            "Sedentaria.",
        "iucn_status": "Least Concern (rara regionalmente)",
        "length_cm": "58-71 cm",
        "wingspan_cm": "120-149 cm",
        "diagnostic":
            "Plumaje completamente negro; tarsos plumosos con barreteado fino blanco; cresta "
            "corta. En vuelo: alas largas con punta digitada, cola larga con 3-4 bandas blancas. "
            "Patrón general parecido a un Buteogallus pero alas más largas y cola más larga.",
        "best_months": "Año redondo (selva alta)",
        "did_you_know":
            "Su vocalización fuerte y prolongada es uno de los sonidos icónicos de las selvas "
            "altas mexicanas en zonas como Calakmul y la selva Lacandona, donde a menudo se oye "
            "más fácilmente de lo que se ve.",
    },
}

# Verificación: deben coincidir las 53 con las de config.SPECIES
assert len(SPECIES_DETAILS) == 53, \
    f"Esperaba 53 especies en SPECIES_DETAILS, hay {len(SPECIES_DETAILS)}"
