from flask import Flask
import threading
import time
import os
import requests
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters

# --- إعداد Flask ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive ✅"

# --- إعداد Telegram Bot ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

def check_bls():
    # هنا ضع رابط موقع المواعيد الحقيقي
    url = "https://www.bls-example.com/appointments"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("available_slots"):
            return True
    except Exception as e:
        print("خطأ في جلب المواعيد:", e)
    return False

# الرد على رسالة "هل انت تعمل"
def handle_message(update, context):
    if "هل انت تعمل" in update.message.text:
        update.message.reply_text("Replit يراقب ✅")

# --- تشغيل Telegram Bot ---
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
updater.start_polling()
print("🚀 Bot started on Replit!")

# --- حلقة التحقق من المواعيد ---
def monitor_bls():
    while True:
        if check_bls():
            bot.send_message(chat_id=CHAT_ID, text="📢 تم فتح موعد في BLS الآن!")
        time.sleep(60)  # كل دقيقة

# تشغيل المراقبة في Thread منفصل
threading.Thread(target=monitor_bls).start()

# تشغيل Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
