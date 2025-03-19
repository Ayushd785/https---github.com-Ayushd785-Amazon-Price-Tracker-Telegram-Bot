import boto3
import uuid
import json

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
table = dynamodb.Table('UserProducts')

def load_product_info():
    with open("product_info.json","r") as file:
        return json.load(file)

def storedata():
    product_info = load_product_info()

    product_id = product_info.get("ProductID")
    stored_price = product_info.get("price")
    email = product_info.get("email")

    if not email:
        return "Error: Email not found in JSON!"
    
    if not stored_price:
        return "Error: Stored price not found in JSON!"
    email = product_info.get("email")

    if not product_id:
        return "Error: Product ID not found in JSON!"
    
    try:
        table.put_item(Item={
            "chat_id": email,
            "product_id": product_id,
            "stored_price": stored_price,
        })
        return f"Tracking Product: {product_id} ✅\nUser ID: {email}"
    except Exception as e:
        return f"Error: {str(e)}"

print(storedata())

    