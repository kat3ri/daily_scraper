# Quick Setup Guide

## Prerequisites Check
- [ ] Python 3.11+ installed
- [ ] Ollama installed (from https://ollama.ai)
- [ ] Reddit API credentials (from https://www.reddit.com/prefs/apps)
- [ ] Email account for SMTP (Gmail recommended)

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Ollama
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve

# Pull model (in another terminal)
ollama pull mistral:7b
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required variables:
- `REDDIT_CLIENT_ID` - From Reddit app
- `REDDIT_CLIENT_SECRET` - From Reddit app
- `REDDIT_USER_AGENT` - Any descriptive string
- `SMTP_HOST` - e.g., smtp.gmail.com
- `SMTP_PORT` - e.g., 587
- `SMTP_USER` - Your email
- `SMTP_PASSWORD` - App password (for Gmail)
- `EMAIL_FROM` - Your email
- `EMAIL_TO` - Recipient email

### 4. Test It
```bash
# Try the demo first (no credentials needed)
python test_demo.py

# Then run the real scraper
python src/main.py
```

### 5. GitHub Actions (Optional)
Set these secrets in GitHub repo settings:
- All variables from .env file
- Use `GH_TOKEN` instead of `GITHUB_TOKEN`

## Troubleshooting Quick Fixes

### Ollama Connection Failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Reddit API Errors
- Verify credentials at https://www.reddit.com/prefs/apps
- Check client ID and secret are correct
- User agent should be descriptive, e.g., "DailyAIScraper/1.0"

### Email Not Sending
- For Gmail: Use App Password, not regular password
- Enable 2FA first, then create app password
- Check SMTP host and port

### No Items in Digest
- Lower the min_score in src/main.py (line ~280)
- Adjust time_range in config/config.yaml
- Try different subreddits/topics

## Next Steps
- Read full [README.md](README.md) for details
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to extend functionality
- Join discussions in GitHub Issues
