# import speech_recognition as sr
# import os
# import webbrowser
# import datetime
# import random
# import streamlit as st
# import win32com.client
# from llm import LLM

# chatStr = ""

# def say(text):
#     speaker = win32com.client.Dispatch("SAPI.SpVoice")
#     speaker.Speak(text)

# def chat(query):
#     global chatStr
#     response = LLM(query)
#     say(response)
#     chatStr += f"Bilal:{query}\njarvis{response}\n"
#     return response


# #take command
# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         # r.pause_threshold =  0.6
#         audio = r.listen(source)
#         try:
#             print("Recognizing...")
#             query = r.recognize_google(audio, language="en-in")
#             print(f"User said: {query}")
#             return query
#         except Exception as e:
#             say("Some Error Occurred. Sorry from Jarvis")
#             return "Some Error Occurred. Sorry from Jarvis"

# if __name__ == '__main__':
#     print('Welcome to Jarvis A.I')
#     say("hey Jarvis AI")
#     while True:
#         print("Listening...")
#         query = takeCommand()
#         # todo: Add more sites
#         sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
#                 ["google", "https://www.google.com"], ["linkdin", "https://www.linkdin.com"],
#                 ["instagram", "https://www.instagram.com"], ["facebook", "https://www.facebook.com"],
#                 ["chatgpt", "https://www.chatgpt.com"], ["deepseek", "https://www.chat.deepseek.com"],
#                 ["tiktok", "https://www.tiktok.com"], ["whatsapp", "https://www.whatsapp.com"]]
#         for site in sites:
#             if f"Open {site[0]}".lower() in query.lower():
#                 say(f"Opening {site[0]} sir...")
#                 webbrowser.open(site[1])
  
#         if "open music" in query:
#             musicPath = "/Users/DELL 5300 A&I/OneDrive/Music/Aam Jahe Munde _ Parmish Verma feat Pardhaan _ Desi Crew _ Laddi Chahal(MP3_160K).mp3"
#             os.system(f"open {musicPath}")

#         elif "the time" in query:
#             musicPath = "/Users/DELL 5300 A&I/OneDrive/Music/Aam Jahe Munde _ Parmish Verma feat Pardhaan _ Desi Crew _ Laddi Chahal(MP3_160K).mp3"
#             hour = datetime.datetime.now().strftime("%H")
#             min = datetime.datetime.now().strftime("%M")
#             say(f"Sir time is {hour} bajke {min} minutes")

#         elif "bye Jarvis".lower() in query.lower():
#             exit()

#         elif "reset chat".lower() in query.lower():
#             chatStr = ""

#         elif "send email".lower() in query.lower():
#             from sendemail import send_email
#             send_email()
#         else:
#             if query != "Some Error Occurred. Sorry from Jarvis":
#                 print("Chatting...")
#                 chat(query)


import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import streamlit as st
import win32com.client
import time
import base64
from llm import LLM  # Assuming this is your custom LLM module
from streamlit.components.v1 import html

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'audio_playing' not in st.session_state:
    st.session_state.audio_playing = False
if 'last_command' not in st.session_state:
    st.session_state.last_command = ""
if 'mic_status' not in st.session_state:
    st.session_state.mic_status = "off"

# Set page config
st.set_page_config(
    page_title="Jarvis AI Assistant",
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
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .header {
        background: linear-gradient(90deg, var(--accent), var(--highlight));
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    
    .message-user {
        background: rgba(15, 52, 96, 0.5);
        border-radius: 15px 15px 0 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid var(--highlight);
    }
    
    .message-jarvis {
        background: rgba(233, 69, 96, 0.2);
        border-radius: 15px 15px 15px 0;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #00b4d8;
    }
    
    .command-button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid var(--highlight) !important;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s;
    }
    
    .command-button:hover {
        background: rgba(233, 69, 96, 0.2) !important;
        transform: scale(1.02);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-on {
        background-color: #4CAF50;
        box-shadow: 0 0 8px #4CAF50;
    }
    
    .status-off {
        background-color: #f44336;
    }
    
    .status-processing {
        background-color: #FFC107;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .site-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .site-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-3px);
    }
    
    .audio-player {
        width: 100%;
        margin: 20px 0;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
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
    </style>
    """, unsafe_allow_html=True)


def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def chat(query):
    response = LLM(query)
    st.session_state.chat_history.append({"role": "user", "content": query})
    st.session_state.chat_history.append({"role": "jarvis", "content": response})
    return response

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.is_listening = True
        st.session_state.mic_status = "listening"
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            try:
                query = r.recognize_google(audio, language="en-in")
                st.session_state.last_command = query
                return query
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            st.session_state.is_listening = False
            st.session_state.mic_status = "off"

def open_site(site_name, site_url):
    webbrowser.open(site_url)
    return f"Opening {site_name}..."

def get_time():
    hour = datetime.datetime.now().strftime("%H")
    minute = datetime.datetime.now().strftime("%M")
    return f"Current time is {hour}:{minute}"

# Sites configuration
sites = [
    {"name": "YouTube", "url": "https://www.youtube.com", "icon": "▶️"},
    {"name": "Wikipedia", "url": "https://www.wikipedia.com", "icon": "📚"},
    {"name": "Google", "url": "https://www.google.com", "icon": "🔍"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com", "icon": "💼"},
    {"name": "Instagram", "url": "https://www.instagram.com", "icon": "📸"},
    {"name": "Facebook", "url": "https://www.facebook.com", "icon": "👥"},
    {"name": "ChatGPT", "url": "https://chat.openai.com", "icon": "🤖"},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "icon": "🧠"},
    {"name": "TikTok", "url": "https://www.tiktok.com", "icon": "🎵"},
    {"name": "WhatsApp", "url": "https://web.whatsapp.com", "icon": "💬"}
]

# App header
st.markdown('<div class="header"><h1>🤖 Jarvis AI Assistant</h1><p>Your personal AI assistant powered by advanced language models</p></div>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 Conversation")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="message-user"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-jarvis"><b>Jarvis:</b> {message["content"]}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Voice input section
    st.subheader("🎤 Voice Commands")
    voice_col1, voice_col2 = st.columns([1, 3])
    
    with voice_col1:
        if st.button("🎤 Start Listening", key="listen_btn", use_container_width=True):
            st.session_state.mic_status = "processing"
            query = takeCommand()
            while "bye jarvis" not in query.lower():
                # todo: Add more sites
                sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                        ["google", "https://www.google.com"], ["linkdin", "https://www.linkdin.com"],
                        ["instagram", "https://www.instagram.com"], ["facebook", "https://www.facebook.com"],
                        ["chatgpt", "https://www.chatgpt.com"], ["deepseek", "https://www.chat.deepseek.com"],
                        ["tiktok", "https://www.tiktok.com"], ["whatsapp", "https://www.whatsapp.com"]]
                for site in sites:
                    if f"Open {site[0]}".lower() in query.lower():
                        say(f"Opening {site[0]} sir...")
                        webbrowser.open(site[1])
        
                if "open music" in query:
                    musicPath = "/Users/DELL 5300 A&I/OneDrive/Music/Aam Jahe Munde _ Parmish Verma feat Pardhaan _ Desi Crew _ Laddi Chahal(MP3_160K).mp3"
                    os.system(f"open {musicPath}")

                elif "the time" in query:
                    musicPath = "/Users/DELL 5300 A&I/OneDrive/Music/Aam Jahe Munde _ Parmish Verma feat Pardhaan _ Desi Crew _ Laddi Chahal(MP3_160K).mp3"
                    hour = datetime.datetime.now().strftime("%H")
                    min = datetime.datetime.now().strftime("%M")
                    say(f"Sir time is {hour} bajke {min} minutes")

                elif "bye Jarvis".lower() in query.lower():
                    exit()

                elif "reset chat".lower() in query.lower():
                    chatStr = ""

                elif "send email".lower() in query.lower():
                    from sendemail import send_email
                    send_email()
                else:
                    if query != "Some Error Occurred. Sorry from Jarvis":
                        print("Chatting...")
                        chat(query)

                    
    
    with voice_col2:
        status_indicator = st.empty()
        if st.session_state.mic_status == "off":
            status_indicator.markdown('<div class="status-indicator status-off"></div> Microphone: Off', unsafe_allow_html=True)
        elif st.session_state.mic_status == "listening":
            status_indicator.markdown('<div class="status-indicator status-processing"></div> Listening... Speak now', unsafe_allow_html=True)
        elif st.session_state.mic_status == "processing":
            status_indicator.markdown('<div class="status-indicator status-processing"></div> Processing command...', unsafe_allow_html=True)
        
        if st.session_state.last_command:
            st.info(f"Last command: {st.session_state.last_command}")
    
    st.divider()
    
    # Text input
    st.subheader("⌨️ Text Input")
    text_input = st.text_input("Type your command here:", placeholder="Ask Jarvis anything...")
    if st.button("Send Text Command", key="text_btn"):
        if text_input:
            response = chat(text_input)
            st.markdown(response)

with col2:
    st.subheader("🚀 Quick Actions")
    
    # Status panel
    with st.expander("🔍 System Status", expanded=True):
        st.markdown(f'<div class="status-indicator status-on"></div> Jarvis: Online', unsafe_allow_html=True)
        st.markdown(f'<div class="status-indicator status-{"on" if st.session_state.mic_status != "off" else "off"}"></div> Microphone: {"Active" if st.session_state.mic_status != "off" else "Inactive"}', unsafe_allow_html=True)
        
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        st.caption(f"System time: {current_time}")
        
    # Quick site access
    st.subheader("🌐 Quick Site Access")
    for site in sites:
        if st.button(f"{site['icon']} Open {site['name']}", key=f"site_{site['name']}", use_container_width=True):
            open_site(site['name'], site['url'])
            st.toast(f"Opening {site['name']}...", icon=site['icon'])


# Add footer
st.divider()
st.caption("Jarvis AI Assistant v1.0 | Created with Streamlit, Python, and ❤️")