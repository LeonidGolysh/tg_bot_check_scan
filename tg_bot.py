from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Hello. Send a photo of the receipt")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  photo = update.message.photo[-1]
  file = await photo.get_file()

  os.makedirs("downlands", exist_ok=True)
  file_path = f"downlands/{file.file_id}.jpg"
  await file.download_to_drive(file_path)

  await update.message.reply_text("Scanning...")
  await update.message.reply_text("Scanning completed")

if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

  print("Start...")
  app.run_polling()