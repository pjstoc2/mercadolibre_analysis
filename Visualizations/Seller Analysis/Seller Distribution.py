import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)

# Load the dataset
df = pd.read_csv(file_path)

# Group by seller to count the number of products each seller has
seller_counts = df.groupby('Seller').size()

# Count how many sellers have each specific number of products
distribution = seller_counts.value_counts().sort_index()

# Convert the distribution to a DataFrame for clarity (optional)
distribution_df = pd.DataFrame({
    'Number of Products': distribution.index,
    'Number of Sellers': distribution.values
})

# Save the distribution data to a CSV file
output_file = os.path.join(output_dir, 'seller_product_distribution.csv')
distribution_df.to_csv(output_file, index=False)
print(f"Seller product distribution saved to {output_file}")

# Chart 1: Standard Y-Axis (Number Format)
plt.figure(figsize=(12, 8))
plt.bar(distribution.index, distribution.values, color='skyblue')
plt.title("Distribution of Sellers by Number of Products Listed (Standard Y-Axis)")
plt.xlabel("Number of Products")
plt.ylabel("Number of Sellers")
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))  # Standard number format
plt.tight_layout()
standard_chart = os.path.join(output_dir, 'seller_product_distribution_standard.png')
plt.savefig(standard_chart)
plt.show()

# Chart 2: Logarithmic Y-Axis (10^3 Scale)
plt.figure(figsize=(12, 8))
plt.bar(distribution.index, distribution.values, color='orange')
plt.title("Distribution of Sellers by Number of Products Listed (Logarithmic Scale)")
plt.xlabel("Number of Products")
plt.ylabel("Number of Sellers")
plt.yscale('log')  # Logarithmic scale
plt.gca().yaxis.set_major_formatter(mticker.LogFormatterSciNotation())  # Scientific notation
plt.tight_layout()
log_chart = os.path.join(output_dir, 'seller_product_distribution_log.png')
plt.savefig(log_chart)
plt.show()

print(f"Charts saved as:\n - {standard_chart}\n - {log_chart}")
