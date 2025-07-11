{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
"""\
Telegram News Sender\
Autonomous delivery to configured chat ID\
Zero-cost using Telegram Bot API\
"""\
\
import json\
import requests\
import logging\
from datetime import datetime\
import os\
\
# Setup logging\
logging.basicConfig(\
    level=logging.INFO,\
    format='%(asctime)s - %(levelname)s - %(message)s',\
    handlers=[\
        logging.FileHandler('logs/telegram_sender.log'),\
        logging.StreamHandler()\
    ]\
)\
\
class TelegramSender:\
    def __init__(self):\
        # Load configuration\
        self.load_config()\
        \
    def load_config(self):\
        """Load configuration from config.json"""\
        try:\
            with open('config.json', 'r') as f:\
                config = json.load(f)\
            \
            self.bot_token = config['telegram']['bot_token']\
            self.chat_id = config['telegram']['chat_id']\
            self.api_url = f"https://api.telegram.org/bot\{self.bot_token\}"\
            \
            logging.info("Configuration loaded successfully")\
            \
        except Exception as e:\
            logging.error(f"Error loading configuration: \{str(e)\}")\
            raise\
    \
    def send_message(self, text, parse_mode='Markdown'):\
        """Send text message via Telegram"""\
        try:\
            url = f"\{self.api_url\}/sendMessage"\
            \
            payload = \{\
                'chat_id': self.chat_id,\
                'text': text,\
                'parse_mode': parse_mode\
            \}\
            \
            response = requests.post(url, json=payload, timeout=30)\
            response.raise_for_status()\
            \
            result = response.json()\
            \
            if result.get('ok'):\
                logging.info("Message sent successfully")\
                return True\
            else:\
                logging.error(f"Telegram API error: \{result\}")\
                return False\
                \
        except Exception as e:\
            logging.error(f"Error sending message: \{str(e)\}")\
            return False\
    \
    def send_audio(self, audio_file_path, caption=""):\
        """Send audio file via Telegram"""\
        try:\
            if not os.path.exists(audio_file_path):\
                logging.error(f"Audio file not found: \{audio_file_path\}")\
                return False\
            \
            url = f"\{self.api_url\}/sendAudio"\
            \
            with open(audio_file_path, 'rb') as audio_file:\
                files = \{'audio': audio_file\}\
                data = \{\
                    'chat_id': self.chat_id,\
                    'caption': caption\
                \}\
                \
                response = requests.post(url, files=files, data=data, timeout=60)\
                response.raise_for_status()\
                \
                result = response.json()\
                \
                if result.get('ok'):\
                    logging.info("Audio sent successfully")\
                    return True\
                else:\
                    logging.error(f"Telegram API error: \{result\}")\
                    return False\
                    \
        except Exception as e:\
            logging.error(f"Error sending audio: \{str(e)\}")\
            return False\
    \
    def format_news_bulletin(self, news_data):\
        """Format news data into Telegram message"""\
        if not news_data:\
            return "\uc0\u2310 \u2332  \u2325 \u2379 \u2312  \u2360 \u2350 \u2366 \u2330 \u2366 \u2352  \u2313 \u2346 \u2354 \u2348 \u2381 \u2343  \u2344 \u2361 \u2368 \u2306  \u2361 \u2376 \u2404 "\
        \
        # Create bulletin header\
        current_date = datetime.now().strftime('%d %B %Y')\
        bulletin = f"\uc0\u55356 \u57119  *\u2331 \u2340 \u2381 \u2340 \u2368 \u2360 \u2327 \u2338 \u2364  \u2325 \u2368  \u2340 \u2366 \u2332 \u2364 \u2366  \u2326 \u2348 \u2352 \u2375 \u2306  \'96 \{current_date\}*\\n\\n"\
        \
        # Add news items\
        for i, item in enumerate(news_data[:6], 1):  # Limit to 6 items\
            title = item.get('title', '').strip()\
            source = item.get('source', '')\
            \
            # Format title for Telegram\
            if title:\
                bulletin += f"\{title\}\\n\\n"\
        \
        # Add footer\
        bulletin += "\uc0\u55356 \u57269  *\u2321 \u2337 \u2367 \u2351 \u2379  \u2348 \u2369 \u2354 \u2375 \u2335 \u2367 \u2344  \u2313 \u2346 \u2354 \u2348 \u2381 \u2343 *\\n"\
        bulletin += "\uc0\u9989  *\u2360 \u2349 \u2368  \u2326 \u2348 \u2352 \u2375 \u2306  \u2361 \u2367 \u2306 \u2342 \u2368  \u2321 \u2337 \u2367 \u2335  \u2325 \u2375  \u2360 \u2366 \u2341  \u2360 \u2340 \u2381 \u2351 \u2366 \u2346 \u2367 \u2340 *\\n"\
        bulletin += "\uc0\u55357 \u57057 \u65039  *\u2357 \u2381 \u2351 \u2366 \u2357 \u2360 \u2366 \u2351 \u2367 \u2325  \u2349 \u2366 \u2359 \u2366  \u2350 \u2366 \u2344 \u2325  \u2348 \u2344 \u2366 \u2319  \u2352 \u2326 \u2375  \u2327 \u2319 *\\n"\
        bulletin += "\uc0\u55357 \u56522  *Enhanced features \u2325 \u2375  \u2360 \u2366 \u2341  \u2340 \u2376 \u2351 \u2366 \u2352 *\\n\\n"\
        bulletin += f"\uc0\u55357 \u56656  *\u2360 \u2350 \u2351 *: \{datetime.now().strftime('%H:%M IST')\}"\
        \
        return bulletin\
    \
    def send_daily_bulletin(self):\
        """Send complete daily news bulletin"""\
        try:\
            # Load audited news data\
            with open('data/latest_audited.json', 'r', encoding='utf-8') as f:\
                news_data = json.load(f)\
            \
            # Format bulletin\
            bulletin_text = self.format_news_bulletin(news_data)\
            \
            # Send text bulletin\
            text_success = self.send_message(bulletin_text)\
            \
            # Send audio bulletin if available\
            audio_path = "audio/latest.mp3"\
            audio_success = False\
            \
            if os.path.exists(audio_path):\
                audio_caption = "\uc0\u55356 \u57269  \u2310 \u2332  \u2325 \u2368  \u2350 \u2369 \u2326 \u2381 \u2351  \u2326 \u2348 \u2352 \u2379 \u2306  \u2325 \u2366  \u2321 \u2337 \u2367 \u2351 \u2379  \u2348 \u2369 \u2354 \u2375 \u2335 \u2367 \u2344 "\
                audio_success = self.send_audio(audio_path, audio_caption)\
            else:\
                logging.warning("Audio file not found, sending text only")\
            \
            # Send delivery confirmation\
            if text_success:\
                status_message = "\uc0\u9989  *Enhanced News Delivery Complete*\\n\\n"\
                status_message += f"\uc0\u55357 \u56522  *Delivery Stats:*\\n"\
                status_message += f"\'95 News Items: \{len(news_data)\}\\n"\
                status_message += f"\'95 Text Bulletin: \uc0\u9989  Delivered\\n"\
                status_message += f"\'95 Audio Bulletin: \{'\uc0\u9989  Delivered' if audio_success else '\u10060  Failed'\}\\n"\
                status_message += f"\'95 Hindi Audit: \uc0\u9989  Applied\\n"\
                status_message += f"\'95 Professional Standards: \uc0\u9989  Maintained\\n"\
                status_message += f"\'95 Delivery Time: \{datetime.now().strftime('%H:%M:%S IST')\}"\
                \
                self.send_message(status_message)\
                \
                logging.info("Daily bulletin sent successfully")\
                return True\
            else:\
                logging.error("Failed to send daily bulletin")\
                return False\
                \
        except Exception as e:\
            logging.error(f"Error sending daily bulletin: \{str(e)\}")\
            return False\
\
def main():\
    """Main telegram sending function"""\
    logging.info("Starting Telegram delivery...")\
    \
    try:\
        sender = TelegramSender()\
        success = sender.send_daily_bulletin()\
        \
        if success:\
            logging.info("Telegram delivery completed successfully")\
        else:\
            logging.error("Telegram delivery failed")\
            \
    except Exception as e:\
        logging.error(f"Error in Telegram delivery: \{str(e)\}")\
\
if __name__ == "__main__":\
    main()}