# Flask Web App — raptors-cnn

App Flask profesional adaptada de [raptor_australia](C:\Projects\raptor_australia). Look estilo SaaS con hero drag-drop, banner colorizado por especie, top-3 con barras de progreso, info detallada estilo Merlin Bird ID, y active learning.

## Estructura

```
app_flask/
├── app.py                    Backend Flask con inferencia + endpoints CNN/YOLO
├── species_data.py           Perfiles enriquecidos de las 53 especies
├── i18n.py                   Sistema de internacionalización (es + en)
├── translations/
│   ├── es.json               Traducciones español
│   └── en.json               Traducciones inglés
├── templates/
│   ├── base.html             Layout base con topbar + footer
│   ├── index.html            Página principal (hero + resultado)
│   ├── species.html          Catálogo de las 53 especies
│   └── data.html             Dashboard de observaciones + descargas
├── static/
│   ├── css/style.css         Stylesheet (Inter + Lora, paleta teal/terracotta)
│   └── js/main.js            Frontend logic (upload, predicción, feedback)
└── uploads/                  Imágenes subidas por el usuario (efímeras)
```

## Cómo correrla

```cmd
conda activate raptors-pt
cd C:\Users\hogwa\raptors-cnn\codigo\pytorch\app_flask
python app.py
```

Abre <http://127.0.0.1:5000>.

> **Requiere:** modelo entrenado en `codigo/pytorch/outputs/checkpoints/best_stage2.pt`. Si no existe, corre primero `python train.py --smoke-test`.

## Características vs. Gradio actual

| Feature | Gradio actual | Flask nuevo |
|---------|---------------|-------------|
| Hero con drag-drop | ❌ | ✅ |
| Banner colorizado por especie | ❌ | ✅ |
| Top-3 con barras de progreso | ❌ | ✅ |
| Video YOLO + tracking | ❌ | ✅ |
| Info Merlin-style (distribución, dieta, did-you-know) | ❌ | ✅ |
| Alerta de baja confianza | ❌ | ✅ |
| Multilenguaje (es+en) | ❌ | ✅ |
| Active learning con dropdown | ✅ | ✅ |
| Darwin Core export | parcial | ✅ |
| Tarjetas de especies (catálogo) | ✅ | ✅ con CSS pro |
| Hot-reload en dev | ✅ | ✅ (`debug=True`) |

## Próximos pasos

- Agregar imágenes hero por especie (pendiente: `pick_hero_images.py` adaptado)
- Entrenar detector YOLO propio con cajas anotadas de rapaces mexicanas
- Grabar videos reales de señas con la comunidad sorda
- Producción: gunicorn + Docker
- Más idiomas (fr, pt, etc.)

## Video con YOLO

La subida de video llama a `/identify_video`. El backend usa:

1. `ultralytics.YOLO` para detectar aves.
2. Tracking por IoU para asignar `track_id` por individuo.
3. La CNN de 53 clases para clasificar cada recorte detectado.
4. Heurísticas de movimiento para resumir comportamiento de vuelo.

Instalación opcional:

```cmd
conda activate raptors-pt
cd C:\Users\hogwa\raptors-cnn\codigo\pytorch
pip install -r requirements-yolo.txt
```

Pesos YOLO:

- Si existe `RAPTORS_YOLO_WEIGHTS`, se usa esa ruta.
- Si existe `codigo/pytorch/outputs/yolo/checkpoints/best.pt`, se usa ese detector propio.
- Si no, se usa `yolov8n.pt` como detector COCO de clase `bird`.

Para defensa academica, ver `documentacion/YOLO_VIDEO_MODULE.md`: YOLO se
presenta como modulo complementario de deteccion/tracking/video, mientras que
la CNN conserva la responsabilidad de clasificar las 53 especies.
