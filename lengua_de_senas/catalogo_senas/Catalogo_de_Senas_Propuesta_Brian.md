# Catálogo de Señas — Propuesta Original del Autor

**Autor del diseño:** Brian Fernández Báez
**Fecha de captura:** mayo 2026
**Origen:** Dibujos a mano sobre papel — fotografías incorporadas al proyecto.
**Estado:** Diseño preliminar, base para iteración con la comunidad sorda.

---

## 1. Especies objetivo del modelo CNN (14 especies — prioridad principal)

Cada especie tiene asignado un código corto de dos letras que sirve tanto para anotación rápida en campo como para etiquetar archivos de video, capturas y referencias del modelo.

| # | Código | Nombre común | Nombre científico | Familia | Abundancia en el corredor (cualitativa) |
|---|--------|--------------|-------------------|---------|------------------------------------------|
| 1 | BW | Broad-winged Hawk | *Buteo platypterus* | Accipitridae | Extrema (la especie más abundante) |
| 2 | SW | Swainson's Hawk | *Buteo swainsoni* | Accipitridae | Muy alta |
| 3 | TV | Turkey Vulture | *Cathartes aura* | Cathartidae | Muy alta |
| 4 | MK | Mississippi Kite | *Ictinia mississippiensis* | Accipitridae | Alta |
| 5 | SS | Sharp-shinned Hawk | *Accipiter striatus* | Accipitridae | Media |
| 6 | CH | Cooper's Hawk | *Astur cooperii* | Accipitridae | Media |
| 7 | RT | Red-tailed Hawk | *Buteo jamaicensis* | Accipitridae | Media |
| 8 | RS | Red-shouldered Hawk | *Buteo lineatus* | Accipitridae | Baja-media |
| 9 | ZT | Zone-tailed Hawk | *Buteo albonotatus* | Accipitridae | Baja |
| 10 | NH | Northern Harrier | *Circus hudsonius* | Accipitridae | Baja-media |
| 11 | PG | Peregrine Falcon | *Falco peregrinus* | Falconidae | Baja |
| 12 | AK | American Kestrel | *Falco sparverius* | Falconidae | Media |
| 13 | OS | Osprey | *Pandion haliaetus* | Pandionidae | Baja-media |
| 14 | ML | Merlin | *Falco columbarius* | Falconidae | Baja |

> **Nota sobre desbalance de clases:** la abundancia varía mucho entre especies. Para el entrenamiento de la CNN se aplicará cross-entropy ponderada (w_i = N / (C · n_i)) y técnicas de oversampling sintético (mixup, CutMix) en las clases minoritarias.

---

## 2. Descripción de las señas propuestas (extraída de los dibujos del autor)

A continuación se documentan las señas dibujadas a mano en las dos láminas de referencia. Cada seña fue diseñada por Brian Fernández Báez sobre la base de la silueta y la dinámica de vuelo de cada especie. El catálogo será sometido a iteración y validación con la comunidad sorda según la metodología del Capítulo 3, sección 3.5.

### 2.1 Especies del modelo CNN (orden alfabético por código)

#### AK — American Kestrel (*Falco sparverius*)
Mano dominante con dedos cerrados imitando una garra pequeña sobre el dorso de la mano no dominante; movimiento corto que simula el vuelo cernido (hovering) característico de la especie.

#### BW — Broad-winged Hawk (*Buteo platypterus*)
Antebrazo y mano extendidos horizontalmente con la palma hacia abajo, dedos juntos, simulando el ala ancha y el planeo en kettle. Movimiento ligero arriba-abajo evocando el batir relajado de los kettles migratorios.

#### CH — Cooper's Hawk (*Astur cooperii*)
Mano abierta apuntando hacia arriba en posición vertical junto al rostro, con tres flechas que indican movimientos cortos (representando aleteos rápidos seguidos de planeos breves, característicos de los antiguos Accipiter — *cooperii* fue reclasificado al género *Astur* por la AOS en 2023, junto con *Accipiter gentilis*). Diferenciación con SS por el contexto: tamaño relativo mayor.

#### ML — Merlin (*Falco columbarius*)
Mano cerrada en puño compacto con un dedo apuntando hacia adelante, simulando el vuelo rápido y directo del halcón pequeño. Movimiento veloz horizontal.

#### MK — Mississippi Kite (*Ictinia mississippiensis*)
Mano abierta vertical junto al hombro con flechas indicando movimiento ascendente y descendente — representa el vuelo ágil y la captura aérea de insectos típica de la especie.

#### NH — Northern Harrier (*Circus hudsonius*)
Antebrazo extendido horizontalmente con la palma abierta hacia abajo y movimiento de barrido lateral — simula el vuelo bajo y planeador sobre pastizales con las alas en V poco marcada.

#### OS — Osprey (*Pandion haliaetus*)
Mano dominante en forma de garra cerrándose sobre la palma de la mano no dominante — simboliza el zambullido del águila pescadora capturando un pez con sus garras.

#### PG — Peregrine Falcon (*Falco peregrinus*)
Mano dominante con dedos juntos en posición vertical descendente rápida — simboliza el stoop (picado) característico del halcón peregrino, una de las imágenes más icónicas en ornitología.

#### RS — Red-shouldered Hawk (*Buteo lineatus*)
Mano dominante a la altura del hombro tocando suavemente la zona del hombro — referencia directa a la mancha rojiza del hombro del adulto.

#### RT — Red-tailed Hawk (*Buteo jamaicensis*)
Mano dominante extendida hacia atrás a la altura de la cadera con flecha indicando el movimiento — referencia directa a la cola roja, rasgo diagnóstico del adulto.

#### SS — Sharp-shinned Hawk (*Accipiter striatus*)
Dos dedos extendidos junto al rostro (similar a CH pero con tamaño/ubicación distinta) — simboliza los aleteos rápidos del Accipiter más pequeño.

#### SW — Swainson's Hawk (*Buteo swainsoni*)
Mano dominante con dedos juntos extendida horizontalmente y movimiento que sugiere las alas en V poco pronunciada del Swainson's en planeo.

#### TV — Turkey Vulture (*Cathartes aura*)
Dos dedos extendidos en V con la mano dominante — referencia directa al diédrico marcado (vuelo en V) más distintivo del Turkey Vulture.

#### ZT — Buteo albonotatus — Zone-tailed Hawk
Mano dominante con dedos en posición que simula el patrón bandeado de la cola del Zone-tailed, con flecha indicando movimiento. Esta especie imita en vuelo al Turkey Vulture, lo que se refleja en una seña que comparte un núcleo visual con TV pero con la modulación de la cola.

---

### 2.2 Especies adicionales con seña propuesta (no priorizadas en el modelo CNN inicial)

Estas especies aparecen en las láminas del autor pero no están en la lista inicial de 14 para el modelo de IA. Se conservan en el catálogo de señas para uso educativo y posible incorporación en una segunda iteración del modelo.

| Código | Nombre común | Nombre científico | Notas |
|--------|--------------|-------------------|-------|
| SK | Swallow-tailed Kite | *Elanoides forficatus* | Cola muy ahorquillada, seña con dos dedos en V invertida |
| HH | Harris's Hawk | *Parabuteo unicinctus* | Pose de la mano simulando el ala plegada lateralmente |
| GH | Gray Hawk | *Buteo plagiatus* (antes *B. nitidus*) | Antebrazo cruzando el pecho |
| GE | Golden Eagle | *Aquila chrysaetos* | Movimiento sobre la cabeza simulando porte imperial |
| HK | Hook-billed Kite | *Chondrohierax uncinatus* | Mano con dedos curvados representando el pico ganchudo |
| ST | Short-tailed Hawk | *Buteo brachyurus* | Mano corta cerca del pecho, cola corta sugerida |
| NG | Northern Goshawk | *Accipiter gentilis* | Mano abierta extendida lateralmente |
| SH | Swainson's Hawk juvenil | — | Variante juvenil de SW (clase morfológica diferente) |
| WK | Adult White-tailed Kite | *Elanus leucurus* | Mano vertical con movimiento de vuelo cernido |
| CA | Crested Caracara | *Caracara plancus* | Dedos cruzados representando la cresta |

### 2.3 Especies no rapaces incluidas en las láminas (referencia educativa)

Aves grandes asociadas a los humedales del corredor de Veracruz que el autor incluyó como complemento didáctico:

- **WI — White Ibis** (*Eudocimus albus*) — mano con dedos curvados simulando el pico decurvado
- **WS — Wood Stork** (*Mycteria americana*) — mano con dedos juntos imitando el pico largo recto
- **PB — Pelícano Blanco** (*Pelecanus erythrorhynchos*) — dos dedos en V imitando el pico abierto

---

## 3. Próximos pasos para el módulo de señas

1. **Digitalización formal:** vectorizar cada seña en formato SVG para incluirla en la tesis y en el prototipo (alternativa al video cuando se requiera estática).
2. **Grabación en video:** filmar cada seña bajo condiciones estandarizadas (fondo blanco, iluminación uniforme, encuadre frontal) — ver Capítulo 3, sección 3.5.2 etapa D.
3. **Iteración con la comunidad sorda:** presentar el catálogo en los talleres de co-creación. Algunas señas pueden requerir ajustes para mejorar iconicidad o compatibilidad con International Sign.
4. **Validación cuantitativa:** aplicar el cuestionario Likert (claridad, naturalidad, memorabilidad) — umbral de aceptación promedio ≥ 4.0 sobre 5.
5. **Comparación con LSM y otras lenguas de señas:** elaborar una tabla de equivalencias que documente, para cada especie, la seña propuesta en IS, su versión en LSM y eventuales referencias en ASL u otras.

---

## 4. Imágenes de referencia

Las dos láminas originales con las señas dibujadas a mano por el autor se conservan como referencia visual del proyecto. Se recomienda al autor:

- Escanear ambas láminas a una resolución mínima de 300 dpi y guardar los archivos como `lengua_de_senas/catalogo_senas/lamina_1.jpg` y `lamina_2.jpg`.
- Asegurar que el catálogo digital final incluya: foto del dibujo original, video de la seña realizada, descripción textual y enlace al sonido del nombre común (cuando aplique).

---

*Este documento es el primer entregable formal del módulo de lengua de señas y servirá como base para todas las iteraciones siguientes.*
