Meeting Assistant 🤖

Meeting Assistant is an AI-powered productivity tool designed to enhance your virtual meetings and daily workflow. Built with Streamlit and powered by Groq's lightning-fast LLMs, this application provides intelligent conversation, voice commands, email automation, and more - all in one place.

Key Features ✨

- AI-Powered Chat: Intelligent conversations using Groq's LLama3-70b model
- Voice Commands: Interact hands-free with microphone support
- Email Automation: Send professional emails with AI-generated content
- Web Search Integration: Get real-time information with Tavily search
- Multi-Page Interface: Organized workflow with dedicated sections
- ext-to-Speech: Hear responses with built-in audio output

Installation 🛠️
Clone the repository:

bash
git clone https://github.com/yourusername/meeting-assistant.git
cd meeting-assistant
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
Install dependencies:

bash
pip install -r requirements.txt
Create a .env file with your API keys:

env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_app_password
Usage 🚀
Run the application:

bash
streamlit run Home.py
Application Sections:
AI Assistant 💬

Chat with the AI using text input

-Perform summarization, text classification, and web searches
-Listen to responses with text-to-speech

Voice Assistant 🎤

- Interact with Jarvis using voice commands
- Open websites with voice prompts
- Send emails and perform system tasks
- 
Email Sender ✉️

- Generate professional emails with AI
- Send to multiple recipients
- Add attachments to your messages

Project Structure 📁

meeting-assistant/
├── Home.py                 # Main navigation hub
├── AI_Assistant.py         # Chat interface with AI
├── Jarvis_AI_Agent.py      # Voice command interface
├── Send_Mail.py            # Email automation tool
├── requirements.txt        # Dependencies
├── .env.example            # Environment template
├── README.md               # Project documentation
└── assets/                 # Media resources

Dependencies 📦

- Streamlit
- Groq SDK
- LangChain Groq
- LangChain Tavily
- python-dotenv
- pywin32 (Windows only)
- SpeechRecognition
- smtplib

Configuration ⚙️
Customize the application in the following ways:

- AI Models: Choose between different LLMs in the settings panel
- Creativity: Adjust the temperature slider for more creative responses
- uick Sites: Customize the website shortcuts in Jarvis_AI_Agent.py
- mail Templates: Modify the prompt in Send_Mail.py for different email styles

License 📄
This project is licensed under the MIT License - see the LICENSE file for details.
