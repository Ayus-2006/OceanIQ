from pathlib import Path

import pandas as pd

from xgboost import XGBRegressor

# ==========================================
# Paths
# ==========================================

DATA = Path("data")

MODEL = Path("models/freight_model.json")

INPUT = DATA / "processed" / "model_dataset.csv"

OUTPUT = DATA / "processed" / "prediction.csv"

# ==========================================
# Load model
# ==========================================

print("Loading model...")

model = XGBRegressor()

model.load_model(MODEL)

# ==========================================
# Load latest data
# ==========================================

print("Loading latest data...")

df = pd.read_csv(INPUT)

latest = df.iloc[[-1]].copy()

prediction_date = (
    pd.to_datetime(latest["date"].iloc[0])
    + pd.Timedelta(days=1)
)

X = latest.drop(
    columns=[
        "date",
        "freight_rate"
    ]
)

prediction = model.predict(X)[0]

prediction_df = pd.DataFrame({
    "prediction_date": [prediction_date.date()],
    "predicted_freight_rate": [round(prediction, 2)]
})

prediction_df.to_csv(
    OUTPUT,
    index=False
)

print()
print(prediction_df)
print()
print("Saved to", OUTPUT)