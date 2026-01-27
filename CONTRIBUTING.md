# Contributing to Daily AI News Scraper

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- **Add new scrapers** for additional data sources
- **Improve LLM prompts** for better analysis
- **Enhance email templates** with better design
- **Add features** from the roadmap
- **Fix bugs** and improve stability
- **Improve documentation** and examples
- **Share feedback** and suggestions

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

### Adding a New Scraper

1. Create a new file in `src/scrapers/`
2. Implement a class with a `scrape()` method
3. Return a list of dictionaries with these keys:
   - `source`: Source identifier (string)
   - `title`: Item title (string)
   - `url`: Link to the item (string)
   - `description`: Brief description (string)
   - `created_utc`: ISO timestamp (string)
   - Additional source-specific fields

Example template:

```python
"""Your scraper description."""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class YourScraper:
    """Scraper for YourSource."""
    
    def __init__(self, api_key: str = None):
        """Initialize scraper."""
        pass
    
    def scrape(self, **kwargs) -> List[Dict]:
        """
        Scrape content.
        
        Returns:
            List of item dictionaries
        """
        items = []
        # Your scraping logic here
        return items
```

4. Add configuration to `config/sources.yaml`:

```yaml
yoursource:
  enabled: true
  # Source-specific settings
```

5. Update `src/main.py` to call your scraper
6. Add any new dependencies to `requirements.txt`
7. Document in README.md

### Improving LLM Prompts

Prompts are in `src/llm/prompts.py`. When modifying:

1. Test with multiple examples
2. Ensure JSON output remains valid
3. Consider token usage
4. Document prompt changes in PR

### Modifying Email Templates

Email templates are in `src/delivery/email_sender.py`:

1. Test with multiple email clients
2. Ensure responsive design
3. Include plain text alternative
4. Validate HTML

## 🧪 Testing

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set up test environment
cp .env.example .env
# Edit .env with test credentials

# Run the scraper
python src/main.py
```

### Testing Checklist

- [ ] Code runs without errors
- [ ] New features work as expected
- [ ] Existing features still work
- [ ] Email renders correctly
- [ ] Logs are informative
- [ ] Error handling works
- [ ] Documentation updated

## 📋 Pull Request Process

1. **Update documentation**: README.md, docstrings, comments
2. **Test thoroughly**: Run locally and verify all features
3. **Keep changes focused**: One feature/fix per PR
4. **Write clear commit messages**: Describe what and why
5. **Reference issues**: Link related issues in PR description

### PR Title Format

- `feat: Add ArXiv scraper`
- `fix: Handle missing Reddit descriptions`
- `docs: Update installation instructions`
- `refactor: Simplify email template`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How you tested the changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Tested locally
```

## 🐛 Reporting Bugs

Use GitHub Issues with:

- **Clear title**: Describe the issue concisely
- **Steps to reproduce**: Detailed steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, dependencies
- **Logs**: Relevant error messages

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if already requested in Issues
2. Describe the feature clearly
3. Explain use case and benefits
4. Consider implementation approach

## 🔮 Roadmap Ideas

High-priority enhancements:

### New Data Sources
- ArXiv (research papers)
- YouTube (AI channels)
- Discord servers (public AI communities)
- Hacker News (AI/ML posts)
- Medium publications

### Analysis Improvements
- Duplicate detection across sources
- Topic clustering
- Sentiment analysis
- Trend detection over time

### Delivery Options
- Slack integration
- Discord webhooks
- Telegram bot
- Web dashboard
- RSS feed

### Data Management
- Database storage (SQLite/PostgreSQL)
- Historical tracking
- Search functionality
- Weekly/monthly digests

### Personalization
- Interest-based filtering
- Custom scoring weights
- User profiles
- Feedback learning

## 🏗️ Architecture Notes

### Project Structure

- `src/scrapers/`: Data collection modules
- `src/llm/`: LLM analysis logic
- `src/delivery/`: Email delivery
- `config/`: Configuration files
- `.github/workflows/`: CI/CD

### Key Design Principles

1. **Modularity**: Each scraper is independent
2. **Configurability**: Settings via YAML and env vars
3. **Error handling**: Graceful degradation
4. **Logging**: Comprehensive and informative
5. **Extensibility**: Easy to add new sources

### Dependencies

Keep dependencies minimal:
- Core: praw, requests, beautifulsoup4, ollama
- Optional: tweepy (Twitter)
- Standard library preferred when possible

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Feature Ideas**: Open a GitHub Issue with `enhancement` label

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping improve Daily AI News Scraper! 🚀
