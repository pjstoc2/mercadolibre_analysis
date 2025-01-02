import pandas as pd
import matplotlib.pyplot as plt
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_chart = os.path.join(output_dir, 'availability_by_shipping_option.png')

# Load the dataset
df = pd.read_csv(file_path)

# Ensure 'Status' and 'Shipping' columns are appropriately filtered for analysis
df_filtered = df[df['Status'].isin(['Available', 'Out of Stock', 'Limited Availability'])]

# Create a pivot table to summarize counts for each shipping type and availability status
availability_shipping = df_filtered.pivot_table(index='Status', columns='Shipping', aggfunc='size', fill_value=0)

# Plot the data
availability_shipping.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.xlabel("Availability Status")
plt.ylabel("Product Count")
plt.title("Availability by Shipping Option (Free vs. Paid)")
plt.legend(title="Shipping Type", loc='upper right')
plt.grid(axis='y')
plt.savefig(output_chart)
plt.show()

print(f"Plot saved to {output_chart}")
