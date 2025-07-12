# Chhattisgarh News Auditor
# Audits news for professional Hindi standards with sentiment/bias detection

import re
import os
import time
from indicnlp.tokenize import sentence_tokenize
from indicnlp.sentiment import SentimentAnalyzer

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
with open('logs/auditor.log', 'a') as log_file:
    log_file.write(f"{time.ctime()} - Auditor started\n")

# Professional replacements and removal list
REPLACEMENTS = {
    "यार": "मित्र", "भाई": "व्यक्ति", "अरे": "", "वाह": "", "जबरदस्त": "महत्वपूर्ण",
    "कमाल": "उल्लेखनीय", "धमाका": "घटना", "बवाल": "विवाद", "फटाफट": "तुरंत",
    "झटपट": "शीघ्र", "शocking": "चिंताजनक", "awesome": "महत्वपूर्ण",
    "amazing": "आश्चर्यजनक", "fantastic": "उत्कृष्ट", "super": "अत्यधिक",
    "cool": "अच्छा", "wow": "", "ok": "ठीक", "sorry": "खेद", "thanks": "धन्यवाद",
    "मार": "हमला", "पीट": "प्रहार", "फंसा": "गिरफ्तार", "पकड़ा": "गिरफ्तार",
    "भागा": "फरार", "छुपा": "अज्ञात स्थान पर", "सनसनीखेज": "महत्वपूर्ण",
    "हैरान": "आश्चर्यचकित", "परेशान": "चिंतित", "गुस्सा": "नाराज़", "खुश": "प्रसन्न"
}
REMOVE_WORDS = ["अरे", "वाह", "हाय", "ओह", "आह", "उफ्फ", "छी", "थू", "wow", "omg", "wtf", "damn", "shit", "fuck", "hell"]

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()

def clean_text(text):
    if not text:
        return text
    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()
    for old_word, new_word in REPLACEMENTS.items():
        text = re.sub(re.escape(old_word), new_word, text, flags=re.IGNORECASE)
    for word in REMOVE_WORDS:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    if text and text[-1] not in '।.!?':
        text = text + '।'
    return text

def categorize_news(title):
    title_lower = title.lower()
    categories = {
        "crime": ["पुलिस", "गिरफ्तार", "चोरी", "हत्या", "अपराध", "मामला", "फ्रॉड"],
        "politics": ["मुख्यमंत्री", "मंत्री", "विधायक", "चुनाव", "सरकार", "नेता"],
        "development": ["विकास", "योजना", "परियोजना", "निर्माण", "उद्घाटन"]
    }
    for cat, keywords in categories.items():
        if any(keyword in title_lower for keyword in keywords):
            return {"category": cat, "emoji": {"crime": "🚨", "politics": "📌", "development": "🏗️"}.get(cat, "📰")}
    return {"category": "general", "emoji": "📰"}

def audit_sentiment(item):
    sentences = sentence_tokenize.sentence_split(item["headline"], lang="hi")
    sentiment = analyzer.get_sentiment(sentences)
    if sentiment["compound"] < -0.8:  # Highly negative sentiment
        with open('logs/auditor.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - Rejected {item['headline']} due to high negativity\n")
        return False
    return True

def audit_news(items):
    verified = []
    for item in items:
        cleaned_text = clean_text(item["headline"])
        if not cleaned_text:
            continue
        category_info = categorize_news(cleaned_text)
        if audit_sentiment({"headline": cleaned_text}):
            item["headline"] = f"{category_info['emoji']} {cleaned_text}"
            item["category"] = category_info["category"]
            item["audit_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            verified.append(item)
        with open('logs/auditor.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - Audited {item['headline']} as {category_info['category']}\n")
    return verified

if __name__ == "__main__":
    # Example usage with test data
    test_items = [{"headline": "जबरदस्त बारिश ने रायपुर को प्रभावित किया", "source": "Test", "date": time.strftime("%Y-%m-%d")}]
    audited_items = audit_news(test_items)
    with open('data/audited_news.json', 'w', encoding='utf-8') as f:
        json.dump(audited_items, f, ensure_ascii=False, indent=2)
