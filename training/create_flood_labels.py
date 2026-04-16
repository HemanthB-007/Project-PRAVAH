import pandas as pd

# load rainfall dataset
df = pd.read_csv("datasets/processed/rainfall_features.csv")

df["Date"] = pd.to_datetime(df["Date"])

# initialize flood column
df["flood_event"] = 0

# known flood dates
flood_dates = pd.date_range(start="2021-11-01", end="2021-11-10")

df.loc[df["Date"].isin(flood_dates), "flood_event"] = 1

# cyclone Michaung event
flood_dates2 = pd.date_range(start="2023-12-01", end="2023-12-05")

df.loc[df["Date"].isin(flood_dates2), "flood_event"] = 1

df.to_csv("datasets/processed/rainfall_with_flood_labels.csv", index=False)

print("Flood labels created successfully")
print(df["flood_event"].value_counts())