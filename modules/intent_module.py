"""Intent Module: classifies the customer's email using the LLM."""
from modules.llm import ask_ollama

INTENTS = [
    "Order Delay", "Refund Request", "Damaged Product",
    "Billing Issue", "Technical Support", "General Inquiry",
]

_KEYWORDS = {
    "Order Delay": ["delay", "late", "not delivered", "not arrived", "where is my order", "shipment"],
    "Refund Request": ["refund", "money back", "return"],
    "Damaged Product": ["damaged", "broken", "cracked", "defective"],
    "Billing Issue": ["charged", "invoice", "billing", "payment", "double"],
    "Technical Support": ["error", "login", "password", "app", "crash", "not working"],
}


def _keyword_intent(text: str) -> str:
    text = text.lower()
    for intent, words in _KEYWORDS.items():
        if any(w in text for w in words):
            return intent
    return "General Inquiry"


def detect_intent(subject: str, email: str, llm=ask_ollama) -> str:
    prompt = (
        "Classify the customer email into exactly one of these categories:\n"
        + "\n".join(f"- {i}" for i in INTENTS)
        + f"\n\nSubject: {subject}\nEmail: {email}\n\n"
        "Answer with only the category name."
    )
    answer = llm(prompt, temperature=0.0).lower()
    for intent in INTENTS:
        if intent.lower() in answer:
            return intent
    # small models sometimes ignore the format; fall back to keyword rules
    return _keyword_intent(f"{subject} {email}")
