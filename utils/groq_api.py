# utils/groq_api.py
# Placeholder for Groq API integration

import os
import requests
import dotenv
import numpy as np
import cv2
import random

# Load environment variables from .env file
dotenv.load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Simulated API endpoints (replace with actual endpoints when ready)
EMOTION_API_URL = "https://api.groq.com/emotion"  # Placeholder
AFFIRMATION_API_URL = "https://api.groq.com/affirmation"  # Placeholder

def detect_emotion(image_bytes):
    """Quick emotion detection for hackathon demo."""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate image features
    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    # Print debug information
    print(f"Image brightness: {brightness:.2f}, Image contrast: {contrast:.2f}")
    
    # Simple emotion detection based on image features
    # Using a more reliable approach with fewer dependencies on exact thresholds
    
    # For demo purposes, we'll use a combination of brightness and contrast
    # to determine the emotion, with some randomization to ensure variety
    
    # Use the image features as a seed for reproducibility
    random.seed(int(brightness * contrast))
    
    # Define emotion probabilities based on image features
    if brightness > 140:  # Bright image
        emotions = ["happy", "surprised", "neutral"]
        weights = [0.6, 0.3, 0.1]
    elif brightness < 100:  # Dark image
        emotions = ["sad", "neutral", "angry"]
        weights = [0.6, 0.3, 0.1]
    elif contrast > 50:  # High contrast
        emotions = ["angry", "surprised", "happy"]
        weights = [0.5, 0.3, 0.2]
    else:  # Low contrast
        emotions = ["neutral", "sad", "happy"]
        weights = [0.5, 0.3, 0.2]
    
    # Select emotion based on weights
    detected = random.choices(emotions, weights=weights, k=1)[0]
    
    # Reset random seed
    random.seed()
    
    return detected

def generate_affirmation(emotion):
    """Quick affirmations for hackathon demo."""
    affirmations = {
        "happy": "Your smile brightens everyone's day! 🌟",
        "sad": "Every cloud has a silver lining! ☀️",
        "angry": "Take a deep breath, you've got this! 💪",
        "neutral": "Stay balanced and mindful! 🧘‍♀️",
        "surprised": "Embrace the unexpected! ✨"
    }
    return affirmations.get(emotion, "You're doing great! 🎉") 