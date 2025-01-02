import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Function to clean file paths
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return cleaned_path.replace("\\", "/")  # Convert all backslashes to forward slashes

# Prompt for input file path
input_file = input("Enter the path to your CSV file: ").strip()
input_file = clean_file_path(input_file)

# Ensure the input file path is cleaned and exists
if not os.path.isfile(input_file):
    print("File not found. Please check the path and try again.")
    exit()

# Load the dataset
df = pd.read_csv(input_file)

# Clean and convert the Price column to numeric
df['Sale Price USD'] = pd.to_numeric(df['Sale Price USD'].replace('[^\d.]', '', regex=True), errors='coerce')

# Drop rows with NaN values in the Price column
df = df.dropna(subset=['Sale Price USD'])

# Create output directory if it doesn't exist
output_dir = os.path.dirname(input_file)
output_file_hist = os.path.join(output_dir, 'price_distribution_histogram.png')
output_file_box = os.path.join(output_dir, 'price_distribution_boxplot.png')

# Plot histogram for price distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Sale Price USD'], bins=30, kde=True)
plt.title("Sale Price Distribution of *Ofertas* Products")
plt.xlabel("Sale Price")
plt.ylabel("Frequency")
plt.savefig(output_file_hist)
print(f"Histogram saved to {output_file_hist}")
plt.show()

# Plot box plot for price distribution
plt.figure(figsize=(8, 4))
sns.boxplot(x=df['Sale Price USD'])
plt.title("Sale Price Range and Outliers")
plt.xlabel("Sale Price")
plt.savefig(output_file_box)
print(f"Box plot saved to {output_file_box}")
plt.show()
