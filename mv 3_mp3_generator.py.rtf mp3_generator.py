{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
"""\
MP3 Audio Generator\
Hindi text-to-speech conversion\
Zero-cost using gTTS free tier\
"""\
\
import json\
import logging\
from datetime import datetime\
import os\
from gtts import gTTS\
import tempfile\
\
# Setup logging\
logging.basicConfig(\
    level=logging.INFO,\
    format='%(asctime)s - %(levelname)s - %(message)s',\
    handlers=[\
        logging.FileHandler('logs/mp3_generator.log'),\
        logging.StreamHandler()\
    ]\
)\
\
class MP3Generator:\
    def __init__(self):\
        self.max_chars = 4500  # Stay within gTTS free tier limits\
        \
    def create_news_bulletin(self, news_data):\
        """Create formatted news bulletin text"""\
        if not news_data:\
            return "\uc0\u2310 \u2332  \u2325 \u2379 \u2312  \u2360 \u2350 \u2366 \u2330 \u2366 \u2352  \u2313 \u2346 \u2354 \u2348 \u2381 \u2343  \u2344 \u2361 \u2368 \u2306  \u2361 \u2376 \u2404 "\
        \
        # Create bulletin header\
        current_date = datetime.now().strftime('%d %B %Y')\
        bulletin_text = f"\uc0\u2331 \u2340 \u2381 \u2340 \u2368 \u2360 \u2327 \u2338 \u2364  \u2344 \u2381 \u2351 \u2370 \u2332 \u2364  \u2348 \u2377 \u2335  \u2346 \u2381 \u2352 \u2360 \u2381 \u2340 \u2369 \u2340  \u2325 \u2352 \u2340 \u2366  \u2361 \u2376  \{current_date\} \u2325 \u2368  \u2350 \u2369 \u2326 \u2381 \u2351  \u2326 \u2348 \u2352 \u2375 \u2306 \u2404 \\n\\n"\
        \
        # Add top news items\
        for i, item in enumerate(news_data[:6], 1):  # Limit to 6 items\
            title = item.get('title', '').replace('\uc0\u55357 \u57000 ', '').replace('\u55357 \u56524 ', '').replace('\u55356 \u57303 \u65039 ', '').replace('\u55357 \u56560 ', '').strip()\
            \
            # Clean title for audio\
            title = self.clean_for_audio(title)\
            \
            bulletin_text += f"\uc0\u2326 \u2348 \u2352  \u2344 \u2306 \u2348 \u2352  \{i\}\u2404  \{title\}\u2404 \\n\\n"\
            \
            # Check character limit\
            if len(bulletin_text) > self.max_chars:\
                bulletin_text = bulletin_text[:self.max_chars] + "\uc0\u2404 "\
                break\
        \
        bulletin_text += "\uc0\u2351 \u2361  \u2341 \u2368  \u2310 \u2332  \u2325 \u2368  \u2350 \u2369 \u2326 \u2381 \u2351  \u2326 \u2348 \u2352 \u2375 \u2306 \u2404  \u2331 \u2340 \u2381 \u2340 \u2368 \u2360 \u2327 \u2338 \u2364  \u2344 \u2381 \u2351 \u2370 \u2332 \u2364  \u2348 \u2377 \u2335  \u2325 \u2375  \u2360 \u2366 \u2341  \u2332 \u2369 \u2337 \u2364 \u2375  \u2352 \u2361 \u2375 \u2306 \u2404 "\
        \
        return bulletin_text\
    \
    def clean_for_audio(self, text):\
        """Clean text for better audio pronunciation"""\
        if not text:\
            return text\
        \
        # Replace numbers with Hindi words\
        number_replacements = \{\
            '1': '\uc0\u2319 \u2325 ',\
            '2': '\uc0\u2342 \u2379 ',\
            '3': '\uc0\u2340 \u2368 \u2344 ',\
            '4': '\uc0\u2330 \u2366 \u2352 ',\
            '5': '\uc0\u2346 \u2366 \u2306 \u2330 ',\
            '6': '\uc0\u2331 \u2361 ',\
            '7': '\uc0\u2360 \u2366 \u2340 ',\
            '8': '\uc0\u2310 \u2336 ',\
            '9': '\uc0\u2344 \u2380 ',\
            '10': '\uc0\u2342 \u2360 ',\
            '20': '\uc0\u2348 \u2368 \u2360 ',\
            '30': '\uc0\u2340 \u2368 \u2360 ',\
            '50': '\uc0\u2346 \u2330 \u2366 \u2360 ',\
            '100': '\uc0\u2360 \u2380 ',\
            '1000': '\uc0\u2361 \u2332 \u2366 \u2352 ',\
            '10000': '\uc0\u2342 \u2360  \u2361 \u2332 \u2366 \u2352 ',\
            '100000': '\uc0\u2319 \u2325  \u2354 \u2366 \u2326 ',\
            '1000000': '\uc0\u2342 \u2360  \u2354 \u2366 \u2326 '\
        \}\
        \
        for num, word in number_replacements.items():\
            text = text.replace(num, word)\
        \
        # Remove special characters that might cause pronunciation issues\
        text = text.replace('&', '\uc0\u2324 \u2352 ')\
        text = text.replace('%', '\uc0\u2346 \u2381 \u2352 \u2340 \u2367 \u2358 \u2340 ')\
        text = text.replace('@', '\uc0\u2319 \u2335 ')\
        text = text.replace('#', '\uc0\u2361 \u2376 \u2358 \u2335 \u2376 \u2327 ')\
        \
        # Clean up extra spaces\
        text = ' '.join(text.split())\
        \
        return text\
    \
    def generate_mp3(self, text, filename):\
        """Generate MP3 from text using gTTS"""\
        try:\
            # Create gTTS object\
            tts = gTTS(text=text, lang='hi', slow=False)\
            \
            # Save to temporary file first\
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:\
                tts.save(temp_file.name)\
                \
            # Move to final location\
            os.makedirs(os.path.dirname(filename), exist_ok=True)\
            os.rename(temp_file.name, filename)\
            \
            logging.info(f"MP3 generated successfully: \{filename\}")\
            return True\
            \
        except Exception as e:\
            logging.error(f"Error generating MP3: \{str(e)\}")\
            return False\
    \
    def create_audio_bulletin(self, news_data):\
        """Create complete audio bulletin"""\
        try:\
            # Create bulletin text\
            bulletin_text = self.create_news_bulletin(news_data)\
            \
            # Generate filename\
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')\
            filename = f"audio/bulletin_\{timestamp\}.mp3"\
            \
            # Generate MP3\
            success = self.generate_mp3(bulletin_text, filename)\
            \
            if success:\
                # Also save as latest.mp3\
                latest_filename = "audio/latest.mp3"\
                os.makedirs(os.path.dirname(latest_filename), exist_ok=True)\
                \
                import shutil\
                shutil.copy2(filename, latest_filename)\
                \
                # Save bulletin text for reference\
                text_filename = f"audio/bulletin_\{timestamp\}.txt"\
                with open(text_filename, 'w', encoding='utf-8') as f:\
                    f.write(bulletin_text)\
                \
                logging.info(f"Audio bulletin created: \{filename\}")\
                return filename, bulletin_text\
            else:\
                return None, None\
                \
        except Exception as e:\
            logging.error(f"Error creating audio bulletin: \{str(e)\}")\
            return None, None\
\
def main():\
    """Main MP3 generation function"""\
    logging.info("Starting MP3 generation...")\
    \
    try:\
        # Load audited news data\
        with open('data/latest_audited.json', 'r', encoding='utf-8') as f:\
            news_data = json.load(f)\
        \
        generator = MP3Generator()\
        filename, bulletin_text = generator.create_audio_bulletin(news_data)\
        \
        if filename:\
            logging.info(f"Successfully generated audio bulletin")\
            logging.info(f"Text length: \{len(bulletin_text)\} characters")\
        else:\
            logging.error("Failed to generate audio bulletin")\
            \
    except FileNotFoundError:\
        logging.error("No audited news data found")\
    except Exception as e:\
        logging.error(f"Error in MP3 generation: \{str(e)\}")\
\
if __name__ == "__main__":\
    main()}