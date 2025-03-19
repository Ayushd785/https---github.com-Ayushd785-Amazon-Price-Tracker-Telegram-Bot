import boto3
import requests
from bs4 import BeautifulSoup
import time

SCRAPER_API_KEY = "80c3e53a081bfc092642a86bae330f7e"

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
product_table = dynamodb.Table("AmazonProducts")

def fetch_price(product_id):
    """Fetches product price from Amazon using ScraperAPI."""
    scrapper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.amazon.in/dp/{product_id}"
    
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(scrapper_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            price = soup.select_one("span.a-price-whole")
            return price.text.strip().replace(",", "") if price else None
        except requests.exceptions.RequestException as e:
            print(f"Retry {attempt + 1}: Error fetching {product_id}: {e}")
            time.sleep(2)  # Wait before retrying
    
    return None  # Return None if all retries fail

def update_prices():
    """Fetches all products and updates their prices in DynamoDB."""
    response = product_table.scan()
    products = response.get("Items", [])
    
    for product in products:
        product_id = product["ProductID"]
        price_value = fetch_price(product_id)

        if price_value:
            product_table.update_item(
                Key={"ProductID": product_id},
                UpdateExpression="SET price = :p",
                ExpressionAttributeValues={":p": str(price_value)},
            )
            print(f"✅ Price updated for {product_id}: {price_value}")
        else:
            print(f"❌ Price not found for {product_id}")

    print("✅ All product prices updated!")

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    update_prices()
    return {"statusCode": 200, "body": "Product prices updated successfully!"}
