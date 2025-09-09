#!/bin/bash

# Web interface launcher for AI Chat Offline
# This script activates the virtual environment and starts the web interface

echo "🚀 Launching AI Space Station Web Interface..."
echo "🌌 Space Station Control Panel Starting..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "🚀 Launching Space Station Control Panel..."
echo "🌌 Opening Space Station Interface in your browser"
echo "🛸 Space Station URL: http://localhost:3000"
echo "⏳ AI Core initialization may take 1-2 minutes on first launch"
echo ""
echo "Press Ctrl+C to shut down the Space Station"
echo "=============================================="

# Launch the web interface
python3 web_bot.py
