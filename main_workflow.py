#!/usr/bin/env python3
import os
import subprocess
import asyncio
from telegram import Bot
import requests
import json
import time

# Load config for non-sensitive settings
with open('config.json', 'r') as f:
    config = json.load(f)

# Env vars from Heroku Config Vars (already set via deployment environment)
os.environ.setdefault('TELEGRAM_TOKEN', config['telegram']['bot_token'])
os.environ.setdefault('MAIN_CHAT_ID', config['telegram']['chat_id'])
os.environ.setdefault('CG_PROCESS_TOKEN', os.environ.get('CG_PROCESS_TOKEN', ''))
os.environ.setdefault('CG_CHAT_ID', os.environ.get('CG_CHAT_ID', ''))
os.environ.setdefault('GROK_API_KEY', os.environ.get('GROK_API_KEY', ''))

async def run_script(script_name, bot):
    await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Starting {script_name}...")
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    if result.returncode == 0:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"{script_name} completed successfully.")
    else:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Error in {script_name}: {result.stderr}")
    # Grok validation with error handling
    try:
        grok_response = requests.post('https://api.x.ai/v1/chat/completions', 
                                     headers={'Authorization': f'Bearer {os.environ["GROK_API_KEY"]}'}, 
                                     json={'model': 'grok', 'messages': [{'role': 'user', 'content': f'Validate {script_name} output: Check for hallucinations, bias, profanity'}]}).json()
        if 'choices' in grok_response and grok_response['choices']:
            validation_text = grok_response['choices'][0].get('message', {}).get('content', 'No validation response')
        else:
            validation_text = 'Grok API response invalid or empty'
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Grok validation for {script_name}: {validation_text}")
    except Exception as e:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Grok validation error for {script_name}: {str(e)}")

async def main():
    bot = Bot(os.environ['CG_PROCESS_TOKEN'])
    while True:
        scripts = ['news_scraper.py', 'hindi_auditor.py', 'mp3_generator.py', 'telegram_sender.py']
        for script in scripts:
            await run_script(script, bot)
        # Wait for 4 hours (14400 seconds) as per config.json scraping_interval_hours
        await asyncio.sleep(14400)

if __name__ == "__main__":
    asyncio.run(main())
