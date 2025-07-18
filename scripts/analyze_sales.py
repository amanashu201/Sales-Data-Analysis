import pandas as pd

# Load the sales data
df = pd.read_csv('data/sales.csv')

# Show first 5 rows
print("First 5 rows:")
print(df.head())

# Total quantity sold by product
print("\nTotal quantity sold by product:")
print(df.groupby('Product')['Quantity'].sum())

# Total sales amount by product
df['SalesAmount'] = df['Quantity'] * df['Price']
print("\nTotal sales amount by product:")
print(df.groupby('Product')['SalesAmount'].sum())