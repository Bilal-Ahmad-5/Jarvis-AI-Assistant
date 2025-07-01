import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import streamlit as st
import win32com.client
from llm import LLM

chatStr = ""

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def chat(query):
    global chatStr
    response = LLM(query)
    say(response)
    chatStr += f"Bilal:{query}\njarvis{response}\n"
    return response


#take command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            say("Some Error Occurred. Sorry from Jarvis")
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("hey Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
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

