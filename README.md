# 🤖 AI Avatar Therapist

This project brings to life an empathetic AI-powered avatar that acts as a supportive therapist. You can interact with it in two ways: through a real-time terminal conversation or a rich web interface. The AI listens to your voice, understands your words, and responds with a warm, gentle demeanor, complete with a synthesized voice and a lip-synced animated avatar.

The system is designed for fast, responsive interactions, leveraging a suite of powerful AI models for each part of the process: speech-to-text, language understanding, text-to-speech, and video generation. The web interface is optimized for a modern user experience, providing immediate audio feedback while the video generates in the background for a seamless conversation.

## ✨ Features

- **🗣️ Real-Time Voice Conversation**: Speak naturally and get an immediate vocal response from the AI.
- **💻 Two Modes of Operation**:
    1.  **Terminal Mode**: A streamlined, real-time conversational loop directly in your command line.
    2.  **Web App Mode**: A full-featured web interface with voice input, text input, and video/audio playback.
- **👩‍🦳 Empathetic AI Persona**: The AI is configured with a system prompt to act as a warm, wise, and gentle therapist, avoiding repetitive questions and offering thoughtful, concise support.
- **⚡ Optimized for Speed**:
    - Uses Meta's Llama 3 8B for fast and high-quality text generation.
    - Streams audio responses for low-latency feedback.
    - In the web app, audio plays immediately while the more time-intensive video generation happens in the background.
- **🎥 Dynamic Video Generation**: The AI's response is used to generate a lip-synced video of a digital avatar, bringing the character to life.
- **🔌 Modular Architecture**: The project is cleanly separated into modules for different functionalities (Ears, Brain, Voice, Face), making it easy to understand and extend.
- **🛠️ Health Checks & Setup Scripts**: Includes built-in tests to verify API keys and ensure all modules are working correctly before starting.

---

## 🔧 How It Works

The project is built around a core orchestration logic that connects several AI services:

1.  **👂 Module 1: Ears (Speech-to-Text)**
    - Uses **Deepgram's** Nova-2 model for highly accurate, real-time transcription of the user's voice from the microphone.

2.  **🧠 Module 2: Brain (Language Model)**
    - The transcribed text is sent to **Replicate** to run **Meta's Llama 3 8B Instruct** model.
    - A carefully crafted system prompt guides the AI to respond as an empathetic therapist.

3.  **🗣️ Module 3: Voice (Text-to-Speech)**
    - The AI's text response is sent to **ElevenLabs** to generate a natural, warm, and gentle voice.
    - In the terminal, the audio is streamed directly for instant playback.
    - In the web app, the audio is saved to a file for playback.

4.  **🙂 Module 4: Face (Video Generation)**
    - For the web app, the generated audio file and a source avatar image (`avatar.png`) are sent to the **SadTalker** model on **Replicate**.
    - SadTalker creates a lip-synced video of the avatar speaking the AI's response.

---

## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- Python 3.8 or higher
- A microphone connected to your computer
- API keys for the following services:
    - **Replicate**: For running the Llama 3 and SadTalker models.
    - **ElevenLabs**: For text-to-speech generation.
    - **Deepgram**: For speech-to-text transcription.

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>