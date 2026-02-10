import os
import requests
from datetime import date
from openai import OpenAI
from tavily import TavilyClient
from urllib.parse import quote

def generate():
    # Initialize clients
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    today = date.today()
    today_str = today.isoformat()

    # Generate monthly filename (e.g., feb-ai-news.md)
    month_name = today.strftime("%b").lower()  # jan, feb, mar, etc.
    filename = f"{month_name}-ai-news.md"

    # Search for AI news using Tavily
    try:
        search_response = tavily_client.search(
            query=f"artificial intelligence AI machine learning news {today_str}",
            search_depth="advanced",
            max_results=15
        )

        results = search_response.get('results', [])

        if not results:
            content = "No major AI developments today."
        else:
            # Format results for GPT
            articles_text = "\n\n".join([
                f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content'][:400]}"
                for r in results
            ])

            prompt = f"""Here are recent AI news articles from today. Summarize 10 of the most important/interesting ones.

{articles_text}

Rules:
- Pick 10 most significant items
- Bullet points format
- 1-2 lines per bullet, include the link
- Neutral, factual tone
- No hype, no emojis
- Format: - **[Title]**: Brief summary ([source](url))
"""

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
            )

            content = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {e}")
        content = "Error fetching AI news today."

    if content:
        # Create file with header if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(f"# AI News - {today.strftime('%B %Y')}\n\n")

        with open(filename, "a") as f:
            f.write(f"\n## {today_str}\n{content}\n")

if __name__ == "__main__":
    generate()
