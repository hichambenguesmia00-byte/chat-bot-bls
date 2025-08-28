from flask import Flask
from telegram.ext import Updater, CommandHandler
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running on Render!"

def start(update, context):
    update.message.reply_text("البوت شغال ✅")

if __name__ == "__main__":
    # Telegram bot setup
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Start bot polling in background
    updater.start_polling()

    # Run Flask web server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
