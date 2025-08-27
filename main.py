import os
import time
import requests
from gtts import gTTS
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# رابط موقع BLS (بدلو بالرابط الصحيح لصفحة الحجز)
BLS_URL = "https://algeria.blsspainvisa.com/algiers/french/"

def check_bls():
    """
    وظيفة بسيطة تتأكد إذا المواعيد مفتوحة أو لا.
    لازم تعدلها حسب نص الموقع الحقيقي.
    """
    try:
        response = requests.get(BLS_URL, timeout=10)
        if "No appointments available" in response.text:
            return False
        else:
            return True
    except Exception as e:
        print("Error checking BLS:", e)
        return False

def notify(bot):
    """يبعث إشعار نصي وصوتي"""
    message = "📢 المواعيد مفتوحة الآن في موقع BLS!"
    bot.send_message(chat_id=CHAT_ID, text=message)

    # إنشاء ملف صوتي
    tts = gTTS(message, lang="ar")
    tts.save("alert.mp3")

    # إرسال الصوت
    with open("alert.mp3", "rb") as audio:
        bot.send_audio(chat_id=CHAT_ID, audio=audio)

def start(update, context):
    update.message.reply_text("✅ البوت شغال ويفحص المواعيد كل دقيقتين...")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    bot = updater.bot

    # رسالة عند بداية التشغيل
    bot.send_message(chat_id=CHAT_ID, text="🚀 Bot started successfully on Render!\n⏳ سأفحص المواعيد كل دقيقتين.")

    # حلقة الفحص كل دقيقتين
    while True:
        if check_bls():
            notify(bot)
        time.sleep(120)  # كل 2 دقيقة
