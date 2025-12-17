import requests
from bs4 import BeautifulSoup

def fetch_article_text(url: str) -> str:
    """
    Fetches main readable text from a given webpage URL.
    Designed for news articles, blogs, and text-heavy pages.
    Returns extracted text as a single clean string.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try common article containers
        targets = [
            ("article", None, None),                           # <article>
            ("div", "post-content", "class"),                 # class="post-content"
            ("div", "entry-content", "class"),                # class="entry-content"
            ("div", "article-content", "class"),              # class="article-content"
            ("div", "blog-content", "class"),                 # class="blog-content"
            ("div", "main-content", "id"),                    # id="main-content"
        ]

        article_text = ""

        for tag, value, attr in targets:
            if attr == "class":
                container = soup.find(tag, class_=value)
            elif attr == "id":
                container = soup.find(tag, id=value)
            else:
                container = soup.find(tag)

            if container:
                article_text = container.get_text(separator="\n", strip=True)
                break

        # If nothing matched, fallback to full page text
        if not article_text:
            article_text = soup.get_text(separator="\n", strip=True)

        # Cleanup: remove very short lines, trim whitespace
        cleaned = []
        for line in article_text.split("\n"):
            line = line.strip()
            if len(line) > 50:      # filters out menus/headers/footers
                cleaned.append(line)

        return "\n".join(cleaned)

    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    test_url = "https://www.district.in/events/messi-2025-india-tour-ticket-booking"

    text = fetch_article_text(test_url)

    print("\n===== SCRAPED ARTICLE TEXT =====\n")
    print(text)
    print("\n===== END =====\n")
