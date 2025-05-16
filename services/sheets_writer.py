from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import gspread

load_dotenv()

def append_to_sheet(date: str, shop: str, total: str):
  scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
  creds_path = os.getenv("GOOGLE_CREDS_JSON", "keys/tg-bot-check-scan-87d8fc21bf74.json")
  creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
  client = gspread.authorize(creds)

  sheet = client.open(os.getenv("SPREADSHEET_NAME")).sheet1

  sheet.append_row([date, shop, total])