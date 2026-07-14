"""
weather.py

Downloads historical weather data for major European ports
using the Open-Meteo Archive API.

Author: Ayushman Sinha
Project: OceanIQ
"""

from pathlib import Path
import requests
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

DATA_DIR = Path("data/external/weather")
DATA_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2020-01-01"
END_DATE = "2025-12-31"

PORTS = {
    "Rotterdam": (51.9244, 4.4777),
    "Antwerp": (51.2602, 4.3997),
    "Hamburg": (53.5461, 9.9661),
    "Bremerhaven": (53.5396, 8.5809),
    "Le_Havre": (49.4944, 0.1079),
    "Felixstowe": (51.9630, 1.3511),
    "Barcelona": (41.3525, 2.1589),
    "Valencia": (39.4480, -0.3167),
    "Genoa": (44.4048, 8.9463),
    "Piraeus": (37.9420, 23.6465),
}

# ==========================================================
# Functions
# ==========================================================

def download_weather(port_name, latitude, longitude):

    print(f"Downloading weather for {port_name}...")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={START_DATE}"
        f"&end_date={END_DATE}"
        "&daily="
        "temperature_2m_mean,"
        "precipitation_sum,"
        "wind_speed_10m_max"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "daily" not in data:
        print(f"No weather data for {port_name}")
        return

    df = pd.DataFrame(data["daily"])

    output_file = DATA_DIR / f"{port_name}.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")


def download_all():

    print("=" * 60)
    print("OceanIQ Weather Pipeline")
    print("=" * 60)

    for port, coordinates in PORTS.items():

        latitude, longitude = coordinates

        try:
            download_weather(port, latitude, longitude)

        except Exception as e:
            print(f"Failed downloading {port}")
            print(e)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    download_all()