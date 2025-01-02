import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import json
import os
from requests.exceptions import HTTPError, RequestException

# Base URL for MercadoLibre
base_url = 'https://www.mercadolibre.com.mx/ofertas?page='

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Paths for last page file and CSV file
last_page_file = os.path.join(script_dir, 'last_page.txt')
csv_file = os.path.join(script_dir, 'mercadolibre_products_extended.csv')

# Function to extract product details from a product page
def scrape_product_details(product_url):
    try:
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product title
        title_tag = soup.find('h1', class_='ui-pdp-title')
        title = title_tag.text.strip() if title_tag else 'N/A'

        # Extract price
        price_tag = soup.find('span', class_='andes-money-amount__fraction')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Extract rating (stars)
        rating_tag = soup.find('span', class_='ui-pdp-review__rating')
        rating = rating_tag.text.strip() if rating_tag else 'N/A'

        if rating_tag:
            rating = rating_tag.text.strip()
        else:
            print(f"Star rating not available for: {product_url}")

        # Extract availability status
        status_tag = soup.find('span', class_='ui-pdp-buybox__quantity__available')
        status = status_tag.text.strip() if status_tag else 'Available'

        # Extract seller name using two strategies
        seller = 'N/A'
        # Primary strategy: Extract from 'ui-pdp-seller__label-text-with-icon'
        seller_tag = soup.find('span', class_='ui-pdp-seller__label-text-with-icon')
        if seller_tag:
            seller = seller_tag.get_text(strip=True)
        else:
            # Secondary strategy: Extract from 'ui-pdp-seller__label-sold' and its sibling
            vendido_por_span = soup.find('span', class_='ui-pdp-seller__label-sold')
            if vendido_por_span:
                seller_span = vendido_por_span.find_next_sibling('span', class_='')
                if seller_span:
                    seller = seller_span.get_text(strip=True)

        # Extract brand (Marca) using multiple strategies
        brand = 'N/A'
        brand_extraction_method = 'None'

        # Strategy 1: Remove prefixes from 'ui-pdp-brand__link' or 'ui-pdp-color--BLUE' elements
        brand_tag = soup.find('a', class_='ui-pdp-brand__link') or soup.find('p', class_='ui-pdp-color--BLUE')
        if brand_tag:
            brand_text = brand_tag.get_text(strip=True)
            brand = re.sub(r'^(Visita la Tienda oficial de\s+|Ver más productos marca\s+)', '', brand_text, flags=re.I)
            brand_extraction_method = 'Strategy 1: Brand link or title'

        # Strategy 2: Extract brand from JSON-LD scripts
        if brand == 'N/A':
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if 'brand' in data:
                        if isinstance(data['brand'], dict):
                            brand = data['brand'].get('name', 'N/A')
                        else:
                            brand = data['brand']
                        brand = brand.strip()
                        brand_extraction_method = 'Strategy 2: JSON-LD script'
                        break
                except (json.JSONDecodeError, TypeError):
                    continue

        # Strategy 3: Extract brand from 'brandId' pattern in page source
        if brand == 'N/A':
            match = re.search(r'"brandId":"([^"]+)"', response.text)
            if match:
                brand = match.group(1).strip()
                brand_extraction_method = 'Strategy 3: brandId pattern'

        # Strategy 4: Extract brand from attributes in JSON-like structures
        if brand == 'N/A':
            match = re.search(r'"attributes":\[\{"id":"Marca","name":"Marca","value_name":"([^"]+)"', response.text)
            if match:
                brand = match.group(1).strip()
                brand_extraction_method = 'Strategy 4: JSON attributes'

        # Exclude incorrect values
        if brand.lower() in ['iva incluido'] or brand.lower().startswith('en '):
            brand_extraction_method += ' (Filtered Out)'
            brand = 'N/A'

        # Extract description
        description_tag = soup.find('p', class_='ui-pdp-description__content')
        description = description_tag.text.strip() if description_tag else 'N/A'

        # Extract shipping info
        shipping = 'Paid Shipping'
        shipping_tag = soup.find('span', class_='ui-pdp-color--GREEN ui-pdp-family--SEMIBOLD')
        if shipping_tag and 'Envío gratis' in shipping_tag.text:
            shipping = 'Free Shipping'

        # Extract discount information
        discount = 'No Discount'
        discount_tag = soup.find('span', class_='ui-pdp-price__second-line__label')
        if discount_tag:
            discount = discount_tag.text.strip()

        # Extract reviews count
        reviews_count = 'No Reviews'
        reviews_tag = soup.find('span', class_='ui-pdp-review__amount')
        if reviews_tag:
            reviews_count = reviews_tag.text.strip()

        # Extract category
        category = 'N/A'
        category_tag = soup.find('a', class_='andes-breadcrumb__link')
        if category_tag:
            category = category_tag.text.strip()

        return {
            'Product': title,
            'Product URL': product_url,
            'Price': price,
            'Stars': rating,
            'Status': status,
            'Seller': seller,
            'Marca': brand,
            'Brand Extraction Method': brand_extraction_method,
            'Description': description,
            'Shipping': shipping,
            'Discount': discount,
            'Reviews Count': reviews_count,
            'Category': category
        }

    except HTTPError as e:
        print(f"HTTP error occurred while scraping product: {product_url} - {e}")
        return None
    except RequestException as e:
        print(f"Request failed while scraping product: {product_url} - {e}")
        return None

# Function to extract product links from a search results page
def scrape_search_results(page_number):
    url = base_url + str(page_number)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        product_links = []
        for link in soup.find_all('a', class_='poly-component__title'):
            product_url = link['href']
            # Skip click-tracking URLs
            if 'click1.mercadolibre.com.mx' in product_url:
                print(f"Skipping click-tracking URL: {product_url}")
                continue

            product_links.append(product_url)

        if not product_links:
            print(f"No product links found on page {page_number}")

        return product_links

    except HTTPError as e:
        print(f"HTTP error occurred while scraping page {page_number}: {e}")
        return []
    except RequestException as e:
        print(f"Request failed while scraping page {page_number}: {e}")
        return []

# Save progress to last_page.txt
def save_last_page(page_number):
    with open(last_page_file, 'w') as f:
        f.write(str(page_number))

# Get the last page scraped from last_page.txt
def get_last_page():
    if os.path.exists(last_page_file):
        with open(last_page_file, 'r') as f:
            return int(f.read().strip())
    return 1  # Start from the first page if no last_page.txt exists

# Main function to orchestrate the scraping
def main():
    all_product_details = []
    
    # Get the last page scraped
    start_page = get_last_page()

    max_pages = 10000  # Adjust the number of pages for the full run

    # If CSV exists, append data; if not, create a new file
    file_exists = os.path.isfile(csv_file)

    for page in range(start_page, max_pages + 1):
        print(f"Scraping page {page}...")

        # Get all product links on the current page
        product_links = scrape_search_results(page)

        # If no links found, break the loop as the page might not exist or IP is blocked
        if not product_links:
            print(f"No product links found on page {page}. Ending scrape.")
            break

        # Visit each product page and scrape details
        for product_url in product_links:
            print(f"Scraping product: {product_url}")
            details = scrape_product_details(product_url)
            if details:
                all_product_details.append(details)

            # Delay to avoid overloading the server
            time.sleep(15)  # Significantly increased delay

        # Write data to the CSV file after each page
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Product', 'Product URL', 'Price', 'Stars', 'Status', 'Seller', 'Marca', 
                          'Brand Extraction Method', 'Description', 'Shipping', 'Discount', 'Reviews Count', 'Category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # Write header only once
                file_exists = True  # Set flag so that header isn't written again
            writer.writerows(all_product_details)

        # Save progress to last_page.txt
        save_last_page(page)

        # Clear the product details list to free up memory
        all_product_details.clear()

        # Additional delay between pages
        time.sleep(60)

    print("Scraping complete.")

if __name__ == '__main__':
    main()
