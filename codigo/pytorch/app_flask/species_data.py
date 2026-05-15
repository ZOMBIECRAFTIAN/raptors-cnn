"""
raptors-cnn — Perfiles enriquecidos por especie (estilo Merlin Bird ID)

Adaptado de raptor_australia/gui/species_data.py para las 23 rapaces
del corredor migratorio de Veracruz (VRR).

Cada perfil sigue la misma forma para que la plantilla pueda renderizar
las 23 especies uniformemente.

Referencias consultadas:
  - Bildstein, K. L. (2006). Migrating raptors of the world. Cornell U. Press.
  - Howell, S. N. G. (2012). Raptors: Annual cycle, age determination, and migration.
  - Liguori, J. (2005, 2011). Hawks from every angle / Hawks at a distance.
  - Pronatura Veracruz (2020). Manual de rapaces migratorias del corredor de Veracruz.
  - IUCN Red List (2024).
  - AOS (2023). Check-list of North and Middle American Birds — 64th Supplement.
"""

SPECIES_DETAILS: dict[str, dict] = {

    # ──────────────────────────────────────────────────────────────────────
    "Accipiter_striatus": {  # SS — Sharp-shinned Hawk — Gavilán pecho rufo
        "distribution":
            "Reproductor en bosques boreales y templados de Norteamérica; "
            "migra al sur en otoño. En Veracruz pasa por el corredor de septiembre a noviembre.",
        "diet":
            "Aves pequeñas atrapadas en emboscadas rápidas en bosque; "
            "ocasionalmente murciélagos y grandes insectos.",
        "behavior":
            "Vuelo veloz con aleteos rápidos y planeos cortos. Solitario en migración. "
            "Difícil de distinguir del Gavilán de Cooper a distancia.",
        "migration":
            "Migrador completo. Pico en Veracruz: mediados de octubre a inicios de noviembre.",
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
    "Aquila_chrysaetos": {  # GE — Golden Eagle — Águila real
        "distribution":
            "Distribución holártica. En México, principalmente regiones montañosas. "
            "Registros raros pero validados en zona centro de Veracruz.",
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
        "best_months": "Diciembre-Febrero (registros invernales)",
        "did_you_know":
            "Ave nacional de México prehispánica y representada en la bandera. "
            "Pueden bajar en picada a más de 320 km/h al atacar presas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_atricapillus": {  # NG — Northern Goshawk — Gavilán azor norteño
        "distribution":
            "Bosques boreales y templados de Norteamérica. En Veracruz, observación "
            "muy rara — fotografiada en Chichicaxtle en migraciones excepcionales.",
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
            "junto con Cooper's Hawk, basado en estudios filogenómicos.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Astur_cooperii": {  # CH — Cooper's Hawk — Gavilán de Cooper
        "distribution":
            "Bosques caducifolios y mixtos de Norteamérica. Migra a México y "
            "Centroamérica en invierno. Común en migración por Veracruz.",
        "diet":
            "Aves medianas (palomas, mirlos, codornices) y pequeños mamíferos.",
        "behavior":
            "Similar a SS pero más grande y de vuelo más recto. "
            "Cazador de emboscada en bordes de bosque.",
        "migration":
            "Migrador completo. Pico en Veracruz: octubre-noviembre.",
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
    "Buteo_albonotatus": {  # ZT — Zone-tailed Hawk — Aguililla aura
        "distribution":
            "Suroeste de EE.UU., México, Centroamérica y norte de Sudamérica. "
            "En Veracruz es residente local en zonas boscosas.",
        "diet":
            "Reptiles, mamíferos pequeños y aves. Sorprende a sus presas imitando al Turkey Vulture.",
        "behavior":
            "Mimetismo agresivo: vuela en V poco marcada, casi idéntica al Turkey Vulture, "
            "para acercarse a presas que ignoran a los zopilotes.",
        "migration":
            "Parcialmente migrador. Algunas poblaciones sedentarias en Veracruz.",
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
    "Buteo_brachyurus": {  # STH — Short-tailed Hawk — Aguililla colicorta
        "distribution":
            "Florida sur, México y Centroamérica. En Veracruz residente en bosque tropical.",
        "diet":
            "Aves pequeñas atrapadas en vuelo, ocasionalmente mamíferos.",
        "behavior":
            "Caza desde altura — gira en círculos altos y se lanza en picada. "
            "Existe en dos morfos: claro y oscuro.",
        "migration":
            "Mayormente sedentaria con dispersión local.",
        "iucn_status": "Least Concern",
        "length_cm": "38-43 cm",
        "wingspan_cm": "82-103 cm",
        "diagnostic":
            "Cola corta para un Buteo. Morfo claro con pecho blanco; morfo oscuro completamente negro.",
        "best_months": "Año redondo (residente)",
        "did_you_know":
            "Una de las rapaces más pequeñas del género Buteo. Su técnica de caza por picada "
            "desde altura la diferencia del resto de Buteos del corredor.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_jamaicensis": {  # RT — Red-tailed Hawk — Aguililla cola roja
        "distribution":
            "Toda Norteamérica y norte de México. Migración parcial. "
            "Común en Veracruz tanto como residente como migrante invernal.",
        "diet":
            "Mamíferos pequeños (ratones, ardillas), reptiles y aves.",
        "behavior":
            "Cazadora generalista. Térmica amplia, planeo largo, caza desde percha.",
        "migration":
            "Parcialmente migradora. Pico migratorio en Veracruz: octubre-noviembre.",
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
    "Buteo_lagopus": {  # RL — Rough-legged Hawk — Aguililla patas ásperas
        "distribution":
            "Reproduce en tundra ártica. Migra al sur de EE.UU. y norte de México en invierno. "
            "Registrada cruzando el corredor de Cardel — muy rara para Veracruz.",
        "diet":
            "Mamíferos pequeños, especialmente lemmings en zona de cría; "
            "ratones de campo en zonas de invernada.",
        "behavior":
            "Único Buteo que practica vuelo cernido (hovering) regular. "
            "Caza desde el aire en zonas abiertas.",
        "migration":
            "Migrador completo. Llega al sur solo en inviernos extremos.",
        "iucn_status": "Least Concern",
        "length_cm": "46-60 cm",
        "wingspan_cm": "120-153 cm",
        "diagnostic":
            "Tarsos emplumados hasta los dedos (de ahí el nombre). "
            "Banda subterminal oscura en cola, parche oscuro en muñeca.",
        "best_months": "Diciembre-Febrero (irregular en Veracruz)",
        "did_you_know":
            "Es el único Buteo que rutinariamente practica vuelo cernido sin viento. "
            "Su distribución ártica lo hace una rapaz adaptada a temperaturas extremas.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_lineatus": {  # RS — Red-shouldered Hawk — Aguililla pecho rojo
        "distribution":
            "Bosques caducifolios húmedos de EE.UU. y noreste de México. "
            "En Veracruz observada en migración y como residente local.",
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
    "Buteo_plagiatus": {  # GH — Gray Hawk — Aguililla gris
        "distribution":
            "Bosques ribereños y selvas bajas del sur de EE.UU., México y Centroamérica. "
            "En Veracruz residente en bosque tropical caducifolio.",
        "diet":
            "Reptiles (especialmente iguanas), anfibios, mamíferos pequeños.",
        "behavior":
            "Caza desde percha y en planeo bajo. Vocaliza con un silbido descendente único.",
        "migration":
            "Sedentaria con dispersión local en Veracruz.",
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
    "Buteo_platypterus": {  # BW — Broad-winged Hawk — Aguililla alas anchas
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
    "Buteo_regalis": {  # FH — Ferruginous Hawk — Aguililla de Ferruginous
        "distribution":
            "Praderas y semidesiertos del oeste de Norteamérica. "
            "Registros juveniles en zonas altas aledañas al corredor (La Joya).",
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
        "best_months": "Noviembre-Febrero (juveniles raros)",
        "did_you_know":
            "Es el Buteo más grande de Norteamérica. Sus tarsos emplumados (como B. lagopus) "
            "son una adaptación al frío de las grandes planicies.",
    },

    # ──────────────────────────────────────────────────────────────────────
    "Buteo_swainsoni": {  # SW — Swainson's Hawk — Aguililla de Swainson
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
    "Cathartes_aura": {  # TV — Turkey Vulture — Zopilote aura
        "distribution":
            "Distribución amplia en América. Migración parcial. Muy común en Veracruz "
            "tanto residente como migrante.",
        "diet":
            "Carroña casi exclusivamente. Olfato extraordinario para detectar gases de descomposición.",
        "behavior":
            "Soaring constante en V marcada (diédrico). Balanceo lateral característico. "
            "Forma dormideros comunales.",
        "migration":
            "Migración parcial. Pico en Veracruz: octubre.",
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
    "Chondrohierax_uncinatus": {  # HK — Hook-billed Kite — Milano picogarfio
        "distribution":
            "Selvas tropicales de México a Argentina. "
            "En Veracruz residente raro en bosque tropical húmedo.",
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
    "Circus_hudsonius": {  # NH — Northern Harrier — Gavilán rastrero
        "distribution":
            "Reproduce en praderas y pantanos de Norteamérica. "
            "Migra al sur de EE.UU., México y Caribe. En Veracruz invernante.",
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
    "Elanoides_forficatus": {  # STK — Swallow-tailed Kite — Milano tijereta
        "distribution":
            "Sur de EE.UU., México, Centro y Sudamérica. "
            "En Veracruz reproductor y migratorio.",
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
    "Falco_columbarius": {  # ML — Merlin — Halcón esmerejón
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
    "Falco_peregrinus": {  # PG — Peregrine Falcon — Halcón peregrino
        "distribution":
            "Cosmopolita. Reproduce en acantilados y crecientes urbanos. "
            "En Veracruz invernante y residente local.",
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
    "Falco_sparverius": {  # AK — American Kestrel — Halcón cernícalo americano
        "distribution":
            "Amplia distribución en América. En Veracruz residente y migratorio.",
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
    "Haliaeetus_leucocephalus": {  # BE — Bald Eagle — Águila calva
        "distribution":
            "Toda Norteamérica, especialmente costas y grandes lagos. "
            "Registrada en Cardel — observación rara en Veracruz.",
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
    "Ictinia_mississippiensis": {  # MK — Mississippi Kite — Milano de Mississippi
        "distribution":
            "Sur central de EE.UU. Migra a Sudamérica. "
            "Pico migratorio fuerte en Veracruz.",
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
    "Pandion_haliaetus": {  # OS — Osprey — Águila pescadora
        "distribution":
            "Cosmopolita. En Veracruz invernante a lo largo de la costa y ríos.",
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
}

# Verificación: deben coincidir las 23 con las de config.SPECIES
assert len(SPECIES_DETAILS) == 23, f"Esperaba 23 especies, hay {len(SPECIES_DETAILS)}"
