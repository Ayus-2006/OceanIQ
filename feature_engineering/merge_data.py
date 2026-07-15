from pathlib import Path
import pandas as pd


# ==========================================================
# Paths
# ==========================================================

DATA = Path("data")

OUTPUT = DATA / "processed" / "training_dataset.csv"


# ==========================================================
# Load Freight (Target)
# ==========================================================

print("Loading freight data...")

freight = pd.read_csv(
    DATA / "processed" / "freight_clean.csv"
)


freight["date"] = pd.to_datetime(
    freight["date"]
)


# Aggregate freight daily

freight_daily = (
    freight
    .groupby("date")
    ["freight_rate"]
    .mean()
    .reset_index()
)


print(
    "Freight rows:",
    len(freight_daily)
)


# ==========================================================
# Load News Risk
# ==========================================================

print("Loading news risk...")

news = pd.read_csv(
    DATA / "processed" / "news_risk_scores.csv"
)


news["date"] = pd.to_datetime(
    news["date"]
)


# ==========================================================
# Merge
# ==========================================================

print("Merging datasets...")


dataset = freight_daily.merge(
    news,
    on="date",
    how="left"
)


# ==========================================================
# Missing values
# ==========================================================

# News may not exist every day

risk_columns = [
    "red_sea_risk",
    "suez_risk",
    "panama_risk",
    "port_strike_risk",
    "tariff_risk",
    "supply_chain_risk"
]


for col in risk_columns:

    if col in dataset.columns:
        dataset[col] = dataset[col].fillna(0)


# ==========================================================
# Save
# ==========================================================

dataset = dataset.sort_values(
    "date"
)


dataset.to_csv(
    OUTPUT,
    index=False
)


print("="*50)
print("Training dataset created")
print(OUTPUT)
print("Rows:", len(dataset))
print("Columns:", list(dataset.columns))
print("="*50)