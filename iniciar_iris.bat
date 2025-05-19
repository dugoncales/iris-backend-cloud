@echo off
title Iniciando projeto Iris
echo === Iniciando Backend Flask ===
cd /d C:\Users\eduardo.sellan\Downloads\iris_backend_cloud
start cmd /k "python app.py"

timeout /t 5

echo === Iniciando App Flutter no emulador Android ===
cd /d C:\Users\eduardo.sellan\Downloads\iris_app
start cmd /k "flutter run -d emulator-5554"

echo === Tudo iniciado ===
pause
