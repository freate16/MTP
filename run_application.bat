@echo off
setlocal

:: Ensure we are in the Deployment_Package directory
cd /d "%~dp0"

echo ========================================================
echo   Glacial Lake Outburst Flood (GLOF) Agentic System
echo ========================================================
echo.

:: Initialize Conda environment if double-clicked from Windows Explorer
if exist "C:\Users\rubel\miniconda3\Scripts\activate.bat" (
    call "C:\Users\rubel\miniconda3\Scripts\activate.bat"
)

:: Attempt to activate conda environment
call conda activate glof_agent >nul 2>&1
if %errorlevel% neq 0 (
    call conda activate .\.venv >nul 2>&1
)

:: Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    pause
    exit /b
)

:: Check for HF_TOKEN
if "%HF_TOKEN%"=="" (
    echo [WARNING] HF_TOKEN is not set in your environment. 
    echo           The remote Hugging Face API for embeddings/chat might fail.
    echo           Please set it via: setx HF_TOKEN "your_token"
    echo.
)

echo [1/2] Starting the Agentic RAG Backend Server...
start "GLOF Chatbot Backend" cmd /k "python chatbot\chat_server.py"

echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak >nul

echo [2/2] Launching the Frontend Interface...
start "" "website\index.html"

echo.
echo Both systems are now running. 
echo - The backend server is running in a separate command window.
echo - The frontend has opened in your default web browser.
echo.
echo To shut down, simply close the backend command window.
pause
