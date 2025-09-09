import os
import sys
import subprocess
import webbrowser
import datetime
import random
import time
import json
import threading

# Added MultiTTS
import pygame
from pathlib import Path

try:
    import speech_recognition as sr
    import pyttsx3
    import pyaudio
    print(" All speech modules imported successfully")
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install SpeechRecognition pyttsx3 pyaudio")
    sys.exit(1)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Ollama not available")

try:
    import pyautogui
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False

try:
    import psutil
    BATTERY_AVAILABLE = True
except ImportError:
    BATTERY_AVAILABLE = False

class MultiTTS:
    """Multi-engine TTS class to replace pyttsx3 and fix vocal response issues"""
    def __init__(self, engine="auto"):
        self.engine = self._select_engine(engine)
        pygame.mixer.init()
        
        # Initialize chosen engine
        if self.engine == "coqui":
            try:
                from TTS.api import TTS
                self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
            except ImportError:
                self.engine = "windows" if sys.platform.startswith('win') else "pyttsx3"
        elif self.engine == "elevenlabs":
            try:
                from elevenlabs import generate, play
                self.elevenlabs = True
            except ImportError:
                self.engine = "windows" if sys.platform.startswith('win') else "pyttsx3"
        elif self.engine == "google":
            try:
                from gtts import gTTS
                self.gtts = True
            except ImportError:
                self.engine = "windows" if sys.platform.startswith('win') else "pyttsx3"
        
        # Default to pyttsx3 with engine reinitialization fix
        if self.engine == "pyttsx3":
            self.pyttsx3_available = True
    
    def _select_engine(self, preference):
        """Auto-select best available engine"""
        if preference != "auto":
            return preference
        
        # Trying Coqui first (best quality local)
        try:
            import TTS
            return "coqui"
        except ImportError:
            pass
        
        # Try Windows SAPI (reliable on Windows)
        if sys.platform.startswith('win'):
            return "windows"
        
        # Try eSpeak (lightweight Default)
        try:
            if os.system("espeak --version > /dev/null 2>&1") == 0:
                return "espeak"
        except:
            pass
        
        # Default to Google TTS (requires internet)
        try:
            import gtts
            return "google"
        except ImportError:
            pass
        
        # Final Default to fixed pyttsx3
        return "pyttsx3"
    
    def speak(self, text):
        """Universal speak method with engine-specific implementations"""
        if not text or not text.strip():
            return
        
        print(f"🗣️ Speaking with {self.engine}: {text}")
        
        try:
            if self.engine == "coqui":
                self._coqui_speak(text)
            elif self.engine == "elevenlabs":
                self._elevenlabs_speak(text)
            elif self.engine == "google":
                self._google_speak(text)
            elif self.engine == "windows":
                self._windows_speak(text)
            elif self.engine == "espeak":
                self._espeak_speak(text)
            elif self.engine == "pyttsx3":
                self._pyttsx3_speak_fixed(text)
            
            print(" Speech completed successfully")
            
        except Exception as e:
            print(f" TTS Error with {self.engine}: {e}")
            # Try Default
            self._Default_speak(text)
    
    def _coqui_speak(self, text):
        """Coqui TTS implementation"""
        self.tts.tts_to_file(text=text, file_path="temp_audio.wav")
        self._play_audio("temp_audio.wav")
    
    def _elevenlabs_speak(self, text):
        """ElevenLabs TTS implementation"""
        from elevenlabs import generate
        audio = generate(text=text, voice="Adam")
        with open("temp_audio.wav", "wb") as f:
            f.write(audio)
        self._play_audio("temp_audio.wav")
    
    def _google_speak(self, text):
        """Google TTS implementation"""
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save("temp_audio.mp3")
        self._play_audio("temp_audio.mp3")
    
    def _windows_speak(self, text):
        """ Windows TTS with base64 encoding to avoid all PowerShell quote issues"""
        import os
        import base64
    
        try:
            
            encoded_text = base64.b64encode(text.encode('utf-8')).decode('ascii')
        
            
            command = (
                f'powershell -NoProfile -Command "'
                f'Add-Type -AssemblyName System.Speech; '
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\'{encoded_text}\')); '
                f'$synth.Speak($decoded)'
                f'"'
            )
        
            os.system(command)
        
        except Exception as e:
            print(f"Windows TTS error: {e}")
            # Final  Default
            print(f"  Default: {text}")

    
    def _espeak_speak(self, text):
        """eSpeak TTS implementation"""
        # Escape quotes and special characters
        clean_text = text.replace('"', '\\"')
        os.system(f'espeak "{clean_text}" 2>/dev/null')
    
    def _pyttsx3_speak_fixed(self, text):
        """reinitialize engine each time"""
        try:
            #Reinitialize engine each time to prevent death
            engine = pyttsx3.init()
            engine.setProperty('rate', 140)
            engine.setProperty('volume', 1.0)
            
            # Select male voice if available
            voices = engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            engine.say(text)
            engine.runAndWait()  # Must have parentheses!
            
            # Brief delay to ensure completion
            time.sleep(0.1)
            
        except Exception as e:
            print(f"pyttsx3 error: {e}")
            self._Default_speak(text)
    
    def _play_audio(self, file_path):
        """Play audio file using pygame"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up temp file
            try:
                Path(file_path).unlink()
            except:
                pass
                
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def _Default_speak(self, text):
        """ Default - try Windows SAPI or print"""
        try:
            if sys.platform.startswith('win'):
                self._windows_speak(text)
            else:
                print(f" Default SPEECH: {text}")
        except:
            print(f"  Default: {text}")

class ConversationMemory:
    """Simple memory system to maintain context"""
    def __init__(self, max_size=10):
        self.context = []
        self.max_size = max_size
        self.user_preferences = {}
    
    def add_message(self, role, message):
        """Add message to conversation history"""
        self.context.append({"role": role, "message": message, "timestamp": datetime.datetime.now()})
        if len(self.context) > self.max_size:
            self.context.pop(0)
    
    def get_context_string(self):
        """Get context as formatted string for LLaMA"""
        if not self.context:
            return ""
        
        context_str = "\nRecent conversation:\n"
        for entry in self.context[-5:]:  # Last 5 messages
            context_str += f"{entry['role']}: {entry['message']}\n"
        return context_str
    
    def save_preference(self, key, value):
        """Save user preference"""
        self.user_preferences[key] = value
    
    def get_preference(self, key):
        """Get user preference"""
        return self.user_preferences.get(key)

class LlamaClient:
    """ LLaMA 3.1 8B client with conversation support"""
    def __init__(self, model_name="llama3.1:8b", host_url="http://localhost:11434"):
        self.model_name = model_name
        self.host_url = host_url
        self.is_ready = False
        
        if OLLAMA_AVAILABLE:
            self.is_ready = self.check_connection()
            if self.is_ready:
                print(f" LLaMA 3.1 8B connected: {model_name}")
            else:
                print(" LLaMA not available - using Default responses")
    
    def check_connection(self):
        """Check if Ollama server is running and model is available"""
        import requests
        try:
            response = requests.get(f"{self.host_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model.get('name', '') for model in data.get('models', [])]
                return any('llama3.1' in model.lower() for model in models)
            return False
        except Exception as e:
            print(f"Connection check failed: {e}")
            return False
    
    def generate_response(self, prompt, context="", max_tokens=200):
        """Generate response using LLaMA 3.1 8B"""
        if not self.is_ready:
            return None
        
        try:
            # Create comprehensive prompt for natural conversation
            system_prompt = """You are a helpful AI voice assistant running on a PC. You should:
- Give natural, conversational responses
- Be concise but informative
- Sound friendly and approachable
- Answer questions directly and helpfully
- For chit-chat, be engaging and personable
- Keep responses under 50 words unless more detail is specifically requested"""
            
            full_prompt = f"{system_prompt}\n{context}\nUser: {prompt}\nAssistant:"
            
            # Call Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": full_prompt}],
                options={"temperature": 0.7, "max_tokens": max_tokens}
            )
            
            if response and 'message' in response:
                return response['message']['content'].strip()
            
        except Exception as e:
            print(f"LLaMA generation error: {e}")
        
        return None

class VoiceAssistant:
    """Main AI Voice Assistant with LLaMA 3.1 8B integration and Fixed TTS"""
    
    def __init__(self):
        print(" Initializing Enhanced AI Voice Assistant with MultiTTS...")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate microphone
        with self.microphone as source:
            print("🎤 Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # REPLACED: Initialize MultiTTS instead of pyttsx3
        self.tts = MultiTTS(engine="auto")  # Will auto-select best available TTS
        print(" ")
        
        # Initialize AI and memory
        self.llama_client = LlamaClient()
        self.memory = ConversationMemory()
        
        # Configuration
        self.websites = {
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
            'discord': 'https://discord.com'
        }
        
        self.apps = {
            'chrome': ['chrome.exe', 'google-chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'brave': ['brave.exe', 'brave-browser', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'],
            'firefox': ['firefox.exe', 'firefox', '/Applications/Firefox.app/Contents/MacOS/firefox'],
            'notepad': ['notepad.exe', 'gedit', '/Applications/TextEdit.app/Contents/MacOS/TextEdit'],
            'calculator': ['calc.exe', 'gnome-calculator', '/Applications/Calculator.app/Contents/MacOS/Calculator'],
            'spotify': ['spotify.exe', 'spotify', '/Applications/Spotify.app/Contents/MacOS/Spotify']
        }
        
        # Default responses for when LLaMA is not available
        self.Default_responses = {
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
                "Sorry?",
                "That's an interesting question! I'm still learning. Can you ask me something else?",
                "I don't have a good answer for that right now. What else can I help you with?"
            ]
        }
        
        self.running = True
        print(" Enhanced AI Voice Assistant ready!")
    
    def listen_command(self):
        """Capture user voice input and convert to text"""
        try:
            with self.microphone as source:
                print("\n Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            print(" Processing speech...")
            command = self.recognizer.recognize_google(audio)
            print(f" You said: '{command}'")
            return command.strip()
            
        except sr.WaitTimeoutError:
            print(" No speech detected")
            return None
        except sr.UnknownValueError:
            print(" Could not understand speech")
            self.speak_response(" ")
            return None
        except sr.RequestError as e:
            print(f" Speech recognition error: {e}")
            self.speak_response("I'm having trouble with speech recognition. Please try again.")
            return None
        except Exception as e:
            print(f" Listen error: {e}")
            return None
    
    def speak_response(self, text):
        """FIXED: Use MultiTTS for reliable vocal responses"""
        if not text or not text.strip():
            return
        
        # Use the new MultiTTS system - no threading issues!
        self.tts.speak(text)
    
    def generate_response(self, prompt, is_question=True):
        """Generate AI response using LLaMA 3.1 8B with context"""
        context = self.memory.get_context_string()
        
        if self.llama_client.is_ready:
            response = self.llama_client.generate_response(prompt, context)
            if response:
                return response
        
        # Default responses when LLaMA is not available
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return random.choice(self.Default_responses['greeting'])
        elif any(phrase in prompt_lower for phrase in ['how are you', 'how do you feel']):
            return random.choice(self.Default_responses['how_are_you'])
        elif any(phrase in prompt_lower for phrase in ['what can you do', 'help', 'capabilities']):
            return random.choice(self.Default_responses['capabilities'])
        else:
            return random.choice(self.Default_responses['unknown'])
    
    def process_command(self, command):
        """Process and execute commands - distinguish between direct commands and queries"""
        if not command:
            return True
        
        command_lower = command.lower()
        
        # Add to conversation memory
        self.memory.add_message("User", command)
        
        try:
            # EXIT COMMANDS
            if any(word in command_lower for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
                response = "Goodbye! It's been great talking with you. Have a wonderful day!"
                self.speak_response(response)
                self.memory.add_message("Assistant", response)
                return False
            
            # SYSTEM COMMANDS - Execute immediately
            if self._handle_system_commands(command_lower):
                return True
            
            # WEB COMMANDS - Execute immediately  
            if self._handle_web_commands(command_lower):
                return True
            
            # SEARCH COMMANDS - Execute immediately
            if self._handle_search_commands(command_lower, command):
                return True
            
            # ALL OTHER QUERIES - Send to LLaMA 3.1 8B
            response = self.generate_response(command)
            if response:
                self.speak_response(response)
                self.memory.add_message("Assistant", response)
            else:
                Default = "I'm not sure how to help with that. Could you try asking me something else?"
                self.speak_response(Default)
                self.memory.add_message("Assistant", Default)
            
            return True
            
        except Exception as e:
            print(f" Command processing error: {e}")
            error_response = "I encountered an error processing that request. Please try again."
            self.speak_response(error_response)
            return True
    
    def _handle_system_commands(self, command):
        """Handle direct system commands"""
        # Application launching
        for app_name, commands in self.apps.items():
            if f'open {app_name}' in command or f'launch {app_name}' in command or f'start {app_name}' in command:
                success = self._open_application(app_name)
                if success:
                    response = f"Opening {app_name.title()}!"
                else:
                    response = f"Sorry, I couldn't open {app_name}. Make sure it's installed."
                self.speak_response(response)
                self.memory.add_message("Assistant", response)
                return True
        
        # System commands
        if 'lock computer' in command or 'lock screen' in command:
            self.speak_response("Locking your computer now!")
            if sys.platform.startswith('win'):
                os.system("rundll32.exe user32.dll,LockWorkStation")
            self.memory.add_message("Assistant", "Locked the computer")
            return True
        
        if 'shutdown computer' in command:
            self.speak_response("Are you sure you want to shutdown? This is just a demo response for safety.")
            self.memory.add_message("Assistant", "Shutdown request (demo only)")
            return True
        
        if 'screenshot' in command or 'take screenshot' in command:
            if SCREENSHOT_AVAILABLE:
                success = self._take_screenshot()
                if success:
                    response = "Screenshot taken and saved to your desktop!"
                else:
                    response = "Sorry, I couldn't take a screenshot."
            else:
                response = "Screenshot feature is not available. Please install pyautogui."
            
            self.speak_response(response)
            self.memory.add_message("Assistant", response)
            return True
        
        if 'battery' in command and BATTERY_AVAILABLE:
            battery_info = self._get_battery_status()
            self.speak_response(battery_info)
            self.memory.add_message("Assistant", battery_info)
            return True
        
        return False
    
    def _handle_web_commands(self, command):
        """Handle website opening commands"""
        for site_name, url in self.websites.items():
            if f'open {site_name}' in command:
                webbrowser.open(url)
                response = f"Opening {site_name.title()} in your browser!"
                self.speak_response(response)
                self.memory.add_message("Assistant", response)
                return True
        return False
    
    def _handle_search_commands(self, command_lower, original_command):
        """Handle web search commands"""
        search_patterns = [
            'search google for ',
            'google search for ',
            'search for ',
            'google ',
            'look up '
        ]
        
        for pattern in search_patterns:
            if pattern in command_lower:
                query = original_command.lower().split(pattern, 1)
                if len(query) > 1 and query[1].strip():
                    search_query = query[1].strip()
                    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                    webbrowser.open(search_url)
                    response = f"Searching Google for: {search_query}"
                    self.speak_response(response)
                    self.memory.add_message("Assistant", response)
                    return True
        
        return False
    
    def _open_application(self, app_name):
        """Open system application"""
        if app_name in self.apps:
            for command in self.apps[app_name]:
                try:
                    subprocess.Popen([command])
                    return True
                except FileNotFoundError:
                    continue
                except Exception:
                    continue
        return False
    
    def _take_screenshot(self):
        """Take screenshot and save to desktop"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(desktop_path)
            return True
        except Exception as e:
            print(f"Screenshot error: {e}")
            return False
    
    def _get_battery_status(self):
        """Get battery status information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "charging" if battery.power_plugged else "on battery power"
                
                if percent > 80:
                    status_comment = "Battery level is excellent!"
                elif percent > 50:
                    status_comment = "Battery level looks good."
                elif percent > 20:
                    status_comment = "You might want to charge soon."
                else:
                    status_comment = "Please charge your device soon!"
                
                return f"Battery is at {percent} percent and {plugged}. {status_comment}"
            else:
                return "Battery information is not available on this system."
        except Exception:
            return "Sorry, I couldn't check the battery status."
    
    def main_loop(self):
        """Main continuous listening loop"""
        # Welcome message
        welcome_messages = [
            "Hello! I'm your  AI voice assistant, I'm ready to help with anything you need!",
            "Hi there! Your AI assistant is online and ready to assist you.",
            "Welcome! I'm your personal AI assistant, How can I help you today?"
        ]
        
        welcome = random.choice(welcome_messages)
        self.speak_response(welcome)
        self.memory.add_message("Assistant", welcome)
        
        print("\n Enhanced AI Voice Assistant is active!")
        print(" Try saying:")
        print("   • 'Hello' or 'How are you?' - Conversation")
        print("   • 'What time is it?' or 'Tell me about...' - Questions")
        print("   • 'Open Chrome' or 'Launch Brave' - Apps")
        print("   • 'Open YouTube' or 'Open Instagram' - Websites")
        print("   • 'Search Google for Python tutorials' - Web search")
        print("   • 'Take a screenshot' - System commands")
        print("   • 'Exit' or 'Goodbye' - Stop assistant")
        print("\n Make sure your microphone and speakers are working!")
        
        conversation_count = 0
        
        while self.running:
            try:
                # Listen for voice command
                user_command = self.listen_command()
                
                if user_command:
                    conversation_count += 1
                    print(f"\n--- Conversation #{conversation_count} ---")
                    
                    # Process the command
                    continue_running = self.process_command(user_command)
                    
                    if not continue_running:
                        self.running = False
                        break
                
                # Brief pause between listening cycles
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n Assistant stopped by user")
                farewell = "Voice assistant shutting down. Thanks for using me! Goodbye!"
                self.speak_response(farewell)
                break
            except Exception as e:
                print(f" Main loop error: {e}")
                error_msg = "I encountered an issue, but I'm still here and ready to help!"
                self.speak_response(error_msg)

def main():
    """Main function with comprehensive error handling"""
    print("🔍 Checking system requirements...")
    
    # Check essential dependencies
    missing_deps = []
    
    try:
        import speech_recognition
        import pyttsx3
        import pyaudio
    except ImportError as e:
        missing_deps.append(str(e))
    
    if missing_deps:
        print(" Missing essential dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with: pip install SpeechRecognition pyttsx3 pyaudio pygame")
        return
    
    try:
        # Initialize and run the assistant
        assistant = VoiceAssistant()
        assistant.main_loop()
        
    except Exception as e:
        print(f" Failed to start assistant: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your microphone is connected and working")
        print("2. Check that your speakers/headphones are connected")
        print("3. Install pygame: pip install pygame")
        print("4. For LLaMA: Start Ollama server and pull llama3.1:8b model")
        print("5. Test microphone with other applications")

if __name__ == "__main__":
    main()
