"""Tone Module: rewrites a reply in a chosen tone."""
from modules.llm import ask_ollama

TONES = {
    "Formal": "formal and professional",
    "Friendly": "warm, friendly and conversational",
    "Empathetic": "empathetic and reassuring, acknowledging the customer's frustration",
    "Concise": "short and direct (3 sentences at most)",
}


def improve_tone(reply: str, tone: str, llm=ask_ollama) -> str:
    prompt = (
        f"Rewrite this customer support email reply so it sounds {TONES[tone]}. "
        "Keep every fact exactly the same and do not add new information.\n\n"
        f"Reply:\n{reply}\n\nRewritten reply:"
    )
    return llm(prompt)
