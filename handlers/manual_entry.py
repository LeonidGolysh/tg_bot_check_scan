from telegram import Update
from telegram.ext import ContextTypes

from handlers.utils.messages import ask_to_save
from services.parser.date_parser import extract_date

async def start_manual_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("🗓 Please enter the date (DD-MM-YYYY):")
  context.user_data["manual_step"] = "date"

async def handle_manual_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text.strip()

  if context.user_data.get("awaiting_manual_date"):
    context.user_data["awaiting_manual_date"] = False

    shop = context.user_data.get("shop", "Not Found")
    total = context.user_data.get("total", "Not Found")

    await ask_to_save(update, context, extract_date(text), shop, total)
    return

  step = context.user_data.get("manual_step")

  if step == "date":
    date = extract_date(update.message.text)
    context.user_data["manual_date"] = date
    context.user_data["manual_step"] = "shop"
    await update.message.reply_text("🏪 Now enter the shop name:")
  
  elif step == "shop":
    context.user_data["manual_shop"] = update.message.text
    context.user_data["manual_step"] = "total"
    await update.message.reply_text("💵 Finally, enter the total amount (e.g., 45.90):")

  elif step == "total":
    context.user_data["manual_total"] = update.message.text
    context.user_data["manual_step"] = None

    date = context.user_data["manual_date"]
    shop = context.user_data["manual_shop"]
    total = context.user_data["manual_total"]

    await ask_to_save(update, context, date, shop, total, prefix="Manual Entry Summary")