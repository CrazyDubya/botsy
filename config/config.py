"""
Configuration settings for Botsy information scraping framework.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (use environment variables for security)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')

# Scraping Settings
DEFAULT_DELAY = 1  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30  # seconds

# Output Settings
OUTPUT_DIR = 'data'
LOG_LEVEL = 'INFO'

# Category-specific settings
CATEGORIES = {
    'news': {
        'sources': ['reuters', 'bbc-news', 'the-verge'],
        'max_articles': 50
    },
    'research': {
        'max_papers': 20,
        'subjects': ['cs.AI', 'cs.LG', 'cs.CL']
    },
    'finance': {
        'symbols': ['AAPL', 'GOOGL', 'TSLA', 'MSFT'],
        'indicators': ['SMA', 'EMA', 'RSI']
    },
    'technology': {
        'languages': ['Python', 'JavaScript', 'Go', 'Rust'],
        'trending_repos': 10
    },
    'social': {
        'platforms': ['reddit'],
        'subreddits': ['technology', 'programming', 'MachineLearning']
    },
    'government': {
        'agencies': ['SEC', 'FDA', 'EPA'],
        'data_types': ['press_releases', 'regulations']
    },
    'weather': {
        'cities': ['New York', 'London', 'Tokyo', 'Sydney'],
        'forecast_days': 5
    },
    'sports': {
        'leagues': ['NBA', 'NFL', 'MLB'],
        'team_count': 5
    },
    'ecommerce': {
        'categories': ['electronics', 'books', 'clothing'],
        'review_count': 100
    },
    'health': {
        'topics': ['covid-19', 'vaccine', 'mental health'],
        'source_types': ['pubmed', 'who']
    }
}