# System Architecture

## Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    Daily AI News Scraper                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Data Collection (src/scrapers/)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────────┐  ┌────────┐  ┌────────┐      │
│  │ Reddit   │  │ HuggingFace  │  │ GitHub │  │Twitter │      │
│  │ Scraper  │  │   Scraper    │  │Scraper │  │Scraper │      │
│  └────┬─────┘  └──────┬───────┘  └───┬────┘  └───┬────┘      │
│       │               │              │           │            │
│       └───────────────┴──────────────┴───────────┘            │
│                          │                                     │
│                  Raw Data Items                                │
│              (titles, URLs, metadata)                          │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: LLM Analysis (src/llm/)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │             Ollama (Local LLM)                        │   │
│  │         Models: Mistral 7B / Llama 3.2                │   │
│  └──────────────────────┬─────────────────────────────────┘   │
│                         │                                      │
│         ┌───────────────┴───────────────┐                     │
│         │                               │                     │
│    ┌────▼────┐                    ┌─────▼─────┐              │
│    │ Analyze │                    │ Generate  │              │
│    │ & Score │                    │ Summary   │              │
│    │ (1-10)  │                    │           │              │
│    └────┬────┘                    └─────┬─────┘              │
│         │                               │                     │
│         └───────────────┬───────────────┘                     │
│                         │                                      │
│              Scored & Ranked Items                             │
│          (with summaries & categories)                         │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Email Generation (src/delivery/)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │            Email Template Engine                         │ │
│  │                                                          │ │
│  │  ┌────────────┐              ┌──────────────┐          │ │
│  │  │    HTML    │              │  Plain Text  │          │ │
│  │  │  Template  │              │   Template   │          │ │
│  │  └─────┬──────┘              └──────┬───────┘          │ │
│  │        │                            │                  │ │
│  │        └────────────┬───────────────┘                  │ │
│  │                     │                                  │ │
│  │           ┌─────────▼─────────┐                       │ │
│  │           │  Categorized      │                       │ │
│  │           │  Email Digest     │                       │ │
│  │           └─────────┬─────────┘                       │ │
│  └─────────────────────┼─────────────────────────────────┘ │
│                        │                                   │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Delivery (SMTP)                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │             SMTP Server                                │   │
│  │        (Gmail, SendGrid, etc.)                         │   │
│  └──────────────────────┬─────────────────────────────────┘   │
│                         │                                      │
│                         ▼                                      │
│                  📧 Daily Digest                               │
│                   Delivered!                                   │
└─────────────────────────────────────────────────────────────────┘


## Automation (GitHub Actions)

┌─────────────────────────────────────────────────────────────────┐
│  GitHub Actions Workflow (.github/workflows/daily_scrape.yml)  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Trigger: Daily at 8 AM UTC (or manual)                        │
│                                                                 │
│  1. ☑️  Checkout code                                           │
│  2. ☑️  Install Python & dependencies                           │
│  3. ☑️  Install & start Ollama                                  │
│  4. ☑️  Pull LLM model                                          │
│  5. ☑️  Run scraper (src/main.py)                               │
│  6. ☑️  Upload logs as artifacts                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


## Data Flow

Raw Content → LLM Analysis → Ranked Items → HTML Email → Inbox
   ↓              ↓              ↓             ↓
Scrapers      Ollama        Filtering    SMTP Server
   ↓              ↓              ↓             ↓
Multiple      Scoring      Top 10-15    Daily Digest
Sources      (1-10)        Items


## Configuration

┌─────────────────────────────────────────────────────────────────┐
│  Configuration Files                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  .env                      → API keys, credentials             │
│  config/config.yaml        → App settings, thresholds          │
│  config/sources.yaml       → Data sources to scrape            │
│  src/llm/prompts.py        → LLM prompt templates              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


## Error Handling

┌─────────────────────────────────────────────────────────────────┐
│  Graceful Degradation                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Source fails?      → Continue with other sources            │
│  • Ollama offline?    → Clear error message                    │
│  • Email fails?       → Logged for troubleshooting             │
│  • Partial data?      → Send what's available                  │
│                                                                 │
│  All errors logged to: logs/scraper.log                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


## Extensibility

Easy to add new components:

1. New Scraper:
   - Create class in src/scrapers/
   - Add to config/sources.yaml
   - Import in src/main.py

2. New LLM Model:
   - Change OLLAMA_MODEL in .env
   - Pull with: ollama pull <model>

3. New Delivery Method:
   - Create class in src/delivery/
   - Add configuration
   - Call from src/main.py

4. New Data Fields:
   - Update scraper output
   - Modify email template
   - Adjust LLM prompts
