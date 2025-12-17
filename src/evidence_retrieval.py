import requests
import urllib.parse
import re

# ==============================
# CONFIG
# ==============================

API_KEY = "pub_444e5f779b4f47e2bc9cbfac5dde1b84"
BASE_URL = "https://newsdata.io/api/1/latest"
TOP_N = 5


# ==============================
# CLAIM CLEANING
# ==============================

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


# ==============================
# FETCH NEWS
# ==============================

def fetch_news_for_claim(claim: str, language: str = "en"):
    encoded_claim = urllib.parse.quote(claim)

    url = (
        f"{BASE_URL}"
        f"?apikey={API_KEY}"
        f"&q={encoded_claim}"
        f"&language={language}"
        f"&removeduplicate=1"
        f"&sort=relevancy"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Request Error:", e)
        return None


# ==============================
# PARSE ARTICLES
# ==============================

def parse_articles(data):
    articles = []

    for item in data.get("results", []):
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "source": item.get("source_id", ""),
            "published_at": item.get("pubDate", ""),
            "url": item.get("link", "")
        })

    return articles


# ==============================
# RELEVANCE SCORING
# ==============================

def relevance_score(claim: str, text: str) -> int:
    claim_words = set(clean_text(claim).split())
    text_words = set(clean_text(text).split())
    return len(claim_words.intersection(text_words))


def get_top_relevant_articles(claim, articles, top_n=TOP_N):
    scored_articles = []

    for article in articles:
        combined_text = f"{article['title']} {article['description']}"
        score = relevance_score(claim, combined_text)

        if score > 0:
            article["relevance_score"] = score
            scored_articles.append(article)

    scored_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored_articles[:top_n]


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    claim = "Lionel Messi came to Kolkata on December 2025"

    print("🔍 Searching evidence for claim:")
    print(f'   "{claim}"')

    data = fetch_news_for_claim(claim)

    if not data or not data.get("results"):
        print("\n⚠️ No evidence found.")
        exit()

    articles = parse_articles(data)
    top_articles = get_top_relevant_articles(claim, articles)
    #print(top_articles)
    if top_articles:
        print(f"\n✅ Top {len(top_articles)} relevant articles:\n")
        for i, a in enumerate(top_articles, 1):
            print(f"{i}. {a['title']}")
            print(f"   Source: {a['source']}")
            print(f"   Published: {a['published_at']}")
            print(f"   Relevance Score: {a['relevance_score']}")
            print(f"   URL: {a['url']}\n")
    else:
        print("\n⚠️ No highly relevant evidence found.")