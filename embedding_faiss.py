# === INSTALL REQUIRED LIBS (ONLY ONCE) ===
# pip install sentence-transformers faiss-cpu

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === CONFIG ===
INPUT_FILE = "output_chunks_fixed.txt"  # path to your cleaned & chunked file
INDEX_FILE = "faiss_index.bin"          # where to save FAISS index
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # small, fast model good for local RAG

# === LOAD CHUNKS ===
chunks = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    current_chunk = []
    for line in f:
        if line.startswith("chunk"):
            if current_chunk:
                chunks.append("".join(current_chunk).strip())
                current_chunk = []
        current_chunk.append(line)
    if current_chunk:
        chunks.append("".join(current_chunk).strip())

print(f"✅ Loaded {len(chunks)} chunks")

# === EMBEDDINGS ===
print("🔄 Generating embeddings...")
model = SentenceTransformer(EMBEDDING_MODEL)
embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

# === CREATE FAISS INDEX ===
dimension = embeddings.shape[1]  # embedding vector size
index = faiss.IndexFlatL2(dimension)  # L2 similarity index
index.add(embeddings)
print(f"✅ FAISS index built with {index.ntotal} vectors")

# === SAVE INDEX FOR LATER USE ===
faiss.write_index(index, INDEX_FILE)
print(f"💾 FAISS index saved to {INDEX_FILE}")

# === SIMPLE TEST: SEARCH ===
query = "What is an operating system?"
query_emb = model.encode([query], convert_to_numpy=True)
distances, indices = index.search(query_emb, k=3)

print("\n🔍 Top 3 Relevant Chunks:")
for i, idx in enumerate(indices[0]):
    print(f"\nRank {i+1} (distance={distances[0][i]:.4f}):")
    print(chunks[idx][:300] + "...")
