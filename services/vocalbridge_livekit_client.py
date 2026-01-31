"""
Vocal Bridge + LiveKit Client Integration

Vocal Bridge uses LiveKit for real-time voice communication.
This client connects to Vocal Bridge agents via LiveKit rooms.
"""

import requests
import asyncio
from typing import Optional, Callable
from config import config


class VocalBridgeClient:
    """
    Client for Vocal Bridge voice agents using LiveKit.

    Vocal Bridge architecture:
    1. Use API key to get LiveKit credentials
    2. Connect to LiveKit room with those credentials
    3. Agent automatically joins and handles conversation
    4. Audio streams bidirectionally through LiveKit
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Vocal Bridge client.

        Args:
            api_key: Vocal Bridge API key (vb_xxx format)
        """
        self.api_key = api_key or config.vocalbridge_api_key
        self.endpoint = "https://vocalbridgeai.com/api/v1"

        if not self.api_key:
            raise ValueError(
                "Vocal Bridge API key not found. "
                "Please set VOCALBRIDGE_API_KEY in .env file"
            )

        self.livekit_url: Optional[str] = None
        self.livekit_token: Optional[str] = None
        self.room_name: Optional[str] = None
        self.participant_identity: Optional[str] = None

    def get_livekit_credentials(self) -> dict:
        """
        Get LiveKit connection credentials from Vocal Bridge.

        Returns:
            dict with keys: livekit_url, token, room_name, participant_identity

        Example:
            >>> client = VocalBridgeClient()
            >>> creds = client.get_livekit_credentials()
            >>> print(creds['livekit_url'])
            wss://tutor-j7bhwjbm.livekit.cloud
        """
        try:
            response = requests.post(
                f"{self.endpoint}/token",
                headers={
                    'X-API-Key': self.api_key,
                    'Content-Type': 'application/json'
                },
                json={},  # Empty body - uses default agent config
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            # Store credentials
            self.livekit_url = data['livekit_url']
            self.livekit_token = data['token']
            self.room_name = data['room_name']
            self.participant_identity = data['participant_identity']

            return {
                'livekit_url': self.livekit_url,
                'token': self.livekit_token,
                'room_name': self.room_name,
                'participant_identity': self.participant_identity,
                'expires_in': data.get('expires_in', 3600),
                'agent_mode': data.get('agent_mode', 'unknown')
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get LiveKit credentials: {e}")

    async def connect_to_room(
        self,
        on_agent_response: Optional[Callable[[str], None]] = None,
        on_agent_speaking: Optional[Callable[[bool], None]] = None
    ):
        """
        Connect to LiveKit room and interact with voice agent.

        This requires the livekit SDK. Install with:
            pip install livekit

        Args:
            on_agent_response: Callback when agent responds (receives transcript)
            on_agent_speaking: Callback when agent speaking state changes

        Example:
            >>> async def on_response(text):
            ...     print(f"Agent: {text}")
            >>>
            >>> client = VocalBridgeClient()
            >>> await client.connect_to_room(on_agent_response=on_response)
        """
        try:
            from livekit import rtc
        except ImportError:
            raise ImportError(
                "LiveKit SDK required for voice connections. "
                "Install with: pip install livekit"
            )

        # Get credentials if not already fetched
        if not self.livekit_url:
            self.get_livekit_credentials()

        # Create LiveKit room
        room = rtc.Room()

        # Set up event handlers
        @room.on("track_subscribed")
        def on_track_subscribed(
            track: rtc.Track,
            publication: rtc.RemoteTrackPublication,
            participant: rtc.RemoteParticipant
        ):
            """Handle incoming audio from the agent."""
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                # Audio from agent - can play it or process it
                print(f"Receiving audio from agent: {participant.identity}")

                if on_agent_speaking:
                    on_agent_speaking(True)

        @room.on("data_received")
        def on_data_received(data: rtc.DataPacket):
            """Handle data messages (transcripts, etc.) from agent."""
            try:
                message = data.decode('utf-8')
                print(f"Agent message: {message}")

                if on_agent_response:
                    on_agent_response(message)
            except Exception as e:
                print(f"Error processing data: {e}")

        # Connect to the room
        print(f"Connecting to room: {self.room_name}")
        await room.connect(self.livekit_url, self.livekit_token)
        print("✅ Connected to Vocal Bridge agent!")

        return room

    def create_web_integration_html(self, output_file: str = "vocalbridge_demo.html"):
        """
        Generate HTML file with Vocal Bridge web integration.

        This creates a ready-to-use web page that connects to your agent.
        Uses LiveKit Web SDK in the browser.

        Args:
            output_file: Path to save HTML file
        """
        # Get credentials
        creds = self.get_livekit_credentials()

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReturnFlow Voice Agent</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        button {{
            width: 100%;
            padding: 20px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px 0;
            transition: all 0.3s;
        }}
        #startCall {{
            background: #4CAF50;
            color: white;
        }}
        #startCall:hover {{
            background: #45a049;
        }}
        #endCall {{
            background: #f44336;
            color: white;
            display: none;
        }}
        #endCall:hover {{
            background: #da190b;
        }}
        #status {{
            text-align: center;
            padding: 20px;
            margin: 20px 0;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }}
        #transcript {{
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 20px;
        }}
        .message {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }}
        .user {{
            background: rgba(100, 126, 234, 0.3);
            text-align: right;
        }}
        .agent {{
            background: rgba(76, 175, 80, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ ReturnFlow Voice Agent</h1>

        <div id="status">
            <h3>Ready to connect</h3>
            <p>Click "Start Call" to begin voice conversation</p>
        </div>

        <button id="startCall">Start Call</button>
        <button id="endCall">End Call</button>

        <div id="transcript">
            <h3>Conversation Transcript</h3>
        </div>
    </div>

    <!-- LiveKit Web SDK -->
    <script src="https://unpkg.com/livekit-client@latest/dist/livekit-client.umd.min.js"></script>

    <script>
        const LiveKit = window.LiveKitClient;

        // Vocal Bridge credentials
        const LIVEKIT_URL = "{creds['livekit_url']}";
        const TOKEN = "{creds['token']}";
        const ROOM_NAME = "{creds['room_name']}";

        let room = null;
        let localAudioTrack = null;

        // UI elements
        const startBtn = document.getElementById('startCall');
        const endBtn = document.getElementById('endCall');
        const status = document.getElementById('status');
        const transcript = document.getElementById('transcript');

        // Update status
        function updateStatus(title, message) {{
            status.innerHTML = `<h3>${{title}}</h3><p>${{message}}</p>`;
        }}

        // Add message to transcript
        function addMessage(speaker, text) {{
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${{speaker}}`;
            msgDiv.innerHTML = `<strong>${{speaker === 'user' ? 'You' : 'Agent'}}:</strong> ${{text}}`;
            transcript.appendChild(msgDiv);
            transcript.scrollTop = transcript.scrollHeight;
        }}

        // Start call
        startBtn.addEventListener('click', async () => {{
            try {{
                updateStatus('Connecting...', 'Setting up voice connection');

                // Create new room
                room = new LiveKit.Room();

                // Handle agent audio
                room.on(LiveKit.RoomEvent.TrackSubscribed, (track, publication, participant) => {{
                    if (track.kind === LiveKit.Track.Kind.Audio) {{
                        const audioElement = track.attach();
                        document.body.appendChild(audioElement);
                        updateStatus('🎤 Connected', 'Agent is ready - start speaking!');
                    }}
                }});

                // Handle messages/transcripts
                room.on(LiveKit.RoomEvent.DataReceived, (payload, participant) => {{
                    const message = new TextDecoder().decode(payload);
                    addMessage('agent', message);
                }});

                // Connect to room
                await room.connect(LIVEKIT_URL, TOKEN);

                // Publish microphone
                await room.localParticipant.setMicrophoneEnabled(true);

                updateStatus('✅ Connected!', 'Start speaking to the agent');
                startBtn.style.display = 'none';
                endBtn.style.display = 'block';

                console.log('Connected! Start speaking...');

            }} catch (error) {{
                console.error('Connection error:', error);
                updateStatus('❌ Error', error.message);
            }}
        }});

        // End call
        endBtn.addEventListener('click', async () => {{
            if (room) {{
                await room.disconnect();
                room = null;
            }}

            updateStatus('Disconnected', 'Call ended');
            startBtn.style.display = 'block';
            endBtn.style.display = 'none';
        }});
    </script>
</body>
</html>"""

        # Save HTML file
        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"✅ Created web integration: {output_file}")
        print(f"   Open this file in a browser to test voice conversation!")
        print(f"   Room: {creds['room_name']}")
        print(f"   Expires in: {creds['expires_in']} seconds")

        return output_file


def get_vocalbridge_client() -> VocalBridgeClient:
    """Get a configured Vocal Bridge client instance."""
    return VocalBridgeClient()


# Example usage
if __name__ == "__main__":
    client = VocalBridgeClient()

    # Test: Get credentials
    print("Testing Vocal Bridge API...")
    creds = client.get_livekit_credentials()

    print("\n✅ Successfully connected to Vocal Bridge!")
    print(f"LiveKit URL: {creds['livekit_url']}")
    print(f"Room Name: {creds['room_name']}")
    print(f"Participant: {creds['participant_identity']}")
    print(f"Agent Mode: {creds['agent_mode']}")
    print(f"Expires in: {creds['expires_in']} seconds")

    # Generate web demo
    print("\n" + "="*70)
    html_file = client.create_web_integration_html()
    print(f"\nOpen {html_file} in your browser to test the voice agent!")
