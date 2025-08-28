import os
from telegram.ext import Updater, CommandHandler
from flask import Flask
import threading

# ============= إعدادات البوت =============
TOKEN = os.getenv("BOT_TOKEN")   # التوكن من Render
CHAT_ID = os.getenv("CHAT_ID")   # خليه نصياً للتجربة

# ============= Flask =============
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Bot + Flask Server is running ✅"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ============= أوامر البوت =============
def start(update, context):
    update.message.reply_text("🚀 البوت شغال 100%!")

def ping(update, context):
    update.message.reply_text("✅ السيرفر حي ومراقب!")

# ============= تشغيل البوت =============
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

# ============= Main =============
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
