import streamlit as st
import datetime

# set home

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
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

pg = st.navigation([st.Page("AI_Assistant.py"), st.Page("Jarvis_AI_Agent.py"), st.Page("Send_Mail.py")])
pg.run()