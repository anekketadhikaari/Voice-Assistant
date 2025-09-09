#!/usr/bin/env python3
"""
Installation helper for AI Voice Assistant
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f" {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f" {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f" {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(" Python 3.8+ required. Current version:", sys.version)
        return False
    print(f" Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing core dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def setup_ollama():
    """Setup Ollama and LLaMA model"""
    system = platform.system().lower()
    
    print(" Ollama Setup Instructions:")
    if system == "windows":
        print("1. Download Ollama from https://ollama.ai/download")
        print("2. Run the installer")
        print("3. Open Command Prompt and run: ollama pull llama3.1:8b")
    elif system == "linux":
        print("1. Run: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Run: ollama pull llama3.1:8b")
    elif system == "darwin":  # macOS
        print("1. Download Ollama from https://ollama.ai/download")
        print("2. Install the .dmg file")
        print("3. Run: ollama pull llama3.1:8b")
    
    print("\n  Please complete Ollama setup manually, then press Enter to continue...")
    input()

def test_installation():
    """Test if installation is working"""
    print(" Testing installation...")
    
    # Test imports
    try:
        import speech_recognition
        import pyttsx3
        import pygame
        print(" Core speech modules imported successfully")
    except ImportError as e:
        print(f" Import error: {e}")
        return False
    
    # Test TTS
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print(" TTS engine initialized successfully")
    except Exception as e:
        print(f"⚠️  TTS warning: {e}")
    
    print(" Installation test completed")
    return True

def main():
    """Main installation process"""
    print(" AI Voice Assistant Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print(" Dependency installation failed")
        sys.exit(1)
    
    # Setup Ollama
    setup_ollama()
    
    # Test installation
    if not test_installation():
        print(" Installation test failed")
        sys.exit(1)
    
    print("\n Installation completed successfully!")
    print("\nTo start the assistant, run:")
    print("python main.py")
    print("\nMake sure your microphone and speakers are connected!")

if __name__ == "__main__":
    main()
