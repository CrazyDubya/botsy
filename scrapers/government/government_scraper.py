"""
Government & Legal scraper using free government APIs.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper

class GovernmentScraper(BaseScraper):
    """Scraper for government and legal information."""
    
    def __init__(self):
        super().__init__('government')
    
    def scrape_data_gov(self) -> List[Dict]:
        """Scrape from Data.gov catalog."""
        try:
            # Data.gov CKAN API is free
            url = "https://catalog.data.gov/api/3/action/package_search"
            params = {'q': 'finance', 'rows': 5}
            
            response = self.make_request(url, params)
            data = response.json()
            
            datasets = []
            for dataset in data.get('result', {}).get('results', []):
                datasets.append({
                    'title': dataset.get('title', ''),
                    'name': dataset.get('name', ''),
                    'notes': dataset.get('notes', ''),
                    'organization': dataset.get('organization', {}).get('title', ''),
                    'url': f"https://catalog.data.gov/dataset/{dataset.get('name', '')}",
                    'source': 'Data.gov',
                    'scraped_at': datetime.now().isoformat()
                })
            
            return datasets
        except Exception as e:
            self.logger.error(f"Error scraping Data.gov: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        return self.scrape_data_gov()
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for government scraping."""
        return {
            'SEC EDGAR': 'Free access to SEC filings and reports',
            'Data.gov': 'Free US government datasets',
            'Federal Register API': 'Free access to federal regulations',
            'Congress API': 'Free access to congressional data',
            'Court APIs': 'Various free court record APIs'
        }