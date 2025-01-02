import pandas as pd
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_file = os.path.join(output_dir, 'updated_dataset_with_sale_price.csv')

# Load the dataset
df = pd.read_csv(file_path)

# Ensure 'USD' column is string type before removing commas, then convert to numeric
df['USD'] = pd.to_numeric(df['USD'].astype(str).str.replace(',', ''), errors='coerce')

# Calculate sale price by parsing 'Discount' column
def calculate_sale_price(row):
    if "OFF" in row['Discount']:
        discount_percent = float(row['Discount'].replace('% OFF', '').strip()) / 100
        sale_price = row['USD'] * (1 - discount_percent)
    else:
        sale_price = row['USD']  # No discount
    return round(sale_price, 2)

# Apply function to calculate sale price
df['Sale Price USD'] = df.apply(calculate_sale_price, axis=1)

# Save the updated dataset
df.to_csv(output_file, index=False)
print(f"Updated dataset with sale price saved to: {output_file}")
