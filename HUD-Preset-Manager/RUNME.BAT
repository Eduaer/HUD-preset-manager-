@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

pushd ".\Files"
".\python-capado\python.exe" ".\ui.py"
popd

pause
endlocal