import asyncio
import os
import sys
import threading
from dotenv import load_dotenv
import pyaudio
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    LiveResultResponse,
)

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# --- Configuration ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)

class Microphone:
    def __init__(self, callback, loop):
        self.callback = callback
        self.loop = loop
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        self.is_running = False
        self.thread = None

    def start(self):
        print("\n🎤 Microphone stream started. Speak now! (Press Ctrl+C to stop testing)\n")
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self.is_running and self.stream.is_active():
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                asyncio.run_coroutine_threadsafe(self.callback(data), self.loop)
            except IOError:
                break

    def finish(self):
        if self.is_running:
            self.is_running = False
            if self.thread:
                self.thread.join()
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            print("🎤 Microphone stream finished.")

# This is the main function that will be imported by our orchestrator
async def listen_for_speech():
    """Listens for a single utterance and returns the final transcript."""
    transcription_complete = asyncio.Event()
    final_transcript = ""
    transcript_collector = TranscriptCollector()
    microphone = None
    dg_connection = None

    try:
        config = DeepgramClientOptions(verbose=0)
        deepgram = DeepgramClient(DEEPGRAM_API_KEY, config)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        async def on_message(self, result: LiveResultResponse, **kwargs):
            nonlocal final_transcript
            sentence = result.channel.alternatives[0].transcript
            if not sentence:
                return

            if result.is_final:
                transcript_collector.add_part(sentence)
                full_transcript = transcript_collector.get_full_transcript()
                sys.stdout.write(f"\r{' ' * 80}\r")
                sys.stdout.flush()
                print(f"Current Sentence: {full_transcript}")

                if result.speech_final:
                    final_transcript = full_transcript
                    transcript_collector.reset()
                    transcription_complete.set() # Signal that we're done
            else:
                sys.stdout.write(f"\r Interim: {sentence.ljust(80)}")
                sys.stdout.flush()

        async def on_error(self, error, **kwargs):
            print(f"\n\nError: {error}\n\n")
            transcription_complete.set()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2", language="en-US", smart_format=True,
            encoding="linear16", channels=1, sample_rate=RATE,
            interim_results=True, endpointing="500", utterance_end_ms="1000",
        )

        await dg_connection.start(options)
        
        loop = asyncio.get_running_loop()
        microphone = Microphone(dg_connection.send, loop)
        microphone.start()

        await transcription_complete.wait()
        return final_transcript

    except Exception as e:
        print(f"An unexpected error in transcription: {e}")
        return None
    finally:
        if microphone:
            microphone.finish()
        if dg_connection:
            await dg_connection.finish()

# This block allows you to run this script by itself for testing Module 1
if __name__ == "__main__":
    if DEEPGRAM_API_KEY is None:
        print("Please set your DEEPGRAM_API_KEY environment variable.")
        sys.exit(1)
        
    try:
        transcript = asyncio.run(listen_for_speech())
        if transcript:
            print(f"\n✅ Standalone Test - Final Transcript: {transcript}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
