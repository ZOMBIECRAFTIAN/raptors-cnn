# Workflow Completo — Dataset Real para raptors-cnn

Guía paso a paso del proceso integral, desde la descarga hasta el modelo entrenado y evaluado. Cada fase indica tiempo realista, comandos exactos y checkpoint de calidad.

---

## Resumen del pipeline

```
1. DESCARGAR  →  2. CURAR  →  3. ANOTAR  →  4. DIVIDIR  →  5. ENTRENAR  →  6. EVALUAR  →  7. INTERPRETAR
   (download)     (curate)     (annotate)    (split)        (train)         (evaluate)     (gradcam)
```

Tiempos estimados acumulados:

| Fase | Tarea | Tiempo |
|------|-------|--------|
| 1 | Descarga iNaturalist (~3,500 imgs) | 1-2 h |
| 1 | Descarga eBird hotspots + observaciones | 5 min |
| 2 | Curación automática | 10 min |
| 3 | Doble anotación de 1,400 imgs | 8-12 h |
| 4 | Split estratificado | 1 min |
| 5 | Training 4 archs × 60 epochs (RTX 3050) | 2-4 h |
| 5 | Training en Colab T4 (alternativa) | 1-2 h |
| 6 | Evaluación + comparativa | 10 min |
| 7 | Grad-CAM sobre el modelo ganador | 10 min |
| **Total** | | **~14-20 horas distribuidas en 3-5 días** |

---

## Fase 1 — Descarga

### 1.1 iNaturalist (imágenes con licencia abierta)

```bash
conda activate raptors-pt
cd /d C:\Users\hogwa\raptors-cnn\codigo\pytorch

# Primero un dry-run con una sola especie para verificar la API responde
python download_inaturalist.py --species TV --target 5 --dry-run

# Si pasa, descarga completa
python download_inaturalist.py --target 250 --max-pages 5
```

Resultado esperado:
- 3,500 imágenes JPG/PNG en `datos/raw/<scientific_name>/`
- CSV con metadatos en `datos/annotations/inaturalist_metadata.csv`

> **Tip:** corre esto al final del día. Tarda 1-2 horas. Si te quedas sin pestaña, no problema — solo vuelve a ejecutar y skipea las que ya tiene.

### 1.2 eBird (observaciones recientes y hotspots)

Asegúrate de tener `.env` con `EBIRD_API_KEY=...` configurado.

```bash
python download_ebird.py --region MX-VER --days 30 --hotspots
```

Genera dos CSVs útiles para el Cap. 4:
- `ebird_observations_MX-VER.csv` — observaciones recientes con coordenadas
- `ebird_hotspots_MX-VER.csv` — todos los hotspots de Veracruz

---

## Fase 2 — Curación automática

Elimina imágenes obviamente no aptas usando umbrales de calidad (resolución, brillo, contraste, blur, aspect ratio, duplicados).

```bash
# Dry-run: solo genera reporte CSV, no toca archivos
python curate.py

# Revisa datos/annotations/curation_report.csv en Excel para entender qué pasaría

# Si te convencen los descartes propuestos, aplica:
python curate.py --apply
```

`--apply` mueve archivos a 3 subcarpetas dentro de cada especie:
- `_keep/` — score ≥ 75 (mantener)
- `_review/` — score 45-74 (revisar manualmente)
- `_discard/` — score < 45 o duplicado (descartar)

### Umbrales por defecto (ajustables en `curate.py`)
- Resolución mínima: 640 px lado mayor
- Brillo: 30–240 / 255
- Contraste: ≥ 15 (desviación estándar)
- Sharpness: ≥ 60 (Laplacian variance)
- Aspect ratio: 0.4–2.5

> **Resultado típico:** de 3,500 imágenes brutas, ~60-70% pasan a `_keep`, ~20% a `_review`, ~10-20% a `_discard`.

---

## Fase 3 — Anotación doble con cálculo de Kappa

### 3.1 Anotador 1 (tú)

```bash
python annotate.py --annotator brian
```

Se abre imagen por imagen en tu visor del sistema. Responde:
- **Enter** o `k` = etiqueta correcta, mantener
- `d` = descartar (no apta — posada, otra especie, mala calidad)
- `c` = cambiar etiqueta → te pide código (BW, TV, etc.)
- `s` = skip (no estoy seguro, lo veo después)
- `q` = quit (tu progreso se guarda automáticamente)

Tiempo realista: ~3-5 segundos por imagen → **8-12 horas para 1,400 imágenes**. Hazlo en sesiones de 1h máx para no fatigar la vista. **Importante:** ten Liguori (2005, 2011) o un colega ornitólogo cerca para resolver dudas.

### 3.2 Anotador 2 (compañero/asesor)

Idealmente, un segundo anotador independiente hace el mismo proceso sobre las MISMAS imágenes:

```bash
python annotate.py --annotator carlos
```

### 3.3 Comparar y calcular Kappa

```bash
python annotate.py --compare brian carlos
```

Te dice:
- κ de Cohen (≥ 0.80 = casi perfecto, criterio del Cap. 3)
- Número y lista de discrepancias
- CSV con las imágenes en desacuerdo para tercera revisión

Si κ < 0.80, **discusión obligatoria** entre anotadores para resolver discrepancias y mejorar protocolo.

---

## Fase 4 — División estratificada train/val/test

```bash
python split_dataset.py
```

(Este script lo agregamos en la siguiente sesión si no existe — alternativa: usa los splits que crea ImageFolder automáticamente.)

Stratified 70/15/15 manteniendo proporciones por clase.

---

## Fase 5 — Entrenamiento

### Opción A — Local en RTX 3050 (4 GB VRAM)

Config ya optimizado: BATCH_SIZE=16 + AMP + gradient accumulation (efectivo 32).

```bash
# Entrenamiento real (no smoke-test)
python train.py --arch resnet50
# luego renombra: ren outputs\checkpoints\best_stage2.pt best_resnet50_stage2.pt

python train.py --arch mobilenet_v3_large
# Renombra...

# EfficientNet-B3 y ConvNeXt pueden necesitar BATCH_SIZE=8
# Edita config.py temporalmente:  BATCH_SIZE = 8
python train.py --arch efficientnet_b3
python train.py --arch convnext_tiny
```

Tiempo estimado por arquitectura: 30–60 min. Total: ~3 horas.

### Opción B — Google Colab Pro (T4 o A100)

1. Sube tu carpeta `datos/processed/` a tu Google Drive en `MyDrive/raptors-cnn-dataset/processed/`.
2. Abre `codigo/pytorch/train_colab.ipynb` en Colab.
3. Runtime → Change runtime type → GPU (T4 gratis o A100 con Pro).
4. Runtime → Run all.
5. Al terminar, baja los pesos `.pt` de tu Drive a `outputs/checkpoints/`.

Tiempo en T4: ~15 min/arch · ~1 hora total. En A100: ~5 min/arch.

---

## Fase 6 — Evaluación y comparativa

```bash
for arch in resnet50 efficientnet_b3 mobilenet_v3_large convnext_tiny:
    python evaluate.py --arch $arch --weights outputs\checkpoints\best_$arch.pt
```

Esto genera por arquitectura:
- Reporte por especie en consola
- `outputs/confusion_matrix.png`
- `outputs/roc_curves.png`

Para la comparativa estadística (McNemar + t-test pareado), corre el script de comparación (a crear en `codigo/comparacion/compare.py`).

---

## Fase 7 — Interpretabilidad (Grad-CAM)

Sobre el modelo ganador:

```bash
python gradcam.py --image datos\processed\test\Buteo_platypterus\img_001.jpg \
                  --arch resnet50 \
                  --weights outputs\checkpoints\best_resnet50.pt
```

Repite con 2-3 imágenes por especie. **Verifica que el modelo atienda al ave, NO al fondo ni al cielo.** Si atiende mal → indicador de problemas (revisar dataset o re-entrenar).

---

## Checkpoint de calidad por fase

Después de cada fase, valida antes de seguir:

| Fase | Checkpoint mínimo |
|------|-------------------|
| 1 | ≥ 150 imágenes descargadas por especie |
| 2 | ≥ 100 imágenes en `_keep` por especie |
| 3 | Kappa ≥ 0.80 entre anotadores |
| 4 | Splits balanceados (proporciones similares en train/val/test) |
| 5 | Loss decreciente en train Y val, sin overfitting catastrófico |
| 6 | Accuracy ≥ 70% en test (≥ 85% para H1 confirmada) |
| 7 | Grad-CAM atiende al individuo, no a artefactos |

Si un checkpoint falla, **NO avances** — diagnostica y arregla la fase actual.

---

## Active learning post-deployment

Cuando tengas la app Gradio corriendo con el modelo real, podrás aprovechar el módulo de **active learning**:

1. Usuarios suben fotos → modelo predice.
2. Si predice mal, usuario corrige → la corrección se guarda en `datos/feedback/`.
3. Mensual o cuando acumules ≥ 100 correcciones: corre `python retrain_with_feedback.py`.
4. Esto hace fine-tuning incremental con la nueva data → modelo se mejora con el tiempo.

Ver `documentacion/active_learning.md` para detalles.

---

## Plan B si algo se traba

| Problema | Solución |
|----------|----------|
| Pocas imágenes para una especie rara | Complementa con Macaulay Library (requiere API key Cornell) |
| GPU local insuficiente para ConvNeXt | Usar Colab Pro para esa arquitectura |
| Kappa < 0.80 entre anotadores | Sesión de calibración con guías de Liguori antes de re-anotar |
| Accuracy < 70% con dataset completo | Aumentar data augmentation, usar weighted loss, considerar más imágenes |
| Grad-CAM atiende al fondo (cielo) | Crop más ajustado al ave, aumentar augmentation de fondo |

---

*Documento vivo. Actualizar fechas y observaciones reales conforme avance el proceso.*
