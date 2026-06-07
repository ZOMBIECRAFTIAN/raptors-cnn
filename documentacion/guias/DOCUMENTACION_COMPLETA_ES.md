# Documentacion completa del proyecto raptors-cnn

**Proyecto:** raptors-cnn  
**Autor:** Brian Fernandez Baez  
**Tipo:** propuesta/prototipo de investigacion de maestria  
**Version documentada:** estructura actual del repositorio despues de la reorganizacion  

---

## 1. Que es este documento

El archivo `README_ES.md` es la portada informativa del proyecto para GitHub: explica el objetivo, el problema cientifico, la metodologia general, como instalar y como ejecutar.

Este documento es mas tecnico y completo. Sirve para responder: donde esta cada cosa, que hace cada carpeta, que hace cada archivo importante, como se entrena el modelo, como se evalua, donde vive la interfaz Flask y que partes estan en desarrollo.

---

## 2. Objetivo del proyecto

`raptors-cnn` busca construir una herramienta de vision por computadora para identificar rapaces diurnas de Mexico a partir de imagenes y, posteriormente, video.

El objetivo academico es disenar, construir y evaluar un pipeline reproducible de inteligencia artificial que:

- identifique 53 especies de rapaces diurnas de Mexico;
- use aprendizaje profundo con CNN y transfer learning;
- favorezca rasgos de silueta y forma, no solo color de plumaje;
- compare varias arquitecturas bajo el mismo protocolo;
- evalue el modelo con metricas cuantitativas e interpretabilidad;
- entregue una interfaz web usable para demostracion y captura de observaciones.

---

## 3. Que problema busca resolver

La identificacion de rapaces en campo es dificil porque muchas veces el ave:

- esta lejos;
- aparece contra cielo brillante;
- se ve como silueta;
- no muestra color real del plumaje;
- cambia de forma segun postura, vuelo y angulo.

Un contador de aves, naturalista o aficionado no siempre puede detenerse a revisar una guia de campo completa. El proyecto intenta apoyar esa decision con una herramienta que proponga candidatos probables y muestre informacion biologica asociada.

---

## 4. Para quien sirve

El proyecto puede pensarse como una herramienta para:

- contadores de aves en monitoreos migratorios;
- naturalistas de campo;
- estudiantes de biologia, ecologia o conservacion;
- usuarios de ciencia ciudadana;
- personas que quieren aprender a diferenciar rapaces;
- investigadores que necesitan un pipeline reproducible de clasificacion visual.

No debe presentarse como reemplazo de un ornitologo experto. Es un asistente de identificacion y una base de investigacion.

---

## 5. Diferencia frente a Merlin Bird ID

Merlin Bird ID es una herramienta muy fuerte, generalista y cerrada. Este proyecto se diferencia en:

| Aspecto | Merlin Bird ID | raptors-cnn |
|---|---|---|
| Alcance | Muchas aves y regiones | Enfoque en 53 rapaces diurnas de Mexico |
| Codigo | Cerrado | Abierto y revisable |
| Enfoque | Identificacion general por foto/audio | Silueta, forma y comportamiento de vuelo |
| Reproducibilidad | No expone todo el pipeline | Scripts, datos esperados, entrenamiento y evaluacion documentados |
| Investigacion | Producto terminado | Prototipo academico en desarrollo |
| Video/comportamiento | No es el foco principal de Merlin | Prototipo YOLO implementado para deteccion, tracking y comportamiento heuristico |
| Interpretabilidad | No expuesta al usuario | Grad-CAM para revisar donde mira el modelo |

La idea central no es competir con Merlin por escala, sino demostrar un enfoque especializado, abierto y academico para rapaces en vuelo.

---

## 6. Estructura general del repositorio

```text
raptors-cnn/
├── README.md / README_ES.md        Portada publica del proyecto
├── codigo/                         Codigo fuente de modelos e interfaces
├── datos/                          Dataset local, anotaciones y videos futuros
├── documentacion/                  Documentos academicos, guias y resultados
├── lengua_de_senas/                Entregable secundario de accesibilidad
├── referencias/                    Bibliografia y plantillas
├── scripts/                        Utilidades de Windows y dataset
├── .gitignore                      Reglas para no subir datos pesados o secretos
├── .env.example                    Ejemplo de variables de entorno
├── CITATION.cff                    Metadata para citar el proyecto
├── CONTRIBUTING.md                 Guia de contribucion
└── LICENSE                         Licencia del codigo
```

---

## 7. Archivos de la raiz

| Archivo | Funcion |
|---|---|
| `README.md` | Portada principal en ingles para GitHub. |
| `README_ES.md` | Portada principal en espanol. Es la mejor entrada para explicar el proyecto. |
| `.gitignore` | Evita subir datasets, videos pesados, pesos entrenados, caches, `.env` y uploads. |
| `.gitattributes` | Configuracion de Git para manejo de archivos y formatos. |
| `.env` | Variables locales. No debe subirse a GitHub. |
| `.env.example` | Plantilla segura para que otra persona cree su `.env`. |
| `CITATION.cff` | Informacion academica para citar el proyecto. |
| `CONTRIBUTING.md` | Reglas para colaborar: codigo, datos, documentacion y lengua de senas. |
| `LICENSE` | Licencia del codigo. |

---

## 8. Carpeta `codigo/`

Contiene el codigo fuente. Esta dividida en tres partes:

| Carpeta | Funcion |
|---|---|
| `codigo/pytorch/` | Implementacion principal del proyecto. Aqui se entrena y evalua el modelo. |
| `codigo/tensorflow/` | Implementacion espejo/alternativa en TensorFlow. Es secundaria. |
| `codigo/comparacion/` | Scripts y resultados para comparar arquitecturas. |

---

## 9. Carpeta `codigo/pytorch/`

Es el corazon del proyecto. Aqui esta el pipeline principal.

| Archivo/carpeta | Que hace |
|---|---|
| `config.py` | Define rutas, especies, codigos, nombres comunes, clases, batch size, epochs y etapas de entrenamiento. |
| `data_loader.py` | Carga `datos/processed/train`, `val` y `test` con `ImageFolder`; aplica augmentations y normalizacion. |
| `model.py` | Construye las arquitecturas CNN: ResNet-50, EfficientNet-B3, MobileNetV3-Large y ConvNeXt-Tiny. |
| `train.py` | Entrena el modelo en dos etapas: feature extraction y fine-tuning. |
| `evaluate.py` | Evalua el checkpoint en test; genera reporte, matriz de confusion y curvas ROC. |
| `gradcam.py` | Genera mapas Grad-CAM para revisar si el modelo mira al ave y no al fondo. |
| `curate.py` | Filtra/califica imagenes por resolucion, nitidez, brillo y duplicados. |
| `split_dataset.py` | Divide datos en train/val/test con proporcion 70/15/15. |
| `download_inaturalist.py` | Descarga imagenes desde iNaturalist. |
| `download_ebird.py` | Descarga o prepara metadatos relacionados con eBird. |
| `annotate.py` | Soporte para anotacion/revision y calculo de acuerdo entre anotadores. |
| `exclude_empty_species.py` | Maneja especies con pocos datos o carpetas vacias. |
| `make_synthetic_dataset.py` | Crea un dataset sintetico para pruebas rapidas. |
| `retrain_with_feedback.py` | Permite reentrenar usando correcciones acumuladas de usuarios. |
| `verify_setup.py` | Verifica que Python, PyTorch y dependencias funcionen. |
| `train_colab.ipynb` | Notebook para entrenamiento en Google Colab. |
| `environment.yml` | Entorno Conda para GPU NVIDIA/CUDA. |
| `environment-cpu.yml` | Entorno Conda para CPU. |
| `environment-mps.yml` | Entorno Conda para Apple Silicon/MPS. |
| `pip-requirements.txt` / `requirements.txt` | Dependencias instalables con pip. |
| `outputs/` | Salidas generadas: checkpoints, matrices, curvas, Grad-CAM. No es la fuente del proyecto. |
| `app/` | App/prototipo alternativo anterior. |
| `app_flask/` | Interfaz web principal en Flask. |

---

## 10. Donde se entrenan los modelos

El entrenamiento principal ocurre en:

```text
codigo/pytorch/train.py
```

Comando tipico:

```bash
cd codigo/pytorch
python train.py --arch resnet50
```

Comando de prueba rapida:

```bash
cd codigo/pytorch
python train.py --arch resnet50 --smoke-test
```

Arquitecturas soportadas:

- `resnet50`
- `efficientnet_b3`
- `mobilenet_v3_large`
- `convnext_tiny`

Los pesos entrenados se guardan en:

```text
codigo/pytorch/outputs/checkpoints/
```

Los checkpoints esperados son:

```text
best_stage1.pt
best_stage2.pt
```

La interfaz Flask intenta cargar:

```text
codigo/pytorch/outputs/checkpoints/best_stage2.pt
```

---

## 11. Como se entrena el modelo

El entrenamiento usa transfer learning en dos etapas:

1. **Stage 1 / feature extraction**  
   El backbone preentrenado queda congelado y se entrena principalmente la cabeza clasificadora.

2. **Stage 2 / fine-tuning**  
   Se descongela el modelo completo y se ajustan los pesos con una tasa de aprendizaje menor.

Parametros importantes:

| Parametro | Donde esta | Funcion |
|---|---|---|
| `SPECIES` | `config.py` | Lista oficial de 53 especies. |
| `NUM_CLASSES` | `config.py` | Numero de clases. |
| `BATCH_SIZE` | `config.py` | Tamano de lote. |
| `USE_AMP` | `config.py` | Usa mixed precision cuando hay GPU compatible. |
| `GRADIENT_ACCUM_STEPS` | `config.py` | Simula un batch efectivo mayor. |
| `STAGE1` | `config.py` | Configuracion de la primera etapa. |
| `STAGE2` | `config.py` | Configuracion de fine-tuning. |

---

## 12. Donde esta el dataset

El proyecto espera los datos en:

```text
datos/
├── raw/                         imagenes originales descargadas
├── processed/
│   ├── train/                   entrenamiento
│   ├── val/                     validacion
│   └── test/                    prueba final
├── annotations/                 metadatos y reportes CSV
├── feedback/                    correcciones/feedback de usuarios
└── videos/                      videos para el modulo futuro de comportamiento
```

Los datos pesados no deben subirse a GitHub. Por eso `datos/raw/`, `datos/processed/` y videos reales estan ignorados.

---

## 13. Como se evalua la eficiencia del modelo

La evaluacion principal esta en:

```text
codigo/pytorch/evaluate.py
```

Comando:

```bash
cd codigo/pytorch
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

Evalua:

- accuracy;
- reporte por clase;
- precision, recall y F1;
- matriz de confusion;
- curvas ROC;
- comportamiento del modelo en el conjunto `test`.

Salidas esperadas:

```text
codigo/pytorch/outputs/confusion_matrix.png
codigo/pytorch/outputs/roc_curves.png
```

La comparacion entre arquitecturas esta en:

```text
codigo/comparacion/comparar_arquitecturas.py
codigo/comparacion/README.md
```

Esa comparacion considera:

- accuracy;
- F1-macro;
- top-3 accuracy;
- tiempo de entrenamiento;
- latencia de inferencia;
- tamano del modelo;
- graficas de trade-off.

---

## 14. Donde se genera la interfaz Flask

La interfaz principal vive en:

```text
codigo/pytorch/app_flask/
```

Archivos principales:

| Archivo/carpeta | Funcion |
|---|---|
| `app.py` | Backend Flask: carga modelo, rutas web, inferencia, feedback y exportaciones. |
| `templates/base.html` | Plantilla base comun. |
| `templates/index.html` | Pantalla principal para subir imagen/video y ver resultados. |
| `templates/species.html` | Guia de especies. |
| `templates/data.html` | Panel de datos/exportaciones. |
| `static/css/style.css` | Estilos visuales de la interfaz. |
| `static/js/main.js` | JavaScript del frontend: carga imagen, llama `/identify` y muestra resultados. |
| `translations/es.json` | Textos de interfaz en espanol. |
| `translations/en.json` | Textos de interfaz en ingles. |
| `species_info.py` | Informacion resumida por especie. |
| `species_data.py` | Fichas biologicas extensas en espanol/base. |
| `species_data_en.py` | Fichas biologicas en ingles. |
| `uploads/` | Archivos temporales subidos por usuarios. No debe subirse a GitHub. |

Comando para correr:

```bash
cd C:\Users\hogwa\raptors-cnn
conda activate raptors-pt
cd codigo\pytorch\app_flask
python app.py
```

URL:

```text
http://localhost:5000
```

---

## 15. Rutas principales de Flask

| Ruta | Funcion |
|---|---|
| `/` | Pagina principal. |
| `/identify` | Recibe imagen y devuelve prediccion top-3. |
| `/identify_video` | Analisis de video con YOLO, tracking IoU, CNN por recorte y comportamiento heuristico. |
| `/species` | Guia de especies. |
| `/data` | Panel de datos y observaciones. |
| `/feedback` | Guarda correcciones de usuario. |
| `/feedback_stats` | Muestra conteo de feedback acumulado. |
| `/save_observation` | Guarda observaciones con metadatos. |
| `/export/observations.csv` | Exporta observaciones. |
| `/export/feedback.csv` | Exporta feedback. |
| `/is_videos/<filename>` | Sirve videos de lengua de senas. |
| `/behavior_videos/<filename>` | Sirve videos de comportamiento si existen. |

---

## 16. Apartado de video y YOLO

Actualmente existen dos zonas relacionadas con video:

```text
datos/videos/
codigo/pytorch/app_flask/static/behavior_videos/
```

`datos/videos/` esta pensado para clips de campo usados por el modulo de comportamiento. La version actual ya implementa deteccion/seguimiento con YOLO para localizar aves en video, asignar `track_id` por individuo y analizar comportamiento de vuelo con heuristicas conservadoras.

Estado recomendado para presentacion:

- **actual:** pipeline YOLO implementado como prototipo reproducible;
- **pendiente:** entrenar detector YOLO propio con cajas anotadas y validar etiquetas temporales;
- **no afirmar:** que el modulo de video ya es un clasificador final validado.

---

## 17. Carpeta `codigo/comparacion/`

Sirve para comparar arquitecturas y generar graficas.

| Archivo/carpeta | Funcion |
|---|---|
| `comparar_arquitecturas.py` | Ejecuta entrenamiento/evaluacion por arquitectura y genera reporte. |
| `README.md` | Explica el protocolo comparativo. |
| `metricas_arquitecturas.csv` | Tabla de metricas comparativas. |
| `figures/` | Graficas: accuracy, F1-macro y latencia vs accuracy. |

---

## 18. Carpeta `codigo/tensorflow/`

Implementacion secundaria en TensorFlow/Keras.

| Archivo | Funcion |
|---|---|
| `config.py` | Configuracion equivalente para TensorFlow. |
| `data_loader.py` | Carga de datos para TensorFlow. |
| `model.py` | Arquitectura del modelo en TensorFlow. |
| `train.py` | Entrenamiento con TensorFlow. |
| `evaluate.py` | Evaluacion con TensorFlow. |
| `make_synthetic_dataset.py` | Dataset sintetico para pruebas. |
| `verify_setup.py` | Verificacion de dependencias. |
| `environment.yml` | Entorno Conda. |
| `requirements.txt` / `pip-requirements.txt` | Dependencias pip. |
| `outputs/` | Salidas generadas. |

Esta parte no es la principal. Para explicar el proyecto conviene decir que PyTorch es la implementacion autoritativa.

---

## 19. Carpeta `documentacion/`

Contiene la parte academica y de gestion del proyecto.

| Archivo/carpeta | Funcion |
|---|---|
| `guias/` | Manuales de instalacion, comandos y documentacion completa. |
| `resultados/` | Plantillas para reportar metricas, curvas, confusion matrix y Grad-CAM. |
| `diagramas/` | Diagramas de arquitectura. |
| `LISTA_OFICIAL_RAPACES_MEXICO.md` | Lista taxonomica oficial de especies objetivo. |
| `WORKFLOW_DATASET_REAL.md` | Flujo para construir el dataset real. |
| `data_management_plan.md` | Plan de gestion de datos. |
| `preregistration.md` | Prerregistro de hipotesis/metodologia. |
| `contribucion_novedosa.md` | Explica la contribucion academica. |
| `glosario.md` | Glosario de terminos. |
| `RESUMEN_EJECUTIVO.md` | Resumen ejecutivo del proyecto. |

Los borradores internos, auditorias, entrevistas, presentaciones binarias y capitulos en Word se conservan localmente, pero estan excluidos de GitHub mediante `.gitignore`.

---

## 20. Carpeta `documentacion/resultados/`

No contiene necesariamente resultados finales; contiene plantillas y protocolos.

| Archivo | Funcion |
|---|---|
| `README.md` | Explica que va en la carpeta de resultados. |
| `METRICS_TEMPLATE.md` | Plantilla de metricas por arquitectura/especie. |
| `CONFUSION_MATRIX_TEMPLATE.md` | Plantilla para matriz de confusion. |
| `GRADCAM_EXAMPLES.md` | Protocolo para revisar Grad-CAM. |
| `TRAINING_CURVES.md` | Guia para interpretar curvas de entrenamiento. |
| `SHORTCUT_LEARNING_FINDING.md` | Documento sobre aprendizaje de atajos. |

---

## 21. Carpeta `scripts/`

Utilidades externas al codigo principal.

### `scripts/windows/`

| Archivo | Funcion |
|---|---|
| `descargar_v1_1.bat` | Descarga dataset desde Windows. |
| `entrenar_v1_1.bat` | Ejecuta smoke test o entrenamiento desde Windows. |
| `pipeline_completo_v1_1.bat` | Ejecuta curacion, split, entrenamiento y evaluacion. |
| `limpiar_v1_1.bat` | Limpieza de archivos generados/obsoletos. |
| `commit_v1_1.bat` | Atajo local para commit/push. Usarlo con cuidado. |

### `scripts/dataset/`

| Archivo | Funcion |
|---|---|
| `contar_dataset.py` | Cuenta imagenes por split y por especie. |
| `seleccionar_imagenes_galeria.py` | Elige automaticamente imagenes para la guia de especies. |
| `selector_galeria_gui.py` | Interfaz Tkinter para elegir manualmente imagenes de galeria. |

---

## 22. Carpeta `datos/`

| Carpeta/archivo | Funcion |
|---|---|
| `README.md` | Explica la organizacion de datos. |
| `FUENTES_DE_IMAGENES.md` | Fuentes y criterios de imagenes. |
| `annotations/` | Metadatos CSV, reportes de curacion y archivo `.gitkeep`. |
| `feedback/` | Feedback de usuarios y casos fuera de dominio. |
| `videos/README.md` | Plan de organizacion de videos para comportamiento/YOLO. |
| `raw/` | Imagenes originales descargadas. Ignorado por Git. |
| `processed/` | Dataset partido en train/val/test. Ignorado por Git. |

---

## 23. Carpeta `lengua_de_senas/`

Entregable secundario de accesibilidad.

| Archivo/carpeta | Funcion |
|---|---|
| `README.md` | Explica el modulo de lengua de senas. |
| `glosario_IS_LSM.md` | Glosario entre International Sign, LSM y terminos relacionados. |
| `catalogo_senas/` | Catalogo propuesto de senas por especie. |
| `instrumentos_validacion/` | Cuestionarios y validacion con usuarios. |
| `videos/` | Videos de senas. Pesados o futuros, no centrales para IA. |

Este apartado no debe venderse como la contribucion principal de IA; es un componente de inclusion.

---

## 24. Carpeta `referencias/`

| Archivo | Funcion |
|---|---|
| `bibliografia.md` | Bibliografia base del proyecto. |
| `plantilla_ficha.md` | Plantilla para fichas de referencia/especies. |

---

## 25. Carpeta `.vscode/`

Configuracion para Visual Studio Code.

| Archivo | Funcion |
|---|---|
| `settings.json` | Preferencias del editor/lint/formato. |
| `extensions.json` | Extensiones recomendadas. |
| `launch.json` | Configuraciones de ejecucion/debug. |

No es parte del modelo, pero ayuda a que el entorno de desarrollo sea consistente.

---

## 26. Flujo completo del proyecto

```text
1. Definir especies objetivo
   documentacion/LISTA_OFICIAL_RAPACES_MEXICO.md
   codigo/pytorch/config.py

2. Descargar imagenes
   codigo/pytorch/download_inaturalist.py
   codigo/pytorch/download_ebird.py

3. Curar imagenes
   codigo/pytorch/curate.py

4. Dividir dataset
   codigo/pytorch/split_dataset.py

5. Cargar datos y augmentations
   codigo/pytorch/data_loader.py

6. Construir modelo
   codigo/pytorch/model.py

7. Entrenar
   codigo/pytorch/train.py

8. Evaluar
   codigo/pytorch/evaluate.py

9. Interpretar con Grad-CAM
   codigo/pytorch/gradcam.py

10. Mostrar en interfaz
    codigo/pytorch/app_flask/app.py
    codigo/pytorch/app_flask/templates/
    codigo/pytorch/app_flask/static/
```

---

## 27. Comandos principales

### Verificar entorno

```bash
cd codigo/pytorch
python verify_setup.py
```

### Contar dataset

```bash
python scripts/dataset/contar_dataset.py --por-especie
```

### Entrenar rapido

```bash
cd codigo/pytorch
python train.py --arch resnet50 --smoke-test
```

### Entrenar completo

```bash
cd codigo/pytorch
python train.py --arch resnet50
```

### Evaluar

```bash
cd codigo/pytorch
python evaluate.py --arch resnet50 --weights outputs/checkpoints/best_stage2.pt
```

### Ejecutar Flask

```bash
cd C:\Users\hogwa\raptors-cnn
conda activate raptors-pt
cd codigo\pytorch\app_flask
python app.py
```

---

## 28. Que decir en una presentacion

Version corta:

> Este proyecto desarrolla un pipeline reproducible de inteligencia artificial para identificar las 53 rapaces diurnas de Mexico. A diferencia de herramientas generalistas como Merlin, el enfoque se centra en rapaces en vuelo, donde la silueta, la forma y el comportamiento son mas informativos que el color. El sistema incluye entrenamiento CNN, evaluacion cuantitativa, Grad-CAM e interfaz Flask para demostracion.

Version honesta del estado:

> La clasificacion por imagen y la interfaz estan implementadas como prototipo. La parte de video/comportamiento ya usa YOLO para deteccion y seguimiento, pero sus etiquetas de comportamiento son heuristicas hasta contar con anotaciones temporales validadas.

---

## 29. Que NO conviene afirmar todavia

No afirmar:

- que el sistema ya supera a Merlin;
- que el modulo de video YOLO ya esta validado como resultado final;
- que los resultados finales de las 53 especies ya estan validados si aun no se corrio el benchmark completo;
- que sustituye a expertos humanos;
- que la lengua de senas es una contribucion central de IA.

Si conviene afirmar:

- que el proyecto es abierto y reproducible;
- que esta orientado a rapaces mexicanas;
- que usa transfer learning;
- que tiene pipeline de entrenamiento/evaluacion;
- que la interfaz Flask permite una demostracion clara;
- que video/YOLO ya existe como prototipo y el siguiente paso es validarlo con anotaciones reales.
