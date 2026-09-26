import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Smart Education AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CHECK API KEY
# ==================================================

if not API_KEY:
    st.error("❌ OpenRouter API key not found.")
    st.info("Please add OPENROUTER_API_KEY to your .env file.")
    st.stop()

# ==================================================
# OPENROUTER CLIENT
# ==================================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODEL = "google/gemini-2.5-flash"

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ==============================================
       MAIN APP
       ============================================== */

    .stApp {
        background-color: #f5f7fb;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ==============================================
       MAIN HEADER
       ============================================== */

    .main-header {
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );

        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
    }

    .main-header h1 {
        font-size: 42px;
        margin: 0;
        color: white !important;
    }

    .main-header p {
        font-size: 18px;
        margin-top: 8px;
        color: white !important;
    }

    /* ==============================================
       WELCOME BOX
       ============================================== */

    .welcome {
        background-color: white;
        padding: 22px;
        border-radius: 16px;
        margin-bottom: 25px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.06);
    }

    .welcome h3 {
        margin-top: 0;
        color: #222222 !important;
    }

    .welcome p {
        color: #444444 !important;
        font-size: 16px;
    }

    /* ==============================================
       FEATURE CARDS
       ============================================== */

    .card {
        background-color: white;

        padding: 20px;

        border-radius: 16px;

        text-align: center;

        min-height: 145px;

        border: 1px solid #eeeeee;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.05);
    }

    .card-icon {
        font-size: 35px;
    }

    .card-title {
        font-size: 17px;
        font-weight: bold;
        margin-top: 8px;
        color: #222222 !important;
    }

    .card-text {
        font-size: 13px;
        color: #777777 !important;
        margin-top: 5px;
    }

    /* ==============================================
       SECTION TITLE
       ============================================== */

    .section-title {
        font-size: 24px;
        font-weight: bold;

        margin-top: 25px;
        margin-bottom: 15px;

        color: #222222 !important;
    }

    /* ==============================================
       SIDEBAR
       ============================================== */

    section[data-testid="stSidebar"] {
        background-color: white;
    }

    section[data-testid="stSidebar"] * {
        color: #222222;
    }

    /* Sidebar buttons */

    section[data-testid="stSidebar"]
    .stButton button {
        color: #222222 !important;
        background-color: #f5f5f5 !important;
        border: 1px solid #dddddd !important;
    }

    /* ==============================================
       CHAT MESSAGE
       ============================================== */

    [data-testid="stChatMessage"] {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] p {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] span {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] li {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] ul {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] ol {
        color: #222222 !important;
    }

    [data-testid="stChatMessage"] strong {
        color: #111111 !important;
    }

    [data-testid="stChatMessage"] em {
        color: #333333 !important;
    }

    /* ==============================================
       CODE IN AI RESPONSE
       ============================================== */

    [data-testid="stChatMessage"] code {
        color: #222222 !important;
    }

    /* ==============================================
       CHAT INPUT
       ============================================== */

    [data-testid="stChatInput"] textarea {
        color: #222222 !important;
        background-color: white !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #777777 !important;
    }

    /* ==============================================
       NORMAL MARKDOWN
       ============================================== */

    .stMarkdown p {
        color: #222222;
    }

    .stMarkdown li {
        color: #222222;
    }

    /* ==============================================
       FOOTER
       ============================================== */

    .footer {
        text-align: center;
        color: #777777 !important;
        padding: 15px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
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
- Explain the code clearly

Always try to make the answer easy for students
to understand.

Avoid unnecessarily complicated explanations.
"""

# ==================================================
# CHAT MEMORY
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🎓 Smart Education AI")

    st.caption(
        "Your Personal AI Learning Assistant"
    )

    st.divider()

    # New Chat Button

    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()

    st.divider()

    # Features

    st.markdown("### 📚 Features")

    st.write("🤖 AI Chatbot")
    st.write("📖 Study Assistance")
    st.write("📝 Exam Preparation")
    st.write("💻 Programming Help")
    st.write("💡 Simple Explanations")

    st.divider()

    # Study Tip

    st.markdown("### 🎯 Study Tip")

    st.info(
        "Ask your question naturally. "
        "You can ask for short notes, examples, "
        "exam answers or programming help."
    )

    st.divider()

    st.caption("Smart Education AI")
    st.caption("AI-Powered Learning Assistant")

# ==================================================
# MAIN HEADER
# ==================================================

st.markdown(
    """
    <div class="main-header">

        <h1>🎓 Smart Education AI</h1>

        <p>
            Your Personal AI Learning Assistant
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# WELCOME SECTION
# ==================================================

st.markdown(
    """
    <div class="welcome">

        <h3>👋 Welcome, Student!</h3>

        <p>
            Learn smarter with AI. Ask questions,
            understand difficult concepts, prepare
            for exams and get programming help.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# FEATURES
# ==================================================

st.markdown(
    """
    <div class="section-title">
        ✨ What can I help you with?
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

# --------------------------------------------------
# CARD 1
# --------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">
                🤖
            </div>

            <div class="card-title">
                AI Chatbot
            </div>

            <div class="card-text">
                Ask questions and get instant answers.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# CARD 2
# --------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">
                📚
            </div>

            <div class="card-title">
                Study Assistance
            </div>

            <div class="card-text">
                Understand difficult topics easily.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# CARD 3
# --------------------------------------------------

with col3:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">
                📝
            </div>

            <div class="card-title">
                Exam Preparation
            </div>

            <div class="card-text">
                Get simple and exam-friendly answers.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# CARD 4
# --------------------------------------------------

with col4:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">
                💻
            </div>

            <div class="card-title">
                Programming Help
            </div>

            <div class="card-text">
                Learn coding with simple examples.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# CHAT SECTION
# ==================================================

st.markdown(
    """
    <div class="section-title">
        💬 Ask Smart Education AI
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# ==================================================
# CHAT INPUT
# ==================================================

user_question = st.chat_input(
    "💬 Ask your study question..."
)

# ==================================================
# AI RESPONSE
# ==================================================

if user_question:

    # ------------------------------------------------
    # ADD USER MESSAGE
    # ------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # ------------------------------------------------
    # DISPLAY USER MESSAGE
    # ------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            user_question
        )

    # ------------------------------------------------
    # GENERATE AI RESPONSE
    # ------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤔 Smart Education AI is thinking..."
        ):

            try:

                response = client.chat.completions.create(

                    model=MODEL,

                    messages=st.session_state.messages,

                    temperature=0.7,

                    max_tokens=1000
                )

                # Get response

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                # Display response

                st.markdown(answer)

                # Save response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong "
                    "while connecting to the AI."
                )

                st.code(
                    str(e)
                )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">

        🎓 <b>Smart Education AI</b>

        <br>

        Learn • Understand • Practice • Improve

    </div>
    """,
    unsafe_allow_html=True
            )
