🚀 Built an Intelligent Email Assistant that runs 100% locally with Ollama!

Customer support replies shouldn't start from a blank page. My assistant learns from past conversations:

🔍 Detects the intent of each customer email (delay, refund, damaged item, billing...)
📚 Retrieves the 3 most similar past emails with Sentence Transformers
🤖 Drafts a professional reply grounded in those past replies (qwen2.5:0.5b via Ollama)
🎭 Rewrites the reply in a formal, friendly, empathetic or concise tone
📝 Summarizes the conversation with the customer
💾 Saves every reply locally, with no cloud APIs and no API keys

The big lesson: a tiny 0.5B model writes well but can invent policy details. Showing it real past replies as examples (retrieval) keeps its answers grounded, so facts come from your history and the LLM handles the language.

📂 Code: https://github.com/rishijayanath24-cpu/email-assistant-ollama

#Ollama #LLM #GenerativeAI #Python #NLP #SentenceTransformers #Streamlit #LocalAI #BuildInPublic
