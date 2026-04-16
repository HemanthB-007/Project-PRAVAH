import pandas as pd

# load rainfall dataset
df = pd.read_csv("datasets/processed/chennai_rainfall_timeseries.csv")

# convert date
df["Date"] = pd.to_datetime(df["Date"])

# sort by date
df = df.sort_values("Date")

# rainfall rolling features
df["rainfall_3day_avg"] = df["rainfall_mm"].rolling(3).mean()
df["rainfall_7day_avg"] = df["rainfall_mm"].rolling(7).mean()

# remove NaN rows
df = df.dropna()

# save processed dataset
df.to_csv("datasets/processed/rainfall_features.csv", index=False)

print("Rainfall features created successfully")
print(df.head())