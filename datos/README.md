# Datos del Proyecto

Estructura de la carpeta de datos. **No subir imágenes con derechos restringidos a un repositorio público.**

```
datos/
├── raw/             imágenes originales sin procesar (organizadas por especie)
├── processed/       imágenes redimensionadas y divididas en train/val/test
└── annotations/     CSV con metadatos: archivo, especie, fuente, licencia, ángulo, condiciones
```

## Estructura esperada de raw/ y processed/

```
raw/
└── <Cod>_<Genero_especie>/
    └── *.jpg

processed/
├── train/
│   └── <Cod>_<Genero_especie>/   (70 % del total por especie)
├── val/
│   └── <Cod>_<Genero_especie>/   (15 % del total)
└── test/
    └── <Cod>_<Genero_especie>/   (15 % del total)
```

Donde `<Cod>` es el código de dos letras y `<Genero_especie>` es el nombre científico con guion bajo. Coincide con `config.SPECIES` en los dos frameworks.

## Carpetas a crear (las 14 especies)

`SS_Accipiter_striatus` · `CH_Astur_cooperii` · `ZT_Buteo_albonotatus` · `RT_Buteo_jamaicensis` · `RS_Buteo_lineatus` · `BW_Buteo_platypterus` · `SW_Buteo_swainsoni` · `TV_Cathartes_aura` · `NH_Circus_hudsonius` · `ML_Falco_columbarius` · `PG_Falco_peregrinus` · `AK_Falco_sparverius` · `MK_Ictinia_mississippiensis` · `OS_Pandion_haliaetus`

## Archivo de metadatos (`annotations/metadata.csv`)

Columnas mínimas:

| Columna | Descripción |
|---------|-------------|
| `filename` | nombre del archivo (sin ruta) |
| `species_code` | código de dos letras |
| `scientific_name` | nombre científico |
| `source` | macaulay / inaturalist / pronatura / propio |
| `license` | CC-BY, CC0, etc. |
| `photographer` | nombre del autor de la foto |
| `date` | YYYY-MM-DD si está disponible |
| `location` | sitio de captura |
| `angle` | dorsal / ventral / lateral |
| `condition` | clear / cloudy / backlit |
| `resolution_w` | ancho en píxeles |
| `resolution_h` | alto en píxeles |
| `annotator_1` | inicial del primer anotador |
| `annotator_2` | inicial del segundo anotador |
| `agreement` | 1 si los dos coinciden, 0 si discrepan |
| `final_label` | etiqueta tras resolución de conflictos |

## Reglas

- **Inclusión:** identificable por experto, ≥ 640 px en lado mayor, ave en vuelo, sin manipulación digital evidente.
- **Exclusión:** múltiples especies sin posibilidad de recortar, marcas de agua sobre el individuo, ambigüedad de especie.
- **Acuerdo inter-anotador requerido:** κ de Cohen ≥ 0.80.

## .gitignore sugerido

Las imágenes pueden pesar mucho. Recomendado mantener fuera del repositorio:

```
datos/raw/
datos/processed/
datos/annotations/*.csv  (incluir solo el ejemplo, no los datos reales)
```
