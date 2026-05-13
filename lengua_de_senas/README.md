# Módulo de Lengua de Señas — International Sign para Aves Rapaces

Este módulo contiene el catálogo de señas en International Sign (IS) para las 14 especies objetivo del proyecto. Es el componente social del sistema y cumple con los principios del Diseño Universal para el Aprendizaje (CAST, 2018).

## Estructura

```
lengua_de_senas/
├── catalogo_senas/
│   ├── Catalogo_de_Senas_Propuesta_Brian.md   # Diseño preliminar del autor (14 especies + adicionales)
│   ├── lamina_1.jpg                           # (a digitalizar) lámina hand-drawn original
│   ├── lamina_2.jpg                           # (a digitalizar) lámina hand-drawn original
│   ├── ficha_<COD>.md                         # ficha por especie tras refinamiento
│   └── svg/                                   # vectorizaciones (a producir)
├── videos/
│   └── <COD>_<especie>.mp4                    # videos finales tras grabación
├── glosario_IS_LSM.md                         # tabla de equivalencias IS ↔ LSM ↔ ASL
└── instrumentos_validacion/
    └── cuestionario_likert.md                 # instrumento aplicado al grupo focal
```

## Especies cubiertas (14 + adicionales)

### Núcleo del modelo CNN (14 prioritarias)

`BW` Broad-winged Hawk · `SW` Swainson's Hawk · `TV` Turkey Vulture · `MK` Mississippi Kite · `SS` Sharp-shinned Hawk · `CH` Cooper's Hawk · `RT` Red-tailed Hawk · `RS` Red-shouldered Hawk · `ZT` Zone-tailed Hawk · `NH` Northern Harrier · `PG` Peregrine Falcon · `AK` American Kestrel · `OS` Osprey · `ML` Merlin

### Adicionales documentadas en las láminas (uso educativo, segunda iteración)

`SK` Swallow-tailed Kite · `HH` Harris's Hawk · `GH` Gray Hawk · `GE` Golden Eagle · `HK` Hook-billed Kite · `ST` Short-tailed Hawk · `NG` Northern Goshawk · `CA` Crested Caracara · `WK` White-tailed Kite

### Aves no rapaces documentadas (referencia didáctica)

`WI` White Ibis · `WS` Wood Stork · `PB` Pelícano Blanco

## Flujo de trabajo del módulo

1. **Documento de propuesta** → `catalogo_senas/Catalogo_de_Senas_Propuesta_Brian.md` (✅ creado).
2. **Digitalización de láminas** → escanear y guardar como `lamina_1.jpg` y `lamina_2.jpg` (≥ 300 dpi).
3. **Talleres de refinamiento** → con la comunidad sorda; producir una `ficha_<COD>.md` por especie con la versión final.
4. **Grabación de videos** → fondo blanco, iluminación uniforme, encuadre frontal.
5. **Validación** → aplicar cuestionario Likert al grupo focal; iterar señas que no superen el umbral 4.0.
6. **Vectorización** → producir SVG estáticos para impresos y la tesis.
7. **Integración con el modelo** → el prototipo (`codigo/`) consume el video correspondiente al código de especie devuelto por la CNN.

## Referencias clave

- Kusters, A., & De Meulder, M. (2019). Sign Language Studies and Deaf Studies in marine biology contexts. Sign Language Studies, 19(4).
- López-Núñez, J., Gallego-Pérez, M., & Solano-Galán, V. (2018). Glosario de astronomía en LSM.
- WFD (2019). Position paper on International Sign.
- CAST (2018). Universal Design for Learning Guidelines v2.2.
