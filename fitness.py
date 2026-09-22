import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

GEMINI_API_KEY = "AQ.Ab8RN6LBZ-Xd1PUpZoQCnVhyXnqssm__kwnggbridjgcEPkXDQ"

if not GEMINI_API_KEY:
    st.error("Gemini API Key not found in .env file")
    st.stop()

# ==============================
# Configure Gemini
# ==============================
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-lite-latest")

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Gym Trainer AI",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ Gym Trainer AI")

# ==============================
# User Session
# ==============================
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_1"

history_file = f"history_{st.session_state.user_id}.json"

# ==============================
# System Prompt
# ==============================
SYSTEM_PROMPT = """
You are Gym Trainer AI.

You specialize in:
- Strength Training
- Muscle Building
- Fat Loss
- Nutrition
- Recovery
- Sports Performance

When information is missing ask for:
- Age
- Gender
- Height
- Weight
- Goal
- Experience
- Equipment
- Diet Preference
- Injuries

Always respond in this format:

🎯 Goal Assessment

🏋️ Training Recommendation

🥗 Nutrition Guidance

💪 Recovery Recommendations

✅ Action Plan
"""

DEFAULT_MESSAGES = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# ==============================
# Load History
# ==============================
if os.path.exists(history_file):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except Exception:
        messages = DEFAULT_MESSAGES.copy()
else:
    messages = DEFAULT_MESSAGES.copy()

# ==============================
# Save History
# ==============================
def save_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.header("Settings")

    if st.button("🗑 Clear Chat"):
        messages = DEFAULT_MESSAGES.copy()

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2)

        st.rerun()

# ==============================
# Display Chat History
# ==============================
for msg in messages:
    if msg["role"] == "system":
        continue

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# Chat Input
# ==============================
prompt = st.chat_input("Ask your fitness question...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Build conversation context
    conversation = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            conversation += f"System: {content}\n\n"
        elif role == "user":
            conversation += f"User: {content}\n\n"
        elif role == "assistant":
            conversation += f"Assistant: {content}\n\n"

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:
                response = model.generate_content(conversation)

                answer = response.text

                st.markdown(answer)

                messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                save_history()

            except Exception as e:
                st.error(f"Error: {str(e)}")