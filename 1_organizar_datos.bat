@echo off
title Pipeline EEG - Organizador Local
color 0A

:: --- RUTA LOCAL DE ARCHIVOS CRUDOS ---
set RUTA_DATOS="D:\Sleep"

echo ===================================================
echo   INICIANDO ORGANIZACION DE DATASETS EEG (LOCAL)
echo ===================================================
echo.

python organizar_datasets.py %RUTA_DATOS% --modo sueno

echo.
echo ===================================================
echo   PROCESO TERMINADO
echo ===================================================
pause