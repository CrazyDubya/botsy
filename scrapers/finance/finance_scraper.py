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
    
    def scrape_iex_cloud(self, symbol: str) -> Dict:
        """Scrape using IEX Cloud API (500K requests/month free)."""
        # Placeholder for IEX Cloud implementation
        try:
            self.logger.info(f"Scraping IEX Cloud for: {symbol}")
            return {
                'symbol': symbol,
                'source': 'IEX Cloud',
                'note': 'Requires IEX Cloud API key - 500K requests/month free',
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error scraping IEX Cloud: {e}")
            return {}
    
    def scrape_polygon_io(self, symbol: str) -> Dict:
        """Scrape using Polygon.io API (5 requests/minute free)."""
        # Placeholder for Polygon.io implementation
        try:
            self.logger.info(f"Scraping Polygon.io for: {symbol}")
            return {
                'symbol': symbol,
                'source': 'Polygon.io',
                'note': 'Requires Polygon.io API key - 5 requests/minute free',
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error scraping Polygon.io: {e}")
            return {}

    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for finance scraping."""
        return {
            # Free APIs - No key required
            'yfinance': 'Unlimited Yahoo Finance data via Python wrapper',
            'Yahoo Finance RSS': 'Free financial news RSS feeds',
            'FRED API': 'Federal Reserve economic data - unlimited with key',
            'World Bank API': 'Global economic indicators - completely free',
            
            # Free APIs - Key required with generous limits
            'Alpha Vantage': 'Free tier: 500 calls/day, stock/forex/crypto data',
            'IEX Cloud': 'Free tier: 500K requests/month for market data',
            'Polygon.io': 'Free tier: 5 requests/minute for real-time data',
            'Finnhub': 'Free tier: 60 requests/minute for stock data',
            'Twelve Data': 'Free tier: 800 requests/day for market data',
            'Quandl': 'Free tier: 50 requests/day for financial datasets',
            
            # Specialized Python libraries
            'pandas-datareader': 'Multiple financial data sources wrapper',
            'ccxt': 'Cryptocurrency exchange APIs (github: ccxt/ccxt)',
            'zipline': 'Algorithmic trading library (github: quantopian/zipline)',
            'backtrader': 'Trading strategy backtesting (github: mementum/backtrader)',
            'fredapi': 'FRED data access library (github: mortada/fredapi)',
            'investpy': 'Historical market data (github: alvarobartt/investpy)',
            'financetoolkit': 'Financial analysis toolkit (github: JerBouma/FinanceToolkit)',
            
            # Premium/Enterprise options
            'Alpha Vantage Premium': 'Paid tiers: $50-600/month for higher limits',
            'IEX Cloud Pro': 'Paid tiers: $9-99/month for enhanced data',
            'Polygon.io Premium': 'Paid tiers: $99-399/month for real-time data',
            'Bloomberg API': 'Enterprise: $2000+/month for professional data',
            'Refinitiv (Reuters)': 'Enterprise: $1500+/month for real-time market data',
            'Quandl Premium': 'Paid tiers: $50-500/month for premium datasets',
            
            # Alternative free sources
            'SEC EDGAR': 'Free access to SEC filings and financial reports',
            'Yahoo Finance Scraping': 'Web scraping fallback for Yahoo Finance',
            'Google Finance': 'Limited data via web scraping',
            'Morningstar': 'Some free data available via web scraping',
            
            # Cryptocurrency specific
            'CoinGecko API': 'Free cryptocurrency market data',
            'CoinMarketCap API': 'Free tier for crypto data',
            'Binance API': 'Free exchange data',
            'Coinbase API': 'Free market data access'
        }

if __name__ == "__main__":
    scraper = FinanceScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} financial data points")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")