# Echo Motion: AI-Powered Sign Language Assistant

**Echo Motion** is a real-time, gesture-controlled digital assistant (Jarvis) that bridges the gap between sign language and computer interaction. Using Computer Vision and Large Language Models (LLMs), it translates finger patterns into complex system commands, web searches, and natural language conversations.



---

## Key Features

* **32-Gesture Recognition:** Utilizes a complete binary finger-state map (Thumb to Pinky) for 32 unique commands.
* **Gemini AI Integration:** Uses `gemini-1.5-flash` to turn raw signs into natural, helpful sentences.
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
git clone https://github.com/your-username/Echo-Motion.git
cd Echo-Motion
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
| *+ 26 more...* | *See source* | *Custom system triggers* |

---

## Tutorials & Development History

### Phase 1: The Local Script
Originally developed as a local Python script using a floating `cv2.imshow` window. This phase focused on perfecting the MediaPipe landmark logic and coordinate math.

### Phase 2: AI Brain Implementation
Integration of the Gemini API. Instead of just static "if/else" commands, Jarvis began understanding context, turning a string of signs into a fluid sentence.

### Phase 3: The Streamlit Migration
To solve the "Terminal-only" limitation, the project was migrated to a web interface. This involved:
* Implementing **Session State** to prevent Jarvis from "forgetting" the chat history on every frame refresh.
* Moving camera processing into a loop that updates a `st.empty()` container.

### Phase 4: Solving the Threading Crisis
The final hurdle was `win32com` crashing in a multi-threaded environment. We solved this by:
1.  Using `pythoncom.CoInitialize()` inside a background thread.
2.  Allowing the speaker to run as a `daemon` so the UI remains responsive.

---

## Contributing
Contributions are welcome! If you'd like to add more complex gestures (like motion-based signs), feel free to fork and submit a PR.

---
