import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import json
import subprocess

# ScraperAPI Key
SCRAPER_API_KEY = "80c3e53a081bfc092642a86bae330f7e" 

# Base Amazon URL
base_url = "https://www.amazon.in/"

# Get user input for Amazon product URL
url_inp = input("Enter the URL of the product: ")
email = input("Enter your email: ")

# Extract Product ID from URL
ID_match = re.search(r"/dp/([A-Z0-9]{10})", url_inp)
if not ID_match:
    print("Error: Product ID not found in the URL.")
    exit(1)

ID = ID_match.group(1)

# ScraperAPI endpoint with Amazon URL
scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.amazon.in/dp/{ID}"

# Fetch product page via ScraperAPI
try:
    response = requests.get(scraper_url)
    response.raise_for_status()  # Raise an error for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Error fetching product page: {e}")
    exit(1)

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Debug: Save the HTML to a file for inspection
with open("product_page.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

# Extract product title
title = soup.select_one("span#productTitle")
title_text = title.text.strip() if title else "Title not found"

# Extract product price
price = soup.select_one("span.a-price-whole")
if price:
    price_value = price.text.strip().replace(',', '')  # Remove commas
else:
    # Alternative price selector
    price = soup.select_one("span.a-offscreen")  
    price_value = price.text.strip().replace('₹', '').replace(',', '') if price else "Price not found"

# Save product info to JSON
product_info = {
    "ProductID": ID,
    "price": price_value,
    "url": url_inp,
    "title": title_text,
    "timestamp": datetime.now().isoformat(),
    "email": email
}

print("Product Info:", product_info)

with open("product_info.json", "w") as file:
    json.dump(product_info, file)

print("Data has been saved to product_info.json")

# Call the next scripts
subprocess.run(["python3", "store-data.py"])
print("Data saved to DynamoDB...")

subprocess.run(["python3", "user-script.py"])
print("Data saved to UserProducts table")
