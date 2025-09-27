"""
News & Media scraper using free APIs and RSS feeds.
"""
import feedparser
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import NEWS_API_KEY, CATEGORIES

class NewsScraper(BaseScraper):
    """Scraper for news and media content."""
    
    def __init__(self):
        super().__init__('news')
        self.api_key = NEWS_API_KEY
        self.rss_feeds = {
            'reuters': 'https://feeds.reuters.com/reuters/topNews',
            'bbc': 'https://feeds.bbci.co.uk/news/rss.xml',
            'techcrunch': 'https://techcrunch.com/feed/',
            'reuters_tech': 'https://feeds.reuters.com/reuters/technologyNews'
        }
    
    def scrape_rss(self, feed_name: str, feed_url: str) -> List[Dict]:
        """Scrape articles from RSS feed."""
        try:
            self.logger.info(f"Scraping RSS feed: {feed_name}")
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'source': feed_name,
                    'scraped_at': datetime.now().isoformat()
                }
                articles.append(article)
            
            self.logger.info(f"Scraped {len(articles)} articles from {feed_name}")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping {feed_name}: {e}")
            return []
    
    def scrape_newsapi(self) -> List[Dict]:
        """Scrape using NewsAPI (requires API key)."""
        if not self.api_key:
            self.logger.warning("NewsAPI key not provided, skipping NewsAPI scraping")
            return []
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.api_key,
                'language': 'en',
                'pageSize': 20
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'scraped_at': datetime.now().isoformat()
                })
            
            self.logger.info(f"Scraped {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping NewsAPI: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        all_articles = []
        
        # Scrape RSS feeds
        for feed_name, feed_url in self.rss_feeds.items():
            articles = self.scrape_rss(feed_name, feed_url)
            all_articles.extend(articles)
        
        # Scrape NewsAPI if key is available
        newsapi_articles = self.scrape_newsapi()
        all_articles.extend(newsapi_articles)
        
        # Save data
        if all_articles:
            self.save_data(all_articles, f"articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_articles
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for news scraping."""
        return {
            'RSS Feeds': 'Free RSS feeds from major news sources (Reuters, BBC, TechCrunch)',
            'NewsAPI': 'Free tier: 1000 requests/month for top headlines',
            'Feedparser': 'Python library for parsing RSS and Atom feeds',
            'Newspaper3k': 'Article extraction and curation library',
            'Beautiful Soup': 'Web scraping for custom news sites'
        }

if __name__ == "__main__":
    scraper = NewsScraper()
    articles = scraper.scrape()
    print(f"Scraped {len(articles)} articles")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")