from pathlib import Path
import pandas as pd


# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = Path(
    "C:\\Users\\user\\Desktop\\RALSON PROJECT\\PROJECTS\\ROW DASHBOARD.xlsx"
)

OUTPUT_FILE = Path(
    "data/processed/freight_clean.csv"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Load Data
# ==========================================================

print("="*60)
print("OceanIQ Freight Pipeline")
print("="*60)

print("Loading freight data...")

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="Sheet1",
    engine="openpyxl"
)

print(f"Loaded {len(df)} rows")


# ==========================================================
# Rename Columns
# ==========================================================

df = df.rename(columns={
    "Planned loading date": "date",
    "Geography": "region",
    "Country": "destination_country",
    "Port": "origin_port",
    "POD": "destination_port",
    "Line": "carrier",
    "Forwarder": "forwarder",
    "O/F": "freight_rate",
    "ROW/RTNA": "trade_type"
})


# ==========================================================
# Keep Required Columns
# ==========================================================

df = df[
    [
        "date",
        "region",
        "destination_country",
        "origin_port",
        "destination_port",
        "carrier",
        "forwarder",
        "trade_type",
        "freight_rate"
    ]
]


# ==========================================================
# Cleaning
# ==========================================================

print("Cleaning data...")


# Convert date
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# Convert freight rate to numeric
# Removes FOB and other text values

df["freight_rate"] = pd.to_numeric(
    df["freight_rate"],
    errors="coerce"
)


# Remove rows without freight rate

before = len(df)

df = df.dropna(
    subset=["freight_rate"]
)

after = len(df)


print(
    f"Removed {before-after} rows without freight rates"
)


# Remove duplicates

df = df.drop_duplicates()


# Sort by date

df = df.sort_values(
    "date"
)


# ==========================================================
# Create Route Feature
# ==========================================================

df["route"] = (
    df["origin_port"].astype(str)
    + " → "
    + df["destination_port"].astype(str)
)


# ==========================================================
# Save
# ==========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("="*60)
print("Freight pipeline completed")
print(f"Saved: {OUTPUT_FILE}")
print(f"Final rows: {len(df)}")
print("="*60)