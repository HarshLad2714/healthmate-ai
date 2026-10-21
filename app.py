import os
import streamlit as st
from google import genai
from google.genai import types

# ---------- Config ----------
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # change if a newer model is available

SYSTEM_PROMPT = """You are HealthMate AI, a friendly health information assistant for people in India.

Rules:
1. Reply in the SAME language the user writes in: Gujarati, Hindi, or English. If the user writes
   Gujarati/Hindi in English letters (e.g. "mane taav che"), reply in that language using the same style.
2. Use very simple words. Keep answers short (under 150 words), with small bullet points when useful.
3. Give general information and basic self-care tips only (rest, fluids, diet, hygiene, sleep).
4. NEVER diagnose a disease. NEVER recommend prescription medicines or exact doses.
5. Clearly say when the user should see a doctor. For serious symptoms (chest pain, trouble breathing,
   severe bleeding, stroke signs, high fever in infants, thoughts of self-harm), tell them to seek
   emergency care immediately.
6. If the question is not about health or wellness, politely say you can only help with health topics.
7. End every answer with one short line reminding that this is general information, not medical advice.
"""

EMERGENCY_WORDS = [
    "chest pain", "can't breathe", "cannot breathe", "heart attack", "stroke",
    "suicide", "kill myself", "self harm", "overdose", "severe bleeding",
    "chhatima dukhavo", "chhati ma dukhavo", "सीने में दर्द", "छाती में दर्द",
    "આત્મહત્યા", "आत्महत्या",
]

EMERGENCY_MSG = (
    "🚨 **This may be an emergency.** Please act now:\n\n"
    "- Call **112** (national emergency number) or **108** (ambulance)\n"
    "- Go to the nearest hospital or ask someone nearby to help you\n"
    "- For emotional distress, call **Tele-MANAS: 14416**\n"
)

# ---------- Page ----------
st.set_page_config(page_title="HealthMate AI", page_icon="🩺", layout="centered")
st.title("🩺 HealthMate AI")
st.caption("Simple health answers in Gujarati • Hindi • English")

with st.sidebar:
    st.header("About")
    st.write(
        "HealthMate AI gives general health information in simple language. "
        "It does **not** replace a doctor."
    )
    st.markdown("**Try asking:**")
    st.markdown(
        "- I have a mild fever, what should I do?\n"
        "- મને માથાનો દુખાવો છે, શું કરવું?\n"
        "- मुझे सर्दी-खांसी है, क्या करूँ?"
    )
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- API key ----------
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it as an environment variable or in .streamlit/secrets.toml")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------- Chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info("👋 Hi! Ask me any everyday health question in Gujarati, Hindi or English.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])


def to_contents(messages):
    return [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]


# ---------- Handle input ----------
if prompt := st.chat_input("Ask a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = ""
        if any(w in prompt.lower() for w in EMERGENCY_WORDS):
            reply += EMERGENCY_MSG + "\n---\n"
            st.markdown(EMERGENCY_MSG)
        try:
            with st.spinner("Thinking..."):
                resp = client.models.generate_content(
                    model=MODEL,
                    contents=to_contents(st.session_state.messages),
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                        max_output_tokens=800,
                    ),
                )
            answer = resp.text or "Sorry, I could not generate an answer. Please try again."
        except Exception as e:
            answer = f"⚠️ Something went wrong: {e}"
        st.markdown(answer)
        reply += answer

    st.session_state.messages.append({"role": "assistant", "content": reply})
