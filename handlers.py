from telegram import Update
from telegram.ext import ContextTypes
import traceback
import os

from ocr import extract_text_from_image, parse_receipt_text
from sheets_writer import append_to_sheet

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Hello. Send a photo of the receipt")

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

    response = (
      f"*Check recognized*\n\n"
      f"Date: {result['date']}\n"
      f"Shop: {result['shop']}\n"
      f"Sum: {result['total']}"
    )
    date = result["date"]
    shop = result['shop']
    total = result['total']

    append_to_sheet(date, shop, total)

    print("Recognized text: ", result)
    await update.message.reply_text(response, parse_mode="Markdown")

  except Exception as e:
    print("Error in OCR: ")
    traceback.print_exc()
    await update.message.reply_text("An error occurred while recognizing the text")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
  print("Error in Telegram API: ")
  print(f"Update: {update}")
  print(f"Context: {context.error}")