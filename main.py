import os
import time
import requests
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def check_bls():
    # هنا تكتب الكود اللي يتحقق من المواعيد
    return False

print("🚀 Bot started on Railway!")

while True:
    if check_bls():
        bot.send_message(chat_id=CHAT_ID, text="📢 تم فتح المواعيد في BLS!")
    time.sleep(120)  # كل 2 دقائق
