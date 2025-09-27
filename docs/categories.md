# Information Scraping Categories

## Overview

Botsy organizes information scraping into ten strategic categories, each optimized with the best available free tools and APIs.

## Categories

### 1. News & Media
- **Purpose**: Real-time news aggregation and analysis
- **Primary Tools**: RSS Feeds, NewsAPI, Feedparser
- **Free Tier Limits**: NewsAPI - 1000 requests/month
- **Data Sources**: Reuters, BBC, TechCrunch, Custom RSS feeds

### 2. Finance & Markets
- **Purpose**: Financial data and market information
- **Primary Tools**: yfinance, Alpha Vantage, Yahoo Finance RSS
- **Free Tier Limits**: Alpha Vantage - 500 calls/day
- **Data Sources**: Stock prices, market news, financial indicators

### 3. Technology & Software
- **Purpose**: Tech news, repositories, and developments
- **Primary Tools**: GitHub API, Hacker News API, Tech RSS feeds
- **Free Tier Limits**: GitHub API - 5000/hour with auth
- **Data Sources**: Trending repos, tech news, developer discussions

### 4. Research & Academia
- **Purpose**: Scientific papers and academic content
- **Primary Tools**: arXiv API, PubMed API, bioRxiv API
- **Free Tier Limits**: arXiv - Unlimited, PubMed - Rate limited
- **Data Sources**: Research papers, academic publications, preprints

### 5. Social Media
- **Purpose**: Social platform monitoring and analysis
- **Primary Tools**: Reddit JSON API, Twitter API v2
- **Free Tier Limits**: Reddit - Rate limited, Twitter - 500K tweets/month
- **Data Sources**: Social posts, trends, community discussions

### 6. Weather & Environment
- **Purpose**: Environmental data and weather patterns
- **Primary Tools**: OpenWeatherMap, NOAA API, WeatherAPI
- **Free Tier Limits**: OpenWeather - 1000 calls/day
- **Data Sources**: Weather data, environmental monitoring, forecasts

### 7. Government & Legal
- **Purpose**: Public records and regulatory information
- **Primary Tools**: Data.gov, SEC EDGAR, Federal Register API
- **Free Tier Limits**: Most government APIs are unlimited
- **Data Sources**: Public datasets, regulatory filings, legal documents

### 8. Sports & Entertainment
- **Purpose**: Sports statistics and entertainment news
- **Primary Tools**: ESPN RSS, Sports APIs, Entertainment feeds
- **Free Tier Limits**: Varies by API
- **Data Sources**: Sports scores, player stats, entertainment news

### 9. E-commerce & Reviews
- **Purpose**: Product information and customer reviews
- **Primary Tools**: eBay API, Product APIs, Web scraping
- **Free Tier Limits**: eBay - 5000 calls/day
- **Data Sources**: Product data, pricing, customer reviews

### 10. Health & Medical
- **Purpose**: Health news and medical research
- **Primary Tools**: CDC API, NIH API, WHO API, PubMed
- **Free Tier Limits**: Most medical APIs are free
- **Data Sources**: Health statistics, medical research, public health data

## Usage Examples

```bash
# Scrape news data
python main.py --category news

# Scrape all financial data
python main.py --category finance

# Show all available tools
python main.py --tools
```

## API Key Setup

Copy `.env.example` to `.env` and add your API keys:

```bash
NEWS_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
```