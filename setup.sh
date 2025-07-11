#!/bin/bash

# Autonomous Setup Script
# Creates virtual environment and installs dependencies

# Create logs directory
mkdir -p logs
mkdir -p data
mkdir -p audio

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

echo "Setup complete. Virtual environment created and dependencies installed."
echo "To activate: source venv/bin/activate"
echo "To run: python3 script_name.py"
