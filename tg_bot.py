from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os

from handlers.photo_handler import start, handle_photo, error_handler
from handlers.callback_handler import handle_date_choice, handle_save_choice
from handlers.text_handler import handle_manual_date_entry
from handlers.manual_entry import start_manual_entry, handle_manual_entry

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("manual", start_manual_entry))

  app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
  app.add_handler(CallbackQueryHandler(handle_date_choice, pattern="^(enter_date|skip_date)$"))
  app.add_handler(CallbackQueryHandler(handle_save_choice, pattern="^(save_yes|save_no)$"))
  app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_entry))
  app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_date_entry))
  app.add_error_handler(error_handler)

  print("Start...")
  app.run_polling()