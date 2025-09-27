#!/usr/bin/env python3
"""
Main orchestrator for the Botsy information scraping framework.
"""
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.dirname(__file__))

# Import all scrapers
from scrapers.news.news_scraper import NewsScraper
from scrapers.finance.finance_scraper import FinanceScraper
from scrapers.technology.tech_scraper import TechnologyScraper
from scrapers.research.research_scraper import ResearchScraper
from scrapers.weather.weather_scraper import WeatherScraper
from scrapers.social.social_scraper import SocialScraper
from scrapers.government.government_scraper import GovernmentScraper
from scrapers.sports.sports_scraper import SportsScraper
from scrapers.ecommerce.ecommerce_scraper import EcommerceScraper
from scrapers.health.health_scraper import HealthScraper

from utils.logger import setup_logger

class BotsyOrchestrator:
    """Main orchestrator for all scraping categories."""
    
    def __init__(self):
        self.logger = setup_logger('botsy_main')
        self.scrapers = {
            'news': NewsScraper,
            'finance': FinanceScraper,
            'technology': TechnologyScraper,
            'research': ResearchScraper,
            'weather': WeatherScraper,
            'social': SocialScraper,
            'government': GovernmentScraper,
            'sports': SportsScraper,
            'ecommerce': EcommerceScraper,
            'health': HealthScraper
        }
    
    def run_category(self, category: str) -> List[Dict[str, Any]]:
        """Run scraper for a specific category."""
        if category not in self.scrapers:
            self.logger.error(f"Unknown category: {category}")
            return []
        
        try:
            scraper_class = self.scrapers[category]
            scraper = scraper_class()
            
            self.logger.info(f"Starting scraper for category: {category}")
            start_time = datetime.now()
            
            data = scraper.scrape()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"Completed {category} scraping in {duration:.2f} seconds. Collected {len(data)} items.")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error running {category} scraper: {e}")
            return []
    
    def run_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run all scrapers."""
        self.logger.info("Starting comprehensive scraping for all categories")
        results = {}
        
        for category in self.scrapers.keys():
            results[category] = self.run_category(category)
        
        total_items = sum(len(data) for data in results.values())
        self.logger.info(f"Comprehensive scraping completed. Total items collected: {total_items}")
        
        return results
    
    def show_available_tools(self):
        """Display all available tools for each category."""
        print("\n🔧 AVAILABLE TOOLS BY CATEGORY\n" + "="*50)
        
        for category, scraper_class in self.scrapers.items():
            scraper = scraper_class()
            tools = scraper.get_available_tools()
            
            print(f"\n📂 {category.upper()}")
            print("-" * 30)
            for tool, description in tools.items():
                print(f"• {tool}: {description}")
        
        print("\n" + "="*50)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Botsy Information Scraping Framework')
    parser.add_argument('--category', '-c', 
                       choices=['news', 'finance', 'technology', 'research', 'weather', 
                               'social', 'government', 'sports', 'ecommerce', 'health'],
                       help='Scrape specific category')
    parser.add_argument('--all', '-a', action='store_true', 
                       help='Scrape all categories')
    parser.add_argument('--tools', '-t', action='store_true',
                       help='Show available tools for each category')
    
    args = parser.parse_args()
    
    orchestrator = BotsyOrchestrator()
    
    if args.tools:
        orchestrator.show_available_tools()
    elif args.category:
        orchestrator.run_category(args.category)
    elif args.all:
        orchestrator.run_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()