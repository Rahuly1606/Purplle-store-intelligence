import pandas as pd

csv_file = r"data/metadata/Brigade_Bangalore_10_April_26.csv"

df = pd.read_csv(csv_file)

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nSHAPE:")
print(df.shape)

print("\nFIRST 10 ROWS:")
print(df.head(10))