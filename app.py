import streamlit as st
import random
import time
import cv2
import numpy as np
from PIL import Image
import io

# Simplified emotion detection for reliable demo
def detect_emotion(image_bytes):
    # For demo purposes, we'll use a weighted random selection
    # This ensures all emotions are shown but with different probabilities
    emotions = ["happy", "sad", "surprised", "angry", "neutral"]
    weights = [0.3, 0.2, 0.2, 0.15, 0.15]  # Higher weight for happy
    
    # Add some randomness based on image properties
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate basic image properties
    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    # Adjust weights based on image properties
    if brightness > 130:
        # Brighter image - increase happy and surprised weights
        weights = [0.4, 0.1, 0.3, 0.1, 0.1]
    elif brightness < 90:
        # Darker image - increase sad and angry weights
        weights = [0.1, 0.3, 0.1, 0.3, 0.2]
    
    # Select emotion based on weights
    selected_emotion = random.choices(emotions, weights=weights, k=1)[0]
    
    # Print debug information
    st.write(f"Debug - Brightness: {brightness:.2f}, Contrast: {contrast:.2f}")
    st.write(f"Debug - Selected emotion: {selected_emotion}")
    
    return selected_emotion

# Mapping for emotion to emoji and color
emotion_map = {
    "happy": {"emoji": "😊", "color": "#FFD700", "score": 5, "bg_color": "#2C3E50"},
    "sad": {"emoji": "😢", "color": "#4682B4", "score": 2, "bg_color": "#2C3E50"},
    "angry": {"emoji": "😠", "color": "#FF6347", "score": 1, "bg_color": "#2C3E50"},
    "neutral": {"emoji": "😐", "color": "#A9A9A9", "score": 3, "bg_color": "#2C3E50"},
    "surprised": {"emoji": "😲", "color": "#9370DB", "score": 4, "bg_color": "#2C3E50"}
}

# Initialize session state
if 'mood_score' not in st.session_state:
    st.session_state.mood_score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

# Set page config
st.set_page_config(page_title="MoodSnap!", page_icon="😊", layout="centered")

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    .mood-card {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 1px solid #333;
    }
    .stTextInput>div>div>input {
        background-color: #2C2C2C;
        color: white;
        border: 1px solid #444;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid #4CAF50;
    }
    .stMarkdown, p, h1, h2, h3, h4, h5, h6, span {
        color: #FFFFFF;
    }
    .stInfo {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #333;
    }
    .stSuccess {
        background-color: #1E1E1E;
        color: #4CAF50;
        border: 1px solid #333;
    }
    .stSpinner>div {
        border-top-color: #4CAF50 !important;
    }
    .debug-info {
        background-color: #2C3E50;
        color: #FFFFFF;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: monospace;
    }
    .camera-container {
        background-color: #2C3E50;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid #4CAF50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .mood-history {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .mood-icon {
        font-size: 30px;
        padding: 10px;
        background-color: #1E1E1E;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌈 MoodSnap!")
st.markdown("### Take a selfie and boost your mood! 🚀")

# Display score and streak
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="mood-card" style="background-color: #1E1E1E; border: 2px solid #FFD700;">
        <h2 style="text-align: center; color: #FFD700;">Score: {st.session_state.mood_score}</h2>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="mood-card" style="background-color: #1E1E1E; border: 2px solid #FF6347;">
        <h2 style="text-align: center; color: #FF6347;">Streak: {st.session_state.streak} 🔥</h2>
    </div>
    """, unsafe_allow_html=True)

# Camera input with improved visibility
st.markdown("""
<div class="camera-container">
    <h3 style="text-align: center; color: #4CAF50;">📸 Take your mood selfie!</h3>
</div>
""", unsafe_allow_html=True)
photo = st.camera_input("Smile, frown, or make any expression!")

if photo:
    with st.spinner("Analyzing your mood..."):
        detected_emotion = detect_emotion(photo.getvalue())
        emotion_data = emotion_map.get(detected_emotion, {"emoji": "😊", "color": "#FFD700", "score": 3, "bg_color": "#2C3E50"})
        
        # Update score and streak
        st.session_state.mood_score += emotion_data["score"]
        st.session_state.streak += 1
        st.session_state.mood_history.append(detected_emotion)
        
        # Display results
        st.markdown(f"""
        <div class="mood-card" style="background-color: {emotion_data['bg_color']}; border: 2px solid {emotion_data['color']};">
            <h2 style="text-align: center; color: {emotion_data['color']};">{emotion_data['emoji']} {detected_emotion.upper()} {emotion_data['emoji']}</h2>
            <p style="text-align: center; color: white;">You earned {emotion_data['score']} points!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display mood history
        if len(st.session_state.mood_history) > 1:
            st.markdown("### Your Mood Journey")
            mood_history_html = '<div class="mood-history">'
            for mood in st.session_state.mood_history[-5:]:
                emoji = emotion_map.get(mood, {"emoji": "😊"})["emoji"]
                color = emotion_map.get(mood, {"color": "#FFD700"})["color"]
                mood_history_html += f'<div class="mood-icon" style="border: 2px solid {color};">{emoji}</div>'
            mood_history_html += '</div>'
            st.markdown(mood_history_html, unsafe_allow_html=True)
        
        # Mood boosting activities
        st.markdown("### 🎮 Mood Boosting Activities")
        
        # Activity buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😄 Random Joke"):
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "What do you call a fake noodle? An impasta!",
                    "Why did the scarecrow win an award? Because he was outstanding in his field!",
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Why don't eggs tell jokes? They'd crack up!"
                ]
                st.markdown(f"""
                <div class="mood-card" style="background-color: #1E1E1E; border: 2px solid #FFD700;">
                    <p style="text-align: center; font-size: 20px; color: #FFD700;">{random.choice(jokes)}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🧘‍♀️ Breathing Exercise"):
                st.markdown("### Take a deep breath...")
                for i in range(3):
                    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>Breathe in... {i+1}</h2>", unsafe_allow_html=True)
                    time.sleep(2)
                st.success("Great job! Feeling better?")
        
        with col3:
            if st.button("💝 Self-Compliment"):
                st.markdown("### Give yourself a compliment!")
                compliment = st.text_input("I am...")
                if compliment:
                    st.success(f"You're right! You are {compliment}!")
else:
    st.info("👆 Click above to take a photo and start playing!") 