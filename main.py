import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import json
import subprocess


base_url = "https://www.amazon.in/"

url_inp = input("Enter the URL of the product: ")

# Extract ID (Product ID)

ID_match = re.search(r"/dp/([A-Z0-9]{10})", url_inp)
ID = ID_match.group(1) if ID_match else "ID not found"


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

url = base_url + "dp/" + ID

# Create a session
session = requests.Session()
session.headers.update(headers)

base_response = session.get(base_url,headers=headers)

if base_response.status_code != 200:
    print("Error: Unable to fetch Amazon homepage. Amazon might be blocking requests.")
    exit(1)

product_response = session.get(url,cookies=base_response.cookies)

if product_response.status_code != 200:
    print("Error: Unable to fetch product details.")
    exit(1)

soup = BeautifulSoup(product_response.text, 'html.parser')
print("scraping product data...")
price = soup.select_one("div.a-section.a-spacing-none.aok-align-center.aok-relative span.a-price-whole")
price_value = price.text.strip() if price else None
title = soup.select_one("span#productTitle")


product_info = {
    "ProductID": ID,
    "price": price_value,
    "price": price_value if 'price_value' in locals() else None,
    "url": url,
    "title": title.text.strip() if title else None,
    "timestamp": datetime.now().isoformat()
}
print(product_info)
with open("product_info.json", "w") as file:
    json.dump(product_info, file)

print("Data has been saved to product_info.json")

subprocess.run(["python3", "store-data.py"])  
print("data Saved to DynamoDB...")

subprocess.run(["python3", "user-script.py"])
print("Data saved to UserProducts table")

''' just a test '''