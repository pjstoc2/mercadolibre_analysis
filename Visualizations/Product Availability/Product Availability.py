import pandas as pd
import matplotlib.pyplot as plt
import os

# Prompt for file path and clean it
file_path = input("Enter the file path of the dataset: ").strip('"').replace("\\", "/")
output_dir = os.path.dirname(file_path)
output_file = os.path.join(output_dir, 'product_availability_summary.csv')
chart_file = os.path.join(output_dir, 'product_availability_chart.png')

# Load the dataset
df = pd.read_csv(file_path)

# Group by 'Status' to analyze availability
availability_summary = df['Status'].value_counts().reset_index()
availability_summary.columns = ['Availability Status', 'Count']

# Calculate percentages for each availability category
total_products = availability_summary['Count'].sum()
availability_summary['Percentage'] = (availability_summary['Count'] / total_products) * 100

# Save the summary to CSV for record-keeping
availability_summary.to_csv(output_file, index=False)
print(f"Availability summary saved to {output_file}")

# Plotting availability distribution
plt.figure(figsize=(10, 6))
plt.bar(availability_summary['Availability Status'], availability_summary['Count'], color=['green', 'orange', 'red'])
plt.xlabel("Availability Status")
plt.ylabel("Count of Products")
plt.title("Product Availability Distribution")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart
plt.savefig(chart_file)
print(f"Chart saved to {chart_file}")

# Display the chart
plt.show()
