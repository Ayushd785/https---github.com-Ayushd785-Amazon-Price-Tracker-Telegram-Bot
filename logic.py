import boto3
import requests
import json


dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

amazon_products_table = dynamodb.Table('AmazonProducts')
user_products_table = dynamodb.Table('UserProducts')
bot_token = '7909609931:AAG42ERGau0907bqjEfnvq27Ym7vIvqWZis'
telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

def sendmessage(chat_id,message):
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(telegram_api_url, json=payload)

def check_price_and_notify():
    response = user_products_table.scan()
    for item in response.get('Items',[]):
        chat_id = item['chat_id']
        product_id = item['product_id']
        stored_price = item['stored_price']

        product_data = amazon_products_table.get_item(Key={'ProductID': product_id})
        if 'Item' not in product_data:
            continue  # Skip if product not found

        current_price = float(product_data['Item']['price'].replace(',', ''))
        if current_price < stored_price:
            message = f'Price Drop Alert! \n{product_data["Item"]["title"]} is now ₹{current_price} (was ₹{stored_price}).\nCheck here: {product_data["Item"]["url"]}'
            sendmessage(chat_id, message)
            
            user_products_table.update_item(
                Key={'chat_id': chat_id, 'product_id': product_id},
                UpdateExpression='SET stored_price = :new_price',
                ExpressionAttributeValues={':new_price': str(current_price)}
            )

check_price_and_notify()
print("Price check completed")