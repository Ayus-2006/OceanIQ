"""
fred.py

Downloads macroeconomic indicators from FRED.

Author: Ayushman Sinha
Project: OceanIQ
"""

from pathlib import Path
from fredapi import Fred
from utils.config import FRED_API_KEY

# ==========================================================
# Configuration
# ==========================================================

DATA_DIR = Path("data/external/fred")
DATA_DIR.mkdir(parents=True, exist_ok=True)

fred = Fred(api_key=FRED_API_KEY)

FRED_SERIES = {
    "federal_funds_rate": "FEDFUNDS",
    "consumer_price_index": "CPIAUCSL",
    "producer_price_index": "PPIACO",
    "unemployment_rate": "UNRATE",
    "industrial_production": "INDPRO",
}

# ==========================================================
# Functions
# ==========================================================

def download_all():
    """
    Downloads all FRED datasets defined in FRED_SERIES.
    """

    print("=" * 60)
    print("OceanIQ FRED Data Pipeline")
    print("=" * 60)

    successful = 0

    for filename, series in FRED_SERIES.items():
        try:
            print(f"Downloading {filename}...")

            data = fred.get_series(series)

            output_file = DATA_DIR / f"{filename}.csv"
            data.to_csv(output_file, header=["value"])

            print(f"Saved -> {output_file}")
            successful += 1

        except Exception as e:
            print(f"Failed: {filename}")
            print(e)

    print("\nDownload Complete")
    print(f"{successful}/{len(FRED_SERIES)} datasets downloaded.")

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    download_all()