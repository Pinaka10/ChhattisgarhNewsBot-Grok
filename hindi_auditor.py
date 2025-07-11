#!/usr/bin/env python3
"""
Hindi Content Auditor
Professional Hindi standards enforcement
Zero-cost local processing
"""

import json
import re
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/auditor.log'),
        logging.StreamHandler()
    ]
)

class HindiContentAuditor:
    def __init__(self):
        # Professional replacements for casual/inappropriate terms
        self.replacements = {
            # Casual to formal
            'यार': 'मित्र',
            'भाई': 'व्यक्ति',
            'अरे': '',
            'वाह': '',
            'जबरदस्त': 'महत्वपूर्ण',
            'कमाल': 'उल्लेखनीय',
            'धमाका': 'घटना',
            'बवाल': 'विवाद',
            'फटाफट': 'तुरंत',
            'झटपट': 'शीघ्र',
            
            # English to Hindi
            'shocking': 'चिंताजनक',
            'awesome': 'महत्वपूर्ण',
            'amazing': 'आश्चर्यजनक',
            'fantastic': 'उत्कृष्ट',
            'super': 'अत्यधिक',
            'cool': 'अच्छा',
            'wow': '',
            'ok': 'ठीक',
            'sorry': 'खेद',
            'thanks': 'धन्यवाद',
            
            # Inappropriate terms (replace with professional alternatives)
            'मार': 'हमला',
            'पीट': 'प्रहार',
            'फंसा': 'गिरफ्तार',
            'पकड़ा': 'गिरफ्तार',
            'भागा': 'फरार',
            'छुपा': 'अज्ञात स्थान पर',
            
            # Sensational to neutral
            'सनसनीखेज': 'महत्वपूर्ण',
            'हैरान': 'आश्चर्यचकित',
            'परेशान': 'चिंतित',
            'गुस्सा': 'नाराज़',
            'खुश': 'प्रसन्न'
        }
        
        # Words to remove completely
        self.remove_words = [
            'अरे', 'वाह', 'हाय', 'ओह', 'आह', 'उफ्फ', 'छी', 'थू',
            'wow', 'omg', 'wtf', 'damn', 'shit', 'fuck', 'hell'
        ]
        
        # Professional news prefixes
        self.news_categories = {
            'crime': '🚨',
            'politics': '📌',
            'development': '🏗️',
            'education': '📚',
            'health': '🏥',
            'sports': '⚽',
            'weather': '🌤️',
            'economy': '💰',
            'agriculture': '🌾',
            'technology': '💻'
        }
    
    def clean_text(self, text):
        """Clean and professionalize text"""
        if not text:
            return text
        
        # Convert to string if not already
        text = str(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Apply replacements
        for old_word, new_word in self.replacements.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old_word), re.IGNORECASE)
            text = pattern.sub(new_word, text)
        
        # Remove inappropriate words
        for word in self.remove_words:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            text = pattern.sub('', text)
        
        # Clean up extra spaces after removals
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Ensure proper sentence structure
        text = self.fix_sentence_structure(text)
        
        return text
    
    def fix_sentence_structure(self, text):
        """Fix basic sentence structure issues"""
        if not text:
            return text
        
        # Ensure first letter is capitalized
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        # Remove multiple punctuation
        text = re.sub(r'[।.]{2,}', '।', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        # Ensure proper ending punctuation
        if text and text[-1] not in '।.!?':
            text += '।'
        
        return text
    
    def categorize_news(self, title):
        """Categorize news and add appropriate emoji"""
        title_lower = title.lower()
        
        crime_keywords = ['पुलिस', 'गिरफ्तार', 'चोरी', 'हत्या', 'अपराध', 'मामला', 'फ्रॉड']
        politics_keywords = ['मुख्यमंत्री', 'मंत्री', 'विधायक', 'चुनाव', 'सरकार', 'नेता']
        development_keywords = ['विकास', 'योजना', 'परियोजना', 'निर्माण', 'उद्घाटन']
        
        if any(keyword in title_lower for keyword in crime_keywords):
            return '🚨'
        elif any(keyword in title_lower for keyword in politics_keywords):
            return '📌'
        elif any(keyword in title_lower for keyword in development_keywords):
            return '🏗️'
        else:
            return '📰'
    
    def audit_news_item(self, news_item):
        """Audit a single news item"""
        try:
            audited_item = news_item.copy()
            
            # Clean the title
            original_title = news_item.get('title', '')
            cleaned_title = self.clean_text(original_title)
            
            # Add category emoji
            emoji = self.categorize_news(cleaned_title)
            audited_item['title'] = f"{emoji} {cleaned_title}"
            
            # Track changes
            audited_item['audit_info'] = {
                'original_title': original_title,
                'cleaned_title': cleaned_title,
                'changes_made': original_title != cleaned_title,
                'audit_timestamp': datetime.now().isoformat()
            }
            
            return audited_item
            
        except Exception as e:
            logging.error(f"Error auditing news item: {str(e)}")
            return news_item
    
    def audit_news_data(self, news_data):
        """Audit all news data"""
        if not news_data:
            return []
        
        audited_data = []
        changes_count = 0
        
        for item in news_data:
            audited_item = self.audit_news_item(item)
            audited_data.append(audited_item)
            
            if audited_item.get('audit_info', {}).get('changes_made', False):
                changes_count += 1
        
        logging.info(f"Audited {len(news_data)} items, made changes to {changes_count} items")
        return audited_data
    
    def save_audited_news(self, audited_data):
        """Save audited news data"""
        try:
            os.makedirs('data', exist_ok=True)
            
            filename = f"data/audited_news_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(audited_data, f, ensure_ascii=False, indent=2)
            
            # Save as latest audited
            with open('data/latest_audited.json', 'w', encoding='utf-8') as f:
                json.dump(audited_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Audited news saved to {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Error saving audited news: {str(e)}")
            return None

def main():
    """Main auditing function"""
    logging.info("Starting Hindi content audit...")
    
    try:
        # Load latest news data
        with open('data/latest.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        auditor = HindiContentAuditor()
        audited_data = auditor.audit_news_data(news_data)
        
        if audited_data:
            filename = auditor.save_audited_news(audited_data)
            if filename:
                logging.info(f"Successfully audited {len(audited_data)} news items")
            else:
                logging.error("Failed to save audited data")
        else:
            logging.warning("No audited data to save")
            
    except FileNotFoundError:
        logging.error("No news data found to audit")
    except Exception as e:
        logging.error(f"Error in auditing process: {str(e)}")

if __name__ == "__main__":
    main()
