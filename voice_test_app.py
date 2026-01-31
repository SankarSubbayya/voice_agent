#!/usr/bin/env python3
"""
Flask app for testing Vocal Bridge voice agent.
Provides a web interface with backend proxy to avoid CORS issues.
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from services.vocalbridge_livekit_client import VocalBridgeClient
import webbrowser
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = VocalBridgeClient()

@app.route('/')
def index():
    """Serve the test page."""
    return send_from_directory('.', 'test_vocal_bridge_live.html')

@app.route('/api/credentials')
def get_credentials():
    """Get LiveKit credentials from Vocal Bridge."""
    try:
        creds = client.get_livekit_credentials()
        return jsonify({
            'success': True,
            'data': creds
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test')
def test():
    """Test endpoint to verify server is running."""
    return jsonify({
        'status': 'ok',
        'message': 'Vocal Bridge test server is running'
    })

def open_browser():
    """Open browser after server starts."""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  VOCAL BRIDGE TEST SERVER")
    print("="*70 + "\n")
    print("Starting Flask server...")
    print("Server will run on: http://localhost:5000")
    print()
    print("Opening browser in 1.5 seconds...")
    print()
    print("="*70)
    print("  INSTRUCTIONS")
    print("="*70)
    print()
    print("1️⃣  Click 'Step 1: Get Credentials'")
    print("2️⃣  Click 'Step 2: Start Voice Call'")
    print("3️⃣  Allow microphone and start speaking")
    print()
    print("="*70)
    print()
    print("Press Ctrl+C to stop the server.")
    print()

    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Run Flask app
    app.run(debug=False, port=5000)
