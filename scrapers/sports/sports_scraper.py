"""
Sports & Entertainment scraper using free sports APIs.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper

class SportsScraper(BaseScraper):
    """Scraper for sports and entertainment content."""
    
    def __init__(self):
        super().__init__('sports')
    
    def scrape_sports_data(self) -> List[Dict]:
        """Scrape sports data from free APIs."""
        try:
            sports_data = []
            # ESPN RSS feeds are free
            import feedparser
            feed = feedparser.parse('https://www.espn.com/espn/rss/news')
            
            for entry in feed.entries[:10]:
                sports_data.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': 'ESPN RSS',
                    'scraped_at': datetime.now().isoformat()
                })
            
            return sports_data
        except Exception as e:
            self.logger.error(f"Error scraping sports data: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        return self.scrape_sports_data()
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for sports scraping."""
        return {
            'ESPN RSS': 'Free sports news feeds',
            'Sports Open Data': 'Free datasets for various sports',
            'The Sports DB': 'Free sports database API',
            'ESPN API': 'Limited free access to sports data',
            'NBA API': 'Free access to NBA statistics'
        }