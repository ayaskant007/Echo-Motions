# Echo Motion: AI-Powered Sign Language Assistant
# USE PYTHON VERSION 3.12

Streamlit website url is: https://echomotionai.streamlit.app
IT SLEEPS VERY OFTEN SO LET ME KNOW IF IT SLEPT

A SIGN LANGUAGE/GESTURE BASED AI ASSISTANT that bridges the sign language/computer interaction gap is Echo Motion. It converts finger patterns to complex hands-free system commands, web searches and natural language conversations using Computer Vision and Large Language Models (LLMs).

## Tech Stack

* **Language:** Python 3.10+
* **Vision:** OpenCV, MediaPipe
* **AI:** Google Generative AI
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

### 2. Create a VENV
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

It uses a  binary state system `(Thumb, Index, Middle, Ring, Pinky)` where `1` is open and `0` is closed.

u can view the map its in the website on the sidebar 😋

## AI was just used for code debugging purposes.


