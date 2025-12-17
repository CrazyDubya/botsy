"""
Base scraper class with common functionality.
"""
import time
import requests
import requests_cache
import aiohttp
import asyncio
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Union
from utils.logger import setup_logger
from utils.config_loader import ConfigManager
import logging
import os

class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, category: str):
        self.category = category
        self.logger = setup_logger(f"{category}_scraper")
        self.config = ConfigManager()

        # Error logger
        self.error_logger = logging.getLogger(f"{category}_error")
        handler = logging.FileHandler(f"logs/{category}_error.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(handler)
        self.error_logger.setLevel(logging.ERROR)

        # Caching
        if self.config.get_boolean('Scraping', 'use_cache', True):
            expire_after = self.config.get_int('Scraping', 'cache_expire_after', 3600)
            requests_cache.install_cache(f'cache_{category}', expire_after=expire_after)

        self.session = requests.Session()
        self.user_agent = self.config.get('Scraping', 'user_agent', 'Botsy Information Scraper 1.0')
        self.session.headers.update({
            'User-Agent': self.user_agent
        })

        # Proxy
        self.proxy = None
        if self.config.get_boolean('Scraping', 'use_proxy', False):
            self.proxy = self.config.get('Scraping', 'proxy_url')
            if self.proxy:
                self.session.proxies.update({'http': self.proxy, 'https': self.proxy})

        self.default_delay = self.config.get_int('Scraping', 'default_delay', 1)
        self.max_retries = self.config.get_int('Scraping', 'max_retries', 3)
        self.timeout = self.config.get_int('Scraping', 'timeout', 30)

    def make_request(self, url: str, params: Dict = None, retries: int = None) -> requests.Response:
        """Make HTTP request with retry logic."""
        retries = retries or self.max_retries
        for attempt in range(retries):
            try:
                self.logger.info(f"Making request to: {url}")
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.default_delay)
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                self.error_logger.error(f"Request failed: {url} - {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(self.default_delay * (attempt + 1))

    async def make_async_request(self, url: str, params: Dict = None) -> str:
        """Make async HTTP request."""
        # Increase max_field_size to handle large headers (default is 8190)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        headers = {'User-Agent': self.user_agent}

        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            try:
                self.logger.info(f"Making async request to: {url}")
                # Use proxy if configured
                async with session.get(url, params=params, proxy=self.proxy) as response:
                    response.raise_for_status()
                    return await response.text()
            except Exception as e:
                self.logger.error(f"Async request failed: {e}")
                self.error_logger.error(f"Async request failed: {url} - {e}")

                # Fallback to sync requests in thread using self.session (preserves proxy, headers, cache)
                try:
                    self.logger.info(f"Falling back to sync request for: {url}")
                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(None, lambda: self.session.get(url, params=params, timeout=self.timeout))
                    response.raise_for_status()
                    return response.text
                except Exception as e2:
                    self.logger.error(f"Fallback sync request failed: {e2}")
                    self.error_logger.error(f"Fallback sync request failed: {url} - {e2}")
                    return ""

    def save_data(self, data: List[Dict], filename: str):
        """Save scraped data to file in configured format."""
        import json
        
        output_dir = self.config.get('Output', 'output_dir', 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        output_format = self.config.get('Output', 'format', 'json').lower()
        
        # Normalize data to ensure it's a list of dicts or models
        normalized_data = []
        for item in data:
            if hasattr(item, 'model_dump'):
                normalized_data.append(item.model_dump())
            elif isinstance(item, dict):
                normalized_data.append(item)
            else:
                self.logger.warning(f"Skipping item of unknown type: {type(item)}")

        if not normalized_data:
            self.logger.warning("No data to save.")
            return

        filepath_base = f"{output_dir}/{self.category}_{filename}"

        if output_format == 'csv':
            df = pd.DataFrame(normalized_data)
            df.to_csv(f"{filepath_base}.csv", index=False)
            self.logger.info(f"Data saved to: {filepath_base}.csv")
        elif output_format == 'parquet':
            df = pd.DataFrame(normalized_data)
            df.to_parquet(f"{filepath_base}.parquet", index=False)
            self.logger.info(f"Data saved to: {filepath_base}.parquet")
        else: # Default to JSON
            with open(f"{filepath_base}.json", 'w', encoding='utf-8') as f:
                json.dump(normalized_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to: {filepath_base}.json")
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> Dict[str, str]:
        """Return dictionary of available tools and their descriptions."""
        pass
