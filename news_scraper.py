# Chhattisgarh News Scraper
# Collects news from multiple local sources and X accounts

import requests
from bs4 import BeautifulSoup
import os
import json
from indicnlp.tokenize import sentence_tokenize
import time

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup logging
with open('logs/scraper.log', 'a') as log_file:
    log_file.write(f"{time.ctime()} - Scraper started\n")

# Expanded list of Chhattisgarh sources
SOURCES = {
    "Dainik Bhaskar CG": "https://www.bhaskar.com/chhattisgarh",
    "Patrika CG": "https://www.patrika.com/chhattisgarh",
    "Amar Ujala CG": "https://www.amarujala.com/chhattisgarh",
    "Haribhoomi": "https://haribhoomi.com/chhattisgarh",
    "Nava Bharat": "https://navabharat.com/chhattisgarh",
    "Deshbandhu": "https://deshbandhu.co.in/chhattisgarh",
    "Chhattisgarh Today": "https://chhattisgarhtoday.net"
}

# X API configuration (using Basic tier for verified accounts)
X_API_KEY = "YOUR_X_API_KEY"  # Replace with your X API key from secrets
X_URL = "https://api.twitter.com/2/tweets/search/recent"
X_PARAMS = {
    "query": "Chhattisgarh -is:retweet lang:hi",
    "max_results": 10,
    "user.fields": "verified"
}
X_HEADERS = {"Authorization": f"Bearer {X_API_KEY}"}

def scrape_web_sources():
    results = []
    for name, url in SOURCES.items():
        try:
            response = requests.get(url, headers={"User-Agent": "ChhattisgarhNewsBot/1.0"}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            headlines = soup.select("h3, h2")[:5]  # Target top 5 headlines
            for headline in headlines:
                text = headline.text.strip()
                if len(text) > 20:
                    results.append({"headline": text, "source": name, "date": time.strftime("%Y-%m-%d")})
            time.sleep(2)  # Respect server load
        except Exception as e:
            with open('logs/scraper.log', 'a') as log_file:
                log_file.write(f"{time.ctime()} - Error scraping {name}: {str(e)}\n")
    return results

def scrape_x_accounts():
    results = []
    try:
        response = requests.get(X_URL, headers=X_HEADERS, params=X_PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        for tweet in data.get("data", []):
            if tweet.get("author_id") in ["verified_accounts_ids"]:  # Replace with actual verified IDs
                text = tweet.get("text", "").strip()
                if len(text) > 20:
                    results.append({"headline": text, "source": "X Account", "date": time.strftime("%Y-%m-%d")})
        time.sleep(2)  # Respect API rate limits
    except Exception as e:
        with open('logs/scraper.log', 'a') as log_file:
            log_file.write(f"{time.ctime()} - Error scraping X: {str(e)}\n")
    return results

def remove_duplicates(items):
    unique_items = []
    for item in items:
        is_duplicate = False
        for unique_item in unique_items:
            sentences1 = sentence_tokenize.sentence_split(item["headline"], lang="hi")
            sentences2 = sentence_tokenize.sentence_split(unique_item["headline"], lang="hi")
            if len(sentences1) > 0 and len(sentences2) > 0:
                similarity = sum(1 for s1 in sentences1 for s2 in sentences2 if s1 in s2 or s2 in s1) / max(len(sentences1), len(sentences2))
                if similarity > 0.7:  # 70% semantic similarity threshold
                    is_duplicate = True
                    break
        if not is_duplicate:
            unique_items.append(item)
    return unique_items

def scrape_all():
    web_results = scrape_web_sources()
    x_results = scrape_x_accounts()
    all_results = web_results + x_results
    unique_results = remove_duplicates(all_results)
    with open('logs/scraper.log', 'a') as log_file:
        log_file.write(f"{time.ctime()} - Scraped {len(unique_results)} unique items\n")
    return unique_results[:80]  # Limit to 80 daily

if __name__ == "__main__":
    news_items = scrape_all()
    with open('data/scraped_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
