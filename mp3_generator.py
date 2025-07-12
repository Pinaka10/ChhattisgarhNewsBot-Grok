# Chhattisgarh News MP3 Generator
# Converts audited news into high-quality MP3 audio

import os
import time
from gtts import gTTS
from pydub import AudioSegment

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
with open('logs/mp3_generator.log', 'a') as log_file:
    log_file.write(f"{time.ctime()} - MP3 Generator started\n")

def create_news_bulletin(news_items):
    if not news_items:
        return "आज कोई समाचार उपलब्ध नहीं है।"
    current_date = time.strftime("%d %B %Y")
    bulletin_text = f"🌟 छत्तीसगढ़ की ताज़ा खबरें – {current_date}\n\n"
    for i, item in enumerate(news_items[:8], 1):  # Limit to 8 items
        headline = item.get("headline", "").replace("🚨", "").replace("📌", "").replace("🏗️", "").replace("📰", "").strip()
        bulletin_text += f"खबर नंबर {i}। {headline}।\n\n"
        if len(bulletin_text) > 4500:  # gTTS free tier limit
            bulletin_text = bulletin_text[:4500] + "।"
            break
    bulletin_text += "यह थी आज की मुख्य खबरें। छत्तीसगढ़ न्यूज़ बॉट के साथ जुड़े रहें।"
    return bulletin_text

def clean_for_audio(text):
    if not text:
        return text
    replacements = {
        "1": "एक", "2": "दो", "3": "तीन", "4": "चार", "5": "पांच",
        "6": "छह", "7": "सात", "8": "आठ", "9": "नौ", "10": "दस"
    }
    for num, word in replacements.items():
        text = text.replace(num, word)
    text = text.replace("&", "और").replace("%", "प्रतिशत").replace("@", "एट").replace("#", "हैशटैग")
    return ' '.join(text.split())

def generate_mp3(news_items):
    try:
        bulletin_text = create_news_bulletin(news_items)
        cleaned_text = clean_for_audio(bulletin_text)
        tts = gTTS(text=cleaned_text, lang='hi', slow=False)
        mp3_path = f"audio/bulletin_{time.strftime('%Y%m%d_%H%M')}.mp3"
        os.makedirs('audio', exist_ok=True)
        tts.save(mp3_path)
        audio = AudioSegment.from_mp3(mp3_path)
        if audio.duration_seconds > 30:  # Enterprise-grade limit
            audio = audio[:30000]  # Trim to 30 seconds
        audio.export(mp3_path, format="mp3")
        with open('logs/mp3_generator.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - MP3 generated: {mp3_path}, Duration: {audio.duration_seconds}s\n")
        return mp3_path
    except Exception as e:
        with open('logs/mp3_generator.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - Error generating MP3: {str(e)}\n")
        return None

if __name__ == "__main__":
    # Example usage with test data
    test_items = [{"headline": "🚨 बारिश ने रायपुर को प्रभावित किया", "source": "Test", "date": time.strftime("%Y-%m-%d")}]
    mp3_path = generate_mp3(test_items)
    if mp3_path:
        print(f"MP3 saved at: {mp3_path}")
