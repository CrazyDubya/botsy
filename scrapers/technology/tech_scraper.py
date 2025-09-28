"""
Technology & Software scraper using GitHub API and tech news sources.
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import GITHUB_TOKEN, CATEGORIES

class TechnologyScraper(BaseScraper):
    """Scraper for technology and software development content."""
    
    def __init__(self):
        super().__init__('technology')
        self.github_token = GITHUB_TOKEN
        self.languages = CATEGORIES['technology']['languages']
    
    def scrape_github_trending(self) -> List[Dict]:
        """Scrape trending repositories from GitHub."""
        try:
            self.logger.info("Scraping GitHub trending repositories")
            
            # GitHub trending repositories (using search API)
            url = "https://api.github.com/search/repositories"
            params = {
                'q': 'created:>2023-01-01',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            repositories = []
            
            for repo in data.get('items', []):
                repository = {
                    'name': repo.get('name', ''),
                    'full_name': repo.get('full_name', ''),
                    'description': repo.get('description', ''),
                    'language': repo.get('language', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'url': repo.get('html_url', ''),
                    'created_at': repo.get('created_at', ''),
                    'updated_at': repo.get('updated_at', ''),
                    'scraped_at': datetime.now().isoformat()
                }
                repositories.append(repository)
            
            self.logger.info(f"Scraped {len(repositories)} trending repositories")
            return repositories
            
        except Exception as e:
            self.logger.error(f"Error scraping GitHub trending: {e}")
            return []
    
    def scrape_hacker_news(self) -> List[Dict]:
        """Scrape top stories from Hacker News API."""
        try:
            self.logger.info("Scraping Hacker News top stories")
            
            # Get top story IDs
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            response.raise_for_status()
            story_ids = response.json()[:20]  # Top 20 stories
            
            stories = []
            for story_id in story_ids:
                try:
                    story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                    story_response.raise_for_status()
                    story_data = story_response.json()
                    
                    if story_data and story_data.get('type') == 'story':
                        story = {
                            'id': story_data.get('id'),
                            'title': story_data.get('title', ''),
                            'url': story_data.get('url', ''),
                            'score': story_data.get('score', 0),
                            'by': story_data.get('by', ''),
                            'time': story_data.get('time', 0),
                            'descendants': story_data.get('descendants', 0),
                            'scraped_at': datetime.now().isoformat()
                        }
                        stories.append(story)
                except Exception as e:
                    self.logger.warning(f"Error fetching story {story_id}: {e}")
                    continue
            
            self.logger.info(f"Scraped {len(stories)} Hacker News stories")
            return stories
            
        except Exception as e:
            self.logger.error(f"Error scraping Hacker News: {e}")
            return []
    
    def scrape_tech_rss(self) -> List[Dict]:
        """Scrape technology news from RSS feeds."""
        import feedparser
        
        rss_feeds = {
            'techcrunch': 'https://techcrunch.com/feed/',
            'the_verge': 'https://www.theverge.com/rss/index.xml',
            'ars_technica': 'https://feeds.arstechnica.com/arstechnica/index',
            'wired': 'https://www.wired.com/feed/rss'
        }
        
        all_articles = []
        
        for source, feed_url in rss_feeds.items():
            try:
                self.logger.info(f"Scraping RSS feed: {source}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Limit to 5 per source
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'description': entry.get('description', ''),
                        'published': entry.get('published', ''),
                        'source': source,
                        'scraped_at': datetime.now().isoformat()
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                self.logger.error(f"Error scraping {source}: {e}")
        
        return all_articles
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        all_data = []
        
        # GitHub trending repositories
        github_data = self.scrape_github_trending()
        all_data.extend(github_data)
        
        # Hacker News stories
        hn_data = self.scrape_hacker_news()
        all_data.extend(hn_data)
        
        # Tech news RSS feeds
        rss_data = self.scrape_tech_rss()
        all_data.extend(rss_data)
        
        # Stack Overflow questions
        so_data = self.scrape_stackoverflow("python")
        all_data.extend(so_data)
        
        # Product Hunt (placeholder)
        ph_data = self.scrape_product_hunt()
        all_data.extend(ph_data)
        
        # Save data
        if all_data:
            self.save_data(all_data, f"tech_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_data
    
    def scrape_stackoverflow(self, tag: str = "python") -> List[Dict]:
        """Scrape Stack Overflow questions using their API."""
        try:
            self.logger.info(f"Scraping Stack Overflow for tag: {tag}")
            # Stack Overflow API endpoint
            url = "https://api.stackexchange.com/2.3/questions"
            params = {
                'order': 'desc',
                'sort': 'activity',
                'tagged': tag,
                'site': 'stackoverflow',
                'pagesize': 10
            }
            
            response = self.make_request(url, params)
            data = response.json()
            
            questions = []
            for item in data.get('items', []):
                question = {
                    'title': item.get('title', ''),
                    'question_id': item.get('question_id', ''),
                    'score': item.get('score', 0),
                    'view_count': item.get('view_count', 0),
                    'answer_count': item.get('answer_count', 0),
                    'tags': item.get('tags', []),
                    'creation_date': item.get('creation_date', 0),
                    'link': item.get('link', ''),
                    'source': 'Stack Overflow',
                    'scraped_at': datetime.now().isoformat()
                }
                questions.append(question)
            
            self.logger.info(f"Scraped {len(questions)} Stack Overflow questions")
            return questions
            
        except Exception as e:
            self.logger.error(f"Error scraping Stack Overflow: {e}")
            return []
    
    def scrape_product_hunt(self) -> List[Dict]:
        """Scrape Product Hunt for tech product launches."""
        try:
            self.logger.info("Scraping Product Hunt (placeholder)")
            # Placeholder for Product Hunt API implementation
            return [{
                'name': 'Sample Tech Product',
                'description': 'Innovative technology solution',
                'votes': 150,
                'source': 'Product Hunt',
                'scraped_at': datetime.now().isoformat(),
                'note': 'Requires Product Hunt API token'
            }]
        except Exception as e:
            self.logger.error(f"Error scraping Product Hunt: {e}")
            return []

    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for technology scraping."""
        return {
            # Free APIs - No authentication
            'Hacker News API': 'Completely free Firebase API for all HN data',
            'GitHub Public API': 'Free tier: 60 requests/hour without auth',
            'NPM API': 'Unlimited access to Node.js package data',
            'PyPI API': 'Unlimited access to Python package information',
            'Stack Overflow API': 'Free tier: 10K requests/day with key',
            
            # Free APIs - Authentication required
            'GitHub API (authenticated)': 'Free tier: 5000 requests/hour with token',
            'GitLab API': 'Free tier: 2000 requests/minute with token',
            'Product Hunt API': 'Free tier: 1000 requests/hour with token',
            'Dev.to API': 'Free tier: 1000 requests/hour with token',
            'Bitbucket API': 'Free tier: 1000 requests/hour with token',
            
            # RSS Feeds & Free subscriptions
            'Tech RSS Feeds': 'TechCrunch, The Verge, Ars Technica, Wired feeds',
            'GitHub Trending RSS': 'Trending repositories by language',
            'Dev.to RSS': 'Developer articles and tutorials',
            'Reddit Tech RSS': 'r/programming, r/technology, r/webdev feeds',
            
            # Specialized Python libraries & scrapers
            'PyGithub': 'GitHub API wrapper (github: PyGithub/PyGithub)',
            'github-scraper': 'Repository statistics (github: x4nth055/github-scraper)',
            'stackoverflow-scraper': 'SO data extraction (github: ssut/stackoverflow-scraper)',
            'hackernews-scraper': 'HN content scraper (github: kylelix7/hackernews-scraper)',
            'tech-news-scraper': 'Tech news aggregation (github: rushter/tech-news-scraper)',
            'awesome-scraper': 'GitHub awesome lists scraper',
            'npm-scraper': 'NPM package analytics scraper',
            'pypi-scraper': 'Python package statistics scraper',
            
            # Premium/Enterprise options
            'GitHub Enterprise API': 'Paid: $21/user/month for advanced analytics',
            'GitLab Premium': 'Paid: $19/user/month for enhanced features',
            'Stack Overflow Teams': 'Paid: $6/user/month for private Q&A',
            'JetBrains Space': 'Paid: $8/user/month for team collaboration',
            
            # Web scraping targets
            'GitHub Trending': 'Trending repositories (unofficial scraping)',
            'ProductHunt Unofficial': 'Product launches via web scraping',
            'AngelList': 'Startup and job data (web scraping)',
            'Crunchbase': 'Company and funding data (limited free)',
            'TechStars Directory': 'Startup accelerator data',
            
            # Developer community platforms
            'Dev.to Articles': 'Developer articles and tutorials',
            'Hashnode API': 'Developer blogging platform',
            'Medium Tech Publications': 'Technology articles on Medium',
            'Substack Tech Newsletters': 'Technology-focused newsletters',
            
            # Code quality & analysis
            'Libraries.io': 'Open source library analytics',
            'SourceRank': 'Library popularity metrics',
            'GitHub Archive': 'Historical GitHub event data',
            'Open Source Insights': 'Google\'s open source analysis'
        }

if __name__ == "__main__":
    scraper = TechnologyScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} technology data points")
    
    # Print available tools
    print("\nAvailable Tools:")
    for tool, description in scraper.get_available_tools().items():
        print(f"- {tool}: {description}")