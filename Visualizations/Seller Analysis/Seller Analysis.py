import pandas as pd
import matplotlib.pyplot as plt
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_file = os.path.join(output_dir, 'seller_analysis.csv')

# Load the dataset
df = pd.read_csv(file_path)

# Ensure 'Sale Price USD' and 'Stars' are numeric
df['Sale Price USD'] = pd.to_numeric(df['Sale Price USD'], errors='coerce')
df['Stars'] = pd.to_numeric(df['Stars'], errors='coerce')

# Filter out rows with 0-star ratings (or NaN reviews)
df = df[df['Stars'] > 0]

# Group by seller to calculate metrics
seller_analysis = df.groupby('Seller').agg(
    Product_Count=('Product', 'count'),
    Average_Price=('Sale Price USD', 'mean'),
    Average_Rating=('Stars', 'mean')
).reset_index()

# Save the analysis to a CSV file
seller_analysis.to_csv(output_file, index=False)

# Filter for top 50 sellers by product count
top_50_sellers = seller_analysis.nlargest(50, 'Product_Count')

# Chart: Top 20 Sellers by Product Count
top_20_sellers = top_50_sellers.nlargest(20, 'Product_Count')
plt.figure(figsize=(12, 8))
plt.barh(top_20_sellers['Seller'], top_20_sellers['Product_Count'], color='skyblue')
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.title("Top 20 Sellers by Number of Products")
plt.xlabel("Number of Products")
plt.ylabel("Seller")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_20_sellers_by_product_count.png'))
plt.show()

# Chart: Top 10 Highest Rated Sellers from Top 50 by Product Count
top_10_highest_rated = top_50_sellers.nlargest(10, 'Average_Rating')
plt.figure(figsize=(12, 8))
plt.barh(top_10_highest_rated['Seller'], top_10_highest_rated['Average_Rating'], color='green')
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.title("Top 10 Highest Rated Sellers (Top 50 by Product Count)")
plt.xlabel("Average Rating")
plt.ylabel("Seller")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_10_highest_rated_sellers_top_50.png'))
plt.show()

# Chart: Top 10 Lowest Rated Sellers from Top 50 by Product Count
top_10_lowest_rated = top_50_sellers.nsmallest(10, 'Average_Rating')
plt.figure(figsize=(12, 8))
plt.barh(top_10_lowest_rated['Seller'], top_10_lowest_rated['Average_Rating'], color='red')
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.title("Top 10 Lowest Rated Sellers (Top 50 by Product Count)")
plt.xlabel("Average Rating")
plt.ylabel("Seller")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_10_lowest_rated_sellers_top_50.png'))
plt.show()
