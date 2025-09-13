# --- OPTIMIZED main_orchestrator.py ---

import asyncio
import os
import time
import replicate
from dotenv import load_dotenv

import module1_ears      # STT module
import module3_voice     # Optimized TTS module

# Load environment variables from .env file
load_dotenv()
if not os.getenv("REPLICATE_API_TOKEN"):
    raise Exception("REPLICATE_API_TOKEN environment variable not set!")

# --- Optimized Llama 3 Model Configuration ---
LLAMA3_8B_INSTRUCT = "meta/meta-llama-3-8b-instruct"

def stream_llm_response(transcript: str):
    """
    OPTIMIZED: Generator function that streams response from Llama 3 with faster settings.
    """
    print(f"\n🧠 AI is thinking...")
    start_time = time.time()
    
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
        # Use optimized parameters for faster generation
        stream = replicate.stream(
            LLAMA3_8B_INSTRUCT,
            input={
                "prompt": transcript,
                "system_prompt": system_prompt,
                "max_new_tokens": 100,  # Reduced for faster responses
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50,
                "stop_sequences": ["\n\n"],  # Stop at double newlines
            },
        )
        
        response_started = False
        for event in stream:
            if not response_started:
                think_time = time.time() - start_time
                print(f"   -> Response started in {think_time:.1f}s")
                response_started = True
            yield str(event)
            
    except Exception as e:
        print(f"   -> Error generating response: {e}")
        yield "Sorry, I encountered an error. Please try again."

async def main_conversation_loop():
    """
    OPTIMIZED: Main loop with better performance and error handling.
    """
    print("🚀 AI Avatar Terminal Conversation - Optimized Version")
    print("💡 Tips:")
    print("   - Speak clearly and naturally")
    print("   - Press Ctrl+C to exit")
    print("   - Each conversation cycle is optimized for speed")
    print("="*60)
    
    conversation_count = 0
    
    while True:
        conversation_count += 1
        print(f"\n{'='*20} Conversation #{conversation_count} {'='*20}")
        
        try:
            # 1. Listen for user speech (Module 1)
            print("👂 Listening for your voice...")
            listen_start = time.time()
            
            user_transcript = await module1_ears.listen_for_speech()
            
            if user_transcript and user_transcript.strip():
                listen_time = time.time() - listen_start
                print(f"🗣️ You said: \"{user_transcript}\"")
                print(f"   -> Speech captured in {listen_time:.1f}s")
                
                # 2. Get streaming response from LLM (Module 2)
                print("🤖 AI responding...")
                
                llm_response_stream = stream_llm_response(user_transcript)
                
                # 3. Stream the response through voice (Module 3)
                module3_voice.speak_text_stream(llm_response_stream)
                
                total_time = time.time() - listen_start
                print(f"   -> Total conversation cycle: {total_time:.1f}s")
                
            else:
                print("❌ No clear speech detected. Please try again.")
                print("💡 Tip: Speak clearly and wait for the listening prompt")
                
        except KeyboardInterrupt:
            print("\n👋 Conversation ended by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing conversation... (Press Ctrl+C to exit)")
            continue
    
    print("\n✨ Thanks for chatting! Goodbye!")

def test_all_modules():
    """
    Test all modules to ensure they're working properly.
    """
    print("🧪 Testing all modules...")
    
    # Test API connections
    print("\n1. Testing Replicate API...")
    try:
        # A simple call to list models to verify the API key is working
        list(replicate.models.list())
        print("   ✅ Replicate API connected")
    except Exception as e:
        print(f"   ❌ Replicate API error: {e}")
        return False
    
    print("\n2. Testing ElevenLabs API...")
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("   ⚠️ ELEVENLABS_API_KEY not set - audio will be text-only")
    else:
        try:
            import module3_voice
            success = module3_voice.test_audio_generation()
            if success:
                print("   ✅ ElevenLabs API connected")
            else:
                print("   ❌ ElevenLabs API test failed")
        except Exception as e:
            print(f"   ❌ ElevenLabs API error: {e}")
    
    print("\n3. Testing Deepgram API...")
    if not os.getenv("DEEPGRAM_API_KEY"):
        print("   ❌ DEEPGRAM_API_KEY not set - speech recognition won't work")
        return False
    else:
        print("   ✅ DEEPGRAM_API_KEY configured")
    
    print("\n✅ Module testing complete!")
    return True

if __name__ == "__main__":
    try:
        print("🚀 AI Avatar Terminal - Starting Up...")
        
        # Test all modules first
        if not test_all_modules():
            print("\n❌ Some modules failed testing. Please check your API keys.")
            print("💡 Make sure your .env file contains:")
            print("   - REPLICATE_API_TOKEN")
            print("   - ELEVENLABS_API_KEY") 
            print("   - DEEPGRAM_API_KEY")
            exit(1)
        
        print("\n🎉 All systems ready! Starting conversation...")
        time.sleep(1)
        
        # Run the optimized conversation loop
        asyncio.run(main_conversation_loop())
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("🔧 Please check your configuration and try again")