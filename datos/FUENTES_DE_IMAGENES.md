# Fuentes de imágenes para el dataset de las 14 especies

Este documento describe las fuentes evaluadas para construir el dataset de la tesis, sus pros y contras, y el orden recomendado de uso.

## Resumen rápido

| Fuente | Acceso | Volumen | Calidad | Licencia | Recomendación |
|--------|--------|---------|---------|----------|----------------|
| **iNaturalist** | API pública sin auth | Muy alto | Alta (research-grade) | Mixta, filtrable | **Empezar aquí** |
| **Macaulay Library** | API key gratuita académica | Muy alto | Profesional | Restrictiva | Como complemento |
| **eBird** | API key gratuita | Alto | Variable | A través de Macaulay | Solo metadatos |
| **GBIF** | API pública | Muy alto | Variable | Mixta | Última opción |
| **Pronatura Veracruz** | Contacto directo | Bajo | Profesional, local | Acuerdo bilateral | Insumo de campo |
| **Recolección propia** | Trabajo de campo | Bajo | Variable | CC-BY del autor | Para validación local |

---

## 1. iNaturalist (recomendado para empezar)

**URL base:** `https://api.inaturalist.org/v1/`
**Auth:** no requiere clave de API.
**Documentación:** https://api.inaturalist.org/v1/docs/

**Pros:**

- Sin API key.
- Cada observación tiene un grado de calidad (`research-grade` significa validada por al menos 2 personas con identificaciones concordantes).
- Las fotos tienen su licencia explícita; se puede filtrar a CC-BY, CC0, etc.
- Cobertura excelente para Norteamérica y crecientes para México.
- Cada foto tiene metadatos: fecha, geolocalización (cuando el usuario lo permite), fotógrafo, observación URL.

**Contras:**

- Algunas fotos son de aves posadas o capturadas, no en vuelo. Hay que filtrar manualmente o usando heurísticas (aspect ratio del crop, presencia de cielo, etc.).
- La calidad varía; algunas fotos son de baja resolución o están a gran distancia.

**Cómo usarlo:**

```bash
conda activate raptors-pt
cd C:\Users\hogwa\raptors-cnn\codigo\pytorch
python download_inaturalist.py --target 250 --max-pages 5
```

El script descarga hasta 250 imágenes por especie (3,500 totales para las 14), filtrando por licencias abiertas, y guarda metadatos en `datos/annotations/inaturalist_metadata.csv`.

**Importante:** después de descargar, se requiere una pasada manual para descartar imágenes no aptas (aves posadas, calidad baja, individuo demasiado lejano).

---

## 2. Macaulay Library (Cornell Lab of Ornithology)

**URL base:** `https://search.macaulaylibrary.org/`
**Auth:** requiere API key gratuita para uso académico.
**Cómo obtenerla:** registrarse en https://www.birds.cornell.edu/home y solicitar acceso a la API. Toma 1-3 días hábiles.

**Pros:**

- La fototeca de aves más grande y rigurosa del mundo (>50 millones de registros multimedia).
- Calidad media-alta, validada por curadores.
- Cada foto/grabación tiene metadatos completos, integrados con eBird.
- Cobertura global excelente.

**Contras:**

- Las imágenes tienen licencia restrictiva por defecto (uso académico, sin redistribución sin permiso explícito). No se pueden subir directamente a un repositorio público con el dataset entrenado.
- El acceso requiere registro y autorización de Cornell.

**Estrategia recomendada:** úsalo para complementar especies que iNat tenga pocas fotos (ZT, ML, PG), y documenta con cuidado las licencias por imagen. En el dataset publicado, sustituye las imágenes restrictivas por placeholders y deja la información en metadatos.

---

## 3. eBird (Cornell Lab)

**URL base:** `https://api.ebird.org/v2/`
**Auth:** requiere API key gratuita (registro instantáneo en https://ebird.org/api/keygen).

**Pros:**

- Datos de observaciones (avistamientos) sin las fotos.
- Útil para mapear distribución temporal y geográfica de cada especie en Veracruz.

**Contras:**

- Las fotos están en Macaulay Library, no en eBird directamente. eBird sirve más como complemento metadatístico.

**Uso recomendado:** para enriquecer el dataset con metadatos de abundancia por temporada (¿cuándo pasa cada especie por Veracruz?) y para calibrar el balance de clases.

---

## 4. GBIF (Global Biodiversity Information Facility)

**URL base:** `https://api.gbif.org/v1/`
**Auth:** no requiere clave.

**Pros:**

- Aglomerador de datasets de todo el mundo.
- API pública con licencia documentada por registro.

**Contras:**

- Muy heterogéneo en calidad y licencias.
- Muchos registros sin foto.

**Uso recomendado:** solo si las otras fuentes son insuficientes. Útil para especies muy raras.

---

## 5. Pronatura Veracruz

**Contacto:** información@pronaturaveracruz.org y @pronaturaveracruz en redes sociales.

**Pros:**

- Imágenes propias del corredor del Río de Rapaces (Cardel y Chichicaxtle).
- Calidad profesional en muchos casos.
- Si se establece un acuerdo de colaboración, las imágenes son de la zona específica de estudio (no genéricas).

**Contras:**

- Volumen limitado.
- Requiere gestión institucional (carta de presentación, propósito académico, plan de uso).

**Estrategia recomendada:** contactar formalmente para una colaboración. Pronatura ha sido aliada del proyecto Río de Rapaces desde 1991; un proyecto de tesis que automatice parte de su trabajo es de interés mutuo.

---

## 6. Recolección propia

**Pros:**

- Imágenes 100 % bajo tu autoría y licencia.
- Aseguran que el dataset tenga representación local específica de Veracruz.
- Sirven para validación de campo: "¿el modelo entrenado con datos globales identifica correctamente las aves del corredor en condiciones reales?".

**Contras:**

- Requiere trabajo de campo durante la temporada migratoria (agosto-noviembre).
- Equipo: cámara con teleobjetivo (≥ 300 mm idealmente), tarjeta SD, libreta de campo.

**Estrategia recomendada:** programar al menos una visita a Cardel o Chichicaxtle en pico migratorio (mediados de septiembre — Buteo platypterus) y un viaje de cierre en octubre. Cada imagen propia es oro para la sección de validación.

---

## Plan de recolección sugerido

**Fase 1 (semana 1-2):** descargar de iNaturalist con licencias abiertas. Objetivo: 200-300 imágenes por especie. Total estimado: 3,000-4,000 imágenes brutas.

**Fase 2 (semana 3):** descartar manualmente imágenes no en vuelo, baja calidad o ambiguas. Espera retener ~50-70 % del lote bruto.

**Fase 3 (semana 4-5):** identificar especies con datos insuficientes y suplementar con Macaulay Library (con autorización).

**Fase 4 (semana 6+):** agendar trabajo de campo en Veracruz y/o contactar Pronatura para imágenes locales adicionales.

**Fase 5:** doble anotación con un compañero/asesor → calcular kappa de Cohen → resolver desacuerdos.

---

## Consideraciones éticas y legales

1. **Respeto a la fauna:** el código ético de la American Birding Association (ABA, 2018) prohíbe perturbar a las aves para obtener fotografías. No se usan playback ni cebos para atraer rapaces.
2. **Consentimiento del fotógrafo:** aunque las licencias CC permiten uso, se acredita siempre al autor original en metadatos y en cualquier publicación derivada.
3. **Privacidad geográfica:** algunas observaciones de iNaturalist están geolocalizadas (especialmente las de especies en peligro). El proyecto NO publica esa coordenada, solo el estado/región.
4. **Licencias del dataset entrenado:** publicación final como mosaico de licencias documentadas por imagen. El modelo entrenado se libera bajo Creative Commons CC-BY 4.0.
