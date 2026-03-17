@echo off
REM Script per eseguire gli esempi di Sbargold
echo.
echo ========================================
echo   ESEMPI LINGUAGGIO SBARGOLD
echo ========================================
echo.

:menu
echo Scegli un esempio da eseguire:
echo.
echo 1. Hello World
echo 2. Calcolatrice
echo 3. Loop
echo 4. Condizionali
echo 5. Array
echo 6. Fibonacci
echo 7. Fattoriale
echo 8. Test Completo
echo 9. Esci
echo.
set /p choice="Inserisci la tua scelta (1-9): "

if "%choice%"=="1" (
    echo.
    echo === HELLO WORLD ===
    python sbargold.py examples\hello_world.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo === CALCOLATRICE ===
    python sbargold.py examples\calculator.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo === LOOP ===
    python sbargold.py examples\loop.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo === CONDIZIONALI ===
    python sbargold.py examples\conditional.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo === ARRAY ===
    python sbargold.py examples\arrays.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo === FIBONACCI ===
    python sbargold.py examples\fibonacci.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="7" (
    echo.
    echo === FATTORIALE ===
    python sbargold.py examples\factorial.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="8" (
    echo.
    echo === TEST COMPLETO ===
    python sbargold.py examples\test_all.sbg
    echo.
    pause
    goto menu
)

if "%choice%"=="9" (
    echo.
    echo Arrivederci!
    exit
)

echo Scelta non valida!
pause
goto menu
