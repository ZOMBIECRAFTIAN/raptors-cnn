# Módulo de Lengua de Señas — International Sign para Aves Rapaces de México

> Parte del proyecto: **Sistema de Identificación de Aves Rapaces por Silueta y Comportamiento de Vuelo Utilizando IA y Diseño de Lenguaje de Señas para su Comunicación y Reconocimiento**.

Este módulo contiene el catálogo de señas en **International Sign (IS)** para las **53 especies de rapaces diurnas de México** objetivo del proyecto. Es el componente social del sistema, complementa al módulo de visión (silueta + análisis de vuelo) y cumple con los principios del Diseño Universal para el Aprendizaje (CAST, 2018).

> **V1.1 (mayo 2026):** alcance ampliado de las 23 rapaces migratorias del corredor de Veracruz (V1) a las **53 rapaces nacionales** documentadas por AOS 2024. Las 23 originales mantienen sus señas; las **30 nuevas** están en fase de diseño y validación con la comunidad sorda. Ver `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md` para la lista taxonómica completa.

## Estructura

```
lengua_de_senas/
├── catalogo_senas/
│   ├── Catalogo_de_Senas_Propuesta_Brian.md   # Diseño preliminar del autor (53 especies)
│   ├── lamina_1.jpg                           # (a digitalizar) lámina hand-drawn original
│   ├── lamina_2.jpg                           # (a digitalizar) lámina hand-drawn original
│   ├── lamina_3.jpg                           # (a producir) lámina con especies tropicales
│   ├── ficha_<COD>.md                         # ficha por especie tras refinamiento
│   └── svg/                                   # vectorizaciones (a producir)
├── videos/
│   └── <COD>_<especie>.mp4                    # videos finales tras grabación
├── glosario_IS_LSM.md                         # tabla de equivalencias IS ↔ LSM ↔ ASL (53 entradas)
└── instrumentos_validacion/
    └── cuestionario_likert.md                 # instrumento aplicado al grupo focal
```

## Especies cubiertas (53)

### Cathartidae (4)
`BLVU` Black Vulture · `TUVU` Turkey Vulture · `LYHV` Lesser Yellow-headed Vulture · `KIVU` King Vulture

### Pandionidae (1)
`OSPR` Osprey

### Accipitridae — milanos y gavilanes pequeños (10)
`STKI` Swallow-tailed Kite · `WTKI` White-tailed Kite · `SNKI` Snail Kite · `DTKI` Double-toothed Kite · `MIKI` Mississippi Kite · `PLKI` Plumbeous Kite · `GHKI` Gray-headed Kite · `HBKI` Hook-billed Kite · `SSHA` Sharp-shinned Hawk · `COHA` Cooper's Hawk

### Accipitridae — Astur, Circus, Geranospiza, Rupornis (4)
`NOGO` American Goshawk · `NOHA` Northern Harrier · `CRHA` Crane Hawk · `ROHA` Roadside Hawk

### Accipitridae — Buteo / Geranoaetus / Pseudastur / Parabuteo (12)
`BWHA` Broad-winged Hawk · `SWHA` Swainson's Hawk · `RTHA` Red-tailed Hawk · `RSHA` Red-shouldered Hawk · `ZTHA` Zone-tailed Hawk · `STHA` Short-tailed Hawk · `GRHA` Gray Hawk · `FEHA` Ferruginous Hawk · `RLHA` Rough-legged Hawk · `WTHA` White-tailed Hawk · `WHHA` White Hawk · `HASH` Harris's Hawk

### Accipitridae — Buteogallus / Busarellus (4)
`COBH` Common Black Hawk · `GBHA` Great Black Hawk · `SOEA` Solitary Eagle · `BCHA` Black-collared Hawk

### Accipitridae — Águilas grandes (6)
`GOEA` Golden Eagle · `BAEA` Bald Eagle · `HAEA` Harpy Eagle · `CREA` Crested Eagle · `ORHE` Ornate Hawk-Eagle · `BLHE` Black Hawk-Eagle · `BAWE` Black-and-white Hawk-Eagle

### Falconidae (10)
`AMKE` American Kestrel · `MERL` Merlin · `PEFA` Peregrine Falcon · `APFA` Aplomado Falcon · `BAFA` Bat Falcon · `OBFA` Orange-breasted Falcon · `LAFA` Laughing Falcon · `BFFA` Barred Forest-Falcon · `CFFA` Collared Forest-Falcon · `CRCA` Crested Caracara · `RTCA` Red-throated Caracara

## Flujo de trabajo del módulo

1. **Documento de propuesta** → `catalogo_senas/Catalogo_de_Senas_Propuesta_Brian.md` (✅ versión V1.1 con 53 especies).
2. **Digitalización de láminas** → escanear las 2 originales V1 (23 especies) y producir una tercera para las 30 nuevas.
3. **Talleres de refinamiento** → con la comunidad sorda; producir una `ficha_<COD>.md` por especie con la versión final.
4. **Grabación de videos** → fondo blanco, iluminación uniforme, encuadre frontal.
5. **Validación** → aplicar cuestionario Likert al grupo focal; iterar señas que no superen el umbral 4.0.
6. **Vectorización** → producir SVG estáticos para impresos y la tesis.
7. **Integración con el modelo** → el prototipo Flask consume el video/SVG correspondiente al código de especie devuelto por la CNN.

## Referencias clave

- Kusters, A., & De Meulder, M. (2019). Sign Language Studies and Deaf Studies. Sign Language Studies, 19(4).
- López-Núñez, J., Gallego-Pérez, M., & Solano-Galán, V. (2018). Glosario de astronomía en LSM.
- WFD (2019). Position paper on International Sign.
- CAST (2018). Universal Design for Learning Guidelines v2.2.
- Berlanga et al. (2019). Aves de México: Guía de Campo. CONABIO.
- Howell, S. N. G., & Webb, S. (1995). A Guide to the Birds of Mexico. Oxford UP.
