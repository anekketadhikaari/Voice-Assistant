"""
Configuration file for AI Voice Assistant
"""

# TTS Engine Settings
TTS_CONFIG = {
    'engine': 'auto',  # Options: 'auto', 'coqui', 'elevenlabs', 'google', 'windows', 'espeak', 'pyttsx3'
    'rate': 140,       # Speech rate (words per minute)
    'volume': 1.0,     # Volume level (0.0 to 1.0)
    'voice_preference': 'male'  # 'male', 'female', or 'auto'
}

# LLaMA Configuration
LLAMA_CONFIG = {
    'model_name': 'llama3.1:8b',
    'host_url': 'http://localhost:11434',
    'temperature': 0.7,
    'max_tokens': 200,
    'timeout': 30
}

# Speech Recognition Settings
SPEECH_CONFIG = {
    'timeout': 10,           # Listening timeout in seconds
    'phrase_time_limit': 10, # Maximum phrase duration
    'energy_threshold': 4000, # Microphone sensitivity
    'dynamic_energy_threshold': True
}

# Memory Settings
MEMORY_CONFIG = {
    'max_conversation_size': 10,  # Number of exchanges to remember
    'save_conversations': False,   # Save to file (future feature)
    'context_window': 5           # Messages to include in AI context
}

# Application Shortcuts
APPLICATIONS = {
    'chrome': ['chrome.exe', 'google-chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
    'brave': ['brave.exe', 'brave-browser', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'],
    'firefox': ['firefox.exe', 'firefox', '/Applications/Firefox.app/Contents/MacOS/firefox'],
    'notepad': ['notepad.exe', 'gedit', '/Applications/TextEdit.app/Contents/MacOS/TextEdit'],
    'calculator': ['calc.exe', 'gnome-calculator', '/Applications/Calculator.app/Contents/MacOS/Calculator'],
    'spotify': ['spotify.exe', 'spotify', '/Applications/Spotify.app/Contents/MacOS/Spotify'],
    'discord': ['Discord.exe', 'discord', '/Applications/Discord.app/Contents/MacOS/Discord'],
    'vscode': ['code.exe', 'code', '/Applications/Visual Studio Code.app/Contents/MacOS/Electron']
}

# Website Shortcuts
WEBSITES = {
    'youtube': 'https://www.youtube.com',
    'instagram': 'https://www.instagram.com',
    'linkedin': 'https://www.linkedin.com',
    'gmail': 'https://mail.google.com',
    'facebook': 'https://www.facebook.com',
    'twitter': 'https://twitter.com',
    'reddit': 'https://www.reddit.com',
    'netflix': 'https://www.netflix.com',
    'spotify': 'https://open.spotify.com',
    'github': 'https://github.com',
    'discord': 'https://discord.com',
    'whatsapp': 'https://web.whatsapp.com',
    'chatgpt': 'https://chat.openai.com'
}

# Default Responses (when LLaMA is unavailable)
Default_RESPONSES = {
    'greeting': [
        "Hello! I'm your AI assistant. How can I help you today?",
        "Hi there! Great to hear from you. What can I do for you?",
        "Hey! I'm here and ready to assist. What would you like to do?"
    ],
    'how_are_you': [
        "I'm doing great! All systems are running smoothly and I'm ready to help.",
        "I'm functioning perfectly, thank you for asking! How are you doing?",
        "I'm excellent! Everything is working well. How can I assist you today?"
    ],
    'capabilities': [
        "I can open applications, browse websites, search the web, answer questions, and have conversations with you!",
        "My abilities include system control, web browsing, information queries, and friendly conversation.",
        "I can help with computer tasks, answer your questions, and chat with you naturally!"
    ],
    'unknown': [
        "I'm not quite sure about that. Could you try asking me something else?",
        "That's an interesting question! I'm still learning. Can you ask me something else?",
        "I don't have a good answer for that right now. What else can I help you with?"
    ]
}

# API Keys (set as environment variables)
API_KEYS = {
    'elevenlabs': 'ELEVEN_API_KEY',
    'google_cloud': 'GOOGLE_APPLICATION_CREDENTIALS',
    'openai': 'OPENAI_API_KEY'  # For future OpenAI integration
}

# System Prompts for LLaMA
SYSTEM_PROMPTS = {
    'default': """You are a helpful AI voice assistant running on a PC. You should:
- Give natural, conversational responses
- Be concise but informative
- Sound friendly and approachable
- Answer questions directly and helpfully
- For chit-chat, be engaging and personable
- Keep responses under 50 words unless more detail is specifically requested""",
    
    'technical': """You are a technical AI assistant. Provide:
- Accurate technical information
- Clear step-by-step instructions when needed
- Relevant examples and code snippets
- Troubleshooting guidance""",
    
    'casual': """You are a friendly AI companion. Be:
- Warm and conversational
- Encouraging and positive
- Interested in the user's day and activities
- Helpful with everyday tasks"""
}

# Debug Settings
DEBUG_CONFIG = {
    'verbose_logging': False,
    'save_audio_files': False,
    'log_conversations': True,
    'performance_monitoring': False
}
