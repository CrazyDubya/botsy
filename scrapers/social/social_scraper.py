"""
Social Media scraper using free APIs (Reddit, etc.).
"""
import requests
from typing import Dict, List, Any
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper_base import BaseScraper
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, CATEGORIES

class SocialScraper(BaseScraper):
    """Scraper for social media content."""
    
    def __init__(self):
        super().__init__('social')
        self.reddit_client_id = REDDIT_CLIENT_ID
        self.reddit_client_secret = REDDIT_CLIENT_SECRET
        self.subreddits = CATEGORIES['social']['subreddits']
    
    def scrape_reddit(self, subreddit: str) -> List[Dict]:
        """Scrape Reddit posts using the free JSON API."""
        try:
            self.logger.info(f"Scraping Reddit: r/{subreddit}")
            
            # Use Reddit's JSON API (no auth required for public posts)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {'User-Agent': 'Botsy Scraper 1.0'}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for post in data['data']['children'][:10]:  # Top 10 posts
                post_data = post['data']
                posts.append({
                    'title': post_data.get('title', ''),
                    'author': post_data.get('author', ''),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'created_utc': post_data.get('created_utc', 0),
                    'subreddit': subreddit,
                    'scraped_at': datetime.now().isoformat()
                })
            
            self.logger.info(f"Scraped {len(posts)} posts from r/{subreddit}")
            return posts
            
        except Exception as e:
            self.logger.error(f"Error scraping r/{subreddit}: {e}")
            return []
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method."""
        all_posts = []
        
        for subreddit in self.subreddits:
            posts = self.scrape_reddit(subreddit)
            all_posts.extend(posts)
        
        if all_posts:
            self.save_data(all_posts, f"social_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return all_posts
    
    def get_available_tools(self) -> Dict[str, str]:
        """Return available tools for social media scraping."""
        return {
            'Reddit JSON API': 'Free public posts without authentication',
            'Reddit API': 'Free tier: 100 requests/minute with auth',
            'Twitter API v2': 'Free tier: 500K tweets/month (Essential)',
            'YouTube API': 'Free tier: 10K requests/day',
            'Instagram Basic Display': 'Free for personal use',
            'Mastodon API': 'Free and open source',
            'LinkedIn API': 'Limited free tier',
            'Discord API': 'Free for bot development'
        }

if __name__ == "__main__":
    scraper = SocialScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} social media posts")