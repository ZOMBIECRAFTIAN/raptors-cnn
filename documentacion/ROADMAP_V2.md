# Roadmap V2 — De rapaces VRR a TODAS las rapaces de México + análisis multimodal de vuelo

> Documento que captura la **expansión del alcance del proyecto** decidida tras
> el cierre de la versión V1 (23 rapaces del corredor de Veracruz, identificación
> sobre imagen + GUI Flask). Para la **V2** del proyecto raptors-cnn (potencial
> tesis doctoral o continuación de Maestría) la visión cambia:

## 🎯 Visión V2

Pasar de:

- **V1:** identificar 23 rapaces migratorias del corredor de Veracruz a partir de **imágenes**.

a:

- **V2:** identificar **TODAS las rapaces de México** (aprox. 49 especies entre Accipitriformes y Falconiformes) a partir de **videos**, con módulo adicional de **análisis de vuelo y comportamiento** que enriquece la predicción y la valida ecológicamente.

---

## 1. Expansión taxonómica — de 23 → ~49 especies

### Especies de la V1 que ya están (23)

Las 23 ya implementadas se mantienen como núcleo. Cubren:

- Las 4 familias principales: Accipitridae, Falconidae, Cathartidae, Pandionidae.
- Migratorias dominantes del corredor del Golfo.
- Tres reclasificaciones AOS 2023 ya aplicadas (Astur, Buteo plagiatus).

### Especies nuevas a agregar (~26)

Todas las rapaces de México adicionales que deben incorporarse:

**Cathartidae (zopilotes y cóndores neárticos):**

- *Coragyps atratus* — Zopilote común (BV — Black Vulture)
- *Sarcoramphus papa* — Zopilote rey (KV — King Vulture, tropical)
- *Gymnogyps californianus* — Cóndor de California (CC — extirpado de México pero histórico)

**Pandionidae:** ya cubierto.

**Accipitridae (gavilanes, águilas, milanos residentes/raros):**

- *Rostrhamus sociabilis* — Caracolero común (SK — Snail Kite)
- *Harpagus bidentatus* — Milano dorsigris (DK — Double-toothed Kite)
- *Ictinia plumbea* — Milano plomizo (PK — Plumbeous Kite, tropical)
- *Geranospiza caerulescens* — Gavilán zancón (CR — Crane Hawk)
- *Heterospizias meridionalis* — Aguililla cienaguera (SH — Savanna Hawk)
- *Busarellus nigricollis* — Aguililla canela (BCH — Black-collared Hawk)
- *Pseudastur albicollis* — Aguililla blanca (WH — White Hawk, tropical)
- *Leucopternis semiplumbeus* — Aguililla dorsiplomiza (SPH — Semiplumbeous Hawk, raro)
- *Buteogallus anthracinus* — Aguililla negra menor (CBH — Common Black Hawk)
- *Buteogallus urubitinga* — Aguililla negra mayor (GBH — Great Black Hawk)
- *Buteogallus solitarius* — Águila solitaria (SE — Solitary Eagle)
- *Morphnus guianensis* — Águila monera (CHE — Crested Eagle, en peligro)
- *Harpia harpyja* — Águila arpía (HE — Harpy Eagle, en peligro crítico para México)
- *Spizaetus tyrannus* — Águila tirana (BHE — Black Hawk-Eagle)
- *Spizaetus ornatus* — Águila elegante (OHE — Ornate Hawk-Eagle)
- *Spizaetus melanoleucus* — Águila blanquinegra (BWHE — Black-and-white Hawk-Eagle)
- *Parabuteo unicinctus* — Aguililla rojinegra/Harris's (HH — Harris's Hawk)
- *Buteo nitidus* — Aguililla gris sudamericana (raro, complementa Buteo plagiatus)

**Falconidae adicional:**

- *Caracara plancus* — Caracara quebrantahuesos (CRC — Crested Caracara)
- *Daptrius americanus* — Caracara comecacao (RTC — Red-throated Caracara, tropical)
- *Ibycter americanus* — Caracara avispero (collared, históricamente listado)
- *Micrastur ruficollis* — Halcón selvático barrado (BFF — Barred Forest Falcon)
- *Micrastur semitorquatus* — Halcón selvático mayor (CFF — Collared Forest Falcon)
- *Falco rufigularis* — Halcón murcielaguero (BF — Bat Falcon)
- *Falco femoralis* — Halcón fajado (APF — Aplomado Falcon)
- *Falco deiroleucus* — Halcón pechirrufo (OBF — Orange-breasted Falcon, muy raro)

**Aproximadamente 26 nuevas, total V2 ≈ 49 especies** (la cifra final dependerá de la
revisión taxonómica AOS 2024-2026 y de los criterios de inclusión).

### Implicaciones técnicas

- `config.SPECIES` crece de 23 a ~49. **Re-entrenar todos los modelos.**
- Dataset objetivo: ≥ 200 imgs por especie → **~10,000 imágenes totales**.
- Validación cruzada estratificada se mantiene; matriz de confusión 49×49.
- Riesgo de fusión visual entre subadultos de *Buteogallus* y *Buteo* — análisis Grad-CAM crítico.

---

## 2. Cambio de medio — de imágenes a videos

El análisis principal en V2 se hace sobre **videos** en lugar de imágenes estáticas, porque:

- Los caracteres diagnósticos de vuelo (aleteo, planeo, formación) **requieren temporalidad**.
- Una imagen fija de un *Buteo* en kettle puede confundirse fácilmente; un video del mismo individuo planeando 5 segundos en térmica resuelve ambigüedad instantánea.
- Habilita análisis adicionales: comportamiento térmico, dinámica de aleteo.

### Pipeline V2 propuesto

```
Video de entrada (≤ 30 s)
        │
        ▼
┌──────────────────────────────────┐
│  Extracción de frames             │  Cada 0.5 s (60 frames para 30 s)
│  Tracker (DeepSORT / ByteTrack)   │  Sigue el individuo a través del clip
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│  Modelo de IDENTIFICACIÓN         │  CNN 2D sobre cada crop del individuo
│  (especie)                        │  Agregación temporal (vote / mean prob)
├──────────────────────────────────┤
│  Modelo de TIPO DE VUELO          │  CNN 3D o CNN+LSTM sobre la secuencia
│  (planeo/soaring/flap-glide/      │  Etiquetas: 4-5 clases de vuelo
│   hovering/stoop)                 │
├──────────────────────────────────┤
│  Modelo de FAMILIA                │  Coarse classifier (4 familias)
│  (Accipitridae / Falconidae /     │  Sirve como prior bayesiano
│   Cathartidae / Pandionidae)      │
├──────────────────────────────────┤
│  ANÁLISIS DE COMPORTAMIENTO       │  Métricas físicas extraídas:
│   - Frecuencia de aleteo (Hz)     │   · contar transiciones en silueta
│   - Tasa de ganancia altitud      │   · estimar con bounding box scale
│   - Formación si > 1 individuo    │   · clustering espacial (kettle/par/solo)
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│  ENRIQUECIMIENTO CONTEXTUAL       │
│  - Fecha (mes)                    │  Filtra especies probables por temporada
│  - Hora                            │  Filtra rapaces nocturnas (no aplica aquí, son diurnas)
│  - Altura del observador (GPS)    │  Filtra rapaces de zonas altas (Aquila chrysaetos
│  - Clima                          │   solo en > 1500m)
│  - Coordenadas                    │  Filtra especies según mapa de distribución MX
│  - Dirección migratoria           │  Confirma identidad si la dirección coincide con la
│                                    │   migración esperada (sur en otoño, norte en primavera)
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│  FUSIÓN BAYESIANA                 │  Combina las probabilidades de CNN + contexto:
│                                   │     P(esp | video, contexto)
│                                   │     ∝ P(esp | CNN) · P(contexto | esp)
└──────────────────────────────────┘
        │
        ▼
   Predicción final + intervalo de confianza
   + traza de razonamiento (qué evidencias subieron/bajaron cada especie)
```

### Ventajas

- **Multimodalidad** = mayor robustez. Una imagen única no es desambigua, un video con contexto sí.
- **Trazabilidad**: cada predicción incluye qué factor pesó más → defendible ante el comité.
- Se aproxima al razonamiento real de un ornitólogo experto.
- **Generalizable**: el mismo pipeline funciona para rapaces locales (no solo migratorias) o residentes.

---

## 3. Nuevos análisis a implementar

### 3.1 Tipo de vuelo (4-5 clases)

| Clase | Definición | Especies típicas |
|-------|------------|------------------|
| **Soaring** (planeo amplio) | Vuelo en térmica con muy poco aleteo | Cathartidae, Buteo, Pandionidae |
| **Flap-glide** | Aleteo intermitente entre planeos | Accipiter, Astur |
| **Hovering** (cernido) | Cernido estacionario sobre el suelo | Falco sparverius, Buteo lagopus |
| **Active flapping** | Aleteo constante | Migración activa, Falco peregrinus stoop |
| **Stoop** (picada vertical) | Picada > 200 km/h | Falco peregrinus, Aquila chrysaetos |

**Modelo sugerido**: 3D-CNN (ResNet3D-18) o CNN-LSTM sobre secuencias de 16 frames.
Alternativa más liviana: SlowFast con resolución reducida.

### 3.2 Familia (4 clases)

Coarse classifier que sirve como prior bayesiano. Reduce el espacio de búsqueda inicial:
si el modelo dice "es un Falconidae" con 95% de confianza, ya descartamos 35+ especies.

### 3.3 Patrón de aleteo

Análisis temporal de la silueta extraída por el tracker:

- **Frecuencia de aleteo (Hz):** transformada de Fourier sobre la variación de altura
  de la silueta. Distintivo entre especies pequeñas y grandes.
- **Profundidad del aleteo:** amplitud del movimiento. Buteo aletea poco, Accipiter mucho.
- **Ritmo (continuo vs intermitente):** flap-glide vs active flapping.

### 3.4 Comportamiento térmico

Métricas extraídas del movimiento del individuo:

- **Tasa de ganancia altitud (m/s):** estimable por el cambio de tamaño del bounding box.
- **Radio del círculo en térmica:** distintivo entre kettles (Buteo platypterus) vs
  individuos solitarios (Aquila chrysaetos).

### 3.5 Formación en vuelo

Cuando aparecen múltiples individuos:

- **Kettle** (> 5 individuos en espiral): típico de migración masiva.
- **Pareja**: territorial o reproductor.
- **Grupo familiar**: 2 adultos + juveniles.
- **Solitario**: la mayoría de rapaces fuera de migración.

---

## 4. Enriquecimiento contextual

| Variable | Cómo se usa |
|----------|-------------|
| **Fecha** | Cada especie tiene una "fenología" — meses esperados en México. Buteo platypterus solo es esperable en septiembre-octubre y abril, no en febrero. |
| **Hora del día** | Aves diurnas; descartamos predicciones imposibles (vuelo nocturno). Stooping de Falco peregrinus más típico al amanecer/atardecer. |
| **Altura observador (GPS)** | Aquila chrysaetos solo en > 1500 m. Buteo brachyurus prefiere < 1000 m. |
| **Clima** | Térmicas formadas con calor y humedad → afecta probabilidad de soaring. Día nublado = más probables aves activas (Falco), menos térmicas. |
| **Coordenadas** | Mapa de distribución por especie (IUCN, eBird, CONABIO). Harpia harpyja solo en selvas Lacandona y Calakmul. |
| **Dirección migratoria** | Sur en otoño (sept-nov), norte en primavera (mar-may). Confirma especie migratoria. |

### Implementación técnica

**Función `bayesian_refinement(cnn_probs, context)`** que combina:

```python
P(esp | video, context) ∝ P(esp | CNN) · P(date | esp) · P(location | esp) · P(altitude | esp) · ...
```

Cada `P(x | esp)` viene de los rangos documentados por especie (distribuciones de eBird/IUCN).

---

## 5. Cambios al stack tecnológico

| Componente | V1 | V2 |
|-----------|----|----|
| Modelo principal | CNN 2D (ResNet50) | CNN 3D (ResNet3D-18) + tracker + ensemble |
| Input | Imagen 224×224 | Video 16 frames × 224×224 |
| Tracker | — | DeepSORT / ByteTrack |
| Augmentation | spatial + color | + temporal (jittering en frames) |
| Cómputo en inferencia | ~50 ms / imagen | ~500-2000 ms / video |
| Dataset | 23 × 200 = 4,600 imgs | 49 × 100 videos = 4,900 videos (~500 GB) |
| Almacenamiento | ~5 GB | ~500 GB → necesidad de bucket cloud |
| Hardware entrenamiento | RTX 3050 4GB OK | **RTX 3060+** o cloud GPU obligatorio |

---

## 6. Implicaciones para la tesis

### A. Posible reescritura del título y objetivos

- **V1:** "Identificación de Aves Rapaces Migratorias del Corredor de Veracruz mediante IA y Lengua de Señas Internacional"
- **V2:** "Sistema multimodal de identificación de Falconiformes y Accipitriformes de México mediante visión computacional, análisis de vuelo y co-creación con la comunidad sorda"

### B. ¿Maestría o Doctorado?

V2 tiene la profundidad y novedad típicas de **tesis doctoral**. Opciones:

1. **Defender V1 como Maestría** (que está ya prácticamente lista) y luego usar V2 como propuesta de **doctorado**.
2. **Saltarse Maestría e ir directo a Doctorado** integrando V1 + V2 (requiere apoyo del comité).
3. **Maestría con V2 reducido** — implementar solo identificación de especie + tipo de vuelo, dejar resto como trabajo futuro.

**Recomendación:** **opción 1** — V1 te da el grado de Maestría rápido, V2 abre la puerta al doctorado.

### C. Plan de publicación enriquecido

Las contribuciones V2 generan al menos 3 papers adicionales sobre V1:

1. **CNN 3D para vuelo de rapaces** (revista: *Ecological Informatics* Q1)
2. **Pipeline multimodal con fusión bayesiana** (revista: *Methods in Ecology and Evolution* Q1)
3. **Patrones de aleteo cuantitativos por especie** (revista: *Journal of Raptor Research* Q2)

---

## 7. Cronograma sugerido V2

| Fase V2 | Estimación | Notas |
|---------|------------|-------|
| Curación dataset 49 especies | 3-4 meses | Macaulay Library + ALA + iNaturalist videos |
| Etiquetado de vuelos (4-5 clases) | 2 meses | Necesita ornitólogo + protocolo |
| Implementación CNN 3D + tracker | 2 meses | Adaptar de SlowFast (FAIR) |
| Entrenamiento real (cloud GPU) | 1-2 meses | A100 en Lambda Labs o AWS |
| Fusión bayesiana + contexto | 1 mes | Implementación + tuning |
| Evaluación y comparativa | 1 mes | vs. V1 baseline |
| Re-validación con comunidad sorda | 2 meses | Para señas de las 26 especies nuevas |
| Capítulos adicionales tesis | 2 meses | Si aplica a doctorado |
| **Total V2** | **~15 meses** | |

---

## 8. Estado actual y siguiente paso

- ✅ **V1 = Lista para defensa** (post-entrenamiento real del modelo).
- 📋 **V2 = Documentada en este roadmap**. Pendiente decisión de cuándo y cómo iniciarla.
- 📋 **Decisión de grado** (Maestría con V1 vs Doctorado con V1+V2): consulta con asesor.

**No hay urgencia de implementar V2 ya.** El propósito de este documento es:

1. **Capturar la visión** antes de que se pierda en chat.
2. **Justificar la profundidad** del proyecto si se decide expandir a doctorado.
3. **Dar dirección** a contribuciones futuras (estudiantes, voluntarios, etc.).

---

*Documento elaborado tras la conversación de mayo 2026.
Autor: Brian Fernández Báez. Estado: visión a futuro, V1 prioritaria.*
