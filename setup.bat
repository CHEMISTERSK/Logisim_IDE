@echo off

python --version >nul 2>&1 || exit /b 1
pip --version >nul 2>&1 || exit /b 2

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    pip install customtkinter >nul 2>&1
    python -c "import customtkinter" >nul 2>&1 || exit /b 3
)

exit /b 0