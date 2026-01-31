#!/usr/bin/env python3
"""
Vocal Bridge Voice Test Server - Fixed LiveKit SDK loading
Port: 5040
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

from flask import Flask, jsonify, render_template_string
from services.vocalbridge_livekit_client import VocalBridgeClient
import webbrowser
import threading
import time

# HTML with properly loaded LiveKit SDK
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocal Bridge Voice Test</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            max-width: 700px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 32px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .status {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }

        .status h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 20px;
        }

        .status p {
            color: #666;
            font-size: 14px;
        }

        button {
            width: 100%;
            padding: 18px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px 0;
            transition: all 0.3s ease;
        }

        button:hover:not(:disabled) {
            transform: translateY(-2px);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        #getCredentials {
            background: #667eea;
            color: white;
        }

        #getCredentials:hover:not(:disabled) {
            background: #5568d3;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        #startCall {
            background: #4CAF50;
            color: white;
            display: none;
        }

        #startCall:hover:not(:disabled) {
            background: #45a049;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }

        #endCall {
            background: #f44336;
            color: white;
            display: none;
        }

        #endCall:hover:not(:disabled) {
            background: #da190b;
            box-shadow: 0 5px 15px rgba(244, 67, 54, 0.4);
        }

        .log {
            background: #2d3748;
            color: #a0aec0;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.8;
        }

        .log-entry {
            margin: 5px 0;
            padding: 3px 0;
        }

        .log-time {
            color: #718096;
        }

        .log-success {
            color: #48bb78;
        }

        .log-error {
            color: #f56565;
        }

        .log-info {
            color: #4299e1;
        }

        .log-warning {
            color: #ed8936;
        }

        .sdk-status {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 12px;
            margin: 15px 0;
            font-size: 13px;
            text-align: center;
        }

        .sdk-loaded {
            background: #d4edda;
            border-color: #28a745;
            color: #155724;
        }

        .sdk-loading {
            background: #cce5ff;
            border-color: #007bff;
            color: #004085;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Vocal Bridge Voice Test</h1>
        <p class="subtitle">Live Voice Agent Testing</p>

        <div class="sdk-status" id="sdkStatus">
            ⏳ Loading LiveKit SDK...
        </div>

        <div class="status" id="status">
            <h3 id="statusTitle">Initializing</h3>
            <p id="statusMessage">Please wait...</p>
        </div>

        <button id="getCredentials" onclick="getCredentials()" disabled>
            Step 1: Get Credentials
        </button>

        <button id="startCall" onclick="startCall()">
            Step 2: Start Voice Call
        </button>

        <button id="endCall" onclick="endCall()">
            End Call
        </button>

        <div class="log" id="log"></div>
    </div>

    <!-- LiveKit Web SDK - Using specific version known to work -->
    <script src="https://unpkg.com/livekit-client@2.5.9/dist/livekit-client.umd.min.js"></script>

    <script>
        let LiveKit = null;
        let credentials = null;
        let room = null;

        // Wait for SDK to load
        window.addEventListener('load', function() {
            setTimeout(initializeSDK, 500);
        });

        function initializeSDK() {
            log('Checking LiveKit SDK...', 'info');

            if (typeof window.LiveKitClient !== 'undefined') {
                LiveKit = window.LiveKitClient;
                log('✅ LiveKit SDK loaded successfully!', 'success');
                document.getElementById('sdkStatus').textContent = '✅ LiveKit SDK Ready';
                document.getElementById('sdkStatus').className = 'sdk-status sdk-loaded';

                document.getElementById('getCredentials').disabled = false;
                updateStatus('✅ Ready', 'Click "Get Credentials" to start');
            } else {
                log('❌ LiveKit SDK failed to load', 'error');
                document.getElementById('sdkStatus').textContent = '❌ LiveKit SDK Failed to Load';
                document.getElementById('sdkStatus').style.borderColor = '#dc3545';
                document.getElementById('sdkStatus').style.background = '#f8d7da';
                document.getElementById('sdkStatus').style.color = '#721c24';

                updateStatus('❌ Error', 'SDK failed to load. Please refresh.');

                // Try loading again after 2 seconds
                log('Retrying SDK load in 2 seconds...', 'warning');
                setTimeout(initializeSDK, 2000);
            }
        }

        function log(message, type = 'info') {
            const logDiv = document.getElementById('log');
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';

            const typeClass = `log-${type}`;
            entry.innerHTML = `<span class="log-time">[${time}]</span> <span class="${typeClass}">${message}</span>`;

            logDiv.appendChild(entry);
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function updateStatus(title, message) {
            document.getElementById('statusTitle').textContent = title;
            document.getElementById('statusMessage').textContent = message;
        }

        async function getCredentials() {
            log('Requesting credentials from backend...', 'info');
            updateStatus('⏳ Loading', 'Getting LiveKit credentials...');

            const btn = document.getElementById('getCredentials');
            btn.disabled = true;
            btn.textContent = 'Loading...';

            try {
                const response = await fetch('/api/credentials');
                const data = await response.json();

                if (!data.success) {
                    throw new Error(data.error || 'Failed to get credentials');
                }

                credentials = data.data;

                log('✅ Credentials received!', 'success');
                log(`LiveKit URL: ${credentials.livekit_url}`, 'info');
                log(`Room: ${credentials.room_name}`, 'info');
                log(`Expires in: ${credentials.expires_in} seconds`, 'info');

                btn.style.display = 'none';
                document.getElementById('startCall').style.display = 'block';

                updateStatus('✅ Ready to Connect', 'Click "Start Voice Call"');

            } catch (error) {
                log(`❌ Error: ${error.message}`, 'error');
                updateStatus('❌ Error', error.message);
                btn.disabled = false;
                btn.textContent = 'Step 1: Get Credentials (Retry)';
            }
        }

        async function startCall() {
            if (!credentials) {
                log('❌ No credentials available', 'error');
                return;
            }

            if (!LiveKit) {
                log('❌ LiveKit SDK not loaded', 'error');
                updateStatus('❌ Error', 'SDK not loaded. Please refresh.');
                return;
            }

            log('Starting voice call...', 'info');
            updateStatus('⏳ Connecting', 'Connecting to LiveKit room...');

            const btn = document.getElementById('startCall');
            btn.disabled = true;
            btn.textContent = 'Connecting...';

            try {
                // Create new room
                room = new LiveKit.Room();
                log('✅ LiveKit Room object created', 'success');

                // Set up event handlers
                room.on(LiveKit.RoomEvent.Connected, () => {
                    log('✅ Connected to LiveKit room!', 'success');
                    updateStatus('🎤 Connected', 'Setting up microphone...');
                });

                room.on(LiveKit.RoomEvent.Disconnected, () => {
                    log('⚠️  Disconnected from room', 'warning');
                    updateStatus('Disconnected', 'Call ended');
                    document.getElementById('startCall').style.display = 'block';
                    document.getElementById('endCall').style.display = 'none';
                });

                room.on(LiveKit.RoomEvent.TrackSubscribed, (track, publication, participant) => {
                    log(`📡 Track subscribed: ${track.kind} from ${participant.identity}`, 'info');

                    if (track.kind === LiveKit.Track.Kind.Audio) {
                        log('🔊 Agent audio track received!', 'success');
                        log('You should now hear the agent speak!', 'success');

                        const audioElement = track.attach();
                        document.body.appendChild(audioElement);

                        audioElement.play()
                            .then(() => log('▶️  Audio playback started', 'success'))
                            .catch(e => log(`⚠️  Audio play error: ${e.message}`, 'warning'));
                    }
                });

                room.on(LiveKit.RoomEvent.ParticipantConnected, (participant) => {
                    log(`👤 Participant joined: ${participant.identity}`, 'info');
                });

                room.on(LiveKit.RoomEvent.DataReceived, (payload, participant) => {
                    try {
                        const message = new TextDecoder().decode(payload);
                        log(`💬 Message: ${message}`, 'info');
                    } catch (e) {
                        log(`📨 Data received from ${participant.identity}`, 'info');
                    }
                });

                // Connect to room
                log('Connecting to LiveKit room...', 'info');
                await room.connect(credentials.livekit_url, credentials.token);

                log('✅ Connected! Enabling microphone...', 'success');

                // Enable microphone
                await room.localParticipant.setMicrophoneEnabled(true);

                log('🎤 Microphone enabled!', 'success');
                log('', 'info');
                log('🗣️  START SPEAKING NOW!', 'success');
                log('Say: "I want to return my headphones to Amazon"', 'info');
                log('', 'info');

                updateStatus('✅ LIVE!', 'Start speaking to the agent now');

                btn.style.display = 'none';
                document.getElementById('endCall').style.display = 'block';

            } catch (error) {
                log(`❌ Connection error: ${error.message}`, 'error');
                console.error('Full error:', error);
                updateStatus('❌ Connection Failed', error.message);
                btn.disabled = false;
                btn.textContent = 'Step 2: Start Voice Call (Retry)';
            }
        }

        async function endCall() {
            if (room) {
                log('Ending call...', 'info');
                await room.disconnect();
                room = null;

                log('✅ Call ended', 'success');
                updateStatus('Disconnected', 'Call ended successfully');

                document.getElementById('startCall').style.display = 'block';
                document.getElementById('startCall').disabled = false;
                document.getElementById('startCall').textContent = 'Step 2: Start Voice Call';
                document.getElementById('endCall').style.display = 'none';
            }
        }

        // Initial log
        log('Voice test interface loaded', 'success');
        log('Waiting for LiveKit SDK...', 'info');
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

    @app.route('/api/test')
    def test():
        return jsonify({'status': 'ok', 'server': 'vocal-bridge-test'})

    return app

def main():
    PORT = 5040

    print("\n" + "="*70)
    print("  VOCAL BRIDGE VOICE TEST SERVER")
    print("="*70 + "\n")
    print(f"✅ Starting server on http://localhost:{PORT}")
    print()
    print("🌐 Browser will open automatically...")
    print()
    print("="*70)
    print("  INSTRUCTIONS")
    print("="*70)
    print()
    print("1️⃣  Wait for LiveKit SDK to load (should show ✅)")
    print("2️⃣  Click 'Step 1: Get Credentials'")
    print("3️⃣  Click 'Step 2: Start Voice Call'")
    print("4️⃣  Allow microphone when prompted")
    print("5️⃣  Start speaking: 'I want to return my headphones to Amazon'")
    print()
    print("Watch the log at bottom for detailed status updates!")
    print()
    print("="*70)
    print()
    print("Press Ctrl+C to stop the server")
    print()

    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f'http://localhost:{PORT}')

    threading.Thread(target=open_browser, daemon=True).start()

    app = create_app()
    app.run(debug=False, port=PORT, use_reloader=False)

if __name__ == '__main__':
    main()
