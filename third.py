import re

# === CONFIG ===
INPUT_FILE = "/content/output_cleaned.txt"
OUTPUT_FILE = "/content/output_chunks_fixed.txt"
MAX_WORDS = 400

def split_into_sentences(text):
    """
    Split paragraph into sentences while keeping punctuation.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_paragraph(heading, paragraph, max_words=MAX_WORDS):
    """
    Break paragraph into chunks (if > max_words) without splitting sentences.
    """
    sentences = split_into_sentences(paragraph)
    chunks, current_chunk = [], []
    current_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current_count + word_count > max_words and current_chunk:
            chunks.append(f"{heading}\n" + " ".join(current_chunk))
            current_chunk, current_count = [], 0
        current_chunk.append(sentence)
        current_count += word_count

    if current_chunk:
        chunks.append(f"{heading}\n" + " ".join(current_chunk))
    return chunks

def is_heading(line):
    """
    Detect if a line is a heading.
    - All caps or Title Case lines
    - Or start with Lecture / contains 'Operating System' as title
    - Or short (<= 10 words) with no period at end
    """
    line = line.strip()
    if not line:
        return False
    if re.match(r'^(Lecture|[A-Z][A-Za-z\s\-]+)$', line):
        return True
    if len(line.split()) <= 10 and not line.endswith('.'):
        return True
    return False

# === PROCESS FILE ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

chunks = []
current_heading = None
current_paragraph = []

def flush_paragraph():
    global current_paragraph, current_heading
    if current_paragraph:
        paragraph_text = " ".join(current_paragraph).strip()
        if paragraph_text:
            chunks.extend(chunk_paragraph(current_heading or "General", paragraph_text))
        current_paragraph = []

for line in lines:
    if is_heading(line):
        flush_paragraph()
        current_heading = line.strip()
    elif not line.strip():
        # blank line → paragraph break
        flush_paragraph()
    else:
        current_paragraph.append(line.strip())

flush_paragraph()

# Write chunks with numbering
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, 1):
        f.write(f"chunk{i}:\n{chunk}\n\n")

print(f"✅ Improved chunking complete. Saved at: {OUTPUT_FILE}")
print(f"Total chunks created: {len(chunks)}")




