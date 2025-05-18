from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  help_text = (
    "*Available Commands:*\n\n"
    "/start - Restart the bot and upload a receipt photo\n"
    "/manual - Manually enter receipt data\n"
    "/help - Show this help message\n"
  )
  await update.message.reply_text(help_text, parse_mode="Markdown")