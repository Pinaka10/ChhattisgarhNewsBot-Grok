{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sa240\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 #!/bin/bash\
\
# Autonomous Setup Script\
# Creates virtual environment and installs dependencies\
\
# Create logs directory\
mkdir -p logs\
mkdir -p data\
mkdir -p audio\
\
# Create virtual environment\
python3 -m venv venv\
\
# Activate virtual environment\
source venv/bin/activate\
\
# Upgrade pip\
pip install --upgrade pip\
\
# Install dependencies\
pip install -r requirements.txt\
\
# Deactivate virtual environment\
deactivate\
\
echo "Setup complete. Virtual environment created and dependencies installed."\
echo "To activate: source venv/bin/activate"\
echo "To run: python3 script_name.py"}