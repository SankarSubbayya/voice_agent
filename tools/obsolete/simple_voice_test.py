#!/usr/bin/env python3
"""
Simplest possible voice test - no CORS issues.
Runs a Flask server with backend proxy.
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

try:
    from flask import Flask, jsonify, render_template_string
    flask_available = True
except ImportError:
    flask_available = False

from services.vocalbridge_livekit_client import VocalBridgeClient
import webbrowser
import threading
import time

# HTML template with backend proxy
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vocal Bridge Voice Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            color: #333;
        }
        h1 { color: #667eea; text-align: center; }
        button {
            width: 100%;
            padding: 18px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px 0;
        }
        #getCredentials { background: #667eea; color: white; }
        #startCall { background: #4CAF50; color: white; display: none; }
        #endCall { background: #f44336; color: white; display: none; }
        .status {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .log {
            background: #2d3748;
            color: #a0aec0;
            padding: 20px;
            border-radius: 10px;
            max-height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
        .log-success { color: #48bb78; }
        .log-error { color: #f56565; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Vocal Bridge Voice Test</h1>

        <div class="status" id="status">
            <h3 id="statusTitle">Ready</h3>
            <p id="statusMessage">Click "Get Credentials" to start</p>
        </div>

        <button id="getCredentials" onclick="getCredentials()">Step 1: Get Credentials</button>
        <button id="startCall" onclick="startCall()">Step 2: Start Voice Call</button>
        <button id="endCall" onclick="endCall()">End Call</button>

        <div class="log" id="log"></div>
    </div>

    <script src="https://unpkg.com/livekit-client@latest/dist/livekit-client.umd.min.js"></script>
    <script>
        const LiveKit = window.LiveKitClient;
        let credentials = null;
        let room = null;

        function log(message, type = 'info') {
            const logDiv = document.getElementById('log');
            const time = new Date().toLocaleTimeString();
            const span = document.createElement('div');
            span.className = type === 'error' ? 'log-error' : (type === 'success' ? 'log-success' : '');
            span.textContent = `[${time}] ${message}`;
            logDiv.appendChild(span);
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function updateStatus(title, message) {
            document.getElementById('statusTitle').textContent = title;
            document.getElementById('statusMessage').textContent = message;
        }

        async function getCredentials() {
            log('Requesting credentials from backend...', 'info');
            updateStatus('⏳ Loading', 'Getting credentials...');

            try {
                const response = await fetch('/api/credentials');
                const data = await response.json();

                if (!data.success) {
                    throw new Error(data.error || 'Failed to get credentials');
                }

                credentials = data.data;
                log('✅ Credentials received!', 'success');
                log(`Room: ${credentials.room_name}`, 'info');

                document.getElementById('getCredentials').style.display = 'none';
                document.getElementById('startCall').style.display = 'block';
                updateStatus('✅ Ready', 'Click "Start Voice Call"');

            } catch (error) {
                log(`❌ Error: ${error.message}`, 'error');
                updateStatus('❌ Error', error.message);
            }
        }

        async function startCall() {
            if (!credentials) {
                log('❌ No credentials', 'error');
                return;
            }

            log('Connecting to LiveKit...', 'info');
            updateStatus('⏳ Connecting', 'Setting up voice connection...');

            try {
                room = new LiveKit.Room();

                room.on(LiveKit.RoomEvent.Connected, () => {
                    log('✅ Connected to room!', 'success');
                    updateStatus('🎤 Live!', 'Start speaking now');
                });

                room.on(LiveKit.RoomEvent.TrackSubscribed, (track, publication, participant) => {
                    if (track.kind === LiveKit.Track.Kind.Audio) {
                        log('🔊 Agent audio received!', 'success');
                        const audioElement = track.attach();
                        document.body.appendChild(audioElement);
                        audioElement.play();
                    }
                });

                await room.connect(credentials.livekit_url, credentials.token);
                await room.localParticipant.setMicrophoneEnabled(true);

                log('🎤 Microphone enabled', 'success');
                log('Say: "I want to return my headphones"', 'info');

                document.getElementById('startCall').style.display = 'none';
                document.getElementById('endCall').style.display = 'block';

            } catch (error) {
                log(`❌ Connection error: ${error.message}`, 'error');
                updateStatus('❌ Error', error.message);
            }
        }

        async function endCall() {
            if (room) {
                await room.disconnect();
                room = null;
                log('Call ended', 'info');
                updateStatus('Disconnected', 'Call ended');
                document.getElementById('startCall').style.display = 'block';
                document.getElementById('endCall').style.display = 'none';
            }
        }

        log('Voice test interface loaded', 'success');
    </script>
</body>
</html>'''

def create_app():
    """Create Flask app."""
    app = Flask(__name__)
    client = VocalBridgeClient()

    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)

    @app.route('/api/credentials')
    def get_credentials():
        try:
            creds = client.get_livekit_credentials()
            return jsonify({'success': True, 'data': creds})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    return app

def main():
    if not flask_available:
        print("ERROR: Flask is not installed")
        print("Install with: pip install flask")
        return

    print("\n" + "="*70)
    print("  VOCAL BRIDGE VOICE TEST")
    print("="*70 + "\n")
    print("✅ Starting server on http://localhost:5000")
    print()
    print("The browser will open automatically...")
    print()
    print("INSTRUCTIONS:")
    print("  1. Click 'Step 1: Get Credentials'")
    print("  2. Click 'Step 2: Start Voice Call'")
    print("  3. Allow microphone access")
    print("  4. Say: 'I want to return my headphones to Amazon'")
    print()
    print("Press Ctrl+C to stop")
    print()

    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')

    threading.Thread(target=open_browser, daemon=True).start()

    app = create_app()
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    main()
