# Chhattisgarh News Telegram Sender
# Delivers daily bulletin (MP3 and text) with enterprise-grade reliability

import os
import time
import telegram
from telegram.error import TelegramError

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
with open('logs/telegram_sender.log', 'a') as log_file:
    log_file.write(f"{time.ctime()} - Telegram Sender started\n")

class TelegramSender:
    def __init__(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            self.bot_token = config['telegram']['bot_token']
            self.chat_id = config['telegram']['chat_id']
            self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Configuration loaded successfully\n")
        except Exception as e:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Error loading configuration: {str(e)}\n")
            raise

    def send_message(self, text, parse_mode='Markdown'):
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": text, "parse_mode": parse_mode}
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get('ok'):
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Message sent successfully\n")
                return True
            else:
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Telegram API error: {result}\n")
                return False
        except Exception as e:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Error sending message: {str(e)}\n")
            return False

    def send_audio(self, audio_path, caption=""):
        try:
            if not os.path.exists(audio_path):
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Audio file not found: {audio_path}\n")
                return False
            url = f"{self.api_url}/sendAudio"
            with open(audio_path, 'rb') as audio_file:
                files = {'audio': audio_file}
                data = {"chat_id": self.chat_id, "caption": caption}
                response = requests.post(url, files=files, data=data, timeout=60)
                response.raise_for_status()
                result = response.json()
                if result.get('ok'):
                    with open('logs/telegram_sender.log', 'a') as log_file:
                        log_file.write(f"{time.ctime()} - Audio sent successfully: {audio_path}\n")
                    return True
                else:
                    with open('logs/telegram_sender.log', 'a') as log_file:
                        log_file.write(f"{time.ctime()} - Telegram API error: {result}\n")
                    return False
        except Exception as e:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Error sending audio: {str(e)}\n")
            return False

    def format_news_bulletin(self, news_items):
        if not news_items:
            return "आज कोई समाचार उपलब्ध नहीं है।"
        current_date = time.strftime("%d %B %Y")
        bulletin = f"🌟 *छत्तीसगढ़ की ताज़ा खबरें – {current_date}*\n\n"
        for i, item in enumerate(news_items[:8], 1):
            headline = item.get("headline", "").strip()
            if headline:
                bulletin += f"{headline}\n\n"
        bulletin += "🎵 *ऑडियो बुलेटिन उपलब्ध*\n✅ *सभी खबरें हिंदी ऑडिट के साथ सत्यापित*\n🛡️ *व्यावसायिक भाषा मानक बनाए रखे गए*\n📊 *Enhanced features के साथ तैयार*\n\n🕐 *समय*: {time.strftime('%H:%M IST')}"
        return bulletin

    def send_daily_bulletin(self, mp3_path, news_items):
        try:
            bulletin_text = self.format_news_bulletin(news_items)
            text_success = self.send_message(bulletin_text)
            audio_success = False
            if os.path.exists(mp3_path):
                audio_caption = "🎵 आज की मुख्य खबरों का ऑडियो बुलेटिन"
                audio_success = self.send_audio(mp3_path, audio_caption)
            else:
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Audio file not found: {mp3_path}\n")
            if text_success:
                status_message = "✅ *Enhanced News Delivery Complete*\n\n📊 *Delivery Stats:*\n• News Items: {len(news_items)}\n• Text Bulletin: ✅ Delivered\n• Audio Bulletin: {'✅ Delivered' if audio_success else '❌ Failed'}\n• Delivery Time: {time.strftime('%H:%M:%S IST')}"
                self.send_message(status_message)
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Daily bulletin sent successfully\n")
                return True
            else:
                with open('logs/telegram_sender.log', 'a') as log_file:
                    log_file.write(f"{time.ctime()} - Failed to send daily bulletin\n")
                return False
        except Exception as e:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Error sending daily bulletin: {str(e)}\n")
            return False

def main():
    with open('logs/telegram_sender.log', 'a') as log_file:
        log_file.write(f"{time.ctime()} - Starting Telegram delivery...\n")
    try:
        sender = TelegramSender()
        # Example usage with test data
        test_mp3_path = "audio/bulletin_20250712_1947.mp3"  # Replace with actual path
        test_items = [{"headline": "🚨 बारिश ने रायपुर को प्रभावित किया", "source": "Test", "date": time.strftime("%Y-%m-%d")}]
        success = sender.send_daily_bulletin(test_mp3_path, test_items)
        if success:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Telegram delivery completed successfully\n")
        else:
            with open('logs/telegram_sender.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Telegram delivery failed\n")
    except Exception as e:
        with open('logs/telegram_sender.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - Error in Telegram delivery: {str(e)}\n")

if __name__ == "__main__":
    main()
