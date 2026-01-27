"""HuggingFace scraper for models, datasets, and spaces."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class HuggingFaceScraper:
    """Scraper for HuggingFace trending content."""
    
    BASE_URL = "https://huggingface.co"
    
    def __init__(self):
        """Initialize HuggingFace scraper."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; DailyAIScraper/1.0)'
        })
    
    def scrape(self, endpoints: List[str] = None, sort_by: str = 'trending',
               time_range_hours: int = 24) -> List[Dict]:
        """
        Scrape HuggingFace content.
        
        Args:
            endpoints: List of endpoints to scrape ('models', 'datasets', 'spaces')
            sort_by: Sorting method ('trending', 'recent')
            time_range_hours: Time range for filtering
            
        Returns:
            List of content dictionaries
        """
        if endpoints is None:
            endpoints = ['models', 'datasets']
            
        all_items = []
        
        for endpoint in endpoints:
            try:
                items = self._scrape_endpoint(endpoint, sort_by)
                all_items.extend(items)
                logger.info(f"Scraped {len(items)} items from HuggingFace {endpoint}")
            except Exception as e:
                logger.error(f"Error scraping HuggingFace {endpoint}: {e}")
                continue
        
        logger.info(f"Total HuggingFace items scraped: {len(all_items)}")
        return all_items
    
    def _scrape_endpoint(self, endpoint: str, sort_by: str) -> List[Dict]:
        """Scrape a specific HuggingFace endpoint."""
        items = []
        url = f"{self.BASE_URL}/{endpoint}"
        
        params = {}
        if sort_by == 'trending':
            params['sort'] = 'trending'
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article cards (HuggingFace uses article tags for items)
            articles = soup.find_all('article', limit=30)
            
            for article in articles:
                try:
                    item_data = self._parse_article(article, endpoint)
                    if item_data:
                        items.append(item_data)
                except Exception as e:
                    logger.debug(f"Error parsing article: {e}")
                    continue
                    
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
        
        return items
    
    def _parse_article(self, article, endpoint: str) -> Dict:
        """Parse an article element to extract item data."""
        # Try to find the title/name link
        title_link = article.find('a')
        if not title_link:
            return None
            
        title = title_link.get_text(strip=True)
        href = title_link.get('href', '')
        url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
        
        # Extract description if available
        desc_elem = article.find('p')
        description = desc_elem.get_text(strip=True) if desc_elem else ''
        
        # Extract metadata (likes, downloads, etc.)
        metadata = {}
        meta_elements = article.find_all('div', class_='text-sm')
        for elem in meta_elements:
            text = elem.get_text(strip=True)
            if '↓' in text or 'download' in text.lower():
                metadata['downloads'] = text
            elif '♥' in text or 'like' in text.lower():
                metadata['likes'] = text
        
        return {
            'source': 'huggingface',
            'type': endpoint,
            'title': title,
            'url': url,
            'description': description[:300],
            'metadata': metadata,
            'created_utc': datetime.utcnow().isoformat()
        }
