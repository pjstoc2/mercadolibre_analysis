import pandas as pd
import matplotlib.pyplot as plt
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_chart_availability = os.path.join(output_dir, 'discount_vs_availability.png')

# Load the dataset
df = pd.read_csv(file_path)

# Filter out rows with "No Discount" and extract discount percentages as integers
df = df[df['Discount'] != 'No Discount']
df['Discount Percentage'] = df['Discount'].str.extract('(\d+)%').astype(float)

# Group by discount tiers for availability status
discount_tiers = pd.cut(df['Discount Percentage'], bins=[0, 10, 30, 50, 70, 100], labels=['0-10%', '11-30%', '31-50%', '51-70%', '71-100%'])
availability_by_discount = df.groupby(discount_tiers)['Status'].value_counts(normalize=True).unstack().fillna(0)

# Define a custom color palette with 9 colors
colors = [
    '#FF9999', '#66B2FF', '#99FF99', '#FFCC99', 
    '#FF6666', '#66FFB2', '#B266FF', '#FFB266', 
    '#9999FF'
]

# Plot availability by discount tiers with custom colors
availability_by_discount.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors[:len(availability_by_discount.columns)])
plt.xlabel('Discount Tiers')
plt.ylabel('Proportion of Availability')
plt.title('Availability Status by Discount Tiers')
plt.xticks(rotation=45)
plt.legend(title='Availability Status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(output_chart_availability)
plt.show()

print(f"Availability chart saved to {output_chart_availability}")
