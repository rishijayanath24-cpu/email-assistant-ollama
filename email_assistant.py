import requests

# Ollama API settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

# Step 1: FAQ Knowledge Base
faq = {
    "pricing": "Our basic plan starts at $10/month with premium options.",
    "refund": (
        "Refunds are available within 30 days of purchase. Please share your"
        " order ID."
    ),
    "support": "You can reach support at support@example.com, 24/7.",
}

# Step 6: Maintain Context (Memory)
conversation_history = []

# Step 2: Check FAQ
def check_faq(email_text):
    for keyword, answer in faq.items():
        if keyword in email_text.lower():
            return answer
    return None

# Step 3: Generate AI Response with Ollama API
def ollama_response(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # disable streaming for simplicity
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

# Step 4, 6 & 7: Integrated Email Assistant Logic with Context / Memory
def email_assistant(email_text):
    # 1. Check FAQ first
    faq_answer = check_faq(email_text)
    if faq_answer:
        reply = "FAQ Reply: " + faq_answer
        conversation_history.append({"email": email_text, "reply": reply})
        return reply

    # 2. Append prior context if available
    context_str = ""
    if conversation_history:
        context_str = "Previous conversation history:\n"
        for item in conversation_history[-3:]:
            context_str += (
                f"- User: {item['email']}\n- Assistant: {item['reply']}\n"
            )
        context_str += "\n"

    prompt = (
        f"{context_str}"
        f"Draft a polite, professional email reply to this message:\n\n'{email_text}'"
    )

    # 3. Generate response using AI model and update memory
    ai_answer = ollama_response(prompt)
    reply = "AI Reply: " + ai_answer
    conversation_history.append({"email": email_text, "reply": reply})
    return reply

def main():
    print("=" * 60)
    print("   Ex.3 Intelligent Email Assistant Execution")
    print("=" * 60)

    # Step 8: Test with sample emails from manual
    emails = [
        "Tell me about pricing",
        "How to get refund?",
        "Need support help",
        "Delay in my order",
    ]
    for mail in emails:
        print(f"\nIncoming Email: '{mail}'")
        response = email_assistant(mail)
        print(response)
        print("-" * 50)

    # Test memory / context consistency
    follow_up = "Could you also expedite the delivery for that delayed order?"
    print(f"\nIncoming Follow-up Email: '{follow_up}'")
    response = email_assistant(follow_up)
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    main()
