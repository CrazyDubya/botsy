"""
Health & Medical scraper using free medical APIs and WHO RSS.
"""
import sys
import os
import feedparser
from typing import Dict, List, Any
from datetime import datetime
from models.health_model import HealthData

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper

class HealthScraper(BaseScraper):
    """Scraper for health and medical information."""
    
    def __init__(self):
        super().__init__('health')
    
    def scrape_cdc_news(self) -> List[HealthData]:
        """Scrape health news from CDC RSS."""
        try:
            health_articles = []
            feed_url = 'https://tools.cdc.gov/api/v2/resources/media/316422.rss'
            self.logger.info(f"Fetching CDC RSS from {feed_url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:10]:
                data = HealthData(
                    title=entry.get('title', ''),
                    link=entry.get('link', ''),
                    description=entry.get('description', ''),
                    published=entry.get('published', ''),
                    source='CDC RSS',
                    category='health'
                )
                health_articles.append(data)
            
            return health_articles
        except Exception as e:
            self.logger.error(f"Error scraping CDC news: {e}")
            self.error_logger.error(f"Error scraping CDC news: {e}")
            return []

    async def scrape_who_news(self) -> List[HealthData]:
        """Scrape health news from WHO RSS."""
        try:
            health_articles = []
            # WHO News RSS
            url = "https://www.who.int/rss-feeds/news-english.xml"
            self.logger.info(f"Fetching WHO RSS from {url}")

            # Use async request to fetch XML content
            xml_content = await self.make_async_request(url)

            if not xml_content:
                return []

            feed = feedparser.parse(xml_content)

            for entry in feed.entries[:10]:
                 data = HealthData(
                    title=entry.get('title', ''),
                    link=entry.get('link', ''),
                    description=entry.get('description', ''),
                    published=entry.get('published', ''),
                    source='WHO RSS',
                    category='health'
                )
                 health_articles.append(data)

            return health_articles
        except Exception as e:
            self.logger.error(f"Error scraping WHO news: {e}")
            self.error_logger.error(f"Error scraping WHO news: {e}")
            return []

    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        # This synchronous method is kept for backward compatibility if needed,
        # but the main runner will likely use specific methods or we can run async loop here.
        # For now, let's just return CDC data synchronously.
        return [item.model_dump() for item in self.scrape_cdc_news()]
    
    async def scrape_async(self) -> List[HealthData]:
        """Async main scraping method combining sources."""
        cdc_data = self.scrape_cdc_news() # synchronous
        who_data = await self.scrape_who_news() # asynchronous
        return cdc_data + who_data

    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for health scraping."""
        return {
            'CDC RSS': 'Free access to health data and statistics via RSS',
            'WHO RSS': 'World Health Organization news feed'
        }
