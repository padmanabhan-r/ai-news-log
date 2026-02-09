import os
from datetime import date
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    today = date.today().isoformat()

    prompt = f"""
Using Google Search grounding, summarize 3-5 important AI-related news items
from TODAY ({today}).

Rules:
- AI / ML / LLMs / robotics / chips / regulation only
- Bullet points
- 1-2 lines per bullet
- Neutral, factual tone
- Include a source link per bullet
- No hype, no emojis
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    tools = [
        types.Tool(
            googleSearch=types.GoogleSearch()
        ),
    ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
    )

    response_text = ""

    for chunk in client.models.generate_content_stream(
        model="gemini-3-flash-preview",
        contents=contents,
        config=config,
    ):
        if chunk.text:
            response_text += chunk.text

    with open("ai-news.md", "a") as f:
        f.write(f"\n\n## {today}\n{response_text.strip()}\n")


if __name__ == "__main__":
    generate()
