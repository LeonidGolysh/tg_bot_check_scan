from telegram import Update
from telegram.ext import ContextTypes

from parser.date_parser import extract_date
from services.sheets_writer import search_sheet_by_date

async def search_by_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if context.user_data.get("awaiting_search_date"):
    raw_input = update.message.text.strip()
    input_date = extract_date(raw_input)
    context.user_data["awaiting_search_date"] = False

    results = search_sheet_by_date(input_date)
    if results:
      message = f"📄 *Results for {input_date}:*\n\n"
      for row in results:
        message += f"🗓 Date: {row['Date']}\n🏪 Shop: {row['Shop']}\n💵 Total: {row['Sum']}\n\n"
    else:
      message = f"❌ No data found for {input_date}."

    await update.message.reply_text(message, parse_mode="Markdown")