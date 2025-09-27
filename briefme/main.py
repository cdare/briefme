import feedparser
import smtplib
import ssl
import json
from email.mime.text import MIMEText
from openai import OpenAI
from typing import List

from .log_config import logger

# ---------- CONFIG ----------
from .config import (
    OPENAI_API_KEY,
    EMAIL_FROM,
    EMAIL_TO,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_PASSWORD,
    RSS_FEEDS,
    EMAIL_TEMPLATE,
    TITLE,
    AGENT_PROMPT
)

class RSSItem:
    def __init__(self, title, summary, link):
        self.title = title
        self.summary = summary
        self.link = link

# ---------- FETCH FEEDS ----------
def fetch_rss_content(feeds, max_items=5) -> List[RSSItem]:
    items = []
    for url in feeds:
        feed = feedparser.parse(url)
        logger.info(f"Fetched feed from {url} with {len(feed.entries)} entries.")
        for entry in feed.entries[:max_items]:

            if "pubDate" in entry:
                #Check if published date is older than 24 hours
                from datetime import datetime, timedelta
                pub_date = datetime(*entry.published_parsed[:6])
                if pub_date < datetime.now() - timedelta(days=1):
                    continue
            item = RSSItem(
                title=entry.get("title", ""),
                summary=entry.get("summary", ""),
                link=entry.get("link", "")
            )
            items.append(item)
    return items

# ---------- SUMMARISE WITH OPENAI ----------
def summarise_text(items: List[RSSItem], max_words=2000):
    client = OpenAI(api_key=OPENAI_API_KEY)
    json_dict = [item.__dict__ for item in items]
    prompt = AGENT_PROMPT

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=prompt,
        input=json.dumps(json_dict),
    )

    content = response.output_text
    logger.debug(f"Generated summary content:\n-------\n\n{content}")
    return content

# ---------- SEND EMAIL ----------
def send_email(subject, body):
    msg = MIMEText(body, "html", "utf-8")
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

# ---------- MAIN ----------
if __name__ == "__main__":
    logger.info("Starting daily digest process...")
    rss_items: List[RSSItem] = fetch_rss_content(RSS_FEEDS)
    if not rss_items:
        summary = "No new updates today."
    else:
        summary = summarise_text(rss_items)
        html_summary = EMAIL_TEMPLATE.format(summary=summary, title=TITLE)

    send_email(TITLE, html_summary)
    print("Daily summary sent!")
