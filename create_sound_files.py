import wave
import struct
import os

def create_simple_sound(filename, frequency=440, duration=1):
    """Create a simple sound file with a given frequency."""
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Audio file parameters
    sample_rate = 44100
    amplitude = 32767  # Max amplitude for 16-bit audio
    num_samples = int(sample_rate * duration)
    
    # Create the audio data
    audio_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        value = int(amplitude * 0.5 * (1 + i/num_samples))  # Simple amplitude modulation
        audio_data.append(value)
    
    # Create the WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Write the audio data
        for value in audio_data:
            wav_file.writeframes(struct.pack('h', value))

# Create sound files for each emotion
emotions = ["happy", "sad", "angry", "neutral", "surprised"]
frequencies = [440, 220, 880, 330, 550]  # Different frequencies for each emotion

for emotion, freq in zip(emotions, frequencies):
    filename = f"static/sounds/{emotion}.wav"
    create_simple_sound(filename, frequency=freq)
    print(f"Created {filename}")

print("All sound files created successfully!") 