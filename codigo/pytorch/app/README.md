# App Gradio — raptors-cnn

Interfaz web para identificar aves rapaces a partir de imágenes o videos, con catálogo
integrado de señas en International Sign.

## Estructura

```
app/
├── __init__.py
├── main.py              # Entry point — Gradio Blocks con 4 tabs
├── config_app.py        # Constantes y datos enriquecidos de cada especie
├── inference.py         # Singleton del clasificador + Grad-CAM
├── video_processor.py   # Procesamiento frame-by-frame de video
└── signs.py             # Placeholders SVG de las señas (mientras se graban videos)
```

## Requisitos

Además del entorno `raptors-pt` ya configurado, necesitas:

```bash
conda activate raptors-pt
pip install gradio>=4.0 opencv-python-headless
```

(Ya están incluidos en el `environment.yml` / `pip-requirements.txt` si lo actualizas.)

## Uso

Desde `codigo/pytorch/`:

```bash
python -m app.main
```

Esto abre `http://127.0.0.1:7860` en tu navegador.

> **Importante:** la app espera un modelo entrenado en
> `codigo/pytorch/outputs/checkpoints/best_stage2.pt`. Si no existe, ejecuta primero
> el smoke-test: `python train.py --arch resnet50 --smoke-test`.

## Tabs

### 1. 📷 Identificar imagen
- Sube un JPG/PNG
- Modelo predice especie con probabilidad top-5
- Genera Grad-CAM mostrando "dónde mira" el modelo
- Muestra la tarjeta de la seña correspondiente

### 2. 📹 Identificar video
- Sube MP4 de máx 60s
- Sliders configurables: cada cuántos segundos muestrear + umbral de confianza
- Devuelve timeline visual de detecciones + tabla cronológica
- Muestra la seña de la mejor detección

### 3. 🤟 Catálogo de señas IS
- 14 botones (uno por especie)
- Clic → muestra la tarjeta SVG de la seña + ficha técnica completa

### 4. ℹ️ Acerca de
- Metadatos del proyecto, licencias, contacto

## Reemplazo de placeholders por videos reales

Las "tarjetas" SVG actuales son placeholders. Cuando se graben los videos reales con la
comunidad sorda, colócalos en:

```
lengua_de_senas/videos/<CODIGO>_<scientific_name>.mp4
```

Ej.: `lengua_de_senas/videos/TV_Cathartes_aura.mp4`

La función `get_sign_for_species()` en `signs.py` los detectará automáticamente y los
mostrará en lugar del placeholder.

## Despliegue público (opcional)

Para compartir online a tus compañeros con un link público temporal:

```python
# En main.py, cambia:
demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True, share=False)
# por:
demo.launch(share=True)
```

Para hosting permanente gratuito, sube a **HuggingFace Spaces**:
[huggingface.co/spaces](https://huggingface.co/spaces) → New Space → Gradio → SDK Gradio.
