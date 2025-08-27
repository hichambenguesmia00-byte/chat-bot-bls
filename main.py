import os
import time
import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# جلب المتغيرات من Environment
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# --- التحقق من مواعيد BLS ---
def check_bls():
    url = "https://algeria.blsspainvisa.com/algiers/french/"  # ضع الرابط الصحيح هنا
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("available_slots"):
            return True
    except Exception as e:
        print("خطأ في جلب المواعيد:", e)
    return False

# --- الرد على رسالة "هل انت تعمل" ---
def handle_message(update, context):
    text = update.message.text
    if "هل انت تعمل" in text:
        update.message.reply_text("Replit يراقب ✅")

# --- تشغيل البوت ---
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# إضافة MessageHandler للرد على الرسائل
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start polling
updater.start_polling()
print("🚀 Bot started on Replit!")

# --- حلقة التحقق من المواعيد ---
while True:
    if check_bls():
        bot.send_message(chat_id=CHAT_ID, text="📢 تم فتح موعد في BLS الآن!")
    time.sleep(60)  # كل دقيقة
