REM Adds the environments variables from file ./config/.env

@echo off
for /f "tokens=*" %%a in (%~dp0/config/.env) do (
    for /f "tokens=1,2 delims==" %%b in ("%%a") do set %%b=%%c
)
pause
