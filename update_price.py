import boto3
import requests
from bs4 import BeautifulSoup

SCRAPER_API_KEY = "80c3e53a081bfc092642a86bae330f7e"

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
product_table = dynamodb.Table('AmazonProducts')

# products nikal lo product table se 

response = product_table.scan()
products = response.get('Items', [])
for product in products:
    product_id = product["ProductID"]
    scrapper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.amazon.in/dp/{product_id}"
    
    try:
        response = requests.get(scrapper_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        price = soup.select_one("span.a-price-whole")
        price_value = price.text.strip().replace(',', '') if price else None

        if price_value:
            product_table.update_item(
                Key={"ProductID": product_id},
                UpdateExpression="SET price = :p",
                ExpressionAttributeValues={":p": str(price_value)}
            )
            print(f"Price updated for {product_id}: {price_value}")
        else:
            print(f"Price not found for {product_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product page: {e}")

print("✅ All product prices updated!")