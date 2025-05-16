from telegram import Update
from telegram.ext import ContextTypes

from handlers.callback_handler import ask_to_save
from services.parser.date_parser import extract_date

async def handle_manual_date_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if context.user_data.get("awaiting_manual_date"):
    manual_date = update.message.text.strip()
    context.user_data["awaiting_manual_date"] = False

    shop = context.user_data.get("shop", "Not Found")
    total = context.user_data.get("total", "Not Found")

    await ask_to_save(update, context, extract_date(manual_date), shop, total)