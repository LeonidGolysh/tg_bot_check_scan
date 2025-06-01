import os
import tempfile
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from services.sheets_writer import get_google_sheet

async def export_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
  sheet = get_google_sheet()
  data = sheet.get_all_values()

  if not data:
    await update.message.reply_text("❌ Sheet is empty.")
    return
  
  df = pd.DataFrame(data[1:], columns=data[0])

  with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
    df.to_excel(tmp.name, index=False, engine='openpyxl')
    tmp_path = tmp.name
  
  with open(tmp_path, "rb") as f:
    await update.message.reply_document(f, filename="exported_sheet.xlsx")

  os.remove(tmp_path)