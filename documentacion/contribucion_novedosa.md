# Contribución Novedosa — Justificación para Tesis de Maestría

> Este documento articula explícitamente el aporte original al campo, exigible en una tesis de Maestría. Sirve como insumo para el Capítulo 1.3 (Justificación), Capítulo 5.2 (Contribuciones) y la presentación a comité.

---

## 1. El estado del arte previo a esta tesis

| Sistema | Modalidad | Especies cubiertas | Componente accesible | Limitación principal |
|---------|-----------|---------------------|----------------------|-----------------------|
| **BirdNET** (Kahl et al., 2021) | Acústica (espectrogramas) | >6,000 globales | No | Las rapaces vocalizan poco durante migración → marginal para identificación visual en vuelo |
| **Wildlife Insights** (Ahumada et al., 2020) | Visión, cámaras trampa terrestres | Mamíferos + aves terrestres | No | No optimizado para vuelo en cielo abierto |
| **iNaturalist Vision** (Van Horn et al., 2018) | Visión, fotografías de usuarios | Todas las taxa | No | Fotos posadas o de alta calidad; mal desempeño en vuelo a distancia |
| **Pronatura Veracruz** (1991–presente) | Observación humana experta | Migratorias del corredor | No | No automatizable, alto costo logístico |
| **Boer et al., 2022** | CNN + YOLO sobre rapaces | Subconjunto Países Bajos | No | mAP 78%, otra región y otro catálogo taxonómico |
| **Khandelwal et al., 2022** | CNN para rapaces a nivel género | Género, no especie | No | Resolución taxonómica insuficiente |
| **Glosarios en señas científicas** (LSM astronomía, biología marina) | — | — | Sí, pero otros dominios | No existe para ornitología |

## 2. La brecha específica identificada

**Ningún sistema previo combina simultáneamente:**

1. **Resolución a nivel de especie** sobre las rapaces diurnas de México.
2. **Optimización para cielo abierto** con contraluz, distancia variable y plumajes intra-específicos.
3. **Catalogación inclusiva** mediante lengua de señas internacional (IS).
4. **Validación de interpretabilidad** explícita mediante Grad-CAM como criterio metodológico.
5. **Apertura completa** (código MIT, dataset documentado, pesos publicables al cierre) reutilizable en otros corredores.

## 3. La contribución original de esta tesis

### 3.1 Contribuciones científicas verificables

**C-S1.** Pipeline CNN especializado en identificación de las 53 rapaces diurnas de México, optimizado para observaciones en vuelo y evaluable con accuracy, F1 macro, top-3 accuracy, ROC-AUC, matriz de confusión 53×53 e intervalos de confianza.

**C-S2.** Comparativa empírica planeada entre cuatro arquitecturas (ResNet-50, EfficientNet-B3, MobileNetV3-Large, ConvNeXt-Tiny), con PyTorch como implementación principal y TensorFlow/Keras como espejo metodológico para reproducibilidad.

**C-S3.** Aplicación documentada de Grad-CAM como criterio metodológico explícito de validación del modelo, no solo como visualización post-hoc. La tesis aporta evidencia empírica del **descubrimiento de shortcut learning** en un dataset sintético (modelo aprendió a leer texto en lugar de formas), validando la necesidad de interpretabilidad como salvaguarda.

### 3.2 Contribuciones tecnológicas

**C-T1.** Pipeline modular reproducible (configuración centralizada, paths relativos, semillas fijas, environment.yml) transferible directamente a otros corredores migratorios (Eilat, Gibraltar, Batumi, Panamá) con cambio mínimo de configuración.

**C-T2.** Cliente eBird/iNaturalist con filtros de licencia abierta documentados, contribuyendo a la cultura de datasets reproducibles en ornitología computacional.

**C-T3.** Prototipo funcional con backend de inferencia y frontend accesible, demostrando viabilidad de despliegue en plataformas educativas o ciudadanas.

**C-T4.** Extensión planeada de video con YOLO para detección/seguimiento de aves y extracción de comportamiento de vuelo (planeo, flap-glide, hovering, kettle y stoop), separando el problema de localización temporal del problema de clasificación de especie.

### 3.3 Contribuciones sociales e interdisciplinares

**C-I1.** Catálogo formal propuesto de 53 señas en International Sign para rapaces diurnas de México. Catálogo creado mediante metodología de co-creación con la comunidad sorda (Kusters & De Meulder, 2019), con instrumento de validación cuantitativa (escala Likert sobre tres dimensiones).

**C-I2.** Metodología replicable de **diseño de señas científicas con la comunidad sorda**, documentada paso a paso, transferible a otros campos (mastofauna, herpetofauna, entomología, botánica) y otros corredores migratorios del mundo.

**C-I3.** Demostración empírica de cumplimiento de la Convención sobre los Derechos de las Personas con Discapacidad (ONU, 2006) artículos 9, 21 y 24, mediante un producto científico funcional, no únicamente declarativo.

## 4. Posicionamiento académico

Esta tesis se sitúa en la **intersección de tres campos**, todos consolidados pero rara vez integrados:

```
        Ornitología cuantitativa
                  ▲
                  │
                  │
   Visión ──────● Aporte ●────── Lingüística de
   computacional  novedoso       señas científica
        ▲                              ▲
        │      Diseño Universal        │
        └────── del Aprendizaje ──────┘
```

La novedad NO está en cada componente individual (cada uno tiene literatura abundante), sino en su **integración coherente** dentro de un único producto funcional y abierto, demostrablemente útil tanto para ciencia como para inclusión.

## 5. Plan de publicación (post-defensa)

| # | Revista candidata | Cuartil JCR | Componente del proyecto | Timing tentativo |
|---|-------------------|-------------|--------------------------|-------------------|
| 1 | **Ecological Informatics** (Elsevier, IF ≈ 4.6) | Q1 | Modelo CNN + comparativa de arquitecturas | T+3 meses post-defensa |
| 2 | **Journal of Raptor Research** (Raptor Research Foundation) | Q2 | Aplicación a rapaces mexicanas y monitoreo en vuelo | T+6 meses |
| 3 | **Sign Language Studies** (Gallaudet University Press) | Q1 lingüística | Metodología de co-creación de señas | T+9 meses |
| 4 | **Ardea** (Sociedad Holandesa Ornitológica) | Q2 | Comparativa global de corredores | T+12 meses |
| 5 | **Environmental Education Research** (Taylor & Francis) | Q1 educación | DUA/UDL aplicado a educación ambiental inclusiva | T+12 meses |

**Estrategia:** publicaciones diferenciadas por campo, mismo proyecto, audiencias distintas → maximiza impacto y construye reputación interdisciplinar.

## 6. Comparación con tesis previas en temas análogos

| Tesis previa | Año | Contribución | Diferencia con la presente |
|--------------|-----|--------------|----------------------------|
| Boer et al. (Países Bajos) | 2022 | Detección YOLO de rapaces europeas | Sin componente inclusivo, otra región geográfica |
| Khandelwal et al. (India) | 2022 | CNN a nivel género | Sin especie ni accesibilidad |
| Tesis LSM astronomía (López-Núñez) | 2018 | Glosario en LSM | Otro dominio (astronomía), no integra IA |
| Wildlife Insights (Cornell-CI) | 2020 | Cámaras trampa terrestres | No vuelo, no señas |

**Conclusión:** la tesis presente combina dimensiones que ninguna predecesora aborda simultáneamente, lo que justifica su carácter novedoso al nivel de Maestría.

---

*Documento elaborado para sustentar el carácter novedoso de la investigación.
Sirve como referencia para el Capítulo 1.3 (Justificación), el Capítulo 5.2 (Contribuciones) y la presentación pública.*
