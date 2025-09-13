# --- OPTIMIZED and CORRECTED module2_brain.py ---

import os
import replicate
from flask import Flask, request, jsonify, render_template, url_for
from dotenv import load_dotenv
import module3_voice
import module4_face
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import glob

# Load environment variables
load_dotenv()
if not os.getenv("REPLICATE_API_TOKEN"):
    raise Exception("REPLICATE_API_TOKEN environment variable not set!")

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='static', static_url_path='/static')
if not os.path.exists('static'):
    os.makedirs('static')

# --- Llama 3 Model Configuration ---
LLAMA3_8B_INSTRUCT = "meta/meta-llama-3-8b-instruct"

# --- Avatar Configuration ---
AVATAR_IMAGE_PATH = "avatar.png"

# Thread pool for parallel processing
executor = ThreadPoolExecutor(max_workers=2)

def cleanup_old_files():
    """Clean up old files in background"""
    try:
        if os.path.exists('static'):
            files = glob.glob(os.path.join('static', 'response_*.mp3'))
            if len(files) > 10:
                files.sort(key=os.path.getmtime)
                for old_file in files[:-10]:
                    try:
                        os.remove(old_file)
                    except Exception:
                        pass
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    """
    OPTIMIZED and CORRECTED API endpoint with better performance and error handling.
    """
    print("🧠 Brain (Web UI) received a request...")
    
    if not request.json or 'transcript' not in request.json:
        return jsonify({'error': 'Bad Request: transcript key is missing'}), 400
    
    user_transcript = request.json['transcript']
    if not user_transcript:
        return jsonify({'error': 'Bad Request: transcript cannot be empty'}), 400
    
    print(f"   -> User said: \"{user_transcript}\"")

    # --- MODIFIED SYSTEM PROMPT ---
    system_prompt = (
        "You are an experienced therapist with a warm, empathetic, and gentle demeanor, like a wise older woman. "
        "Your goal is to provide a calm and supportive space. Listen carefully to the user. "
        "IMPORTANT: You must vary your conversational patterns and avoid asking 'Can you tell me more' repeatedly. "
        "Instead, you can: "
        "1. Offer a gentle, comforting observation (e.g., 'That sounds incredibly difficult to carry.'). "
        "2. Ask a specific, clarifying question about a detail (e.g., 'When you say you feel unwell, is it more of a physical feeling or an emotional one?'). "
        "3. Share a brief, reassuring thought (e.g., 'It's alright to not have all the answers right now.'). "
        "Keep your responses concise and thoughtful, typically 1-2 sentences."
    )
    
    try:
        print("   -> 🤔 Thinking...")
        start_time = time.time()
        
        # Get AI response with optimized parameters
        output = replicate.run(
            LLAMA3_8B_INSTRUCT,
            input={
                "prompt": user_transcript,
                "system_prompt": system_prompt,
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        )
        
        full_response = "".join(output)
        ai_time = time.time() - start_time
        print(f"   -> 💭 AI responded in {ai_time:.1f}s: \"{full_response}\"")

        if not full_response:
            return jsonify({'error': 'AI generated empty response'}), 500

        audio_filename = f"response_{hash(full_response)}.mp3"
        audio_filepath = os.path.join(app.static_folder, audio_filename)
        audio_url = url_for('static', filename=audio_filename)
        video_url = None
        
        if not os.path.exists(audio_filepath):
            print("   -> 🔊 Generating audio...")
            audio_start = time.time()
            module3_voice.text_to_audio_file(full_response, audio_filepath)
            audio_time = time.time() - audio_start
            print(f"   -> 🔊 Audio generated in {audio_time:.1f}s")
        else:
            print("   -> 🔊 Using cached audio file")

        if os.path.exists(AVATAR_IMAGE_PATH):
            print("   -> 🎬 Starting video generation...")
            video_start = time.time()
            video_output = module4_face.generate_lip_sync_video(AVATAR_IMAGE_PATH, audio_filepath)
            
            if video_output:
                video_url = str(video_output) # FIX: Convert object to string
                video_time = time.time() - video_start
                print(f"   -> 🎬 Video generated in {video_time:.1f}s")
            else:
                video_url = None
                print("   -> 🎬 Video generation failed, audio-only response")
        else:
            print(f"   -> ⚠️  Avatar image not found at {AVATAR_IMAGE_PATH}")

        executor.submit(cleanup_old_files)
        total_time = time.time() - start_time
        print(f"   -> ✅ Total processing time: {total_time:.1f}s")

        return jsonify({
            'response': full_response,
            'audio_url': audio_url,
            'video_url': video_url,
            'processing_time': round(total_time, 1)
        })

    except Exception as e:
        print(f"   -> ❌ Error occurred: {e}")
        return jsonify({
            'error': f'Processing error: {str(e)}',
            'response': 'Sorry, I encountered an error processing your request.'
        }), 500

@app.route('/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'avatar_available': os.path.exists(AVATAR_IMAGE_PATH),
        'static_files': len([f for f in os.listdir('static') if f.endswith('.mp3')]) if os.path.exists('static') else 0
    })

if __name__ == '__main__':
    print("🤖 Module 2 (Brain for Web App) is running at http://127.0.0.1:5000")
    if os.path.exists(AVATAR_IMAGE_PATH):
        print(f"   ✅ Avatar image found: {AVATAR_IMAGE_PATH}")
    else:
        print(f"   ⚠️  Avatar image missing: {AVATAR_IMAGE_PATH}")
        print("   💡 Add an avatar.png file for video generation")
    
    missing_keys = []
    if not os.getenv("REPLICATE_API_TOKEN"):
        missing_keys.append("REPLICATE_API_TOKEN")
    if not os.getenv("ELEVENLABS_API_KEY"):
        missing_keys.append("ELEVENLABS_API_KEY")
    
    if missing_keys:
        print(f"   ⚠️  Missing API keys: {', '.join(missing_keys)}")
    else:
        print("   ✅ All API keys configured")
    
    print("   🚀 Starting optimized server...")
    app.run(debug=True, port=5000, threaded=True)