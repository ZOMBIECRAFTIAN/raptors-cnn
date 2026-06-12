# Validacion cientifica del proyecto

Este documento separa resultados preliminares de resultados defendibles para
tesis. Su proposito es evitar afirmaciones infladas y dejar claro que el
proyecto sigue un protocolo reproducible.

## 1. Estado de las metricas actuales

ResNet-50 ya fue reentrenado y evaluado con el protocolo defendible por
`observationID`. La auditoria del dataset reporta 0 fugas de observacion entre
train, validacion y test.

Resultado local del 2026-06-12:

| Metrica | Valor |
|---|---:|
| Imagenes de prueba | 2,653 |
| Accuracy | 0.6072 |
| Accuracy IC 95% | 0.5895-0.6246 |
| Balanced accuracy | 0.5808 |
| F1-macro | 0.5837 |
| F1-macro IC 95% | 0.5594-0.6009 |
| Top-3 accuracy | 0.6958 |
| Macro-AUC | 0.9226 |
| Cohen's kappa | 0.5969 |

Interpretacion correcta:

- Estos numeros son mas defendibles que el baseline anterior por imagen.
- Las especies con soporte muy bajo siguen sin ser concluyentes por especie.
- El benchmark de otras arquitecturas queda pendiente y no debe inferirse desde
  ResNet-50.

## 2. Split recomendado para tesis

El split defendible es por observacion:

```bash
cd codigo/pytorch
python split_dataset.py --group-by-observation --clean --link
python audit_dataset.py --fail-on-leak
```

Si se desea conservar el split anterior para comparacion historica:

```bash
python split_dataset.py --group-by-observation --processed-dir ../../datos/processed_grouped --clean --link
python audit_dataset.py --processed-dir ../../datos/processed_grouped --fail-on-leak
```

Luego se reentrena:

```bash
python train.py --arch resnet50 --split-protocol observation
python evaluate.py --arch resnet50 \
  --weights outputs/checkpoints/best_stage2_resnet50.pt \
  --split-protocol observation
```

El resultado puede diferir respecto al split por imagen. Eso es normal: la
metrica agrupada por observacion es mas honesta y mas defendible.

## 3. Auditoria obligatoria antes de reportar

Antes de entrenar o publicar resultados:

```bash
python audit_dataset.py --check-images
```

La auditoria revisa:

- conteos por especie y split;
- fuga de `observationID` entre train/val/test;
- especies con soporte bajo;
- archivos no soportados en `datos/processed`;
- GIFs en `datos/raw`;
- imagenes corruptas si se usa `--check-images`.

## 4. Especies raras

Para especies con `train < 50`, `val < 10` o `test < 10`, la metrica por
especie es inestable. En defensa academica se deben reportar como clases de
soporte bajo, no como fallas definitivas del modelo.

Estrategias aceptables:

- recolectar datos dirigidos para especies raras;
- reportar resultados por familia taxonomica ademas de por especie;
- usar un clasificador jerarquico familia -> genero -> especie;
- mantener top-3 accuracy como metrica ecologicamente realista.

## 5. Arquitecturas y frameworks

PyTorch es la implementacion principal. TensorFlow es una implementacion espejo
parcial y no debe presentarse todavia como comparacion experimental equivalente,
porque no comparte todo el protocolo de entrenamiento avanzado.

El benchmark de arquitecturas solo se considera completo cuando cada backbone
tenga:

- checkpoint identificado por arquitectura;
- `metrics_<arch>.json`;
- reporte de clasificacion;
- matriz de confusion;
- latencia y tamano de modelo;
- manifiesto de entrenamiento/evaluacion.

## 6. YOLO y comportamiento

YOLO esta implementado como prototipo funcional para detectar y seguir aves en
video. No es todavia un resultado final validado de comportamiento.

Para defenderlo como modulo cientifico se requiere:

- cajas anotadas;
- mAP50 y mAP50-95;
- evaluacion de tracking;
- etiquetas temporales de comportamiento;
- comparacion contra baseline.

## 7. Frase recomendada para defensa

> Las metricas actuales de ResNet-50 ya fueron regeneradas con split agrupado
> por `observationID` y auditoria automatica sin fuga entre train, validacion y
> test. Aun asi, las especies raras se reportan con cautela porque algunas
> tienen menos de 10 imagenes de prueba.
