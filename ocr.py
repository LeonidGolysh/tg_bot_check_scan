from PIL import Image
import pytesseract
import json

from parser.date_parser import extract_date
from parser.shop_parser import extract_shop
from parser.total_parser import extract_total

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def load_keywords():
  with open("data/keywords.json", "r", encoding="utf-8") as f:
    return json.load(f)

keywords = load_keywords()

def extract_text_from_image(image_path):
  img = Image.open(image_path)
  text = pytesseract.image_to_string(img, lang='pol')
  return text

def parse_receipt_text(text: str) -> dict:
  lines = [line.strip() for line in text.splitlines() if line.strip()]

  return {
    'date': extract_date(text),
    'shop': extract_shop(lines, keywords["shops"]),
    'total': extract_total(lines, keywords['total_keywords'])
  }