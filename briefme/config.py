# Prompt template for OpenAI summarization
PROMPT_TEMPLATE = """
Summarise the following updates into a clear daily digest (max {max_words} words):\n\n{text}.

Split into the following sections:
- Cybersecurity News
- Vulnerability Writeups and Disclosures

The summary should be concise, informative, and easy to read. Use bullet points or short paragraphs as needed.
It will be inserted into an HTML email template. Each section should be wrapped in <div class="section"> with a heading <h2>.

Include links from the original articles.

If there are any articles in the feed that do not relate to cybersecurity, ignore them.

Translate any non-English text to English.

Do not add any notes, comments, or disclaimers at the beginning or end of the summary. Only produce the HTML content.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TITLE = os.getenv("TITLE", "Your News Digest")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# RSS feeds (blogs + Nitter for Twitter accounts)
RSS_FEEDS = [
    "https://nitter.net/ryotkak/rss",                
    "https://nitter.net/kevin_mizu/rss",   
    "https://nitter.net/terjanq",
    "https://www.bleepingcomputer.com/feed/"
]
EMAIL_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin:0; padding:0; background:#f4f6f8; font-family:Arial, Helvetica, sans-serif; color:#333; }}
    .container {{ max-width:600px; margin:20px auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1); }}
    .header {{ background:#0a3d62; color:#ffffff; padding:20px; text-align:center; }}
    .header h1 {{ margin:0; font-size:22px; font-weight:bold; }}
    .section {{ padding:20px; }}
    .section h2 {{ font-size:18px; margin-bottom:12px; border-bottom:2px solid #0a3d62; padding-bottom:6px; color:#0a3d62; }}
    .section p {{ line-height:1.5; }}
    .footer {{ background:#f0f0f0; text-align:center; font-size:12px; color:#555; padding:15px; }}
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
      © 2025 {title} • You are receiving this because you subscribed to daily updates.
    </div>
  </div>
</body>
</html>
"""