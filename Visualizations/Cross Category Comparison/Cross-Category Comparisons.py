import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import os

# Normalize function to handle accents
def normalize(text):
    if isinstance(text, str):  # Only process strings
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text  # Return as-is if not a string

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)

# Load the dataset
df = pd.read_csv(file_path)

# Ensure numeric conversion for relevant columns
df['Sale Price USD'] = pd.to_numeric(df['Sale Price USD'], errors='coerce')

# Normalize and clean up the Category column
df['Category'] = df['Category'].astype(str).apply(normalize)  # Normalize to handle accents
df['Category'] = df['Category'].replace(['Unknown', 'Otras Categorias', 'nan'], 'Otras Categorias')  # Combine categories and handle NaN

# Calculate average price per category
category_summary = df.groupby('Category').agg({
    'Sale Price USD': 'mean'
}).rename(columns={
    'Sale Price USD': 'Average Price (USD)'
}).reset_index()

# Sort categories by average price
category_summary = category_summary.sort_values(by='Average Price (USD)', ascending=True)

# Save the summary to a CSV
summary_file = os.path.join(output_dir, 'category_summary.csv')
category_summary.to_csv(summary_file, index=False)
print(f"Category summary saved to {summary_file}")

# Plotting the Average Price by Category as a Horizontal Bar Chart
plt.figure(figsize=(10, 8))
plt.barh(category_summary['Category'], category_summary['Average Price (USD)'], color='skyblue')
plt.title("Average Price by Category")
plt.xlabel("Average Price (USD)")
plt.ylabel("Category")
plt.tight_layout()

# Save the chart
output_chart = os.path.join(output_dir, 'average_price_by_category.png')
plt.savefig(output_chart)
plt.show()

print(f"Average price by category chart saved to {output_chart}")
