# Catálogo de Señas — Propuesta Original del Autor

**Autor del diseño:** Brian Fernández Báez
**Fecha de captura inicial:** mayo 2026 (14 especies)
**Última actualización:** mayo 2026 (expansión a 23 especies con AOS 2023)
**Origen:** Dibujos a mano sobre papel — fotografías en `lamina_1.jpg` y `lamina_2.jpg`.
**Estado:** Diseño preliminar, base para iteración con la comunidad sorda.

---

## 1. Especies objetivo del modelo CNN (23 especies — alcance VRR completo)

A cada especie se asigna un código de 2-3 letras útil tanto para anotación rápida en campo
como para etiquetar archivos de video, capturas y referencias del modelo.

| #  | Cód.| Nombre científico (AOS 2023) | Nombre común ES | Familia | Abundancia (cualitativa) |
|----|-----|-------------------------------|------------------|---------|---------------------------|
| 1  | AK  | *Falco sparverius*            | Halcón cernícalo americano | Falconidae | Media (residente + migrante) |
| 2  | BE  | *Haliaeetus leucocephalus*    | Águila calva | Accipitridae | Muy baja (registrada en Cardel) |
| 3  | BW  | *Buteo platypterus*           | Aguililla alas anchas | Accipitridae | Extrema (la dominante en pico migratorio) |
| 4  | CH  | *Astur cooperii* ⚠️           | Gavilán de Cooper | Accipitridae | Media |
| 5  | FH  | *Buteo regalis*               | Aguililla de Ferruginous | Accipitridae | Muy baja (juveniles raros) |
| 6  | GE  | *Aquila chrysaetos*           | Águila real | Accipitridae | Muy baja (zona centro) |
| 7  | GH  | *Buteo plagiatus* ⚠️          | Aguililla gris | Accipitridae | Baja-media |
| 8  | HK  | *Chondrohierax uncinatus*     | Milano picogarfio | Accipitridae | Baja (residente raro) |
| 9  | MK  | *Ictinia mississippiensis*    | Milano de Mississippi | Accipitridae | Alta |
| 10 | ML  | *Falco columbarius*           | Halcón esmerejón | Falconidae | Baja |
| 11 | NG  | *Astur atricapillus* ⚠️       | Gavilán azor norteño | Accipitridae | Muy baja (Chichicaxtle) |
| 12 | NH  | *Circus hudsonius*            | Gavilán rastrero | Accipitridae | Baja-media |
| 13 | OS  | *Pandion haliaetus*           | Águila pescadora | Pandionidae | Baja-media |
| 14 | PG  | *Falco peregrinus*            | Halcón peregrino | Falconidae | Baja |
| 15 | RL  | *Buteo lagopus*               | Aguililla patas ásperas | Accipitridae | Muy baja (cruce raro) |
| 16 | RS  | *Buteo lineatus*              | Aguililla pecho rojo | Accipitridae | Baja-media |
| 17 | RT  | *Buteo jamaicensis*           | Aguililla cola roja | Accipitridae | Media |
| 18 | SS  | *Accipiter striatus*          | Gavilán pecho rufo | Accipitridae | Media |
| 19 | STH | *Buteo brachyurus*            | Aguililla colicorta | Accipitridae | Baja (residente) |
| 20 | STK | *Elanoides forficatus*        | Milano tijereta | Accipitridae | Alta en pico migratorio |
| 21 | SW  | *Buteo swainsoni*             | Aguililla de Swainson | Accipitridae | Muy alta |
| 22 | TV  | *Cathartes aura*              | Zopilote aura | Cathartidae | Muy alta |
| 23 | ZT  | *Buteo albonotatus*           | Aguililla aura | Accipitridae | Baja |

> **Reclasificaciones AOS 2023** ⚠️:
> `Accipiter cooperii` → `Astur cooperii` · `Accipiter gentilis` → `Astur atricapillus` · `Buteo nitidus` → `Buteo plagiatus`

> **Nota sobre desbalance de clases:** la abundancia varía mucho entre especies (de "Extrema" a "Muy baja"). Para el entrenamiento de la CNN se aplica cross-entropy ponderada (w_i = N / (C · n_i)) y técnicas de oversampling sintético (mixup, CutMix) en las clases minoritarias.

---

## 2. Descripción de las señas propuestas

### 2.1 Especies originales V1 (14, con seña dibujada por el autor en las láminas)

#### AK — *Falco sparverius* — Halcón cernícalo americano
Mano cerrada como pequeña garra + movimiento de hovering (vuelo cernido). Tamaño pequeño se enfatiza con la mano cerrada y movimiento corto.

#### BW — *Buteo platypterus* — Aguililla alas anchas
Antebrazo y mano horizontales con palma hacia abajo, ligero arriba-abajo evocando el batir relajado del kettle migratorio. Es la seña "dominante" porque es la especie más numerosa.

#### CH — *Astur cooperii* — Gavilán de Cooper
Mano abierta apuntando hacia arriba en posición vertical junto al rostro, con tres flechas que indican movimientos cortos (aleteos rápidos + planeos breves típicos de los antiguos Accipiter — *cooperii* fue reclasificado al género *Astur* por la AOS en 2023, junto con *atricapillus*). Diferenciación con SS por contexto: tamaño mayor.

#### ML — *Falco columbarius* — Halcón esmerejón
Puño compacto con dedo apuntando adelante, movimiento veloz horizontal. Representa el vuelo rápido y directo del halcón pequeño.

#### MK — *Ictinia mississippiensis* — Milano de Mississippi
Mano abierta vertical junto al hombro con movimiento ascendente-descendente. Representa el vuelo ágil y la captura aérea de insectos.

#### NH — *Circus hudsonius* — Gavilán rastrero
Antebrazo horizontal palma abajo + barrido lateral. Simula el vuelo bajo y planeador sobre pastizales con las alas en V poco marcada.

#### OS — *Pandion haliaetus* — Águila pescadora
Mano dominante en forma de garra cerrándose sobre la palma de la mano no dominante. Simboliza el zambullido y captura del pez con las garras.

#### PG — *Falco peregrinus* — Halcón peregrino
Mano dominante con dedos juntos en posición vertical descendente rápida. Simboliza el stoop (picada vertical) característico.

#### RS — *Buteo lineatus* — Aguililla pecho rojo
Mano dominante a la altura del hombro tocando suavemente la zona del hombro. Referencia directa a la mancha rojiza del hombro del adulto.

#### RT — *Buteo jamaicensis* — Aguililla cola roja
Mano dominante extendida hacia atrás a la altura de la cadera con flecha indicando el movimiento. Referencia directa a la cola roja, rasgo diagnóstico del adulto.

#### SS — *Accipiter striatus* — Gavilán pecho rufo
Dos dedos extendidos junto al rostro (similar a CH pero con tamaño/ubicación distinta). Simboliza los aleteos rápidos del Accipiter más pequeño.

#### SW — *Buteo swainsoni* — Aguililla de Swainson
Mano dominante con dedos juntos extendida horizontalmente y movimiento que sugiere las alas en V poco pronunciada del Swainson's en planeo.

#### TV — *Cathartes aura* — Zopilote aura
Dos dedos extendidos en V con la mano dominante. Referencia directa al diédrico marcado (vuelo en V) más distintivo de la especie.

#### ZT — *Buteo albonotatus* — Aguililla aura
Mano dominante con dedos en posición que simula el patrón bandeado de la cola del Zone-tailed, con flecha indicando movimiento. Esta especie imita en vuelo al TV, así que la seña comparte un núcleo visual con TV pero con la modulación de la cola.

### 2.2 Especies nuevas V2 (9 — pendientes de diseño formal con la comunidad sorda)

Las siguientes 9 especies se agregaron en la expansión taxonómica. **Las propuestas aquí son preliminares del autor y deben validarse con la comunidad sorda en los talleres correspondientes.**

#### BE — *Haliaeetus leucocephalus* — Águila calva
**Propuesta:** ambas manos abiertas a la altura de la cabeza, una palma hacia el rostro para indicar la "cabeza blanca", segunda seña con índice y pulgar formando el pico amarillo curvado.
**Iconicidad:** muy alta — la cabeza blanca y el pico son el rasgo más diagnóstico universalmente reconocido.

#### FH — *Buteo regalis* — Aguililla de Ferruginous
**Propuesta:** seña base de Buteo (mano horizontal) + toque en el muslo/pierna para indicar "patas emplumadas" (rasgo ferruginous-lagopus) + amplitud grande del aleteo (es el Buteo más grande).
**Iconicidad:** media — diferenciada de RL por el contexto de tamaño.

#### GE — *Aquila chrysaetos* — Águila real
**Propuesta:** mano sobre la nuca con movimiento que sugiere "corona dorada", seguido de aleteo amplio y poderoso de ambas manos. Representa la nuca dorada característica + el porte de "águila majestuosa" cultural.
**Iconicidad:** muy alta — ave nacional, reconocible inmediatamente.

#### GH — *Buteo plagiatus* — Aguililla gris
**Propuesta:** seña base de Buteo + dedo trazando dos bandas horizontales en la cola (las dos bandas blancas anchas son diagnósticas).
**Iconicidad:** alta — las bandas de cola son el rasgo único.

#### HK — *Chondrohierax uncinatus* — Milano picogarfio
**Propuesta:** índice y pulgar formando un gancho frente al rostro, simulando el pico ganchudo característico que da nombre a la especie.
**Iconicidad:** muy alta — el pico es el rasgo único y diagnóstico.

#### NG — *Astur atricapillus* — Gavilán azor norteño
**Propuesta:** seña base de CH (Astur cooperii) + ceja blanca trazada sobre el ojo con índice. La ceja blanca marcada es el rasgo más diagnóstico del adulto.
**Iconicidad:** alta — la ceja es distintiva.

#### RL — *Buteo lagopus* — Aguililla patas ásperas
**Propuesta:** seña base de Buteo + toque rápido en el muslo/pierna (indica "patas emplumadas") + seña adicional de "hovering" (cernido), porque es el único Buteo que practica vuelo cernido regularmente.
**Iconicidad:** alta — combinación de patas + hovering es única.

#### STH — *Buteo brachyurus* — Aguililla colicorta
**Propuesta:** seña base de Buteo + mano que se "acorta" hacia adelante (movimiento de "ahorquillado corto") para indicar la cola corta característica.
**Iconicidad:** media-alta.

#### STK — *Elanoides forficatus* — Milano tijereta
**Propuesta:** dos dedos índice cruzándose como tijera con un movimiento ondulante elegante. Representa la cola profundamente ahorquillada y el vuelo "como golondrina gigante".
**Iconicidad:** muy alta — la cola ahorquillada es el rasgo único de la familia.

---

### 2.3 Especies adicionales con seña propuesta (no priorizadas en V1, en las láminas hand-drawn)

Estas especies aparecen en las láminas pero NO están en la lista oficial V1 de 23. Se conservan en el catálogo para uso educativo y futura expansión V2.

| Código | Nombre común | Nombre científico | Notas |
|--------|--------------|-------------------|-------|
| HH | Aguililla rojinegra | *Parabuteo unicinctus* | Harris's Hawk |
| SK | Caracolero | *Rostrhamus sociabilis* | Snail Kite |
| CA | Caracara quebrantahuesos | *Caracara plancus* | Crested Caracara |

### 2.4 Aves no rapaces incluidas en las láminas (referencia educativa)

Aves grandes asociadas a los humedales del corredor de Veracruz que el autor incluyó como complemento didáctico:

- **WI — Ibis blanco** (*Eudocimus albus*)
- **WS — Cigüeña americana** (*Mycteria americana*)
- **PB — Pelícano blanco** (*Pelecanus erythrorhynchos*)

---

## 3. Próximos pasos para el módulo de señas

1. **Digitalización formal:** vectorizar cada una de las 23 señas en formato SVG.
2. **Grabación en video** con miembro sordo nativo de IS: condiciones estandarizadas (fondo blanco, iluminación uniforme, encuadre frontal del torso y manos).
3. **Validación cuantitativa** con grupo focal según el protocolo de `documentacion/is_consultation/validation_protocol.md` (a crear): escala Likert ≥ 4.0 en claridad, naturalidad y memorabilidad.
4. **Diseño formal de las 9 nuevas señas** con la comunidad sorda: las propuestas en sección 2.2 son del autor solamente, no validadas.
5. **Comparación con LSM y otras lenguas de señas:** elaborar tabla de equivalencias.
6. **Para V2 (México completo):** diseñar señas para las ~26 especies adicionales.

---

## 4. Imágenes de referencia

Las dos láminas originales hand-drawn con las 14 señas iniciales se conservan en:

- `lengua_de_senas/catalogo_senas/lamina_1.jpg` (pendiente de escaneo)
- `lengua_de_senas/catalogo_senas/lamina_2.jpg` (pendiente de escaneo)

Se recomienda al autor:

- Escanear ambas láminas a ≥ 300 dpi.
- El catálogo digital final debe incluir, por especie: foto del dibujo original, video de la seña real, descripción textual, vectorización SVG y enlace al sonido del nombre común (cuando aplique).

---

*Este documento es el insumo formal del módulo de lengua de señas y sirve como base para la validación con la comunidad sorda.*
