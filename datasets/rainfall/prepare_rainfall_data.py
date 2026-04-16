import pandas as pd

# load datasets
df1 = pd.read_csv("datasets/rainfall/rainfall_2021.csv")
df2 = pd.read_csv("datasets/rainfall/rainfall_2022.csv")
df3 = pd.read_csv("datasets/rainfall/rainfall_2023.csv")

# merge datasets
df = pd.concat([df1, df2, df3])

# districts we want
districts = ["Chennai", "Chengalpattu", "Thiruvallur", "Kanchipuram", "Tiruvallur"]

# filter region
df = df[df["District"].isin(districts)]

# convert date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# keep only required columns
df = df[["Date", "District", "Avg_rainfall"]]

# rename column
df.rename(columns={"Avg_rainfall": "rainfall_mm"}, inplace=True)

# sort values
df = df.sort_values(by="Date")

# save processed dataset
df.to_csv("datasets/processed/chennai_rainfall_timeseries.csv", index=False)

print("Rainfall dataset prepared successfully!")
print("Total rows:", len(df))
print(df.head())