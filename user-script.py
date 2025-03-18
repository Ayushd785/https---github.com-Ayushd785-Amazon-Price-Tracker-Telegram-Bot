import boto3
import uuid
import json

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
table = dynamodb.Table('UserProducts')

def load_product_info():
    with open("product_info.json","r") as file:
        return json.load(file)

def storedata():
    chat_id = str(uuid.uuid4())
    product_info = load_product_info()

    product_id = product_info.get("ProductID")
    stored_price = product_info.get("price")

    if not product_id:
        return "Error: Product ID not found in JSON!"
    
    try:
        table.put_item(Item={
            "chat_id": chat_id,
            "product_id": product_id,
            "stored_price": stored_price,
        })
        return f"Tracking Product: {product_id} ✅\nUser ID: {chat_id}"
    except Exception as e:
        return f"Error: {str(e)}"

print(storedata())

    