@echo off
REM ===========================================================================
REM commit_v1_1.bat
REM
REM Hace add + commit + push de TODOS los cambios del proyecto al GitHub
REM remoto, evitando los problemas de Windows CMD con mensajes multilinea.
REM
REM Uso:
REM   1) Doble-clic en el archivo, O
REM   2) Desde CMD:  cd C:\Users\hogwa\raptors-cnn  &  commit_v1_1.bat
REM ===========================================================================

setlocal

REM Ir a la raiz del proyecto independientemente desde donde se invoque
cd /d "%~dp0"

echo.
echo === [1/7] Limpia locks orfanos de git ===
if exist .git\index.lock (
    echo   * Eliminando .git\index.lock orfano...
    del /F /Q .git\index.lock
)
if exist .git\HEAD.lock (
    echo   * Eliminando .git\HEAD.lock orfano...
    del /F /Q .git\HEAD.lock
)
if exist .git\refs\heads\main.lock (
    del /F /Q .git\refs\heads\main.lock
)

echo.
echo === [2/7] Estado de git ===
git status --short
if errorlevel 1 (
    echo ERROR: No es un repo de git valido. Aborta.
    pause
    exit /b 1
)

echo.
echo === [3/7] Configura usuario (si no esta) ===
git config user.email >nul 2>&1
if errorlevel 1 (
    git config user.email "brianferbaez@gmail.com"
    git config user.name "Brian Fernandez Baez"
)

echo.
echo === [4/7] Pull con rebase (por si hay cambios remotos) ===
git pull --rebase origin main
if errorlevel 1 (
    echo   ADVERTENCIA: pull fallo. Revisa la conexion o conflictos.
    echo   Continuando con commit local de todas formas...
)

echo.
echo === [5/7] git add . (stage de todos los cambios) ===
git add .
if errorlevel 1 (
    echo ERROR: git add fallo.
    pause
    exit /b 1
)

echo.
echo === [6/7] git commit con mensaje en una sola linea ===
git commit -m "feat(V1.1): expand to 53 Mexican raptors + adopt Australia GUI 1:1 + rename project to Silueta-Vuelo-IS"
if errorlevel 1 (
    echo   No hay cambios nuevos para commitear (o el commit fallo).
    REM No salimos: aun asi intentamos el push por si hay commits locales pendientes.
)

echo.
echo === [7/7] Push a origin main ===
git push origin main
if errorlevel 1 (
    echo.
    echo   El push fallo. Intentos comunes:
    echo     - Si dice "non-fast-forward": ejecuta  git pull --rebase origin main  y vuelve a correr este script.
    echo     - Si dice "authentication": configura un Personal Access Token en GitHub.
    echo     - Si dice "permission denied": verifica el remote con  git remote -v
    pause
    exit /b 1
)

echo.
echo ===========================================================================
echo   LISTO. Cambios subidos a https://github.com/ZOMBIECRAFTIAN/raptors-cnn
echo ===========================================================================
echo.
git log --oneline -5

pause
endlocal
