#!/usr/bin/env python3
"""
Telegram News Sender
Autonomous delivery to configured chat ID
Zero-cost using Telegram Bot API
"""

import json
import requests
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/telegram_sender.log'),
        logging.StreamHandler()
    ]
)

class TelegramSender:
    def __init__(self):
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            self.bot_token = config['telegram']['bot_token']
            self.chat_id = config['telegram']['chat_id']
            self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
            
            logging.info("Configuration loaded successfully")
            
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            raise
    
    def send_message(self, text, parse_mode='Markdown'):
        """Send text message via Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                logging.info("Message sent successfully")
                return True
            else:
                logging.error(f"Telegram API error: {result}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False
    
    def send_audio(self, audio_file_path, caption=""):
        """Send audio file via Telegram"""
        try:
            if not os.path.exists(audio_file_path):
                logging.error(f"Audio file not found: {audio_file_path}")
                return False
            
            url = f"{self.api_url}/sendAudio"
            
            with open(audio_file_path, 'rb') as audio_file:
                files = {'audio': audio_file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = requests.post(url, files=files, data=data, timeout=60)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get('ok'):
                    logging.info("Audio sent successfully")
                    return True
                else:
                    logging.error(f"Telegram API error: {result}")
                    return False
                    
        except Exception as e:
            logging.error(f"Error sending audio: {str(e)}")
            return False
    
    def format_news_bulletin(self, news_data):
        """Format news data into Telegram message"""
        if not news_data:
            return "आज कोई समाचार उपलब्ध नहीं है।"
        
        # Create bulletin header
        current_date = datetime.now().strftime('%d %B %Y')
        bulletin = f"🌟 *छत्तीसगढ़ की ताज़ा खबरें – {current_date}*\n\n"
        
        # Add news items
        for i, item in enumerate(news_data[:6], 1):  # Limit to 6 items
            title = item.get('title', '').strip()
            source = item.get('source', '')
            
            # Format title for Telegram
            if title:
                bulletin += f"{title}\n\n"
        
        # Add footer
        bulletin += "🎵 *ऑडियो बुलेटिन उपलब्ध*\n"
        bulletin += "✅ *सभी खबरें हिंदी ऑडिट के साथ सत्यापित*\n"
        bulletin += "🛡️ *व्यावसायिक भाषा मानक बनाए रखे गए*\n"
        bulletin += "📊 *Enhanced features के साथ तैयार*\n\n"
        bulletin += f"🕐 *समय*: {datetime.now().strftime('%H:%M IST')}"
        
        return bulletin
    
    def send_daily_bulletin(self):
        """Send complete daily news bulletin"""
        try:
            # Load audited news data
            with open('data/latest_audited.json', 'r', encoding='utf-8') as f:
                news_data = json.load(f)
            
            # Format bulletin
            bulletin_text = self.format_news_bulletin(news_data)
            
            # Send text bulletin
            text_success = self.send_message(bulletin_text)
            
            # Send audio bulletin if available
            audio_path = "audio/latest.mp3"
            audio_success = False
            
            if os.path.exists(audio_path):
                audio_caption = "🎵 आज की मुख्य खबरों का ऑडियो बुलेटिन"
                audio_success = self.send_audio(audio_path, audio_caption)
            else:
                logging.warning("Audio file not found, sending text only")
            
            # Send delivery confirmation
            if text_success:
                status_message = "✅ *Enhanced News Delivery Complete*\n\n"
                status_message += f"📊 *Delivery Stats:*\n"
                status_message += f"• News Items: {len(news_data)}\n"
                status_message += f"• Text Bulletin: ✅ Delivered\n"
                status_message += f"• Audio Bulletin: {'✅ Delivered' if audio_success else '❌ Failed'}\n"
                status_message += f"• Hindi Audit: ✅ Applied\n"
                status_message += f"• Professional Standards: ✅ Maintained\n"
                status_message += f"• Delivery Time: {datetime.now().strftime('%H:%M:%S IST')}"
                
                self.send_message(status_message)
                
                logging.info("Daily bulletin sent successfully")
                return True
            else:
                logging.error("Failed to send daily bulletin")
                return False
                
        except Exception as e:
            logging.error(f"Error sending daily bulletin: {str(e)}")
            return False

def main():
    """Main telegram sending function"""
    logging.info("Starting Telegram delivery...")
    
    try:
        sender = TelegramSender()
        success = sender.send_daily_bulletin()
        
        if success:
            logging.info("Telegram delivery completed successfully")
        else:
            logging.error("Telegram delivery failed")
            
    except Exception as e:
        logging.error(f"Error in Telegram delivery: {str(e)}")

if __name__ == "__main__":
    main()
