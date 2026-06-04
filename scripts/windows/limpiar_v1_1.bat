@echo off
REM ===========================================================================
REM limpiar_v1_1.bat  v1.0 - parser-safe
REM
REM Elimina del repo los archivos basura identificados por la auditoria:
REM   - templates _old_backup viejas (reemplazadas por look Australia)
REM   - GUIA_COMANDOS.txt viejo (reemplazado por GUIA_COMANDOS_V1_1.txt)
REM   - Tesis Biologia.docx (archivo huerfano de 2025, no del proyecto)
REM   - __pycache__/ de Python (se regenera solo)
REM
REM NO toca codigo/pytorch/app/ (Gradio antigua, se conserva)
REM NO toca codigo/tensorflow/ (implementacion espejo)
REM
REM Uso: doble-clic, o desde CMD: limpiar_v1_1.bat
REM ===========================================================================

setlocal

cd /d "%~dp0..\.."

echo.
echo === Limpieza de archivos viejos del proyecto ===
echo.

echo [1/4] Borrando templates _old_backup
if exist codigo\pytorch\app_flask\templates\_old_backup (
    rmdir /s /q codigo\pytorch\app_flask\templates\_old_backup
    echo   OK - _old_backup eliminado
) else (
    echo   - ya no existia
)

echo.
echo [2/4] Borrando GUIA_COMANDOS.txt viejo
if exist GUIA_COMANDOS.txt (
    del /F /Q GUIA_COMANDOS.txt
    echo   OK - GUIA_COMANDOS.txt eliminado
) else (
    echo   - ya no existia
)

echo.
echo [3/4] Borrando Tesis Biologia.docx
if exist "Tesis Biologia.docx" (
    del /F /Q "Tesis Biologia.docx"
    echo   OK - Tesis Biologia.docx eliminado
) else (
    echo   - ya no existia
)

echo.
echo [4/4] Borrando carpetas __pycache__ recursivamente
set CONTADOR=0
for /f "delims=" %%d in ('dir /b /s /ad __pycache__ 2^>nul') do (
    rmdir /s /q "%%d"
    set /a CONTADOR+=1
)
echo   OK - carpetas __pycache__ eliminadas

echo.
echo ===========================================================================
echo   LIMPIEZA COMPLETA
echo   Siguiente paso: scripts\windows\commit_v1_1.bat para subir los cambios a GitHub
echo ===========================================================================
echo.
pause
endlocal
exit /b 0
