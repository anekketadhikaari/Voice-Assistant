# Enhanced AI Voice Assistant

A modular PC AI voice assistant powered by LLaMA 3.1 8B with multiple TTS engines and comprehensive system control capabilities.

## Features

🎤 **Voice Recognition**: Advanced speech-to-text using Google Speech Recognition
🗣️ **Multi-Engine TTS**: Supports multiple text-to-speech engines (Coqui, ElevenLabs, Google TTS, Windows SAPI, eSpeak, pyttsx3)
🤖 **AI Integration**: LLaMA 3.1 8B for natural conversations and intelligent responses
💾 **Conversation Memory**: Maintains context across conversations
🖥️ **System Control**: Application launching, screenshot capture, battery monitoring
🌐 **Web Integration**: Website opening and Google search functionality
⚙️ **Modular Design**: Easy to extend and customize

## Prerequisites

### Required Software
- **Python 3.8+** (tested with Python 3.13.5)
- **Ollama** (for LLaMA 3.1 8B integration)
- **Microphone** and **speakers/headphones**

### Platform-Specific Requirements

**Windows:**
- Windows 10/11 with SAPI support
- Microsoft Visual C++ Build Tools (for PyAudio compilation)

**Linux:**
- ALSA development libraries: `sudo apt-get install libasound2-dev`
- eSpeak (optional): `sudo apt-get install espeak`

**macOS:**
- Xcode command line tools: `xcode-select --install`
- Homebrew for package management

## Installation
### 0. Install Dependencies

- Ensure Python 3.8+ is installed.
- Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
- Install and set up Ollama for LLaMA 3.1 8B:
    - [Ollama installation guide](https://ollama.com/download)
- Set up platform-specific dependencies as listed above.
- Connect a microphone and speakers/headphones to your PC.

### 1. Clone Repository

Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/Voice_assistant_project.git
cd Voice_assistant_project
```

### 2. Configure Environment

- Copy the example configuration file and edit as needed:
    ```bash
    cp config.example.yaml config.yaml
    ```
- Update API keys and settings for TTS engines and other integrations in `config.yaml`.

### 3. Download LLaMA Model

- Use Ollama to pull the LLaMA 3.1 8B model:
    ```bash
    ollama pull llama3:8b
    ```

### 4. Run the Voice Assistant

Start the assistant:
```bash
python main.py
```

### 5. (Optional) Test Installation

- Run the included test script to verify microphone and TTS setup:
    ```bash
    python test_setup.py
    ```

### 6. Troubleshooting

- Refer to the [FAQ](docs/FAQ.md) or open an issue for help with installation problems.
- Check platform-specific notes above for additional setup steps.
