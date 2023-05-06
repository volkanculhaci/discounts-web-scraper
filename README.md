# Discount Web Scraper

This is a Python script that scrapes multiple websites for discount deals and
sends notifications to a Telegram chat using the Telegram bot API. The scraped
data is stored in a MongoDB database.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `pymongo` library
- `python-telegram-bot` library

## Installation

1. Clone the repository:

```shell
git clone https://github.com/volkanculhaci/discount-web-scraper.git
Install the required dependencies using pip:

pip install requests beautifulsoup4 pymongo python-telegram-bot
Usage
Create a JSON file named credentials.json in the project directory with the following structure:

{
  "mongo": {
    "host": "your-mongodb-host",
    "database": "your-mongodb-database",
    "collection": "your-mongodb-collection"
  },
  "telegram": {
    "token": "your-telegram-bot-token",
    "chat_id": "your-telegram-chat-id"
  }
}
Replace the placeholder values in the credentials.json file with your MongoDB and Telegram credentials.

Run the script:
python main.py
The script will continuously scrape the specified websites for discount deals and send notifications to the configured Telegram chat whenever a new deal is found.

Customization
Modify the websites list to include or remove URLs you want to scrape.
Adjust the classes list to match the CSS classes used for titles on the respective websites.
Customize the scraping logic in the while True loop to fit your requirements.
Disclaimer
Please use this script responsibly and comply with the terms of use of the websites you are scraping. Check the website's robots.txt file and respect any rate limits or restrictions.
```
