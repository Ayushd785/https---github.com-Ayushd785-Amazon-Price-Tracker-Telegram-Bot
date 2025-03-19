import boto3
import json
import smtplib
from email.mime.text import MIMEText

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
product_table = dynamodb.Table('AmazonProducts')
user_table = dynamodb.Table('UserProducts')

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ayushd785@gmail.com"
EMAIL_PASSWORD = "gsvv igrz iuov kbns"

def send_email(recipent_email,product_id,current_price,stored_price, subject ,body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipent_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipent_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {recipent_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")




def check_price_drop():
    response = user_table.scan()
    users = response.get('Items', [])

    for user in users :
        product_id = user["product_id"]
        stored_price = float(user["stored_price"])
        recipent_email = user["chat_id"]

        # product table se latest price fetch karege
        product = product_table.get_item(Key = {"ProductID": product_id}).get("Item")
        if not product:
            continue
        current_price = float(product["price"])

        # ab hum price compare karege

        if current_price<stored_price:
            subject = "Price Drop Alert"
            body = f"Price of the product has dropped from {stored_price} to {current_price}"
            send_email(recipent_email,product_id,current_price,stored_price,subject,body)
            print("email sent successfuly to ",recipent_email)
        else:
            subject = "no change in price"
            body = f"Price of the product has not changed from {stored_price}"
            send_email(recipent_email,product_id,current_price,stored_price,subject,body)
            print("email sent successfuly to ",recipent_email)


check_price_drop()




