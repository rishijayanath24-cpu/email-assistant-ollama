# Intelligent Email Assistant using Ollama

A local AI email assistant that generates **context-aware customer replies by analysing previous email interactions** – no cloud APIs needed.

Course: 24CS2506 – Building Applications using GPT-4 | Experiment 3

## Features
- **Intent detection** – the LLM classifies each email (Order Delay, Refund Request, Damaged Product, Billing Issue, Technical Support, General Inquiry).
- **Similar email retrieval** – Sentence Transformers (`all-MiniLM-L6-v2`) finds the top-3 most similar past conversations in `data/past_emails.csv`.
- **AI reply** – Ollama (`qwen2.5:0.5b`) drafts a professional reply grounded in those past replies and the ongoing conversation.
- **Tone improvement** – rewrite the reply as Formal, Friendly, Empathetic or Concise.
- **Conversation summary** – a short summary of the thread with the customer.
- **Saved replies** – replies are stored locally in `saved_replies/saved_replies.csv`.

## Architecture
```
Customer Name / Subject / Email
   → Input Module → Intent Module (Ollama) → Retrieval Module (Sentence Transformers + past_emails.csv)
   → Reply Module (Ollama) → Tone Module (Ollama) → Summary Module (Ollama) → Save Module (CSV)
```

## Setup
```bash
ollama pull qwen2.5:0.5b
ollama serve                      # keep running
pip install -r requirements.txt
streamlit run app.py
```
The first run downloads the Sentence Transformer model (needs internet once).

## Project structure
```
├── app.py                 # Streamlit UI
├── modules/
│   ├── input_module.py    ├── intent_module.py   ├── retrieval_module.py
│   ├── reply_module.py    ├── tone_module.py     ├── summary_module.py
│   ├── save_module.py     └── llm.py             # Ollama API wrapper
├── data/past_emails.csv   # historical emails + replies
├── saved_replies/         # generated replies (CSV)
├── screenshots/           # output screenshots
└── docs/                  # lab record (PDF)
```

## Tech stack
Python · Ollama (qwen2.5:0.5b) · Sentence Transformers · Pandas · Streamlit
