import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.scrap_text_from_link import fetch_article_text
url = "https://www.district.in/events/messi-2025-india-tour-ticket-booking"
scraped_text = fetch_article_text(url)
if scraped_text is None:
    print("Failed to scrape article or extracted text was empty")
else:
    print(f"Scraped text length: {len(scraped_text)} characters")
    print(scraped_text)