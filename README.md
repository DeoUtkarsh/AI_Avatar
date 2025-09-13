# 🤖 AI Avatar Therapist

This project brings to life an empathetic AI-powered avatar that acts as a supportive therapist. You can interact with it in two ways: through a real-time terminal conversation or a rich web interface. The AI listens to your voice, understands your words, and responds with a warm, gentle demeanor, complete with a synthesized voice and a lip-synced animated avatar.

The system is designed for fast, responsive interactions, leveraging a suite of powerful AI models for each part of the process: speech-to-text, language understanding, text-to-speech, and video generation. The web interface is optimized for a modern user experience, providing immediate audio feedback while the video generates in the background for a seamless conversation.

## ✨ Features

- **🗣️ Real-Time Voice Conversation**: Speak naturally and get an immediate vocal response from the AI.

- **💻 Two Modes of Operation**:

1. **Terminal Mode**: A streamlined, real-time conversational loop directly in your command line.

2. **Web App Mode**: A full-featured web interface with voice input, text input, and video/audio playback.

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

1. **👂 Module 1: Ears (Speech-to-Text)**

- Uses **Deepgram's** Nova-2 model for highly accurate, real-time transcription of the user's voice from the microphone.

2. **🧠 Module 2: Brain (Language Model)**

- The transcribed text is sent to **Replicate** to run **Meta's Llama 3 8B Instruct** model.

- A carefully crafted system prompt guides the AI to respond as an empathetic therapist.

3. **🗣️ Module 3: Voice (Text-to-Speech)**

- The AI's text response is sent to **ElevenLabs** to generate a natural, warm, and gentle voice.

- In the terminal, the audio is streamed directly for instant playback.

- In the web app, the audio is saved to a file for playback.

4. **🙂 Module 4: Face (Video Generation)**

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

3. Install Dependencies

It’s recommended to use a virtual environment. The following commands will create a virtual environment, create the requirements.txt file, and install all necessary packages.

Copy and paste this entire block into your terminal:

# Create a virtual environment

python -m venv venv

# Activate the virtual environment

# On macOS/Linux:

source venv/bin/activate

# On Windows (Command Prompt/PowerShell):

# venv\Scripts\activate

# Create the requirements.txt file

cat << EOF > requirements.txt

python-dotenv

replicate

elevenlabs

deepgram-sdk

pyaudio

flask

EOF

# Install the packages

pip install -r requirements.txt

echo "✅ Setup complete! Now configure your .env file."```

*Note: After pasting the block, you may need to manually run the activation command for your specific operating system if the default one doesn't apply.*

### 4. Configure Environment Variables

Create a file named `.env` in the root directory of the project and add your API keys.

**`.env`** file:

REPLICATE_API_TOKEN="r8_..."
ELEVENLABS_API_KEY="..."
DEEPGRAM_API_KEY="..."

Replace the `...` with your actual API keys.

### 5. Add Your Avatar Image

For the web application to generate video, place a square portrait image of your desired avatar in the root directory and name it **`avatar.png`**. If you wish to use the provided image of the woman, save it from the project files and name it `avatar.png`.

---

## 🚀 Usage

You can run the project in two different modes.

### Mode 1: Terminal Conversation (Real-Time)

This mode provides a fast, voice-only, real-time chat experience directly in your terminal.

1. Open your terminal (ensure your virtual environment is activated).

2. Run the main orchestrator script:

```bash

python main_orchestrator.py

```

3. The script will first test all your API connections.

4. Once the tests pass, it will prompt "👂 Listening for your voice...".

5. Speak a sentence. The system will detect when you finish speaking.

6. The AI will process your words, and you will hear its response played back through your speakers.

7. The loop will continue until you press `Ctrl+C` to exit.

### Mode 2: Web Application (Video Avatar)

This mode launches a web server, allowing you to interact with the AI through a browser interface, complete with audio and video.

1. Open your terminal (ensure your virtual environment is activated).

2. Run the brain/web server script:

```bash

python module2_brain.py

```

3. Open your web browser and navigate to:

> **http://127.0.0.1:5000\*\*

4. **How to use the web interface:**

- **🎤 Voice Input**: Click "Start Talking", speak your message, and then click "Stop". Your message will appear in the text area.

- **⌨️ Text Input**: Alternatively, you can type your message directly into the "Your Message" text area.

- **➤ Send**: Click "Send Message" to submit your query to the AI.

- **🔊 Instant Audio**: The AI's audio response will play automatically (if auto-play is enabled).

- **🎬 Video Generation**: While the audio is playing, the video of the avatar will generate in the background and replace the audio player once it's ready.

---

## 🛠️ Configuration and Customization

- **AI Persona**: You can modify the `system_prompt` variable in `main_orchestrator.py` and `module2_brain.py` to change the AI's personality, role, or instructions.

- **Voice**: To change the AI's voice, you can change the `VOICE_ID` in `module3_voice.py`. You can find different voice IDs in your ElevenLabs account.

- **Avatar**: To change the avatar, simply replace the `avatar.png` file with a different image. For best results, use a clear, front-facing portrait with a neutral background.
