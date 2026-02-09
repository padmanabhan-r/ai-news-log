import os
from datetime import date, datetime, timedelta
from openai import OpenAI
import feedparser

# AI news RSS feeds
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
]

def fetch_recent_articles():
    """Fetch articles from the last 24 hours"""
    articles = []
    yesterday = datetime.now() - timedelta(days=1)

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:  # Top 10 from each feed
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    pub_date = datetime(*entry.updated_parsed[:6])

                # Only include recent articles
                if pub_date and pub_date >= yesterday:
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', '')[:300]
                    })
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")

    return articles[:15]  # Return top 15 most recent

def generate():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    today = date.today().isoformat()

    # Fetch recent articles
    articles = fetch_recent_articles()

    if not articles:
        content = "No major AI developments today."
    else:
        # Format articles for GPT
        articles_text = "\n\n".join([
            f"Title: {a['title']}\nLink: {a['link']}\nSummary: {a['summary']}"
            for a in articles
        ])

        prompt = f"""Here are recent AI news articles. Summarize 10 of the most important/interesting ones.

{articles_text}

Rules:
- Pick 10 most significant items
- Bullet points format
- 1-2 lines per bullet, include the link
- Neutral, factual tone
- No hype, no emojis
- Format: - **[Title]**: Brief summary ([source](link))
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )

        content = response.choices[0].message.content.strip()

    if content:
        with open("ai-news.md", "a") as f:
            f.write(f"\n\n## {today}\n{content}\n")

if __name__ == "__main__":
    generate()
