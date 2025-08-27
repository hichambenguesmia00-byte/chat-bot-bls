import os
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def start(update, context):
    update.message.reply_text("✅ Bot is running on Render!")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # أرسل رسالة مباشرة لك عند الإقلاع (للتأكد)
    if CHAT_ID:
        updater.bot.send_message(chat_id=CHAT_ID, text="🚀 Bot started successfully on Render!")

    updater.start_polling()
    updater.idle()
