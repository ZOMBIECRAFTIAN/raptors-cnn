# Guía de Configuración del Entorno — Windows + Anaconda + NVIDIA + VS Code

Esta guía te lleva desde "tengo el repo en mi computadora" hasta "el modelo ya corrió un smoke-test y funciona". Diseñada específicamente para tu setup: **Windows con Anaconda, GPU NVIDIA y VS Code**.

Tiempo estimado: **30–60 minutos** la primera vez (la mayoría es descarga de paquetes).

---

## Paso 0 — Verificar prerequisitos

Abre **Anaconda Prompt** (búscalo en el menú Inicio) y corre:

```bash
conda --version
python --version
nvidia-smi
```

Lo que esperas ver:

- `conda 24.x` o superior.
- `Python 3.x.x` (cualquier versión, conda creará entornos con la versión que necesite).
- Una tabla de `nvidia-smi` con tu GPU, memoria y versión de driver. Si dice "command not found", instala los drivers desde [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx) (ya tienes la NVIDIA App, abre desde ahí "Drivers" → "Check for updates").

> **Driver mínimo recomendado**: 535 (para CUDA 12.1). Anota la versión que reporta `nvidia-smi`, la usaremos como referencia.

---

## Paso 1 — Crear el entorno PyTorch

Desde **Anaconda Prompt**, navega a la carpeta del proyecto:

```bash
cd /d C:\Users\hogwa\OneDrive\Documentos\raptors-cnn
```

Crea el entorno PyTorch:

```bash
conda env create -f codigo\pytorch\environment.yml
```

Esto descarga ≈ 4 GB y tarda 10–20 minutos. Cuando termine:

```bash
conda activate raptors-pt
cd codigo\pytorch
python verify_setup.py
```

Lo que esperas ver al final del script: `🎉  Entorno PyTorch listo`. Si reporta que `torch.cuda.is_available()` es `False`, repite el paso 0 (drivers) y reinstala con:

```bash
conda env remove -n raptors-pt
conda env create -f codigo\pytorch\environment.yml
```

---

## Paso 2 — Crear el entorno TensorFlow

Desactiva el entorno anterior y crea el de TensorFlow:

```bash
conda deactivate
cd ..\..\
conda env create -f codigo\tensorflow\environment.yml
conda activate raptors-tf
cd codigo\tensorflow
python verify_setup.py
```

Otra vez: ≈ 3 GB y 10–20 minutos. Esperas ver `🎉  Entorno TensorFlow listo`.

> **Nota:** TensorFlow ≥ 2.11 ya no incluye soporte CUDA nativo en Windows. La línea `tensorflow[and-cuda]` del `environment.yml` lo resuelve descargando las librerías CUDA empaquetadas. Si por alguna razón la GPU no es detectada por TensorFlow (pero sí por PyTorch), una alternativa válida es usar **WSL2 con Ubuntu**, donde TensorFlow GPU es más estable. Avísame si te sucede y te guío.

---

## Paso 3 — Configurar VS Code

1. Abre VS Code.
2. `File > Open Folder...` → selecciona la carpeta del proyecto (la del nombre largo).
3. Cuando VS Code muestre el aviso "This workspace has extension recommendations", presiona **Install**. Esto instala automáticamente:
   - Python + Pylance (autocompletado, lint)
   - Ruff y Black (formato y lint)
   - Jupyter (notebooks)
   - YAML, Markdown, PDF viewer, Python Environment Manager
4. Cambia el intérprete:
   - Abre cualquier `.py` dentro de `codigo/pytorch/`.
   - Esquina inferior derecha: clic en la versión de Python actual.
   - Selecciona **`Python 3.11.x ('raptors-pt')`**.
   - Repite para `codigo/tensorflow/` eligiendo **`raptors-tf`**.
5. Abre la terminal integrada (Ctrl + ñ o Ctrl + `). VS Code activará automáticamente el entorno conda correspondiente al archivo abierto.

> Puedes correr cualquier archivo de prueba con **F5** — ya dejé configuradas en `.vscode/launch.json` cuatro entradas listas para depurar.

---

## Paso 4 — Generar el dataset sintético y correr un smoke-test

Esto te valida que TODO el pipeline funciona, sin necesidad de tener aún imágenes reales de rapaces.

```bash
conda activate raptors-pt
cd codigo\pytorch
python make_synthetic_dataset.py            # crea ~70 imágenes × 14 especies
python train.py --arch resnet50 --smoke-test
```

Esperas ver al final del entrenamiento algo como:

```
[stage1] epoch 001/001  train_loss=2.6418 train_acc=0.1142  val_loss=2.5810 val_acc=0.2143  (15.2s)
[stage2] epoch 001/001  train_loss=2.5012 train_acc=0.1888  val_loss=2.4108 val_acc=0.2786  (28.4s)

Mejor accuracy en validación (etapa 2): 0.2786
Pesos guardados en: ...\outputs\checkpoints\best_stage2.pt
```

Los números no son significativos (es ruido sintético), pero **el pipeline ha corrido end-to-end**: carga, augmentation, modelo, train, validación, checkpointing. Si llegas aquí sin error, todo el código del proyecto está sano y listo para recibir el dataset real.

Repite el paso para TensorFlow:

```bash
conda deactivate
conda activate raptors-tf
cd ..\tensorflow
python make_synthetic_dataset.py
python train.py --arch resnet50 --smoke-test
```

---

## Paso 5 — Verificar que todo funciona con la matriz de confusión

```bash
# Aún en raptors-pt:
cd ..\pytorch
python evaluate.py --arch resnet50 --weights outputs\checkpoints\best_stage2.pt
```

Genera `outputs\confusion_matrix.png` y `outputs\roc_curves.png`. Ábrelos para ver que las figuras se generan correctamente (otra vez: los números no significan nada con dataset sintético).

---

## Resumen de comandos de uso diario

Una vez todo está configurado, tu rutina típica de trabajo será:

```bash
# Abrir VS Code en el proyecto, terminal integrada activa el entorno

# Trabajar con PyTorch
conda activate raptors-pt
cd codigo\pytorch
python train.py --arch resnet50           # entrenamiento real (cuando tengas el dataset)
python evaluate.py --weights outputs\checkpoints\best_stage2.pt --arch resnet50
python gradcam.py --image ruta\a\foto.jpg --weights outputs\checkpoints\best_stage2.pt

# Cambiar a TensorFlow
conda deactivate
conda activate raptors-tf
cd ..\tensorflow
python train.py --arch resnet50
```

---

## Próximos pasos del proyecto

Ahora que el entorno está listo, las siguientes piezas que faltan para entrenar el modelo real son:

1. **Recolectar las imágenes reales** de las 14 especies (Macaulay Library + iNaturalist + Pronatura + propias) — sigue el Capítulo 3, sección 3.3.
2. **Etiquetar y validar** con dos anotadores (kappa de Cohen ≥ 0.80).
3. **Borrar el dataset sintético** de `datos\processed\` y reemplazarlo por el real.
4. **Correr el entrenamiento real** sin `--smoke-test`.

El código ya está listo para todo eso. Cuando llegues a esa fase, dime y te ayudo con el script de descarga desde iNaturalist con licencias filtradas.

---

## Solución de problemas comunes

**Problema:** `nvidia-smi` no funciona o `torch.cuda.is_available()` es `False`.
**Solución:** actualizar drivers NVIDIA desde la NVIDIA App. Reiniciar la PC. Volver a verificar.

**Problema:** la creación del entorno se queda colgada en "Solving environment".
**Solución:** instalar primero `mamba` (`conda install -n base -c conda-forge mamba`) y reemplazar `conda env create` por `mamba env create`. Es 5-10 veces más rápido.

**Problema:** `train.py` falla con `Out of memory`.
**Solución:** reducir `BATCH_SIZE` en `config.py` (de 32 a 16 u 8). En GPUs de 8 GB ó menos, usar `MobileNetV3-Large` que es la arquitectura más ligera.

**Problema:** TensorFlow no detecta la GPU pero PyTorch sí.
**Solución:** instalar WSL2 con Ubuntu y crear el entorno raptors-tf adentro. `tensorflow[and-cuda]` funciona impecable en Linux.

**Problema:** VS Code no aparece el intérprete `raptors-pt`.
**Solución:** `Ctrl+Shift+P` → "Python: Clear Cache and Reload Window". O reiniciar VS Code después de instalar la extensión Python.
