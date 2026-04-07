import cv2
import mediapipe as mp
import speech_recognition as sr
import win32com.client
import webbrowser
import time
import pywhatkit
import requests
from google import genai

speaker = win32com.client.Dispatch("SAPI.SpVoice")
newsapi = "5c0cc32bf90c4ad6a964f7695fa4e5cb"
api_key = "AIzaSyCQe9q8Y06qetk1AbFDIIGcSigkDPZT1Dw"
client = genai.Client(api_key=api_key)
prompter = "You are a sign language translator. I will give you a list of words, please turn them into a natural sentence and help with the users needs, answer whatever they ask."


def speak(text):
    print(f"Jarvis: {text}")
    speaker.Speak(text, 1)


def processCommand(command):
    command = command.lower()
    if "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "hello" in command:
        speak("Hello! How can I help you?")
    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "weather" in command:
        webbrowser.open("https://weather.com")
    elif "surprise" in command:
        speak("Surprising You!")
        webbrowser.open("https://www.youtube.com/watch?v=QDia3e12czc")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif "stop" in command:
        exit()
    elif "news" in command.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])
    else:
        speak(
            f"I heard {command}, and I am connecting with Gemini to support you.")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompter + command,
        )
        speak(response.text)

gesture_map = {
    (0, 1, 0, 0, 0): "Point",
    (0, 1, 1, 0, 0): "Peace",
    (1, 1, 1, 1, 1): "Hello",
    (0, 0, 0, 0, 0): "Stop",
    (0, 0, 0, 0, 1): "News",
    (1, 0, 0, 0, 1): "Surprise me",
    (0, 1, 1, 1, 0): "Weather",


    (1, 0, 0, 0, 0): "Google",
    (0, 1, 1, 1, 1): "Search",
    (1, 1, 0, 0, 0): "Play",
    (0, 0, 1, 1, 1): "Youtube",
    (1, 1, 0, 0, 1): "Love",
    (1, 1, 1, 0, 0): "Help",
    (0, 0, 0, 1, 1): "Facebook"
}


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
last_gesture =  None

hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.9,
    min_tracking_confidence = 0.6
)

cap = cv2.VideoCapture(0)
speak("Jarvis is online.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[4]
            thumb_knuckle = hand_landmarks.landmark[2]
            index_tip = hand_landmarks.landmark[8]
            index_knuckle = hand_landmarks.landmark[6]
            middle_tip = hand_landmarks.landmark[12]
            middle_knuckle = hand_landmarks.landmark[10]
            ring_tip = hand_landmarks.landmark[16]
            ring_knuckle = hand_landmarks.landmark[14]
            pinky_tip = hand_landmarks.landmark[20]
            pinky_knuckle = hand_landmarks.landmark[18]
            
            fingers = []
            fingers.append(int(thumb_tip.x < thumb_knuckle.x))
            fingers.append(int(index_tip.y < index_knuckle.y))
            fingers.append(int(middle_tip.y < middle_knuckle.y))
            fingers.append(int(ring_tip.y < ring_knuckle.y))
            fingers.append(int(pinky_tip.y < pinky_knuckle.y))

            current_gesture = tuple(fingers)

            if current_gesture != last_gesture:
                if current_gesture in gesture_map:
                    gesture = gesture_map[current_gesture]


                    try:
                        word = gesture
                        print(f"Heard: {word}")
                        print("Jarvis Active... Speak now.")
                        command = gesture
                        processCommand(command)

                    except Exception as e:
                        print(f"Status: {e}")
                        continue
                last_gesture = current_gesture


            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        
    else:
        last_gesture = None


    cv2.imshow("Echo Motion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





cap.release()
cv2.destroyAllWindows()