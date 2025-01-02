import pandas as pd
import os
import matplotlib.pyplot as plt

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)

# Load the dataset
df = pd.read_csv(file_path)

# Ensure that 'Sale Price USD' is numeric
df['Sale Price USD'] = pd.to_numeric(df['Sale Price USD'], errors='coerce')

# Remove rows with missing price data
df = df.dropna(subset=['Sale Price USD'])

# Find the top 10 most expensive products
most_expensive = df.nlargest(10, 'Sale Price USD')

# Find the top 10 least expensive products
least_expensive = df.nsmallest(10, 'Sale Price USD')

# Simplify product names for cleaner charts
most_expensive['Short Name'] = most_expensive['Product'].apply(lambda x: ' '.join(str(x).split()[:3]) + '...')
least_expensive['Short Name'] = least_expensive['Product'].apply(lambda x: ' '.join(str(x).split()[:3]) + '...')

# Combine both results for easy export
expensive_summary = pd.concat([most_expensive, least_expensive])
output_file = os.path.join(output_dir, 'expensive_summary.csv')
expensive_summary.to_csv(output_file, index=False)

# Display the summary
print("Most Expensive Products:")
print(most_expensive[['Short Name', 'Sale Price USD', 'Seller', 'Marca']])

print("\nLeast Expensive Products:")
print(least_expensive[['Short Name', 'Sale Price USD', 'Seller', 'Marca']])

print(f"Summary of most and least expensive products saved to {output_file}")

# Plot the top 10 most expensive products
plt.figure(figsize=(10, 6))
plt.barh(most_expensive['Short Name'], most_expensive['Sale Price USD'], color='green')
plt.xlabel('Sale Price USD')
plt.ylabel('Product')
plt.title('Top 10 Most Expensive Products')
plt.gca().invert_yaxis()  # Highest price on top
plt.tight_layout()
most_expensive_chart = os.path.join(output_dir, 'most_expensive_chart.png')
plt.savefig(most_expensive_chart)
plt.show()

# Plot the top 10 least expensive products
plt.figure(figsize=(10, 6))
plt.barh(least_expensive['Short Name'], least_expensive['Sale Price USD'], color='blue')
plt.xlabel('Sale Price USD')
plt.ylabel('Product')
plt.title('Top 10 Least Expensive Products')
plt.gca().invert_yaxis()  # Lowest price on top
plt.tight_layout()
least_expensive_chart = os.path.join(output_dir, 'least_expensive_chart.png')
plt.savefig(least_expensive_chart)
plt.show()

print(f"Charts saved as {most_expensive_chart} and {least_expensive_chart}")
