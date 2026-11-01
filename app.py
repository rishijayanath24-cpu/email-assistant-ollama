"""Intelligent Email Assistant using Ollama - Streamlit app.

Run with:  streamlit run app.py
"""
import streamlit as st

from modules.input_module import build_email
from modules.intent_module import detect_intent
from modules.llm import MODEL_NAME, OllamaError
from modules.reply_module import generate_reply
from modules.retrieval_module import EmailRetriever
from modules.save_module import load_saved, save_reply
from modules.summary_module import summarize_conversation
from modules.tone_module import TONES, improve_tone

st.set_page_config(page_title="Intelligent Email Assistant", page_icon="✉️", layout="wide")


@st.cache_resource(show_spinner="Loading Sentence Transformer model...")
def get_retriever():
    return EmailRetriever("data/past_emails.csv")


def init_state():
    st.session_state.setdefault("history", [])   # finished exchanges (conversation memory)
    st.session_state.setdefault("current", None)  # exchange being worked on
    st.session_state.setdefault("reply_rev", 0)   # bumps the reply box key so new text shows


init_state()

# ---------------- Home screen ----------------
st.title("✉️ Intelligent Email Assistant")
st.caption(f"Local, private and cloud-free · LLM: {MODEL_NAME} via Ollama · "
           "Retrieval: Sentence Transformers")
st.markdown(
    "Paste a customer email below. The assistant detects the intent, finds similar past "
    "conversations, drafts a reply, lets you adjust the tone, summarises the conversation "
    "and saves the reply locally."
)

# ---------------- 1. Customer email ----------------
st.header("1. Customer Email")
with st.form("email_form"):
    c1, c2 = st.columns(2)
    name = c1.text_input("Customer Name")
    subject = c2.text_input("Subject")
    body = st.text_area("Email", height=140)
    submitted = st.form_submit_button("Analyze & Generate Reply")

if submitted:
    try:
        mail = build_email(name, subject, body)
        with st.spinner("Detecting intent..."):
            intent = detect_intent(mail["subject"], mail["email"])
        with st.spinner("Searching similar past emails..."):
            similar = get_retriever().retrieve(mail["subject"], mail["email"])
        with st.spinner("Drafting reply..."):
            reply = generate_reply(mail["customer_name"], mail["subject"], mail["email"],
                                   intent, similar, st.session_state.history)
        st.session_state.current = {**mail, "intent": intent, "similar": similar,
                                    "reply": reply, "tone": "Original", "summary": None}
        st.session_state.reply_rev += 1
    except ValueError as err:
        st.warning(str(err))
    except OllamaError as err:
        st.error(str(err))

cur = st.session_state.current
if cur:
    st.info(f"**{cur['customer_name']}** · {cur['subject']}\n\n{cur['email']}")

    st.header("2. Intent Detection")
    st.success(f"Detected intent: **{cur['intent']}**")

    st.header("3. Similar Email Retrieval")
    st.dataframe(cur["similar"][["Category", "Subject", "Email", "Reply", "Similarity"]],
                 use_container_width=True, hide_index=True)

    st.header("4. AI Reply")
    st.text_area("Generated reply", cur["reply"], height=220,
                 key=f"reply_box_{st.session_state.reply_rev}")

    st.header("5. Tone Improvement")
    t1, t2 = st.columns([1, 3])
    tone = t1.selectbox("Tone", list(TONES))
    if t1.button("Rewrite in this tone"):
        try:
            with st.spinner("Rewriting..."):
                cur["reply"] = improve_tone(cur["reply"], tone)
                cur["tone"] = tone
            st.session_state.reply_rev += 1
            st.rerun()
        except OllamaError as err:
            st.error(str(err))
    t2.caption(f"Current tone: {cur['tone']}")

    st.header("6. Conversation Summary")
    if st.button("Summarize conversation"):
        thread = st.session_state.history + [
            {"subject": cur["subject"], "email": cur["email"], "reply": cur["reply"]}]
        try:
            with st.spinner("Summarising..."):
                cur["summary"] = summarize_conversation(thread)
        except OllamaError as err:
            st.error(str(err))
    if cur["summary"]:
        st.write(cur["summary"])

    st.header("7. Saved Reply")
    if st.button("Save reply"):
        save_reply({"Timestamp": cur["received_at"], "Customer Name": cur["customer_name"],
                    "Subject": cur["subject"], "Email": cur["email"], "Intent": cur["intent"],
                    "Reply": cur["reply"], "Tone": cur["tone"]})
        st.session_state.history.append(
            {"subject": cur["subject"], "email": cur["email"], "reply": cur["reply"]})
        st.success("Reply saved to saved_replies/saved_replies.csv")
    saved = load_saved()
    if not saved.empty:
        st.dataframe(saved, use_container_width=True, hide_index=True)
