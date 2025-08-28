import os
from telegram.ext import Updater, CommandHandler
from flask import Flask
import threading
import requests

# ============= إعدادات البوت =============
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

CHECK_URL = "https://algeria.blsspainvisa.com/algiers/"
CHECK_INTERVAL = 120  # دقيقتين

# ============= Flask =============
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Bot + Flask Server is running ✅"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ============= أوامر البوت =============
def start(update, context):
    update.message.reply_text("🚀 البوت شغال! يراقب المواعيد كل دقيقتين.")

def ping(update, context):
    update.message.reply_text("✅ السيرفر شغال ويراقب!")

# ============= التحقق من المواعيد =============
def check_appointments(context):
    try:
        resp = requests.get(CHECK_URL, timeout=10)
        text = resp.text.lower()

        # إذا النص ما فيه "no appointment" معناها المواعيد فتحت
        if "no appointment" not in text:
            context.bot.send_message(chat_id=CHAT_ID, text="📢 تم فتح المواعيد! ادخل الموقع الآن ✅")

    except Exception as e:
        print("❌ Error checking site:", e)

# ============= تشغيل البوت =============
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    # جدولة التحقق كل دقيقتين
    job_queue = updater.job_queue
    job_queue.run_repeating(check_appointments, interval=CHECK_INTERVAL, first=10, context=CHAT_ID)

    updater.start_polling()
    updater.idle()

# ============= Main =============
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
