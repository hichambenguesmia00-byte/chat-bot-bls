import os
import time
import threading
import requests
from flask import Flask
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# ========= إعداد المتغيرات =========
TOKEN = os.getenv("BOT_TOKEN")  # ضع التوكن في Render env vars
CHAT_ID = os.getenv("CHAT_ID")  # ضع المعرف الخاص بك في Render env vars
CHECK_URL = "https://algeria.blsspainvisa.com/algiers/"  # رابط الموقع

# بوت تيليجرام
bot = Bot(token=TOKEN)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running on Render!"

# ========= دوال المراقبة =========
def check_appointments():
    """
    يتحقق من توفر المواعيد في الموقع
    """
    try:
        response = requests.get(CHECK_URL, timeout=15)
        html = response.text.lower()

        # منطق بدائي: نفترض لو فيه كلمة "appointment" فهي متاحة
        if "appointment" in html and "no appointment" not in html:
            return True
        else:
            return False
    except Exception as e:
        print("خطأ أثناء التحقق:", e)
        return False

def monitor_loop():
    """
    حلقة تتحقق كل دقيقتين
    """
    while True:
        available = check_appointments()
        if available:
            try:
                bot.send_message(chat_id=CHAT_ID, text="📢 مواعيد متاحة الآن!")
            except Exception as e:
                print("خطأ إرسال:", e)
        time.sleep(120)  # كل دقيقتين

# ========= أوامر البوت =========
def start(update, context):
    update.message.reply_text("👋 أهلا! سأبلغك عند فتح المواعيد.")

def ping(update, context):
    available = check_appointments()
    if available:
        update.message.reply_text("✅ البوت شغال — المواعيد متاحة الآن!")
    else:
        update.message.reply_text("✅ البوت شغال — حاليا لا توجد مواعيد.")

# ========= تشغيل =========
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("هل", ping))
    dp.add_handler(CommandHandler("ping", ping))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # تشغيل المراقبة في Thread منفصل
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()

    # تشغيل البوت في Thread
    t2 = threading.Thread(target=run_bot, daemon=True)
    t2.start()

    # تشغيل Flask (Render يحتاج ويب)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
