# Lista oficial de rapaces diurnas de México (V1.1)

> **Documento maestro de especies del proyecto** *Sistema de Identificación de
> Aves Rapaces por Silueta y Comportamiento de Vuelo Utilizando IA y Diseño
> de Lenguaje de Señas para su Comunicación y Reconocimiento* (raptors-cnn).
> Reemplaza el alcance previo de "23 rapaces del corredor de Veracruz" por
> **todas las rapaces diurnas documentadas en México** (Cathartiformes,
> Accipitriformes y Falconiformes). Esta lista es la fuente de verdad para
> `codigo/pytorch/config.py`, `codigo/tensorflow/config.py`, `species_data.py`,
> el catálogo de señas, el README y la base de datos de imágenes.

**Versión:** 1.1 — 17 de mayo de 2026
**Autoridad taxonómica:** American Ornithological Society (AOS) — Check-list of
North and Middle American Birds, 64th supplement (2023) + 65th supplement (2024).
**Fuentes secundarias:** eBird/Clements 2024, IUCN Red List, CONABIO, NOM-059-SEMARNAT-2010.

---

## Resumen ejecutivo

| Familia | N° especies | Notas |
|---------|-------------|-------|
| Cathartidae | 4 | Zopilotes neárticos y neotropicales |
| Pandionidae | 1 | Águila pescadora |
| Accipitridae | 38 | Gavilanes, águilas y milanos |
| Falconidae | 10 | Halcones, caracaras y halcones selváticos |
| **TOTAL** | **53** | Suficientes para cubrir todo el territorio nacional |

---

## Tabla maestra (orden alfabético por nombre científico)

| # | Cód. | Nombre científico (AOS 2024) | Nombre común (ES) | Nombre común (EN) | Familia | Estatus MX | IUCN | NOM-059 |
|---|------|------------------------------|-------------------|-------------------|---------|------------|------|---------|
| 1 | SSHA | *Accipiter striatus* | Gavilán pajarero | Sharp-shinned Hawk | Accipitridae | Migratorio invernal | LC | — |
| 2 | GOEA | *Aquila chrysaetos* | Águila real | Golden Eagle | Accipitridae | Residente (montañas) | LC | A |
| 3 | NOGO | *Astur atricapillus* | Gavilán azor americano | American Goshawk | Accipitridae | Migratorio invernal raro | LC | A |
| 4 | COHA | *Astur cooperii* | Gavilán de Cooper | Cooper's Hawk | Accipitridae | Residente + migratorio | LC | Pr |
| 5 | BCHA | *Busarellus nigricollis* | Aguililla canela | Black-collared Hawk | Accipitridae | Residente tropical | LC | A |
| 6 | ZTHA | *Buteo albonotatus* | Aguililla aura | Zone-tailed Hawk | Accipitridae | Residente + migratorio | LC | Pr |
| 7 | STHA | *Buteo brachyurus* | Aguililla cola corta | Short-tailed Hawk | Accipitridae | Residente tropical | LC | Pr |
| 8 | RTHA | *Buteo jamaicensis* | Aguililla cola roja | Red-tailed Hawk | Accipitridae | Residente + migratorio | LC | — |
| 9 | RLHA | *Buteo lagopus* | Aguililla ártica | Rough-legged Hawk | Accipitridae | Migratorio invernal raro | LC | — |
| 10 | RSHA | *Buteo lineatus* | Aguililla pecho rojo | Red-shouldered Hawk | Accipitridae | Migratorio invernal | LC | — |
| 11 | GRHA | *Buteo plagiatus* | Aguililla gris | Gray Hawk | Accipitridae | Residente + migratorio parcial | LC | — |
| 12 | BWHA | *Buteo platypterus* | Aguililla ala ancha | Broad-winged Hawk | Accipitridae | Migración masiva | LC | Pr |
| 13 | FEHA | *Buteo regalis* | Aguililla real | Ferruginous Hawk | Accipitridae | Migratorio invernal | LC | A |
| 14 | SWHA | *Buteo swainsoni* | Aguililla de Swainson | Swainson's Hawk | Accipitridae | Migración masiva | LC | Pr |
| 15 | COBH | *Buteogallus anthracinus* | Aguililla negra menor | Common Black Hawk | Accipitridae | Residente | LC | Pr |
| 16 | SOEA | *Buteogallus solitarius* | Águila solitaria | Solitary Eagle | Accipitridae | Residente raro | NT | P |
| 17 | GBHA | *Buteogallus urubitinga* | Aguililla negra mayor | Great Black Hawk | Accipitridae | Residente tropical | LC | Pr |
| 18 | CRCA | *Caracara plancus* | Caracara quebrantahuesos | Crested Caracara | Falconidae | Residente | LC | — |
| 19 | TUVU | *Cathartes aura* | Zopilote aura | Turkey Vulture | Cathartidae | Residente + migratorio | LC | — |
| 20 | LYHV | *Cathartes burrovianus* | Zopilote sabanero | Lesser Yellow-headed Vulture | Cathartidae | Residente tropical | LC | Pr |
| 21 | HBKI | *Chondrohierax uncinatus* | Gavilán pico de gancho | Hook-billed Kite | Accipitridae | Residente tropical | LC | Pr |
| 22 | NOHA | *Circus hudsonius* | Aguilucho norteño | Northern Harrier | Accipitridae | Migratorio invernal | LC | — |
| 23 | BLVU | *Coragyps atratus* | Zopilote común | Black Vulture | Cathartidae | Residente | LC | — |
| 24 | RTCA | *Daptrius americanus* | Caracara comecacao | Red-throated Caracara | Falconidae | Residente raro tropical | LC | P |
| 25 | STKI | *Elanoides forficatus* | Milano tijereta | Swallow-tailed Kite | Accipitridae | Reproductor + migratorio | LC | Pr |
| 26 | WTKI | *Elanus leucurus* | Milano coliblanco | White-tailed Kite | Accipitridae | Residente | LC | — |
| 27 | MERL | *Falco columbarius* | Esmerejón | Merlin | Falconidae | Migratorio invernal | LC | — |
| 28 | OBFA | *Falco deiroleucus* | Halcón pechirrufo | Orange-breasted Falcon | Falconidae | Residente raro | NT | P |
| 29 | APFA | *Falco femoralis* | Halcón fajado | Aplomado Falcon | Falconidae | Residente | LC | A |
| 30 | PEFA | *Falco peregrinus* | Halcón peregrino | Peregrine Falcon | Falconidae | Residente + migratorio | LC | Pr |
| 31 | BAFA | *Falco rufigularis* | Halcón murcielaguero | Bat Falcon | Falconidae | Residente tropical | LC | — |
| 32 | AMKE | *Falco sparverius* | Cernícalo americano | American Kestrel | Falconidae | Residente + migratorio | LC | — |
| 33 | WTHA | *Geranoaetus albicaudatus* | Aguililla cola blanca | White-tailed Hawk | Accipitridae | Residente | LC | — |
| 34 | CRHA | *Geranospiza caerulescens* | Gavilán zancón | Crane Hawk | Accipitridae | Residente tropical | LC | — |
| 35 | BAEA | *Haliaeetus leucocephalus* | Águila calva | Bald Eagle | Accipitridae | Migratorio invernal raro | LC | P |
| 36 | DTKI | *Harpagus bidentatus* | Gavilán bidentado | Double-toothed Kite | Accipitridae | Residente tropical | LC | Pr |
| 37 | HAEA | *Harpia harpyja* | Águila arpía | Harpy Eagle | Accipitridae | Residente raro | VU | P |
| 38 | LAFA | *Herpetotheres cachinnans* | Halcón guaco | Laughing Falcon | Falconidae | Residente tropical | LC | — |
| 39 | MIKI | *Ictinia mississippiensis* | Milano de Mississippi | Mississippi Kite | Accipitridae | Migración pasajera | LC | Pr |
| 40 | PLKI | *Ictinia plumbea* | Milano plomizo | Plumbeous Kite | Accipitridae | Reproductor tropical | LC | Pr |
| 41 | GHKI | *Leptodon cayanensis* | Milano cabecigris | Gray-headed Kite | Accipitridae | Residente tropical | LC | Pr |
| 42 | BFFA | *Micrastur ruficollis* | Halcón selvático barrado | Barred Forest-Falcon | Falconidae | Residente tropical | LC | Pr |
| 43 | CFFA | *Micrastur semitorquatus* | Halcón selvático de collar | Collared Forest-Falcon | Falconidae | Residente tropical | LC | Pr |
| 44 | CREA | *Morphnus guianensis* | Águila monera | Crested Eagle | Accipitridae | Residente muy raro | NT | P |
| 45 | OSPR | *Pandion haliaetus* | Águila pescadora | Osprey | Pandionidae | Migratorio + residente parcial | LC | — |
| 46 | HASH | *Parabuteo unicinctus* | Aguililla rojinegra | Harris's Hawk | Accipitridae | Residente | LC | Pr |
| 47 | WHHA | *Pseudastur albicollis* | Aguililla blanca | White Hawk | Accipitridae | Residente tropical | LC | Pr |
| 48 | SNKI | *Rostrhamus sociabilis* | Caracolero común | Snail Kite | Accipitridae | Residente humedales | LC | Pr |
| 49 | ROHA | *Rupornis magnirostris* | Aguililla caminera | Roadside Hawk | Accipitridae | Residente | LC | — |
| 50 | KIVU | *Sarcoramphus papa* | Zopilote rey | King Vulture | Cathartidae | Residente raro tropical | LC | P |
| 51 | BAWE | *Spizaetus melanoleucus* | Águila blanquinegra | Black-and-white Hawk-Eagle | Accipitridae | Residente raro | LC | P |
| 52 | ORHE | *Spizaetus ornatus* | Águila elegante | Ornate Hawk-Eagle | Accipitridae | Residente raro | NT | P |
| 53 | BLHE | *Spizaetus tyrannus* | Águila tirana | Black Hawk-Eagle | Accipitridae | Residente raro | LC | P |

### Leyenda

- **Estatus MX:** *Residente* = anida en México todo el año. *Migratorio invernal* = visita México de octubre a marzo. *Migración pasajera* = atraviesa México sin pernoctar. *Residente raro* = poblaciones pequeñas y localizadas.
- **IUCN:** LC = Preocupación menor, NT = Casi amenazada, VU = Vulnerable, EN = En peligro.
- **NOM-059-SEMARNAT-2010:** Pr = Sujeta a protección especial, A = Amenazada, P = En peligro de extinción.

---

## Cambios respecto a V1 (23 especies del VRR)

### Especies que se mantienen (23)

Todas las especies de la V1 entran sin cambios al nuevo modelo. Solo cambia la
posición alfabética en `config.SPECIES` (el ordenamiento debe coincidir con
`torchvision.datasets.ImageFolder` que ordena alfabéticamente).

### Especies nuevas a incorporar (30)

```
Busarellus_nigricollis        DTKI  Double-toothed Kite (Harpagus bidentatus)
Buteogallus_anthracinus       BCHA  Black-collared Hawk
Buteogallus_solitarius        COBH  Common Black Hawk
Buteogallus_urubitinga        SOEA  Solitary Eagle
Caracara_plancus              GBHA  Great Black Hawk
Cathartes_burrovianus         CRCA  Crested Caracara
Coragyps_atratus              LYHV  Lesser Yellow-headed Vulture
Daptrius_americanus           BLVU  Black Vulture
Elanus_leucurus               RTCA  Red-throated Caracara
Falco_deiroleucus             WTKI  White-tailed Kite
Falco_femoralis               OBFA  Orange-breasted Falcon
Falco_rufigularis             APFA  Aplomado Falcon
Geranoaetus_albicaudatus      BAFA  Bat Falcon
Geranospiza_caerulescens      WTHA  White-tailed Hawk
Harpagus_bidentatus           CRHA  Crane Hawk
Harpia_harpyja                HAEA  Harpy Eagle
Herpetotheres_cachinnans      LAFA  Laughing Falcon
Ictinia_plumbea               PLKI  Plumbeous Kite
Leptodon_cayanensis           GHKI  Gray-headed Kite
Micrastur_ruficollis          BFFA  Barred Forest-Falcon
Micrastur_semitorquatus       CFFA  Collared Forest-Falcon
Morphnus_guianensis           CREA  Crested Eagle
Parabuteo_unicinctus          HASH  Harris's Hawk
Pseudastur_albicollis         WHHA  White Hawk
Rostrhamus_sociabilis         SNKI  Snail Kite
Rupornis_magnirostris         ROHA  Roadside Hawk
Sarcoramphus_papa             KIVU  King Vulture
Spizaetus_melanoleucus        BAWE  Black-and-white Hawk-Eagle
Spizaetus_ornatus             ORHE  Ornate Hawk-Eagle
Spizaetus_tyrannus            BLHE  Black Hawk-Eagle
```

### Reclasificaciones AOS aplicadas

- *Accipiter cooperii* → ***Astur cooperii*** (AOS 2023, 64th Supplement).
- *Accipiter gentilis* (poblaciones americanas) → ***Astur atricapillus*** (AOS 2023, 64th Supplement). Cambio de "Northern Goshawk" a "American Goshawk".
- *Buteo nitidus* → ***Buteo plagiatus*** (AOS 2012, validado AOS 2023).

---

## Criterios de inclusión

1. **Documentación verificada:** especie con registros publicados en eBird, Macaulay Library o CONABIO dentro del territorio mexicano (al menos 50 registros independientes).
2. **Diurnas:** se excluyen Strigiformes (búhos, lechuzas, tecolotes) — son tema de un proyecto hermano.
3. **Estatus actual:** se excluye *Gymnogyps californianus* (Cóndor de California) por estar extirpado de México desde el siglo XIX a pesar de su histórica presencia.
4. **Resolución visual razonable:** se excluyen vagrants accidentales con < 5 registros mexicanos (e.g. *Gampsonyx swainsonii*).

---

## Notas para el modelo

- **Desbalance esperado:** *Buteo jamaicensis*, *Cathartes aura* y *Coragyps atratus* tendrán
  > 1000 imágenes disponibles; *Morphnus guianensis*, *Harpia harpyja* y *Falco deiroleucus*
  apenas alcanzarán 50-100. Aplicar **`class_weight="balanced"`** y/o **focal loss**.
- **Confusiones predecibles:** *Buteogallus* spp. vs. *Buteo* spp. juveniles, *Spizaetus*
  spp. entre sí, *Astur* spp. vs. *Accipiter striatus*, *Cathartes aura* vs. *C. burrovianus*.
  Plan: matriz de confusión 53×53 + Grad-CAM en pares confusos.
- **Estratificación territorial:** especies tropicales (sur del Eje Neovolcánico) no aparecerán
  en imágenes del centro/norte. Incorporar **prior bayesiano por coordenadas** en futuras
  versiones del sistema.

---

## Referencias normativas

- **AOS Check-list of North and Middle American Birds** (64th Supp. 2023, 65th Supp. 2024).
- **eBird/Clements Checklist of the Birds of the World** v2024.
- **IUCN Red List of Threatened Species** (consultada mayo 2026).
- **CONABIO — Catálogo Taxonómico de Especies de México** (CAT).
- **NOM-059-SEMARNAT-2010** y modificaciones posteriores.
- **Howell & Webb (1995)**. *A Guide to the Birds of Mexico and Northern Central America*. Oxford University Press.
- **Berlanga et al. (2019)**. *Aves de México: Guía de Campo*. CONABIO.

---

*Documento creado: 2026-05-17. Autor: Brian Fernández Báez.
Sucede al alcance V1, que estaba limitado a 23 especies del corredor migratorio del VRR (Veracruz River of Raptors).*
