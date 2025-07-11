#!/usr/bin/env python3
"""
Autonomous Chhattisgarh News Scraper
Zero-cost news collection from public sources
"""

import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
import time
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

class ChhattisgarhNewsScraper:
    def __init__(self):
        self.news_sources = [
            {
                'name': 'Dainik Bhaskar CG',
                'url': 'https://www.bhaskar.com/local/chhattisgarh/',
                'selector': '.news-card h3 a'
            },
            {
                'name': 'Patrika CG',
                'url': 'https://www.patrika.com/raipur-news/',
                'selector': '.story-title a'
            },
            {
                'name': 'Amar Ujala CG',
                'url': 'https://www.amarujala.com/chhattisgarh',
                'selector': '.story-title a'
            }
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.news_data = []
    
    def scrape_source(self, source):
        """Scrape news from a single source"""
        try:
            logging.info(f"Scraping {source['name']}")
            response = requests.get(source['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = soup.select(source['selector'])
            
            source_news = []
            for headline in headlines[:5]:  # Get top 5 news
                title = headline.get_text().strip()
                link = headline.get('href', '')
                
                if title and len(title) > 20:  # Filter meaningful headlines
                    source_news.append({
                        'title': title,
                        'link': link,
                        'source': source['name'],
                        'timestamp': datetime.now().isoformat()
                    })
            
            logging.info(f"Found {len(source_news)} news items from {source['name']}")
            return source_news
            
        except Exception as e:
            logging.error(f"Error scraping {source['name']}: {str(e)}")
            return []
    
    def scrape_all_sources(self):
        """Scrape news from all sources"""
        all_news = []
        
        for source in self.news_sources:
            news_items = self.scrape_source(source)
            all_news.extend(news_items)
            time.sleep(2)  # Be respectful to servers
        
        # Remove duplicates based on title similarity
        unique_news = []
        for news in all_news:
            is_duplicate = False
            for existing in unique_news:
                if self.is_similar(news['title'], existing['title']):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_news.append(news)
        
        logging.info(f"Total unique news items: {len(unique_news)}")
        return unique_news
    
    def is_similar(self, title1, title2):
        """Check if two titles are similar (basic duplicate detection)"""
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return similarity > 0.6  # 60% similarity threshold
    
    def save_news(self, news_data):
        """Save news data to JSON file"""
        try:
            os.makedirs('data', exist_ok=True)
            
            filename = f"data/news_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            # Also save as latest.json for easy access
            with open('data/latest.json', 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"News saved to {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Error saving news: {str(e)}")
            return None

def main():
    """Main scraping function"""
    logging.info("Starting Chhattisgarh news scraping...")
    
    scraper = ChhattisgarhNewsScraper()
    news_data = scraper.scrape_all_sources()
    
    if news_data:
        filename = scraper.save_news(news_data)
        if filename:
            logging.info(f"Successfully scraped and saved {len(news_data)} news items")
        else:
            logging.error("Failed to save news data")
    else:
        logging.warning("No news data collected")

if __name__ == "__main__":
    main()
