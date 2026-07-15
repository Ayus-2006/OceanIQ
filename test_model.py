from xgboost import XGBRegressor

model = XGBRegressor()

model.load_model("models/freight_model.json")

print("Loaded successfully!")