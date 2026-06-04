@echo off
REM ===========================================================================
REM descargar_v1_1.bat
REM
REM Descarga imagenes de iNaturalist para las 53 especies del proyecto.
REM Es incremental: respeta lo ya descargado.
REM
REM Uso:
REM   1) Doble-clic                       -> descarga 200 por especie
REM   2) scripts\windows\descargar_v1_1.bat raras   -> descargas focales para raras
REM   3) scripts\windows\descargar_v1_1.bat <CODE>  -> solo una especie (ej: BWHA)
REM ===========================================================================

setlocal

cd /d "%~dp0..\.."

call %USERPROFILE%\anaconda3\Scripts\activate.bat raptors-pt
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno 'raptors-pt'.
    pause
    exit /b 1
)

cd codigo\pytorch

set ARG=%1

if "%ARG%"=="" (
    echo.
    echo === DESCARGA MASIVA: 200 imagenes objetivo por especie ===
    echo     (toma ~6-12 horas, puedes dejarlo de fondo)
    echo.
    python download_inaturalist.py --target 200 --max-pages 5
    goto fin
)

if /i "%ARG%"=="raras" (
    echo.
    echo === DESCARGA FOCAL: especies raras (Harpia, Crested Eagle, etc.) ===
    python download_inaturalist.py --target 150 --max-pages 15 --species HAEA
    python download_inaturalist.py --target 150 --max-pages 15 --species CREA
    python download_inaturalist.py --target 150 --max-pages 15 --species OBFA
    python download_inaturalist.py --target 150 --max-pages 15 --species SOEA
    python download_inaturalist.py --target 150 --max-pages 15 --species RTCA
    python download_inaturalist.py --target 150 --max-pages 15 --species BFFA
    python download_inaturalist.py --target 150 --max-pages 15 --species CFFA
    python download_inaturalist.py --target 150 --max-pages 15 --species BAWE
    python download_inaturalist.py --target 150 --max-pages 15 --species ORHE
    python download_inaturalist.py --target 150 --max-pages 15 --species BLHE
    goto fin
)

echo.
echo === DESCARGA FOCAL: especie %ARG% ===
python download_inaturalist.py --target 200 --max-pages 10 --species %ARG%

:fin
echo.
pause
endlocal
