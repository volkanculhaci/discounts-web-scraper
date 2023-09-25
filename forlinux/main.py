import json
import requests
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import telegram
import asyncio
import datetime

# Function to send notification to telegram chat (asynchronous)
async def send_notification(bot, chat_id, title, link):
    await bot.send_message(chat_id=chat_id, text=f'{title}\n{link}\n')
    await asyncio.sleep(3)  # Use asyncio.sleep for asynchronous sleep

async def main():
    # Load credentials from JSON file
    with open("/home/dietpi/myprojects/discounts_webscraper/credentials.json") as f:
        credentials = json.load(f)

    # Extract MySQL and Telegram credentials from the credentials object
    mysql_creds = credentials['mysql']
    telegram_creds = credentials['telegram']

    # Connect to MySQL
    db = mysql.connector.connect(
        host=mysql_creds['host'],
        user=mysql_creds['user'],
        password=mysql_creds['password'],
        database=mysql_creds['database']
    )
    cursor = db.cursor()
    cursor_30min = db.cursor()
    
    # Connect to Telegram bot
    bot = telegram.Bot(token=telegram_creds['token'])
    chat_id = telegram_creds['chat_id']

    # URLs to scrape and corresponding CSS classes for titles
    websites = ['https://forum.donanimarsivi.com/forumlar/Sicakfirsatlar/',
                'https://forum.donanimhaber.com/sicak-firsatlar--f193?sayfa=1',
                'https://www.r10.net/sicak-firsatlar',
                'https://www.technopat.net/sosyal/bolum/indirim-koesesi.257/']
    classes = ["structItem-title", "kl-konu", "title", 'structItem-title']

    # Base URL for each website (used to construct the full topic URL)
    firsat = ['https://forum.donanimarsivi.com', 'https://forum.donanimhaber.com', '', 'https://www.technopat.net']

    # Infinite loop to continuously scrape the websites
    while True:
        for i, url in enumerate(websites):

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            topics = soup.find_all('div', {'class': classes[i]})

            for topic in topics[1:]:
                title_elem = topic.find('a', {'class': ''})
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                if url == 'https://forum.donanimhaber.com/sicak-firsatlar--f193?sayfa=1':
                    try:
                        topic_link = firsat[i] + title_elem.get("href")
                        if any(x in title for x in ["[ANA KONU]", "ANA KONU", "[ANAKONU]", "Sabit Konu: ",
                                                    "Sponsorlu İçerik:", "ad.donanim"]) or "ad.donanim" in topic_link:
                            continue
                    except Exception:
                        continue
                else:
                    topic_link = firsat[i] + title_elem.get("href")

                cursor.execute("SELECT * FROM discounts WHERE topic = %s", (title,))
                existing_topic = cursor.fetchone()

                # # Calculate the timestamp for 30 minutes ago
                # thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)

                # # Execute the SQL query
                # cursor_30min.execute("SELECT * FROM discounts WHERE topic = %s AND creation >= %s", (title, thirty_minutes_ago))
                # last30min_topic = cursor_30min.fetchone()


                if not existing_topic:
                    cursor.execute("INSERT INTO discounts (creation, topic, link) VALUES (%s, %s, %s)",
                                   (current_time, title, topic_link))
                    db.commit()
                    await send_notification(bot, chat_id, title, topic_link)  # Pass bot and chat_id as arguments

        await asyncio.sleep(60)  # Use await for asynchronous sleep

    # Close the database connection when done
    cursor.close()
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
