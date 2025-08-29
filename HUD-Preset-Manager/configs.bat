@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

pushd ".\Files"
".\python-capado\python.exe" ".\manual_configuration.py"
popd

pause
endlocal