"""Summary Module: summarises the conversation with a customer."""
from modules.llm import ask_ollama


def summarize_conversation(history, llm=ask_ollama) -> str:
    if not history:
        return "No conversation to summarise yet."
    transcript = "\n\n".join(
        f"Customer ({h['subject']}): {h['email']}\nSupport: {h['reply']}" for h in history
    )
    prompt = (
        "Summarise this customer support conversation in 3 short bullet points: "
        "the customer's issue, what support promised, and any pending action.\n\n"
        f"{transcript}\n\nSummary:"
    )
    return llm(prompt)
