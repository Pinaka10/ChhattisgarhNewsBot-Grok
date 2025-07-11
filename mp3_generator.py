#!/usr/bin/env python3
"""
MP3 Audio Generator
Hindi text-to-speech conversion
Zero-cost using gTTS free tier
"""

import json
import logging
from datetime import datetime
import os
from gtts import gTTS
import tempfile

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mp3_generator.log'),
        logging.StreamHandler()
    ]
)

class MP3Generator:
    def __init__(self):
        self.max_chars = 4500  # Stay within gTTS free tier limits
    
    def create_news_bulletin(self, news_data):
        """Create formatted news bulletin text"""
        if not news_data:
            return "आज कोई समाचार उपलब्ध नहीं है।"
        
        # Create bulletin header
        current_date = datetime.now().strftime('%d %B %Y')
        bulletin_text = f"छत्तीसगढ़ न्यूज़ बॉट प्रस्तुत करता है {current_date} की मुख्य खबरें।\n\n"
        
        # Add top news items
        for i, item in enumerate(news_data[:6], 1):  # Limit to 6 items
            title = item.get('title', '').replace('🚨', '').replace('📌', '').replace('🏗️', '').replace('📰', '').strip()
            
            # Clean title for audio
            title = self.clean_for_audio(title)
            
            bulletin_text += f"खबर नंबर {i}। {title}।\n\n"
            
            # Check character limit
            if len(bulletin_text) > self.max_chars:
                bulletin_text = bulletin_text[:self.max_chars] + "।"
                break
        
        bulletin_text += "यह थी आज की मुख्य खबरें। छत्तीसगढ़ न्यूज़ बॉट के साथ जुड़े रहें।"
        
        return bulletin_text
    
    def clean_for_audio(self, text):
        """Clean text for better audio pronunciation"""
        if not text:
            return text
        
        # Replace numbers with Hindi words
        number_replacements = {
            '1': 'एक',
            '2': 'दो',
            '3': 'तीन',
            '4': 'चार',
            '5': 'पांच',
            '6': 'छह',
            '7': 'सात',
            '8': 'आठ',
            '9': 'नौ',
            '10': 'दस',
            '20': 'बीस',
            '30': 'तीस',
            '50': 'पचास',
            '100': 'सौ',
            '1000': 'हजार',
            '10000': 'दस हजार',
            '100000': 'एक लाख',
            '1000000': 'दस लाख'
        }
        
        for num, word in number_replacements.items():
            text = text.replace(num, word)
        
        # Remove special characters that might cause pronunciation issues
        text = text.replace('&', 'और')
        text = text.replace('%', 'प्रतिशत')
        text = text.replace('@', 'एट')
        text = text.replace('#', 'हैशटैग')
        
        # Clean up extra spaces
        text = ' '.join(text.split())
        
        return text
    
    def generate_mp3(self, text, filename):
        """Generate MP3 from text using gTTS"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='hi', slow=False)
            
            # Save to temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                tts.save(temp_file.name)
                
            # Move to final location
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            os.rename(temp_file.name, filename)
            
            logging.info(f"MP3 generated successfully: {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating MP3: {str(e)}")
            return False
    
    def create_audio_bulletin(self, news_data):
        """Create complete audio bulletin"""
        try:
            # Create bulletin text
            bulletin_text = self.create_news_bulletin(news_data)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            filename = f"audio/bulletin_{timestamp}.mp3"
            
            # Generate MP3
            success = self.generate_mp3(bulletin_text, filename)
            
            if success:
                # Also save as latest.mp3
                latest_filename = "audio/latest.mp3"
                os.makedirs(os.path.dirname(latest_filename), exist_ok=True)
                
                import shutil
                shutil.copy2(filename, latest_filename)
                
                # Save bulletin text for reference
                text_filename = f"audio/bulletin_{timestamp}.txt"
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(bulletin_text)
                
                logging.info(f"Audio bulletin created: {filename}")
                return filename, bulletin_text
            else:
                return None, None
                
        except Exception as e:
            logging.error(f"Error creating audio bulletin: {str(e)}")
            return None, None

def main():
    """Main MP3 generation function"""
    logging.info("Starting MP3 generation...")
    
    try:
        # Load audited news data
        with open('data/latest_audited.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        generator = MP3Generator()
        filename, bulletin_text = generator.create_audio_bulletin(news_data)
        
        if filename:
            logging.info(f"Successfully generated audio bulletin")
            logging.info(f"Text length: {len(bulletin_text)} characters")
        else:
            logging.error("Failed to generate audio bulletin")
            
    except FileNotFoundError:
        logging.error("No audited news data found")
    except Exception as e:
        logging.error(f"Error in MP3 generation: {str(e)}")

if __name__ == "__main__":
    main()
