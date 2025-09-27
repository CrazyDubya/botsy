"""
Base scraper class with common functionality.
"""
import time
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from utils.logger import setup_logger
from config.config import DEFAULT_DELAY, MAX_RETRIES, TIMEOUT

class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, category: str):
        self.category = category
        self.logger = setup_logger(f"{category}_scraper")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Botsy Information Scraper 1.0'
        })
    
    def make_request(self, url: str, params: Dict = None, retries: int = MAX_RETRIES) -> requests.Response:
        """Make HTTP request with retry logic."""
        for attempt in range(retries):
            try:
                self.logger.info(f"Making request to: {url}")
                response = self.session.get(url, params=params, timeout=TIMEOUT)
                response.raise_for_status()
                time.sleep(DEFAULT_DELAY)
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(DEFAULT_DELAY * (attempt + 1))
    
    def save_data(self, data: List[Dict], filename: str):
        """Save scraped data to file."""
        import json
        import os
        
        os.makedirs('data', exist_ok=True)
        filepath = f"data/{self.category}_{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Data saved to: {filepath}")
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> Dict[str, str]:
        """Return dictionary of available tools and their descriptions."""
        pass