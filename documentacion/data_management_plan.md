# Plan de Gestión de Datos (Data Management Plan)

> Documento exigible en proyectos de Maestría con componente de dataset abierto. Sigue los principios FAIR (Findable, Accessible, Interoperable, Reusable) y las recomendaciones de Wilkinson et al. (2016).

**Proyecto:** raptors-cnn — Identificación de aves rapaces migratorias mediante IA y lengua de señas
**Autor:** Brian Fernández Báez
**Fecha:** 2026-05-14
**Versión:** 1.0

---

## 1. Tipos de datos generados o utilizados

### 1.1 Datos de entrada (input)

| Categoría | Origen | Volumen estimado | Formato | Licencia |
|-----------|--------|-------------------|---------|----------|
| Imágenes de rapaces en vuelo | iNaturalist, Macaulay Library, Pronatura, recolección propia | ~3,500 archivos / ~5-10 GB | JPG/PNG | Heterogénea (CC0, CC-BY, CC-BY-SA, propietaria con autorización) |
| Observaciones eBird | API eBird 2.0 | ~500 KB | CSV | Bajo términos eBird (sin redistribución comercial) |
| Hotspots eBird Veracruz | API eBird | ~80 KB | CSV | Bajo términos eBird |
| Videos del catálogo de señas | Grabación propia | ~14 archivos / ~200 MB | MP4 | CC-BY-SA 4.0 (co-creación con comunidad sorda) |

### 1.2 Datos generados (output)

| Categoría | Volumen | Formato | Licencia |
|-----------|---------|---------|----------|
| Pesos del modelo entrenado | ~100 MB por arquitectura × 4 | .pt, .keras | CC-BY 4.0 |
| Métricas y reportes | ~10 MB | CSV, JSON, PNG | CC-BY 4.0 |
| Capítulos de tesis | ~150 KB | DOCX | CC-BY-NC 4.0 |
| Código fuente | ~500 KB | Python, JS, MD | MIT License |
| Catálogo de señas | ~200 MB | MP4, MD, SVG | CC-BY-SA 4.0 |

## 2. Estándares de metadatos

### 2.1 Metadatos de imagen

Archivo: `datos/annotations/metadata.csv` con las siguientes columnas (Darwin Core compatible):

| Columna | Descripción | Tipo | Obligatoria |
|---------|-------------|------|-------------|
| `filename` | Nombre del archivo (sin ruta) | string | Sí |
| `species_code` | Código interno de dos letras | string | Sí |
| `scientific_name` | Nombre científico AOS 2024 | string | Sí |
| `source` | macaulay / inaturalist / pronatura / propio | enum | Sí |
| `license` | CC0, CC-BY, CC-BY-SA, etc. | enum | Sí |
| `photographer` | Nombre del autor | string | Sí |
| `date` | YYYY-MM-DD | ISO 8601 | Cuando disponible |
| `location` | Lat,Long o nombre de sitio | string | Cuando disponible |
| `angle` | dorsal / ventral / lateral | enum | Sí |
| `condition` | clear / cloudy / backlit | enum | Sí |
| `resolution_w`, `resolution_h` | Píxeles | int | Sí |
| `annotator_1`, `annotator_2` | Iniciales del anotador | string | Sí |
| `agreement` | 1 si coinciden, 0 si discrepan | binary | Sí |
| `final_label` | Etiqueta tras resolución de conflictos | string | Sí |

### 2.2 Metadatos del modelo

Cada checkpoint incluye archivo `.json` complementario con:
- Arquitectura, framework, versión.
- Hiperparámetros (lr, batch_size, epochs, scheduler, etc.).
- Semilla aleatoria.
- Métricas en val y test.
- Fecha y commit hash del repo.
- Hash SHA-256 del archivo de pesos.

## 3. Almacenamiento y respaldo

| Lugar | Datos | Frecuencia de respaldo |
|-------|-------|------------------------|
| Disco local del autor | Todo el proyecto activo | Cada cambio |
| GitHub (público) | Código, documentación, capítulos, metadatos | Por cada commit |
| Hugging Face Hub (planeado) | Pesos finales del modelo | Al cierre del proyecto |
| Zenodo (planeado) | Dataset etiquetado con DOI | Al cierre del proyecto |

## 4. Cómo se compartirán los datos (FAIR)

### Findable (encontrables)
- DOI permanente vía Zenodo para el dataset y los pesos.
- Repositorio GitHub indexado por Google Scholar y GitHub search.
- CITATION.cff para citación estandarizada.
- Topics relevantes en GitHub (machine-learning, raptors, accessibility, etc.).

### Accessible (accesibles)
- Acceso sin restricciones desde GitHub para código y metadatos.
- Dataset disponible mediante Zenodo (descarga directa).
- Modelo descargable desde Hugging Face Hub.

### Interoperable (interoperables)
- Imágenes en formatos estándar (JPG, PNG).
- Metadatos en CSV (UTF-8) con headers documentados.
- Pesos en formatos ampliamente soportados (.pt PyTorch, .keras Keras 3).
- Estructura de carpetas estándar de ImageFolder (compatible con torchvision y tf.keras).

### Reusable (reutilizables)
- Licencias claras y documentadas por componente.
- Documentación bilingüe (ES principal, EN abstract).
- Scripts de carga y preprocesamiento incluidos.
- Pre-registro de hipótesis y métodos publicado junto con el código.

## 5. Privacidad y consideraciones éticas

### 5.1 Fauna
- Cero captura, manipulación o perturbación de aves.
- Imágenes a distancia o tomadas en sitios públicos.
- Cumple con código ético de la American Birding Association (ABA, 2018).

### 5.2 Comunidad sorda
- Consentimiento informado por escrito para todos los participantes del grupo focal de validación de señas.
- Anonimización: solo se reportan agregados, no identidades.
- Compensación simbólica por tiempo invertido.
- Co-autoría reconocida en publicaciones derivadas (sección de agradecimientos y autoría compartida del catálogo).

### 5.3 Datos sensibles
- **No se publican coordenadas exactas** de avistamientos de especies en estatus de conservación (Buteo albonotatus, Ictinia mississippiensis).
- Coordenadas se anonimizan a nivel de estado o municipio si la especie es vulnerable.

## 6. Período de retención

| Categoría | Período mínimo | Estrategia post-retención |
|-----------|----------------|----------------------------|
| Código | Indefinido (GitHub) | Mirror en Software Heritage |
| Pesos | 10 años | Migración a Zenodo permanente |
| Dataset | 10 años | Migración a Zenodo permanente |
| Datos del grupo focal | 5 años | Anonimización agregada + eliminación de datos individuales |
| Tesis | Indefinido | Repositorio institucional + GitHub |

## 7. Costos estimados de gestión de datos

| Concepto | Costo | Cobertura |
|----------|-------|-----------|
| GitHub público | $0 | Indefinido |
| Zenodo | $0 (gratis para datasets académicos < 50 GB) | Indefinido |
| Hugging Face Hub | $0 (gratis para modelos abiertos) | Indefinido |
| Almacenamiento local | $0 (HDD/SSD del autor) | Mientras dure el proyecto |
| Backup en nube personal | ~$2/mes (OneDrive estudiante) | 5 años |

**Total estimado:** < $120 USD durante 5 años post-defensa.

## 8. Responsabilidades

| Rol | Persona | Responsabilidad |
|-----|---------|-----------------|
| Project Lead | Brian Fernández Báez | Curaduría del repositorio, ediciones de metadatos, comunicación con archivos públicos |
| Asesor de tesis | [a definir] | Revisión y validación científica |
| Comunidad sorda colaboradora | Grupo focal | Validación del catálogo de señas |

---

## Referencias

- Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.
- Force11. (2020). The FAIR Data Principles. https://www.force11.org/group/fairgroup/fairprinciples
- American Birding Association. (2018). Code of Birding Ethics.

---

*Este plan se revisará anualmente y al final del proyecto. Cualquier modificación se documenta con fecha en el changelog del repositorio.*
