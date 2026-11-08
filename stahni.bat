@echo off
chcp 65001 >nul
rem Dvojklik = zepta se, co stahnout.
rem Pretazeni .txt souboru na tuto ikonu = stahne cely seznam.
py "%~dp0downloader.py" %*
echo.
pause
