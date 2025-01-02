import pandas as pd
import matplotlib.pyplot as plt
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_chart = os.path.join(output_dir, 'customer_sentiment_vs_popularity.png')

# Load the dataset
df = pd.read_csv(file_path)

# Ensure 'Stars' and 'Reviews Count' columns have valid values
df = df[df['Stars'].notna() & df['Reviews Count'].notna()]
df['Reviews Count'] = pd.to_numeric(df['Reviews Count'], errors='coerce')
df = df[df['Reviews Count'] > 0]

# Display counts for high ratings and low reviews
high_rating_count = df[df['Stars'] >= 4.5].shape[0]
low_review_count = df[df['Reviews Count'] < 10].shape[0]
print(f"Products with high ratings (>=4.5): {high_rating_count}")
print(f"Products with low review counts (<10): {low_review_count}")

# Plot all products by review count and star rating
plt.figure(figsize=(10, 6))
plt.scatter(df['Reviews Count'], df['Stars'], color='teal', alpha=0.5)
plt.xlabel("Number of Reviews")
plt.ylabel("Star Rating")
plt.title("Customer Sentiment vs. Popularity (All Ratings)")
plt.tight_layout()
plt.savefig(output_chart)
plt.show()

print(f"Customer Sentiment vs. Popularity chart saved to {output_chart}")
