# Manual de instalación — raptors-cnn

**Sistema de Identificación de Aves Rapaces por Silueta y Comportamiento de Vuelo Utilizando IA y Diseño de Lenguaje de Señas para su Comunicación y Reconocimiento.**

Este manual cubre la instalación paso a paso en Windows, Linux y macOS, con y sin tarjeta gráfica NVIDIA. Está pensado para que cualquier persona con conocimientos básicos de la línea de comandos pueda dejar el proyecto funcionando en menos de una hora.

---

## 1. ¿Qué hardware necesito?

El proyecto se entrena con redes neuronales convolucionales sobre 53 especies de rapaces mexicanas. El requisito real depende de qué quieras hacer.

| Caso de uso | RAM | Almacenamiento | GPU | Tiempo entrenamiento |
|---|---|---|---|---|
| **Solo inferencia** (usar la GUI con un modelo ya entrenado) | 4 GB | 5 GB | No requerida | n/a — 1-3 s por imagen |
| **Entrenamiento mínimo** (ResNet-50 batch 8) | 8 GB | 30 GB | GTX 1050 4 GB o equivalente | ~12 h |
| **Entrenamiento recomendado** (ResNet-50 batch 16) | 16 GB | 30 GB | RTX 3050 4 GB / RTX 2060 6 GB | ~6 h |
| **Entrenamiento avanzado** (ConvNeXt-Tiny o EfficientNet-B3) | 16 GB | 40 GB | RTX 3060 12 GB o superior | ~4 h |
| **Sin GPU** (CPU-only) | 8 GB | 30 GB | — | ~80-200 h (no recomendado) |
| **Sin GPU + Colab** (alquilar GPU gratis online) | 4 GB local | 10 GB local | T4 en Colab | ~3-5 h |

### ¿Mi GPU es suficiente?

| GPU | VRAM | ResNet-50 batch | EfficientNet-B3 batch | ConvNeXt-T batch |
|---|---|---|---|---|
| GTX 1050 / MX350 | 2 GB | 4 (lento, no recomendado) | 2 | no cabe |
| GTX 1050 Ti / 1650 / MX450 | 4 GB | 8 | 4 | 4 |
| GTX 1060 / 1660 | 6 GB | 16 | 8 | 8 |
| RTX 3050 / 2060 | 6-8 GB | **16 (default)** | 16 | 16 |
| RTX 3060 / 4060 | 12 GB | 32 | 24 | 24 |
| RTX 3090 / 4090 / A100 | 24+ GB | 64+ | 64+ | 64+ |

Si tu GPU es menor a 4 GB, edita `codigo/pytorch/config.py` y baja `BATCH_SIZE` a 4 u 8.

---

## 2. Prerrequisitos generales (todos los sistemas operativos)

Hay dos cosas que necesitas instalar antes de cualquier sistema operativo: **Miniconda** y **Git**.

### 2.1 Miniconda

Es un manejador de entornos de Python que evita conflictos entre proyectos. **NO uses pip suelto**, siempre crea entornos. Descarga el instalador desde `https://www.anaconda.com/download/success` (sección Miniconda) según tu sistema operativo. Acepta los defaults; al final asegúrate de marcar "Add Anaconda to PATH" en Windows.

Verifica con:

```bash
conda --version
```

Debería responder algo como `conda 24.x.x`.

### 2.2 Git

Para clonar el repositorio y subir cambios. Descarga desde `https://git-scm.com/downloads`. Acepta los defaults. Verifica con:

```bash
git --version
```

### 2.3 (Solo si tienes GPU NVIDIA) Drivers CUDA

NO instales el CUDA Toolkit a mano. PyTorch trae sus propias librerías CUDA bundleadas dentro del entorno conda. Solo asegúrate de tener un **driver de NVIDIA reciente** (>= 530.x para CUDA 12.1):

- **Windows:** descarga el último Game Ready Driver desde `https://www.nvidia.com/Download/index.aspx`.
- **Linux:** usa el gestor de paquetes (`sudo apt install nvidia-driver-535`) o `sudo ubuntu-drivers autoinstall`.

Verifica con:

```bash
nvidia-smi
```

Debería listar tu GPU. Si no, no hay GPU NVIDIA disponible y debes usar la instalación CPU-only.

---

## 3. Clonar el repositorio

Abre una terminal (CMD en Windows, Terminal en macOS/Linux), navega a donde quieras instalar el proyecto, y clona:

```bash
cd C:\Users\TU_USUARIO          # Windows
cd ~/Documents                   # macOS/Linux

git clone https://github.com/ZOMBIECRAFTIAN/raptors-cnn.git
cd raptors-cnn
```

**Importante en Windows:** el path completo no debe superar 260 caracteres y no debe contener tildes ni eñes. Si te aparece un error de path largo, mueve el proyecto a `C:\raptors-cnn` y vuelve a empezar.

---

## 4. Instalación según tu sistema

Salta a la sección que corresponde a tu hardware/sistema.

### 4.A Windows con GPU NVIDIA

Esta es la ruta recomendada para entrenar.

```cmd
cd C:\Users\TU_USUARIO\raptors-cnn

conda env create -f codigo\pytorch\environment.yml
conda activate raptors-pt
pip install -r codigo\pytorch\pip-requirements.txt
```

La primera línea tarda ~10-15 minutos (descarga ~3 GB).

Verifica que CUDA está detectado:

```cmd
python codigo\pytorch\verify_setup.py
```

Debe imprimir tu GPU y `torch.cuda.is_available() = True`.

### 4.B Windows sin GPU NVIDIA (CPU-only)

Útil si solo quieres probar la GUI o ejecutar inferencia.

```cmd
cd C:\Users\TU_USUARIO\raptors-cnn

conda env create -f codigo\pytorch\environment-cpu.yml
conda activate raptors-pt-cpu
pip install -r codigo\pytorch\pip-requirements.txt
```

### 4.C Linux con GPU NVIDIA

```bash
cd ~/raptors-cnn

conda env create -f codigo/pytorch/environment.yml
conda activate raptors-pt
pip install -r codigo/pytorch/pip-requirements.txt
```

### 4.D Linux sin GPU (CPU-only)

```bash
cd ~/raptors-cnn

conda env create -f codigo/pytorch/environment-cpu.yml
conda activate raptors-pt-cpu
pip install -r codigo/pytorch/pip-requirements.txt
```

### 4.E macOS Apple Silicon (M1/M2/M3/M4)

PyTorch usa MPS (Metal Performance Shaders) para acelerar con la GPU integrada del Apple Silicon. Es 3-10x más rápido que CPU pero más lento que una RTX.

```bash
cd ~/raptors-cnn

conda env create -f codigo/pytorch/environment-mps.yml
conda activate raptors-pt-mps
pip install -r codigo/pytorch/pip-requirements.txt
```

Verifica que MPS está disponible:

```bash
python -c "import torch; print('MPS disponible:', torch.backends.mps.is_available())"
```

### 4.F macOS Intel (sin Apple Silicon)

Macs Intel no tienen MPS. Usa CPU-only:

```bash
cd ~/raptors-cnn

conda env create -f codigo/pytorch/environment-cpu.yml
conda activate raptors-pt-cpu
pip install -r codigo/pytorch/pip-requirements.txt
```

---

## 5. Probar que todo funciona (smoke test, ~5 min)

Con el entorno activado:

**Windows:**

```cmd
scripts\windows\entrenar_v1_1.bat smoke
```

**Linux/macOS:**

```bash
cd codigo/pytorch
python train.py --arch resnet50 --smoke-test
```

Debe correr 1 epoch sin errores. Verás algo como:

```
Device: cuda    (o mps, o cpu)
Cargando 53 clases ...
Epoch 1/1 [stage1]   loss=2.83 acc=0.31
✓ Smoke test OK
```

Si llegaste hasta aquí, **la instalación está terminada**.

---

## 6. Descargar el dataset (6-12 horas la primera vez)

El proyecto no incluye las imágenes (pesan demasiado para git). Las descarga de iNaturalist bajo licencias Creative Commons. Necesitas internet estable.

**Windows:**

```cmd
scripts\windows\descargar_v1_1.bat
```

**Linux/macOS:**

```bash
cd codigo/pytorch
python download_inaturalist.py --target 200 --max-pages 5
```

Esto baja hasta 200 imágenes por especie (~10 600 imágenes en total, ~3 GB). Puedes dejarlo corriendo de noche y mirar el avance con:

```bash
python scripts/dataset/contar_dataset.py --por-especie
```

Si quieres reforzar especies raras (Harpia harpyja, Crested Eagle):

```cmd
scripts\windows\descargar_v1_1.bat raras
```

---

## 7. Entrenar el modelo

**Windows (pipeline automático completo, 5-10 horas):**

```cmd
scripts\windows\pipeline_completo_v1_1.bat
```

**Linux/macOS (manual):**

```bash
conda activate raptors-pt    # o raptors-pt-cpu / raptors-pt-mps según corresponda
cd codigo/pytorch
python curate.py --apply
python split_dataset.py
python exclude_empty_species.py
python train.py --arch resnet50
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

Si tu GPU es de 4 GB o menos, abre `codigo/pytorch/config.py` y cambia:

```python
BATCH_SIZE = 8    # antes 16
GRADIENT_ACCUM_STEPS = 4    # antes 2 (compensa: batch efectivo sigue siendo 32)
```

Si quieres entrenar en Google Colab (GPU gratis), abre `codigo/pytorch/train_colab.ipynb` desde colab.research.google.com → File → Upload notebook.

---

## 8. Lanzar la GUI web (Flask)

Con el modelo entrenado (o sin él, en modo demo con pesos pre-cargados):

**Cualquier sistema:**

```bash
conda activate raptors-pt          # o raptors-pt-cpu / raptors-pt-mps
cd codigo/pytorch/app_flask
python app.py
```

Abre el navegador en `http://localhost:5000`. Sube una foto de un ave rapaz y verás top-3 candidatos con Grad-CAM, ficha estilo Merlin Bird ID y video de la seña en International Sign.

Para detenerla: `Ctrl+C` en la terminal.

---

## 9. Resolución de problemas comunes

### "ModuleNotFoundError: No module named 'torch'"
Olvidaste activar el entorno conda. Corre `conda activate raptors-pt` antes de cualquier `python`.

### "CUDA out of memory"
Tu batch es muy grande para tu GPU. En `codigo/pytorch/config.py` baja `BATCH_SIZE` a 8 o 4 y aumenta `GRADIENT_ACCUM_STEPS` proporcionalmente.

### "ImageFolder found 0 files"
Te falta correr la descarga o el split. Revisa con `python scripts/dataset/contar_dataset.py`. Si hay especies en 0, usa `python codigo/pytorch/exclude_empty_species.py` que crea placeholders.

### Windows: "The system cannot find the path specified"
Tu ruta tiene tildes, eñes o pasa de 260 caracteres. Mueve el proyecto a `C:\raptors-cnn`.

### Windows: ". was unexpected at this time"
Estás corriendo un `.bat` viejo. Actualízalos con `git pull` o usa los `*_v1_1.bat` que están parser-safe.

### macOS MPS: "operator not implemented"
Algunas operaciones de PyTorch aún no están en MPS y fallan. Solución temporal: lanza con `PYTORCH_ENABLE_MPS_FALLBACK=1 python train.py --arch resnet50` para que se ejecuten en CPU automáticamente.

### Linux: "libnvinfer.so.7: cannot open shared object file"
Solo si usaste TensorRT manualmente. Ignora, no se usa en este proyecto.

### El entrenamiento es muy lento (CPU)
Es esperado. CPU entrena en 80-200 horas vs 4-8 en GPU. Opciones:
1. Sube el notebook a Google Colab (gratis, GPU T4).
2. Pide prestada una RTX por un fin de semana.
3. Renta una vps con GPU en RunPod o vast.ai (~0.20 USD/hora).

### conda tarda eternidades en "Solving environment"
Usa mamba en lugar de conda, es 10x más rápido: `conda install -n base -c conda-forge mamba` y luego `mamba env create -f ...` en lugar de `conda env create -f ...`.

---

## 10. Desinstalar

Para borrar todo limpiamente:

```bash
conda deactivate
conda env remove -n raptors-pt           # (o raptors-pt-cpu / raptors-pt-mps)
```

Y borra la carpeta del proyecto manualmente.

---

## 11. Estructura del repo (para que sepas dónde está cada cosa)

```
raptors-cnn/
├── README.md                       Documentación general
├── documentacion/guias/
│   ├── MANUAL_INSTALACION.md       Este archivo
│   ├── GUIA_COMANDOS_V1_1.txt      Comandos paso a paso
│   └── SETUP.md                    Setup resumido
├── LICENSE                          MIT
├── CITATION.cff                     Cómo citar el proyecto
│
├── codigo/pytorch/                  Implementación principal
│   ├── config.py                    Hiperparámetros centrales
│   ├── train.py                     Entrenamiento
│   ├── evaluate.py                  Métricas + matriz de confusión
│   ├── gradcam.py                   Interpretabilidad
│   ├── download_inaturalist.py      Bajada de imágenes
│   ├── curate.py                    Filtro de calidad
│   ├── split_dataset.py             70/15/15 train/val/test
│   ├── environment.yml              NVIDIA CUDA
│   ├── environment-cpu.yml          CPU-only multiplataforma
│   ├── environment-mps.yml          Apple Silicon
│   └── app_flask/                   GUI web (Flask + JS)
│
├── codigo/tensorflow/               Implementación espejo TF (opcional)
│
├── datos/
│   ├── raw/                         Imágenes recién bajadas (ignorado por git)
│   ├── processed/{train,val,test}/  Particiones (ignorado por git)
│   └── annotations/                 CSVs de etiquetado
│
├── documentacion/
│   ├── LISTA_OFICIAL_RAPACES_MEXICO.md
│   ├── tesis/                       Capítulos 1-5 en .docx
│   ├── ROADMAP_V2.md                Plan para doctorado
│   └── ...
│
├── lengua_de_senas/
│   ├── catalogo_senas/              53 fichas de señas
│   ├── glosario_IS_LSM.md           Equivalencias IS/LSM/ASL
│   └── videos/                      Grabaciones (ignorado por git)
│
├── scripts/
│   ├── windows/
│   │   ├── descargar_v1_1.bat       Atajo Windows
│   │   ├── entrenar_v1_1.bat        Atajo Windows
│   │   ├── pipeline_completo_v1_1.bat
│   │   └── commit_v1_1.bat
│   └── dataset/
│       ├── contar_dataset.py
│       ├── seleccionar_imagenes_galeria.py
│       └── selector_galeria_gui.py
```

---

## 12. Contacto

**Autor:** Brian Fernández Báez
**Email:** brianferbaez@gmail.com
**GitHub:** https://github.com/ZOMBIECRAFTIAN/raptors-cnn
**Licencia:** MIT (código) + CC-BY (datos y catálogo de señas)

Si encuentras un bug o tienes dudas, abre un *issue* en GitHub o escríbeme directamente.
