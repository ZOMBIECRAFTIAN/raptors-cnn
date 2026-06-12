# Validacion cientifica del proyecto

Este documento separa resultados preliminares de resultados defendibles para
tesis. Su proposito es evitar afirmaciones infladas y dejar claro que el
proyecto sigue un protocolo reproducible.

## 1. Estado de las metricas actuales

Las metricas ResNet-50 existentes son **preliminares** porque fueron generadas
sobre un split por imagen. En el dataset actual, varios archivos siguen el
patron `<observationID>_<photoID>` y multiples fotos de la misma observacion
pueden caer en train, val y test al mismo tiempo.

Interpretacion correcta:

- Sirven como baseline tecnico inicial.
- No deben presentarse como estimacion final de generalizacion.
- Deben repetirse despues de regenerar `datos/processed/` con split agrupado
  por `observationID`.

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

El resultado esperado puede bajar respecto al split por imagen. Eso es normal:
la metrica nueva es mas honesta y mas defendible.

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

> Las metricas actuales son preliminares y se generaron con split por imagen.
> Durante la auditoria detectamos posible fuga por observacion, por lo que el
> protocolo final usa split agrupado por `observationID`, auditoria automatica
> del dataset y reentrenamiento antes de reportar resultados finales.
