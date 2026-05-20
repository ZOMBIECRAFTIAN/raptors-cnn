@echo off
REM ===========================================================================
REM pipeline_completo_v1_1.bat
REM
REM Flujo END-TO-END del proyecto post-descarga:
REM   1) Curacion automatica de imagenes
REM   2) Aplicar curacion (mover rechazos a _review)
REM   3) Limpiar placeholders gris si existen
REM   4) Re-splittear train/val/test
REM   5) Verificar conteo por especie
REM   6) Smoke test
REM   7) Entrenamiento real
REM   8) Evaluacion
REM
REM Uso: doble-clic. Tarda ~5-10 horas en RTX 3050.
REM ===========================================================================

setlocal

cd /d "%~dp0"

call %USERPROFILE%\anaconda3\Scripts\activate.bat raptors-pt
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno 'raptors-pt'.
    pause
    exit /b 1
)

cd codigo\pytorch

echo.
echo === [1/8] Curacion automatica ===
python curate.py
if errorlevel 1 ( pause & exit /b 1 )

echo.
echo === [2/8] Aplicando curacion (mueve rechazos) ===
python curate.py --apply
if errorlevel 1 ( pause & exit /b 1 )

echo.
echo === [3/8] Limpiando placeholders gris (si existen) ===
python exclude_empty_species.py --clean

echo.
echo === [4/8] Re-splittear dataset 70/15/15 ===
python split_dataset.py
if errorlevel 1 ( pause & exit /b 1 )

echo.
echo === [5/8] Verificacion del conteo por especie ===
cd /d "%~dp0"
python -c "import os; p='datos\\processed\\train'; rows=sorted([(d, sum(1 for f in os.listdir(f'{p}/{d}') if f.lower().endswith(('.jpg','.jpeg','.png','.webp')))) for d in sorted(os.listdir(p))], key=lambda x: x[1]); [print(f'{c:5d}  {s}') for s,c in rows]"

cd codigo\pytorch

echo.
echo === [6/8] Re-llenar placeholders en especies que aun esten vacias ===
python exclude_empty_species.py

echo.
echo === [7/8] Smoke test (1 epoch) ===
python train.py --arch resnet50 --smoke-test
if errorlevel 1 (
    echo Smoke test fallo. Revisa el error arriba.
    pause
    exit /b 1
)

echo.
echo === [8/8] Entrenamiento real (4-8 horas) ===
echo Esto va a tomar varias horas. Puedes minimizar la ventana.
echo Para cancelar: Ctrl+C
timeout /t 5
python train.py --arch resnet50
if errorlevel 1 ( pause & exit /b 1 )

echo.
echo === EVALUACION ===
python evaluate.py --arch resnet50 --weights outputs\checkpoints\best_stage2.pt

echo.
echo ===========================================================================
echo   PIPELINE COMPLETO. Pesos finales: outputs\checkpoints\best_stage2.pt
echo   Lanza la GUI con: cd app_flask ^&^& python app.py
echo ===========================================================================
pause
endlocal
