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
            # Free APIs - No authentication
            'Reddit JSON API': 'Free public posts without authentication (rate limited)',
            'Mastodon API': 'Free and open source social network API',
            
            # Free APIs - Authentication required
            'Reddit API (OAuth)': 'Free tier: 100 requests/minute with authentication',
            'Twitter API v2': 'Free tier: 500K tweets/month (Essential access)',
            'YouTube API': 'Free tier: 10K requests/day for video metadata',
            'Instagram Basic Display': 'Free for personal use (limited)',
            'LinkedIn API': 'Limited free tier for basic profile data',
            'Discord API': 'Free for bot development (rate limited)',
            'Telegram Bot API': 'Free for bot interactions (rate limited)',
            'Pinterest API': 'Free tier: 1000 requests/hour',
            
            # Specialized Python libraries & scrapers
            'praw': 'Reddit API wrapper (github: praw-dev/praw)',
            'tweepy': 'Twitter API wrapper (github: tweepy/tweepy)',
            'instaloader': 'Instagram scraper (github: instaloader/instaloader)',
            'youtube-dl': 'Video downloader (github: ytdl-org/youtube-dl)',
            'yt-dlp': 'Enhanced youtube-dl fork (github: yt-dlp/yt-dlp)',
            'social-media-scraper': 'Multi-platform scraper (github: arc298/social-media-scraper)',
            'tiktok-scraper': 'TikTok content scraper',
            'linkedin-scraper': 'LinkedIn profile scraper',
            'facebook-scraper': 'Facebook public posts scraper',
            
            # Premium/Paid options
            'Twitter API Pro': 'Paid tier: $100/month for 1M tweets',
            'Brandwatch': 'Enterprise: $800+/month for social listening',
            'Hootsuite Insights': 'Paid: $49+/month for analytics',
            'Sprout Social': 'Paid: $99+/month for management and analytics',
            'Mention': 'Paid: $25+/month for social monitoring',
            'Socialbakers': 'Enterprise social media analytics',
            
            # Web scraping targets
            'TikTok Public Data': 'Public posts and trends (web scraping)',
            'Facebook Public Pages': 'Public page content (limited)',
            'Instagram Public Profiles': 'Public posts and hashtags',
            'LinkedIn Public Profiles': 'Public professional data',
            'Snapchat Discover': 'Public discover content',
            'Clubhouse': 'Audio social network (limited data)',
            
            # Alternative platforms
            'Parler': 'Conservative social platform',
            'Gab': 'Free speech social platform',
            'Truth Social': 'Trump-affiliated platform',
            'Gettr': 'Free speech platform',
            'MeWe': 'Privacy-focused social network',
            'Minds': 'Open source social network',
            
            # Analytics and monitoring
            'Social Mention': 'Free social media search engine',
            'Tweetdeck': 'Twitter management (limited free)',
            'Buffer': 'Social media scheduling (limited free)',
            'Later': 'Instagram scheduling (limited free)'
        }

if __name__ == "__main__":
    scraper = SocialScraper()
    data = scraper.scrape()
    print(f"Scraped {len(data)} social media posts")