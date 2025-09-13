# --- OPTIMIZED module3_voice.py ---

import os
import time
from elevenlabs import stream, save
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- ElevenLabs Client Initialization ---
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# --- MODIFIED VOICE SETTINGS FOR GRANDMA PERSONA ---

# Using "Matilda", a voice confirmed to be on your account.
VOICE_ID = "XrExE9yKIg1WjnnlVkGX" 

# --- FIX: Reverting to the multilingual model which is confirmed to be on your account. ---
MODEL_ID = "eleven_multilingual_v2"

def speak_text_stream(text_stream):
    """
    OPTIMIZED: Takes a generator of text chunks and streams the audio directly.
    """
    if not ELEVENLABS_API_KEY:
        print("Warning: ELEVENLABS_API_KEY not set. Skipping audio playback.")
        full_text = "".join(text for text in text_stream)
        print(f"🤖 AI Says (audio skipped): {full_text}")
        return

    print("🔊 Voice module streaming audio...")
    start_time = time.time()
    
    try:
        audio_stream = client.text_to_speech.stream(
            text=text_stream,
            voice=VOICE_ID,
            model=MODEL_ID,
        )
        
        stream(audio_stream)
        
        stream_time = time.time() - start_time
        print(f"   -> Audio streamed in {stream_time:.1f}s")
        
    except Exception as e:
        print(f"   -> Audio streaming error: {e}")
        full_text = "".join(text for text in text_stream)
        print(f"🤖 AI Says (audio failed): {full_text}")

def text_to_audio_file(text: str, file_path: str):
    """
    OPTIMIZED: Converts text to audio file with settings for the grandma persona.
    """
    if not ELEVENLABS_API_KEY:
        print("Warning: ELEVENLABS_API_KEY not set. Cannot generate audio file.")
        return False

    if not text or not text.strip():
        print("Warning: Empty text provided. Cannot generate audio.")
        return False

    print(f"🔊 Voice module generating audio file at {file_path}...")
    start_time = time.time()
    
    try:
        if os.path.exists(file_path):
            print("   -> Using cached audio file")
            return True
        
        audio = client.text_to_speech.convert(
            text=text.strip(),
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            # Fine-tuned settings for a slower, softer, calmer tone
            voice_settings={
                "stability": 0.3,
                "similarity_boost": 0.75, 
                "style": 0.0,
                "use_speaker_boost": True 
            }
        )

        save(audio, file_path)
        
        generation_time = time.time() - start_time
        print(f"   -> Audio file saved in {generation_time:.1f}s")
        
        if not (os.path.exists(file_path) and os.path.getsize(file_path) > 0):
             print("   -> Error: Audio file was not created properly after generation.")
             return False
        return True
            
    except Exception as e:
        print(f"   -> Audio generation error: {e}")
        return False

# (The rest of the file remains the same)

def test_audio_generation():
    test_text = "Beta, have you eaten? You sound tired."
    test_file = "test_audio_grandma.mp3"
    
    print("Testing 'Grandma' persona audio generation...")
    success = text_to_audio_file(test_text, test_file)
    
    if success:
        print("✅ Audio generation test passed!")
        if os.path.exists(test_file):
            print(f"   -> Test file saved at: {os.path.abspath(test_file)}")
    else:
        print("❌ Audio generation test failed!")
    
    return success

if __name__ == '__main__':
    if not ELEVENLABS_API_KEY:
        print("❌ ELEVENLABS_API_KEY not found.")
        exit(1)
    test_audio_generation()