import os
import threading
import time
import requests
from flask import Flask
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ---- Telegram Bot Setup ----
TOKEN = os.getenv("BOT_TOKEN")  # ضع التوكن في Secrets
CHAT_ID = os.getenv("CHAT_ID")  # ضع الشات آيدي في Secrets

bot = Bot(TOKEN)

# ---- Flask Web Server ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

# ---- Telegram Commands ----
def start(update: Update, context: CallbackContext):
    update.message.reply_text("اهلا! البوت يراقب المواعيد.")

def ping(update: Update, context: CallbackContext):
    update.message.reply_text("Replit يراقب ✅")

# ---- BLS Checking Logic ----
def check_bls():
    while True:
        try:
            url = "https://algeria.blsspainvisa.com/algiers/"  # ضع هنا الرابط اللي نراقبه
            r = requests.get(url, timeout=10)

            if "No appointment" not in r.text:  
                bot.send_message(chat_id=CHAT_ID, text="🚨 مواعيد متوفرة الآن!")
        except Exception as e:
            print("Error checking site:", e)

        time.sleep(60)  # كل دقيقة

# ---- Run Bot ----
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

# ---- Run Both Flask + Bot + Checker ----
if __name__ == "__main__":
    threading.Thread(target=check_bls).start()
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8080)
