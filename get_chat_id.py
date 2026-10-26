# get_chat_id.py - prints your Telegram chat ID. Does not print the token.
import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    print("TELEGRAM_BOT_TOKEN not found in .env")
else:
    r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=15)
    print("Status:", r.status_code)
    data = r.json()
    results = data.get("result", [])
    if not results:
        print("No messages found. Send 'hello' to your bot in Telegram, then run this again.")
    for item in results:
        msg = item.get("message", {})
        chat = msg.get("chat", {})
        print("Chat ID:", chat.get("id"), "| Name:", chat.get("first_name"))