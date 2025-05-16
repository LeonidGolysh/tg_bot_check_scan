from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import traceback
import os

from ocr import extract_text_from_image, parse_receipt_text
from sheets_writer import append_to_sheet

user_data_store = {}

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
      f"Sum: {result['total']}\n\n"
      f"Do you want to save it to Google Sheets?"
    )

    user_id = update.message.from_user.id
    user_data_store[user_id] = result

    keyboard = [
      [
        InlineKeyboardButton("✅ Yes", callback_data="save_yes"),
        InlineKeyboardButton("❌ No", callback_data="save_no")
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    print("Recognized text: ", result)
    await update.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")  #parse_mode="MarkdownV2"

  except Exception as e:
    print("Error in OCR: ")
    traceback.print_exc()
    await update.message.reply_text("An error occurred while recognizing the text")

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  user_id = query.from_user.id

  if query.data == "save_yes":
    result = user_data_store.get(user_id)
    if result:
      try:
        append_to_sheet(result["date"], result["shop"], result["total"])
        await query.edit_message_text("✅ Saved to Google Sheets.")
      except Exception as e:
        print("Failed to save: ", e)
        await query.edit_message_text("⚠️ Error saving to Google Sheets.")
    else:
      await query.edit_message_text("⚠️ No data found to save.")
  elif query.data == "save_no":
    await query.edit_message_text("❌ Data not saved.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
  print("Error in Telegram API: ")
  print(f"Update: {update}")
  print(f"Context: {context.error}")