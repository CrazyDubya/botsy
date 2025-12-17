#!/usr/bin/env python3
"""
Main orchestrator for the Botsy information scraping framework.
"""
import sys
import os
import argparse
import asyncio
import importlib
import pkgutil
from datetime import datetime
from typing import Dict, List, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add project root to path
sys.path.append(os.path.dirname(__file__))

from utils.logger import setup_logger
from utils.scraper_base import BaseScraper
from utils.config_loader import ConfigManager

class BotsyOrchestrator:
    """Main orchestrator for all scraping categories."""
    
    def __init__(self):
        self.logger = setup_logger('botsy_main')
        self.config = ConfigManager()
        self.console = Console()
        self.scrapers = self._load_scrapers()
    
    def _load_scrapers(self) -> Dict[str, Any]:
        """Dynamically load scrapers from scrapers directory."""
        scrapers = {}
        scrapers_path = os.path.join(os.path.dirname(__file__), 'scrapers')

        for _, category, is_pkg in pkgutil.iter_modules([scrapers_path]):
            if is_pkg:
                try:
                    # Look for a scraper class in the category package
                    # Naming convention: category/category_scraper.py -> CategoryScraper
                    module_name = f"scrapers.{category}.{category}_scraper"
                    module = importlib.import_module(module_name)

                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)
                        if (isinstance(attribute, type) and
                            issubclass(attribute, BaseScraper) and
                            attribute is not BaseScraper):
                            scrapers[category] = attribute
                            self.logger.info(f"Loaded scraper for category: {category}")
                            break
                except ImportError as e:
                    self.logger.error(f"Failed to load scraper for {category}: {e}")
                except Exception as e:
                    self.logger.error(f"Error loading scraper for {category}: {e}")

        return scrapers

    async def run_category_async(self, category: str) -> List[Dict[str, Any]]:
        """Run scraper for a specific category asynchronously."""
        if category not in self.scrapers:
            self.logger.error(f"Unknown category: {category}")
            return []
        
        try:
            scraper_class = self.scrapers[category]
            scraper = scraper_class()
            
            self.logger.info(f"Starting scraper for category: {category}")
            start_time = datetime.now()
            
            # Check if scraper has async capability
            if hasattr(scraper, 'scrape_async'):
                data = await scraper.scrape_async()
            else:
                # Run synchronous scrape in a thread
                data = await asyncio.to_thread(scraper.scrape)
            
            # Save data
            scraper.save_data(data, f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"Completed {category} scraping in {duration:.2f} seconds. Collected {len(data)} items.")
            return data
            
        except Exception as e:
            self.logger.error(f"Error running {category} scraper: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def run_all_async(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run all scrapers concurrently."""
        self.logger.info("Starting comprehensive scraping for all categories")
        results = {}
        
        tasks = []
        categories = list(self.scrapers.keys())
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=self.console
        ) as progress:
            task_id = progress.add_task("[cyan]Scraping all categories...", total=len(categories))

            # Create tasks
            for category in categories:
                tasks.append(self.run_category_async(category))

            # Run tasks concurrently
            all_data = await asyncio.gather(*tasks, return_exceptions=True)

            for category, data in zip(categories, all_data):
                if isinstance(data, Exception):
                    self.logger.error(f"Scraper {category} failed with: {data}")
                    results[category] = []
                else:
                    results[category] = data
                progress.advance(task_id)

        total_items = sum(len(data) for data in results.values())

        # Display summary table
        table = Table(title="Scraping Results")
        table.add_column("Category", style="cyan")
        table.add_column("Items", style="magenta")
        table.add_column("Status", style="green")

        for category, data in results.items():
            status = "Success" if data else "No Data/Error"
            table.add_row(category, str(len(data)), status)

        self.console.print(table)
        self.logger.info(f"Comprehensive scraping completed. Total items collected: {total_items}")
        
        return results
    
    def show_available_tools(self):
        """Display all available tools for each category."""
        self.console.print("\n[bold cyan]🔧 AVAILABLE TOOLS BY CATEGORY[/bold cyan]\n" + "="*50)
        
        for category, scraper_class in self.scrapers.items():
            try:
                scraper = scraper_class()
                tools = scraper.get_available_tools()

                self.console.print(f"\n[bold yellow]📂 {category.upper()}[/bold yellow]")
                self.console.print("-" * 30)
                for tool, description in tools.items():
                    self.console.print(f"• [green]{tool}[/green]: {description}")
            except Exception as e:
                self.logger.error(f"Error listing tools for {category}: {e}")
        
        print("\n" + "="*50)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Botsy Information Scraping Framework')
    parser.add_argument('--category', '-c', 
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
        asyncio.run(orchestrator.run_category_async(args.category))
    elif args.all:
        asyncio.run(orchestrator.run_all_async())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()