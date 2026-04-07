# Important Note
*For the streamlit part it is not hostable on streamlit since my streamlit app requires a windows machine to run and streamlit uses linux, my project requires a windows machine since the tts is the windows one and all the alternatives like gtts are slow as well as paid. I will still try to fix it tho but it dint work the first time i tried to fix it and even opencv which is essential for my project doesnt work if i host on streamlit, i would have to switch to streamlit webrtc which is far more complex and would require me rewriting the entire camera capture logic.*



The below modules/commands are not supported to run on linux servers and rely on windows:
* pywin32
* win32com
* cv2
* webbrowser.open

# Echo Motion: AI-Powered Sign Language Assistant

Echo Motion is a real-time, gesture-controlled digital assistant (Jarvis) that bridges the gap between sign language and computer interaction. Using Computer Vision and Large Language Models (LLMs), it translates finger patterns into complex system commands, web searches, and natural language conversations.



---

## Key Features

* **32-Gesture Recognition:** Utilizes a complete binary finger-state map (Thumb to Pinky) for 32 unique commands.
* **Gemini AI Integration:** Uses `gemini-3-flash` to turn raw signs into natural, helpful sentences.
* **Web Dashboard:** A sleek, modern frontend built with **Streamlit** featuring live chat logs and real-time camera processing.
* **Threaded Audio (Jarvis):** Custom Windows SAPI integration that allows Jarvis to speak in the background without freezing the video feed.
* **Local Automation:**
    * **Entertainment:** Play any song on YouTube via `pywhatkit`.
    * **Information:** Fetch live headlines via News API or check the weather.
    * **Web Navigation:** Instant access to Google, Facebook, and YouTube.

---

## Tech Stack

* **Language:** Python 3.10+
* **Vision:** OpenCV, MediaPipe (Hand Landmarks)
* **AI:** Google Generative AI (Gemini API)
* **Frontend:** Streamlit
* **Audio:** Win32Com (SAPI.SpVoice)
* **APIs:** NewsAPI, Google GenAI

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ayaskant007/Echo-Motion.git
cd Echo-Motion
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Due to Windows Application Control policies, it is recommended to run the app using the Python module bypass:
```bash
python -m streamlit run "app.py"
```

---

## The Gesture Map (Hand Dictionary)

Echo Motion uses a binary state system `(Thumb, Index, Middle, Ring, Pinky)` where `1` is open and `0` is closed.

| Gesture Pattern | Command | Action |
| :--- | :--- | :--- |
| `(1, 1, 1, 1, 1)` | **Hello** | Jarvis greets the user |
| `(0, 0, 0, 0, 0)` | **Stop** | Shuts down the camera/app |
| `(1, 0, 0, 0, 0)` | **Google** | Opens google.com |
| `(1, 1, 0, 0, 0)` | **Play** | Triggers YouTube song search |
| `(0, 0, 0, 0, 1)` | **News** | Reads top headlines via News API |
| `(1, 1, 0, 0, 1)` | **Love** | "I Love You" sign |


