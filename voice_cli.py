#!/usr/bin/env python3
"""
Voice-Enabled CLI for ReturnFlow Voice Agent

Uses VocalBridge AI for real voice input/output.
Supports both voice and text input for hybrid mode.
"""

import sys
from pathlib import Path

from config import config
from database.mock_db import MockDatabase
from services.voice_interface import create_voice_interface


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🎤 ReturnFlow Voice Agent (Voice Mode)               ║
║         Powered by: VocalBridge AI                           ║
║                                                               ║
║         Natural voice-based product returns                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_status():
    """Print current configuration status."""
    print("\n📊 Configuration Status:")
    print("=" * 60)
    print(f"Environment: {config.environment}")
    print(f"Mock APIs: {config.use_mock_apis}")
    print(f"VocalBridge API: {'✅ Configured' if config.has_vocalbridge() else '❌ Not configured'}")
    print(f"API Endpoint: {config.vocalbridge_endpoint}")
    print("=" * 60)
    print()


def print_help():
    """Print help information."""
    help_text = """
Voice Commands:
  - Speak naturally: "I want to return my headphones"
  - Press Enter after speaking to process
  - Type 'text' to switch to text mode
  - Type 'help' for this message
  - Type 'quit' or 'exit' to exit

Text Mode Commands:
  - Type your messages normally
  - Type 'voice' to switch to voice mode
  - Type 'demo' to run demo scenario
  - Type 'quit' or 'exit' to exit

Voice Input Methods:
  1. Record from microphone (if available)
  2. Load audio file: "load <filename>"
  3. Use text mode for testing

Example Voice Flow:
  🎤 You: [Speak] "I want to return my headphones"
  🤖 Agent: [Responds with voice] "I'll help you start a return..."

Example Text Flow:
  💬 You: I want to return my coffee maker
  🤖 Agent: [Voice response] I found your recent orders...
    """
    print(help_text)


def check_microphone_available():
    """Check if microphone is available for recording."""
    try:
        import pyaudio
        return True
    except ImportError:
        return False


def record_audio(duration_seconds: int = 5):
    """
    Record audio from microphone.

    Args:
        duration_seconds: Recording duration

    Returns:
        Audio bytes in WAV format
    """
    try:
        import pyaudio
        import wave
        import io

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()

        print(f"🎤 Recording for {duration_seconds} seconds...")

        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        frames = []

        for i in range(0, int(RATE / CHUNK * duration_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("✅ Recording complete!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Convert to WAV bytes
        wav_buffer = io.BytesIO()
        wf = wave.open(wav_buffer, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        wav_buffer.seek(0)
        return wav_buffer.read()

    except ImportError:
        print("❌ PyAudio not installed. Install with: pip install pyaudio")
        return None
    except Exception as e:
        print(f"❌ Recording error: {e}")
        return None


def load_audio_file(filepath: str):
    """Load audio from file."""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None


def voice_mode(interface):
    """Run in voice input mode."""
    print("\n🎤 Voice Mode Active")
    print("=" * 60)

    has_mic = check_microphone_available()

    if has_mic:
        print("✅ Microphone detected")
        print("Press Enter to record, or type 'text' to switch modes")
    else:
        print("⚠️  Microphone not available (pyaudio not installed)")
        print("You can:")
        print("  - Install microphone support: pip install pyaudio")
        print("  - Load audio files: load <filename>")
        print("  - Use text mode: type 'text'")

    print()

    while True:
        try:
            user_input = input("🎤 [Press Enter to record] or command: ").strip()

            if not user_input:
                # Record from microphone
                if not has_mic:
                    print("⚠️  Microphone not available. Use 'load <file>' or switch to 'text' mode.")
                    continue

                audio = record_audio(duration_seconds=5)
                if audio:
                    success, text, audio_response = interface.process_voice_input(audio)
                    print(f"\n🤖 Agent: {text}\n")
                    # In real use, would play audio_response

            elif user_input.lower() == 'text':
                return 'text'

            elif user_input.lower().startswith('load '):
                filename = user_input[5:].strip()
                audio = load_audio_file(filename)
                if audio:
                    success, text, audio_response = interface.process_voice_input(audio)
                    print(f"\n🤖 Agent: {text}\n")

            elif user_input.lower() in ['quit', 'exit', 'bye']:
                return 'quit'

            elif user_input.lower() == 'help':
                print_help()

            else:
                print("⚠️  Unknown command. Press Enter to record, or type 'help'.")

        except KeyboardInterrupt:
            print("\n")
            return 'quit'


def text_mode(interface):
    """Run in text input mode (hybrid - text in, voice out)."""
    print("\n💬 Text Mode Active (Voice responses enabled)")
    print("=" * 60)
    print("Type naturally, and the agent will respond with voice.")
    print("Type 'voice' to switch to voice mode, or 'help' for help.")
    print()

    while True:
        try:
            user_input = input("💬 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == 'voice':
                return 'voice'

            if user_input.lower() in ['quit', 'exit', 'bye']:
                return 'quit'

            if user_input.lower() == 'help':
                print_help()
                continue

            if user_input.lower() == 'demo':
                print("\n⚠️  Demo mode not available in voice CLI.")
                print("    Use regular CLI: python3 main.py")
                continue

            # Process text input
            success, text, audio_response = interface.process_text_input(user_input)
            print(f"\n🤖 Agent: {text}\n")

            # In real use, would also play audio_response
            if not config.use_mock_apis and len(audio_response) > 100:
                print("    [🔊 Voice response generated - would play audio here]")
            print()

        except KeyboardInterrupt:
            print("\n")
            return 'quit'


def main():
    """Main entry point for voice CLI."""
    print_banner()
    print_status()

    # Check if VocalBridge is configured
    if not config.has_vocalbridge() and not config.use_mock_apis:
        print("⚠️  VocalBridge API key not found!")
        print()
        print("To enable voice features:")
        print("  1. Edit .env file")
        print("  2. Add: VOCALBRIDGE_API_KEY=your_key_here")
        print("  3. Set: USE_MOCK_APIS=false")
        print()
        print("For now, running in MOCK MODE (text-based demo)...")
        print()

    # Create voice interface
    try:
        interface = create_voice_interface()
    except Exception as e:
        print(f"❌ Failed to initialize voice interface: {e}")
        print()
        print("Please check your .env configuration:")
        print("  - VOCALBRIDGE_API_KEY must be set")
        print("  - Or set USE_MOCK_APIS=true for mock mode")
        sys.exit(1)

    # Start conversation
    print("Starting conversation session...")
    orch_session, voice_session = interface.start_voice_conversation("USER001")
    print(f"✅ Session started: {orch_session[:20]}...\n")

    # Determine starting mode
    has_mic = check_microphone_available()
    current_mode = 'text' if not has_mic else 'voice'

    if current_mode == 'voice':
        print("🎤 Starting in VOICE mode (microphone available)")
    else:
        print("💬 Starting in TEXT mode (hybrid voice responses)")

    print()
    print("Type 'help' for available commands")
    print("=" * 60)
    print()

    # Main loop
    while True:
        if current_mode == 'voice':
            result = voice_mode(interface)
        else:
            result = text_mode(interface)

        if result == 'quit':
            break
        elif result == 'voice':
            current_mode = 'voice'
        elif result == 'text':
            current_mode = 'text'

    # Cleanup
    print("\n👋 Ending conversation...")
    interface.end_conversation()
    print("Thanks for using ReturnFlow Voice Agent!")
    print()


if __name__ == "__main__":
    main()
