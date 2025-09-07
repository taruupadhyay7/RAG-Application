# === INSTALL REQUIRED LIBS (ONLY ONCE) ===
# pip install sentence-transformers faiss-cpu llama-cpp-python

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# === CONFIG ===
INPUT_FILE = "output_chunks_fixed.txt"
INDEX_FILE = "faiss_index.bin"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLAMA_MODEL_PATH = "models/llama-2-7b-chat.Q3_K_M.gguf"
MAX_CONTEXT_CHARS = 500  # max characters per chunk
TOP_K_CHUNKS = 2  # how many chunks to include in prompt
MAX_TOKENS = 100  # output tokens

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

# === LOAD FAISS INDEX ===
index = faiss.read_index(INDEX_FILE)
print(f"✅ Loaded FAISS index with {index.ntotal} vectors")

# === LOAD EMBEDDING MODEL ===
embed_model = SentenceTransformer(EMBEDDING_MODEL)
print("✅ SentenceTransformer loaded")

# === LOAD LLaMA MODEL ===
llm = Llama(model_path=LLAMA_MODEL_PATH, n_ctx=512)
print("🤖 RAG Chatbot is ready! Type 'exit' to quit.\n")


# === HELPER FUNCTIONS ===
def retrieve_chunks(query, k=TOP_K_CHUNKS):
    """Return top k relevant chunks (truncated to MAX_CONTEXT_CHARS)."""
    query_emb = embed_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k=k)
    relevant_texts = []
    for idx in indices[0]:
        text = chunks[idx]
        if len(text) > MAX_CONTEXT_CHARS:
            text = text[:MAX_CONTEXT_CHARS] + "..."
        relevant_texts.append(text)
    return "\n".join(relevant_texts)


def generate_answer(query):
    """Generate answer using retrieved context and LLaMA."""
    context = retrieve_chunks(query)
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    response = llm(prompt=prompt, max_tokens=MAX_TOKENS)
    # Llama-cpp-python returns a dict with 'choices'
    answer = response['choices'][0]['text'].strip()
    return answer


# === MAIN LOOP ===
while True:
    user_query = input("You: ").strip()
    if user_query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    try:
        answer = generate_answer(user_query)
        print(f"\nBot: {answer}\n")
    except ValueError as e:
        print(f"⚠️ Error: {e}")
        print("Try a shorter question or fewer/more concise context chunks.\n")

