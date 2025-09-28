"""
Health & Medical scraper using free medical APIs.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper

class HealthScraper(BaseScraper):
    """Scraper for health and medical information."""
    
    def __init__(self):
        super().__init__('health')
    
    def scrape_health_news(self) -> List[Dict]:
        """Scrape health news from free sources."""
        try:
            health_articles = []
            # CDC RSS feeds are free
            import feedparser
            feed = feedparser.parse('https://tools.cdc.gov/api/v2/resources/media/316422.rss')
            
            for entry in feed.entries[:10]:
                health_articles.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'source': 'CDC RSS',
                    'scraped_at': datetime.now().isoformat()
                })
            
            return health_articles
        except Exception as e:
            self.logger.error(f"Error scraping health news: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        return self.scrape_health_news()
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for health scraping."""
        return {
            'CDC API': 'Free access to health data and statistics',
            'NIH API': 'Free access to medical research',
            'PubMed API': 'Free access to biomedical literature',
            'WHO API': 'Free access to global health data',
            'FDA API': 'Free access to drug and device information',
            'NCBI API': 'Free access to biological databases'
        }