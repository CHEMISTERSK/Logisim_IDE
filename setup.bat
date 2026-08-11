@echo off

echo Checking Python and pip installation...
python --version >nul 2>&1 || exit /b 1
pip --version >nul 2>&1 || exit /b 2

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing customtkinter...
    pip install customtkinter >nul 2>&1
    python -c "import customtkinter" >nul 2>&1 || exit /b 3
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install pillow >nul 2>&1
    python -c "import PIL" >nul 2>&1 || exit /b 3
)

echo All dependencies are installed successfully.
exit /b 0