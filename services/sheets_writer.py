from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import gspread

load_dotenv()

def get_google_sheet():
  scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
  creds_path = os.getenv("GOOGLE_CREDS_JSON", "keys/tg-bot-check-scan-87d8fc21bf74.json")
  creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
  client = gspread.authorize(creds)
  return client.open(os.getenv("SPREADSHEET_NAME")).sheet1

def append_to_sheet(date: str, shop: str, total: str):
  sheet = get_google_sheet()
  sheet.append_row([date, shop, total])

def search_sheet_by_date(date: str) -> list:
  sheet = get_google_sheet()
  records = sheet.get_all_records()

  return [row for row in records if row["Date"] == date]