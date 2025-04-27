# MoodSnap!

A fun hackathon web app that snaps your photo, detects your mood using Groq's API, and gives you a positive affirmation with a matching sound and emoji!

## Features
- Snap a webcam photo
- Detect your emotion (via Groq API or simulation)
- Get a positive affirmation (Groq LLM)
- Play a mood-matching sound
- See your emotion, affirmation, and a cute emoji or GIF

## Tech Stack
- [Streamlit](https://streamlit.io/) for the frontend
- Modular Python backend (utils for API calls)
- `.env` for API keys
- Static folder for sounds/images

## Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your Groq API key:**
   - Copy `.env.example` to `.env` and fill in your key.
4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Folder Structure
```
├── app.py
├── requirements.txt
├── .env.example
├── utils/
│   └── groq_api.py
├── static/
│   ├── sounds/
│   └── images/
```

---

*Hackathon-ready. Fast, fun, and simple!*
