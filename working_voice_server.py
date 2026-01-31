#!/usr/bin/env python3
"""
Working Voice Test Server - Serves LiveKit SDK locally
No external CDN dependencies - everything served from localhost
Port: 5040
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

from flask import Flask, jsonify, render_template_string, send_from_directory
from services.vocalbridge_livekit_client import VocalBridgeClient
import webbrowser
import threading
import time
import os

app = Flask(__name__, static_folder='static')

# HTML with local LiveKit SDK
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
        h1 { color: #667eea; text-align: center; margin-bottom: 10px; font-size: 32px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }
        .status {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .status h3 { color: #333; margin-bottom: 10px; font-size: 20px; }
        .status p { color: #666; font-size: 14px; }
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
        button:hover:not(:disabled) { transform: translateY(-2px); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        #getCredentials { background: #667eea; color: white; }
        #getCredentials:hover:not(:disabled) { background: #5568d3; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        #startCall { background: #4CAF50; color: white; display: none; }
        #startCall:hover:not(:disabled) { background: #45a049; box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4); }
        #endCall { background: #f44336; color: white; display: none; }
        #endCall:hover:not(:disabled) { background: #da190b; box-shadow: 0 5px 15px rgba(244, 67, 54, 0.4); }
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
        .log-entry { margin: 5px 0; padding: 3px 0; }
        .log-time { color: #718096; }
        .log-success { color: #48bb78; }
        .log-error { color: #f56565; }
        .log-info { color: #4299e1; }
        .log-warning { color: #ed8936; }
        .sdk-status {
            background: #d4edda;
            border: 2px solid #28a745;
            border-radius: 8px;
            padding: 12px;
            margin: 15px 0;
            font-size: 13px;
            text-align: center;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Vocal Bridge Voice Test</h1>
        <p class="subtitle">Live Voice Agent Testing</p>

        <div class="sdk-status" id="sdkStatus">
            ✅ LiveKit SDK Loaded (Local)
        </div>

        <div class="status" id="status">
            <h3 id="statusTitle">Ready</h3>
            <p id="statusMessage">Click "Get Credentials" to start</p>
        </div>

        <button id="getCredentials" onclick="getCredentials()">
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

    <!-- LiveKit SDK loaded from local server -->
    <script src="/static/livekit-client.js"></script>

    <script>
        // Debug: Log what the SDK exports
        console.log('=== LiveKit SDK Debug ===');
        console.log('window.LiveKitClient:', typeof window.LiveKitClient);
        console.log('window.LivekitClient:', typeof window.LivekitClient);
        console.log('window.LiveKit:', typeof window.LiveKit);
        console.log('window.livekit:', typeof window.livekit);
        console.log('Properties containing "live":',
            Object.keys(window).filter(k => k.toLowerCase().includes('live')));
        console.log('Properties containing "kit":',
            Object.keys(window).filter(k => k.toLowerCase().includes('kit')));
        console.log('========================');

        // SDK exports as LivekitClient (lowercase 'k')
        const LiveKit = window.LivekitClient;
        let credentials = null;
        let room = null;

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

        // Check if SDK loaded
        if (typeof LiveKit === 'undefined') {
            log('❌ ERROR: LiveKit SDK failed to load!', 'error');
            log('Check browser console for SDK export debug info', 'warning');

            // Log which variables we checked
            const checked = [
                `LiveKitClient: ${typeof window.LiveKitClient}`,
                `LivekitClient: ${typeof window.LivekitClient}`,
                `LiveKit: ${typeof window.LiveKit}`,
                `livekit: ${typeof window.livekit}`
            ];
            log(`Checked: ${checked.join(', ')}`, 'info');

            document.getElementById('sdkStatus').style.background = '#f8d7da';
            document.getElementById('sdkStatus').style.borderColor = '#dc3545';
            document.getElementById('sdkStatus').style.color = '#721c24';
            document.getElementById('sdkStatus').textContent = '❌ LiveKit SDK Failed - Check Console';
            updateStatus('Error', 'SDK not loaded - check browser console (F12)');
        } else {
            log('✅ LiveKit SDK loaded successfully!', 'success');
            log(`SDK Version: ${LiveKit.version || 'unknown'}`, 'info');
            log(`Export type: ${Object.keys(window).find(k => window[k] === LiveKit)}`, 'info');
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

            if (typeof LiveKit === 'undefined') {
                log('❌ LiveKit SDK not available', 'error');
                alert('LiveKit SDK failed to load. Please refresh the page.');
                return;
            }

            log('Starting voice call...', 'info');
            updateStatus('⏳ Connecting', 'Connecting to LiveKit room...');

            const btn = document.getElementById('startCall');
            btn.disabled = true;
            btn.textContent = 'Connecting...';

            try {
                room = new LiveKit.Room();
                log('✅ LiveKit Room created', 'success');

                room.on(LiveKit.RoomEvent.Connected, () => {
                    log('✅ Connected to LiveKit room!', 'success');
                    updateStatus('🎤 Connected', 'Microphone starting...');
                });

                room.on(LiveKit.RoomEvent.Disconnected, () => {
                    log('⚠️  Disconnected from room', 'warning');
                    updateStatus('Disconnected', 'Call ended');
                    document.getElementById('startCall').style.display = 'block';
                    document.getElementById('endCall').style.display = 'none';
                });

                room.on(LiveKit.RoomEvent.TrackSubscribed, (track, publication, participant) => {
                    log(`📡 Track: ${track.kind} from ${participant.identity}`, 'info');

                    if (track.kind === LiveKit.Track.Kind.Audio) {
                        log('🔊 AGENT AUDIO RECEIVED!', 'success');
                        log('You should hear the agent speaking!', 'success');

                        const audioElement = track.attach();
                        document.body.appendChild(audioElement);
                        audioElement.play()
                            .then(() => log('▶️  Audio playing', 'success'))
                            .catch(e => log(`⚠️  Audio error: ${e.message}`, 'warning'));
                    }
                });

                room.on(LiveKit.RoomEvent.ParticipantConnected, (participant) => {
                    log(`👤 Participant: ${participant.identity}`, 'info');
                });

                log('Connecting to room...', 'info');
                await room.connect(credentials.livekit_url, credentials.token);

                log('✅ Connected! Enabling mic...', 'success');
                await room.localParticipant.setMicrophoneEnabled(true);

                log('', 'info');
                log('🎤 MICROPHONE ACTIVE!', 'success');
                log('🗣️  START SPEAKING NOW!', 'success');
                log('', 'info');
                log('Say: "I want to return my headphones to Amazon"', 'info');

                updateStatus('✅ LIVE!', 'Start speaking to the agent');

                btn.style.display = 'none';
                document.getElementById('endCall').style.display = 'block';

            } catch (error) {
                log(`❌ Error: ${error.message}`, 'error');
                console.error('Full error:', error);
                updateStatus('❌ Failed', error.message);
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
                updateStatus('Disconnected', 'Call ended');
                document.getElementById('startCall').style.display = 'block';
                document.getElementById('startCall').disabled = false;
                document.getElementById('startCall').textContent = 'Step 2: Start Voice Call';
                document.getElementById('endCall').style.display = 'none';
            }
        }

        log('Voice test interface ready', 'success');
        log('LiveKit loaded from local server', 'info');
    </script>
</body>
</html>'''

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

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def main():
    PORT = 5040

    print("\n" + "="*70)
    print("  VOCAL BRIDGE VOICE TEST - WORKING VERSION")
    print("="*70 + "\n")

    # Check if LiveKit SDK exists
    sdk_path = os.path.join('static', 'livekit-client.js')
    if not os.path.exists(sdk_path):
        print("❌ Error: LiveKit SDK not found at static/livekit-client.js")
        print("   Please run the script from /Users/sankar/projects/voice_agent/")
        return

    sdk_size = os.path.getsize(sdk_path)
    print(f"✅ LiveKit SDK found: {sdk_size:,} bytes")
    print()
    print(f"🚀 Starting server on http://localhost:{PORT}")
    print()
    print("="*70)
    print("  TESTING STEPS")
    print("="*70)
    print()
    print("1️⃣  Click 'Get Credentials'")
    print("2️⃣  Click 'Start Voice Call'")
    print("3️⃣  Allow microphone")
    print("4️⃣  Say: 'I want to return my headphones to Amazon'")
    print()
    print("="*70)
    print()
    print("Press Ctrl+C to stop")
    print()

    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f'http://localhost:{PORT}')

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=False, port=PORT, use_reloader=False)

if __name__ == '__main__':
    main()
