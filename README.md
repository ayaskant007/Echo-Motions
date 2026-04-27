# Echo Motion: AI-Powered Sign Language Assistant
Streamlit website url is: https://echomotionai.streamlit.app
IT SLEEPS VERY OFTEN SO LET ME KNOW IF IT SLEPT

Echo Motion is a real-time, gesture-controlled digital assistant (Jarvis) that bridges the gap between sign language and computer interaction. Using Computer Vision and Large Language Models (LLMs), it translates finger patterns into complex system commands, web searches, and natural language conversations.



---

## Key Features

* **32-Gesture Recognition:** Utilizes a complete binary finger-state map (Thumb to Pinky) for 32 unique commands.
* **Gemini AI Integration:** Uses `gemini-3-flash` to turn raw signs into natural, helpful sentences.
* **Web Dashboard:** A v v cool frontend built with **Streamlit** featuring live chat logs and real-time camera processing.
* **Threaded Audio (Jarvis):** Custom Windows SAPI integration that allows Jarvis to speak in the background without freezing the video feed it doesnt work on the hosted streamlit website tho due to os limitations 🥀.
* **Local Automation:**
    * **Entertainment:** Play any song on YouTube via `pywhatkit` (a button appears on the web version due to server limitations 🥀 it doesnt auto open cuz it will open the site on the server itself not on the client's device 😭)
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
```bash
python -m streamlit run "app.py"
```
or just visit the goddamn link!!!
---

## The Gesture Map (Hand Dictionary)

Echo Motion uses a binary state system `(Thumb, Index, Middle, Ring, Pinky)` where `1` is open and `0` is closed.

u can view the map its in the website on the sidebar 😋

## AI was just used for code debugging purposes.


