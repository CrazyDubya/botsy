---
title: "Tools and APIs Reference"
layout: default
---

# Tools and APIs Reference

## Free APIs with Generous Limits

### News & Media
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| NewsAPI | 1000 requests/month | Free | Yes |
| RSS Feeds | Unlimited | Free | No |
| Feedparser | Unlimited | Free | No |

### Finance & Markets
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| yfinance | Unlimited | Free | No |
| Alpha Vantage | 500 calls/day | Free | Yes |
| Yahoo Finance RSS | Unlimited | Free | No |

### Technology & Software
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| GitHub API | 5000/hour with auth | Free | Optional |
| Hacker News API | Unlimited | Free | No |
| Tech RSS Feeds | Unlimited | Free | No |

### Research & Academia
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| arXiv API | Unlimited | Free | No |
| PubMed API | Rate limited | Free | No |
| bioRxiv API | Rate limited | Free | No |

### Social Media
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| Reddit JSON API | Rate limited | Free | No |
| Twitter API v2 | 500K tweets/month | Free | Yes |
| Reddit API (auth) | 100 requests/minute | Free | Yes |

### Weather & Environment
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| OpenWeatherMap | 1000 calls/day | Free | Yes |
| WeatherAPI | 1M calls/month | Free | Yes |
| NOAA API | Unlimited | Free | No |

### Government & Legal
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| Data.gov | Unlimited | Free | No |
| SEC EDGAR | Unlimited | Free | No |
| Federal Register API | Unlimited | Free | No |

### Sports & Entertainment
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| ESPN RSS | Unlimited | Free | No |
| The Sports DB | 1000 requests/day | Free | No |
| NBA API | Rate limited | Free | No |

### E-commerce & Reviews
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| eBay API | 5000 calls/day | Free | Yes |
| Fake Store API | Unlimited | Free | No |
| Best Buy API | Rate limited | Free | Yes |

### Health & Medical
| Tool | Limit | Cost | Key Required |
|------|-------|------|--------------|
| CDC API | Unlimited | Free | No |
| NIH API | Rate limited | Free | No |
| WHO API | Rate limited | Free | No |

## Getting API Keys

### Free API Keys Setup

1. **NewsAPI**: Sign up at [newsapi.org](https://newsapi.org)
2. **Alpha Vantage**: Register at [alphavantage.co](https://www.alphavantage.co)
3. **OpenWeatherMap**: Create account at [openweathermap.org](https://openweathermap.org/api)
4. **GitHub**: Generate token in GitHub Settings > Developer settings
5. **Reddit**: Create app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)

### Environment Setup

```bash
# Copy template
cp .env.example .env

# Edit with your keys
nano .env
```

## Web Scraping Tools

### Python Libraries
- **requests**: HTTP client for API calls
- **beautifulsoup4**: HTML parsing and extraction
- **selenium**: Dynamic content and JavaScript execution
- **feedparser**: RSS and Atom feed parsing
- **pandas**: Data manipulation and analysis

### Rate Limiting Best Practices
- Implement delays between requests
- Use exponential backoff for retries
- Respect robots.txt files
- Monitor API quotas
- Cache responses when appropriate

## Tool Selection Criteria

Each tool was selected based on:
1. **Free tier availability**
2. **API reliability and uptime**
3. **Documentation quality**
4. **Rate limit generosity**
5. **Data quality and coverage**
6. **Terms of service compliance**

## Alternative Tools

If primary tools are unavailable:
- **News**: Ground News API, News Catcher API
- **Finance**: Finnhub, Twelve Data
- **Tech**: Dev.to API, Stack Overflow API
- **Research**: Semantic Scholar, CORE API
- **Social**: Mastodon API, LinkedIn API (limited)
- **Weather**: Visual Crossing, Weatherbit
- **Government**: OpenFEMA, USASpending API