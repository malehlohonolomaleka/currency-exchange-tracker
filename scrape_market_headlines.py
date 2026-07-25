"""
scrape_market_headlines.py
----------------------------
Demonstrates web scraping fundamentals: requesting a page, parsing HTML
with BeautifulSoup, and extracting structured data into a clean CSV.

Targets https://quotes.toscrape.com — a site explicitly built and
maintained for scraping practice (no ToS concerns, safe to reference in
a portfolio). The same pattern (request -> parse -> extract -> save)
applies directly to scraping real financial news headlines, product
listings, or job boards.

Run: python scrape_market_headlines.py
Output: ./scraped_quotes.csv
"""

import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
OUTPUT_FILE = "./scraped_quotes.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-demo-scraper)"}


def scrape_all_pages():
    """Walk through every paginated page on the site and collect quotes."""
    records = []
    url = BASE_URL
    page_num = 1

    while url:
        print(f"Scraping page {page_num}: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_block in soup.select(".quote"):
            text = quote_block.select_one(".text").get_text(strip=True)
            author = quote_block.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in quote_block.select(".tags .tag")]
            records.append({
                "text": text,
                "author": author,
                "tags": ", ".join(tags),
            })

        next_link = soup.select_one("li.next a")
        url = BASE_URL + next_link["href"] if next_link else None
        page_num += 1
        time.sleep(1)  # polite delay between requests

    return records


def save_to_csv(records):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(records)


def main():
    records = scrape_all_pages()
    save_to_csv(records)
    print(f"Scraped {len(records)} quotes -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
