"""Reply Module: drafts a professional, context-aware reply."""
from modules.llm import ask_ollama


def generate_reply(customer_name, subject, email, intent, similar, history=None, llm=ask_ollama) -> str:
    examples = "\n\n".join(
        f"Past email: {r.Email}\nPast reply: {r.Reply}" for r in similar.itertuples()
    )
    past = ""
    if history:
        past = "Earlier in this conversation:\n" + "\n".join(
            f"- Customer: {h['email']}\n- Us: {h['reply']}" for h in history[-3:]
        ) + "\n\n"
    prompt = (
        "You are a customer support agent. Write a polite, professional email reply.\n"
        "Follow the style and policy shown in the similar past replies. Do not invent "
        "policies, prices, dates or order details that are not in the examples.\n\n"
        f"Similar past conversations:\n{examples}\n\n{past}"
        f"New email from {customer_name}\nSubject: {subject}\nDetected intent: {intent}\n"
        f"Message: {email}\n\n"
        f"Write only the reply, addressed to {customer_name} and signed 'Customer Support Team'."
    )
    return llm(prompt)
