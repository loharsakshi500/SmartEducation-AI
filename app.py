import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Education AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("OpenRouter API key not found.")
    st.info("Add OPENROUTER_API_KEY to your .env file.")
    st.stop()

# =========================================================
# OPENROUTER
# =========================================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

MODEL = "google/gemini-2.5-flash"

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Smart Education AI, an AI learning assistant for students.

Help students with:
- Programming
- Computer Science
- Mathematics
- Database
- Software Engineering
- Cyber Security
- Data Analytics
- Web Development
- General academic subjects

Use simple, clear language.

For academic questions:
- Give a definition when useful
- Explain the concept clearly
- Give examples
- Give important points

For exam questions:
- Give point-wise answers
- Use easy language
- Make answers exam-friendly
- Follow the requested mark format if the student mentions 2 marks,
  5 marks, 10 marks, etc.

For programming:
- Give clean code
- Explain the code
- Keep examples understandable

Do not unnecessarily make answers complicated.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = []

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background: #ffffff;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #f7f7f8;
        border-right: 1px solid #e5e5e5;
    }

    section[data-testid="stSidebar"] * {
        color: #202123;
    }

    .sidebar-brand {
        font-size: 20px;
        font-weight: 700;
        padding: 8px 4px 18px 4px;
    }

    /* =========================
       MAIN AREA
       ========================= */

    .main-container {
        max-width: 900px;
        margin: auto;
        padding: 20px;
    }

    /* =========================
       WELCOME
       ========================= */

    .welcome-container {
        text-align: center;
        padding-top: 17vh;
        padding-bottom: 30px;
    }

    .welcome-icon {
        font-size: 45px;
        margin-bottom: 12px;
    }

    .welcome-title {
        font-size: 32px;
        font-weight: 650;
        color: #202123 !important;
        margin-bottom: 8px;
    }

    .welcome-subtitle {
        font-size: 16px;
        color: #6b6b6b !important;
    }

    /* =========================
       QUICK ACTIONS
       ========================= */

    .quick-title {
        font-size: 14px;
        font-weight: 600;
        color: #555 !important;
        margin-bottom: 8px;
    }

    /* =========================
       CHAT
       ========================= */

    [data-testid="stChatMessage"] {
        color: #202123 !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #202123 !important;
    }

    [data-testid="stChatMessage"] code {
        color: #202123 !important;
    }

    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stChatInput"] textarea {
        color: #202123 !important;
        background: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #777777 !important;
    }

    /* =========================
       BUTTONS
       ========================= */

    .stButton button {
        border-radius: 10px;
        border: 1px solid #dddddd;
        background: white;
        color: #202123;
    }

    .stButton button:hover {
        border-color: #999999;
        background: #f5f5f5;
    }

    /* =========================
       FOOTER
       ========================= */

    .app-footer {
        text-align: center;
        color: #999999 !important;
        font-size: 12px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            🎓 Smart Education AI
        </div>
        """,
        unsafe_allow_html=True
    )

    # New chat

    if st.button(
        "＋  New chat",
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

    # Study tools

    st.markdown("### Study tools")

    if st.button(
        "📚  Explain a topic",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Explain a difficult academic topic in simple language."
        )

    if st.button(
        "📝  Generate quiz",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Generate a short quiz for me on a topic I provide."
        )

    if st.button(
        "📖  Make study notes",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Help me create short and important study notes."
        )

    if st.button(
        "💻  Coding help",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Help me understand a programming concept with simple code."
        )

    st.divider()

    # Chat history

    st.markdown("### Recent chats")

    user_messages = [
        m for m in st.session_state.messages
        if m["role"] == "user"
    ]

    if user_messages:

        for msg in user_messages[-5:]:
            title = msg["content"][:35]

            if len(msg["content"]) > 35:
                title += "..."

            st.caption("💬 " + title)

    else:

        st.caption("No conversations yet")

    st.divider()

    st.caption("Smart Education AI")
    st.caption("AI learning assistant")

# =========================================================
# MAIN
# =========================================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True
)

# =========================================================
# CHECK WHETHER CHAT EXISTS
# =========================================================

has_chat = any(
    message["role"] == "user"
    for message in st.session_state.messages
)

# =========================================================
# WELCOME SCREEN
# =========================================================

if not has_chat:

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-icon">
                🎓
            </div>

            <div class="welcome-title">
                What can I help you learn?
            </div>

            <div class="welcome-subtitle">
                Ask questions, understand concepts,
                prepare for exams or learn programming.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="quick-title">Try asking</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "📖 Explain a topic",
            use_container_width=True
        ):
            st.session_state.quick_prompt = (
                "Explain a difficult academic topic in simple language."
            )
            st.rerun()

    with q2:

        if st.button(
            "📝 Prepare for exam",
            use_container_width=True
        ):
            st.session_state.quick_prompt = (
                "Help me prepare an exam answer."
            )
            st.rerun()

    with q3:

        if st.button(
            "💻 Learn programming",
            use_container_width=True
        ):
            st.session_state.quick_prompt = (
                "Teach me a programming concept with a simple example."
            )
            st.rerun()

# =========================================================
# DISPLAY CHAT
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================================================
# QUICK PROMPT
# =========================================================

quick_prompt = st.session_state.pop(
    "quick_prompt",
    None
)

# =========================================================
# CHAT INPUT
# =========================================================

user_question = st.chat_input(
    "Message Smart Education AI..."
)

if quick_prompt and not user_question:
    user_question = quick_prompt

# =========================================================
# SEND MESSAGE
# =========================================================

if user_question:

    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Display user

    with st.chat_message("user"):

        st.markdown(user_question)

    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

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
                    "Unable to connect to the AI."
                )

                st.code(str(e))

st.markdown(
    """
    <div class="app-footer">
        Smart Education AI • Learn smarter with AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
