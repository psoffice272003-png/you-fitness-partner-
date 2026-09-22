import streamlit as st
from google import genai


st.set_page_config(
    page_title="Gym Trainer AI",
    page_icon="🏋️",
    layout="wide"
)

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "Gemini API Key not found. Add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key = GEMINI_API_KEY)

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

Only provide fitness, gym, workout, nutrition,
recovery and health related guidance.
"""

# ==============================
# Session State
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# Sidebar
# ==============================

with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ==============================
# Main UI
# ==============================

st.title("🏋️ Gym Trainer AI")
st.caption("Personal Fitness & Nutrition Assistant")

# Show Chat History

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# Chat Input
# ==============================

prompt = st.chat_input("Ask your fitness question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = SYSTEM_PROMPT + "\n\n"

    for msg in st.session_state.messages:
        role = msg["role"]

        if role == "user":
            conversation += f"User: {msg['content']}\n"

        elif role == "assistant":
            conversation += f"Assistant: {msg['content']}\n"

    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:
                response = client.models.generate_content(model = 'gemini-flash-lite-latest', contents=prompt)

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
