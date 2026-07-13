"""
macro.py

Downloads macroeconomic data from Yahoo Finance and saves it as CSV files.

Author: Ayushman Sinha
Project: OceanIQ
"""

from pathlib import Path
import yfinance as yf

# ==========================================================
# Configuration
# ==========================================================

DATA_DIR = Path("data/external")
DATA_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2015-01-01"

# Add new datasets here
MACRO_SERIES = {
    "brent_oil": "BZ=F",
    "gold": "GC=F",
    "silver": "SI=F",
    "natural_gas": "NG=F",
    "usd_index": "DX-Y.NYB",
    "eur_usd": "EURUSD=X",
    "usd_jpy": "JPY=X",
}

# ==========================================================
# Functions
# ==========================================================

def download_yahoo_data(symbol: str, dataset_name: str):
    """
    Downloads historical data from Yahoo Finance.

    Parameters
    ----------
    symbol : str
        Yahoo Finance ticker symbol.

    dataset_name : str
        Name used when saving the CSV.

    Returns
    -------
    bool
        True if download succeeded.
    """

    print(f"Downloading {dataset_name} ({symbol})...")

    try:
        df = yf.download(
            symbol,
            start=START_DATE,
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            print(f"No data returned for {dataset_name}")
            return False

        output_file = DATA_DIR / f"{dataset_name}.csv"

        df.to_csv(output_file)

        print(f"Saved -> {output_file}")

        return True

    except Exception as e:
        print(f"Failed downloading {dataset_name}")
        print(e)
        return False


def download_all_macro():
    """
    Downloads every macroeconomic dataset defined in MACRO_SERIES.
    """

    print("=" * 60)
    print("OceanIQ Macroeconomic Data Pipeline")
    print("=" * 60)

    successful = 0

    for dataset_name, symbol in MACRO_SERIES.items():

        success = download_yahoo_data(
            symbol,
            dataset_name
        )

        if success:
            successful += 1

    print("\nDownload Complete")
    print(f"{successful}/{len(MACRO_SERIES)} datasets downloaded.")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    download_all_macro()