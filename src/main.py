"""Main orchestrator for the daily AI news scraper."""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yaml
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.reddit_scraper import RedditScraper
from scrapers.huggingface_scraper import HuggingFaceScraper
from scrapers.github_scraper import GitHubScraper
from scrapers.twitter_scraper import TwitterScraper
from llm.analyzer import LLMAnalyzer
from delivery.email_sender import EmailSender


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """Set up logging configuration."""
    # Create logs directory if needed
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def load_config() -> Dict:
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    
    # Try example file if config doesn't exist
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml.example'
        logging.info(f"Using example config file: {config_path}")
    
    if not config_path.exists():
        logging.warning("No configuration file found, using defaults")
        return {}
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
        logging.info(f"Loaded configuration from {config_path}")
        return config if config else {}


def load_sources_config() -> Dict:
    """Load data sources configuration."""
    sources_path = Path(__file__).parent.parent / 'config' / 'sources.yaml'
    
    if not sources_path.exists():
        logging.error("sources.yaml not found!")
        return {}
    
    with open(sources_path) as f:
        return yaml.safe_load(f)


def scrape_all_sources(sources_config: Dict, config: Dict) -> Tuple[List[Dict], List[Tuple[str, str]]]:
    """
    Scrape all configured data sources.
    
    Args:
        sources_config: Sources configuration
        config: General configuration
        
    Returns:
        Tuple of (list of all scraped items, list of (source, error) tuples)
    """
    all_items = []
    errors = []
    
    # Get settings
    time_range = config.get('scraping', {}).get('time_range', 24)
    
    # Reddit
    if sources_config.get('reddit', {}).get('enabled', True):
        try:
            logging.info("Starting Reddit scraping...")
            reddit_scraper = RedditScraper(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT')
            )
            
            reddit_config = sources_config['reddit']
            reddit_items = reddit_scraper.scrape(
                subreddits=reddit_config.get('subreddits', []),
                sort_by=reddit_config.get('sort_by', 'hot'),
                limit=reddit_config.get('limit', 50),
                time_range_hours=time_range
            )
            all_items.extend(reddit_items)
            logging.info(f"Reddit: {len(reddit_items)} items")
        except Exception as e:
            logging.error(f"Reddit scraping failed: {e}")
            errors.append(('Reddit', str(e)))
    
    # HuggingFace
    if sources_config.get('huggingface', {}).get('enabled', True):
        try:
            logging.info("Starting HuggingFace scraping...")
            hf_scraper = HuggingFaceScraper()
            
            hf_config = sources_config['huggingface']
            hf_items = hf_scraper.scrape(
                endpoints=hf_config.get('endpoints', ['models', 'datasets']),
                sort_by=hf_config.get('sort_by', 'trending'),
                time_range_hours=time_range
            )
            all_items.extend(hf_items)
            logging.info(f"HuggingFace: {len(hf_items)} items")
        except Exception as e:
            logging.error(f"HuggingFace scraping failed: {e}")
            errors.append(('HuggingFace', str(e)))
    
    # GitHub
    if sources_config.get('github', {}).get('enabled', True):
        try:
            logging.info("Starting GitHub scraping...")
            github_scraper = GitHubScraper(
                token=os.getenv('GITHUB_TOKEN')
            )
            
            github_config = sources_config['github']
            github_items = github_scraper.scrape(
                topics=github_config.get('topics', []),
                language=github_config.get('language', 'python'),
                since=github_config.get('since', 'daily'),
                time_range_hours=time_range
            )
            all_items.extend(github_items)
            logging.info(f"GitHub: {len(github_items)} items")
        except Exception as e:
            logging.error(f"GitHub scraping failed: {e}")
            errors.append(('GitHub', str(e)))
    
    # Twitter (optional)
    if sources_config.get('twitter', {}).get('enabled', False):
        try:
            logging.info("Starting Twitter scraping...")
            twitter_scraper = TwitterScraper(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN')
            )
            
            twitter_config = sources_config['twitter']
            twitter_items = twitter_scraper.scrape(
                accounts=twitter_config.get('accounts', []),
                max_tweets=twitter_config.get('max_tweets', 20),
                time_range_hours=time_range
            )
            all_items.extend(twitter_items)
            logging.info(f"Twitter: {len(twitter_items)} items")
        except Exception as e:
            logging.error(f"Twitter scraping failed: {e}")
            errors.append(('Twitter', str(e)))
    
    logging.info(f"Total items scraped: {len(all_items)}")
    
    if errors:
        logging.warning(f"Scraping completed with {len(errors)} errors:")
        for source, error in errors:
            logging.warning(f"  - {source}: {error}")
    
    return all_items, errors


def analyze_with_llm(items: List[Dict], config: Dict) -> List[Dict]:
    """
    Analyze items with LLM.
    
    Args:
        items: Items to analyze
        config: Configuration
        
    Returns:
        Analyzed items
    """
    llm_config = config.get('llm', {})
    
    analyzer = LLMAnalyzer(
        host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        model=os.getenv('OLLAMA_MODEL', 'mistral:7b')
    )
    
    # Limit items to analyze based on configuration
    max_items_to_analyze = llm_config.get('top_items_to_analyze', 100)
    
    # Sort items by engagement metrics before limiting
    # Higher scores/engagement should be analyzed first
    sorted_items = sorted(
        items,
        key=lambda x: x.get('score', 0) + x.get('num_comments', 0) + x.get('stars', 0),
        reverse=True
    )
    
    items_to_analyze = sorted_items[:max_items_to_analyze]
    
    if len(items) > max_items_to_analyze:
        logging.info(f"Limiting analysis to top {max_items_to_analyze} items (out of {len(items)} total)")
    
    # Analyze items
    analyzed = analyzer.analyze_items(
        items_to_analyze,
        temperature=llm_config.get('temperature', 0.3),
        max_tokens=llm_config.get('max_tokens', 500)
    )
    
    return analyzed


def send_email_digest(items: List[Dict], stats: Dict, config: Dict, errors: List):
    """
    Send email digest.
    
    Args:
        items: Top items to include
        stats: Statistics
        config: Configuration
        errors: Any errors that occurred
    """
    # Initialize analyzer for summary generation
    analyzer = LLMAnalyzer(
        host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        model=os.getenv('OLLAMA_MODEL', 'mistral:7b')
    )
    
    # Generate summary
    summary = analyzer.generate_digest_summary(items)
    
    # Add error summary if needed
    if errors:
        error_summary = f"\n\nNote: {len(errors)} source(s) had errors during scraping: " + \
                       ", ".join([e[0] for e in errors])
        summary += error_summary
    
    # Initialize email sender
    sender = EmailSender(
        smtp_host=os.getenv('SMTP_HOST'),
        smtp_port=int(os.getenv('SMTP_PORT', 587)),
        smtp_user=os.getenv('SMTP_USER'),
        smtp_password=os.getenv('SMTP_PASSWORD'),
        from_email=os.getenv('EMAIL_FROM')
    )
    
    # Send email
    email_config = config.get('email', {})
    success = sender.send_digest(
        to_email=os.getenv('EMAIL_TO'),
        items=items,
        digest_summary=summary,
        stats=stats,
        subject_prefix=email_config.get('subject_prefix', '[AI Daily Digest]')
    )
    
    return success


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    sources_config = load_sources_config()
    
    # Set up logging
    log_config = config.get('logging', {})
    setup_logging(
        log_level=os.getenv('LOG_LEVEL', log_config.get('level', 'INFO')),
        log_file=log_config.get('file', 'logs/scraper.log')
    )
    
    logger = logging.getLogger(__name__)
    logger.info("="*70)
    logger.info("Starting Daily AI News Scraper")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("="*70)
    
    try:
        # Step 1: Scrape all sources
        logger.info("Step 1: Scraping data sources...")
        all_items, scraping_errors = scrape_all_sources(sources_config, config)
        
        if not all_items:
            logger.error("No items scraped! Cannot proceed.")
            return 1
        
        # Step 2: Analyze with LLM
        logger.info("Step 2: Analyzing with LLM...")
        analyzed_items = analyze_with_llm(all_items, config)
        
        # Step 3: Rank and filter
        logger.info("Step 3: Ranking and filtering...")
        llm_config = config.get('llm', {})
        analyzer = LLMAnalyzer(
            host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
            model=os.getenv('OLLAMA_MODEL', 'mistral:7b')
        )
        
        top_items = analyzer.rank_and_filter(
            analyzed_items,
            top_n=llm_config.get('final_digest_size', 15),
            min_score=5
        )
        
        if not top_items:
            logger.warning("No items met the quality threshold. Lowering threshold...")
            top_items = analyzer.rank_and_filter(
                analyzed_items,
                top_n=llm_config.get('final_digest_size', 15),
                min_score=3
            )
        
        # Calculate stats
        stats = {
            'total_items': len(all_items),
            'sources': len([s for s in sources_config.values() if s.get('enabled', True)]),
            'analyzed': len(analyzed_items),
            'selected': len(top_items)
        }
        
        logger.info(f"Statistics: {stats}")
        
        # Step 4: Send email
        logger.info("Step 4: Sending email digest...")
        email_success = send_email_digest(top_items, stats, config, scraping_errors)
        
        if email_success:
            logger.info("="*70)
            logger.info("Daily AI News Scraper completed successfully!")
            logger.info("="*70)
            return 0
        else:
            logger.error("Email sending failed!")
            return 1
            
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
