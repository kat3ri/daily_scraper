"""Reddit scraper for AI-related subreddits."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import praw
from praw.exceptions import PRAWException

logger = logging.getLogger(__name__)


class RedditScraper:
    """Scraper for Reddit AI communities."""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize Reddit scraper.
        
        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
    def scrape(self, subreddits: List[str], sort_by: str = 'hot', 
               limit: int = 50, time_range_hours: int = 24) -> List[Dict]:
        """
        Scrape posts from specified subreddits.
        
        Args:
            subreddits: List of subreddit names
            sort_by: Sorting method ('hot', 'new', 'top')
            limit: Maximum posts per subreddit
            time_range_hours: Filter posts within this time range
            
        Returns:
            List of post dictionaries
        """
        posts = []
        cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        for subreddit_name in subreddits:
            try:
                logger.info(f"Scraping r/{subreddit_name}")
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get posts based on sort method
                if sort_by == 'hot':
                    submissions = subreddit.hot(limit=limit)
                elif sort_by == 'new':
                    submissions = subreddit.new(limit=limit)
                elif sort_by == 'top':
                    submissions = subreddit.top(time_filter='day', limit=limit)
                else:
                    submissions = subreddit.hot(limit=limit)
                
                for submission in submissions:
                    post_time = datetime.utcfromtimestamp(submission.created_utc)
                    
                    # Filter by time range
                    if post_time < cutoff_time:
                        continue
                    
                    post_data = {
                        'source': 'reddit',
                        'subreddit': subreddit_name,
                        'title': submission.title,
                        'url': submission.url,
                        'permalink': f"https://reddit.com{submission.permalink}",
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': post_time.isoformat(),
                        'author': str(submission.author) if submission.author else '[deleted]',
                        'selftext': submission.selftext[:500] if submission.selftext else '',
                        'is_self': submission.is_self
                    }
                    posts.append(post_data)
                    
                logger.info(f"Scraped {len([p for p in posts if p['subreddit'] == subreddit_name])} posts from r/{subreddit_name}")
                
            except PRAWException as e:
                logger.error(f"Error scraping r/{subreddit_name}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error scraping r/{subreddit_name}: {e}")
                continue
        
        logger.info(f"Total Reddit posts scraped: {len(posts)}")
        return posts
