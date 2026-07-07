@echo off
title Pipeline EEG Local Completo
color 0F

echo ===================================================
echo   PIPELINE AUTOMATICO DE PROCESAMIENTO LOCAL EEG
echo ===================================================
echo.

:: CONFIGURACION DE RUTAS LOCALES DIRECTAS
set RUTA_CRUDOS="D:\Sleep"
set RUTA_DESTINO="C:\Servicio\Epilepsia\Participantes"

echo [PASO 1/2] Organizando archivos crudos...
python organizar_datasets.py %RUTA_CRUDOS% --modo sueno
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ---------------------------------------------------
echo.

echo [PASO 2/2] Ejecutando procesamiento y optimizacion en Polars...
python procesar_eeg.py %RUTA_DESTINO%
if %ERRORLEVEL% NEQ 0 goto :error

echo.
echo ===================================================
echo   ✨ TODO EL PIPELINE LOCAL SE EJECUTO CORRECTAMENTE ✨
echo ===================================================
pause
exit

:error
color 0C
echo.
echo ===================================================
echo   ❌ EL PROCESO TERMINO CON ERRORES LOCALES
echo ===================================================
pause