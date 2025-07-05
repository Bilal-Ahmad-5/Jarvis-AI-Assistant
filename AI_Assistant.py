import streamlit as st
from langchain_groq import ChatGroq
from groq import Groq
import os
from dotenv import load_dotenv
import time
from langchain_tavily import TavilySearch
import win32com.client

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = str(os.getenv("GROQ_API_KEY"))
os.environ["TAVILY_API_KEY"] = str(os.getenv("TAVILY_API_KEY"))
# Initialize Groq client
client = Groq()


def LLM(query):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        # max_tokens=None,
        # reasoning_format="parsed",
        # timeout=None,
        # max_retries=2,
        # # other params...
    )
    prompt = "You are Jarvis AI Assistent, Answer according to user query: {query}."
    response = llm.invoke(prompt.format(query=query)).content
    print(response)
    return response

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# Page configuration
st.set_page_config(
    page_title=" AI Personal Assistant",
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

# App header
st.markdown('<div class="header"><h1>🤖 AI Assistant</h1></div>', unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

# settings
with col2:
    st.subheader("⚙️ Settings")
    model_name = st.selectbox(
        "AI Model",
        ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "meta-llama/llama-4-maverick-17b-128e-instruct", "deepseek-r1-distill-llama-70b", "distil-whisper-large-v3-en"],
        index=0
    )

    temperature = st.slider("Creativity", 0.0, 1.0, 0.3, 0.1)
    st.divider()
    
    st.subheader("ℹ️ About")
    st.info("This AI assistant uses Groq's lightning-fast LLMs and text-to-speech technology to provide interactive responses.")
    st.caption("Made with ❤️ using Streamlit, Groq, and LLaMA3")

# initialize chat history
Chat = ""

# Chat functions
def generate_response():
    global  Chat
    llm = ChatGroq(
        model=model_name,
        temperature=temperature,
    )
    query = st.text_input("Enter the Input!")
    # Custom prompt with user context
    st.write("Select Task")
    prompt = ""
    if st.button("Chat"):
        prompt = f"""
        You are Jarvis, an advanced AI assistant. Your responses should be:
        - Helpful and accurate
        - Concise but comprehensive
        - Friendly and engaging
        - Include emojis where appropriate
        
        Current time: {time.strftime("%Y-%m-%d %H:%M")}
        
        User query: {query}
        """
        

    if st.button("Summarization"):
        prompt = f"""Create a concise summary of the text below that captures the key points and main ideas. Follow these guidelines:
                1. Length: 1/4 of given text
                2. Focus: Identify and prioritize methodology and findings
                3. Style: Use academic and precise language
                4. Omit: Literature review details
                5. Structure: Abstract format with headings: Objective, Methods, Results, Conclusion

                Text to summarize: {query}

                Summary:"""

    
    if st.button("Text Classification"):
        if query:
            prompt = f"""This is the text for Classification:
                    {query}
                        
                    Detect the emotions expressed in the query by the user."""
        
    if st.button("Web search"):
        tool = TavilySearch(
            max_results=5,
            topic="general",
            # include_answer=False,
            # include_raw_content=False,
            # include_images=False,
            # include_image_descriptions=False,
            # search_depth="basic",
            # time_range="day",
            # include_domains=None,
            # exclude_domains=None
        )

        search = tool.invoke({"query": query})
        prompt = f"This is the search from web:{search} \n Also Use This to responed user query:{query} and Give user a well organized Response."
    response = llm.invoke(prompt).content
    Chat += f"User: {query} \n BilalGPT: {response}\n"
    return response 

# print chat
if Chat:
    print(Chat)
# Main chat interface
with col1:
    st.subheader("💬 Chat with AI")
        
    # User input
    response = generate_response()
    st.markdown(response)

    if st.button("Play 🔊"):
        say(response)
        if st.button("stop"):
            say("Thank You!I am done.")

