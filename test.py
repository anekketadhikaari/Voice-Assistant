import os
import sys
import pygame
from pathlib import Path

class MultiTTS:
    def __init__(self, engine="auto"):
        self.engine = self._select_engine(engine)
        pygame.mixer.init()
        
        # Initialize chosen engine
        if self.engine == "coqui":
            from TTS.api import TTS
            self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
        elif self.engine == "elevenlabs":
            from elevenlabs import generate, play
            self.elevenlabs = True
        elif self.engine == "google":
            from gtts import gTTS
            self.gtts = True
    
    def _select_engine(self, preference):
        """Auto-select best available engine"""
        if preference != "auto":
            return preference
        
        # Try Coqui first
        try:
            import TTS
            return "coqui"
        except ImportError:
            pass
        
        # Try Windows SAPI
        if sys.platform.startswith('win'):
            return "windows"
        
        # Try eSpeak
        if os.system("espeak --version") == 0:
            return "espeak"
        
        # Default to Google (requires internet)
        return "google"
    
    def speak(self, text):
        """Universal speak method"""
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
            
            print("✅ Speech completed")
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def _coqui_speak(self, text):
        self.tts.tts_to_file(text=text, file_path="temp_audio.wav")
        self._play_audio("temp_audio.wav")
    
    def _elevenlabs_speak(self, text):
        from elevenlabs import generate
        audio = generate(text=text, voice="Adam")
        with open("temp_audio.wav", "wb") as f:
            f.write(audio)
        self._play_audio("temp_audio.wav")
    
    def _google_speak(self, text):
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save("temp_audio.mp3")
        self._play_audio("temp_audio.mp3")
    
    def _windows_speak(self, text):
        clean_text = text.replace("'", "''")
        command = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak(\'{clean_text}\')"'
        os.system(command)
    
    def _espeak_speak(self, text):
        os.system(f'espeak "{text}" -w temp_audio.wav')
        self._play_audio("temp_audio.wav")
    
    def _play_audio(self, file_path):
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

# Usage in your voice assistant
class FixedVoiceAssistant:
    def __init__(self):
        # Replace pyttsx3 with MultiTTS
        self.tts = MultiTTS(engine="auto")  # or specify: "coqui", "elevenlabs", etc.
    
    def speak_response(self, text):
        """Fixed TTS method"""
        if text:
            self.tts.speak(text)

# Test the new TTS system
if __name__ == "__main__":
    assistant = FixedVoiceAssistant()
    assistant.speak_response("Hello! This is the new TTS system working perfectly!")
    assistant.speak_response("I can now speak multiple responses without issues!")
