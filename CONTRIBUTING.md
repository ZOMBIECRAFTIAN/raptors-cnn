# Guía para Contribuir

¡Gracias por tu interés en este proyecto! Este es un trabajo de tesis abierto a colaboraciones académicas y de la comunidad. A continuación se describe cómo participar.

## 🐦 Tipos de contribuciones bienvenidas

| Tipo | Ejemplos |
|------|----------|
| **Datos** | Imágenes propias de rapaces en vuelo (con licencia abierta), correcciones de etiquetado, registros del corredor |
| **Código** | Mejoras al pipeline, optimizaciones, nuevas arquitecturas, scripts de evaluación |
| **Documentación** | Correcciones, traducciones, ejemplos de uso |
| **Lengua de señas** | Refinamiento del catálogo IS, traducciones a LSM/ASL/otras lenguas de señas, feedback de la comunidad sorda |
| **Validación** | Anotación cruzada, revisión de identificaciones, reporte de errores del modelo |

## 📋 Flujo de trabajo recomendado

### Para cambios pequeños (typos, mejoras menores)

1. Haz clic en el ícono de editar (🖊️) sobre el archivo en GitHub.
2. Edita directamente y abre un Pull Request.

### Para cambios mayores (código, dataset, documentación extensa)

1. **Fork** el repositorio a tu cuenta de GitHub.
2. **Clona** tu fork localmente:
   ```bash
   git clone https://github.com/<tu-usuario>/raptors-cnn.git
   cd raptors-cnn
   ```
3. **Crea una rama** descriptiva:
   ```bash
   git checkout -b feature/agregar-mobilenet-v4
   ```
   Prefijos sugeridos: `feature/`, `fix/`, `docs/`, `dataset/`, `senas/`.
4. **Configura el entorno** siguiendo `SETUP.md`.
5. **Haz tus cambios**, asegurando que:
   - El código pasa `python verify_setup.py`.
   - Se mantiene el formato del proyecto (Black + Ruff, configurados en `.vscode/settings.json`).
   - Las nuevas dependencias se agregan al `environment.yml` o `pip-requirements.txt`.
6. **Commit con mensaje claro**:
   ```bash
   git commit -m "feat(model): agregar soporte para MobileNetV4-Large"
   ```
   Seguimos [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.
7. **Push** y abre Pull Request explicando el cambio.

## 🎯 Estándares del proyecto

- **Python ≥ 3.10**, con type hints donde sea posible.
- **Black** para formato, **Ruff** para lint (líneas ≤ 100 caracteres).
- **Docstrings** en español, lo más concisos posible.
- **Reproducibilidad**: todas las semillas aleatorias se fijan; ninguna constante hard-coded en scripts (todo en `config.py`).
- **Comentarios en código** principalmente en español; los nombres de funciones y variables, en inglés (estándar Python).

## 🦅 Contribuciones específicas de dataset

Si quieres aportar imágenes:

1. **Licencia obligatoria**: solo se aceptan imágenes con licencia Creative Commons (CC0, CC-BY, CC-BY-SA, CC-BY-NC) o de tu propia autoría declarando licencia.
2. **Calidad mínima**: lado mayor ≥ 640 px, ave claramente identificable, en vuelo (no posada para el dataset principal).
3. **Metadatos requeridos**: completar las columnas de `datos/annotations/metadata.csv` (fuente, licencia, fotógrafo, fecha si está disponible, ángulo).
4. **Validación**: al menos otro anotador debe coincidir en la identificación.

## 🤟 Contribuciones al catálogo de señas

El módulo de Lengua de Señas Internacional sigue una metodología de **co-creación** con la comunidad sorda. Si eres parte de esta comunidad o trabajas con ella:

- Las propuestas de señas nuevas o revisiones deben presentarse con un video corto (5-10 segundos, fondo neutral) y descripción textual.
- Se discuten en taller con el equipo y se documentan los argumentos a favor y en contra.
- Solo se incorporan al catálogo final tras validación cuantitativa (escala Likert ≥ 4.0).

## ⚖️ Código de conducta

Este proyecto se compromete a un ambiente colaborativo respetuoso. No se tolerará discriminación de ningún tipo, especialmente hacia la comunidad sorda u otros grupos históricamente excluidos del discurso científico.

## 📬 Contacto

Para coordinación de contribuciones, dudas o colaboraciones formales (Pronatura, Cornell Lab, universidades, etc.):

**Brian Fernández Báez** — `brianferbaez@gmail.com`

---

*Este documento se actualizará conforme crezca la comunidad alrededor del proyecto.*
