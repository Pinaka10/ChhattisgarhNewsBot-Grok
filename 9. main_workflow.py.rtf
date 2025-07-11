{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
import os\
import subprocess\
from telegram import Bot\
import requests\
import json\
\
# Load config\
with open('config.json', 'r') as f:\
    config = json.load(f)\
\
# Env vars from config (for GitHub Actions/Heroku)\
os.environ['TELEGRAM_TOKEN'] = config['telegram']['bot_token']\
os.environ['MAIN_CHAT_ID'] = config['telegram']['chat_id']\
os.environ['CG_PROCESS_TOKEN'] = "YOUR_CG_PROCESS_TOKEN_HERE"  # Replace with actual\
os.environ['CG_CHAT_ID'] = "YOUR_CG_CHAT_ID_HERE"  # Replace with actual\
os.environ['GROK_API_KEY'] = "YOUR_GROK_API_KEY_HERE"  # Replace with actual\
\
def run_script(script_name):\
    cg_bot = Bot(os.environ['CG_PROCESS_TOKEN'])\
    cg_bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Starting \{script_name\}...")\
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)\
    if result.returncode == 0:\
        cg_bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"\{script_name\} completed successfully.")\
    else:\
        cg_bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Error in \{script_name\}: \{result.stderr\}")\
    # Grok validation\
    grok_response = requests.post('https://api.x.ai/v1/chat/completions', headers=\{'Authorization': f'Bearer \{os.environ["GROK_API_KEY"]\}'\}, json=\{'model': 'grok', 'messages': [\{'role': 'user', 'content': f'Validate \{script_name\} output: Check for hallucinations, bias, profanity'\}]\}).json()\
    cg_bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Grok validation for \{script_name\}: \{grok_response['choices'][0]['message']['content']\}")\
\
if __name__ == "__main__":\
    scripts = ['news_scraper.py', 'hindi_auditor.py', 'mp3_generator.py', 'telegram_sender.py']\
    for script in scripts:\
        run_script(script)}