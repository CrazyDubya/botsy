"""
E-commerce & Reviews scraper using free APIs and web scraping.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper

class EcommerceScraper(BaseScraper):
    """Scraper for e-commerce and product review data."""
    
    def __init__(self):
        super().__init__('ecommerce')
    
    def scrape_product_data(self) -> List[Dict]:
        """Scrape product data from free APIs."""
        try:
            products = []
            # Fake Store API is free and doesn't require authentication
            response = self.make_request('https://fakestoreapi.com/products')
            data = response.json()
            
            for product in data[:5]:  # Limit to 5 products
                products.append({
                    'title': product.get('title', ''),
                    'price': product.get('price', 0),
                    'description': product.get('description', ''),
                    'category': product.get('category', ''),
                    'rating': product.get('rating', {}),
                    'source': 'Fake Store API',
                    'scraped_at': datetime.now().isoformat()
                })
            
            return products
        except Exception as e:
            self.logger.error(f"Error scraping product data: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        return self.scrape_product_data()
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for e-commerce scraping."""
        return {
            'Fake Store API': 'Free fake e-commerce data for testing',
            'eBay API': 'Free tier: 5000 calls/day',
            'Amazon Product API': 'Limited free access via affiliate programs',
            'Best Buy API': 'Free tier available',
            'Etsy API': 'Free for non-commercial use',
            'Selenium': 'Free web scraping for sites without APIs'
        }