import os
import smtplib
import ssl
from llm import LLM
import streamlit as st
from email.message import EmailMessage
from pathlib import Path

# Page seting


# Page configuration
st.set_page_config(
    page_title="Email_Sender",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    :root {
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #0f3460;
        --highlight: #e94560;
        --text: #f1f1f1;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: var(--text);
    }
    
    .stChatInput {
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: var(--highlight) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--highlight);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--highlight) !important;
        border-bottom: 2px solid var(--highlight);
        padding-bottom: 10px;
    }
    
    .stAudio {
        width: 100%;
        margin-top: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
    }
    
    .message-user {
        background: rgba(15, 52, 96, 0.5) !important;
        border-radius: 15px 15px 0 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .message-assistant {
        background: rgba(233, 69, 96, 0.2) !important;
        border-radius: 15px 15px 15px 0;
        padding: 15px;
        margin: 10px 0;
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, var(--accent), var(--highlight));
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: var(--secondary) !important;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)


# 1. CONFIGURATION
# ───────────────────────────────────────────────────────────────
# You can hardcode these (not recommended) or export as env vars:
SMTP_HOST    = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", 587))
SMTP_USER    =  "muhammad.bilal.05.07.09@gmail.com"
SMTP_PASSWORD = "yywomlkfypolzabj"

# App header
st.markdown('<div class="header"><h1>🤖 Email Sender</h1></div>', unsafe_allow_html=True)



SENDER       = SMTP_USER
RECIPIENTS   = st.text_input("Enter Recipients").split(",")
SUBJECT      = st.text_input("Enter Subject")

# 2. BUILD THE MESSAGE
msg = EmailMessage()
msg["From"]    = SENDER
msg["To"]      = ", ".join(RECIPIENTS)
msg["Subject"] = SUBJECT

prompt = "You are an AI email generator, take user query and make a well organized emails according to the user query./n user query:{query}. /n You must have to genrate a ready to send email, there will be no change in your genrated email. So make the final emailto send."

query = st.text_input("Enter Query")
text = LLM(query)
st.write(text)
text_body = st.text_area("Copy text and Enter as Email Message (Modify if you want)")
msg.set_content(text_body)

# 3. ATTACH FILES (optional)
# ───────────────────────────────────────────────────────────────
files_to_attach = [
    "reports/summary.pdf",
    "images/chart.png"
    ]
for file_path in files_to_attach:
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️ Warning: attachment not found: {path}")
        continue

    maintype, subtype = ("application", "octet-stream")
    if path.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
        maintype, subtype = ("image", path.suffix.replace(".", ""))
    elif path.suffix.lower() == ".pdf":
        maintype, subtype = ("application", "pdf")

    data = path.read_bytes()
    msg.add_attachment(data,
                      maintype=maintype,
                      subtype=subtype,
                      filename=path.name)

    # 4. SEND THE MESSAGE
    # ───────────────────────────────────────────────────────────────
def send_email(message: EmailMessage):
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Upgrade to secure TLS
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)
        st.success("✅ Email sent successfully!")

if __name__ == "__main__":
    # sanity check
    if not (SMTP_USER and SMTP_PASSWORD):
        print("❌ Please set SMTP_USER and SMTP_PASSWORD as environment variables.")
        exit(1)
    if st.button("Send email"):
        send_email(msg)
