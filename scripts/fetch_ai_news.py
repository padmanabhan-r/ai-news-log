import os
from datetime import date
from perplexity import Perplexity

def generate():
    client = Perplexity(api_key=os.environ["PERPLEXITY_API_KEY"])

    today = date.today().isoformat()

    # Search for AI news from today
    search = client.search.create(
        query=f"AI artificial intelligence machine learning news {today}",
        max_results=10,
        max_tokens_per_page=2048
    )

    if not search.results:
        content = "No major AI developments today."
    else:
        # Format the results as a summary
        items = []
        for i, result in enumerate(search.results[:5]):  # Top 5 results
            snippet = result.snippet[:150].strip()
            if snippet:
                items.append(f"- **{result.title}**: {snippet}... ([source]({result.url}))")

        content = "\n".join(items) if items else "No major AI developments today."

    if not content:
        return

    with open("ai-news.md", "a") as f:
        f.write(f"\n\n## {today}\n{content}\n")


if __name__ == "__main__":
    generate()
