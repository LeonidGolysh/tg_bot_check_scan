from telegram import Update
from telegram.ext import ContextTypes

async def start_manual_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("🗓 Please enter the date (DD-MM-YYYY):")
  context.user_data["manual_step"] = "date"