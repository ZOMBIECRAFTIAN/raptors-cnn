# 🔍 Reporte de Auditoría — Fase 1

**Fecha:** 2026-05-14
**Estado del proyecto antes de la auditoría:** 67 archivos en GitHub, commit `69ddecb`
**Objetivo:** detectar inconsistencias, claims sin respaldo y elementos que no están al nivel de Maestría.

---

## A. Inconsistencias en el nivel académico

| # | Archivo | Texto problemático | Acción |
|---|---------|--------------------|--------|
| A1 | `README.md` | "Tesis de Licenciatura en Biología" (2 menciones) | Cambiar a "Tesis de Maestría" |
| A2 | `CITATION.cff` | `affiliation: "Tesis de Licenciatura en Biología"` y `thesis-type: "Licenciatura en Biología"` | Cambiar a Maestría |
| A3 | `documentacion/guias/GUIA_COMANDOS_V1_1.txt` | "Brian Fernandez Baez - Tesis de Biologia" | Actualizar |
| A4 | Capítulo 1 (cap1.js) | Portada dice "Tesis de Licenciatura en Biología" | Regenerar |
| A5 | `documentacion/RESUMEN_CHAT_PROYECTO_IA_AVES_RAPACES.md` | Doc histórico del chat anterior — opcional actualizar | Marcar como histórico |

## B. Inconsistencias en el número de señas

| # | Archivo | Texto problemático | Corregido a |
|---|---------|--------------------|-------------|
| B1 | `outputs/cap5.js` línea 24 | "catálogo final de 7 señas" | "catálogo final de 14 señas" |
| B2 | `outputs/cap5.js` línea 47 | "Primer catálogo de siete señas" | "Primer catálogo de 14 señas" |
| B3 | Capítulo 5 (.docx generado) | Refleja el error de cap5.js | Regenerar |

## C. Gaps científicos detectados (a reforzar para Maestría)

### C1. Justificación estadística del tamaño muestral
**Estado actual:** El proyecto define un mínimo de 200 imágenes/especie sin justificación estadística explícita.
**Para Maestría:** debe incluir cálculo de tamaño muestral con potencia estadística (p.ej. fórmula de Cohen para clasificación multiclase, o referencia a estudios análogos).

### C2. Validación cruzada
**Estado actual:** Mencionada 5-fold pero sin detallar el procedimiento exacto.
**Para Maestría:** describir Stratified K-Fold, manejo de fuga de datos entre splits, reporte de intervalos de confianza.

### C3. Análisis estadístico de comparativa PyTorch vs TensorFlow
**Estado actual:** Solo se planean comparar métricas puntuales.
**Para Maestría:** agregar test estadístico (p.ej. McNemar test para clasificadores pareados, t-test pareado sobre folds).

### C4. Discusión de "shortcut learning" hallado con Grad-CAM
**Estado actual:** Mencionado brevemente.
**Para Maestría:** profundizar — referencia a Geirhos et al. (2020) sobre shortcut learning, conexión con literatura de fairness y robustez.

### C5. Contribución novedosa explícita
**Estado actual:** Implícita en las contribuciones del Cap. 5.
**Para Maestría:** sección dedicada que articule:
1. **Lo que ya existe** (BirdNET acústico, Wildlife Insights mamíferos, sistemas de identificación posada).
2. **El gap específico** (rapaces en vuelo en cielo abierto, sin componente accesible).
3. **La contribución original de esta tesis** (clasificador especialista + co-creación con comunidad sorda + Grad-CAM como validación).

### C6. Plan de publicación
**Estado actual:** No documentado.
**Para Maestría:** mapa de revistas candidatas (Ecological Informatics IF≈4.6, Sign Language Studies, Journal of Raptor Research, Ardea) con timing de submission post-defensa.

## D. Bibliografía

| Métrica | Actual | Para Maestría | Gap |
|---------|--------|---------------|-----|
| Referencias en `referencias/bibliografia.md` | ~48 | 80+ | +32 |
| Referencias por bloque temático | Variable | Mínimo 15 por bloque (A, B, C, D) | Equilibrar |
| Referencias de los últimos 5 años | ~40% | ≥ 60% | Actualizar |

**Bloques de referencias a expandir:**
- **Shortcut learning / fairness en ML** (Geirhos, Buolamwini, Mehrabi, etc.)
- **Validación con comunidad sorda** (más Kusters, De Meulder, McCleary)
- **Ornitología cuantitativa moderna** (más Newton 2010, BirdLife 2024 trends, IUCN red list updates)
- **Veracruz post-2020** (Pronatura updates, papers recientes del corredor)

## E. Elementos faltantes que un proyecto de Maestría debería tener

| # | Elemento | Existe | Acción |
|---|----------|--------|--------|
| E1 | Protocolo de ética para grupo focal con comunidad sorda | Parcial (cuestionario Likert) | Agregar consentimiento informado escrito y bilingüe |
| E2 | Pre-registro de hipótesis y métodos | No | Crear `documentacion/preregistration.md` |
| E3 | Data Management Plan (DMP) | No | Crear `documentacion/data_management_plan.md` |
| E4 | Análisis de riesgos del proyecto | Sí, en Cap. 3 | Reforzar con matriz cuantitativa |
| E5 | Cronograma Gantt en LaTeX/imagen | Solo en RESUMEN_EJECUTIVO | Hacer figura formal para tesis |
| E6 | Glosario de términos técnicos | No | Crear `documentacion/glosario.md` |
| E7 | Resumen abstract bilingüe estructurado (IMRaD) | Parcial | Refinar para que cumpla estándar de revista |
| E8 | Plan de difusión post-tesis | No | Agregar al Cap. 5 trabajo futuro |

## F. Cosas que YA están bien (no tocar)

✅ Estructura modular del código
✅ Reproducibilidad (seeds, environment.yml, paths relativos)
✅ Licencias diferenciadas (código MIT, señas CC-BY-SA, datos por imagen)
✅ Verificación funcional del pipeline end-to-end
✅ Documentación de hardware mínimo
✅ Diagramas Mermaid del sistema
✅ Manejo de credenciales (.env / .gitignore)
✅ Conventional Commits
✅ Multilenguaje (resumen en EN + ES)

---

## 📋 Plan de rectificación

Las fases a ejecutar en orden:

1. **FASE 2 — Elevar a Maestría:** corregir A1-A5 y B1-B3 (correcciones triviales, 15 min).
2. **FASE 3 — Reforzar marco teórico:** atender C1-C6 y expandir bibliografía (D), agregar elementos faltantes (E1-E8). Tiempo estimado: 4-6 horas distribuidas en 2-3 sesiones.
3. **FASE 4 — Plan de publicación:** crear documento dedicado de contribución novedosa y plan de publicación.
4. **FASE 5 — Presentación base:** PowerPoint de 15-20 slides basado en el proyecto rectificado.

Al cerrar las 5 fases tendrás:
- Tesis técnicamente sólida al nivel de Maestría.
- Capítulos 1-3 con marco metodológico defendible.
- Capítulos 4-5 con estructura lista para llenar con resultados reales.
- Bibliografía equilibrada y actualizada.
- Documento explícito de contribución novedosa.
- PowerPoint listo para presentar a tus compañeros y comité.
- README de GitHub que comunique el valor académico.
