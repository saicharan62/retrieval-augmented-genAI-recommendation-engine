"""
scrape.py

Scrapes SHL Individual Test Solutions from the SHL product catalog
and saves them into a clean CSV file.

This script is meant to be run once (or occasionally).
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

OUTPUT_PATH = "data/shl_catalog.csv"


def get_soup(url: str) -> BeautifulSoup:
    """
    Fetches a URL and returns a BeautifulSoup object.
    """
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def is_individual_solution(card) -> bool:
    """
    Returns True if the product card corresponds to
    an Individual Test Solution.

    We explicitly exclude 'Pre-packaged Job Solutions'.
    """
    category = card.find("span", class_="product-type")
    if not category:
        return False

    return "Individual" in category.get_text(strip=True)


def parse_product_page(url: str) -> dict:
    """
    Parses a single assessment detail page and extracts
    required fields.
    """
    soup = get_soup(url)

    def safe_text(selector, default=""):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else default

    return {
        "name": safe_text("h1"),
        "url": url,
        "description": safe_text(".product-description"),
        "test_type": safe_text(".test-type"),  # K / P
        "duration": safe_text(".duration"),
        "remote_support": safe_text(".remote-testing"),
        "adaptive_support": safe_text(".adaptive-testing"),
    }


def scrape_catalog() -> pd.DataFrame:
    """
    Main scraping logic:
    - Loads catalog page
    - Finds all product cards
    - Filters Individual Test Solutions
    - Visits each product page
    """
    print("Loading SHL product catalog...")
    soup = get_soup(CATALOG_URL)

    product_cards = soup.select(".product-card")
    print(f"Found {len(product_cards)} product cards")

    records = []

    for card in product_cards:
        if not is_individual_solution(card):
            continue

        link = card.find("a", href=True)
        if not link:
            continue

        product_url = BASE_URL + link["href"]

        try:
            record = parse_product_page(product_url)
            records.append(record)
            print(f"Scraped: {record['name']}")
            sleep(0.5)  # be polite to the server
        except Exception as e:
            print(f"Failed to scrape {product_url}: {e}")

    return pd.DataFrame(records)


def main():
    df = scrape_catalog()

    print(f"\nTotal individual assessments scraped: {len(df)}")

    if len(df) < 377:
        raise ValueError(
            "Less than 377 assessments scraped. "
            "This does not meet assignment requirements."
        )

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved catalog to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
