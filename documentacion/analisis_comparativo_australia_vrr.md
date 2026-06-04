# Análisis Comparativo: raptor_australia ↔ raptors-cnn (VRR)

> Reporte de revisión del proyecto **`C:\Projects\raptor_australia`** y plan de adaptaciones para el proyecto **`C:\Users\hogwa\raptors-cnn`** (VRR — Veracruz River of Raptors).
>
> El proyecto australiano es **propiedad del mismo autor** (Brian Fernández Báez) y está mucho más avanzado en varios componentes. Hay piezas excelentes que vale la pena trasladar y adaptar al VRR.

**Fecha del análisis:** 2026-05-16

---

## 1. Resumen de cada proyecto

| Dimensión | 🇦🇺 raptor_australia | 🇲🇽 raptors-cnn (VRR) |
|-----------|---------------------|------------------------|
| **Estado** | Avanzado, con modelo real entrenado | Infraestructura completa, modelo solo con dataset sintético (smoke-test) |
| **Especies** | 8 rapaces del sureste de Australia | 14 rapaces migratorias del corredor de Veracruz |
| **Modelo** | EfficientNetB4 (~19 M params) | ResNet-50 / EfficientNet-B3 / MobileNetV3 / ConvNeXt — comparativa |
| **Accuracy real** | **84.95 % global (206 imgs test)** | Sintético: 100 % (no es real) |
| **F1 macro** | **0.848** | Sintético: 1.0 (no es real) |
| **Dataset** | ~5,000 imgs (iNat + Atlas of Living Australia) | Por descargar (script listo) |
| **Lengua de señas** | AUSLAN (Australian Sign Language) | International Sign (IS) |
| **Idiomas UI** | **10 idiomas** (es/en/fr/de/it/pt/ja/ko/ru/zh) | Solo español |
| **GUI** | Flask + HTML + CSS (~36 KB CSS, 27 KB index.html) | Gradio (más rápido pero menos pulido) |
| **Active learning** | ✅ Implementado + retraining cycle | ✅ Implementado en backend |
| **Darwin Core export** | ✅ Para Atlas of Living Australia / GBIF | Parcial (observations.py) |
| **Docker** | ✅ Dockerfile + .dockerignore + gunicorn | ❌ No |
| **CI/CD** | ✅ GitHub Actions workflow | ❌ No |
| **Notebooks Jupyter** | ✅ 4 numerados (01-04) + 9 scripts extra | ❌ No (solo train_colab.ipynb) |
| **Consulta comunidad sorda** | ✅ 5 docs (protocolo, presupuesto, contactos, email template) | ✅ 1 doc (cuestionario Likert) |
| **Documentación tesis** | ⚠️ MPhil proposal, no tesis completa | ✅ 5 capítulos DOCX, DMP, pre-registro |
| **Marco metodológico** | Práctico, orientado a despliegue | Académico, orientado a defensa de tesis |

## 2. Tesoros del proyecto Australia para adaptar al VRR

### 🥇 PRIORIDAD CRÍTICA

#### A1. Flask web app con look profesional
**Australia:** `gui/app.py` (36 KB), `gui/templates/index.html` (27 KB), `gui/static/css/style.css` (36 KB). 3 rutas: `/`, `/species`, `/data`.
**VRR actual:** Gradio (más rápido pero genérico).
**Acción:** **Migrar de Gradio → Flask**. Copiar `gui/app.py` como base, adaptar 14 especies VRR, traducir AUSLAN → International Sign. **Esfuerzo: 6-8 horas.**

#### A2. species_data.py estilo Merlin Bird ID
**Australia:** perfiles ricos por especie: `distribution`, `diet`, `behavior`, `migration`, `nesting`, `breeding_months`, `best_months`, `did_you_know`. Citas científicas en cabecera (HANZAB, Olsen, Debus, DAWE, BirdLife).
**VRR actual:** solo `field_marks`, `sign_description`, `abundance`. Falta toda la información biológica profunda.
**Acción:** Crear `app/species_data_full.py` para las 14 VRR siguiendo el mismo schema. Datos de Bildstein 2006, Pronatura, Howell 2012, IUCN. **Esfuerzo: 4-6 horas.**

#### A3. Internacionalización con 10 idiomas (i18n.py)
**Australia:** `gui/i18n.py` + `gui/translations/{de,en,es,fr,it,ja,ko,pt,ru,zh}.json` + `species_data_i18n.py` (120 KB!). Cookie de idioma de 1 año.
**VRR actual:** solo español.
**Acción:** Para Maestría no es crítico, pero **sería un diferenciador enorme**. Al menos ES + EN para alcance internacional. **Esfuerzo: 3-4 horas para 2 idiomas, +1 hora por idioma adicional.**

### 🥈 PRIORIDAD ALTA

#### A4. Notebooks Jupyter numerados (01-04)
**Australia:** workflow científico exportable: `01_download`, `02_preprocessing`, `03_training`, `04_evaluation`. Más 9 scripts auxiliares (`pick_hero_images.py`, `generate_auslan_svgs.py`, `restore_archived.py`, `retrain.py`, `filter_ala_quality.py`).
**VRR actual:** scripts sueltos sin numerar.
**Acción:** Reorganizar el flujo de VRR en notebooks numerados — facilita la **reproducibilidad** (criterio crítico de Maestría) y la **enseñanza** del workflow. **Esfuerzo: 3-4 horas.**

#### A5. Hero image picker con Faster R-CNN
**Australia:** `notebooks/pick_hero_images.py` usa Faster R-CNN para detectar el bounding box del ave y elegir automáticamente la mejor foto representativa por especie (sharpness + resolución + bird-detection score).
**VRR actual:** sin hero picker automático.
**Acción:** Copiar y adaptar. Critical para el catálogo de especies y para el catálogo de señas (los thumbnails). **Esfuerzo: 1-2 horas.**

#### A6. Protocolo de validación con comunidad sorda completo
**Australia:** `docs/auslan_consultation/` con 5 docs maduros:
- `validation_protocol.md` — Fase A iterativa + Fase B con 12+ participantes, escala Likert ≥ 4.0 sin componente < 3.5
- `sign_descriptions.md` — descripciones formales de cada seña
- `email_template.md` — plantilla para contactar Deaf Society
- `contacts.md` — Deaf Society of NSW, RIDBC, Auslan Signbank
- `budget_estimate.md` — costos estimados
**VRR actual:** solo cuestionario Likert.
**Acción:** Adaptar los 5 docs al contexto mexicano (IS + comunidad sorda mexicana). **Esfuerzo: 2-3 horas.**

#### A7. Docker + GitHub Actions CI
**Australia:** `Dockerfile` + `.dockerignore` + `.github/workflows/ci.yml`.
**VRR actual:** sin contenedor ni CI.
**Acción:** Copiar Dockerfile (adaptar app Flask), agregar workflow CI básico (tests + lint). **Esfuerzo: 1-2 horas.**

### 🥉 PRIORIDAD MEDIA (después de defensa de tesis)

#### A8. Darwin Core export robusto
**Australia:** exporta directamente al formato compatible con Atlas of Living Australia y GBIF.
**VRR actual:** `observations.py` parcial.
**Acción:** Reforzar `observations.py` para exportar también a GBIF/iNaturalist México. **Esfuerzo: 1-2 horas.**

#### A9. SVG-based AUSLAN signs animados
**Australia:** `generate_auslan_svgs.py` genera animaciones de seña en SVG (más ligeras que video, más fácil de producir sin necesidad de grabación con persona real).
**VRR actual:** tarjetas estáticas con descripción textual.
**Acción:** Adaptar el generador. **Esfuerzo: 2-3 horas.**

#### A10. CHANGELOG.md formal con SemVer
**Australia:** registro detallado de cambios versión por versión.
**VRR actual:** sin CHANGELOG.
**Acción:** Crear `CHANGELOG.md` y empezar a versionar con SemVer (v0.1.0 actual). **Esfuerzo: 30 min inicial.**

### ⚙️ EN PARALELO (criterio editorial)

| Pieza de Australia | ¿Adaptar a VRR? |
|---------------------|-------------------|
| `dataset/raw_archive/` (backup) | ✅ Sí — buena práctica |
| `dataset/metadata/quality_filter.csv` | ✅ Ya tenemos algo similar con `curate.py` |
| `restore_archived.py` (rollback de raw) | ✅ Útil si alguna vez se equivoca el filtro de curación |
| `pick_hero_manual.py` (override manual) | ✅ Práctico |
| `download_ala_videos.py` (videos de comportamiento) | ⚠️ Veracruz no tiene un equivalente directo a ALA |
| `fetch_ebird_data.py` | ✅ Ya tenemos `download_ebird.py` |

## 3. Lo que el VRR tiene que Australia NO

| Componente | VRR | Australia |
|-----------|-----|-----------|
| **Capítulos de tesis formal (DOCX)** | ✅ 5 capítulos | ❌ Solo "MPhil proposal" |
| **Data Management Plan formal** | ✅ DMP.md | ❌ |
| **Pre-registro de hipótesis (COS)** | ✅ preregistration.md | ❌ |
| **Documento de contribución novedosa** | ✅ contribucion_novedosa.md | ❌ |
| **Glosario unificado de 3 dominios** | ✅ glosario.md | ❌ |
| **Presentación PowerPoint** | ✅ 18 slides | ❌ |
| **Workflow de dataset real documentado** | ✅ WORKFLOW_DATASET_REAL.md | ❌ |
| **Guía de comandos paso a paso** | ✅ `documentacion/guias/GUIA_COMANDOS_V1_1.txt` | ❌ |
| **Auditoría de coherencia** | ✅ AUDITORIA_FASE1.md | ❌ |
| **Comparativa estadística entre 4 archs × 2 frameworks** | 📋 Planificada (McNemar + t-test) | ❌ Solo 1 arch (EfficientNetB4) |
| **Mixed Precision + Gradient Accumulation** | ✅ Para RTX 3050 4 GB | ⚠️ Asume RTX 3060+ |

**Conclusión:** el VRR tiene **mejor andamiaje académico** (todo lo necesario para defensa de Maestría), Australia tiene **mejor producto desplegable** (Flask, Docker, i18n, dataset real). Combinando ambos, el VRR puede ser un proyecto de Maestría con producto profesional, no solo experimento académico.

## 4. Plan de adaptaciones recomendado

### 🎯 Trayectoria sugerida (40-60 horas de trabajo)

**Sprint 1 — La GUI profesional (8-12 hrs)**
1. Copiar y adaptar `gui/app.py` de Australia → `codigo/pytorch/app_flask/` en VRR (Flask reemplaza Gradio).
2. Adaptar `gui/templates/{index,species,data}.html` con las 14 especies VRR.
3. Adaptar `gui/static/css/style.css`.
4. Migrar `species_data.py` con perfiles completos para las 14 VRR.

**Sprint 2 — Datos enriquecidos (4-6 hrs)**
5. Documentar perfiles biológicos completos por especie (Merlin-style).
6. Generar/seleccionar hero images con `pick_hero_images.py` adaptado.
7. Internacionalización ES + EN (después se agrega más).

**Sprint 3 — Despliegue y reproducibilidad (4-6 hrs)**
8. Copiar `Dockerfile` y `.github/workflows/ci.yml`.
9. Reorganizar scripts en notebooks numerados.
10. Crear `CHANGELOG.md` y arrancar versionado SemVer.

**Sprint 4 — Validación comunidad sorda (3-4 hrs)**
11. Adaptar los 5 docs de `auslan_consultation/` a `is_consultation/` (mexicano).
12. Generar SVG animations para las 14 señas.

**Sprint 5 — Entrenamiento real y métricas (variable, ya está documentado en WORKFLOW)**

### 📋 Resumen de archivos a copiar/adaptar

| Origen (Australia) | Destino (VRR) | Adaptación |
|---|---|---|
| `gui/app.py` | `codigo/pytorch/app_flask/app.py` | 8 → 14 especies, AUSLAN → IS, ES default |
| `gui/species_data.py` | `codigo/pytorch/app_flask/species_data_full.py` | Reescribir con datos de las 14 |
| `gui/i18n.py` | `codigo/pytorch/app_flask/i18n.py` | Sin cambios |
| `gui/translations/{es,en}.json` | `codigo/pytorch/app_flask/translations/` | Adaptar a textos VRR |
| `gui/templates/*.html` | `codigo/pytorch/app_flask/templates/` | Branding, especies |
| `gui/static/css/style.css` | `codigo/pytorch/app_flask/static/css/style.css` | Paleta VRR (verde/terracotta) |
| `notebooks/0[1-4]_*.ipynb` | `notebooks/` | Adaptar al pipeline VRR |
| `notebooks/pick_hero_images.py` | `codigo/pytorch/pick_hero_images.py` | Apenas tocar |
| `notebooks/generate_auslan_svgs.py` | `codigo/pytorch/generate_is_svgs.py` | Renombrar + 14 descripciones |
| `Dockerfile` | `Dockerfile` | Cambiar referencias |
| `.github/workflows/ci.yml` | `.github/workflows/ci.yml` | Cambiar nombres |
| `CHANGELOG.md` | `CHANGELOG.md` | Empezar desde cero v0.1.0 |
| `docs/auslan_consultation/*.md` | `documentacion/is_consultation/*.md` | Comunidad sorda mexicana |

## 5. Cosas críticas a tener en cuenta

1. **AUSLAN vs International Sign:** Australia usa AUSLAN (lengua de señas australiana). VRR usa IS (International Sign). **NO confundir.** Las señas DEBEN re-validarse con comunidad sorda mexicana, no reutilizar las australianas.

2. **Atlas of Living Australia vs iNaturalist México:** Australia tiene una API local muy potente (ALA). VRR tiene que apoyarse en iNaturalist + eBird + Macaulay. Distintas APIs, distintos workflows de descarga.

3. **Naming convention:** Australia usa `Aquila_audax`, VRR usa `Astur_cooperii`. Mantener consistencia con AOS 2024 en VRR (ya está).

4. **Modelo:** Australia usa **EfficientNetB4** (input 380×380). VRR compara 4 arquitecturas con input 224×224. Si se quiere comparabilidad directa, sumar EfficientNetB4 a la comparativa VRR (modificar `config.py`).

5. **Licencias:** ambos son MIT. Las señas en Australia tienen "additional terms" — adaptarlos al VRR con CC-BY-SA 4.0 (co-creación con comunidad sorda).

6. **Hardware:** Australia asume RTX 3060+. VRR ya tiene config optimizada para RTX 3050 4GB. **Mantener AMP + gradient accum.** en VRR.

## 6. Estructura final propuesta para VRR

Tras integrar lo mejor de Australia:

```
raptors-cnn/
├── README.md, LICENSE, CHANGELOG.md, CITATION.cff
├── Dockerfile, .dockerignore
├── .github/workflows/ci.yml
│
├── codigo/
│   ├── pytorch/
│   │   ├── app/            ← Gradio actual (lo mantenemos como alternativa rápida)
│   │   ├── app_flask/      ← NUEVO — adaptado del australiano
│   │   │   ├── app.py
│   │   │   ├── species_data.py
│   │   │   ├── species_data_i18n.py
│   │   │   ├── i18n.py
│   │   │   ├── templates/  ← index, species, data
│   │   │   ├── static/     ← css, js, img, is_signs/
│   │   │   └── translations/{es,en}.json
│   │   └── tensorflow/
│   ├── pick_hero_images.py
│   └── generate_is_svgs.py
│
├── notebooks/              ← NUEVO — reorganizado al estilo Australia
│   ├── 01_download_dataset.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_training.ipynb
│   ├── 04_evaluation.ipynb
│   └── (los scripts existentes integrados)
│
├── dataset/
│   ├── raw/, processed/, raw_archive/, feedback/, metadata/
│
├── models/
├── documentacion/resultados/ ← plantillas de reporte, métricas y Grad-CAM
│
├── documentacion/
│   ├── tesis/              ← lo que ya tenemos
│   ├── is_consultation/    ← NUEVO — protocolo, contactos, email, presupuesto
│   ├── diagramas/, analisis_comparativo_australia_vrr.md (este doc)
│   ├── preregistration.md, data_management_plan.md, ...
│
├── lengua_de_senas/
└── referencias/
```

---

## 7. Mi recomendación final

**Empezar por el Sprint 1 (la GUI Flask)** — es lo que más cambia el "wow factor" del proyecto. Las screenshots que me compartiste al principio mostraban EXACTAMENTE esa GUI. Adaptarla al VRR es trabajo concreto y produce algo visualmente fuerte para tus compañeros.

Después, **Sprint 2 (datos enriquecidos)** porque sin perfiles biológicos completos la GUI se ve vacía.

**Sprint 3 (Docker/CI/notebooks)** y **Sprint 4 (consulta comunidad sorda)** se pueden hacer en paralelo.

**El entrenamiento real (Sprint 5) lo tienes ya en `WORKFLOW_DATASET_REAL.md`** — no requiere copiar de Australia, ya está documentado.

---

*Documento generado tras inspección directa del repo `C:\Projects\raptor_australia` (~7,000 archivos, 13 .py, 13 .md, 6,983 imágenes).
Reporte preparado por Claude / Cowork — 2026-05-16.*
