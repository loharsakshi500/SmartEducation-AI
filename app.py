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
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    st.error("❌ OpenRouter API key not found.")
    st.info("Add OPENROUTER_API_KEY to your .env file.")
    st.stop()

# --------------------------------------------------
# OPENROUTER CLIENT
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODEL = "google/gemini-2.5-flash"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
    }

    .main-header h1 {
        font-size: 42px;
        margin: 0;
    }

    .main-header p {
        font-size: 18px;
        margin-top: 8px;
    }

    /* Welcome Box */
    .welcome {
        background: white;
        padding: 22px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
    }

    .welcome h3 {
        margin-top: 0;
    }

    /* Cards */
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        min-height: 145px;
        border: 1px solid #eeeeee;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .card-icon {
        font-size: 35px;
    }

    .card-title {
        font-size: 17px;
        font-weight: bold;
        margin-top: 8px;
    }

    .card-text {
        font-size: 13px;
        color: #777;
        margin-top: 5px;
    }

    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin: 25px 0 15px 0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
You are Smart Education AI, an educational AI assistant.

Your purpose is to help students learn difficult topics
in simple and understandable language.

You can help with:
- Programming
- Computer Science
- Mathematics
- Database
- Software Engineering
- Cyber Security
- Data Analytics
- Web Development
- General academic subjects

For academic questions:
1. Give a simple definition
2. Explain clearly
3. Give an example
4. Give important points

For exam questions:
- Use easy language
- Give point-wise answers
- Make answers exam-friendly
- Mention important points

For programming questions:
- Give clean and simple code
- Explain the code

Avoid unnecessarily complicated explanations.
"""
        }
    ]

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎓 Smart Education AI")

    st.caption("Your Personal AI Learning Assistant")

    st.divider()

    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": """
You are Smart Education AI.

Help students understand academic subjects
using simple explanations, examples,
step-by-step solutions and exam-friendly answers.

For programming questions, provide clean,
understandable code.
"""
            }
        ]

        st.rerun()

    st.divider()

    st.markdown("### 📚 Features")

    st.write("🤖 AI Chatbot")
    st.write("📖 Study Assistance")
    st.write("📝 Exam Preparation")
    st.write("💻 Programming Help")
    st.write("💡 Simple Explanations")

    st.divider()

    st.markdown("### 🎯 Study Tip")

    st.info(
        "Ask your question naturally. "
        "You can ask for short notes, examples, "
        "exam answers or code."
    )

    st.divider()

    st.caption("Smart Education AI")
    st.caption("AI-Powered Learning Assistant")

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="main-header">
        <h1>🎓 Smart Education AI</h1>
        <p>Your Personal AI Learning Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# WELCOME
# --------------------------------------------------

st.markdown(
    """
    <div class="welcome">
        <h3>👋 Welcome, Student!</h3>
        <p>
        Learn smarter with AI. Ask questions, understand
        difficult concepts, prepare for exams and get
        programming help.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">✨ What can I help you with?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🤖</div>
            <div class="card-title">AI Chatbot</div>
            <div class="card-text">
                Ask questions and get instant answers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📚</div>
            <div class="card-title">Study Assistance</div>
            <div class="card-text">
                Understand difficult topics easily.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📝</div>
            <div class="card-title">Exam Preparation</div>
            <div class="card-text">
                Get simple and exam-friendly answers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">💻</div>
            <div class="card-title">Programming Help</div>
            <div class="card-text">
                Learn coding with simple examples.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# CHAT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">💬 Ask Smart Education AI</div>',
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
    "💬 Ask your study question..."
)

# --------------------------------------------------
# AI RESPONSE
# --------------------------------------------------

if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

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

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while connecting to the AI."
                )

                st.code(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        🎓 <b>Smart Education AI</b>
        <br>
        Learn • Understand • Practice • Improve
    </div>
    """,
    unsafe_allow_html=True
)
