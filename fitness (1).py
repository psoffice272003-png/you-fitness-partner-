import streamlit as st
from google import genai
from google.genai import types

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Gym Trainer AI",
    page_icon="🏋️",
    layout="wide"
)

# =========================================================
# GEMINI API
# =========================================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error(
        "Gemini API Key not found. "
        "Add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Gym Trainer AI.

You specialize in:
- Strength Training
- Muscle Building
- Fat Loss
- Nutrition
- Recovery
- Sports Performance

When information is missing, ask for:
- Age
- Gender
- Height
- Weight
- Goal
- Experience
- Equipment
- Diet Preference
- Injuries

Always respond using this format:

🎯 Goal Assessment

🏋️ Training Recommendation

🥗 Nutrition Guidance

💪 Recovery Recommendations

✅ Action Plan

Only provide fitness, gym, workout, nutrition,
recovery and health-related guidance.

Do not diagnose medical conditions.

If the user describes a serious injury,
medical emergency, severe symptoms, or
other medical concerns, recommend consulting
a qualified healthcare professional.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# MAIN UI
# =========================================================

st.title("🏋️ Gym Trainer AI")
st.caption("Personal Fitness & Nutrition Assistant")

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input("Ask your fitness question...")

if prompt:

    # Save and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build Gemini conversation history
    conversation = []

    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "model"

        conversation.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ]
            )
        )

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🏋️ Your trainer is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )

                answer = response.text

                if not answer:
                    answer = "I couldn't generate a response. Please try again."

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                st.error(f"Gemini API Error:\n\n{str(e)}")
