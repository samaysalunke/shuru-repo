@echo off
REM Shuru Tech Chatbot Setup Script for Windows
REM This script creates a virtual environment and installs dependencies

echo 🚀 Setting up Shuru Tech Chatbot...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Display Python version
echo ✓ Python version:
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist .env (
    echo 📝 .env file not found. Please configure your .env file with your OpenAI API key.
    echo    Edit the .env file and add your OPENAI_API_KEY
) else (
    echo ✓ .env file exists
)

echo.
echo ✅ Setup complete!
echo.
echo To get started:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Update your .env file with your OpenAI API key
echo.
echo 3. Scrape the Shuru Tech website:
echo    python scrape_website.py
echo.
echo 4. Run the chatbot:
echo    streamlit run app.py
echo.
echo To deactivate the virtual environment later, run:
echo    deactivate
echo.
pause
