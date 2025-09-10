# Copilot Instructions for briefme

## Project Overview
- **Purpose:** Generates a daily news digest by fetching RSS feeds, summarizing them with OpenAI, and sending the result as an HTML email.
- **Main entrypoint:** `briefme/app.py` (run as a script)
- **Configuration:** All sensitive and environment-specific values are loaded from `.env` via `briefme/config.py` using `python-dotenv`.
- **Logging:** Configured in `briefme/log_config.py` to output to stdout. Log level is set via the `LOG_LEVEL` environment variable.

## Key Components
- `app.py`: Orchestrates the workflow: fetches RSS feeds, summarizes with OpenAI, formats as HTML, and (optionally) sends email.
- `config.py`: Loads environment variables and defines constants, including the HTML email template and RSS feed list.
- `log_config.py`: Sets up a logger that outputs to stdout with a standard format. Uses the log level from config.

## Developer Workflows
- **Run the daily digest:**
  ```sh
  python briefme/app.py
  ```
- **Configure environment:**
  - Copy `.env.example` to `.env` and fill in required values (API keys, email credentials, etc).
  - All config is loaded at runtime; no secrets should be hardcoded.
- **Add/modify feeds:**
  - Edit the `RSS_FEEDS` list in `config.py`.
- **Change email template:**
  - Edit `EMAIL_TEMPLATE` in `config.py` (HTML string).
- **Set email title:**
  - Modify the `TITLE` variable in `config.py` or set the `TITLE` environment variable in `.env`.
- **Update the OpenAI prompt:**
  - Modify `PROMPT_TEMPLATE` in `config.py` to change how summaries are generated.
- **Logging:**
  - All logs go to stdout. Adjust verbosity with the `LOG_LEVEL` env var (e.g., `DEBUG`, `INFO`).

## Patterns & Conventions
- **No hardcoded secrets:** All sensitive values must be loaded from environment variables.
- **Logging:** Use `from log_config import logger` for consistent logging.
- **Summarization:** The OpenAI prompt is structured for HTML output, with sections and translation as needed.
- **Email sending:** Uses SMTP with SSL. Ensure credentials are correct in `.env`.

## External Dependencies
- `feedparser` for RSS parsing
- `openai` for summarization
- `python-dotenv` for env loading
- Standard Python `logging`, `smtplib`, `ssl`, and `email` modules

## Example: Adding a New Feed
Edit `RSS_FEEDS` in `config.py`:
```python
RSS_FEEDS = [
    ...
    "https://nitter.net/new_account/rss",
]
```

## Example: Changing Log Level
Set in `.env`:
```
LOG_LEVEL=DEBUG
```


---
If you add new components, document their purpose and integration points here.
