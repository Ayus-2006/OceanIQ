from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

# ===========================================
# Paths
# ===========================================

DATA = Path("data")
MODEL_PATH = Path("models/freight_model.json")

# ===========================================
# Load Dataset
# ===========================================

print("Loading dataset...")

df = pd.read_csv(
    DATA / "processed" / "model_dataset.csv"
)

# ===========================================
# Features
# ===========================================

X = df.drop(
    columns=[
        "date",
        "freight_rate"
    ]
)

y = df["freight_rate"]

print(f"Rows: {len(df)}")
print(f"Features: {len(X.columns)}")

# ===========================================
# Train/Test Split
# ===========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ===========================================
# Model
# ===========================================

print("\nTraining model...")

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42,
    objective="reg:squarederror"
)

model.fit(
    X_train,
    y_train
)

# ===========================================
# Predictions
# ===========================================

predictions = model.predict(
    X_test
)

# ===========================================
# Metrics
# ===========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("\n" + "=" * 50)
print("Model Performance")
print("=" * 50)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

# ===========================================
# Save Model
# ===========================================

MODEL_PATH.parent.mkdir(
    exist_ok=True
)

model.save_model(
    MODEL_PATH
)

print("\nModel saved successfully!")
print(f"Saved to: {MODEL_PATH}")

print("=" * 50)