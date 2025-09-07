import re
from pathlib import Path

# === CONFIG ===
INPUT_FILE = "output_layout_preserved.txt"  # Put file in same folder as script
OUTPUT_FILE = "output_cleaned.txt"

def clean_text_keep_layout(text):
    """
    Clean text while preserving layout.
    - Remove page numbers & markers
    - Normalize spaces
    - Keep headings, bullets, indentation
    - Remove too many blank lines
    """
    text = re.sub(r'---\s*Page\s*\d+\s*---', '', text)
    text = re.sub(r'\bPage\s+\d+\b', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# === CHECK FILE EXISTENCE ===
if not Path(INPUT_FILE).exists():
    raise FileNotFoundError(f"❌ File not found: {INPUT_FILE}")

# === READ, CLEAN, SAVE ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

cleaned_text = clean_text_keep_layout(raw_text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print(f"✅ Cleaned file saved at: {OUTPUT_FILE}")


