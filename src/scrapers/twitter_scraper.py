"""Twitter/X scraper for AI researcher tweets (optional)."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Try to import tweepy, but make it optional
try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    logger.warning("tweepy not installed. Twitter scraping will be disabled.")


class TwitterScraper:
    """Scraper for Twitter/X posts from AI researchers."""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize Twitter scraper.
        
        Args:
            bearer_token: Twitter API Bearer token
        """
        if not TWEEPY_AVAILABLE:
            logger.warning("Twitter scraper disabled: tweepy not installed")
            self.client = None
            return
            
        if not bearer_token:
            logger.warning("Twitter scraper disabled: no bearer token provided")
            self.client = None
            return
        
        try:
            self.client = tweepy.Client(bearer_token=bearer_token)
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            self.client = None
    
    def scrape(self, accounts: List[str], max_tweets: int = 20,
               time_range_hours: int = 24) -> List[Dict]:
        """
        Scrape tweets from specified accounts.
        
        Args:
            accounts: List of Twitter usernames
            max_tweets: Maximum tweets per account
            time_range_hours: Hours to look back
            
        Returns:
            List of tweet dictionaries
        """
        if not self.client:
            logger.info("Twitter scraping skipped (not configured)")
            return []
        
        tweets = []
        start_time = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        for username in accounts:
            try:
                user_tweets = self._get_user_tweets(username, max_tweets, start_time)
                tweets.extend(user_tweets)
                logger.info(f"Scraped {len(user_tweets)} tweets from @{username}")
            except Exception as e:
                logger.error(f"Error scraping tweets from @{username}: {e}")
                continue
        
        logger.info(f"Total tweets scraped: {len(tweets)}")
        return tweets
    
    def _get_user_tweets(self, username: str, max_results: int,
                        start_time: datetime) -> List[Dict]:
        """Get tweets from a specific user."""
        tweets = []
        
        try:
            # Get user ID
            user = self.client.get_user(username=username)
            if not user.data:
                logger.warning(f"User not found: @{username}")
                return []
            
            user_id = user.data.id
            
            # Get tweets
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'entities'],
                start_time=start_time.isoformat() + 'Z'
            )
            
            if not response.data:
                return []
            
            for tweet in response.data:
                tweet_data = {
                    'source': 'twitter',
                    'username': username,
                    'title': tweet.text[:100] + ('...' if len(tweet.text) > 100 else ''),
                    'text': tweet.text,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'created_utc': tweet.created_at.isoformat(),
                    'likes': tweet.public_metrics.get('like_count', 0),
                    'retweets': tweet.public_metrics.get('retweet_count', 0),
                    'replies': tweet.public_metrics.get('reply_count', 0)
                }
                tweets.append(tweet_data)
                
        except tweepy.TweepyException as e:
            logger.error(f"Tweepy error for @{username}: {e}")
        
        return tweets
