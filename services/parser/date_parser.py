from datetime import datetime
import re

def normalize_date(date_str: str) -> str:
  original = date_str.strip()
  possible_formats = [
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%d.%m.%y",
    "%Y.%m.%d",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%d-%m-%y"
  ]

  fixed = fix_ocr_date_misread(original)

  for fmt in possible_formats:
    try:
      dt = datetime.strptime(fixed, fmt)
      return dt.strftime("%d.%m.%Y")
    except ValueError:
      continue
  
  return f"(Could not parse: {original})"

def fix_ocr_date_misread(date_str: str) -> str:
  """
  Corrects OCR error: '2025-85-12' -> '2025-05-12'
  Only if year is at the beginning.
  """

  match = re.match(r'^(\d{2,4})[./-](\d{2})[./-](\d{2})$', date_str)

  if not match:
    return date_str
  
  year, month, day = match.groups()

  if month.startswith('8') and int(month) > 12:
    month = '0' + month[1]

  if day.startswith('8') and int(day) > 31:
    day = '0' + day[1]
  
  return f"{year}-{month}-{day}"

def extract_date(text: str) -> str:
  date_pattern = r'(\d{2,4}[./-]\d{2}[./-]\d{2,4})'
  match = re.search(date_pattern, text)
  if match:
    return normalize_date(match.group(1))
  
  return "Not Found"