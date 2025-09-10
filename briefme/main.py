import feedparser
import smtplib
import ssl
from email.mime.text import MIMEText
from openai import OpenAI

from briefme.log_config import logger

# ---------- CONFIG ----------
from briefme.config import (
    OPENAI_API_KEY,
    EMAIL_FROM,
    EMAIL_TO,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_PASSWORD,
    RSS_FEEDS,
    EMAIL_TEMPLATE,
    TITLE,
    PROMPT_TEMPLATE
)

# ---------- FETCH FEEDS ----------
def fetch_rss_content(feeds, max_items=5):
    texts = []
    for url in feeds:
        feed = feedparser.parse(url)
        logger.info(f"Fetched feed from {url} with {len(feed.entries)} entries.")
        for entry in feed.entries[:max_items]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            texts.append(f"{title}\n{summary}")
    return "\n\n".join(texts)

# ---------- SUMMARISE WITH OPENAI ----------
def summarise_text(text, max_words=2000):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = PROMPT_TEMPLATE.format(max_words=max_words, text=text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )
    content = response.choices[0].message.content
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
    raw_content = fetch_rss_content(RSS_FEEDS)
    if not raw_content.strip():
        summary = "No new updates today."
    else:
        summary = summarise_text(raw_content)
        html_summary = EMAIL_TEMPLATE.format(summary=summary, title=TITLE)

    send_email(TITLE, html_summary)
    print("Daily summary sent!")
