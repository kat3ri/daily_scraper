"""GitHub scraper for trending AI repositories."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests

logger = logging.getLogger(__name__)


class GitHubScraper:
    """Scraper for GitHub trending AI repositories."""
    
    API_BASE = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub scraper.
        
        Args:
            token: GitHub personal access token (optional, for higher rate limits)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'DailyAIScraper/1.0'
        })
        
        if token:
            self.session.headers['Authorization'] = f'token {token}'
    
    def scrape(self, topics: List[str] = None, language: str = 'python',
               since: str = 'daily', time_range_hours: int = 24) -> List[Dict]:
        """
        Scrape trending GitHub repositories.
        
        Args:
            topics: List of topics to search for
            language: Programming language filter
            since: Time range for trending ('daily', 'weekly', 'monthly')
            time_range_hours: Hours to look back
            
        Returns:
            List of repository dictionaries
        """
        if topics is None:
            topics = ['machine-learning', 'artificial-intelligence', 'deep-learning']
        
        repos = []
        
        # Calculate date threshold
        date_threshold = (datetime.utcnow() - timedelta(hours=time_range_hours)).strftime('%Y-%m-%d')
        
        for topic in topics:
            try:
                topic_repos = self._search_repositories(topic, language, date_threshold)
                repos.extend(topic_repos)
                logger.info(f"Scraped {len(topic_repos)} repos for topic: {topic}")
            except Exception as e:
                logger.error(f"Error scraping GitHub topic {topic}: {e}")
                continue
        
        # Remove duplicates based on repo full_name
        unique_repos = {}
        for repo in repos:
            if repo['full_name'] not in unique_repos:
                unique_repos[repo['full_name']] = repo
        
        repos = list(unique_repos.values())
        logger.info(f"Total unique GitHub repos scraped: {len(repos)}")
        return repos
    
    def _search_repositories(self, topic: str, language: str, 
                           since_date: str, per_page: int = 30) -> List[Dict]:
        """Search repositories by topic and date."""
        repos = []
        
        # Build search query
        query_parts = [f'topic:{topic}']
        if language:
            query_parts.append(f'language:{language}')
        query_parts.append(f'created:>={since_date}')
        
        query = ' '.join(query_parts)
        
        url = f"{self.API_BASE}/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('items', []):
                repo_data = {
                    'source': 'github',
                    'full_name': item['full_name'],
                    'name': item['name'],
                    'title': item['full_name'],
                    'url': item['html_url'],
                    'description': item.get('description', ''),
                    'stars': item['stargazers_count'],
                    'forks': item['forks_count'],
                    'language': item.get('language', ''),
                    'topics': item.get('topics', []),
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'created_utc': item['created_at']
                }
                repos.append(repo_data)
                
        except requests.RequestException as e:
            logger.error(f"GitHub API request error: {e}")
        
        return repos
