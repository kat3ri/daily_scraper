#!/usr/bin/env python3
"""
Test/Demo script for Daily AI News Scraper.

This script demonstrates the core functionality without requiring
API credentials or Ollama installation. It uses sample data and
generates a sample email output.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from test_data import get_sample_data
from datetime import datetime


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def demo_scrapers():
    """Demonstrate scraper output."""
    print_header("DEMO: Data Scraping")
    
    items = get_sample_data()
    
    print(f"\n✓ Scraped {len(items)} sample items from multiple sources:")
    print(f"  - Reddit: {len([i for i in items if i['source'] == 'reddit'])} posts")
    print(f"  - GitHub: {len([i for i in items if i['source'] == 'github'])} repos")
    print(f"  - HuggingFace: {len([i for i in items if i['source'] == 'huggingface'])} items")
    
    print("\nSample items:")
    for i, item in enumerate(items[:3], 1):
        print(f"\n{i}. {item['title'][:60]}...")
        print(f"   Source: {item['source']} | URL: {item['url'][:50]}...")


def demo_llm_analysis():
    """Demonstrate LLM analysis (simulated)."""
    print_header("DEMO: LLM Analysis (Simulated)")
    
    print("\nNote: This demo simulates LLM analysis.")
    print("For real analysis, install Ollama and run src/main.py")
    
    items = get_sample_data()
    
    # Simulate LLM scoring dynamically based on item count
    import random
    random.seed(42)  # For consistent demo results
    
    print(f"\n✓ Analyzed {len(items)} items with simulated LLM scoring:")
    
    for i, item in enumerate(items, 1):
        # Generate score between 6-9 for demo
        score = random.randint(6, 9)
        item['llm_score'] = score
        item['llm_analysis'] = {
            'score': score,
            'summary': f'This {item["source"]} item discusses important AI developments.',
            'category': 'model' if 'model' in item['title'].lower() else 'tool',
            'novelty_reason': 'Significant advancement in the field'
        }
        print(f"\n{i}. [{score}/10] {item['title'][:55]}...")
    
    return items


def demo_email_generation(analyzed_items):
    """Demonstrate email generation."""
    print_header("DEMO: Email Generation")
    
    # Sort by score
    top_items = sorted(analyzed_items, key=lambda x: x.get('llm_score', 0), reverse=True)[:5]
    
    print(f"\n✓ Generated email digest with top {len(top_items)} items")
    print("\nEmail Preview:")
    print("-" * 70)
    
    # Generate simple text preview
    date_str = datetime.now().strftime('%B %d, %Y')
    print(f"\n🤖 AI Daily Digest - {date_str}\n")
    print("Today's top AI/ML developments, analyzed and ranked by AI:\n")
    
    for i, item in enumerate(top_items, 1):
        score = item.get('llm_score', 0)
        title = item['title']
        url = item['url']
        source = item['source']
        
        print(f"{i}. {title}")
        print(f"   Score: {score}/10 | Source: {source}")
        print(f"   {url}")
        print()
    
    print("-" * 70)
    print("\nNote: Actual emails include:")
    print("  • Rich HTML formatting with categories")
    print("  • Detailed summaries for each item")
    print("  • Source-specific metadata (upvotes, stars, etc.)")
    print("  • Responsive design for mobile devices")


def demo_workflow():
    """Demonstrate the complete workflow."""
    print("\n" + "=" * 70)
    print("  DAILY AI NEWS SCRAPER - DEMO MODE")
    print("=" * 70)
    print("\nThis demo shows the workflow without requiring API credentials.")
    print("For full functionality, set up credentials and run: python src/main.py")
    
    # Step 1: Scraping
    demo_scrapers()
    
    input("\nPress Enter to continue to LLM analysis...")
    
    # Step 2: LLM Analysis
    analyzed_items = demo_llm_analysis()
    
    input("\nPress Enter to continue to email generation...")
    
    # Step 3: Email Generation
    demo_email_generation(analyzed_items)
    
    print_header("DEMO COMPLETE")
    
    print("\n📚 Next Steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Set up Ollama: https://ollama.ai")
    print("  3. Configure .env file with your API credentials")
    print("  4. Run the full scraper: python src/main.py")
    print("  5. Set up GitHub Actions for daily automation")
    print("\n  See README.md for detailed instructions.")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    try:
        demo_workflow()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Exiting...")
        sys.exit(0)
