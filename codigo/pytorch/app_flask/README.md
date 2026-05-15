# Flask Web App — raptors-cnn

App Flask profesional adaptada de [raptor_australia](C:\Projects\raptor_australia). Look estilo SaaS con hero drag-drop, banner colorizado por especie, top-3 con barras de progreso, info detallada estilo Merlin Bird ID, y active learning.

## Estructura

```
app_flask/
├── app.py                    Backend Flask con inferencia + endpoints
├── species_data.py           Perfiles enriquecidos de las 23 especies
├── i18n.py                   Sistema de internacionalización (es + en)
├── translations/
│   ├── es.json               Traducciones español
│   └── en.json               Traducciones inglés
├── templates/
│   ├── base.html             Layout base con topbar + footer
│   ├── index.html            Página principal (hero + resultado)
│   ├── species.html          Catálogo de las 23 especies
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
| Info Merlin-style (distribución, dieta, did-you-know) | ❌ | ✅ |
| Alerta de baja confianza | ❌ | ✅ |
| Multilenguaje (es+en) | ❌ | ✅ |
| Active learning con dropdown | ✅ | ✅ |
| Darwin Core export | parcial | ✅ |
| Tarjetas de especies (catálogo) | ✅ | ✅ con CSS pro |
| Hot-reload en dev | ✅ | ✅ (`debug=True`) |

## Próximos pasos

- Agregar imágenes hero por especie (pendiente: `pick_hero_images.py` adaptado)
- Grabar videos reales de señas con la comunidad sorda
- Producción: gunicorn + Docker
- Más idiomas (fr, pt, etc.)
