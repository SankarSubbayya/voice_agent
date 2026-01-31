#!/usr/bin/env python3
"""
Simple Vocal Bridge Voice Agent Tester

This script will:
1. Test the API connection
2. Open a browser with the test interface
3. Guide you through testing the voice agent
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

from services.vocalbridge_livekit_client import VocalBridgeClient
import webbrowser
import os


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    print_header("VOCAL BRIDGE VOICE AGENT - QUICK TEST")

    # Step 1: Test API
    print("Step 1: Testing API Connection...")
    print("-" * 70)

    try:
        client = VocalBridgeClient()
        print(f"✅ Client initialized")
        print(f"   API Key: {client.api_key[:20]}...")
        print(f"   Endpoint: {client.endpoint}")
        print()

        print("Getting LiveKit credentials...")
        creds = client.get_livekit_credentials()

        print("✅ API is working!")
        print(f"   LiveKit URL: {creds['livekit_url']}")
        print(f"   Room: {creds['room_name']}")
        print(f"   Expires in: {creds['expires_in']} seconds")
        print()

    except Exception as e:
        print(f"❌ API Error: {e}")
        print()
        print("Please check:")
        print("  1. Your internet connection")
        print("  2. API key in .env file")
        print("  3. Vocal Bridge dashboard (agent status)")
        return

    # Step 2: Open browser
    print_header("Step 2: Opening Browser Test Interface")

    html_file = os.path.abspath('test_vocal_bridge_live.html')

    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found")
        return

    print(f"Opening: {html_file}")
    print()

    try:
        webbrowser.open(f'file://{html_file}')
        print("✅ Browser should open shortly...")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"   Please manually open: {html_file}")

    print()
    print_header("TESTING INSTRUCTIONS")

    print("When the browser opens, follow these steps:\n")

    print("1️⃣  Click 'Step 1: Get Credentials'")
    print("   • Should see: ✅ Credentials Retrieved")
    print("   • Should display LiveKit URL and Room name")
    print()

    print("2️⃣  Click 'Step 2: Start Voice Call'")
    print("   • Allow microphone access when prompted")
    print("   • Should see: ✅ Connected to room!")
    print("   • Should see: 🎤 Microphone enabled")
    print()

    print("3️⃣  Start Speaking!")
    print("   • Say: 'I want to return my headphones to Amazon'")
    print("   • The agent should respond with voice")
    print("   • Continue the conversation naturally")
    print()

    print("4️⃣  Watch the Log")
    print("   • Bottom section shows all events")
    print("   • Look for 'Agent audio track received'")
    print("   • Look for 'Participant joined' messages")
    print()

    print_header("TROUBLESHOOTING")

    print("If nothing happens:")
    print("  • Check browser console (F12 → Console tab)")
    print("  • Ensure microphone permissions are granted")
    print("  • Try Chrome or Edge (best LiveKit support)")
    print()

    print("If you hear nothing:")
    print("  • Check your speaker/headphone volume")
    print("  • Look for '🔊 Agent audio track received' in log")
    print("  • Try saying something to trigger the agent")
    print()

    print("If agent doesn't respond:")
    print("  • Check Vocal Bridge dashboard → Call Logs")
    print("  • Verify your agent is 'Active'")
    print("  • Wait 2-3 seconds after speaking")
    print()

    print_header("WHAT TO EXPECT")

    print("✅ Successful test looks like:")
    print()
    print("  1. Credentials load instantly")
    print("  2. Connection takes 2-5 seconds")
    print("  3. Microphone turns on (browser shows indicator)")
    print("  4. Agent greets you within 2-3 seconds")
    print("  5. Natural conversation begins")
    print()

    print("Your agent ('Vice Agent') should:")
    print("  • Greet you professionally")
    print("  • Ask which store (Amazon or Walmart)")
    print("  • Collect order number")
    print("  • Ask for return reason")
    print("  • Confirm details")
    print()

    print_header("READY!")

    print("The browser test interface should now be open.")
    print("Follow the instructions above and start testing!")
    print()
    print(f"If browser didn't open, manually open:")
    print(f"  {html_file}")
    print()


if __name__ == "__main__":
    main()
