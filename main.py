import os
import time
import requests
from telegram import Bot
from gtts import gTTS

# قراءة المتغيرات من إعدادات Render
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# رابط BLS (غيّره حسب بلدك)
URL = "https://algeria.blsspainvisa.com/book_appointment.php"

def check_appointments():
    try:
        r = requests.get(URL, timeout=10)
        if "No appointments available" in r.text or "لا توجد مواعيد" in r.text:
            return False
        else:
            return True
    except Exception as e:
        print("خطأ:", e)
        return False

def send_voice_alert():
    text = "المواعيد مفتوحة الآن في موقع بي إل إس، أسرع للحجز!"
    tts = gTTS(text=text, lang="ar")
    tts.save("alert.mp3")
    with open("alert.mp3", "rb") as voice:
        bot.send_voice(chat_id=CHAT_ID, voice=voice)
    bot.send_message(chat_id=CHAT_ID, text="📅 المواعيد مفتوحة الآن!")

if __name__ == "__main__":
    while True:
        if check_appointments():
            send_voice_alert()
            time.sleep(600)  # انتظر 10 دقائق قبل التبليغ مرة أخرى
        else:
            print("لا توجد مواعيد...")
        time.sleep(300)  # إعادة المحاولة كل 5 دقائق
