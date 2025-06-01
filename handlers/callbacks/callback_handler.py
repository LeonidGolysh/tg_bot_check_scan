from telegram import Update
from telegram.ext import ContextTypes

from handlers.utils.messages import ask_to_save
from handlers.messages.manual_entry import handle_manual_entry
from handlers.commands.search_command import search_by_date
from services.sheets_writer import append_to_sheet

async def handle_date_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  await query.edit_message_reply_markup(reply_markup=None)

  if query.data == "enter_date":
    context.user_data["awaiting_manual_date"] = True
    await query.message.reply_text("Please enter the date (DD-MM-YYYY):")
  elif query.data == "skip_date":
    await ask_to_save(query, context, "Not Found", context.user_data["shop"], context.user_data["total"])

async def handle_save_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  await query.edit_message_reply_markup(reply_markup=None)

  if query.data == "save_yes":
    date = context.user_data.get("final_date")
    shop = context.user_data.get("final_shop")
    total = context.user_data.get("final_total")

    append_to_sheet(date, shop, total)
    await query.message.reply_text("✅ Saved to Google Sheets.")
  else:
    await query.message.reply_text("❌ Not saved.")

async def handle_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if context.user_data.get("manual_step"):
    await handle_manual_entry(update, context)
  elif context.user_data.get("awaiting_search_date"):
    await search_by_date(update, context)