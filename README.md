# 🤖 Daily AI News Scraper

An automated daily digest that collects AI/ML news from multiple sources, analyzes it with a local LLM, and delivers the most interesting findings via email.

## ✨ Features

- **Multi-Source Scraping**: Automatically collects content from:
  - Reddit (r/MachineLearning, r/artificial, r/LocalLLaMA, r/StableDiffusion, etc.)
  - HuggingFace (trending models, datasets, spaces)
  - GitHub (trending AI repositories)
  - Twitter/X (optional, AI researchers and orgs)

- **Smart LLM Analysis**: Uses Ollama (local LLM) to:
  - Identify novel and significant AI developments
  - Score and rank content by importance
  - Generate concise summaries
  - Categorize findings (models, papers, tools, etc.)

- **Automated Delivery**: 
  - Beautiful HTML emails with organized sections
  - Daily schedule via GitHub Actions
  - Plain text fallback for all email clients

- **Highly Configurable**:
  - YAML configuration for sources and settings
  - Environment variables for secrets
  - Customizable prompts and scoring

## 📋 Prerequisites

- Python 3.11 or higher
- [Ollama](https://ollama.ai) installed (for local LLM analysis)
- SMTP email account (Gmail, SendGrid, etc.)
- API credentials for:
  - Reddit (free at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps))
  - GitHub (optional, for higher rate limits)
  - Twitter/X (optional, requires API access)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kat3ri/daily_scraper.git
cd daily_scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Ollama

Install Ollama from [ollama.ai](https://ollama.ai), then pull a model:

```bash
# Install Ollama (Mac/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended model
ollama pull mistral:7b

# Or use a smaller model for lower resource usage
ollama pull llama3.2:3b
```

Start Ollama server:

```bash
ollama serve
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Reddit API (Create app at https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=DailyAIScraper/1.0

# GitHub Token (optional, create at https://github.com/settings/tokens)
GITHUB_TOKEN=your_token

# Email Configuration (for Gmail, use App Password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b
```

#### Gmail Setup

For Gmail, you need to create an App Password:
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if not already)
3. App Passwords → Create new app password
4. Use this password in `SMTP_PASSWORD`

### 5. Configure Sources (Optional)

Edit `config/sources.yaml` to customize which sources to scrape:

```yaml
reddit:
  enabled: true
  subreddits:
    - MachineLearning
    - artificial
    # Add more subreddits...
  
github:
  enabled: true
  topics:
    - machine-learning
    - llm
    # Add more topics...
```

### 6. Run Locally

Test the scraper:

```bash
python src/main.py
```

You should see logs of the scraping process and receive an email digest!

## 🔧 Configuration

### Main Configuration (`config/config.yaml`)

Copy the example and customize:

```bash
cp config/config.yaml.example config/config.yaml
```

Key settings:

```yaml
scraping:
  max_items_per_source: 50
  time_range: 24  # Hours to look back

llm:
  temperature: 0.3
  final_digest_size: 15  # Items in email

email:
  subject_prefix: "[AI Daily Digest]"
```

### Sources Configuration (`config/sources.yaml`)

Already included in the repo. Customize subreddits, GitHub topics, Twitter accounts, etc.

## ⚙️ GitHub Actions Setup

The scraper runs automatically via GitHub Actions. To set it up:

### 1. Add Repository Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add all the secrets from your `.env` file:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`
- `GH_TOKEN` (note: use `GH_TOKEN` instead of `GITHUB_TOKEN`)
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `EMAIL_TO`
- `OLLAMA_MODEL` (optional, defaults to mistral:7b)
- `TWITTER_BEARER_TOKEN` (optional)

### 2. Enable GitHub Actions

The workflow is already configured in `.github/workflows/daily_scrape.yml`

It will:
- Run daily at 8 AM UTC
- Install Ollama and pull the model
- Scrape all sources
- Analyze with LLM
- Send email digest
- Upload logs as artifacts

### 3. Manual Trigger

You can manually trigger a run:
1. Go to Actions tab
2. Select "Daily AI News Scraper"
3. Click "Run workflow"

## 📧 Email Format

The email digest includes:

- **Summary**: LLM-generated overview of today's highlights
- **Statistics**: Items analyzed, sources checked
- **Categorized Sections**:
  - New Models & Architectures
  - Research Papers
  - Tools & Libraries
  - Techniques & Methods
  - Applications & Use Cases
  - Community Discussions
- **Rich Metadata**: Scores, categories, source info, engagement metrics

## 🛠️ Customization

### Adding New Sources

1. Create a new scraper in `src/scrapers/`
2. Follow the pattern from existing scrapers
3. Add configuration to `config/sources.yaml`
4. Update `src/main.py` to call your scraper

### Adjusting LLM Prompts

Edit prompts in `src/llm/prompts.py`:

- `ANALYSIS_SYSTEM_PROMPT`: System context for the LLM
- `CONTENT_ANALYSIS_PROMPT`: Individual item analysis
- `DIGEST_SUMMARY_PROMPT`: Email introduction

### Changing Scoring Criteria

Modify the scoring guidelines in `CONTENT_ANALYSIS_PROMPT` in `prompts.py`

### Using a Different LLM Model

Set in your `.env`:

```bash
OLLAMA_MODEL=llama3.2:3b  # Smaller, faster
# or
OLLAMA_MODEL=mixtral:8x7b  # Larger, more capable
```

Available models: [ollama.ai/library](https://ollama.ai/library)

## 🧪 Testing

### Test Mode

For testing without waiting for full scraping:

```bash
# Reduce time range and item limits in config/config.yaml
scraping:
  max_items_per_source: 10
  time_range: 48
```

### Test Email

Run the scraper and check your inbox. The email will include:
- Number of items analyzed
- Top-ranked items
- Categories and scores

### Logs

Check `logs/scraper.log` for detailed execution information.

## 🐛 Troubleshooting

### "Failed to connect to Ollama"

- Make sure Ollama is running: `ollama serve`
- Check the model is pulled: `ollama list`
- Pull the model if needed: `ollama pull mistral:7b`

### "Reddit scraping failed"

- Verify your Reddit API credentials
- Check you created an app at reddit.com/prefs/apps
- Ensure client ID and secret are correct

### "Email sending failed"

- For Gmail, use an App Password (not your regular password)
- Check SMTP host and port are correct
- Verify firewall isn't blocking port 587

### "No items met quality threshold"

- The LLM may be scoring content low
- Lower `min_score` in the code, or
- Adjust prompt scoring guidelines
- Try a different LLM model

### GitHub Actions Fails

- Check the Actions tab for error logs
- Verify all secrets are set correctly
- The workflow installs Ollama automatically, but it may take time
- Check the uploaded log artifacts for details

## 📊 Performance Tips

### Resource Usage

- **Mistral 7B**: ~4GB RAM, good balance
- **Llama 3.2 3B**: ~2GB RAM, faster, less capable
- **Mixtral 8x7B**: ~32GB RAM, most capable

### Speed Optimization

1. Reduce items analyzed: Lower `max_items_per_source` in config
2. Use a smaller model: Switch to `llama3.2:3b`
3. Reduce `final_digest_size` if you want fewer items

### API Rate Limits

- GitHub: Use a token to increase rate limit to 5000/hour
- Reddit: Default limits are usually sufficient
- Twitter: Requires paid API access for higher limits

## 🔮 Future Enhancements

Ideas for extending the scraper:

- [ ] Web dashboard for viewing history
- [ ] Database storage for historical tracking
- [ ] Webhook delivery (Slack, Discord)
- [ ] Support for more sources (ArXiv, YouTube, Discord)
- [ ] Sentiment analysis
- [ ] Personalization based on interests
- [ ] Weekly/monthly digest options
- [ ] RSS feed generation
- [ ] Machine learning for better filtering
- [ ] Duplicate detection across sources

See `CONTRIBUTING.md` for guidelines on adding features.

## 📝 Project Structure

```
daily_scraper/
├── .github/
│   └── workflows/
│       └── daily_scrape.yml          # GitHub Actions workflow
├── src/
│   ├── scrapers/
│   │   ├── reddit_scraper.py         # Reddit API integration
│   │   ├── huggingface_scraper.py    # HuggingFace scraping
│   │   ├── github_scraper.py         # GitHub API integration
│   │   └── twitter_scraper.py        # Twitter API (optional)
│   ├── llm/
│   │   ├── analyzer.py               # LLM analysis logic
│   │   └── prompts.py                # Prompt templates
│   ├── delivery/
│   │   └── email_sender.py           # Email formatting & sending
│   └── main.py                       # Main orchestrator
├── config/
│   ├── config.yaml.example           # Configuration template
│   └── sources.yaml                  # Data source definitions
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new scrapers
- Improving LLM prompts
- Adding features
- Submitting bug fixes

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM runtime
- [PRAW](https://praw.readthedocs.io/) for Reddit API
- All the AI communities that share their knowledge

## 💬 Support

- Open an issue for bug reports
- Discussions for questions and ideas
- Star the repo if you find it useful!

---

**Built with ❤️ for the AI community**