"""
Weather & Environment scraper using free weather APIs.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import OPENWEATHER_API_KEY, CATEGORIES

class WeatherScraper(BaseScraper):
    """Scraper for weather and environmental data."""
    
    def __init__(self):
        super().__init__('weather')
        self.api_key = OPENWEATHER_API_KEY
        self.cities = CATEGORIES['weather']['cities']
    
    def scrape_openweather(self, city: str) -> Dict:
        """Scrape weather data using OpenWeatherMap API."""
        if not self.api_key:
            self.logger.warning("OpenWeatherMap API key not provided")
            return {}
        
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'visibility': data.get('visibility', 0),
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping weather for {city}: {e}")
            return {}
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        weather_data = []
        
        for city in self.cities:
            data = self.scrape_openweather(city)
            if data:
                weather_data.append(data)
        
        if weather_data:
            self.save_data(weather_data, f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return weather_data
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for weather scraping."""
        return {
            'OpenWeatherMap': 'Free tier: 1000 calls/day',
            'WeatherAPI': 'Free tier: 1M calls/month',
            'NOAA API': 'Free US government weather data',
            'World Weather Online': 'Free tier: 500 requests/day',
            'AccuWeather': 'Free tier: 50 calls/day'
        }

if __name__ == "__main__":
    scraper = WeatherScraper()
    data = scraper.scrape()
    print(f"Scraped weather data for {len(data)} cities")