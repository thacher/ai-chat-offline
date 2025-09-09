#!/bin/bash

# Simple script to run the Hugging Face chatbot
# This script activates the virtual environment and starts the bot

echo "Starting Hugging Face Chatbot..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Launching chatbot..."
python3 bot.py
