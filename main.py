import os
from telegram import Bot
import threading
import time
import requests
from flask import Flask
from telegram.ext import Updater, CommandHandler

# ============= إعدادات البوت =============
TOKEN = "ضع_توكن_البوت_هنا"
CHAT_ID = 123456789   # ضع هنا Chat ID الخاص بك

CHECK_URL = "https://algeria.blsspainvisa.com/algiers/"  # رابط الصفحة اللي تراقبها
CHECK_INTERVAL = 120  # مدة التحقق بالثواني (120 = دقيقتين)

# ============= Flask للإبقاء على السيرفر شغال =============
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Bot + Flask Server is running ✅"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ============= وظائف البوت =============
def start(update, context):
    update.message.reply_text("🚀 البوت شغال! استخدمني لمراقبة المواعيد.")

def ping(update, context):
    update.message.reply_text("Replit/Render يراقب ✅")

# دالة التحقق من المواعيد
def check_appointments(context):
    try:
        resp = requests.get(CHECK_URL, timeout=10)
        text = resp.text

        if "no appointments" not in text.lower():  
            context.bot.send_message(chat_id=CHAT_ID, text="📢 تم فتح المواعيد! ادخل الموقع الآن ✅")
        # إذا ما في مواعيد → ما يرسل شيء
    except Exception as e:
        print("❌ Error checking site:", e)

# ============= تشغيل البوت =============
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    # جدولة التحقق كل CHECK_INTERVAL ثانية
    job_queue = updater.job_queue
    job_queue.run_repeating(check_appointments, interval=CHECK_INTERVAL, first=10)

    updater.start_polling()
    updater.idle()

# ============= Main =============
if __name__ == "__main__":
    # Flask في thread فرعي
    threading.Thread(target=run_flask).start()

    # بوت التلغرام في Main thread
    run_bot()
