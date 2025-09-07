from llama_cpp import Llama

# Model ka path
model_path = r"models/llama-2-7b-chat.Q3_K_M.gguf"

# LLaMA model load karo
llm = Llama(model_path=model_path, n_ctx=512)  # 512 tokens is enough for a simple chat

# Prompt bhejo
prompt = "Hi"

# Model se response lo
response = llm(prompt=prompt, max_tokens=50)  # max 50 tokens ka reply

# Response print karo
print(response['choices'][0]['text'])
