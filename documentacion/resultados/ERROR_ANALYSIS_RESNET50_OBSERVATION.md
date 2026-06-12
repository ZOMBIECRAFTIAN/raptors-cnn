# Error analysis: ResNet-50 observation-level run

Run date: 2026-06-12  
Checkpoint: `codigo/pytorch/outputs/checkpoints/best_stage2_resnet50.pt`  
Metrics file: `codigo/pytorch/outputs/metrics_resnet50.json`  
Protocol: 53 species, stratified split grouped by `observationID`

## Headline result

| Metric | Value |
|---|---:|
| Test images | 2,653 |
| Accuracy | 0.6072 |
| Accuracy 95% CI | 0.5895-0.6246 |
| Balanced accuracy | 0.5808 |
| F1-macro | 0.5837 |
| F1-macro 95% CI | 0.5594-0.6009 |
| F1-weighted | 0.6133 |
| Top-3 accuracy | 0.6958 |
| Macro-AUC | 0.9226 |
| Cohen's kappa | 0.5969 |
| Latency | 19.08 ms/image |
| Model size | 90.40 MB |

Dataset audit: train=12,261, val=2,609, test=2,653, observation leakage=0.

## Strongest species

| Species | F1 | Test support |
|---|---:|---:|
| *Falco rufigularis* | 0.8780 | 41 |
| *Busarellus nigricollis* | 0.8632 | 48 |
| *Falco sparverius* | 0.8261 | 110 |
| *Herpetotheres cachinnans* | 0.8247 | 52 |
| *Elanus leucurus* | 0.7945 | 40 |

Interpretation: the model performs best where the species have distinctive
shape, posture, or enough representative examples in the observation-level
split.

## Weakest species

| Species | F1 | Test support | Primary interpretation |
|---|---:|---:|---|
| *Buteogallus solitarius* | 0.0000 | 4 | Very low support; do not over-interpret species-level F1. |
| *Morphnus guianensis* | 0.0000 | 5 | Very low support; needs targeted data collection. |
| *Ictinia plumbea* | 0.2308 | 39 | Mostly confused with *Ictinia mississippiensis*. |
| *Astur atricapillus* | 0.2388 | 46 | Confused with accipiter/falcon-shaped silhouettes. |
| *Buteo platypterus* | 0.3117 | 87 | Confused with other broad-winged Buteo silhouettes. |

## Main confusion pairs

| True species | Predicted species | Count | Biological reading |
|---|---|---:|---|
| *Ictinia plumbea* | *Ictinia mississippiensis* | 27 | Same genus; expected silhouette similarity. |
| *Accipiter striatus* | *Astur cooperii* | 20 | Classic field-identification pair. |
| *Astur cooperii* | *Accipiter striatus* | 17 | Reciprocal small/medium accipiter confusion. |
| *Buteo jamaicensis* | *Buteo platypterus* | 15 | Buteo silhouette overlap. |
| *Buteo jamaicensis* | *Buteo lineatus* | 15 | Broad Buteo confusion. |
| *Buteo platypterus* | *Buteo lineatus* | 12 | Similar soaring/perched image bias. |
| *Buteogallus urubitinga* | *Buteogallus anthracinus* | 12 | Same genus; expected confusion cluster. |

## Family-level reading

| Family | Accuracy | Support |
|---|---:|---:|
| Pandionidae | 0.8137 | 102 |
| Falconidae | 0.7540 | 569 |
| Cathartidae | 0.6565 | 230 |
| Accipitridae | 0.5411 | 1,752 |

Accipitridae is the hardest group because it contains most classes and many
look-alike genera. This supports reporting both species-level and family-level
metrics.

## Defense notes in Spanish

- El resultado ya no usa un split por imagen: usa `observationID`, por lo que
  no hay fuga directa del mismo avistamiento entre entrenamiento y prueba.
- Las clases raras no deben venderse como "resueltas". En especies con 4 o 5
  imagenes de prueba, el F1 por especie es inestable y exige recoleccion
  dirigida.
- Los errores principales son biologicamente plausibles: muchos ocurren dentro
  del mismo genero o entre pares que tambien confunden a observadores humanos.
- El top-3 accuracy es importante en campo: una herramienta de apoyo puede
  mostrar candidatos probables, no reemplazar el juicio experto.

## Recommended next data actions

1. Target new data for *Buteogallus solitarius* and *Morphnus guianensis*.
2. Add more difficult backgrounds for *Spizaetus*, *Harpagus*, forest-falcons
   and tropical canopy species.
3. Use Grad-CAM audits to remove images where the model attends to background
   rather than the bird.
4. Keep the YOLO video module separated from the species classifier until
   bounding boxes and temporal behaviour labels are validated.
