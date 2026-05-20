@echo off
REM ===========================================================================
REM entrenar_v1_1.bat
REM
REM Lanza el smoke test + entrenamiento real del modelo desde el directorio
REM raiz del proyecto (sin tener que recordar el cd codigo\pytorch).
REM
REM Uso:
REM   1) Doble-clic en el archivo
REM   2) O desde CMD:  entrenar_v1_1.bat
REM   3) Opciones:
REM        entrenar_v1_1.bat smoke   -> solo smoke test (1 epoch)
REM        entrenar_v1_1.bat real    -> entrenamiento completo
REM        entrenar_v1_1.bat all     -> arquitecturas comparativas
REM ===========================================================================

setlocal

REM Ir a la raiz del proyecto
cd /d "%~dp0"

REM Activar el entorno conda (asume Anaconda en %USERPROFILE%\anaconda3)
call %USERPROFILE%\anaconda3\Scripts\activate.bat raptors-pt
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno 'raptors-pt'.
    echo Asegurate de tener Anaconda instalado y el entorno creado.
    pause
    exit /b 1
)

set MODO=%1
if "%MODO%"=="" set MODO=smoke

cd codigo\pytorch

if "%MODO%"=="smoke" (
    echo.
    echo === SMOKE TEST: 1 epoch por etapa (~5 min) ===
    python train.py --arch resnet50 --smoke-test
    goto fin
)

if "%MODO%"=="real" (
    echo.
    echo === ENTRENAMIENTO REAL: ResNet-50 sobre silueta + vuelo (~4-8 horas) ===
    python train.py --arch resnet50
    goto fin
)

if "%MODO%"=="all" (
    echo.
    echo === COMPARATIVA: 4 arquitecturas (~16-24 horas total) ===
    python train.py --arch resnet50
    python train.py --arch efficientnet_b3
    python train.py --arch mobilenet_v3_large
    python train.py --arch convnext_tiny
    goto fin
)

echo ERROR: modo invalido '%MODO%'.
echo Usa: entrenar_v1_1.bat [smoke^|real^|all]

:fin
echo.
pause
endlocal
