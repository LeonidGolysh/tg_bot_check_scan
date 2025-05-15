import re

def extract_total(text_lines: list[str], total_keywords: list[str]) -> str:
  for line in reversed(text_lines):
    if any(keyword in line.lower() for keyword in total_keywords):
      match = re.search(r'([\d]+[.,]\d{2})', line)
      if match:
        return match.group(1)

  return "Not Found"