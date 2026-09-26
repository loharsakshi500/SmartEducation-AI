import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Education AI",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    st.error("OpenRouter API key not found.")
    st.info("Please add OPENROUTER_API_KEY to your .env file.")
    st.stop()


# --------------------------------------------------
# OPENROUTER CLIENT
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


# --------------------------------------------------
# AI MODEL
# --------------------------------------------------

MODEL = "google/gemini-2.5-flash"


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #888888;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🎓 Smart Education")

    st.write("AI Learning Assistant")

    st.divider()

    if st.button("🆕 New Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "system",
                "content": """
                You are Smart Education AI,
                an educational AI assistant.

                Your job is to help students understand
                academic subjects clearly.

                Give:
                - Simple explanations
                - Examples
                - Step-by-step solutions
                - Important points
                - Exam-friendly answers

                If the student asks for a difficult topic,
                explain it in simple language.

                Do not unnecessarily make answers complicated.
                """
            }
        ]

        st.rerun()

    st.divider()

    st.subheader("📚 Features")

    st.write("🤖 AI Chatbot")
    st.write("📖 Study Assistance")
    st.write("📝 Exam Preparation")
    st.write("💡 Simple Explanations")

    st.divider()

    st.caption("Smart Education AI")
    st.caption("BCA Final Year Project")


# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are Smart Education AI,
            an educational AI assistant.

            Help students with:
            - Programming
            - Computer Science
            - Mathematics
            - Database
            - Software Engineering
            - Cyber Security
            - General academic subjects

            Answer in simple and clear language.

            When appropriate, provide:
            1. Definition
            2. Explanation
            3. Example
            4. Important points

            For programming questions,
            provide clean and understandable code.
            """
        }
    ]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 Smart Education AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Personal AI Learning Assistant</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_question = st.chat_input(
    "Ask your study question..."
)


# --------------------------------------------------
# AI RESPONSE
# --------------------------------------------------

if user_question:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "Something went wrong while connecting to the AI."
                )

                st.code(str(e))