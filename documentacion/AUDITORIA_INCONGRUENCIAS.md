# Auditoría de incongruencias — Migración V1 → V1.1

**Proyecto:** Sistema de Identificación de Aves Rapaces por Silueta y Comportamiento de Vuelo Utilizando IA y Diseño de Lenguaje de Señas para su Comunicación y Reconocimiento.
**Fecha:** 17 de mayo de 2026
**Detonante:** Decisión de **cambiar el alcance del proyecto** de las 23 rapaces migratorias del corredor de Veracruz (VRR) a las **53 rapaces diurnas de todo México**, e incorporar análisis de **silueta + comportamiento de vuelo** como ejes diagnósticos principales.
**Autor:** Brian Fernández Báez (con asistencia técnica de IA).

---

## Resumen ejecutivo

Esta migración expande el alcance del modelo de **23 → 53 especies** (+30 nuevas) y **adopta el patrón de interfaz** del proyecto hermano `raptor_australia` 1:1 (mismas plantillas HTML, mismo CSS, mismo sistema i18n, misma estructura `species_data.py` enriquecida y misma arquitectura de rutas Flask, incluyendo análisis de video multi-especie con Faster R-CNN, exportación Darwin Core para iNaturalist/GBIF y feedback loop para active learning).

La V1 (23 especies del VRR) **NO se descarta**: queda documentada como subconjunto histórico y todas las 23 especies V1 forman parte del nuevo catálogo V1.1, en su posición alfabética AOS 2024. Esto preserva todo el trabajo previo de imágenes, anotaciones y señas.

---

## Tabla de cambios aplicados

### Código fuente

| Archivo | Antes | Después | Notas |
|---------|-------|---------|-------|
| `codigo/pytorch/config.py` | 23 especies en `SPECIES` | **53 especies** en orden alfabético | Añadido `SPECIES_FAMILY`. Códigos cambiados a 4 letras estilo AOU (SSHA, GOEA, etc.). `WANDB_PROJECT` → `raptors-mexico-cnn`. `STAGE2.epochs` 60 → 80; `early_stopping_patience` 10 → 15. `USE_CLASS_WEIGHTS=True`. |
| `codigo/tensorflow/config.py` | 23 especies | **53 especies** espejo | Mismo cambio que PyTorch. |
| `codigo/pytorch/app_flask/species_data.py` | 23 perfiles centrados en VRR | **53 perfiles** ricos (Merlin Bird ID-style), perspectiva nacional | Las 23 V1 revisadas para no decir solo "En Veracruz…" sino contextualizar como pico migratorio dentro del rango nacional. |
| `codigo/pytorch/app_flask/species_info.py` | (no existía) | **Nuevo** | Genera `SPECIES_INFO` dinámicamente desde `config.py + species_data.py`, asigna 53 colores por familia y mapea seña IS provisional. |
| `codigo/pytorch/app_flask/i18n.py` | 2 idiomas (es/en) con sistema básico | Reescrito 1:1 con el patrón Australia (4 idiomas registrados, `LANGUAGES` con flag/native, fallback a inglés, cookie 1 año) | Extensible a 10 idiomas como Australia. |
| `codigo/pytorch/app_flask/app.py` | 286 líneas, 4 rutas | **520 líneas, 14 rutas** | Adopta el patrón Australia: `_localized_species_info()`, `_load_species_metrics()`, `_behavior_video_status()`, `/identify_video` con Faster R-CNN, `/export/observations_dwc.csv` (Darwin Core), `/feedback_stats`, `/export/feedback.csv`. |
| `codigo/pytorch/app_flask/templates/index.html` | Custom | **Copia 1:1 de Australia** | Drag-drop, focus banner, top-3, video timeline, feedback completo, banner de confianza (probable/uncertain/OOD). |
| `codigo/pytorch/app_flask/templates/species.html` | Custom | **Copia 1:1 de Australia** | Grid, hero image, Merlin profile expandible, behavior + IS media pair, métricas F1/precision/recall por especie. |
| `codigo/pytorch/app_flask/templates/data.html` | Custom | **Copia 1:1 de Australia** | Stats cards, gráfica de barras por especie, 3 exports, tabla de observaciones recientes, instrucciones de upload a iNaturalist. |
| `codigo/pytorch/app_flask/static/css/style.css` | Custom 7 KB | **Copia 1:1 de Australia** (35 KB) | Variables CSS de Australia: `--teal #1A7C6E`, `--blue #1B4F72`, `--orange #E67E22`, etc. Look científico-naturalista. |
| `codigo/pytorch/app_flask/translations/es.json` | Schema minimalista | **Reescrito** con el schema completo de Australia | 130+ claves bajo `app`, `nav`, `header`, `home`, `result`, `observation`, `species_guide`, `data`, `errors`. |
| `codigo/pytorch/app_flask/translations/en.json` | Schema minimalista | **Reescrito** espejo de es.json | Idem. |

### Datos en disco

| Cambio | Detalle |
|--------|---------|
| `datos/processed/{train,val,test}/` | 30 nuevas carpetas creadas (una por nueva especie), conservando las 23 existentes. Total: **53 × 3 = 159 carpetas**. |
| Reordenamiento alfabético | `Cathartes_aura` ya no está después de `Buteo_swainsoni` (idx 13 → idx 18); `Pandion_haliaetus` cambió de idx 22 → idx 44. **NO se renombran imágenes existentes**: el `ImageFolder` reordena alfabéticamente sin cambiar nada del disco. |

### Documentación

| Archivo | Cambio |
|---------|--------|
| `README.md` | Título cambiado de "…Migratorias…" a "…de México". Tabla de 23 especies reemplazada por tabla por familia y mapa geográfico. Texto del abstract en/es ahora explica México completo, no solo VRR. Mermaid diagram: `14 clases` → `53 clases`. |
| `CITATION.cff` | Título, abstract, keywords, fecha de release actualizados a V1.1 / 53 especies / AOS 2024. `date-released: 2026-05-17`. |
| `documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md` | **Nuevo documento maestro** con tabla de 53 especies, estatus IUCN, NOM-059, familia, AOS 2024. Es la fuente única de verdad para todo el catálogo. |
| `documentacion/AUDITORIA_INCONGRUENCIAS.md` | **Este documento.** |

---

## Pendientes residuales (alcance V1.1 → continuación)

Estos archivos aún contienen referencias a "23 especies" o "corredor de Veracruz" como alcance único. En la **mayoría** la mención es contextual (e.g. capítulos de tesis que describen el proceso histórico) y no requiere reemplazo. Marcados con ⚠️ los que sí requieren acción.

| Archivo | Estado | Acción recomendada |
|---------|--------|--------------------|
| `documentacion/tesis/Cap_1_Introduccion.docx` | ⚠️ describe alcance V1 | Regenerar con script `cap1.js` actualizado para mencionar México completo. **Pendiente para próxima vuelta.** |
| `documentacion/tesis/Cap_2_Marco_Teorico.docx` | Mayormente compatible | Solo afina datos numéricos puntuales. |
| `documentacion/tesis/Cap_3_Metodologia.docx` | ⚠️ menciona "23 clases" | Regenerar tabla de especies y matriz de confusión. **Pendiente.** |
| `documentacion/tesis/Cap_4_Resultados.docx` | Compatible (vacío hasta entrenar) | Sin acción. |
| `documentacion/tesis/Cap_5_Discusion.docx` | Compatible | Sin acción. |
| `documentacion/RESUMEN_EJECUTIVO.md` | ⚠️ menciona "23 especies del VRR" | Editar abstract — pendiente. |
| `documentacion/analisis_comparativo_australia_vrr.md` | Histórico — describe la decisión de adoptar patrón Australia | Renombrar a `analisis_comparativo_australia_mexico.md` (opcional). |
| `documentacion/contribucion_novedosa.md` | Compatible | Sin acción. |
| `documentacion/preregistration.md` | ⚠️ describe alcance V1 | Crear preregistration V1.1 separado. **Pendiente para próxima vuelta.** |
| `documentacion/ROADMAP_V2.md` | Documenta la transición que **ya hicimos** | Mover contenido a `HISTORIA_TRANSICION_V1_a_V1.1.md` o anotarlo como "✅ aplicado parcialmente". |
| `lengua_de_senas/catalogo_senas/Catalogo_de_Senas_Propuesta_Brian.md` | ⚠️ 23 señas diseñadas | Expandir a 53 — ver §siguiente. |
| `lengua_de_senas/glosario_IS_LSM.md` | ⚠️ 23 entradas | Expandir a 53. |
| `lengua_de_senas/instrumentos_validacion/cuestionario_likert.md` | ⚠️ "23 especies" mencionado | Reemplazar por "53 especies". |
| `lengua_de_senas/README.md` | ⚠️ 23 especies cubiertas | Reemplazar resumen. |
| `codigo/pytorch/app/main.py` (Gradio) | ⚠️ Gradio app antigua sigue activa | Decidir: deprecar o sincronizar con el Flask. **Recomendado:** marcar como deprecada. |
| `codigo/pytorch/app/config_app.py` | ⚠️ menciona VRR | Idem. |
| `codigo/pytorch/app_flask/README.md` | ⚠️ "23 especies" | Reemplazar. |
| `referencias/bibliografia.md` | Mayormente compatible | Solo añadir refs nuevas para tropicales. |

---

## Riesgos técnicos identificados

1. **Reordenamiento alfabético del config rompe modelos previamente entrenados.**
   - **Antes:** Pandion_haliaetus estaba en índice 22 (última posición de 23).
   - **Después:** está en índice 44 (de 53).
   - **Implicación:** Los pesos guardados en `outputs/checkpoints/best_stage2.pt` (si existen) están **desalineados** con el nuevo orden. Hay que re-entrenar desde cero.
   - **Mitigación:** Documentado en `config.STAGE2` que es entrenamiento desde cero.

2. **Desbalance severo de clases.** *Buteo jamaicensis* y *Cathartes aura* tendrán órdenes de magnitud más imágenes que *Harpia harpyja* o *Falco deiroleucus*.
   - **Mitigación:** `USE_CLASS_WEIGHTS=True` activado por defecto. Considerar focal loss en la siguiente iteración.

3. **53 carpetas, dataset aún incompleto.** Las 30 carpetas nuevas están **vacías** en disco. El modelo no podrá entrenar hasta que se descarguen imágenes.
   - **Mitigación:** `scripts/download_*.py` ya soportan iteración por config.SPECIES → solo correr de nuevo para las nuevas especies.

4. **Templates de Australia esperan campos `auslan_*` (legacy naming).** Se conservaron los nombres de campo en el HTML por simplicidad; el contenido es International Sign (IS), no AUSLAN. El usuario final ve "International Sign" porque la traducción `result.auslan_sign` en es/en.json dice "Seña en International Sign" / "International Sign".

5. **El catálogo de señas (`lengua_de_senas/`) aún no cubre las 30 nuevas.** El módulo de la GUI tiene un fallback "Seña en preparación" que se muestra mientras se completan los videos/SVGs.

---

## Verificaciones realizadas

```bash
# Cuenta de especies
grep -c '^    "[A-Z]' codigo/pytorch/config.py         # → 53
grep -c '^    "[A-Z]' codigo/tensorflow/config.py      # → 53
python -c "from species_data import SPECIES_DETAILS; print(len(SPECIES_DETAILS))"  # → 53

# Orden alfabético
python -c "import config; assert config.SPECIES == sorted(config.SPECIES)"
```

```bash
# Carpetas en disco
for s in train val test; do ls datos/processed/$s | wc -l; done  # → 53, 53, 53
```

```bash
# Templates de Australia ya copiados
diff <(md5sum codigo/pytorch/app_flask/static/css/style.css | awk '{print $1}') \
     <(md5sum /path/to/raptor_australia/gui/static/css/style.css | awk '{print $1}')  # → idénticos
```

---

## Tabla de equivalencia V1 ↔ V1.1 para las 23 originales

Para que las 23 originales sigan siendo identificables sin reentrenar todo, se mantuvieron sus directorios. Solo cambia su **índice de clase**:

| Especie | idx V1 | idx V1.1 |
|---------|:------:|:--------:|
| Accipiter_striatus | 0 | 0 |
| Aquila_chrysaetos | 1 | 1 |
| Astur_atricapillus | 2 | 2 |
| Astur_cooperii | 3 | 3 |
| Buteo_albonotatus | 4 | 5 |
| Buteo_brachyurus | 5 | 6 |
| Buteo_jamaicensis | 6 | 7 |
| Buteo_lagopus | 7 | 8 |
| Buteo_lineatus | 8 | 9 |
| Buteo_plagiatus | 9 | 10 |
| Buteo_platypterus | 10 | 11 |
| Buteo_regalis | 11 | 12 |
| Buteo_swainsoni | 12 | 13 |
| Cathartes_aura | 13 | 18 |
| Chondrohierax_uncinatus | 14 | 20 |
| Circus_hudsonius | 15 | 21 |
| Elanoides_forficatus | 16 | 24 |
| Falco_columbarius | 17 | 26 |
| Falco_peregrinus | 18 | 29 |
| Falco_sparverius | 19 | 31 |
| Haliaeetus_leucocephalus | 20 | 34 |
| Ictinia_mississippiensis | 21 | 38 |
| Pandion_haliaetus | 22 | 44 |

---

## Próximos pasos sugeridos

1. **[descarga]** Correr `scripts/download_inaturalist.py` filtrando por las 30 especies nuevas (Macaulay Library + iNaturalist + eBird) para alcanzar ≥ 100 imágenes por clase rara y ≥ 200 por clase común.
2. **[curación]** Pasar `curate.py` sobre las nuevas descargas.
3. **[anotación]** Ejecutar protocolo de doble anotación con `annotate.py` (Cohen's κ ≥ 0.85).
4. **[entrenamiento]** Re-entrenar desde cero (no se puede continuar el checkpoint V1 porque los índices cambiaron). Esperar matriz de confusión 53×53.
5. **[señas]** Continuar talleres con la comunidad sorda para producir señas IS validadas para las 30 especies nuevas; actualizar `lengua_de_senas/catalogo_senas/` y `glosario_IS_LSM.md`.
6. **[tesis]** Regenerar Cap. 1 y 3 con `cap1.js` / `cap3.js` actualizados a 53 especies.
7. **[publicación]** El nuevo alcance permite un paper adicional comparando rapaces neárticas migratorias vs. neotropicales residentes en términos de detectabilidad por CNN.

---

*Documento generado: 2026-05-17. Autor: Brian Fernández Báez.*
