# 📦 Amazon Price Tracker Telegram Bot

## 📌 Overview
Amazon Price Tracker Telegram Bot is a powerful tool that allows users to track the price of Amazon products via Telegram. Users can send an Amazon product URL to the bot, and it will monitor the price and notify them whenever the price drops.

## 🚀 Features
- 📩 **Track Prices Instantly** – Users can send product URLs to start tracking.
- 📊 **Real-Time Price Updates** – Fetches the latest price from Amazon.
- 🔔 **Automated Alerts** – Sends Telegram notifications when the price drops.
- 📂 **Data Storage** – Uses AWS DynamoDB to store product details and price history.
- 🏗 **Scalable & Efficient** – Built with Python and BeautifulSoup for scraping.

## 🛠 Tech Stack
- **Python** – Backend logic and web scraping.
- **BeautifulSoup** – Scraping product details from Amazon.
- **AWS DynamoDB** – Storing product price history.
- **Telegram Bot API** – Sending notifications to users.

## 📖 How It Works
1. **Send a Product URL** – A user sends an Amazon product link to the Telegram bot.
2. **Scraping & Storage** – The bot fetches the product details and stores them in DynamoDB.
3. **Price Monitoring** – The bot checks the price at intervals.
4. **Price Drop Alerts** – If the price decreases, the bot notifies the user via Telegram.

## 🔧 Setup Instructions
### Prerequisites
- Install **Python 3.x**
- Install required dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Create a **Telegram Bot** via [BotFather](https://t.me/BotFather) and get the API token.
- Set up an **AWS DynamoDB table** to store product data.

### Running the Bot
```sh
python main.py
```

## 🌟 Future Enhancements
- ✅ Support for multiple e-commerce websites.
- ✅ User authentication for tracking multiple products.
- ✅ Web dashboard for product tracking.

## 🤝 Contributing
Pull requests are welcome! If you'd like to improve the bot, feel free to fork the repository and create a PR.

## 📜 License
This project is licensed under the **MIT License**.

