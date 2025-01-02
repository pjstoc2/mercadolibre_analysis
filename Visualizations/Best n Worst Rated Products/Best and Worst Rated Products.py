import pandas as pd
import os
import matplotlib.pyplot as plt

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)

# Load the dataset
df = pd.read_csv(file_path)

# Ensure that 'Stars' and 'Reviews Count' are numeric
df['Stars'] = pd.to_numeric(df['Stars'], errors='coerce')
df['Reviews Count'] = pd.to_numeric(df['Reviews Count'], errors='coerce')

# Remove rows with missing star ratings and those with 0 stars or fewer than 1000 reviews
df = df.dropna(subset=['Stars'])
df = df[(df['Stars'] > 0) & (df['Reviews Count'] >= 1000)]

# Find the top 10 best-rated products
best_rated = df.nlargest(10, 'Stars').sort_values(by=['Stars', 'Reviews Count'], ascending=[False, False])

# Find the top 10 worst-rated products
worst_rated = df.nsmallest(10, 'Stars').sort_values(by=['Stars', 'Reviews Count'], ascending=[True, False])

# Find the top 10 most-reviewed products
most_reviewed = df.nlargest(10, 'Reviews Count').sort_values(by='Reviews Count', ascending=False)

# Simplify product names for cleaner charts
best_rated['Short Name'] = best_rated['Product'].apply(lambda x: ' '.join(str(x).split()[:3]) + '...')
worst_rated['Short Name'] = worst_rated['Product'].apply(lambda x: ' '.join(str(x).split()[:3]) + '...')
most_reviewed['Short Name'] = most_reviewed['Product'].apply(lambda x: ' '.join(str(x).split()[:3]) + '...')

# Combine results for export
rating_summary = pd.concat([best_rated, worst_rated, most_reviewed])
output_file = os.path.join(output_dir, 'filtered_rating_summary.csv')
rating_summary.to_csv(output_file, index=False)

# Display summaries
print("Best Rated Products:")
print(best_rated[['Short Name', 'Stars', 'Reviews Count', 'Seller', 'Marca']])

print("\nWorst Rated Products:")
print(worst_rated[['Short Name', 'Stars', 'Reviews Count', 'Seller', 'Marca']])

print("\nMost Reviewed Products:")
print(most_reviewed[['Short Name', 'Stars', 'Reviews Count', 'Seller', 'Marca', 'Sale Price USD']])

print(f"Summary of filtered products saved to {output_file}")

# Plot the top 10 best-rated products
plt.figure(figsize=(10, 6))
plt.barh(best_rated['Short Name'], best_rated['Stars'], color='green', alpha=0.7)
plt.xlabel('Stars')
plt.ylabel('Product')
plt.title('Top 10 Best Rated Products (1000+ Reviews)')
plt.tight_layout()
best_rated_chart = os.path.join(output_dir, 'best_rated_chart_filtered.png')
plt.savefig(best_rated_chart)
plt.show()

# Plot the top 10 worst-rated products
plt.figure(figsize=(10, 6))
plt.barh(worst_rated['Short Name'], worst_rated['Stars'], color='red', alpha=0.7)
plt.xlabel('Stars')
plt.ylabel('Product')
plt.title('Top 10 Worst Rated Products (1000+ Reviews)')
plt.tight_layout()
worst_rated_chart = os.path.join(output_dir, 'worst_rated_chart_filtered.png')
plt.savefig(worst_rated_chart)
plt.show()

# Scatter plot for ratings vs. reviews count
plt.figure(figsize=(10, 6))
plt.scatter(df['Reviews Count'], df['Stars'], alpha=0.5, color='purple')
plt.xlabel('Reviews Count')
plt.ylabel('Stars')
plt.title('Product Ratings vs. Number of Reviews (Filtered)')
scatter_chart = os.path.join(output_dir, 'ratings_vs_reviews_filtered.png')
plt.savefig(scatter_chart)
plt.show()

print(f"Charts saved as:\n - {best_rated_chart}\n - {worst_rated_chart}\n - {scatter_chart}")

# Generate a visualized table for most-reviewed products
from pandas.plotting import table

plt.figure(figsize=(12, 6))
ax = plt.subplot(111, frame_on=False)  # No axes
ax.xaxis.set_visible(False)  # Hide x axis
ax.yaxis.set_visible(False)  # Hide y axis
tbl = table(
    ax,
    most_reviewed[['Short Name', 'Stars', 'Reviews Count', 'Sale Price USD', 'Marca']].reset_index(drop=True),
    loc='center',
    colWidths=[0.2] * 5
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.2)
for key, cell in tbl.get_celld().items():
    cell.set_text_props(ha='center', va='center')  # Center-align text
visualized_table = os.path.join(output_dir, 'most_reviewed_table.png')
plt.savefig(visualized_table)
plt.show()

print(f"Visualized table saved as: {visualized_table}")
