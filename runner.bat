@echo off
call venv\Scripts\activate.bat
waitress-serve --listen=localhost:5000 main:app
