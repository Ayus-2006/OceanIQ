from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

# ===========================================
# Load Dataset
# ===========================================

DATA = Path("data")

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

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# ===========================================
# Predictions
# ===========================================

predictions = model.predict(X_test)

# ===========================================
# Metrics
# ===========================================

mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("="*50)

print("MAE :", round(mae,2))
print("RMSE:", round(rmse,2))
print("R²  :", round(r2,3))

print("="*50)

# ===========================================
# Save Model
# ===========================================

Path("models").mkdir(exist_ok=True)

joblib.dump(
    model,
    "models/freight_model.pkl"
)

print("Model saved.")