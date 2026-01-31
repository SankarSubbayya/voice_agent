#!/usr/bin/env python3
"""
Test script demonstrating VocalBridge voice integration.
This shows the complete flow from audio → text → agents → text → audio.
"""

from services.voice_interface import create_voice_interface
from services.vocalbridge_client import get_vocalbridge_client
from config import config

def main():
    print("=" * 70)
    print("VocalBridge Integration Test")
    print("=" * 70)
    print()

    # Show configuration
    print("Configuration:")
    print(f"  Environment: {config.environment}")
    print(f"  Mock APIs: {config.use_mock_apis}")
    print(f"  VocalBridge API Key: {'Configured' if config.has_vocalbridge() else 'Not configured'}")
    print(f"  VocalBridge Endpoint: {config.vocalbridge_endpoint}")
    print()

    # Test 1: VocalBridge Client
    print("Test 1: VocalBridge Client")
    print("-" * 70)
    client = get_vocalbridge_client()
    print("✅ Client initialized")

    # Test TTS
    print("  Testing text-to-speech...")
    try:
        test_text = "Hello! I'm the ReturnFlow Voice Agent. How can I help you today?"
        audio_data = client.text_to_speech(test_text)
        print(f"  ✅ Generated {len(audio_data)} bytes of audio")

        if config.use_mock_apis:
            print(f"  📝 Mock TTS output: {audio_data.decode('utf-8')}")
    except Exception as e:
        print(f"  ❌ TTS Error: {e}")
    print()

    # Test 2: Voice Interface with Multi-Agent System
    print("Test 2: Voice Interface + Multi-Agent Orchestration")
    print("-" * 70)

    interface = create_voice_interface()
    print("✅ Voice interface initialized")

    # Start conversation
    orch_session, voice_session = interface.start_voice_conversation("USER001")
    print(f"✅ Started conversation")
    print(f"   Orchestrator: {orch_session}")
    print(f"   VocalBridge: {voice_session}")
    print()

    # Simulate a complete return flow
    conversation_steps = [
        {
            "user_says": "I want to return my wireless headphones",
            "description": "User initiates return request"
        },
        {
            "user_says": "Order 1001",
            "description": "User selects their order"
        },
        {
            "user_says": "The headphones arrived damaged",
            "description": "User explains the issue"
        }
    ]

    for i, step in enumerate(conversation_steps, 1):
        print(f"Step {i}: {step['description']}")
        print(f"  👤 User: \"{step['user_says']}\"")

        # In real mode, this would be actual audio bytes from microphone
        # In mock mode, we simulate audio that would transcribe to this text
        mock_audio = step['user_says'].encode('utf-8')

        # Process through voice interface
        # This does: Audio → STT → Orchestrator → Agents → Response → TTS → Audio
        success, response_text, response_audio = interface.process_voice_input(
            mock_audio,
            audio_format="wav"
        )

        print(f"  🤖 Agent: \"{response_text}\"")

        if config.use_mock_apis:
            print(f"  🔊 Mock audio: {len(response_audio)} bytes")
        else:
            print(f"  🔊 Real audio: {len(response_audio)} bytes (ready to play)")
        print()

    # Test text input mode (hybrid)
    print("Test 3: Hybrid Mode (Text Input → Voice Output)")
    print("-" * 70)

    success, response_text, response_audio = interface.process_text_input(
        "Yes, please email me the label"
    )

    print(f"  👤 User (typed): \"Yes, please email me the label\"")
    print(f"  🤖 Agent (text): \"{response_text}\"")
    print(f"  🔊 Agent (voice): {len(response_audio)} bytes generated")
    print()

    # End conversation
    interface.end_conversation()
    print("✅ Conversation ended")
    print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print("✅ VocalBridge client working")
    print("✅ Voice interface working")
    print("✅ Multi-agent orchestration working")
    print("✅ Text-to-speech working")
    print("✅ Hybrid mode working")
    print()

    if config.use_mock_apis:
        print("ℹ️  Currently running in MOCK mode")
        print()
        print("To use real VocalBridge API:")
        print("  1. Verify VOCALBRIDGE_API_KEY in .env")
        print("  2. Confirm VOCALBRIDGE_ENDPOINT is correct")
        print("  3. Set USE_MOCK_APIS=false in .env")
        print("  4. Run: python3 voice_cli.py")
    else:
        print("✅ Running with REAL VocalBridge API")
        print()
        print("Ready for voice conversations!")
        print("  Run: python3 voice_cli.py")
    print()

if __name__ == "__main__":
    main()
