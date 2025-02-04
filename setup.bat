@echo off
echo === Opsætter miljøet for projektet ===

:: Download og installer Python, hvis det ikke allerede er installeret
echo Tjekker for Python installation...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python ikke fundet. Henter og installerer Python...
    curl -O https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    start /wait python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
) else (
    echo Python er allerede installeret.
)

:: Opdater pip
echo Opdaterer pip...
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Installer nødvendige Python-pakker
echo Installerer afhængigheder...
python -m pip install selenium sqlalchemy mysql-connector-python webdriver-manager

:: Opsætning færdig
echo === Opsætning fuldført! ===
pause
