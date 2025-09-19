# briefme

**briefme** is a Python application that generates a daily news digest by fetching RSS feeds, summarizing them using OpenAI, and sending the result as an HTML email.

## Features

- Fetches and parses multiple RSS feeds
- Summarizes news items with OpenAI
- Formats summaries as a styled HTML email
- Sends the digest via SMTP email
- All configuration via environment variables

## Quick Start

1. **Clone the repository and install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Configure environment:**
    - Copy `.env.example` to `.env` and fill in required values (API keys, email credentials, etc).
    - Copy `feeds.yaml.example` to `feeds.yaml` and add the  RSS feeds you want to subscribe to

3. **Run the daily digest:**
    ```sh
    python -m briefme.main
    ```

## Configuration

All sensitive and environment-specific values are loaded from `.env` via `briefme/config.py` using `python-dotenv`.  
No secrets are hardcoded.

- **Add/modify RSS feeds:** Edit `RSS_FEEDS` in `config.py`.
- **Change email template:** Edit `EMAIL_TEMPLATE` in `config.py`.
- **Set email title:** Modify `TITLE` in `config.py` or set `TITLE` in `.env`.
- **Update OpenAI prompt:** Edit `PROMPT_TEMPLATE` in `config.py`.
- **Logging:** Set `LOG_LEVEL` in `.env` (e.g., `DEBUG`, `INFO`).

## Automation

You can run as a GitHub action, see [workflow.example.yml](workflow.example.yml) for an example. Note that the feeds yml is provided as a base64 encode secret. You can create that as follows:

```
cat feeds.yaml | base64
```

## Testing

Run `./run_tests.sh` to run pytest with coverage report

## Developer Notes

- No hardcoded secrets: use environment variables for all sensitive data.
- Summarization prompt is structured for HTML output.
- Email sending uses SMTP with SSL.

## External Dependencies

- `feedparser` for RSS parsing
- `openai` for summarization
- `python-dotenv` for environment loading
- Standard Python modules: `logging`, `smtplib`, `ssl`, `email`

## Example: Adding a New Feed

Edit `feeds.yaml` in `briefme/`:
```yaml
feeds:
    - https://nitter.net/new_account/rss
```
