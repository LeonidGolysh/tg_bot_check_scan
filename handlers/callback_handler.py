from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.sheets_writer import append_to_sheet

async def handle_date_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  if query.date == "enter_date":
    context.user_data["awaiting_manual_date"] = True
    await query.message.reply_text("Please enter the date (DD-MM-YYYY):")
  elif query.data == "skip_date":
    await ask_to_save(query, context, "Not Found", context.user_data["shop"], context.user_data["total"])

async def handle_save_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  if query.data == "save_yes":
    date = context.user_data.get("final_date")
    shop = context.user_data.get("final_shop")
    total = context.user_data.get("final_total")

    append_to_sheet(date, shop, total)
    await query.message.reply_text("✅ Saved to Google Sheets.")
  else:
    await query.message.reply_text("❌ Not saved.")

async def ask_to_save(update_or_query, context, date, shop, total):
  context.user_data["final_date"] = date
  context.user_data["final_shop"] = shop
  context.user_data["final_total"] = total

  response = (
    f"*Check recognized*\n\n"
    f"Date: {date}\n"
    f"Shop: {shop}\n"
    f"Sum: {total}\n\n"
    f"Do you want ot save it to Google Sheets?"
  )

  keyboard = [
    [
      InlineKeyboardButton("✅ Yes", callback_data="save_yes"),
      InlineKeyboardButton("❌ No", callback_data="save_no")
    ]
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)
  await update_or_query.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")