@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 goto use_py
python rppa.py
goto done
:use_py
where py >nul 2>nul
if errorlevel 1 goto missing
py -3 rppa.py
goto done
:missing
echo Install Python 3.10 or newer, then open this file again.
:done
pause
