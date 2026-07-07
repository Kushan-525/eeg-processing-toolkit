@echo off
title Pipeline EEG - Procesador Central Local
color 0B

:: --- RUTA LOCAL EN TU DISCO (AJUSTABLE) ---
set RUTA_PARTICIPANTES="C:\Servicio\Epilepsia\Participantes"

echo ===================================================
echo   INICIANDO PROCESAMIENTO Y COMPRESION EN DISCO
echo ===================================================
echo.

python procesar_eeg.py %RUTA_PARTICIPANTES%

echo.
echo ===================================================
echo   PIPELINE FINALIZADO EXITOSAMENTE
echo ===================================================
pause
