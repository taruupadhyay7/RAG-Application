import pdfplumber
import re
from pathlib import Path

# === CONFIG ===
INPUT_PDF = "rag pdf book-pages.pdf"  # Put file in same folder as script OR give full path
OUTPUT_TXT = "output_layout_preserved.txt"

def clean_text(text):
    """
    Clean text while preserving layout as much as possible.
    - Removes extra spaces
    - Keeps bullet points, headings, indentation
    """
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# Check file existence
if not Path(INPUT_PDF).exists():
    raise FileNotFoundError(f"❌ Input file not found: {INPUT_PDF}")

# === EXTRACT PDF ===
all_text = []
with pdfplumber.open(INPUT_PDF) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text(layout=True)
        if text:
            cleaned = clean_text(text)
            all_text.append(f"--- Page {i+1} ---\n{cleaned}\n")

with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print(f"✅ Text extracted and saved to {OUTPUT_TXT}")


