from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
  img = Image.open(image_path)
  text = pytesseract.image_to_string(img, lang='pol')
  return text