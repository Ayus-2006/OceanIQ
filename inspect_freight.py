import pandas as pd

file = "data/raw/freight/ROW DASHBOARD.xlsx"

df = pd.read_excel(
    file,
    sheet_name="Sheet1",
    engine="openpyxl"
)

print("O/F values:")
print(df["O/F"].head(20))

print("\nMissing values:")
print(df["O/F"].isna().sum())

print("\nUnique values:")
print(df["O/F"].unique()[:20])