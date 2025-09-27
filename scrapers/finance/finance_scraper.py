"""
Finance & Markets scraper using free APIs.
"""
import yfinance as yf
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import ALPHA_VANTAGE_API_KEY, CATEGORIES

class FinanceScraper(BaseScraper):
    """Scraper for financial data and market information."""
    
    def __init__(self):
        super().__init__('finance')
        self.alpha_vantage_key = ALPHA_VANTAGE_API_KEY
        self.symbols = CATEGORIES['finance']['symbols']
    
    def scrape_yahoo_finance(self, symbol: str) -> Dict:
        """Scrape stock data using yfinance (free)."""
        try:
            self.logger.info(f"Scraping Yahoo Finance data for: {symbol}")
            ticker = yf.Ticker(symbol)
            
            # Get current info
            info = ticker.info
            
            # Get historical data (last 30 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            hist = ticker.history(start=start_date, end=end_date)
            
            stock_data = {
                'symbol': symbol,
                'company_name': info.get('longName', ''),
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'historical_data': {
                    'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                    'close_prices': hist['Close'].round(2).tolist(),
                    'volumes': hist['Volume'].tolist()
                },
                'scraped_at': datetime.now().isoformat()
            }
            
            return stock_data
            
        except Exception as e:
            self.logger.error(f"Error scraping Yahoo Finance for {symbol}: {e}")
            return {}
    
    def scrape_alpha_vantage(self, symbol: str) -> Dict:
        """Scrape using Alpha Vantage API (free tier: 5 calls/minute, 500/day)."""
        if not self.alpha_vantage_key:
            self.logger.warning("Alpha Vantage API key not provided")
            return {}
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            quote = data.get('Global Quote', {})
            if not quote:
                return {}
            
            return {
                'symbol': quote.get('01. symbol', ''),
                'price': float(quote.get('05. price', 0)),
                'change': quote.get('09. change', ''),
                'change_percent': quote.get('10. change percent', ''),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day', ''),
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping Alpha Vantage for {symbol}: {e}")
            return {}
    
    def scrape_market_news(self) -> List[Dict]:
        """Scrape financial news from free sources."""
        news_articles = []
        
        # Yahoo Finance RSS feed
        try:
            import feedparser
            feed = feedparser.parse('https://feeds.finance.yahoo.com/rss/2.0/headline')
            
            for entry in feed.entries[:10]:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': 'Yahoo Finance',
                    'scraped_at': datetime.now().isoformat()
                }
                news_articles.append(article)
                
        except Exception as e:
            self.logger.error(f"Error scraping financial news: {e}")
        
        return news_articles
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        all_data = []
        
        # Scrape stock data for each symbol
        for symbol in self.symbols:
            # Yahoo Finance data (free, no API key needed)
            yahoo_data = self.scrape_yahoo_finance(symbol)
            if yahoo_data:
                all_data.append(yahoo_data)
            
            # Alpha Vantage data (if API key available)
            alpha_data = self.scrape_alpha_vantage(symbol)
            if alpha_data:
                all_data.append({**alpha_data, 'source': 'alpha_vantage'})
        
        # Scrape market news
        news_data = self.scrape_market_news()
        all_data.extend(news_data)
        
        # Save data
        if all_data:
            self.save_data(all_data, f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_data
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for finance scraping."""
        return {
            'yfinance': 'Free Python library for Yahoo Finance data',
            'Alpha Vantage': 'Free tier: 5 calls/minute, 500 calls/day',
            'Yahoo Finance RSS': 'Free financial news RSS feeds',
            'SEC EDGAR': 'Free access to SEC filings and reports',
            'Federal Reserve Economic Data (FRED)': 'Free economic data API',
            'Quandl': 'Free tier available for financial datasets',
            'IEX Cloud': 'Free tier with 500K requests/month',
            'Polygon.io': 'Free tier with delayed market data'
        }

if __name__ == "__main__":
    scraper = FinanceScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} financial data points")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")