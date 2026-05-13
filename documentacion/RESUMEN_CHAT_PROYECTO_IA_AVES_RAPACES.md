# Resumen del Chat: Proyecto de IA para Identificación de Aves Rapaces con Lenguaje de Señas Internacional

**Fuente:** Chat de Claude.ai (`https://claude.ai/chat/8113d34b-5ed1-4676-a59f-a56a04072748`)
**Fechas:** 15-16 de abril de 2026
**Proyecto:** Identificación de Aves Rapaces Migratorias mediante Inteligencia Artificial y Diseño de Lenguaje de Señas para su Comunicación y Reconocimiento
**Autor:** Brian Fernández Báez

---

## 1. Solicitud Inicial del Usuario

Brian planteó que quiere llevar a cabo el proyecto **paso a paso, desde cero**, comenzando con la investigación teórica y luego con la parte práctica. Para el lenguaje de señas pidió explorar la posibilidad de un **lenguaje internacional** (International Sign) para que el sistema pueda ser utilizado en todo el mundo. Después seguiría la programación de la IA para la identificación de aves rapaces. Solicitó ir tema por tema con la guía de Claude actuando como su asesor de tesis.

---

## 2. Mapa General del Proyecto

Claude propuso un proyecto estructurado por fases. La conversación detalló específicamente la Fase 1 y comenzó con la redacción formal de los Capítulos 1 y 2 de la tesis.

---

## 3. FASE 1 — Investigación Teórica y Bibliográfica

Esta fase es el cimiento científico del proyecto. Sin ella, el modelo de IA no tiene justificación y el lenguaje de señas no tiene base. Consta de 4 tareas concretas.

### Tarea 1.1 — Construir la Base Bibliográfica Científica

Mínimo **30 referencias sólidas** divididas en 4 bloques temáticos.

#### Bloque A — Migración de Aves Rapaces (especialmente Veracruz)

Bases de datos sugeridas:

- Google Scholar (`scholar.google.com`)
- JSTOR (`jstor.org`)
- Scielo (`scielo.org`) — publicaciones latinoamericanas
- BioOne (`bioone.org`)

Términos de búsqueda:

- "raptor migration" Veracruz
- "Río de Rapaces" Chichicaxtle
- Buteo platypterus migration
- corridor hawk count methodology

Referencias de arranque obligatorias:

| Autor | Año | Obra | Por qué la necesitas |
|---|---|---|---|
| Bildstein, K.L. | 2006 | Migrating Raptors of the World | Base ecológica fundamental |
| Zalles & Bildstein | 2000 | Raptor Watch | Rutas migratorias globales |
| Pronatura Veracruz | 2020 | Manual de Rapaces Migratorias | Datos locales de Chichicaxtle |
| Newton, I. | 2010 | The Migration Ecology of Birds | Marco teórico de migración |

#### Bloque B — Inteligencia Artificial y Visión Computacional

Bases de datos sugeridas:

- arXiv.org (preprints gratuitos de IA)
- Papers With Code (`paperswithcode.com`)
- Semantic Scholar (`semanticscholar.org`)

Términos de búsqueda:

- convolutional neural network bird classification
- species identification deep learning
- transfer learning wildlife monitoring
- YOLOv8 bird detection

Referencias obligatorias:

| Autor | Año | Obra |
|---|---|---|
| Krizhevsky, Sutskever & Hinton | 2012 | ImageNet Classification with Deep CNNs (artículo fundacional de las CNN) |
| He et al. | 2016 | Deep Residual Learning (ResNet) — modelo candidato a usar |
| Goodfellow, Bengio & Courville | 2016 | Deep Learning (MIT Press, libre en deeplearningbook.org) |
| Kahl et al. | 2021 | BirdNET: A deep learning solution for bird sound identification |

#### Bloque C — Lengua de Señas e Inclusión Científica

Bases de datos sugeridas:

- ERIC (`eric.ed.gov`) — educación
- PubMed — salud y comunicación
- UNESCO — publicaciones de accesibilidad

Términos de búsqueda:

- sign language science education
- deaf community environmental education
- International Sign Language biodiversity
- Lengua de Señas Mexicana ciencia

Referencias de arranque:

| Fuente | Documento |
|---|---|
| UNESCO (2020) | Hacia una ciencia más inclusiva: barreras y oportunidades para personas con discapacidad |
| WFD (World Federation of the Deaf) | Documentos sobre International Sign (IS) |
| Ramírez & López (2019) | Accesibilidad e inclusión en educación ambiental: LSM |

#### Bloque D — Ciencia Ciudadana y Conservación Participativa

Términos de búsqueda:

- citizen science bird monitoring
- participatory conservation technology
- iNaturalist eBird methodology

### Tarea 1.2 — Crear Ficha Bibliográfica por Cada Referencia

Plantilla de ficha:

```
FICHA BIBLIOGRÁFICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autor(es):
Año:
Título:
Revista / Editorial:
DOI o URL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Idea principal (1-2 oraciones):
Dato o hallazgo clave para mi proyecto:
Cita textual relevante (con número de página):
Cómo se conecta con mi hipótesis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Herramienta recomendada: **Zotero** (`zotero.org`) — gratuito, organiza referencias automáticamente en formato APA o Chicago.

### Tarea 1.3 — Redactar el Estado del Arte

Documento más importante de la Fase 1. Debe responder 4 preguntas científicamente:

1. **¿Qué se sabe sobre la migración de rapaces en el corredor del Golfo de México?** Citar a Bildstein (2006), Pronatura (2020), Newton (2010). Dato clave: más de 5 millones de individuos por temporada en Veracruz (Pronatura, 2020).
2. **¿Qué sistemas de IA existen ya para identificar aves?** BirdNET (Cornell Lab, acústico), Wildlife Insights (cámaras trampa), iNaturalist (visión). Brecha: ninguno está optimizado para rapaces en vuelo en cielos abiertos.
3. **¿Qué existe sobre lengua de señas en ciencias ambientales?** Glosarios de astronomía y biología marina existen; ausencia de uno para aves. Justificar International Sign (IS) sobre LSM por alcance global.
4. **¿Por qué tu proyecto llena un vacío real?** Nadie ha combinado CNN para rapaces en vuelo + señas ambientales internacionales + plataforma accesible.

### Tarea 1.4 — Definir Variables de Investigación

- **Variable independiente principal:** conjunto de datos de entrenamiento (imágenes de rapaces etiquetadas por especie, ángulo y condición atmosférica).
- **Variable dependiente principal:** precisión de identificación del modelo CNN (accuracy, recall, F1-score).
- **Variables de control:**
  - Resolución mínima ≥ 640px
  - Mínimo de imágenes por especie ≥ 200
  - Condiciones de iluminación documentadas
- **Variable del componente social:** nivel de aceptación de las señas diseñadas (escala Likert 1-5 en claridad, naturalidad y memorabilidad).

### Entregables de la Fase 1

1. Carpeta Zotero con mínimo 30 referencias organizadas por bloque temático.
2. Fichas bibliográficas de cada referencia (Word o Notion).
3. Documento de Estado del Arte — mínimo 8 páginas, citas en APA 7.ª edición.
4. Tabla de Variables formalizada.
5. Borrador del Planteamiento del Problema refinado.

### Advertencia del Asesor

Fortalecer la **justificación de International Sign (IS) sobre LSM**. Construir el argumento con literatura de la World Federation of the Deaf y estudios de IS — esto es lo que hace al proyecto verdaderamente global.

### Plan de Acción Inmediato

1. Instalar Zotero (5 min).
2. Buscar en Google Scholar: `"raptor migration" "Veracruz" -site:wikipedia.org` — descargar 5 artículos con acceso abierto.
3. Buscar en arXiv.org: `bird species identification convolutional neural network` — guardar los 3 más citados.
4. Llenar la primera ficha bibliográfica.

---

## 4. Capítulo 1 — Generado en el Chat

Claude generó el archivo **`Capitulo1 tesis brian.docx`** con 8 secciones:

- **1.1 Antecedentes** — contexto global de la migración de rapaces, Veracruz como sitio de mayor volumen mundial (>5 millones de individuos), estado de la IA en conservación, brecha de inclusión para personas sordas. Cada afirmación con su cita.
- **1.2 Planteamiento del Problema** — tres problemas estructurales: (1) dependencia del experto, (2) ausencia de automatización, (3) exclusión de comunidades sordas. Tres preguntas de investigación verificables.
- **1.3 Justificación** — cuatro dimensiones: científica-ecológica, tecnológica, social-inclusiva y ética.
- **1.4 Objetivos** — 1 objetivo general + 6 específicos numerados (OE1 a OE6) con verbos de acción verificables.
- **1.5 Alcances y Limitaciones** — categorías etiquetadas (taxonómica, lingüística, dataset, etc.).
- **1.6 Hipótesis** — hipótesis principal + hipótesis complementaria del componente social + tabla de variables con indicadores y umbrales cuantificables.
- **1.7 Comparativa Internacional** — tabla con 5 corredores mundiales, datos de individuos por temporada con citas reales.
- **1.8 Comparación de Métodos** — tabla justificando científicamente CNN vs. observación directa, bioacústica y radar.
- **Referencias** — 18 citas en APA 7.ª edición, todas reales y verificables.

---

## 5. Capítulo 2 — Marco Teórico — Generado en el Chat

Claude generó el archivo **`Capitulo2 tesis brian.docx`** con 10 secciones:

- **2.1 Aves Rapaces Migratorias del Golfo de México** — taxonomía formal de Accipitriformes y Falconiformes; corredor como embudo biogeográfico; Tabla 2.1 con 7 especies objetivo, caracteres diagnósticos de silueta, tipo de vuelo y abundancia documentada.
- **2.2 Identificación Visual en Vuelo** — 4 caracteres morfológicos diagnósticos (forma del ala, cola, aspect ratio, dinámica de vuelo); 5 factores que dificultan la identificación (variación de plumaje, contraluz, distancia, densidad migratoria, condiciones atmosféricas).
- **2.3 Redes Neuronales y Visión Computacional** — base biológica (Hubel & Wiesel, 1959); Tabla 2.2 con 7 componentes arquitecturales de una CNN; proceso completo de entrenamiento (forward pass, función de pérdida, retropropagación con fórmulas); Tabla 2.3 comparando 4 arquitecturas: ResNet-50, EfficientNet-B3, MobileNetV3 y ConvNeXt-Tiny.
- **2.4 Aplicaciones de IA en Conservación** — análisis de BirdNET, Wildlife Insights, antecedentes directos de CNN para rapaces en vuelo (Boer et al., 2022; Khandelwal et al., 2022); 6 técnicas de data augmentation justificadas para el contexto.
- **2.5 Accesibilidad y Ciencia Inclusiva** — fundamento legal con la CDPD de la ONU; datos de OMS e INEGI sobre discapacidad auditiva; LSM y sus vacíos léxicos; 3 argumentos técnicos a favor de International Sign.
- **2.6 Casos de Estudio Similares** — BirdNET, Wildlife Insights, Pronatura Veracruz, proyectos de señas científicas con lecciones concretas.
- **2.7 Historia del Monitoreo en Veracruz** — desde 1991 con Ernesto Ruelas Inzunza, establecimiento de Chichicaxtle; el proyecto como modernización tecnológica de ese legado.
- **2.8 Comparación de Métodos** — Tabla 2.4: 6 métodos en 5 criterios con datos cuantitativos, conclusión a favor de CNN.
- **2.9 Detalles Técnicos Avanzados** — pipeline completo de 6 etapas; Grad-CAM para interpretabilidad; función de pérdida ponderada para clases desbalanceadas.
- **2.10 Barreras Educativas para Personas Sordas** — vacío léxico en LSM; barreras metodológicas de campo; diseño del módulo de señas basado en DUA/UDL de CAST con ejemplos para *Cathartes aura* y *Buteo platypterus*.
- **Referencias** — 54 citas reales en APA 7.ª edición.

---

## 6. Archivos Adjuntos al Proyecto en Claude.ai

El proyecto en Claude.ai tiene cargados los siguientes documentos de contexto:

- `Tesis_Australia_Raptors_CNN_AUSLAN.docx` — 956 líneas
- `Tesis Biologia.docx` — 2,766 líneas
- `TP-09.pdf` — 4,298 líneas

---

## 7. Próximos Pasos Sugeridos

Según el último mensaje de Claude en el chat, el siguiente paso es el **Capítulo 3: Metodología**, que detallará el plan de trabajo práctico paso a paso.

Antes de avanzar al Capítulo 3, el chat dejó pendiente:

1. Confirmar si los Capítulos 1 y 2 generados como `.docx` están disponibles en este workspace o si hay que regenerarlos.
2. Decidir si se profundiza en la Fase 1 (búsqueda bibliográfica práctica con Zotero) antes de continuar con la metodología.
3. Definir formalmente la elección entre LSM e International Sign con la literatura de respaldo.

---

## Citas y Fuentes

- Chat original en Claude.ai: `https://claude.ai/chat/8113d34b-5ed1-4676-a59f-a56a04072748`
