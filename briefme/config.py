import os
from dotenv import load_dotenv
import yaml

# Load environment variables
if os.path.exists('.env'):
    load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TITLE = os.getenv("TITLE", "Your Security News Digest")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configuration validation
required_vars = ['OPENAI_API_KEY', 'EMAIL_FROM', 'EMAIL_TO', 'EMAIL_PASSWORD']
missing_vars = [var for var in required_vars if not globals()[var]]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: "
        f"{', '.join(missing_vars)}"
    )

# Configurable parameters
MAX_ITEMS_PER_FEED = int(os.getenv("MAX_ITEMS_PER_FEED", "5"))
MAX_AGE_HOURS = int(os.getenv("MAX_AGE_HOURS", "24"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "800"))


# Load RSS feeds from feeds.yaml
try:
    # Try package directory first
    feeds_file = os.path.join(os.path.dirname(__file__), 'feeds.yaml')
    if not os.path.exists(feeds_file):
        # Fallback to project root
        feeds_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'feeds.yaml'
        )

    with open(feeds_file, 'r') as f:
        feeds_config = yaml.safe_load(f)
    RSS_FEEDS = feeds_config.get('feeds', [])
except (FileNotFoundError, yaml.YAMLError) as e:
    print(f"Warning: Could not load feeds.yaml: {e}")
    RSS_FEEDS = []
EMAIL_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin:0; padding:0; background:#f4f6f8; \
font-family:Arial, Helvetica, sans-serif; color:#333; }}
    .container {{ max-width:600px; margin:20px auto; \
background:#ffffff; border-radius:8px; overflow:hidden; \
box-shadow:0 2px 6px rgba(0,0,0,0.1); }}
    .header {{ background:#0a3d62; color:#ffffff; \
padding:20px; text-align:center; }}
    .header h1 {{ margin:0; font-size:22px; font-weight:bold; }}
    .section {{ padding:5px; }}
    .section h2 {{ font-size:18px; margin-bottom:12px; \
border-bottom:2px solid #0a3d62; padding-bottom:6px; color:#0a3d62; }}
    .section p {{ line-height:1.5; }}
    .footer {{ background:#f0f0f0; text-align:center; \
font-size:12px; color:#555; padding:15px; }}
    a {{ color:#0a7dda; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Cybersecurity Daily Digest</h1>
    </div>
    {summary}
    <div class="footer">
      © 2025 {title} • You are receiving this because you \
subscribed to daily updates.
    </div>
  </div>
</body>
</html>
"""

# Prompt template for OpenAI summarization
AGENT_PROMPT = f"""
You are an assistant that creates a daily cybersecurity news digest \
from a list of JSON items. Each JSON item represents a news article.

Summarize the provided list of JSON items into a concise daily digest, \
with a maximum length of 600 words.

Instructions:

- The summary must begin with a brief overview paragraph.
- Organize the digest into the following sections, in this order:
  1. Cybersecurity News (general cybersecurity news)
  2. Vulnerability Writeups and Disclosures \
(bug bounties, vulnerabilities, exploits, and disclosures)
- The summary will be inserted into an HTML template for email \
as a <div> element
- Each section must be wrapped in <div class="section"> and \
have a <h2> heading.
- Present content as bullet points or short paragraphs for clarity \
and readability.
- Each article title must be a clickable link \
(<a href="URL">Title</a>), using the URLs from the JSON.
- Strictly adhere to the 600-word limit. If there are too many \
articles, prioritize the most important and relevant ones.
- **Give highest priority to articles about AI security, \
web security, and cloud security.**
- Only include articles:
    - Directly related to cybersecurity (ignore unrelated topics)
    - Published within the last {MAX_AGE_HOURS} hours \
(ignore older articles)
- Translate any non-English text to English.
- Do NOT add any introductory or closing notes, comments, \
or disclaimers. Only produce the HTML content for insertion into \
the template. Do NOT wrap the output in backticks or quotes.
- If an article is missing a title or URL, skip it.
- Do not alter the template, only add the summary content in the \
[SUMMARIES] placeholder.

Example output structure:

<!-- Overview paragraph here -->
<div class="section">
  <h2>Cybersecurity News</h2>
  <ul>
    <li><a href="url1">Title 1</a> – summary</li>
    ...
  </ul>
</div>
<div class="section">
  <h2>Vulnerability Writeups and Disclosures</h2>
  <ul>
    <li><a href="url2">Title 2</a> – summary</li>
    ...
  </ul>
</div>
"""
