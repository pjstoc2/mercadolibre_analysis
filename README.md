# Mercado Libre Analysis

This project analyzes e-commerce data from **Mercado Libre**, a leading e-commerce platform in Latin America. The analysis explores various aspects of product listings, discounts, ratings, and sellers, providing insights into market trends and seller activity.

## Key Features

### 1. **Data Cleaning and Preparation**
- Filtered and organized data to exclude irrelevant or incomplete entries.
- Converted discount and rating columns into usable formats for analysis.

### 2. **Visualizations**
- **Distribution of Sellers by Product Count**:
  - A bar chart showing how many sellers have a specific number of products listed.
  - Included both a standard y-axis and a logarithmic scale view.
- **Availability Status by Discount Tiers**:
  - A stacked bar chart illustrating product availability status across discount ranges.

### 3. **Insights**
- Explored seller activity distribution, identifying trends such as:
  - The majority of sellers have a small number of product listings.
  - Patterns of product availability across different discount tiers.

### 4. **Market Context**
- Discussed the dominance of Mercado Libre in Latin America's e-commerce market compared to competitors like Amazon.

## File Structure
- **scripts/**: Python scripts used for analysis and visualizations.
- **data/**: Cleaned datasets used in the project.
- **charts/**: Generated charts for key visualizations.
- **README.md**: Overview of the project.

## How to Run
1. Clone this repository:
   git clone https://github.com/your-username/mercado-libre-analysis.git
2. Navigate to the project directory:
   cd mercadolibre_analysis
3. Install required Python packages (if not already installed):
   pip install pandas matplotlib
4. Run the scripts for specific analyses:
   Distribution of Sellers:
   python scripts/seller_distribution.py
   Availability by Discount:
   python scripts/discount_vs_availability.py
## About
  This project highlights the power of e-commerce data analysis and visualization. 
  It was developed to showcase insights into the Mercado Libre platform and provide actionable takeaways for sellers and market analysts.

