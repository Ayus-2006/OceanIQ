from pathlib import Path
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

DATA = Path("data")

INPUT_FILE = DATA / "processed" / "training_dataset.csv"
OUTPUT_FILE = DATA / "processed" / "model_dataset.csv"

# ==========================================================
# Load Data
# ==========================================================

print("Loading training dataset...")

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)

# ==========================================================
# Calendar Features
# ==========================================================

print("Creating calendar features...")

df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["day_of_week"] = df["date"].dt.dayofweek
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
df["day_of_month"] = df["date"].dt.day

# ==========================================================
# Lag Features
# ==========================================================

print("Creating lag features...")

df["lag_1"] = df["freight_rate"].shift(1)
df["lag_3"] = df["freight_rate"].shift(3)
df["lag_7"] = df["freight_rate"].shift(7)
df["lag_14"] = df["freight_rate"].shift(14)
df["lag_30"] = df["freight_rate"].shift(30)

# ==========================================================
# Moving Averages
# ==========================================================

print("Creating moving averages...")

df["ma_3"] = df["freight_rate"].rolling(3).mean()
df["ma_7"] = df["freight_rate"].rolling(7).mean()
df["ma_14"] = df["freight_rate"].rolling(14).mean()
df["ma_30"] = df["freight_rate"].rolling(30).mean()

# ==========================================================
# Rolling Volatility
# ==========================================================

print("Creating rolling volatility...")

df["rolling_std_7"] = df["freight_rate"].rolling(7).std()
df["rolling_std_14"] = df["freight_rate"].rolling(14).std()
df["rolling_std_30"] = df["freight_rate"].rolling(30).std()

# ==========================================================
# Clean Data
# ==========================================================

print("Removing incomplete rows...")

df = df.drop(columns=["summary"], errors="ignore")

df["confidence"] = df["confidence"].fillna(0)

df = df.dropna(subset=[
        "lag_1",
        "lag_3",
        "lag_7",
        "lag_14",
        "lag_30"
    ]).reset_index(drop=True)

# ==========================================================
# Save
# ==========================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nFeature engineering complete!")
print(f"Saved to: {OUTPUT_FILE}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(df.head())