import boto3
import json

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
table = dynamodb.Table('AmazonProducts')

with open("product_info.json","r") as file:
    product_info = json.load(file)

def storedata():
    if "ProductID" in product_info:
        response = table.put_item(Item=product_info)
        print("Data saved successfully")
    else:
        print("Error: Missing ProductID")

storedata()