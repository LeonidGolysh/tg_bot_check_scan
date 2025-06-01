from telegram import BotCommand

async def set_bot_commands(app):
  commands = [
    BotCommand("start", "Start the bot"),
    BotCommand("manual", "Enter receipt data manually"),
    BotCommand("search", "Search by date"),
    BotCommand("export", "Export file"),
    BotCommand("help", "Show help info")
  ]
  await app.bot.set_my_commands(commands)