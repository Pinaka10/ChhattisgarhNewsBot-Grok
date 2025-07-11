{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
"""\
Hindi Content Auditor\
Professional Hindi standards enforcement\
Zero-cost local processing\
"""\
\
import json\
import re\
import logging\
from datetime import datetime\
import os\
\
# Setup logging\
logging.basicConfig(\
    level=logging.INFO,\
    format='%(asctime)s - %(levelname)s - %(message)s',\
    handlers=[\
        logging.FileHandler('logs/auditor.log'),\
        logging.StreamHandler()\
    ]\
)\
\
class HindiContentAuditor:\
    def __init__(self):\
        # Professional replacements for casual/inappropriate terms\
        self.replacements = \{\
            # Casual to formal\
            '\uc0\u2351 \u2366 \u2352 ': '\u2350 \u2367 \u2340 \u2381 \u2352 ',\
            '\uc0\u2349 \u2366 \u2312 ': '\u2357 \u2381 \u2351 \u2325 \u2381 \u2340 \u2367 ',\
            '\uc0\u2309 \u2352 \u2375 ': '',\
            '\uc0\u2357 \u2366 \u2361 ': '',\
            '\uc0\u2332 \u2348 \u2352 \u2342 \u2360 \u2381 \u2340 ': '\u2350 \u2361 \u2340 \u2381 \u2357 \u2346 \u2370 \u2352 \u2381 \u2339 ',\
            '\uc0\u2325 \u2350 \u2366 \u2354 ': '\u2313 \u2354 \u2381 \u2354 \u2375 \u2326 \u2344 \u2368 \u2351 ',\
            '\uc0\u2343 \u2350 \u2366 \u2325 \u2366 ': '\u2328 \u2335 \u2344 \u2366 ',\
            '\uc0\u2348 \u2357 \u2366 \u2354 ': '\u2357 \u2367 \u2357 \u2366 \u2342 ',\
            '\uc0\u2347 \u2335 \u2366 \u2347 \u2335 ': '\u2340 \u2369 \u2352 \u2306 \u2340 ',\
            '\uc0\u2333 \u2335 \u2346 \u2335 ': '\u2358 \u2368 \u2328 \u2381 \u2352 ',\
            \
            # English to Hindi\
            'shocking': '\uc0\u2330 \u2367 \u2306 \u2340 \u2366 \u2332 \u2344 \u2325 ',\
            'awesome': '\uc0\u2350 \u2361 \u2340 \u2381 \u2357 \u2346 \u2370 \u2352 \u2381 \u2339 ',\
            'amazing': '\uc0\u2310 \u2358 \u2381 \u2330 \u2352 \u2381 \u2351 \u2332 \u2344 \u2325 ',\
            'fantastic': '\uc0\u2313 \u2340 \u2381 \u2325 \u2371 \u2359 \u2381 \u2335 ',\
            'super': '\uc0\u2309 \u2340 \u2381 \u2351 \u2343 \u2367 \u2325 ',\
            'cool': '\uc0\u2309 \u2330 \u2381 \u2331 \u2366 ',\
            'wow': '',\
            'ok': '\uc0\u2336 \u2368 \u2325 ',\
            'sorry': '\uc0\u2326 \u2375 \u2342 ',\
            'thanks': '\uc0\u2343 \u2344 \u2381 \u2351 \u2357 \u2366 \u2342 ',\
            \
            # Inappropriate terms (replace with professional alternatives)\
            '\uc0\u2350 \u2366 \u2352 ': '\u2361 \u2350 \u2354 \u2366 ',\
            '\uc0\u2346 \u2368 \u2335 ': '\u2346 \u2381 \u2352 \u2361 \u2366 \u2352 ',\
            '\uc0\u2347 \u2306 \u2360 \u2366 ': '\u2327 \u2367 \u2352 \u2347 \u2381 \u2340 \u2366 \u2352 ',\
            '\uc0\u2346 \u2325 \u2337 \u2364 \u2366 ': '\u2327 \u2367 \u2352 \u2347 \u2381 \u2340 \u2366 \u2352 ',\
            '\uc0\u2349 \u2366 \u2327 \u2366 ': '\u2347 \u2352 \u2366 \u2352 ',\
            '\uc0\u2331 \u2369 \u2346 \u2366 ': '\u2309 \u2332 \u2381 \u2334 \u2366 \u2340  \u2360 \u2381 \u2341 \u2366 \u2344  \u2346 \u2352 ',\
            \
            # Sensational to neutral\
            '\uc0\u2360 \u2344 \u2360 \u2344 \u2368 \u2326 \u2375 \u2332 ': '\u2350 \u2361 \u2340 \u2381 \u2357 \u2346 \u2370 \u2352 \u2381 \u2339 ',\
            '\uc0\u2361 \u2376 \u2352 \u2366 \u2344 ': '\u2310 \u2358 \u2381 \u2330 \u2352 \u2381 \u2351 \u2330 \u2325 \u2367 \u2340 ',\
            '\uc0\u2346 \u2352 \u2375 \u2358 \u2366 \u2344 ': '\u2330 \u2367 \u2306 \u2340 \u2367 \u2340 ',\
            '\uc0\u2327 \u2369 \u2360 \u2381 \u2360 \u2366 ': '\u2344 \u2366 \u2352 \u2366 \u2332 \u2364 ',\
            '\uc0\u2326 \u2369 \u2358 ': '\u2346 \u2381 \u2352 \u2360 \u2344 \u2381 \u2344 '\
        \}\
        \
        # Words to remove completely\
        self.remove_words = [\
            '\uc0\u2309 \u2352 \u2375 ', '\u2357 \u2366 \u2361 ', '\u2361 \u2366 \u2351 ', '\u2323 \u2361 ', '\u2310 \u2361 ', '\u2313 \u2347 \u2381 \u2347 ', '\u2331 \u2368 ', '\u2341 \u2370 ',\
            'wow', 'omg', 'wtf', 'damn', 'shit', 'fuck', 'hell'\
        ]\
        \
        # Professional news prefixes\
        self.news_categories = \{\
            'crime': '\uc0\u55357 \u57000 ',\
            'politics': '\uc0\u55357 \u56524 ',\
            'development': '\uc0\u55356 \u57303 \u65039 ',\
            'education': '\uc0\u55357 \u56538 ',\
            'health': '\uc0\u55356 \u57317 ',\
            'sports': '\uc0\u9917 ',\
            'weather': '\uc0\u55356 \u57124 \u65039 ',\
            'economy': '\uc0\u55357 \u56496 ',\
            'agriculture': '\uc0\u55356 \u57150 ',\
            'technology': '\uc0\u55357 \u56507 '\
        \}\
    \
    def clean_text(self, text):\
        """Clean and professionalize text"""\
        if not text:\
            return text\
        \
        # Convert to string if not already\
        text = str(text)\
        \
        # Remove extra whitespace\
        text = re.sub(r'\\s+', ' ', text).strip()\
        \
        # Apply replacements\
        for old_word, new_word in self.replacements.items():\
            # Case-insensitive replacement\
            pattern = re.compile(re.escape(old_word), re.IGNORECASE)\
            text = pattern.sub(new_word, text)\
        \
        # Remove inappropriate words\
        for word in self.remove_words:\
            pattern = re.compile(r'\\b' + re.escape(word) + r'\\b', re.IGNORECASE)\
            text = pattern.sub('', text)\
        \
        # Clean up extra spaces after removals\
        text = re.sub(r'\\s+', ' ', text).strip()\
        \
        # Ensure proper sentence structure\
        text = self.fix_sentence_structure(text)\
        \
        return text\
    \
    def fix_sentence_structure(self, text):\
        """Fix basic sentence structure issues"""\
        if not text:\
            return text\
        \
        # Ensure first letter is capitalized\
        if text and text[0].islower():\
            text = text[0].upper() + text[1:]\
        \
        # Remove multiple punctuation\
        text = re.sub(r'[\uc0\u2404 .]\{2,\}', '\u2404 ', text)\
        text = re.sub(r'[!]\{2,\}', '!', text)\
        text = re.sub(r'[?]\{2,\}', '?', text)\
        \
        # Ensure proper ending punctuation\
        if text and text[-1] not in '\uc0\u2404 .!?':\
            text += '\uc0\u2404 '\
        \
        return text\
    \
    def categorize_news(self, title):\
        """Categorize news and add appropriate emoji"""\
        title_lower = title.lower()\
        \
        crime_keywords = ['\uc0\u2346 \u2369 \u2354 \u2367 \u2360 ', '\u2327 \u2367 \u2352 \u2347 \u2381 \u2340 \u2366 \u2352 ', '\u2330 \u2379 \u2352 \u2368 ', '\u2361 \u2340 \u2381 \u2351 \u2366 ', '\u2309 \u2346 \u2352 \u2366 \u2343 ', '\u2350 \u2366 \u2350 \u2354 \u2366 ', '\u2347 \u2381 \u2352 \u2377 \u2337 ']\
        politics_keywords = ['\uc0\u2350 \u2369 \u2326 \u2381 \u2351 \u2350 \u2306 \u2340 \u2381 \u2352 \u2368 ', '\u2350 \u2306 \u2340 \u2381 \u2352 \u2368 ', '\u2357 \u2367 \u2343 \u2366 \u2351 \u2325 ', '\u2330 \u2369 \u2344 \u2366 \u2357 ', '\u2360 \u2352 \u2325 \u2366 \u2352 ', '\u2344 \u2375 \u2340 \u2366 ']\
        development_keywords = ['\uc0\u2357 \u2367 \u2325 \u2366 \u2360 ', '\u2351 \u2379 \u2332 \u2344 \u2366 ', '\u2346 \u2352 \u2367 \u2351 \u2379 \u2332 \u2344 \u2366 ', '\u2344 \u2367 \u2352 \u2381 \u2350 \u2366 \u2339 ', '\u2313 \u2342 \u2381 \u2328 \u2366 \u2335 \u2344 ']\
        \
        if any(keyword in title_lower for keyword in crime_keywords):\
            return '\uc0\u55357 \u57000 '\
        elif any(keyword in title_lower for keyword in politics_keywords):\
            return '\uc0\u55357 \u56524 '\
        elif any(keyword in title_lower for keyword in development_keywords):\
            return '\uc0\u55356 \u57303 \u65039 '\
        else:\
            return '\uc0\u55357 \u56560 '\
    \
    def audit_news_item(self, news_item):\
        """Audit a single news item"""\
        try:\
            audited_item = news_item.copy()\
            \
            # Clean the title\
            original_title = news_item.get('title', '')\
            cleaned_title = self.clean_text(original_title)\
            \
            # Add category emoji\
            emoji = self.categorize_news(cleaned_title)\
            audited_item['title'] = f"\{emoji\} \{cleaned_title\}"\
            \
            # Track changes\
            audited_item['audit_info'] = \{\
                'original_title': original_title,\
                'cleaned_title': cleaned_title,\
                'changes_made': original_title != cleaned_title,\
                'audit_timestamp': datetime.now().isoformat()\
            \}\
            \
            return audited_item\
            \
        except Exception as e:\
            logging.error(f"Error auditing news item: \{str(e)\}")\
            return news_item\
    \
    def audit_news_data(self, news_data):\
        """Audit all news data"""\
        if not news_data:\
            return []\
        \
        audited_data = []\
        changes_count = 0\
        \
        for item in news_data:\
            audited_item = self.audit_news_item(item)\
            audited_data.append(audited_item)\
            \
            if audited_item.get('audit_info', \{\}).get('changes_made', False):\
                changes_count += 1\
        \
        logging.info(f"Audited \{len(news_data)\} items, made changes to \{changes_count\} items")\
        return audited_data\
    \
    def save_audited_news(self, audited_data):\
        """Save audited news data"""\
        try:\
            os.makedirs('data', exist_ok=True)\
            \
            filename = f"data/audited_news_\{datetime.now().strftime('%Y%m%d_%H%M')\}.json"\
            \
            with open(filename, 'w', encoding='utf-8') as f:\
                json.dump(audited_data, f, ensure_ascii=False, indent=2)\
            \
            # Save as latest audited\
            with open('data/latest_audited.json', 'w', encoding='utf-8') as f:\
                json.dump(audited_data, f, ensure_ascii=False, indent=2)\
            \
            logging.info(f"Audited news saved to \{filename\}")\
            return filename\
            \
        except Exception as e:\
            logging.error(f"Error saving audited news: \{str(e)\}")\
            return None\
\
def main():\
    """Main auditing function"""\
    logging.info("Starting Hindi content audit...")\
    \
    try:\
        # Load latest news data\
        with open('data/latest.json', 'r', encoding='utf-8') as f:\
            news_data = json.load(f)\
        \
        auditor = HindiContentAuditor()\
        audited_data = auditor.audit_news_data(news_data)\
        \
        if audited_data:\
            filename = auditor.save_audited_news(audited_data)\
            if filename:\
                logging.info(f"Successfully audited \{len(audited_data)\} news items")\
            else:\
                logging.error("Failed to save audited data")\
        else:\
            logging.warning("No audited data to save")\
            \
    except FileNotFoundError:\
        logging.error("No news data found to audit")\
    except Exception as e:\
        logging.error(f"Error in auditing process: \{str(e)\}")\
\
if __name__ == "__main__":\
    main()}