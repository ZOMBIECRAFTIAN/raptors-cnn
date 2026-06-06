# Resumen Ejecutivo — raptors-cnn

> Hoja de una página para presentar el proyecto a tus compañeros, asesor o comité en menos de 3 minutos de lectura.

---

## 🎯 ¿Qué es este proyecto?

Un sistema de **inteligencia artificial** que identifica automáticamente las **53 especies de rapaces diurnas de México**, con énfasis en observaciones en vuelo, silueta y comportamiento. Incluye además un **catálogo de señas en International Sign** como entregable secundario de accesibilidad.

## 🧪 ¿Por qué importa?

- **México combina alta diversidad de rapaces y corredores migratorios clave**, incluido Veracruz River of Raptors, con más de 5 millones de individuos por temporada.
- **El monitoreo actual depende totalmente de expertos humanos**, con sesgo inter-observador y costo logístico alto.
- **Las personas sordas están sistemáticamente excluidas** del discurso ornitológico: no existen señas formalizadas para la mayoría de las rapaces.
- Este proyecto **atiende el problema técnico de identificación y abre una línea de inclusión científica**.

## 🛠️ ¿Cómo lo hacemos?

| Componente | Tecnología | Estado |
|------------|-----------|--------|
| Identificación visual | CNN (ResNet-50, EfficientNet-B3, MobileNetV3, ConvNeXt-Tiny) + transfer learning | ✅ Pipeline verificado |
| Comparativa | PyTorch principal + TensorFlow espejo | 🚧 En consolidación |
| Interpretabilidad | Grad-CAM | ✅ Funcionando |
| Video/comportamiento | YOLO detección/seguimiento + análisis de vuelo | 🚧 Siguiente módulo |
| Dataset | iNaturalist + Macaulay Library + eBird + CONABIO | 🚧 En curación y evaluación |
| Lengua de señas | Catálogo de 53 señas en International Sign | 🚧 Propuesta y validación pendiente |
| Validación inclusiva | Escala Likert con grupo focal sordo | 🚧 Pendiente |

## 📊 ¿Qué resultados esperamos?

- **H1**: reportar accuracy, F1 macro, top-3 accuracy, matriz de confusión y métricas por especie sobre las 53 clases.
- **H2**: Promedio Likert ≥ 4.0 / 5.0 en claridad, naturalidad y memorabilidad de cada seña.

## 🔍 Hallazgo destacado durante la verificación

Durante el smoke-test, **Grad-CAM detectó "shortcut learning"** — el modelo alcanzó 100 % accuracy aprendiendo a leer las etiquetas de texto burned-in, NO las formas geométricas que pretendían representar a las aves. Esto **valida empíricamente** la metodología de incluir interpretabilidad como criterio obligatorio: las métricas perfectas pueden estar engañando al investigador. Será una sección destacada del Capítulo 4.5 (Discusión).

## 🏗️ Estado actual del proyecto

```mermaid
gantt
    title Avance del proyecto
    dateFormat YYYY-MM
    section Investigación
    Estado del arte y bibliografía    :done, 2026-01, 2026-03
    Capítulos 1, 2, 3                 :done, 2026-03, 2026-05
    section Infraestructura
    Pipeline PyTorch + CUDA           :done, 2026-04, 2026-05
    Pipeline TensorFlow espejo        :active, 2026-05, 1M
    Modulo YOLO video/comportamiento  :2026-06, 2M
    section Dataset
    Descargador iNaturalist           :done, 2026-05, 1w
    Recolección real                  :2026-05, 2M
    Etiquetado doble-anotador         :2026-06, 1M
    section Modelo
    Evaluacion 53 clases              :2026-06, 1M
    Entrenamiento/comparativa completa :2026-07, 1M
    Comparativa de arquitecturas      :2026-08, 2w
    section Señas
    Catálogo IS preliminar            :done, 2026-04, 1w
    Validación con comunidad sorda    :2026-07, 1M
    Grabación de videos               :2026-08, 2w
    section Cierre
    Capítulos 4, 5 + entrega          :2026-09, 2M
```

## 🤝 ¿Cómo pueden ayudar mis compañeros?

- **Compañeros biólogos**: aportar fotografías propias, ayudar con la doble anotación y validar especies raras.
- **Compañeros de cómputo**: revisar el código, sugerir optimizaciones, ayudar con el frontend del prototipo.
- **Comunidad sorda y aliados**: participar en los talleres de co-creación y validación de señas.
- **Comité y asesor**: revisar capítulos, sugerir bibliografía, conectar con Pronatura.

## 📦 ¿Qué hay disponible hoy?

- 🌐 **Repositorio público**: `github.com/<usuario>/raptors-cnn`
- 📑 **Capítulos de tesis** conservados como material interno local
- 🧪 **Pipeline reproducible** verificado end-to-end con GPU NVIDIA
- 🎨 **Catálogo preliminar de señas** en `lengua_de_senas/catalogo_senas/`
- 📚 **Bibliografía consolidada** de 50+ referencias en APA 7.ª

---

**Contacto:** Brian Fernández Báez — brianferbaez@gmail.com
