from telegram import Update
from telegram.ext import ContextTypes

async def search_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
  context.user_data['awaiting_search_date'] = True
  await update.message.reply_text("🔍 Please enter the date to search (e.g., 01-06-2025):")