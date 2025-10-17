#!/bin/bash

# Shuru Tech Chatbot Setup Script for Mac/Linux
# This script creates a virtual environment and installs dependencies

echo "🚀 Setting up Shuru Tech Chatbot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Display Python version
echo "✓ Python version: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists, if not create from template
if [ ! -f .env ]; then
    echo "📝 .env file not found. Please configure your .env file with your OpenAI API key."
    echo "   Edit the .env file and add your OPENAI_API_KEY"
else
    echo "✓ .env file exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Update your .env file with your OpenAI API key"
echo ""
echo "3. Scrape the Shuru Tech website:"
echo "   python scrape_website.py"
echo ""
echo "4. Run the chatbot:"
echo "   streamlit run app.py"
echo ""
echo "To deactivate the virtual environment later, run:"
echo "   deactivate"
