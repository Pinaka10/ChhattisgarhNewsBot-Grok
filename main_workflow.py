# Chhattisgarh News Workflow
# Orchestrates scraping, auditing, fact-checking, and delivery

import os
import time
import subprocess
import asyncio
from telegram import Bot
import json
import requests
from indicnlp.sentiment import SentimentAnalyzer
from googleapiclient.discovery import build

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
with open('logs/workflow.log', 'a') as log_file:
    log_file.write(f"{time.ctime()} - Workflow started\n")

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Environment variables from Heroku Config Vars
os.environ.setdefault('TELEGRAM_TOKEN', config['telegram']['bot_token'])
os.environ.setdefault('MAIN_CHAT_ID', config['telegram']['chat_id'])
os.environ.setdefault('CG_PROCESS_TOKEN', os.environ.get('CG_PROCESS_TOKEN', ''))
os.environ.setdefault('CG_CHAT_ID', os.environ.get('CG_CHAT_ID', ''))
os.environ.setdefault('X_API_KEY', os.environ.get('X_API_KEY', ''))

# Initialize bots
bot_process = Bot(os.environ['CG_PROCESS_TOKEN'])

async def run_script(script_name, bot):
    await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Starting {script_name}...")
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    if result.returncode == 0:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"{script_name} completed successfully.")
    else:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Error in {script_name}: {result.stderr}")

async def fact_check_event(event, bot):
    try:
        # Local source validation (mocked for now, expand with X API)
        local_sources_confirmed = 2  # Placeholder, replace with actual check
        if local_sources_confirmed < 2:
            raise ValueError("Insufficient local source confirmation")

        # BERT Hindi mock validation (replace with actual API call)
        bert_similarity = 0.92  # Placeholder, >90% required
        if bert_similarity < 0.9:
            raise ValueError("BERT similarity below threshold")

        # Google Fact Check mock validation (replace with API call)
        fact_check_result = {"claim": "true"}  # Placeholder, no false flags
        if fact_check_result.get("claim") == "false":
            raise ValueError("Fact check flagged as false")

        return True
    except ValueError as e:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Fact check failed for event: {str(e)}")
        return False

async def main():
    bot = Bot(os.environ['CG_PROCESS_TOKEN'])
    first_run = True
    while True:
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text="Starting daily workflow...")
        scripts = ['news_scraper.py', 'hindi_auditor.py', 'mp3_generator.py', 'telegram_sender.py']
        verified_items = []
        for script in scripts:
            await run_script(script, bot)
        # Load scraped and audited data (mocked for now)
        with open('data/audited_news.json', 'r', encoding='utf-8') as f:
            news_items = json.load(f)
        # Fact-checking loop
        candidate_items = news_items[:15]
        while len(verified_items) < 6 and candidate_items:
            for item in candidate_items[:]:
                if await fact_check_event(item, bot):
                    verified_items.append(item)
                else:
                    candidate_items.remove(item)
            if len(verified_items) < 6 and candidate_items:
                await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Replacing rejected items, {len(candidate_items)} remaining...")
                # Mock additional scraping or pool refresh
        if len(verified_items) >= 6:
            verified_items = verified_items[:8]  # Limit to 8
            mp3_path = "audio/bulletin_{time.strftime('%Y%m%d_%H%M')}.mp3"  # Mock path
            subprocess.run(['python3', 'telegram_sender.py', mp3_path, json.dumps(verified_items)], check=True)
        else:
            await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text="Failed to verify 6 items, bulletin not sent.")
        # Schedule for 7:00 PM IST (19:00)
        delay = 60 if first_run else (19 * 3600 - time.time() % (24 * 3600))  # 1 minute or time to 19:00
        first_run = False
        await bot.send_message(chat_id=os.environ['CG_CHAT_ID'], text=f"Worker sleeping for {delay/60} minutes...")
        await asyncio.sleep(delay)

if __name__ == "__main__":
    asyncio.run(main())
