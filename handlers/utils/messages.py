from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def ask_to_save(update_or_query, context, date, shop, total, prefix="Check recognized"):
  context.user_data["final_date"] = date
  context.user_data["final_shop"] = shop
  context.user_data["final_total"] = total

  response = (
    f"*{prefix}*\n\n"
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