from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv() 

os.environ["GROQ_API_KEY"] = str(os.getenv("GROQ_API_KEY"))
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))

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
    prompt = "You are Jarvis AI Assistent, Give a very short and concise answer to the user according to user query: {query}. /n Response must be smaller than 50 words"
    response = llm.invoke(prompt.format(query=query)).content
    print(response)
    return response
