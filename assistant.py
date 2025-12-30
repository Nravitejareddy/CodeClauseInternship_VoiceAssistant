import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import requests
import re

# ---------------------- Initialization ----------------------
engine = pyttsx3.init()
WEATHER_API_KEY = "1e0acd7a07883f2c9da0a2879256309c"

# ---------------------- Helper Functions ----------------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

def display_and_speak(text, tag="assistant"):
    status_text.insert(tk.END, f"{text}\n", tag)
    status_text.see(tk.END)
    threading.Thread(target=speak, args=(text,), daemon=True).start()

def get_weather(city):
    if not city:
        return None
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return None
        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C"
    except:
        return None

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it caught a virus!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the math book sad? Because it had too many problems.",
        "Why did the computer show up at work late? It had a hard drive.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why did the AI go to therapy? Too many deep thoughts."
    ]
    return random.choice(jokes)

# ---------------------- Command Processing ----------------------
def process_command(command):
    display_and_speak(f"\n>> {command}", "user")
    command_lower = command.lower()
    response = ""

    if "time" in command_lower:
        response = f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif "date" in command_lower:
        response = f"Today's date is {datetime.datetime.now().strftime('%d %B %Y')}"
    elif "wikipedia" in command_lower:
        topic = command_lower.replace("wikipedia", "").strip()
        if topic:
            try:
                response = wikipedia.summary(topic, sentences=2)
            except:
                response = "Wikipedia lookup failed."
        else:
            response = "Please specify a Wikipedia topic."
    elif command_lower.startswith("search"):
        query = command_lower.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response = f"Searching for {query}..."
    elif "google" in command_lower:
        webbrowser.open("https://www.google.com")
        response = "Opening Google..."
    elif "youtube" in command_lower:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube..."
    elif "gmail" in command_lower or "email" in command_lower:
        webbrowser.open("https://mail.google.com")
        response = "Opening Gmail..."
    elif any(k in command_lower for k in ["chatgpt", "chat gpt", "charge gpt", "gpt"]):
        webbrowser.open("https://chat.openai.com")
        response = "Opening ChatGPT..."
    elif any(k in command_lower for k in ["notes", "keep"]):
        webbrowser.open("https://keep.google.com")
        response = "Opening Google Notes..."
    elif "meet" in command_lower:
        webbrowser.open("https://meet.google.com")
        response = "Opening Google Meet..."
    elif "calendar" in command_lower:
        webbrowser.open("https://calendar.google.com")
        response = "Opening Google Calendar..."
    elif "maps" in command_lower:
        webbrowser.open("https://maps.google.com")
        response = "Opening Google Maps..."
    elif "drive" in command_lower:
        webbrowser.open("https://drive.google.com")
        response = "Opening Google Drive..."
    elif "joke" in command_lower:
        response = tell_joke()
    elif "weather" in command_lower:
        city_match = re.search(r'weather in ([a-zA-Z\s]+)', command_lower)
        city = city_match.group(1).strip() if city_match else None
        response = get_weather(city) or "Could not retrieve weather information."
    elif "who created you" in command_lower or "created you" in command_lower:
        response = (
            "I was created by Nagella Ravi Teja Reddy, "
            "as a Golden Project for the CodeClause Internship, "
            "on 30th December 2025. "
            "Built with vision, dedication, and passion for intelligent systems."
        )
    else:
        response = "Command not recognized."

    display_and_speak(response, "assistant")

# ---------------------- Listening ----------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        display_and_speak("\nListening...", "status")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=6)
            process_command(r.recognize_google(audio))
        except:
            display_and_speak("Could not understand audio", "assistant")

def listen_thread():
    threading.Thread(target=listen, daemon=True).start()

# ---------------------- GUI ----------------------
root = tk.Tk()
root.title("CodeClause Voice Assistant")
root.geometry("650x650")
root.configure(bg="#0f2027")

status_text = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=75, height=28,
    bg="#1c1c1c", fg="white"
)
status_text.pack(pady=10)

status_text.tag_config("user", foreground="#66ccff")
status_text.tag_config("assistant", foreground="#66ff66")
status_text.tag_config("status", foreground="#ffff66")

tk.Button(
    root, text="🎤 Click to Speak",
    bg="#4CAF50", fg="white",
    width=25, height=2,
    command=listen_thread
).pack(pady=10)

root.mainloop()
