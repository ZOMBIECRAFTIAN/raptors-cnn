@echo off
REM ===========================================================================
REM commit_v1_1.bat  v1.3 - parser-safe
REM
REM Add + commit + push de TODOS los cambios al GitHub remoto.
REM Evita comillas anidadas, parentesis y puntos suspensivos en bloques if.
REM
REM Uso: doble-clic, o desde CMD: cd C:\Users\hogwa\raptors-cnn ^& commit_v1_1.bat
REM ===========================================================================

setlocal

REM Ir a la raiz del proyecto independientemente desde donde se invoque
cd /d "%~dp0"

REM ----- Paso 1: Limpieza de locks y huerfanos (sin if anidados) -----
echo.
echo === [1/7] Limpia locks orfanos de git y archivos huerfanos ===
if exist .git\index.lock del /F /Q .git\index.lock
if exist .git\HEAD.lock del /F /Q .git\HEAD.lock
if exist .git\refs\heads\main.lock del /F /Q .git\refs\heads\main.lock
if exist Ibycter del /F /Q Ibycter
echo   Limpieza terminada

echo.
echo === [2/7] Estado de git ===
git status --short
if errorlevel 1 goto err_git_repo

echo.
echo === [3/7] Configura usuario si no esta ===
git config user.email >nul 2>&1
if errorlevel 1 (
    git config user.email "brianferbaez@gmail.com"
    git config user.name "Brian Fernandez Baez"
)

echo.
echo === [4/7] Pull con rebase por si hay cambios remotos ===
git pull --rebase origin main
if errorlevel 1 (
    echo   ADVERTENCIA: pull fallo - revisa conexion o conflictos
    echo   Continuando con commit local de todas formas
)

echo.
echo === [5/7] git add . - stage de todos los cambios ===
git add .
if errorlevel 1 goto err_git_add

echo.
echo === [6/7] git commit con mensaje en una sola linea ===
git commit -m "chore(V1.1): fixes generales del proyecto - parser-safe .bat + numeracion pipeline + huerfanos + DOCX tesis"
if errorlevel 1 (
    echo   No hay cambios nuevos para commitear - intentando push de commits pendientes
)

echo.
echo === [7/7] Push a origin main ===
git push origin main
if errorlevel 1 goto err_push

echo.
echo ===========================================================================
echo   LISTO. Cambios subidos a https://github.com/ZOMBIECRAFTIAN/raptors-cnn
echo ===========================================================================
echo.
git log --oneline -5
echo.
pause
endlocal
exit /b 0

REM ----- bloques de error con goto (parser-safe) -----
:err_git_repo
echo ERROR: No es un repo de git valido. Aborta.
pause
endlocal
exit /b 1

:err_git_add
echo ERROR: git add fallo.
pause
endlocal
exit /b 1

:err_push
echo.
echo   El push fallo. Intentos comunes:
echo     - non-fast-forward    ejecuta  git pull --rebase origin main  y vuelve a correr
echo     - authentication      configura un Personal Access Token en GitHub
echo     - permission denied   verifica el remote con  git remote -v
pause
endlocal
exit /b 1
