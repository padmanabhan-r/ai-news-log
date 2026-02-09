import os
from datetime import date
from openai import OpenAI

def generate():
    client = OpenAI(
        api_key=os.environ["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai"
    )

    today = date.today().isoformat()

    prompt = f"""
Search the web and summarize 3-5 important AI-related news items from TODAY ({today}).

Rules:
- AI / ML / LLMs / robotics / chips / regulation only
- Bullet points
- 1-2 lines per bullet
- Neutral, factual tone
- No hype, no emojis
- If there is no major news, say "No major AI developments today."
"""

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    content = response.choices[0].message.content.strip()

    if not content:
        return

    with open("ai-news.md", "a") as f:
        f.write(f"\n\n## {today}\n{content}\n")


if __name__ == "__main__":
    generate()
