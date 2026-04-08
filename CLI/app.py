import pythoncom
import streamlit as st
import cv2
import mediapipe as mp
import win32com.client
import webbrowser
import time
import pywhatkit
import requests
from google import genai

st.set_page_config(page_title="Echo Motion AI", layout="wide", page_icon="🤖")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_gesture" not in st.session_state:
    st.session_state.last_gesture = None
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

with st.sidebar:
    st.title("Echo Motion Settings")

    st.markdown("### API Keys")
    gemini_key = st.text_input(
        "Gemini API Key", value="AIzaSyCQe9q8Y06qetk1AbFDIIGcSigkDPZT1Dw", type="password")
    news_key = st.text_input(
        "News API Key", value="5c0cc32bf90c4ad6a964f7695fa4e5cb", type="password")

    st.markdown("### Controls")
    if st.button("Start Camera" if not st.session_state.camera_active else "Stop Camera"):
        st.session_state.camera_active = not st.session_state.camera_active
        st.rerun()

    st.markdown("---")
    st.markdown("### Available Signs")
    st.markdown("""
    - ✌️ **Peace:** Peace
    - 🖐️ **Hello:** All Open
    - ✊ **Stop:** Fist
    - 🤘 **Surprise me:** Rock On
    - 🤏 **Google:** Thumb Only
    - 👌 **Youtube:** OK Sign
    """)

prompter = "You are a sign language translator. I will give you a list of words, please turn them into a natural sentence and help with the users needs, answer whatever they ask."


def log_chat(role, text):
    st.session_state.chat_history.append({"role": role, "text": text})


def speak(text):
    pythoncom.CoInitialize()
    log_chat("Jarvis", text)
    speaker.Speak(text, 1)


def processCommand(command, client):
    command = command.lower()
    log_chat("User", f"[Signed: {command}]")

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
        speak("Checking the weather...")
        webbrowser.open("https://weather.com")
    elif "surprise" in command:
        speak("Surprising You!")
        webbrowser.open("https://www.youtube.com/watch?v=QDia3e12czc")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif "stop" in command:
        speak("Stopping system.")
        st.session_state.camera_active = False
        st.rerun()
    elif "news" in command:
        speak("Fetching top headlines...")
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_key}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])[:3]
            for article in articles:
                speak(article['title'])
    else:
        speak(f"I heard {command}, connecting with Gemini...")
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompter + command,
            )
            speak(response.text)
        except Exception as e:
            speak(f"Error connecting to AI: {e}")


st.title("Echo Motion Dashboard")

col1, col2 = st.columns([2, 1])

gesture_map = {
    (0, 1, 0, 0, 0): "Point",
    (0, 1, 1, 0, 0): "Peace",
    (1, 1, 1, 1, 1): "Hello",
    (0, 0, 0, 0, 0): "Stop",
    (0, 0, 0, 0, 1): "News",
    (1, 0, 0, 0, 1): "Surprise",
    (0, 1, 1, 1, 0): "Weather",
    (1, 0, 0, 0, 0): "Google",
    (0, 1, 1, 1, 1): "Search",
    (1, 1, 0, 0, 0): "Play",
    (0, 0, 1, 1, 1): "Youtube",
    (1, 1, 0, 0, 1): "Love",
    (1, 1, 1, 0, 0): "Help",
    (0, 0, 0, 1, 1): "Facebook"
}

with col2:
    st.subheader("Live Chat")
    chat_container = st.container(height=500)
    for msg in st.session_state.chat_history:
        if msg["role"] == "Jarvis":
            chat_container.info(f"**Jarvis:** {msg['text']}")
        else:
            chat_container.success(f"**You:** {msg['text']}")

with col1:
    st.subheader("Camera Feed")
    frame_placeholder = st.empty()

    if st.session_state.camera_active:
        if not gemini_key:
            st.error("Please provide a Gemini API Key in the sidebar.")
            st.session_state.camera_active = False
            st.rerun()

        client = genai.Client(api_key=gemini_key)
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.6
        )

        cap = cv2.VideoCapture(0)

        while cap.isOpened() and st.session_state.camera_active:
            success, frame = cap.read()
            if not success:
                st.error("Failed to read from camera.")
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

                    if current_gesture != st.session_state.last_gesture:
                        if current_gesture in gesture_map:
                            gesture = gesture_map[current_gesture]

                            try:
                                processCommand(gesture, client)
                            except Exception as e:
                                log_chat(
                                    "System", f"Error processing command: {e}")

                        st.session_state.last_gesture = current_gesture

                    mp_drawing.draw_landmarks(
                        rgb_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            else:
                st.session_state.last_gesture = None

            frame_placeholder.image(
                rgb_frame, channels="RGB", use_container_width=True)

        cap.release()
    else:
        frame_placeholder.info(
            "Camera is currently off. Click 'Start Camera' in the sidebar.")
