from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os

from handlers.photo_handler import start, handle_photo, handle_confirmation, error_handler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
  app.add_handler(CallbackQueryHandler(handle_confirmation))
  app.add_error_handler(error_handler)

  print("Start...")
  app.run_polling()