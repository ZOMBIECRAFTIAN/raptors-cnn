@echo off
REM ===========================================================================
REM pipeline_completo_v1_1.bat  (v1.2 - numeracion corregida 9/9)
REM
REM Flujo END-TO-END del proyecto post-descarga:
REM   1) Curacion automatica de imagenes
REM   2) Aplicar curacion (mover rechazos a _review)
REM   3) Limpiar placeholders gris si existen
REM   4) Re-splittear train/val/test
REM   5) Verificar conteo por especie
REM   6) Re-llenar placeholders en especies que sigan vacias
REM   7) Smoke test (1 epoch)
REM   8) Entrenamiento real (4-8 horas)
REM   9) Evaluacion final
REM
REM Uso: doble-clic. Tarda ~5-10 horas en RTX 3050.
REM ===========================================================================

setlocal

cd /d "%~dp0"

call %USERPROFILE%\anaconda3\Scripts\activate.bat raptors-pt
if errorlevel 1 goto err_env

cd codigo\pytorch

echo.
echo === [1/9] Curacion automatica ===
python curate.py
if errorlevel 1 goto err_step

echo.
echo === [2/9] Aplicando curacion - mueve rechazos a _review ===
python curate.py --apply
if errorlevel 1 goto err_step

echo.
echo === [3/9] Limpiando placeholders gris si existen ===
python exclude_empty_species.py --clean

echo.
echo === [4/9] Re-splittear dataset 70/15/15 ===
python split_dataset.py
if errorlevel 1 goto err_step

echo.
echo === [5/9] Verificacion del conteo por especie ===
cd /d "%~dp0"
python -c "import os; p='datos\\processed\\train'; rows=sorted([(d, sum(1 for f in os.listdir(f'{p}/{d}') if f.lower().endswith(('.jpg','.jpeg','.png','.webp')))) for d in sorted(os.listdir(p))], key=lambda x: x[1]); [print(f'{c:5d}  {s}') for s,c in rows]"

cd codigo\pytorch

echo.
echo === [6/9] Re-llenar placeholders en especies que aun esten vacias ===
python exclude_empty_species.py

echo.
echo === [7/9] Smoke test - 1 epoch ===
python train.py --arch resnet50 --smoke-test
if errorlevel 1 goto err_smoke

echo.
echo === [8/9] Entrenamiento real - 4 a 8 horas ===
echo Esto va a tomar varias horas - puedes minimizar la ventana
echo Para cancelar: Ctrl+C
timeout /t 5
python train.py --arch resnet50
if errorlevel 1 goto err_step

echo.
echo === [9/9] Evaluacion final ===
python evaluate.py --arch resnet50 --weights outputs\checkpoints\best_stage2.pt

echo.
echo ===========================================================================
echo   PIPELINE COMPLETO. Pesos finales: outputs\checkpoints\best_stage2.pt
echo   Lanza la GUI con:  cd app_flask  ^&^&  python app.py
echo ===========================================================================
pause
endlocal
exit /b 0

REM ----- bloques de error parser-safe -----
:err_env
echo ERROR: No se pudo activar el entorno conda 'raptors-pt'
pause
endlocal
exit /b 1

:err_step
echo ERROR: un paso del pipeline fallo - revisa el mensaje de arriba
pause
endlocal
exit /b 1

:err_smoke
echo Smoke test fallo - revisa el error arriba antes de lanzar entrenamiento real
pause
endlocal
exit /b 1
