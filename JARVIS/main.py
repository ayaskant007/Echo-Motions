import speech_recognition as sr
import win32com.client
import webbrowser
import time
import pywhatkit
import requests
from google import genai



speaker = win32com.client.Dispatch("SAPI.SpVoice")
newsapi = ""
api_key = ""
client = genai.Client(api_key=api_key)
prompter = "You are an AI Voice Agent, provide a short and consise response to the user's needs ensure it contains the key details the user asks.  Command from the user: "

def speak(text):
    print(f"Jarvis: {text}")
    speaker.Speak(text)


def processCommand(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "hello" in command:
        speak("Hello! How can I help you?")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "what's the weather" in command:
        webbrowser.open("https://weather.com")
    elif "surprise me" in command:
        speak("Surprising You!")
        webbrowser.open("https://www.youtube.com/watch?v=QDia3e12czc")
    elif "play" in command:
        song = command.replace("play", "").strip()  
        speak(f"Playing {song}")    
        pywhatkit.playonyt(song)
    elif "stop" in command:
        exit()
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code ==200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'], time=100)
    else:
        speak(f"I heard {command}, and I am connecting with Gemini to support you.")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompter  + command,
        )
        speak(response.text)


if __name__ == "__main__":
    speak("Jarvis is online.")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=None)

            word = recognizer.recognize_google(audio).lower()
            print(f"Heard: {word}")

            if "jarvis" in word:
                speak("Yes!")
                time.sleep(1)

                with sr.Microphone() as source:
                    print("Jarvis Active... Speak now.")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(
                        source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"Status: {e}")
            continue
