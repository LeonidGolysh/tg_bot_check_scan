from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import traceback
import os

from services.ocr import extract_text_from_image, parse_receipt_text
from handlers.utils.messages import ask_to_save

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  photo = update.message.photo[-1]
  file = await photo.get_file()

  os.makedirs("downlands", exist_ok=True)
  file_path = f"downlands/{file.file_id}.jpg"
  await file.download_to_drive(file_path)

  await update.message.reply_text("Scanning...")
  try:
    text = extract_text_from_image(file_path)
    result = parse_receipt_text(text)

    if result["date"] == "Not Found":
      context.user_data["shop"] = result["shop"]
      context.user_data["total"] = result["total"]

      keyboard = [
        [
          InlineKeyboardButton("📝 Enter date manually", callback_data="enter_date"),
          InlineKeyboardButton("⏭ Skip", callback_data="skip_date")
        ]
      ]

      reply_markup = InlineKeyboardMarkup(keyboard)

      await update.message.reply_text("⚠️ Date not found. Would you like to enter it manually?", reply_markup=reply_markup)
    else:
      await ask_to_save(update, context, result["date"], result["shop"], result["total"])

    print("Recognized text: ", result)

  except Exception as e:
    print("Error in OCR: ")
    traceback.print_exc()
    await update.message.reply_text("An error occurred while recognizing the text")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
  print("Error in Telegram API: ")
  print(f"Update: {update}")
  print(f"Context: {context.error}")