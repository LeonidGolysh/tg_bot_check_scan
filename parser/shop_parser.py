def extract_shop(text_lines: list[str], shop_keywords: list[str]) -> str:
  for line in text_lines:
    words = line.lower().split()
    if not words:
      continue

    first_word = words[0]

    for keyword in shop_keywords:
      if keyword in first_word:
        return keyword.upper()

  return "Not Found"