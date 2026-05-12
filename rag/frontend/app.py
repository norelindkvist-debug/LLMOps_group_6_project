import streamlit as st
import httpx
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/rag/query")

st.set_page_config(page_title="CSN Assistant", layout="wide")

# Initialisera session state
if "chip_input" not in st.session_state:
    st.session_state.chip_input = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #f5f5f0 !important;
    color: #1a1a1a;
}
.stApp { background-color: #f5f5f0; }

.csn-navbar {
    background: white;
    padding: 0 40px;
    display: flex;
    align-items: center;
    height: 72px;
    border-bottom: 1px solid #e0e0e0;
}
.csn-logo-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
}
.csn-logo-box {
    width: 52px;
    height: 52px;
    background: #4a1a6b;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
    color: white;
    letter-spacing: 0.5px;
}
.csn-tagline {
    font-size: 15px;
    color: #444;
    font-style: italic;
}
.csn-hero {
    background: #4a1a6b;
    padding: 70px 40px;
    text-align: center;
}
.csn-hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    color: white;
    margin: 0;
}
.csn-hero h1 span { color: #f0804a; }

.chat-wrapper {
    max-width: 700px;
    margin: 0 auto;
    padding: 0 24px 60px;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #4a1a6b;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #ede8f5;
}

/* Tightare och snyggare chips */
div[data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: white !important;
    color: #4a1a6b !important;
    border: 1.5px solid #4a1a6b !important;
    border-radius: 24px !important;
    padding: 8px 16px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    min-height: 42px !important;
    white-space: nowrap;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #4a1a6b !important;
    color: white !important;
}

/* Meddelanden */
.msg-user .bubble {
    background: #4a1a6b;
    color: white;
    padding: 13px 18px;
    border-radius: 20px 4px 20px 20px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.6;
}
.msg-bot {
    display: flex;
    gap: 14px;
    margin-bottom: 16px;
    align-items: flex-start;
}
.bot-avatar {
    width: 40px;
    height: 40px;
    background: #4a1a6b;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 11px;
    color: white;
    flex-shrink: 0;
}
.msg-bot .bubble {
    background: white;
    color: #1a1a1a;
    padding: 16px 20px;
    border-radius: 4px 20px 20px 20px;
    max-width: 80%;
    font-size: 15px;
    line-height: 1.75;
    border: 1px solid #e0d8ee;
    box-shadow: 0 2px 8px rgba(74,26,107,0.06);
}
.source-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    padding: 5px 14px;
    background: #ede8f5;
    border: 1px solid #c5b8e0;
    border-radius: 20px;
    font-size: 12px;
    color: #4a1a6b;
    font-weight: 600;
}

.stTextInput > div > div > input {
    background: #f9f7fc !important;
    border: 2px solid #d5cce8 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
}
.stButton > button {
    background: #4a1a6b !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 32px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #f0804a !important;
}
</style>
""", unsafe_allow_html=True)

CHIP_QUESTIONS = [
    "Hur ansöker jag om studielån?",
    "När börjar återbetalningen?",
    "Bidrag vs lån",
    "Hur mycket kan jag få?",
]

def layout():
    st.markdown("""
    <div class="csn-navbar">
        <div class="csn-logo-wrap">
            <div class="csn-logo-box">CSN</div>
            <span class="csn-tagline">Vi gör studier möjligt.</span>
        </div>
    </div>
    <div class="csn-hero">
        <h1>Vad vill du ha <span>hjälp med idag?</span></h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Vanliga frågor</div>', unsafe_allow_html=True)

    # === TIGHTARE CHIP-KNAPPAR ===
    cols = st.columns(len(CHIP_QUESTIONS), gap="small")
    for i, question in enumerate(CHIP_QUESTIONS):
        with cols[i]:
            if st.button(question, key=f"chip_{i}", use_container_width=True):
                st.session_state.chip_input = question
                st.session_state.pending_question = question
                st.rerun()

    # === TEXT INPUT ===
    prefill = st.session_state.get("chip_input", "")

    text_input = st.text_input(
        "Ställ din fråga",
        value=prefill,
        placeholder="Ställ din fråga om CSN här...",
        label_visibility="collapsed",
        key="user_question"
    )

    # === SKICKA KNAPP ===
    col1, col2, col3 = st.columns([6, 3, 6])
    with col2:
        send_clicked = st.button("Skicka fråga", key="send_btn", type="primary")

    # === VISA TIDIGARE MEDDELANDEN ===
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-user"><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-bot">
                <div class="bot-avatar">CSN</div>
                <div class="bubble">
                    {msg["content"]}
                    <div class="source-pill">Källa: {msg.get("source", "csn.se")}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # === HANTERA SKICKAD FRÅGA (från knapp eller textfält) ===
    if (send_clicked and text_input.strip()) or st.session_state.get("pending_question"):
        user_question = st.session_state.get("pending_question") or text_input.strip()
        
        if user_question:
            # Visa användarens fråga
            st.markdown(f'<div class="msg-user"><div class="bubble">{user_question}</div></div>', unsafe_allow_html=True)

            with st.spinner("Hämtar svar..."):
                try:
                    response = httpx.post(API_URL, json={"prompt": user_question}, timeout=120)
                    response.raise_for_status()
                    data = response.json()

                    answer = data.get("answer", "Inget svar kunde hämtas.")
                    source = data.get("filename", "csn.se")

                    st.markdown(f"""
                    <div class="msg-bot">
                        <div class="bot-avatar">CSN</div>
                        <div class="bubble">
                            {answer}
                            <div class="source-pill">Källa: {source}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Spara till historik
                    st.session_state.messages.append({"role": "user", "content": user_question})
                    st.session_state.messages.append({"role": "assistant", "content": answer, "source": source})

                except Exception as e:
                    st.error(f"Något gick fel: {str(e)}")

            # Rensa efter skickning
            st.session_state.chip_input = ""
            st.session_state.pending_question = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    layout()