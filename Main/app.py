import platform
import threading
from urllib.parse import quote_plus

import numpy as np
import requests
import streamlit as st
from google import genai
from PIL import Image

cv2 = None
mp = None


def ensure_vision_libs():
    """Lazy-load OpenCV and MediaPipe only when camera is activated."""
    global cv2, mp
    if cv2 is None:
        import cv2 as _cv2
        cv2 = _cv2
    if mp is None:
        import mediapipe as _mp
        mp = _mp


try:
    import pywhatkit
except ImportError:
    pywhatkit = None

try:
    import pythoncom
    import win32com.client
except ImportError:
    pythoncom = None
    win32com = None


IS_WINDOWS = platform.system() == "Windows"
HAS_TTS = pythoncom is not None and win32com is not None


st.set_page_config(page_title="Echo Motion AI", layout="wide", page_icon="🤖")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_gesture" not in st.session_state:
    st.session_state.last_gesture = None
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False


with st.sidebar:
    st.title("Settings")
    
    st.markdown("### Security")
    gemini_key = st.text_input("Gemini API Key", value="", type="password")
    news_key = st.text_input("News API Key", value="", type="password")
    
    st.markdown("### Controls")
    if st.button("Start Camera" if not st.session_state.camera_active else "Stop Camera", use_container_width=True):
        st.session_state.camera_active = not st.session_state.camera_active
        st.rerun()

    if not IS_WINDOWS:
        st.info("Hosted mode uses browser camera capture and disables Windows-only speech output.")

    st.markdown("---")
    st.markdown("### Sign Dictionary")
    st.info("""
    ✌️ **Peace:** Peace \n
    🖐️ **Hello:** All Open \n
    ✊ **Stop:** Fist \n
    🤘 **Surprise:** Rock On \n
    🤏 **Google:** Thumb Only \n
    👌 **Youtube:** OK Sign
   \n # More Gestures below 
            
            \n (0 for thumb, 1 for index, 2 for middle, 3 for ring, 4 for pinky)
        
    (0, 1, 0, 0, 0): "Point",        Index Only \n
    (0, 1, 1, 0, 0): "Peace",        Index + Middle \n
    (1, 1, 1, 1, 1): "Hello",        All Open \n
    (0, 0, 0, 0, 0): "Stop",         Fist \n
    (0, 0, 0, 0, 1): "News",         Pinky Only \n
    (1, 0, 0, 0, 1): "Surprise",     Thumb + Pinky (Shaka) \n
    (0, 1, 1, 1, 0): "Weather",      Index, Middle, Ring \n
    (1, 0, 0, 0, 0): "Google",       Thumb Only \n
    (0, 1, 1, 1, 1): "Search",       4 Fingers (No Thumb) \n
    (1, 1, 0, 0, 0): "Play",         Thumb + Index (L-Shape) \n
    (0, 0, 1, 1, 1): "Youtube",      OK Sign (Middle, Ring, Pinky) \n
    (1, 1, 0, 0, 1): "Love",         I Love You (Thumb, Index, Pinky) \n
    (1, 1, 1, 0, 0): "Help",         Thumb, Index, Middle \n
    (0, 0, 0, 1, 1): "Facebook",     Ring + Pinky \n

    # Middle finger only  \n
    (0, 0, 1, 0, 0): "Cancel", \n
    # Ring finger only \n
    (0, 0, 0, 1, 0): "Next",\n
            \n
    (0, 1, 0, 1, 0): "Pause",        Index + Ring \n
    (0, 1, 0, 0, 1): "Agree",        Index + Pinky (Promise) \n
    (0, 0, 1, 1, 0): "Cut",          Middle + Ring \n
    (0, 0, 1, 0, 1): "Music",        Middle + Pinky \n
    (0, 1, 1, 0, 1): "Network",      Index + Middle + Pinky (Spider-man web) \n
    (0, 1, 0, 1, 1): "Wait",         Index + Ring + Pinky \n

    (1, 0, 1, 0, 0): "Quick",        Thumb + Middle (Snap) \n
    (1, 0, 0, 1, 0): "Call",         Thumb + Ring \n
    (1, 0, 1, 1, 0): "Calculate",    Thumb + Middle + Ring \n
    (1, 0, 0, 1, 1): "Phone",        Thumb + Ring + Pinky \n
    (1, 0, 1, 0, 1): "Party",        Thumb + Middle + Pinky \n
    (1, 0, 1, 1, 1): "Explain",      Thumb + Middle + Ring + Pinky \n

    (1, 1, 0, 1, 0): "Measure",      Thumb + Index + Ring \n
    (1, 1, 0, 1, 1): "Volume",       Thumb + Index + Ring + Pinky \n
    (1, 1, 1, 0, 1): "Email",        Thumb + Index + Middle + Pinky \n
    (1, 1, 1, 1, 0): "Almost"        Thumb + Index + Middle + Ring (No Pinky) \n
    """)

def update_chat_ui(placeholder):
    with placeholder.container():
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["text"])


def append_chat(role, text):
    st.session_state.chat_history.append({"role": role, "text": text})

def speak(text, chat_placeholder):
    append_chat("assistant", text)
    update_chat_ui(chat_placeholder)

    if not HAS_TTS:
        return

    def _speak_thread():
        pythoncom.CoInitialize()
        try:
            local_speaker = win32com.client.Dispatch("SAPI.SpVoice")
            local_speaker.Speak(text)
        finally:
            pythoncom.CoUninitialize()

    threading.Thread(target=_speak_thread, daemon=True).start()


def gesture_from_landmarks(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    thumb_knuckle = hand_landmarks.landmark[2]
    fingers = [
        int(thumb_tip.x < thumb_knuckle.x),
        int(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y),
        int(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y),
        int(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y),
        int(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y),
    ]
    return tuple(fingers)


def analyze_frame(rgb_frame, hands, mp_drawing, mp_hands):
    results = hands.process(rgb_frame)
    annotated_frame = rgb_frame.copy()
    detected_gesture = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            detected_gesture = gesture_from_landmarks(hand_landmarks)
            mp_drawing.draw_landmarks(annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            break

    return detected_gesture, annotated_frame, bool(results.multi_hand_landmarks)

def processCommand(command, client, chat_placeholder):
    command = command.lower()

    append_chat("user", f"[Signed: {command.capitalize()}]")
    update_chat_ui(chat_placeholder)

    if "google" in command:
        speak("Opening Google", chat_placeholder)
        st.link_button("Open Google", "https://google.com")
    elif "hello" in command:
        speak("Hello! How can I help you?", chat_placeholder)
    elif "facebook" in command:
        speak("Opening Facebook", chat_placeholder)
        st.link_button("Open Facebook", "https://facebook.com")
    elif "youtube" in command:
        speak("Opening Youtube", chat_placeholder)
        st.link_button("Open YouTube", "https://youtube.com")
    elif "weather" in command:
        speak("Checking the weather...", chat_placeholder)
        st.link_button("Open Weather", "https://weather.com")
    elif "surprise" in command:
        speak("Surprising You!", chat_placeholder)
        st.link_button("Watch Surprise Video", "https://www.youtube.com/watch?v=QDia3e12czc")
    elif "play" in command:
        song = command.replace("play", "").strip()
        if not song:
            speak("Say a song name after Play.", chat_placeholder)
            return

        speak(f"Searching YouTube for {song}", chat_placeholder)
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(song)}"
        st.link_button(f"Search YouTube for {song}", search_url)

        if IS_WINDOWS and pywhatkit is not None:
            try:
                pywhatkit.playonyt(song)
            except Exception:
                pass
    elif "stop" in command:
        speak("Stopping system.", chat_placeholder)
        st.session_state.camera_active = False
        st.rerun()
    elif "news" in command:
        if not news_key:
            speak("Please enter a News API key in the sidebar first.", chat_placeholder)
            return
        speak("Fetching top headlines...", chat_placeholder)
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_key}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])[:2]
                for article in articles:
                    speak(article['title'], chat_placeholder)
        except Exception:
            speak("Couldn't reach the news server.", chat_placeholder)
    else:
        if client is None:
            speak("Please enter a Gemini API key in the sidebar first.", chat_placeholder)
            return

        speak(f"Processing '{command}', connecting to Gemini...", chat_placeholder)
        try:
            prompter = "You are a sign language translator. I will give you a list of words, please turn them into a natural sentence and help with the users needs, answer whatever they ask."
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompter + command,
            )
            speak(response.text, chat_placeholder)
        except Exception as e:
            speak("I am having trouble connecting to my AI brain right now.", chat_placeholder)

st.title("Echo Motion Dashboard")

col1, col2 = st.columns([2, 1.2]) 

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
    (0, 0, 0, 1, 1): "Facebook",

    (0, 0, 1, 0, 0): "Cancel",
    (0, 0, 0, 1, 0): "Next",
    (0, 1, 0, 1, 0): "Pause",
    (0, 1, 0, 0, 1): "Agree",
    (0, 0, 1, 1, 0): "Cut",
    (0, 0, 1, 0, 1): "Music",
    (0, 1, 1, 0, 1): "Network",
    (0, 1, 0, 1, 1): "Wait",

    (1, 0, 1, 0, 0): "Quick",
    (1, 0, 0, 1, 0): "Call",
    (1, 0, 1, 1, 0): "Calculate",
    (1, 0, 0, 1, 1): "Phone",
    (1, 0, 1, 0, 1): "Party",
    (1, 0, 1, 1, 1): "Explain",

    (1, 1, 0, 1, 0): "Measure",
    (1, 1, 0, 1, 1): "Volume",
    (1, 1, 1, 0, 1): "Email",
    (1, 1, 1, 1, 0): "Almost"
}

with col2:
    st.subheader("Live Chat")
    chat_placeholder = st.empty()
    update_chat_ui(chat_placeholder)

with col1:
    st.subheader("Camera Feed")
    frame_placeholder = st.empty() 
    
    if st.session_state.camera_active:
        if not gemini_key:
            st.error("Please provide a Gemini API Key in the sidebar.")
            st.session_state.camera_active = False
            st.rerun()

        ensure_vision_libs()
        client = genai.Client(api_key=gemini_key)
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.98,
            min_tracking_confidence=0.7,
        )

        if IS_WINDOWS:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                frame_placeholder.error("Could not open the webcam. Try hosted mode or check camera permissions.")
            else:
                while cap.isOpened() and st.session_state.camera_active:
                    success, frame = cap.read()
                    if not success:
                        break

                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    current_gesture, annotated_frame, has_hand = analyze_frame(rgb_frame, hands, mp_drawing, mp_hands)

                    if has_hand:
                        if current_gesture != st.session_state.last_gesture and current_gesture in gesture_map:
                            gesture = gesture_map[current_gesture]
                            try:
                                processCommand(gesture, client, chat_placeholder)
                            except Exception:
                                pass
                            st.session_state.last_gesture = current_gesture
                    else:
                        st.session_state.last_gesture = None

                    frame_placeholder.image(annotated_frame, channels="RGB", use_container_width=True)

                cap.release()
        else:
            snapshot = st.camera_input("Capture a hand gesture from your browser camera")

            if snapshot is None:
                frame_placeholder.info("Capture a gesture to trigger a command. This hosted mode uses your browser camera, not the server webcam.")
            else:
                image = Image.open(snapshot).convert("RGB")
                rgb_frame = np.array(image)
                current_gesture, annotated_frame, has_hand = analyze_frame(rgb_frame, hands, mp_drawing, mp_hands)
                frame_placeholder.image(annotated_frame, channels="RGB", use_container_width=True)

                if has_hand and current_gesture in gesture_map and current_gesture != st.session_state.last_gesture:
                    gesture = gesture_map[current_gesture]
                    try:
                        processCommand(gesture, client, chat_placeholder)
                    except Exception:
                        pass
                    st.session_state.last_gesture = current_gesture
                elif not has_hand:
                    st.info("No hand was detected in the capture. Try again with better lighting and a single hand in frame.")
    else:
        frame_placeholder.info("Camera is currently off. Click 'Start Camera' in the sidebar.")