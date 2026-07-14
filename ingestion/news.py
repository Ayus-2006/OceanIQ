"""
news.py

Downloads shipping-related news from GDELT.

Author: Ayushman Sinha
Project: OceanIQ
"""

from pathlib import Path
import requests
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

DATA_DIR = Path("data/external/news")
DATA_DIR.mkdir(parents=True, exist_ok=True)

KEYWORDS = [
    "Ocean Freight",
    "Container Shipping",
    "Red Sea",
    "Suez Canal",
    "Panama Canal",
    "Port Strike",
    "Port Congestion",
    "Shipping Disruption",
    "Trade Tariffs",
    "Global Logistics",
]

# ==========================================================
# Functions
# ==========================================================

def search_keyword(keyword):

    print(f"Searching: {keyword}")

    url = (
        "https://api.gdeltproject.org/api/v2/doc/doc"
        f"?query={keyword}"
        "&mode=artlist"
        "&maxrecords=100"
        "&format=json"
    )

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    if "articles" not in data:
        return []

    return data["articles"]


def download_all():

    print("=" * 60)
    print("OceanIQ News Pipeline")
    print("=" * 60)

    all_articles = []

    for keyword in KEYWORDS:

        try:

            articles = search_keyword(keyword)

            all_articles.extend(articles)

            print(f"{len(articles)} articles found")

        except Exception as e:

            print(f"Failed: {keyword}")

            print(e)

    df = pd.DataFrame(all_articles)

    df.drop_duplicates(inplace=True)

    output_file = DATA_DIR / "shipping_news.csv"

    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} unique articles")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    download_all()